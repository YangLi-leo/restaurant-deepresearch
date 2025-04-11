"""Main functionality for restaurant_deep_research."""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Optional
import os

from camel.agents import ChatAgent
from camel.configs import GeminiConfig
from camel.toolkits import MCPToolkit, FunctionTool
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelType, ModelPlatformType
from camel.utils import print_text_animated
from colorama import Fore
from dotenv import load_dotenv

from restaurant_deep_research.agents.role_playing import OwlRolePlaying, arun_society
from restaurant_deep_research.config.prompts import RESTAURANT_CLARIFIER_PROMPT

# Load environment variables
load_dotenv()

def get_default_config_path() -> str:
    """Get the default config path for MCP servers."""
    # First check if it's in the package directory
    package_config_dir = Path(__file__).parent.parent.parent / "config"
    package_config = package_config_dir / "mcp_servers_config.json"
    
    # Get Google Maps API key from environment
    google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    
    if google_maps_api_key:
        # Create or update the config file with the API key from environment
        config_data = {
            "mcpServers": {
                "google-maps": {
                    "command": "npx",
                    "args": [
                        "-y",
                        "@modelcontextprotocol/server-google-maps"
                    ],
                    "env": {
                        "GOOGLE_MAPS_API_KEY": google_maps_api_key
                    }
                }
            }
        }
        
        # Ensure the config directory exists
        package_config_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the config file
        with open(package_config, 'w') as f:
            json.dump(config_data, f, indent=4)
    
    if package_config.exists():
        return str(package_config)
    
    # Fall back to the current directory
    current_dir_config = Path.cwd() / "mcp_servers_config.json"
    if current_dir_config.exists():
        return str(current_dir_config)
    
    raise FileNotFoundError("Could not find mcp_servers_config.json")

async def construct_society(
    question: str,
    tools: List[FunctionTool],
    tool_names: List[str],
) -> OwlRolePlaying:
    """Build a multi-agent OwlRolePlaying instance.

    Args:
        question (str): The question to ask.
        tools (List[FunctionTool]): The MCP tools to use.
        tool_names (List[str]): The names of the available tools.
        
    Returns:
        OwlRolePlaying: The configured society instance.
    """
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.GEMINI,
            model_type=ModelType.GEMINI_2_5_PRO_EXP, 
            model_config_dict=GeminiConfig(temperature=0.3).as_dict(),
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.GEMINI,
            model_type=ModelType.GEMINI_2_5_PRO_EXP, # Highly recommend use some really strong reansoning and tool-calling model, that will make the result solid.
            model_config_dict=GeminiConfig(temperature=0.4).as_dict(),
        ),
    }

    # Modify the question to include the available tools
    question_with_tools = f"{question}\n\nNOTE: Only the following Google Maps tools are available: {', '.join(tool_names)}. Do not try to use any other tools like search_web, search_google, etc."
    
    # Use only MCP tools
    all_tools = tools

    user_agent_kwargs = {"model": models["user"]}
    assistant_agent_kwargs = {
        "model": models["assistant"],
        "tools": all_tools,
    }

    task_kwargs = {
        "task_prompt": question_with_tools,
        "with_task_specify": False,
    }

    society = OwlRolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
    )
    return society

async def process_restaurant_query(
    query: Optional[str] = None, 
    config_path: Optional[str] = None,
    chat_turn_limit: int = 10,
    verbose: bool = True
) -> str:
    """Process a restaurant query using multi-agent conversation.
    
    Args:
        query (str, optional): The restaurant query. Defaults to a sample query.
        config_path (str, optional): Path to MCP config. Defaults to looking in package directory.
        chat_turn_limit (int, optional): Maximum conversation turns. Defaults to 10.
        verbose (bool, optional): Whether to print detailed output. Defaults to True.
        
    Returns:
        str: The final response from the assistant.
    """
    # Create a single model instance to fully understand the needs from user and translate into markdown format to make models easy to understand.
    model = ModelFactory.create(
        model_platform=ModelPlatformType.GEMINI,
        model_type=ModelType.GEMINI_2_5_PRO_EXP, # Hah, you know why you should use a solid model here.
        model_config_dict=GeminiConfig(temperature=0.2).as_dict(),
    )

    # Use default query if none provided
    if query is None:
        query = "I'm looking for a casual yet authentic Japanese restaurant near Shibuya Station in Tokyo for dinner tonight. My budget is around ¥2,000–¥4,000, and I'm interested in sushi, ramen, or izakaya-style dishes. It should have good local reviews, an enjoyable atmosphere, and not be too fancy. Please recommend a few options."

    # Process the query
    md_task_sys_msg = BaseMessage.make_user_message(
        role_name="Request Clarifier",
        content=RESTAURANT_CLARIFIER_PROMPT,
    )
    md_agent = ChatAgent(md_task_sys_msg, model)
    md_agent.reset()
    
    response = md_agent.step(query)
    if verbose:
        print("Initial response:", response)

    # Initialize MCP toolkit with Google Maps
    config_path = config_path or get_default_config_path()
    mcp_toolkit = MCPToolkit(config_path=config_path)

    try:
        await mcp_toolkit.connect()
        default_task = response
        task = default_task

        # Connect to MCP servers
        tools = mcp_toolkit.get_tools()
        tool_names = [tool.get_function_name() for tool in tools]
        
        if verbose:
            print("Available MCP tools:", tool_names)
        
        society = await construct_society(task, tools, tool_names)
        
        if verbose:
            print(Fore.GREEN + f"AI Assistant sys message:\n{society.assistant_sys_msg}\n")
            print(Fore.BLUE + f"AI User sys message:\n{society.user_sys_msg}\n")
            print(Fore.YELLOW + f"Original task prompt:\n{task}\n")
        
        # Start the conversation loop
        n = 0
        input_msg = society.init_chat()
        final_response = None

        while n < chat_turn_limit:
            n += 1
            assistant_response, user_response = await society.astep(input_msg)

            if assistant_response.terminated:
                if verbose:
                    print(
                        Fore.GREEN
                        + (
                            "AI Assistant terminated. Reason: "
                            f"{assistant_response.info['termination_reasons']}."
                        )
                    )
                break
                
            if user_response.terminated:
                if verbose:
                    print(
                        Fore.GREEN
                        + (
                            "AI User terminated. "
                            f"Reason: {user_response.info['termination_reasons']}."
                        )
                    )
                break

            if verbose:
                print_text_animated(
                    Fore.BLUE + f"AI User:\n\n{user_response.msg.content}\n"
                )

            if "TASK_DONE" in user_response.msg.content:
                final_response = assistant_response.msg.content
                break

            if verbose:
                print_text_animated(
                    Fore.GREEN + "AI Assistant:\n\n"
                    f"{assistant_response.msg.content}\n"
                )

            input_msg = assistant_response.msg
            
        return final_response or assistant_response.msg.content

    finally:
        # Make sure to disconnect safely after all operations are completed.
        try:
            await mcp_toolkit.disconnect()
        except Exception:
            if verbose:
                print("Disconnect failed")

async def main():
    """Main entry point for the application."""
    result = await process_restaurant_query()
    print("\nFinal Result:")
    print("=" * 50)
    print(result)
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
