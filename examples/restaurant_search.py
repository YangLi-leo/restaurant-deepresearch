#!/usr/bin/env python3
"""
Basic example of using the restaurant-finder package.

This example demonstrates how to use the restaurant-finder package to get
restaurant recommendations based on a user query. It shows the basic usage
pattern and how to handle the results.

To run this example:
1. Make sure you have installed the restaurant-finder package
2. Set up your environment variables (GEMINI_API_KEY and GOOGLE_MAPS_API_KEY)
3. Run: python restaurant_search.py
"""

import asyncio
import os
from dotenv import load_dotenv
from restaurant_deep_research import process_restaurant_query

# Load environment variables from .env file
load_dotenv()

# Check if required API keys are available
if not os.getenv("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable is not set.")
    print("Please set it in your .env file or environment variables.")
    exit(1)

if not os.getenv("GOOGLE_MAPS_API_KEY"):
    print("Error: GOOGLE_MAPS_API_KEY environment variable is not set.")
    print("Please set it in your .env file or environment variables.")
    exit(1)


async def main():
    """Run the restaurant search example."""
    print("Restaurant Finder Example")
    print("========================\n")
    
    # Example query - you can modify this or take input from the user
    query = """
    I'm looking for a casual yet authentic Japanese restaurant near Shibuya Station 
    in Tokyo for dinner tonight. My budget is around ¥2,000–¥4,000, and I'm interested 
    in sushi, ramen, or izakaya-style dishes. It should have good local reviews, 
    an enjoyable atmosphere, and not be too fancy.
    """
    
    print(f"Query: {query}\n")
    print("Processing request... (this may take a minute)\n")
    
    try:
        # Process the query and get recommendations
        result = await process_restaurant_query(
            query=query,
            verbose=True  # Set to False to hide detailed processing output
        )
        
        print("\n=== Restaurant Recommendations ===\n")
        print(result)
        print("\n=================================\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your API keys are correct and you have internet access.")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
