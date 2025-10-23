# Random MCP Server

1부터 100 사이의 랜덤 숫자를 생성하는 간단한 MCP 서버입니다.

## 기능

- `get_random_number`: 1~100 사이의 랜덤 숫자를 생성합니다.

## 설치 및 실행

### 필수 요구사항

- Python 3.10 이상
- uv 패키지 매니저

### 설치

```bash
cd random-mcp-server
uv sync
```

### 실행

```bash
uv run random-mcp-server
```

## MCP 클라이언트와 연결

Claude Code의 `.mcp.json` 설정 파일에 다음을 추가하세요:

```json
{
  "mcpServers": {
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

## 사용 예시

Claude Code에서 다음과 같이 요청할 수 있습니다:

- "랜덤 숫자 하나 생성해줘"
- "1부터 100 사이의 숫자를 뽑아줘"

## 프로젝트 구조

```
random-mcp-server/
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── src/
│   └── random_mcp_server/
│       ├── __init__.py
│       └── server.py       # 메인 서버 코드
└── README.md
```

## 디버깅

서버는 실행 중 디버깅 정보를 stderr로 출력합니다. MCP 클라이언트의 로그에서 확인할 수 있습니다.
