"""
Claude Agent SDK Service Wrapper.
Handles interactions with Claude AI for processing Slack messages.
Phase 2: Claude Agent SDK Integration
Phase 3: Notion MCP Integration
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from anthropic import Anthropic

from config import settings
from mcp_client import NotionMCPClient

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service wrapper for Claude Agent SDK interactions."""

    def __init__(
        self,
        api_key: str = settings.ANTHROPIC_API_KEY,
        notion_token: Optional[str] = None,
        system_prompt_path: str = "csbot_system_prompt.txt",
    ):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key
            notion_token: Notion integration token (if None, MCP is disabled)
            system_prompt_path: Path to system prompt file
        """
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-haiku-4-5-20251001"
        self.system_prompt = self._load_system_prompt(system_prompt_path)

        # Initialize MCP client if token provided
        self.mcp_client: Optional[NotionMCPClient] = None
        if notion_token:
            self.mcp_client = NotionMCPClient(notion_token=notion_token)

    def _load_system_prompt(self, prompt_path: str) -> str:
        """
        Load system prompt from file.

        Args:
            prompt_path: Path to system prompt file

        Returns:
            System prompt text with current datetime injected
        """
        try:
            path = Path(prompt_path)
            if not path.exists():
                logger.warning(f"System prompt file not found: {prompt_path}, using default")
                return "You are a helpful AI assistant. Answer questions concisely and clearly."

            prompt_template = path.read_text(encoding="utf-8")

            # Inject current datetime
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prompt = prompt_template.replace("{{currentDateTime}}", current_datetime)

            return prompt
        except Exception as e:
            logger.error(f"Failed to load system prompt: {e}")
            return "You are a helpful AI assistant. Answer questions concisely and clearly."

    async def process_message(
        self,
        user_message: str,
        conversation_history: Optional[list[dict[str, str]]] = None,
    ) -> dict[str, Any]:
        """
        Process a user message with Claude and return the response.

        Args:
            user_message: The user's question/message
            conversation_history: List of previous messages with format:
                [{"role": "user"/"assistant", "content": "message"}, ...]

        Returns:
            Dictionary with keys:
                - "response": Claude's text response
                - "tokens": Token usage info
                - "stop_reason": Why Claude stopped
                - "tool_uses": List of tool calls made (if any)
        """
        try:
            # Initialize MCP client if available
            tools = []
            if self.mcp_client:
                await self.mcp_client.initialize()
                tools = self.mcp_client.get_tools_for_claude()
                logger.info(f"Using {len(tools)} MCP tools")

            # Build messages list
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            logger.info(
                json.dumps(
                    {
                        "action": "claude_request",
                        "model": self.model,
                        "history_length": len(conversation_history) if conversation_history else 0,
                        "message_preview": user_message[:100],
                        "mcp_enabled": self.mcp_client is not None,
                    }
                )
            )

            tool_uses = []
            final_response_text = ""
            total_input_tokens = 0
            total_output_tokens = 0

            # Agentic loop: Allow Claude to use tools
            max_turns = 5
            for turn in range(max_turns):
                # Call Claude API
                api_params = {
                    "model": self.model,
                    "max_tokens": 2048,
                    "messages": messages,
                    "system": self.system_prompt,
                }

                if tools:
                    api_params["tools"] = tools

                response = self.client.messages.create(**api_params)

                # Track tokens
                total_input_tokens += response.usage.input_tokens
                total_output_tokens += response.usage.output_tokens

                # Check stop reason
                if response.stop_reason == "end_turn":
                    # Final response
                    final_response_text = response.content[0].text if response.content else ""
                    break

                elif response.stop_reason == "tool_use":
                    # Claude wants to use tools
                    tool_results = []

                    for content_block in response.content:
                        if content_block.type == "tool_use":
                            tool_name = content_block.name
                            tool_input = content_block.input
                            tool_use_id = content_block.id

                            logger.info(f"Tool use: {tool_name} with input: {tool_input}")

                            # Track tool use
                            tool_uses.append(
                                {
                                    "name": tool_name,
                                    "input": tool_input,
                                }
                            )

                            # Call MCP tool
                            if self.mcp_client:
                                tool_result = await self.mcp_client.call_tool(
                                    tool_name, tool_input
                                )
                            else:
                                tool_result = {"error": "MCP client not available"}

                            logger.info(f"Tool result: {tool_result}")

                            # Add tool result to messages
                            tool_results.append(
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use_id,
                                    "content": json.dumps(tool_result),
                                }
                            )

                    # Add assistant message with tool use
                    messages.append({"role": "assistant", "content": response.content})

                    # Add tool results
                    messages.append({"role": "user", "content": tool_results})

                else:
                    # Unexpected stop reason
                    logger.warning(f"Unexpected stop reason: {response.stop_reason}")
                    final_response_text = response.content[0].text if response.content else ""
                    break

            # Log response metrics
            logger.info(
                json.dumps(
                    {
                        "action": "claude_response",
                        "stop_reason": response.stop_reason,
                        "input_tokens": total_input_tokens,
                        "output_tokens": total_output_tokens,
                        "tool_uses_count": len(tool_uses),
                    }
                )
            )

            return {
                "response": final_response_text,
                "tokens": {
                    "input": total_input_tokens,
                    "output": total_output_tokens,
                },
                "stop_reason": response.stop_reason,
                "tool_uses": tool_uses,
            }

        except Exception as e:
            logger.error(
                json.dumps(
                    {
                        "error": "claude_api_error",
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                    }
                )
            )
            raise
        finally:
            # Clean up MCP client
            if self.mcp_client:
                self.mcp_client.close()


def convert_slack_history_to_claude_messages(
    slack_messages: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """
    Convert Slack message history to Claude message format.

    Args:
        slack_messages: List of Slack message objects with 'user', 'text', 'bot_id' keys

    Returns:
        List of messages in Claude format: [{"role": "user"/"assistant", "content": "..."}, ...]
    """
    messages = []

    for msg in slack_messages:
        # Skip messages without text
        if "text" not in msg:
            continue

        # Determine sender role
        if msg.get("bot_id"):
            # Message from bot
            role = "assistant"
        elif msg.get("user"):
            # Message from user
            role = "user"
        else:
            # Skip messages we can't determine sender for
            continue

        messages.append({"role": role, "content": msg["text"]})

    return messages
