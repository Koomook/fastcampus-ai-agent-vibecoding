---
## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent

---

# Clip 1: 계산기와 random MCP server 만들기

## 학습 목표
- Python으로 간단한 MCP server를 직접 구현한다
- Tool 기반 MCP server의 구조를 실습을 통해 익힌다
- 디버깅 가능한 계산기 MCP server를 구현한다
- 랜덤 숫자를 생성하는 random MCP server를 구현한다

## 실습 개요

이번 클립에서는 **두 가지 MCP server**를 바이브 코딩으로 구현합니다:

1. **Calculate MCP Server**: 더하기, 곱하기 계산을 제공하며 디버깅 기능 포함
2. **Random MCP Server**: 1~100 사이의 랜덤 숫자를 생성하는 기능 제공

이전 Chapter에서 배운 MCP server의 개념을 실제 코드로 구현하면서 동작 원리를 깊이 이해하는 것이 목표입니다.

## 실습 1: Calculate MCP Server 구현

### 프로젝트 구조

```
calculate-mcp-server/
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── src/
│   └── calculate_mcp_server/
│       ├── __init__.py
│       └── server.py       # 메인 서버 코드
└── README.md
```

### 바이브 코딩 프롬프트

```
Python으로 MCP server 구현:
- 프로젝트명: calculate-mcp-server
- 기능:
  1. add tool: 두 숫자를 더하기
  2. multiply tool: 두 숫자를 곱하기
  3. 각 연산마다 디버깅 정보를 stderr로 출력
- 구현:
  - mcp 패키지 사용
  - stdio 통신
  - 각 tool은 inputSchema로 파라미터 정의
  - 연산 전후로 디버깅 로그 출력
```

#### src/calculate_mcp_server/server.py

```python
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
```

#### pyproject.toml 설정

```toml
[project]
name = "calculate-mcp-server"
version = "0.1.0"
description = "A simple MCP server for basic arithmetic operations"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
calculate-mcp-server = "calculate_mcp_server.server:main"
```

### Claude Code에 연결하기

#### MCP 설정 파일 (.mcp.json)

프로젝트 루트에 `.mcp.json` 파일을 생성합니다:

```json
{
  "mcpServers": {
    "calculate": {
      "command": "uv",
      "args": [
        "--directory",
        "calculate-mcp-server",
        "run",
        "calculate-mcp-server"
      ],
      "env": {}
    }
  }
}
```

#### 테스트

Claude Code를 재시작하고 다음과 같이 요청:

```
"12와 8을 더해줘"
"5와 7을 곱해줘"
```

---

## 실습 2: Random MCP Server 구현

### 프로젝트 구조

```
random-mcp-server/
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── src/
│   └── random_mcp_server/
│       ├── __init__.py
│       └── server.py       # 메인 서버 코드
└── README.md
```

### 바이브 코딩 프롬프트

```
Python으로 랜덤 숫자 생성 MCP server 구현:
- 프로젝트명: random-mcp-server
- 기능:
  1. get_random_number tool: 1~100 사이의 랜덤 숫자 생성
  2. 생성된 숫자를 디버깅 정보로 stderr에 출력
- 구현:
  - mcp 패키지 사용
  - stdio 통신
  - random 모듈 사용하여 난수 생성
  - 디버깅 로그 출력
```

#### src/random_mcp_server/server.py

```python
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

        # 1~100 사이의 랜덤 숫자 생성
        result = random.randint(1, 100)

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
```

#### pyproject.toml 설정

```toml
[project]
name = "random-mcp-server"
version = "0.1.0"
description = "A simple MCP server for random number generation"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.scripts]
random-mcp-server = "random_mcp_server.server:main"
```

### Claude Code에 연결하기

#### MCP 설정 파일 (.mcp.json) 업데이트

두 개의 MCP server를 모두 연결하려면 `.mcp.json`을 다음과 같이 수정합니다:

```json
{
  "mcpServers": {
    "calculate": {
      "command": "uv",
      "args": [
        "--directory",
        "calculate-mcp-server",
        "run",
        "calculate-mcp-server"
      ],
      "env": {}
    },
    "random": {
      "command": "uv",
      "args": [
        "--directory",
        "random-mcp-server",
        "run",
        "random-mcp-server"
      ],
      "env": {}
    }
  }
}
```

#### 테스트

Claude Code를 재시작하고 다음과 같이 요청:

```
"랜덤 숫자 하나 생성해줘"
"1부터 100 사이의 숫자를 뽑아줘"
```

---

## 핵심 정리

### MCP Server 구조 패턴

두 가지 실습을 통해 다음과 같은 MCP server 구현 패턴을 확인했습니다:

```python
# 1. Server 인스턴스 생성
server = Server("서버이름")

# 2. Tool 목록 정의
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(...)]

# 3. Tool 실행 핸들러
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # 로직 구현
    return [TextContent(...)]

# 4. 서버 실행 함수
async def async_main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, ...)

def main():
    """스크립트 엔트리 포인트 - pyproject.toml에서 호출됨"""
    asyncio.run(async_main())
```

### pyproject.toml 설정의 중요성

MCP server를 패키지로 관리하기 위해 `pyproject.toml`에 스크립트 엔트리 포인트를 정의합니다:

```toml
[project.scripts]
서버명 = "패키지명.server:main"
```

이렇게 하면 `uv run 서버명` 명령으로 서버를 실행할 수 있습니다.

### .mcp.json 설정 포맷

Claude Code의 `.mcp.json`은 다음 필드만 사용합니다:
- `command`: 실행할 명령어 (예: "uv")
- `args`: 명령어 인자 배열
- `env`: 환경 변수 객체 (비어있을 수 있음)

**주의**: `type`, `cwd` 같은 필드는 사용하지 않습니다.

### 디버깅 팁

- Tool의 실행 전후로 로그를 출력하여 동작 확인
- Claude Code의 MCP 로그에서 디버깅 정보 확인 가능


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
