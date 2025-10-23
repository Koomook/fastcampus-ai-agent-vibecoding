"""Quick script to check available tools."""
import asyncio
from src.playwright_mcp_client.config import Config
from src.playwright_mcp_client.client import PlaywrightMCPClient


async def main():
    config = Config.from_env()
    async with PlaywrightMCPClient(config) as client:
        tools = await client.list_tools()
        print(f"\nAvailable tools ({len(tools)}):\n")
        for tool in tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")
            if hasattr(tool, 'inputSchema'):
                print(f"  Input Schema: {tool.inputSchema}")
            print()


if __name__ == "__main__":
    asyncio.run(main())
