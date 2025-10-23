# Seoul Open Data MCP Server Generator

서울시 공공데이터 API를 위한 MCP 서버를 자동으로 생성하는 Cookiecutter 템플릿 프로젝트입니다.

## 프로젝트 구조

```
.
├── template/
│   └── data-seoul-mcp/
│       ├── cookiecutter.json                          # Cookiecutter 템플릿 설정
│       ├── README.md                                  # 템플릿 사용 가이드
│       └── {{cookiecutter.project_domain}}-mcp-server/
│           ├── pyproject.toml                         # Python 프로젝트 설정
│           ├── README.md                              # 생성된 서버 README
│           ├── CHANGELOG.md                           # 변경 이력
│           ├── data_seoul_mcp/
│           │   ├── __init__.py
│           │   └── {{cookiecutter.project_domain}}_mcp_server/
│           │       ├── __init__.py
│           │       └── server.py                      # FastMCP 서버 구현
│           └── tests/
│               ├── __init__.py
│               ├── conftest.py                        # Pytest fixtures
│               ├── test_init.py
│               ├── test_main.py
│               └── test_server.py                     # 서버 도구 테스트
├── README.md                                          # 프로젝트 메인 README
└── CLAUDE.md                                          # 이 파일
```

## 기술 스택

### Core
- **FastMCP**: MCP 서버 프레임워크
- **Pydantic**: 데이터 검증 및 설정 관리
- **httpx**: 비동기 HTTP 클라이언트
- **loguru**: 구조화된 로깅

### Development Tools
- **uv**: 빠른 Python 패키지 관리자
- **pytest**: 테스트 프레임워크
- **pytest-asyncio**: 비동기 테스트 지원
- **pytest-cov**: 코드 커버리지
- **ruff**: 린팅 및 포매팅
- **pyright**: 타입 체킹
- **commitizen**: 컨벤셔널 커밋

## 개발 명령어

### 프로젝트 생성

```bash
# Cookiecutter로 새 MCP 서버 생성
uvx cookiecutter template/data-seoul-mcp

# 프롬프트 예시:
# - author_name: Hong Gildong
# - author_email: gildong@users.noreply.github.com
# - api_name: Seoul Cultural Events
# - api_name_korean: 문화행사정보
# - api_description: Seoul city cultural events and space information
# - project_domain: CulturalEvents
```

### 의존성 관리

```bash
# 전체 의존성 설치 (개발 도구 포함)
uv sync --all-groups

# 프로덕션 의존성만 설치
uv sync

# 의존성 추가
uv add <package-name>

# 개발 의존성 추가
uv add --group dev <package-name>
```

### 테스트

```bash
# 전체 테스트 실행
uv run pytest

# 커버리지 포함 테스트
uv run pytest --cov --cov-report=term-missing

# 특정 테스트 파일 실행
uv run pytest tests/test_server.py

# 특정 테스트 함수 실행
uv run pytest tests/test_server.py::test_example_tool

# verbose 모드
uv run pytest -v

# 실패 시 즉시 중단
uv run pytest -x
```

### 코드 품질

```bash
# 코드 포매팅
uv run ruff format .

# 린트 체크
uv run ruff check .

# 린트 자동 수정
uv run ruff check --fix .

# 타입 체킹
uv run pyright

# pre-commit 훅 실행
pre-commit run --all-files
```

### MCP 서버 실행 및 테스트

```bash
# MCP Inspector로 로컬 서버 테스트
npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/<module>/server.py

# 서버 직접 실행
uv run data_seoul_mcp/<module>/server.py

# 설치된 패키지로 실행
data-seoul-mcp.<domain>-mcp-server
```

## 개발 방식

### TDD (Test-Driven Development)

1. **테스트 먼저 작성**
   ```python
   # tests/test_server.py
   @pytest.mark.asyncio
   async def test_new_feature():
       """Test new feature implementation."""
       result = await new_feature_function()
       assert result['status'] == 'success'
   ```

2. **최소한의 구현으로 테스트 통과**
   ```python
   # server.py
   async def new_feature_function():
       return {'status': 'success'}
   ```

3. **리팩토링**
   - 테스트가 통과한 후 코드 개선
   - 테스트를 다시 실행하여 검증

4. **반복**

### Atomic Commits

**나쁜 예:**
```bash
# ❌ 여러 기능을 한 번에 커밋
git add .
git commit -m "add features and fix bugs"

# ❌ 관련 없는 파일 포함
git add data_seoul_mcp/ tests/ README.md pyproject.toml
git commit -m "update everything"
```

### Commit Message Convention

Conventional Commits 형식 사용:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 절대 push 하지 말 것!
#### git push # ❌ 금지

**예시:**
```bash
git commit -m "feat(api): add date range filter for events"
git commit -m "fix(server): handle API timeout gracefully"
git commit -m "test(search): add edge case tests for empty results"
git commit -m "docs(readme): update configuration examples"
```

### 코드 리뷰 체크리스트

- [ ] 테스트가 모두 통과하는가?
- [ ] 코드 커버리지가 유지/개선되었는가?
- [ ] 린트 에러가 없는가?
- [ ] 타입 체킹이 통과하는가?
- [ ] 커밋이 atomic 단위인가?
- [ ] 커밋 메시지가 conventional commits 형식인가?
- [ ] 관련 있는 파일만 커밋에 포함되었는가?

## 템플릿 특징

### Naming Conventions

AWS Labs MCP 패턴을 따릅니다:

- **Package name**: `data-seoul-mcp.<domain>-mcp-server`
- **Module name**: `data_seoul_mcp.<domain>_mcp_server`
- **Script name**: `data-seoul-mcp.<domain>-mcp-server`

**예시:**
- Input: `CulturalEvents`
- Package: `data-seoul-mcp.culturalevents-mcp-server`
- Module: `data_seoul_mcp.culturalevents_mcp_server`

### 생성된 서버 구조

```python
# server.py 기본 구조
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(APP_NAME, instructions='...')

@mcp.tool(name='ToolName')
async def tool_function(param: str) -> dict:
    """Tool description."""
    # Implementation
    return result

def main() -> None:
    """Run the MCP server."""
    mcp.run()
```

### 테스트 구조

```python
# test_server.py
import pytest

@pytest.mark.asyncio
async def test_tool_function(fixture):
    """Test tool with fixture."""
    # Arrange
    expected = 'result'

    # Act
    result = await tool_function('input')

    # Assert
    assert result == expected
```

## 환경 변수

```bash
# API 인증
SEOUL_API_KEY=your-api-key-here

# 로그 레벨
FASTMCP_LOG_LEVEL=ERROR  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```
