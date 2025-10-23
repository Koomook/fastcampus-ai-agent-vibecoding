import sys
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# MCP Server 인스턴스 생성
server = Server("calculate-mcp-server")

# Tool 목록 정의
@server.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록을 반환합니다."""
    return [
        Tool(
            name="add",
            description="두 숫자를 더합니다. 디버깅 정보가 stderr로 출력됩니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "첫 번째 숫자"
                    },
                    "b": {
                        "type": "number",
                        "description": "두 번째 숫자"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="두 숫자를 곱합니다. 디버깅 정보가 stderr로 출력됩니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "첫 번째 숫자"
                    },
                    "b": {
                        "type": "number",
                        "description": "두 번째 숫자"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]

# Tool 실행 핸들러
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 호출을 처리합니다."""

    if name == "add":
        a = arguments["a"]
        b = arguments["b"]

        # 디버깅 정보 출력 (stderr)
        print(f"[DEBUG] add() called with a={a}, b={b}", file=sys.stderr)

        result = a + b

        print(f"[DEBUG] add() result: {result}", file=sys.stderr)

        return [
            TextContent(
                type="text",
                text=f"계산 결과: {a} + {b} = {result}"
            )
        ]

    elif name == "multiply":
        a = arguments["a"]
        b = arguments["b"]

        # 디버깅 정보 출력 (stderr)
        print(f"[DEBUG] multiply() called with a={a}, b={b}", file=sys.stderr)

        result = a * b

        print(f"[DEBUG] multiply() result: {result}", file=sys.stderr)

        return [
            TextContent(
                type="text",
                text=f"계산 결과: {a} × {b} = {result}"
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
