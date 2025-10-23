"""
Tests for MCP Client.
Phase 3: Notion MCP Integration
"""
import pytest

from mcp_client import MCPClient, NotionMCPClient


class TestMCPClient:
    """Test MCP Client base functionality."""

    def test_mcp_client_initialization(self):
        """Test MCP client can be initialized."""
        client = MCPClient(
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            env={"NOTION_TOKEN": "test_token"},
        )

        assert client.command == "npx"
        assert client.args == ["-y", "@notionhq/notion-mcp-server"]
        assert client.env == {"NOTION_TOKEN": "test_token"}
        assert client.process is None
        assert client._initialized is False

    def test_notion_mcp_client_initialization(self):
        """Test Notion MCP client initialization."""
        client = NotionMCPClient(notion_token="test_token")

        assert client.command == "npx"
        assert "-y" in client.args
        assert "@notionhq/notion-mcp-server" in client.args
        assert client.env["NOTION_TOKEN"] == "test_token"


class TestClaudeServiceWithMCP:
    """Test Claude Service with MCP integration."""

    @pytest.mark.asyncio
    async def test_claude_service_without_notion_token(self):
        """Test Claude service works without Notion token (MCP disabled)."""
        from claude_service import ClaudeService

        service = ClaudeService(notion_token=None)

        assert service.mcp_client is None
        assert service.system_prompt is not None

    @pytest.mark.asyncio
    async def test_claude_service_with_notion_token(self):
        """Test Claude service initializes with Notion token."""
        from claude_service import ClaudeService

        service = ClaudeService(notion_token="test_token")

        assert service.mcp_client is not None
        assert isinstance(service.mcp_client, NotionMCPClient)

    @pytest.mark.asyncio
    async def test_system_prompt_loading(self):
        """Test system prompt is loaded from file."""
        from claude_service import ClaudeService

        service = ClaudeService(system_prompt_path="csbot_system_prompt.txt")

        # Check system prompt is not empty and not the default
        assert len(service.system_prompt) > 100
        assert "위워크 강남 지점" in service.system_prompt or "CS 봇" in service.system_prompt

    @pytest.mark.asyncio
    async def test_system_prompt_fallback(self):
        """Test system prompt falls back to default if file not found."""
        from claude_service import ClaudeService

        service = ClaudeService(system_prompt_path="nonexistent_file.txt")

        # Should use default prompt
        assert service.system_prompt == "You are a helpful AI assistant. Answer questions concisely and clearly."

    @pytest.mark.asyncio
    async def test_process_message_returns_tool_uses(self):
        """Test that process_message returns tool_uses key."""
        from claude_service import ClaudeService

        service = ClaudeService(notion_token=None)

        # Simple message without tools
        response = await service.process_message("Say 'hello' only")

        assert "response" in response
        assert "tokens" in response
        assert "tool_uses" in response
        assert isinstance(response["tool_uses"], list)


class TestMCPIntegration:
    """Integration tests for MCP (skipped if no Notion token available)."""

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="MCP integration tests require valid NOTION_TOKEN and are opt-in")
    async def test_mcp_client_initialize_and_list_tools(self):
        """Test MCP client can initialize and list tools (requires valid NOTION_TOKEN)."""
        import os

        notion_token = os.getenv("NOTION_TOKEN")
        if not notion_token:
            pytest.skip("NOTION_TOKEN not set")

        client = NotionMCPClient(notion_token=notion_token)

        try:
            await client.initialize()

            # Check tools were fetched
            assert len(client.tools) > 0

            # Check tools have required fields
            for tool in client.tools:
                assert "name" in tool
                assert "description" in tool or "inputSchema" in tool

            # Check Claude format conversion
            claude_tools = client.get_tools_for_claude()
            assert len(claude_tools) > 0

            for tool in claude_tools:
                assert "name" in tool
                assert "description" in tool
                assert "input_schema" in tool

        finally:
            client.close()


class TestClaudeWithMCPToolUsage:
    """Test Claude's ability to use MCP tools (with mocks)."""

    @pytest.mark.asyncio
    async def test_claude_uses_mcp_tool_with_mock(self, monkeypatch):
        """Test Claude calls MCP tool when needed (mocked)."""
        from unittest.mock import AsyncMock, MagicMock
        from claude_service import ClaudeService

        # Mock MCP client
        mock_mcp_client = MagicMock()
        mock_mcp_client.get_tools_for_claude = MagicMock(return_value=[
            {
                "name": "search_notion",
                "description": "Search Notion database",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    }
                }
            }
        ])
        mock_mcp_client.call_tool = AsyncMock(return_value={
            "results": [{"title": "회의실 예약 가이드"}]
        })
        mock_mcp_client.close = MagicMock()

        # Mock Anthropic client to simulate tool_use response
        mock_anthropic = MagicMock()

        # First response: Claude wants to use tool
        tool_use_response = MagicMock()
        tool_use_response.stop_reason = "tool_use"
        tool_use_response.usage.input_tokens = 100
        tool_use_response.usage.output_tokens = 50

        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.name = "search_notion"
        tool_use_block.input = {"query": "회의실"}
        tool_use_block.id = "tool_123"

        tool_use_response.content = [tool_use_block]

        # Second response: Claude provides final answer
        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.usage.input_tokens = 150
        final_response.usage.output_tokens = 100
        final_response.content = [
            MagicMock(
                type="text",
                text="회의실 예약은 위워크 앱에서 하실 수 있습니다."
            )
        ]

        mock_anthropic.messages.create = MagicMock(side_effect=[tool_use_response, final_response])

        # Create service with mocked components
        service = ClaudeService(notion_token="test_token")
        service.client = mock_anthropic
        service.mcp_client = mock_mcp_client

        # Mock initialize
        async def mock_initialize():
            pass
        service.mcp_client.initialize = mock_initialize

        # Execute
        result = await service.process_message("회의실 예약 방법 알려줘")

        # Verify
        assert result["response"] == "회의실 예약은 위워크 앱에서 하실 수 있습니다."
        assert len(result["tool_uses"]) == 1
        assert result["tool_uses"][0]["name"] == "search_notion"
        assert result["tokens"]["input"] == 250  # 100 + 150
        assert result["tokens"]["output"] == 150  # 50 + 100

        # Verify MCP tool was called
        mock_mcp_client.call_tool.assert_called_once_with("search_notion", {"query": "회의실"})

    @pytest.mark.asyncio
    async def test_tool_result_added_to_conversation(self, monkeypatch):
        """Test tool execution result is properly added to conversation."""
        from unittest.mock import AsyncMock, MagicMock
        from claude_service import ClaudeService

        mock_mcp_client = MagicMock()
        mock_mcp_client.get_tools_for_claude = MagicMock(return_value=[
            {
                "name": "search_notion",
                "description": "Search Notion",
                "input_schema": {"type": "object", "properties": {}}
            }
        ])
        mock_mcp_client.call_tool = AsyncMock(return_value={"content": "Test result"})
        mock_mcp_client.close = MagicMock()

        mock_anthropic = MagicMock()

        # Tool use response
        tool_use_response = MagicMock()
        tool_use_response.stop_reason = "tool_use"
        tool_use_response.usage.input_tokens = 100
        tool_use_response.usage.output_tokens = 50
        tool_use_block = MagicMock(
            type="tool_use",
            name="search_notion",
            input={},
            id="tool_456"
        )
        tool_use_response.content = [tool_use_block]

        # Final response
        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.usage.input_tokens = 120
        final_response.usage.output_tokens = 80
        final_response.content = [MagicMock(type="text", text="답변입니다")]

        # Track API calls
        call_messages = []

        def track_calls(**kwargs):
            call_messages.append(kwargs.get("messages", []))
            if len(call_messages) == 1:
                return tool_use_response
            return final_response

        mock_anthropic.messages.create = MagicMock(side_effect=track_calls)

        service = ClaudeService(notion_token="test_token")
        service.client = mock_anthropic
        service.mcp_client = mock_mcp_client

        async def mock_initialize():
            pass
        service.mcp_client.initialize = mock_initialize

        result = await service.process_message("테스트")

        # Verify tool result was added to conversation
        assert len(call_messages) == 2

        # Second call should include assistant message with tool use + user message with tool result
        second_call_messages = call_messages[1]

        # Check that assistant message with tool use was added
        assistant_msg = next((m for m in second_call_messages if m["role"] == "assistant"), None)
        assert assistant_msg is not None

        # Check that user message with tool result was added
        tool_result_msg = next(
            (m for m in second_call_messages if m["role"] == "user" and isinstance(m["content"], list)),
            None
        )
        assert tool_result_msg is not None

    @pytest.mark.asyncio
    async def test_mcp_tool_failure_handling(self):
        """Test graceful handling when MCP tool execution fails."""
        from unittest.mock import AsyncMock, MagicMock
        from claude_service import ClaudeService

        mock_mcp_client = MagicMock()
        mock_mcp_client.get_tools_for_claude = MagicMock(return_value=[
            {
                "name": "search_notion",
                "description": "Search Notion",
                "input_schema": {"type": "object", "properties": {}}
            }
        ])
        # Simulate tool failure
        mock_mcp_client.call_tool = AsyncMock(return_value={"error": "Connection timeout"})
        mock_mcp_client.close = MagicMock()

        mock_anthropic = MagicMock()

        tool_use_response = MagicMock()
        tool_use_response.stop_reason = "tool_use"
        tool_use_response.usage.input_tokens = 100
        tool_use_response.usage.output_tokens = 50

        tool_use_block = MagicMock()
        tool_use_block.type = "tool_use"
        tool_use_block.name = "search_notion"
        tool_use_block.input = {}
        tool_use_block.id = "tool_789"

        tool_use_response.content = [tool_use_block]

        final_response = MagicMock()
        final_response.stop_reason = "end_turn"
        final_response.usage.input_tokens = 120
        final_response.usage.output_tokens = 80
        final_response.content = [
            MagicMock(
                type="text",
                text="죄송합니다. 검색 중 오류가 발생했습니다."
            )
        ]

        mock_anthropic.messages.create = MagicMock(side_effect=[tool_use_response, final_response])

        service = ClaudeService(notion_token="test_token")
        service.client = mock_anthropic
        service.mcp_client = mock_mcp_client

        async def mock_initialize():
            pass
        service.mcp_client.initialize = mock_initialize

        # Should not raise exception
        result = await service.process_message("검색해줘")

        # Verify graceful response
        assert result["response"] is not None
        assert result["tool_uses"][0]["name"] == "search_notion"

    @pytest.mark.asyncio
    async def test_claude_without_mcp_tools(self):
        """Test Claude works normally without MCP tools."""
        from unittest.mock import MagicMock
        from claude_service import ClaudeService

        mock_anthropic = MagicMock()

        response = MagicMock()
        response.stop_reason = "end_turn"
        response.usage.input_tokens = 50
        response.usage.output_tokens = 30
        response.content = [MagicMock(type="text", text="안녕하세요")]

        mock_anthropic.messages.create = MagicMock(return_value=response)

        service = ClaudeService(notion_token=None)  # No MCP
        service.client = mock_anthropic

        result = await service.process_message("안녕")

        assert result["response"] == "안녕하세요"
        assert result["tool_uses"] == []
        assert mock_anthropic.messages.create.call_count == 1

        # Verify no tools parameter was passed
        call_kwargs = mock_anthropic.messages.create.call_args[1]
        assert "tools" not in call_kwargs
