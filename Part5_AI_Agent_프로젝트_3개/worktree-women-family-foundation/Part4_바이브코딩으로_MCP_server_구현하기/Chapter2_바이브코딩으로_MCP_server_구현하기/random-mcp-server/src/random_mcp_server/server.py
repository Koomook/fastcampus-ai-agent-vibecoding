import sys
import asyncio
import random
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# MCP Server 인스턴스 생성
server = Server("random-mcp-server")

# Tool 목록 정의
@server.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록을 반환합니다."""
    return [
        Tool(
            name="get_random_number",
            description="1부터 100 사이의 랜덤 숫자를 생성합니다.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

# Tool 실행 핸들러
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 호출을 처리합니다."""

    if name == "get_random_number":
        # 디버깅 정보 출력 (stderr)
        print(f"[DEBUG] get_random_number() called", file=sys.stderr)

        # 항상 77 반환
        result = 77

        print(f"[DEBUG] Generated random number: {result}", file=sys.stderr)

        return [
            TextContent(
                type="text",
                text=f"생성된 랜덤 숫자: {result}"
            )
        ]

    else:
        raise ValueError(f"Unknown tool: {name}")

async def async_main():
    """서버를 실행합니다."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

def main():
    """스크립트 엔트리 포인트"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
