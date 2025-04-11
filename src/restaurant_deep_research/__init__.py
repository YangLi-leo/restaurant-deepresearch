"""
Restaurant Deep Research - A multi-agent system for restaurant recommendations.

This package provides tools for finding restaurant recommendations using
a multi-agent conversation system built on the CAMEL framework and
Google Maps integration via MCP servers.
"""

__version__ = "0.1.0"

# Import main functionality to expose at the package level
from restaurant_deep_research.main import process_restaurant_query, construct_society
from restaurant_deep_research.agents import OwlRolePlaying, arun_society

# Define what gets imported with "from restaurant_finder import *"
__all__ = [
    "process_restaurant_query",
    "construct_society",
    "OwlRolePlaying",
    "arun_society",
]