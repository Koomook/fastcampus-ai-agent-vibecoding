"""Seoul Cultural Events MCP Server

A Model Context Protocol (MCP) server that provides access to Seoul's cultural events
information through the Seoul Open Data Plaza API.
"""

__version__ = "0.1.0"

from .api_client import SeoulCultureAPIClient
from .server import mcp

__all__ = ["SeoulCultureAPIClient", "mcp"]
