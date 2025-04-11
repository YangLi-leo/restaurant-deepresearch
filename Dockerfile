FROM python:3.12-slim

WORKDIR /app

# Copy only files needed for dependency installation first
COPY README.md ./
COPY setup.py ./
COPY src/ ./src/
# If you had a requirements.txt, you'd copy it here too

# Install build tools needed for some dependencies (like psutil)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -e .

# Now copy the rest of the application code
COPY . .
# This includes examples/, config/, etc.

# Copy and set up the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 
# Note: The application will automatically use the GOOGLE_MAPS_API_KEY environment variable
# for both the Python application and the MCP server. You no longer need to manually edit
# the config/mcp_servers_config.json file.

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run when container starts (passed to entrypoint)
CMD ["python", "examples/restaurant_search.py"]
