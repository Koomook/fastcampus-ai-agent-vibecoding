"""
MCP Client for Notion MCP Server.
Handles stdio communication with external MCP servers.
Phase 3: Notion MCP Integration
"""
import asyncio
import json
import logging
import subprocess
from typing import Any, Optional

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for communicating with MCP servers via stdio."""

    def __init__(self, command: str, args: list[str], env: Optional[dict[str, str]] = None):
        """
        Initialize MCP client.

        Args:
            command: Command to run (e.g., "npx")
            args: Arguments for the command (e.g., ["-y", "@notionhq/notion-mcp-server"])
            env: Environment variables to pass to the subprocess
        """
        self.command = command
        self.args = args
        self.env = env or {}
        self.process: Optional[subprocess.Popen] = None
        self.tools: list[dict[str, Any]] = []
        self._initialized = False

    async def initialize(self):
        """Initialize the MCP server and fetch available tools."""
        if self._initialized:
            return

        try:
            # Start MCP server process
            import os

            full_env = os.environ.copy()
            full_env.update(self.env)

            self.process = subprocess.Popen(
                [self.command] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=full_env,
                text=True,
            )

            # Send initialize request
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "slack-claude-bot", "version": "0.1.0"},
                },
            }

            self._send_request(init_request)

            # Read initialize response
            response = self._read_response()
            logger.info(f"MCP server initialized: {response}")

            # Send initialized notification
            initialized_notification = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }
            self._send_request(initialized_notification)

            # Fetch available tools
            tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

            self._send_request(tools_request)
            tools_response = self._read_response()

            if "result" in tools_response and "tools" in tools_response["result"]:
                self.tools = tools_response["result"]["tools"]
                logger.info(f"Fetched {len(self.tools)} tools from MCP server")

            self._initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize MCP client: {e}")
            self.close()
            raise

    def _send_request(self, request: dict[str, Any]):
        """Send a JSON-RPC request to the MCP server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP process not initialized")

        request_json = json.dumps(request)
        self.process.stdin.write(request_json + "\n")
        self.process.stdin.flush()

    def _read_response(self) -> dict[str, Any]:
        """Read a JSON-RPC response from the MCP server."""
        if not self.process or not self.process.stdout:
            raise RuntimeError("MCP process not initialized")

        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("MCP server closed connection")

        return json.loads(line)

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        if not self._initialized:
            await self.initialize()

        try:
            tool_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": arguments},
            }

            self._send_request(tool_request)
            response = self._read_response()

            if "error" in response:
                logger.error(f"Tool call error: {response['error']}")
                return {"error": response["error"]}

            return response.get("result", {})

        except Exception as e:
            logger.error(f"Failed to call tool {tool_name}: {e}")
            return {"error": str(e)}

    def get_tools_for_claude(self) -> list[dict[str, Any]]:
        """
        Get tools in Claude API format.

        Returns:
            List of tool definitions compatible with Claude API
        """
        claude_tools = []

        for tool in self.tools:
            claude_tool = {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("inputSchema", {"type": "object", "properties": {}}),
            }
            claude_tools.append(claude_tool)

        return claude_tools

    def close(self):
        """Close the MCP server process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            except Exception as e:
                logger.error(f"Error closing MCP process: {e}")
            finally:
                self.process = None
                self._initialized = False


class NotionMCPClient(MCPClient):
    """Specialized MCP client for Notion."""

    def __init__(self, notion_token: str):
        """
        Initialize Notion MCP client.

        Args:
            notion_token: Notion integration token
        """
        super().__init__(
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            env={"NOTION_TOKEN": notion_token},
        )
