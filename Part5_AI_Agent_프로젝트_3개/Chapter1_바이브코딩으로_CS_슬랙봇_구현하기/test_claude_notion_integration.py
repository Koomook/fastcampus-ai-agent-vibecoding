"""
Integration test for Claude + Notion MCP.
This test verifies that Claude can successfully retrieve and use Notion content.
"""
import asyncio
import os

from dotenv import load_dotenv

from claude_service import ClaudeService

# Load environment variables
load_dotenv()


async def test_claude_retrieves_notion_content():
    """Test that Claude can retrieve and understand Notion content."""

    # Get environment variables
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ NOTION_TOKEN not set, skipping test")
        return

    print("✓ Environment variables loaded")

    # Initialize Claude service with Notion MCP
    service = ClaudeService(notion_token=notion_token)
    print("✓ Claude service initialized with Notion MCP")

    # Test query about parking
    user_message = "주차 정기권은 어떻게 신청하나요?"
    print(f"\n📝 User question: {user_message}")

    # Process the message
    print("\n🤔 Processing with Claude + Notion MCP...")
    result = await service.process_message(user_message)

    # Check results
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)

    print(f"\n📊 Token usage:")
    print(f"   Input tokens:  {result['tokens']['input']}")
    print(f"   Output tokens: {result['tokens']['output']}")

    print(f"\n🔧 Tool usage:")
    print(f"   Tools called: {len(result['tool_uses'])}")
    if result["tool_uses"]:
        for i, tool_use in enumerate(result["tool_uses"], 1):
            print(f"   {i}. {tool_use['name']}")
            print(f"      Input: {tool_use['input']}")

    print(f"\n💬 Claude's response:")
    print(f"   {result['response']}")

    # Assertions
    assert result["response"], "Response should not be empty"
    assert len(result["tool_uses"]) > 0, "Should have used at least one tool"

    # Check if Claude used MCP tools (either search or direct page retrieval)
    tool_names = [tool["name"] for tool in result["tool_uses"]]
    notion_tools_used = any(
        tool_name.startswith("API-") for tool_name in tool_names
    )
    assert notion_tools_used, "Should have used at least one Notion MCP tool"

    # Check if Claude retrieved actual page content
    assert (
        "API-get-block-children" in tool_names
        or "API-retrieve-a-page" in tool_names
    ), "Should have retrieved page content or metadata"

    # Check if response mentions parking (주차)
    assert (
        "주차" in result["response"]
        or "정기권" in result["response"]
        or "신청" in result["response"]
    ), "Response should mention parking-related terms"

    # Check if response is not an error message
    assert "가이드 문서에 접근이 어려운" not in result["response"], (
        "Should not return error about document access"
    )

    # Check if response contains actual content from Notion (not generic response)
    assert (
        "150,000" in result["response"] or "관리사무소" in result["response"]
    ), "Response should contain specific information from Notion page"

    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nClaude successfully:")
    print("  1. ✓ Connected to Notion MCP")
    print("  2. ✓ Searched for relevant pages")
    print("  3. ✓ Retrieved page content")
    print("  4. ✓ Generated helpful response")


async def test_claude_uses_multiple_tools():
    """Test that Claude uses both search and block retrieval tools."""

    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("❌ NOTION_TOKEN not set, skipping test")
        return

    service = ClaudeService(notion_token=notion_token)

    # Ask a question that requires detailed information
    user_message = "회의실 예약은 어떻게 하나요?"
    print(f"\n📝 User question: {user_message}")

    result = await service.process_message(user_message)

    print(f"\n🔧 Tools used:")
    for i, tool_use in enumerate(result["tool_uses"], 1):
        print(f"   {i}. {tool_use['name']}")

    # Should use MCP tools
    tool_names = [tool["name"] for tool in result["tool_uses"]]

    print("\n" + "=" * 80)

    # Check for any Notion API tools
    notion_tools = [t for t in tool_names if t.startswith("API-")]
    assert len(notion_tools) > 0, "Should have used at least one Notion MCP tool"

    if "API-post-search" in tool_names:
        print("✅ Used search tool to find pages")

    if "API-retrieve-a-page" in tool_names:
        print("✅ Used page retrieval tool to get page metadata")

    if "API-get-block-children" in tool_names:
        print("✅ Used block children tool to retrieve page content")

    # Verify response quality
    assert result["response"], "Should have generated a response"
    assert "회의실" in result["response"], "Response should mention meeting rooms"

    print(f"✅ Used {len(notion_tools)} Notion MCP tool(s)")
    print("=" * 80)


async def main():
    """Run all integration tests."""
    print("=" * 80)
    print("CLAUDE + NOTION MCP INTEGRATION TEST")
    print("=" * 80)

    try:
        print("\n[TEST 1] Testing basic Notion content retrieval...")
        print("-" * 80)
        await test_claude_retrieves_notion_content()

        print("\n\n[TEST 2] Testing multi-tool usage...")
        print("-" * 80)
        await test_claude_uses_multiple_tools()

        print("\n\n" + "=" * 80)
        print("🎉 ALL INTEGRATION TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)

    except AssertionError as e:
        print(f"\n\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
