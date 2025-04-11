# Restaurant Deep Research

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/get-started)

Restaurant Deep Research is a sophisticated multi-agent system for finding and analyzing restaurant recommendations. It leverages the CAMEL-AI framework and Google Maps MCP Server integration to provide detailed, context-aware restaurant suggestions based on natural language queries.

## Quick Start

1. **Prerequisites**: 
   - Docker installed
   - Google Maps API key ([Get it here](https://console.cloud.google.com/google/maps-apis/credentials))
   - Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

2. **Clone & Build**:
   ```bash
   git clone https://github.com/YangLi-leo/restaurant-deepresearch
   cd restaurant_deep_research
   docker build -t restaurant-research .
   ```

3. **Run**:
   ```bash
   docker run -e GEMINI_API_KEY=your_key -e GOOGLE_MAPS_API_KEY=your_key restaurant-research
   ```

## Features

- **Multi-Agent Architecture**: Utilizes a society of AI agents that collaborate to understand and process restaurant queries
- **Natural Language Understanding**: Process queries in plain language about restaurant preferences
- **Contextual Recommendations**: Considers location, cuisine type, budget, atmosphere, and other preferences
- **Google Maps MCP Server Integration**: Accesses real restaurant data through the Google Maps MCP Server
- **Detailed Analysis**: Provides structured information about recommended restaurants
- **Asynchronous Processing**: Built with modern async Python for efficient processing

## Usage (Docker Required)

This project is designed to be run using Docker, which handles all dependencies and setup.

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- The Docker image includes Node.js, npm, and npx, which are required for the Google Maps MCP server

### API Keys Setup

#### Google Maps API Key
1. Go to the [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/credentials)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Geocoding API
   - Places API
   - Maps JavaScript API
4. Create an API key and copy it
5. Set usage restrictions if needed (recommended for production)

#### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key or use an existing one
3. Note that Gemini API has usage quotas:
   - Free tier: Limited requests per day
   - If you encounter rate limit errors (HTTP 429), consider:
     - Waiting for quota reset
     - Upgrading to a paid tier
     - Switching to Gemini 2.5 Pro Preview model when it's possible(see Troubleshooting section)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YangLi-leo/restaurant-deepresearch
    cd restaurant_deep_research
    ```
2.  **Build the Docker image:**
    ```bash
    docker build -t restaurant-research .
    ```
3.  **Run the default example:**
    Replace `your_gemini_key` and `your_maps_key` with your actual API keys.
    ```bash
    docker run \
      -e GEMINI_API_KEY=your_gemini_key \
      -e GOOGLE_MAPS_API_KEY=your_maps_key \
      restaurant-research
    ```
    
    Note: The application will automatically use the GOOGLE_MAPS_API_KEY environment variable for both the Python application and the MCP server. You no longer need to manually edit the config/mcp_servers_config.json file.

### Custom Queries

You can run the application with your own custom restaurant queries:

```bash
docker run \
  -e GEMINI_API_KEY=your_gemini_key \
  -e GOOGLE_MAPS_API_KEY=your_maps_key \
  restaurant-research \
  python -c "import asyncio; from restaurant_deep_research import process_restaurant_query; asyncio.run(process_restaurant_query('Your custom query here'))"
```

#### Example Custom Queries:

1. **Simple query**:
   ```
   I want a vegetarian restaurant in New York with outdoor seating
   ```

2. **Detailed query**:
   ```
   Looking for a family-friendly Italian restaurant in Chicago with a budget of $30-50 per person, preferably with a kids menu and close to downtown
   ```

3. **Complex query**:
   ```
   We are a family of three from China visiting Tokyo for the very first time, and we are planning our trip for early October to enjoy the mild autumn weather and seasonal Japanese specialties. Our family includes two adults and one enthusiastic 6-year-old child. We are seeking an extraordinary dinner experience that embodies the authentic essence of Japanese cuisine and culture, specifically sushi omakase or kaiseki, with a budget of ¥8,000 to ¥15,000 per person in the Asakusa area.
   ```

### Example Output

When you run the application, you'll receive structured restaurant recommendations. Here's a sample output:

```
=== Restaurant Recommendations ===

Based on your request for a casual yet authentic Japanese restaurant near Shibuya Station in Tokyo, I've found several excellent options that match your criteria:

1. **Genki Sushi Shibuya**
   - **Location**: 5-minute walk from Shibuya Station
   - **Price Range**: ¥1,500-3,000 per person
   - **Highlights**: Conveyor belt sushi, touch-panel ordering system, fresh ingredients
   - **Atmosphere**: Casual, lively, popular with locals and tourists
   - **Recommended Dishes**: Salmon nigiri, tuna rolls, tempura

2. **Ichiran Shibuya**
   - **Location**: 7-minute walk from Shibuya Station
   - **Price Range**: ¥1,000-2,000 per person
   - **Highlights**: Famous tonkotsu ramen, individual booths for private dining
   - **Atmosphere**: Focused on the dining experience, minimal distractions
   - **Recommended Dishes**: Classic tonkotsu ramen with customizable spice level

[Additional restaurants would be listed here...]

These restaurants offer excellent value, authentic Japanese flavors, and are conveniently located near Shibuya Station. Each has good reviews from locals and provides an enjoyable dining atmosphere without being overly fancy.
```

## Project Structure

- `src/restaurant_deep_research/`: Main package
  - `agents/`: Multi-agent system implementation
  - `config/`: Configuration and prompts
  - `main.py`: Core functionality
- `examples/`: Example scripts
- `config/`: Configuration files
- `docs/`: Documentation

## Advanced Usage

For advanced usage and customization, you can directly work with the underlying components:

```python
from restaurant_deep_research import construct_society, arun_society
from restaurant_deep_research.agents import OwlRolePlaying

# Custom implementation using the lower-level API
# See examples for more details
```

## Future Blog Posts and Reflections

My homepage is currently under construction, but I will soon update it with thoughts, interesting details, comparisons with other Deep Research tools (such as Manus, OpenAI, Google, and Perplexity), and future directions for this project, multi-agent systems, and related topics. These posts will also document my learning process, challenges, and deeper insights into multi-agent systems that aren’t covered in this README. Once available, I’ll link to them here: https://yangli-leo.github.io/.

## Acknowledgments

This project utilizes the [CAMEL-AI](https://github.com/camel-ai) framework (Apache License 2.0).

## Troubleshooting

### API Key Issues
- Ensure both API keys are valid and have the necessary permissions
- For Google Maps API key, make sure the following APIs are enabled in your Google Cloud project:
  - Geocoding API
  - Places API
  - Maps JavaScript API
- The application automatically configures the MCP server with your Google Maps API key from the environment variable

### Gemini API Rate Limits
If you encounter this error: `Error code: 429 - You exceeded your current quota`, you have options:
1. **Wait for quota reset**: Quotas typically reset daily
2. **Switch to Gemini 2.5 Pro Preview**: Modify the code in `src/restaurant_deep_research/main.py` to use the preview model:
   ```python
   # Change this:
   model_type=ModelType.GEMINI_2_5_PRO_EXP
   
   # To this:
   model_type=ModelType.GEMINI_2_5_PRO_PREVIEW
   ```
3. **Upgrade to a paid tier**: For production use, consider a paid Google AI API plan

### Docker Environment
- The application uses an entrypoint script to ensure environment variables are properly passed to all processes
- The Docker container includes Node.js, npm, and npx for running the Google Maps MCP server
- If you modify the code, rebuild the Docker image with `docker build -t restaurant-research .`

### Common Issues
- **Empty results**: Check that your Google Maps API key has the correct permissions and APIs enabled
- **Slow performance**: The multi-agent conversation may take time, especially for complex queries
- **Connection errors**: Ensure you have internet access and that your firewall isn't blocking connections

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
