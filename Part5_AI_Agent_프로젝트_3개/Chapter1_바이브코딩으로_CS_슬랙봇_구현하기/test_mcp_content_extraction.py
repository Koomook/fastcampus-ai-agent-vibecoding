"""
Unit tests for MCP content extraction.
Tests the _extract_mcp_content method in ClaudeService.
"""
import json

import pytest

from claude_service import ClaudeService


def test_extract_mcp_content_with_valid_response():
    """Test extracting content from a valid MCP response."""
    service = ClaudeService()

    # Simulate actual MCP response format
    mcp_response = {
        "content": [
            {
                "type": "text",
                "text": '{"object":"page","id":"123","properties":{"title":"Test Page"}}',
            }
        ]
    }

    result = service._extract_mcp_content(mcp_response)

    # Should return the JSON string directly
    assert result == '{"object":"page","id":"123","properties":{"title":"Test Page"}}'

    # Verify it's valid JSON
    parsed = json.loads(result)
    assert parsed["object"] == "page"
    assert parsed["id"] == "123"


def test_extract_mcp_content_with_error():
    """Test extracting content when MCP returns an error."""
    service = ClaudeService()

    mcp_response = {"error": "Page not found"}

    result = service._extract_mcp_content(mcp_response)

    # Should return error as JSON
    parsed = json.loads(result)
    assert "error" in parsed
    assert parsed["error"] == "Page not found"


def test_extract_mcp_content_with_empty_content():
    """Test extracting content when content array is empty."""
    service = ClaudeService()

    mcp_response = {"content": []}

    result = service._extract_mcp_content(mcp_response)

    # Should return the entire response as JSON
    parsed = json.loads(result)
    assert "content" in parsed
    assert parsed["content"] == []


def test_extract_mcp_content_with_missing_text_field():
    """Test extracting content when text field is missing."""
    service = ClaudeService()

    mcp_response = {"content": [{"type": "text"}]}

    result = service._extract_mcp_content(mcp_response)

    # Should return the entire response as JSON
    parsed = json.loads(result)
    assert "content" in parsed


def test_extract_mcp_content_with_notion_search_response():
    """Test extracting content from actual Notion search response."""
    service = ClaudeService()

    # Real Notion search response format
    mcp_response = {
        "content": [
            {
                "type": "text",
                "text": '{"object":"list","results":[{"object":"page","id":"28e2b37d-07c4-81c2-9fa0-c388509dfcec","properties":{"카테고리":{"title":[{"text":{"content":"주차 안내"}}]}}}]}',
            }
        ]
    }

    result = service._extract_mcp_content(mcp_response)

    # Verify it's valid JSON
    parsed = json.loads(result)
    assert parsed["object"] == "list"
    assert "results" in parsed
    assert len(parsed["results"]) > 0
    assert parsed["results"][0]["id"] == "28e2b37d-07c4-81c2-9fa0-c388509dfcec"


def test_extract_mcp_content_with_notion_block_children_response():
    """Test extracting content from Notion block children response."""
    service = ClaudeService()

    # Real Notion block children response format
    mcp_response = {
        "content": [
            {
                "type": "text",
                "text": '{"object":"list","results":[{"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"개요"}}]}},{"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"주차 정기권 신청 방법"}}]}}]}',
            }
        ]
    }

    result = service._extract_mcp_content(mcp_response)

    # Verify it's valid JSON
    parsed = json.loads(result)
    assert parsed["object"] == "list"
    assert "results" in parsed
    assert parsed["results"][0]["type"] == "heading_2"
    assert parsed["results"][1]["type"] == "paragraph"


def test_extract_mcp_content_preserves_korean_text():
    """Test that Korean text is preserved correctly."""
    service = ClaudeService()

    mcp_response = {
        "content": [
            {
                "type": "text",
                "text": '{"message":"주차 정기권 신청은 위워크 앱에서 가능합니다"}',
            }
        ]
    }

    result = service._extract_mcp_content(mcp_response)

    # Verify Korean text is preserved
    parsed = json.loads(result)
    assert "주차 정기권" in parsed["message"]
    assert "위워크 앱" in parsed["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
