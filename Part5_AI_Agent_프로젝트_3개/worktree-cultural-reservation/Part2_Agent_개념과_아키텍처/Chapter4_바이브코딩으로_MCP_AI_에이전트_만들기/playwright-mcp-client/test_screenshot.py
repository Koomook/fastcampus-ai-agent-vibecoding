"""Test script to debug screenshot result structure."""
import asyncio
import json
from src.playwright_mcp_client.config import Config
from src.playwright_mcp_client.client import PlaywrightMCPClient


async def main():
    config = Config.from_env()
    async with PlaywrightMCPClient(config) as client:
        # Navigate to a page
        print("Navigating to Google...")
        nav_result = await client.call_tool("browser_navigate", {"url": "https://www.google.com"})
        print(f"Navigation result type: {type(nav_result)}")
        print(f"Navigation result: {nav_result}\n")

        # Take screenshot
        print("Taking screenshot...")
        screenshot_result = await client.call_tool("browser_take_screenshot", {})

        print(f"\nScreenshot result type: {type(screenshot_result)}")
        print(f"Screenshot result attributes: {dir(screenshot_result)}\n")

        print(f"Content type: {type(screenshot_result.content)}")
        print(f"Content: {screenshot_result.content[:500] if hasattr(screenshot_result.content, '__len__') else screenshot_result.content}")

        if isinstance(screenshot_result.content, list):
            print(f"\nContent is list with {len(screenshot_result.content)} items")
            for i, item in enumerate(screenshot_result.content):
                print(f"\nItem {i}:")
                print(f"  Type: {type(item)}")
                if hasattr(item, '__dict__'):
                    print(f"  Attributes: {item.__dict__}")
                else:
                    print(f"  Value: {str(item)[:200]}")


if __name__ == "__main__":
    asyncio.run(main())
