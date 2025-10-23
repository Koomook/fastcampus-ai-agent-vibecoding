"""
Direct test of Notion MCP server to understand its behavior.
This script tests the MCP server independently to debug integration issues.
"""
import asyncio
import os
import sys

from dotenv import load_dotenv

from mcp_client import NotionMCPClient

# Load environment variables from .env file
load_dotenv()


async def test_mcp_server():
    """Test Notion MCP server directly."""

    # Get Notion token from environment
    notion_token = os.getenv("NOTION_TOKEN")
    if not notion_token:
        print("ERROR: NOTION_TOKEN environment variable not set")
        sys.exit(1)

    print(f"✓ Notion token found (length: {len(notion_token)})")

    # Initialize MCP client
    print("\n1. Initializing Notion MCP client...")
    client = NotionMCPClient(notion_token=notion_token)

    try:
        await client.initialize()
        print("✓ MCP client initialized successfully")

        # Get available tools
        print("\n2. Available tools from MCP server:")
        tools = client.get_tools_for_claude()
        print(f"✓ Found {len(tools)} tools\n")

        for i, tool in enumerate(tools, 1):
            print(f"Tool {i}: {tool['name']}")
            print(f"  Description: {tool['description']}")
            print(f"  Input schema: {tool['input_schema']}")
            print()

        # Test search functionality
        print("\n3. Testing search functionality...")
        search_tool = next((t for t in tools if "search" in t["name"].lower()), None)

        if search_tool:
            print(f"✓ Found search tool: {search_tool['name']}")

            # Try searching for "주차"
            print("\n4. Searching for '주차' in Notion...")
            result = await client.call_tool(
                search_tool["name"],
                {"query": "주차"}
            )

            print(f"Search result type: {type(result)}")
            print(f"Search result keys: {result.keys() if isinstance(result, dict) else 'N/A'}")
            print(f"Search result: {result}")

            # Check if we got actual content
            if "error" in result:
                print(f"\n❌ Error in search: {result['error']}")
            else:
                print(f"\n✓ Search completed successfully")

                # Try to understand the response structure
                if "content" in result:
                    content = result["content"]
                    print(f"Content type: {type(content)}")
                    print(f"Content length: {len(content) if isinstance(content, (list, str)) else 'N/A'}")
                    print(f"Content preview: {str(content)[:500]}...")
        else:
            print("❌ No search tool found in available tools")

        # Test page retrieval
        print("\n5. Testing page metadata retrieval...")
        page_tool = next((t for t in tools if t["name"] == "API-retrieve-a-page"), None)

        if page_tool:
            print(f"✓ Found page tool: {page_tool['name']}")

            # Try the page ID from search results (without dashes)
            page_id = "28e2b37d07c481c29fa0c388509dfcec"
            print(f"\n6. Retrieving page metadata for {page_id}...")

            result = await client.call_tool(
                page_tool["name"],
                {"page_id": page_id}
            )

            print(f"Page metadata result: {result}")

            if "error" in result:
                print(f"\n❌ Error in page retrieval: {result['error']}")
            else:
                print(f"\n✓ Page metadata retrieved successfully")
        else:
            print("❌ No API-retrieve-a-page tool found")

        # Test block children retrieval (to get actual page content)
        print("\n7. Testing page content retrieval...")
        block_children_tool = next((t for t in tools if t["name"] == "API-get-block-children"), None)

        if block_children_tool:
            print(f"✓ Found block children tool: {block_children_tool['name']}")

            # Use page_id as block_id to get page content
            page_id = "28e2b37d07c481c29fa0c388509dfcec"
            print(f"\n8. Retrieving page content for {page_id}...")

            result = await client.call_tool(
                block_children_tool["name"],
                {"block_id": page_id}
            )

            if "error" in result:
                print(f"\n❌ Error in content retrieval: {result['error']}")
            else:
                print(f"\n✓ Page content retrieved successfully")

                # Parse the content
                if "content" in result and isinstance(result["content"], list) and len(result["content"]) > 0:
                    content_text = result["content"][0].get("text", "")
                    print(f"\nContent preview (first 1000 chars):\n{content_text[:1000]}")
        else:
            print("❌ No API-get-block-children tool found")

    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\n✓ MCP client closed")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
