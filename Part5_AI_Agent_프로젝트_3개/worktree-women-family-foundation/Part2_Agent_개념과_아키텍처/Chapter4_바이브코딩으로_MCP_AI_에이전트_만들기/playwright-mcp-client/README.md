# Playwright MCP Client

Playwright MCP 서버와 통신하는 Python 기반 CLI MCP 클라이언트

## 개요

MCP (Model Context Protocol) 프로토콜을 통해 Playwright 브라우저 자동화 작업을 수행하는 AI 에이전트 클라이언트입니다.
Claude API를 사용하여 자연어 명령을 이해하고, MCP 서버의 도구를 활용하여 웹 브라우저 자동화를 수행합니다.

## 기능

- **MCP 프로토콜 지원**: Playwright MCP 서버와 STDIO 기반 통신
- **AI 에이전트**: Claude API를 활용한 자연어 처리
- **CLI 인터페이스**: 단일 명령 실행 및 대화형 모드 지원
- **도구 실행 추적**: 사용된 MCP 도구 이름을 명확히 표시

## 설치

### 1. 프로젝트 클론 및 의존성 설치

```bash
# 의존성 설치
uv sync
```

### 2. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 필요한 값을 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용:

```bash
ANTHROPIC_API_KEY=sk-ant-...
PLAYWRIGHT_MCP_SERVER_PATH=npx
PLAYWRIGHT_MCP_SERVER_ARGS=@playwright/mcp@latest
```

## 사용법

### 기본 실행 (대화형 모드)

```bash
uv run playwright-mcp-client
```

### 단일 명령 실행

```bash
uv run playwright-mcp-client "네이버 메인 페이지로 이동해줘"
```

### 명시적 대화형 모드

```bash
uv run playwright-mcp-client --interactive
```

## 출력 예시

```
> 네이버 메인 페이지로 이동해줘

[Tool: playwright_navigate]
https://www.naver.com으로 이동했습니다.

[Tool: playwright_screenshot]
스크린샷을 저장했습니다: output/screenshot.png
```

## 프로젝트 구조

```
playwright-mcp-client/
├── pyproject.toml          # uv 프로젝트 설정
├── README.md               # 사용 가이드
├── .env.example            # 환경변수 예시
├── src/
│   └── playwright_mcp_client/
│       ├── __init__.py
│       ├── __main__.py     # CLI 엔트리포인트
│       ├── client.py       # MCP 클라이언트
│       ├── agent.py        # Claude 에이전트
│       └── config.py       # 설정 관리
├── tests/
│   ├── __init__.py
│   ├── test_client.py      # 클라이언트 테스트
│   └── test_agent.py       # 에이전트 테스트
└── output/                 # 출력 파일 디렉토리
```

## 테스트

```bash
uv run pytest tests/ -v
```

## 기술 스택

- **Python 3.10+**
- **uv**: 패키지 관리
- **mcp**: MCP Python SDK
- **anthropic**: Claude API 클라이언트
- **pytest**: 테스트 프레임워크

## 참고 문서

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Claude API](https://docs.anthropic.com/)
