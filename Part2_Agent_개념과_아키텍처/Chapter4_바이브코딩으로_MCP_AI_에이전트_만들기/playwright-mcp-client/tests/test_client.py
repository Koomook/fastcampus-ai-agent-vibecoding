"""Tests for MCP Client."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

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
def mock_session():
    """Create mock MCP session."""
    session = AsyncMock()
    session.initialize = AsyncMock()
    session.list_tools = AsyncMock()
    session.call_tool = AsyncMock()
    return session


@pytest.mark.asyncio
async def test_client_initialization(config):
    """Test client initialization."""
    client = PlaywrightMCPClient(config)
    assert client.config == config
    assert client.session is None


@pytest.mark.asyncio
async def test_client_connect(config, mock_session):
    """Test client connection to MCP server."""
    client = PlaywrightMCPClient(config)

    with patch("playwright_mcp_client.client.stdio_client") as mock_stdio:
        # Setup mock
        mock_read = AsyncMock()
        mock_write = AsyncMock()
        mock_stdio.return_value.__aenter__.return_value = (mock_read, mock_write)

        with patch("playwright_mcp_client.client.ClientSession", return_value=mock_session):
            await client.connect()

            # Verify connection
            assert client.session is not None
            mock_session.__aenter__.assert_called_once()
            mock_session.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_client_list_tools(config, mock_session):
    """Test listing tools."""
    client = PlaywrightMCPClient(config)
    client.session = mock_session

    # Mock tools response
    mock_tool = MagicMock()
    mock_tool.name = "playwright_navigate"
    mock_tool.description = "Navigate to URL"
    mock_session.list_tools.return_value = MagicMock(tools=[mock_tool])

    # List tools
    tools = await client.list_tools()

    assert len(tools) == 1
    assert tools[0].name == "playwright_navigate"
    mock_session.list_tools.assert_called_once()


@pytest.mark.asyncio
async def test_client_call_tool(config, mock_session):
    """Test calling a tool."""
    client = PlaywrightMCPClient(config)
    client.session = mock_session

    # Mock tool call response
    mock_result = MagicMock()
    mock_result.content = "Success"
    mock_session.call_tool.return_value = mock_result

    # Call tool
    result = await client.call_tool("playwright_navigate", {"url": "https://example.com"})

    assert result.content == "Success"
    mock_session.call_tool.assert_called_once_with(
        "playwright_navigate", {"url": "https://example.com"}
    )


@pytest.mark.asyncio
async def test_client_not_connected_error(config):
    """Test error when calling methods before connection."""
    client = PlaywrightMCPClient(config)

    with pytest.raises(RuntimeError, match="Not connected to MCP server"):
        await client.list_tools()

    with pytest.raises(RuntimeError, match="Not connected to MCP server"):
        await client.call_tool("test", {})


@pytest.mark.asyncio
async def test_client_context_manager(config, mock_session):
    """Test client as context manager."""
    client = PlaywrightMCPClient(config)

    with patch("playwright_mcp_client.client.stdio_client") as mock_stdio:
        mock_read = AsyncMock()
        mock_write = AsyncMock()
        mock_stdio.return_value.__aenter__.return_value = (mock_read, mock_write)

        with patch("playwright_mcp_client.client.ClientSession", return_value=mock_session):
            async with client:
                assert client.session is not None

            # Verify cleanup
            mock_session.__aexit__.assert_called_once()
