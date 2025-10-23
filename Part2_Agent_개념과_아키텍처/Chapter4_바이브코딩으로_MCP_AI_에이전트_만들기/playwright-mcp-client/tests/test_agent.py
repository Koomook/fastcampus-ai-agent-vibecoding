"""Tests for Claude Agent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from anthropic.types import Message, TextBlock, ToolUseBlock, Usage

from playwright_mcp_client.agent import ClaudeAgent
from playwright_mcp_client.client import PlaywrightMCPClient
from playwright_mcp_client.config import Config


@pytest.fixture
def config():
    """Create test configuration."""
    return Config(
        anthropic_api_key="test-key",
        playwright_server_path="npx",
        playwright_server_args="@playwright/mcp@latest",
    )


@pytest.fixture
def mock_mcp_client():
    """Create mock MCP client."""
    client = AsyncMock(spec=PlaywrightMCPClient)
    client.list_tools = AsyncMock()
    client.call_tool = AsyncMock()
    return client


@pytest.fixture
def mock_tools():
    """Create mock MCP tools."""
    tool = MagicMock()
    tool.name = "playwright_navigate"
    tool.description = "Navigate to a URL"
    tool.inputSchema = {
        "type": "object",
        "properties": {
            "url": {"type": "string"}
        },
        "required": ["url"]
    }
    return [tool]


@pytest.mark.asyncio
async def test_agent_initialization(config, mock_mcp_client, mock_tools):
    """Test agent initialization."""
    mock_mcp_client.list_tools.return_value = mock_tools

    agent = ClaudeAgent(config, mock_mcp_client)
    await agent.initialize()

    assert len(agent.tools) == 1
    assert agent.tools[0]["name"] == "playwright_navigate"
    mock_mcp_client.list_tools.assert_called_once()


@pytest.mark.asyncio
async def test_agent_process_request_simple(config, mock_mcp_client, mock_tools):
    """Test processing a simple request without tool use."""
    mock_mcp_client.list_tools.return_value = mock_tools

    agent = ClaudeAgent(config, mock_mcp_client)
    await agent.initialize()

    # Mock Claude API response
    mock_response = Message(
        id="msg_123",
        type="message",
        role="assistant",
        content=[TextBlock(type="text", text="I'll help you with that.")],
        model="claude-3-5-sonnet-20241022",
        stop_reason="end_turn",
        stop_sequence=None,
        usage=Usage(input_tokens=10, output_tokens=20),
    )

    with patch.object(agent.client.messages, "create", return_value=mock_response):
        response = await agent.process_request("Hello")

        assert "I'll help you with that." in response


@pytest.mark.asyncio
async def test_agent_process_request_with_tool(config, mock_mcp_client, mock_tools):
    """Test processing a request that uses tools."""
    mock_mcp_client.list_tools.return_value = mock_tools

    # Mock tool execution result
    tool_result = MagicMock()
    tool_result.content = "Navigated successfully"
    mock_mcp_client.call_tool.return_value = tool_result

    agent = ClaudeAgent(config, mock_mcp_client)
    await agent.initialize()

    # Mock Claude API responses
    tool_use_response = Message(
        id="msg_123",
        type="message",
        role="assistant",
        content=[
            ToolUseBlock(
                type="tool_use",
                id="tool_123",
                name="playwright_navigate",
                input={"url": "https://example.com"}
            )
        ],
        model="claude-3-5-sonnet-20241022",
        stop_reason="tool_use",
        stop_sequence=None,
        usage=Usage(input_tokens=10, output_tokens=20),
    )

    final_response = Message(
        id="msg_124",
        type="message",
        role="assistant",
        content=[TextBlock(type="text", text="Navigation completed")],
        model="claude-3-5-sonnet-20241022",
        stop_reason="end_turn",
        stop_sequence=None,
        usage=Usage(input_tokens=30, output_tokens=10),
    )

    with patch.object(
        agent.client.messages, "create", side_effect=[tool_use_response, final_response]
    ):
        response = await agent.process_request("Go to example.com")

        assert "[Tool: playwright_navigate]" in response
        assert "Navigation completed" in response
        mock_mcp_client.call_tool.assert_called_once_with(
            "playwright_navigate", {"url": "https://example.com"}
        )
