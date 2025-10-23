"""Claude AI Agent for processing user requests."""

import base64
import json
from pathlib import Path
from typing import Any

import anthropic
from anthropic.types import Message, TextBlock, ToolUseBlock

from .client import PlaywrightMCPClient
from .config import Config


SYSTEM_PROMPT = """당신은 Playwright MCP 서버를 활용하여 웹 브라우저 자동화를 수행하는 전문가입니다.
사용자의 요청을 분석하고 적절한 MCP tool을 선택하여 작업을 수행하세요.
각 단계에서 어떤 tool을 사용했는지 명확히 설명하세요."""


class ClaudeAgent:
    """AI Agent that uses Claude to process requests and call MCP tools."""

    def __init__(self, config: Config, mcp_client: PlaywrightMCPClient):
        """Initialize Claude agent.

        Args:
            config: Configuration object.
            mcp_client: MCP client instance.
        """
        self.config = config
        self.mcp_client = mcp_client
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self.tools: list[dict[str, Any]] = []

    async def initialize(self) -> None:
        """Initialize agent by fetching available tools."""
        # Get tools from MCP server
        mcp_tools = await self.mcp_client.list_tools()

        # Convert MCP tools to Anthropic tool format
        self.tools = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in mcp_tools
        ]

    async def process_request(self, user_message: str) -> str:
        """Process user request using Claude and MCP tools.

        Args:
            user_message: User's natural language request.

        Returns:
            Response message with tool execution results.
        """
        messages = [{"role": "user", "content": user_message}]

        response_text = ""

        while True:
            # Call Claude API
            response: Message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
            )

            # Check stop reason
            if response.stop_reason == "end_turn":
                # Extract text from response
                for content in response.content:
                    if isinstance(content, TextBlock):
                        response_text += content.text
                break

            # Process tool use
            if response.stop_reason == "tool_use":
                # Add assistant message to conversation
                messages.append({"role": "assistant", "content": response.content})

                # Execute tools and collect results
                tool_results = []
                for content in response.content:
                    if isinstance(content, ToolUseBlock):
                        tool_name = content.name
                        tool_input = content.input

                        # Call MCP tool
                        result = await self.mcp_client.call_tool(tool_name, tool_input)

                        # Process screenshot results
                        result_content = str(result.content)
                        if tool_name == "browser_take_screenshot":
                            saved_path = self._save_screenshot(result.content)
                            if saved_path:
                                response_text += f"\n[Tool: {tool_name}]\n스크린샷 저장됨: {saved_path}\n"
                            else:
                                response_text += f"\n[Tool: {tool_name}]\n"
                        else:
                            # Add tool usage to response text
                            response_text += f"\n[Tool: {tool_name}]\n"

                        # Add result to list
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result_content,
                            }
                        )

                # Add tool results to conversation
                messages.append({"role": "user", "content": tool_results})

            else:
                # Unexpected stop reason
                break

        return response_text.strip()

    def _save_screenshot(self, result_content: Any) -> str | None:
        """Save screenshot from MCP tool result to file.

        Args:
            result_content: Tool result content containing screenshot data.

        Returns:
            Path to saved file, or None if saving failed.
        """
        try:
            # Ensure output directory exists
            self.config.ensure_output_dir()

            # Parse result content
            # MCP result.content is a list of content items
            if isinstance(result_content, list):
                for item in result_content:
                    # Check if item has type='image' and data attribute
                    if hasattr(item, 'type') and item.type == 'image' and hasattr(item, 'data'):
                        image_data = item.data
                        mime_type = getattr(item, 'mimeType', 'image/png')

                        # Decode base64 image
                        image_bytes = base64.b64decode(image_data)

                        # Determine file extension
                        ext = "png" if "png" in mime_type else "jpeg"

                        # Generate filename
                        import datetime
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"screenshot_{timestamp}.{ext}"
                        filepath = self.config.output_dir / filename

                        # Save file
                        with open(filepath, "wb") as f:
                            f.write(image_bytes)

                        return str(filepath)

            return None

        except Exception as e:
            print(f"스크린샷 저장 실패: {e}")
            return None
