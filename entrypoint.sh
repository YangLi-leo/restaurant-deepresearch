#!/bin/sh
# Basic entrypoint script to execute the command passed as arguments
# Ensures environment variables from `docker run -e` are available

# Execute the command passed to the script (e.g., python examples/restaurant_search.py)
exec "$@"
