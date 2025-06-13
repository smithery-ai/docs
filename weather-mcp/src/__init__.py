"""Weather MCP Server package configuration."""
import os
from typing import Dict, Any
from .weather_server import mcp

# Configuration schema for Smithery
def get_server(config: Dict[str, Any] = None):
    """
    Factory function for Smithery deployment.
    
    Args:
        config: Configuration passed from Smithery
        
    Returns:
        Configured MCP server instance
    """
    # Apply any runtime configuration
    if config:
        # Example: Use custom API endpoint if provided
        if "weather_api_url" in config:
            import weather_server
            weather_server.WEATHER_API = config["weather_api_url"]
    
    return mcp

# For local testing
__all__ = ["mcp", "get_server"]