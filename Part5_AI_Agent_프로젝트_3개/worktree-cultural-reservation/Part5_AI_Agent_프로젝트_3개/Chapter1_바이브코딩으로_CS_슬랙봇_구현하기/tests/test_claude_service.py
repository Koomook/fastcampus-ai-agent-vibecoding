"""
Tests for Claude Service.
Includes integration tests with real Claude API (brief messages for cost efficiency).
"""
import pytest

from claude_service import ClaudeService, convert_slack_history_to_claude_messages


class TestClaudeService:
    """Test Claude Service wrapper."""

    @pytest.fixture
    def claude_service(self):
        """Create Claude service instance."""
        return ClaudeService()

    @pytest.mark.asyncio
    async def test_process_simple_message(self, claude_service):
        """Test processing a simple message with real Claude API."""
        response = await claude_service.process_message("Say 'hello world' only")

        # Verify response structure
        assert "response" in response
        assert "tokens" in response
        assert "stop_reason" in response
        assert "tool_uses" in response

        # Verify response content
        assert isinstance(response["response"], str)
        assert len(response["response"]) > 0
        assert response["stop_reason"] == "end_turn"

        # Verify tokens are tracked
        assert response["tokens"]["input"] > 0
        assert response["tokens"]["output"] > 0

        # Verify tool_uses is a list
        assert isinstance(response["tool_uses"], list)

    @pytest.mark.asyncio
    async def test_process_message_with_history(self, claude_service):
        """Test processing a message with conversation history using real Claude API."""
        # Create conversation history
        history = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "2+2 equals 4."},
        ]

        # Ask follow-up question
        response = await claude_service.process_message(
            "Is that correct?",
            conversation_history=history,
        )

        # Verify response structure
        assert "response" in response
        assert isinstance(response["response"], str)
        assert len(response["response"]) > 0

        # Response should reference the previous context
        assert response["stop_reason"] == "end_turn"

    @pytest.mark.asyncio
    async def test_process_wework_question(self, claude_service):
        """Test processing a WeWork-related question with real Claude API."""
        response = await claude_service.process_message("회의실 예약은 어떻게 하나요?")

        # Verify response
        assert "response" in response
        assert len(response["response"]) > 0
        # Should contain WeWork or meeting room related terms
        response_lower = response["response"].lower()
        assert any(
            term in response_lower for term in ["회의실", "예약", "위워크", "wework"]
        )

    @pytest.mark.asyncio
    async def test_process_parking_question(self, claude_service):
        """Test processing a parking-related question with real Claude API."""
        response = await claude_service.process_message("주차 정기권은 어떻게 신청하나요?")

        # Verify response
        assert "response" in response
        assert len(response["response"]) > 0
        # Should contain parking-related terms
        response_lower = response["response"].lower()
        assert any(
            term in response_lower for term in ["주차", "정기권"]
        )

    @pytest.mark.asyncio
    async def test_error_handling_invalid_history(self, claude_service):
        """Test error handling with invalid history format."""
        invalid_history = [{"invalid_key": "value"}]

        with pytest.raises(Exception):
            await claude_service.process_message("Test", conversation_history=invalid_history)


class TestSlackToClaudeConversion:
    """Test conversion of Slack messages to Claude format."""

    def test_convert_user_message(self):
        """Test converting a user message."""
        slack_messages = [{"user": "U123", "text": "Hello"}]

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert len(result) == 1
        assert result[0] == {"role": "user", "content": "Hello"}

    def test_convert_bot_message(self):
        """Test converting a bot message."""
        slack_messages = [{"bot_id": "B123", "text": "Hi there"}]

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert len(result) == 1
        assert result[0] == {"role": "assistant", "content": "Hi there"}

    def test_convert_mixed_messages(self):
        """Test converting mixed user and bot messages."""
        slack_messages = [
            {"user": "U123", "text": "What is AI?"},
            {"bot_id": "B123", "text": "AI is artificial intelligence."},
            {"user": "U456", "text": "Tell me more"},
        ]

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert len(result) == 3
        assert result[0]["role"] == "user"
        assert result[1]["role"] == "assistant"
        assert result[2]["role"] == "user"

    def test_convert_skips_messages_without_text(self):
        """Test that messages without text are skipped."""
        slack_messages = [
            {"user": "U123", "text": "Hello"},
            {"user": "U456"},  # No text
            {"user": "U789", "text": "World"},
        ]

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert len(result) == 2
        assert result[0]["content"] == "Hello"
        assert result[1]["content"] == "World"

    def test_convert_empty_history(self):
        """Test converting empty message history."""
        slack_messages = []

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert result == []

    def test_convert_skips_messages_without_sender(self):
        """Test that messages without user or bot_id are skipped."""
        slack_messages = [
            {"text": "Hello"},  # No user or bot_id
            {"user": "U123", "text": "Hi"},
        ]

        result = convert_slack_history_to_claude_messages(slack_messages)

        assert len(result) == 1
        assert result[0]["content"] == "Hi"
