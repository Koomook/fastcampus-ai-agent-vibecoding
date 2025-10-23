"""MCP Client for Playwright server communication."""

import asyncio
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from .config import Config


class PlaywrightMCPClient:
    """MCP Client for communicating with Playwright server."""

    def __init__(self, config: Config):
        """Initialize MCP client.

        Args:
            config: Configuration object.
        """
        self.config = config
        self.session: ClientSession | None = None
        self._stdio_context = None
        self._read = None
        self._write = None

    async def connect(self) -> None:
        """Connect to Playwright MCP server."""
        # Parse server args (split by space if multiple args)
        server_args = self.config.playwright_server_args.split()

        # Create server parameters
        server_params = StdioServerParameters(
            command=self.config.playwright_server_path,
            args=server_args,
            env=None,
        )

        # Connect to server via stdio
        self._stdio_context = stdio_client(server_params)
        self._read, self._write = await self._stdio_context.__aenter__()

        # Initialize session
        self.session = ClientSession(self._read, self._write)
        await self.session.__aenter__()

        # Initialize the session
        await self.session.initialize()

    async def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self.session:
            await self.session.__aexit__(None, None, None)
            self.session = None

        if self._stdio_context:
            await self._stdio_context.__aexit__(None, None, None)
            self._stdio_context = None

    async def list_tools(self) -> list[Any]:
        """List available tools from MCP server.

        Returns:
            List of available tools.

        Raises:
            RuntimeError: If not connected to server.
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call.
            arguments: Arguments to pass to the tool.

        Returns:
            Tool execution result.

        Raises:
            RuntimeError: If not connected to server.
        """
        if not self.session:
            raise RuntimeError("Not connected to MCP server")

        result = await self.session.call_tool(tool_name, arguments)
        return result

    async def __aenter__(self) -> "PlaywrightMCPClient":
        """Context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        await self.disconnect()
