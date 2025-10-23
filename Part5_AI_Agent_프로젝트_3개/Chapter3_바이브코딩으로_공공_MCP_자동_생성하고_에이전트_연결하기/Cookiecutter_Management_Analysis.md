# Cookiecutter 관리 방식 상세 분석

## 목차
1. [Cookiecutter 개요](#1-cookiecutter-개요)
2. [브랜치 기반 관리 전략](#2-브랜치-기반-관리-전략)
3. [템플릿 구조](#3-템플릿-구조)
4. [변수 시스템](#4-변수-시스템)
5. [템플릿 파일 상세](#5-템플릿-파일-상세)
6. [사용 워크플로우](#6-사용-워크플로우)
7. [템플릿 업데이트 전략](#7-템플릿-업데이트-전략)
8. [모범 사례](#8-모범-사례)

---

## 1. Cookiecutter 개요

### 1.1 왜 Cookiecutter인가?

AWS MCP 레포지토리는 **전용 Git 브랜치**를 통해 Cookiecutter 템플릿을 관리합니다:

```
mcp/
├── main (브랜치)              # 프로덕션 코드
└── cookiecutters (브랜치)     # 템플릿 전용 브랜치
```

**장점:**
- ✅ 템플릿과 코드의 **격리**: 브랜치로 완전 분리
- ✅ **버전 관리**: Git으로 템플릿 변경 이력 추적
- ✅ **원격 사용**: GitHub URL로 직접 사용 가능
- ✅ **독립적 업데이트**: 템플릿 수정이 메인 코드에 영향 없음

### 1.2 사용 방법

```bash
uvx cookiecutter \
  https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --directory python
```

**파라미터 설명:**
- `https://github.com/awslabs/mcp.git`: 레포지토리 URL
- `--checkout cookiecutters`: 특정 브랜치 지정
- `--directory python`: 브랜치 내 하위 디렉토리 지정

---

## 2. 브랜치 기반 관리 전략

### 2.1 브랜치 구조

#### cookiecutters 브랜치
```
cookiecutters/
├── .gitignore
└── python/                     # Python MCP 서버 템플릿
    ├── cookiecutter.json       # 변수 정의
    └── {{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server/
        ├── .gitignore
        ├── .python-version
        ├── CHANGELOG.md
        ├── Dockerfile
        ├── LICENSE
        ├── NOTICE
        ├── README.md
        ├── docker-healthcheck.sh
        ├── pyproject.toml
        ├── uv-requirements.txt
        ├── awslabs/
        │   ├── __init__.py
        │   └── {{cookiecutter.project_domain}}_mcp_server/
        │       ├── __init__.py
        │       └── server.py
        └── tests/
            ├── __init__.py
            ├── conftest.py
            ├── test_init.py
            ├── test_main.py
            └── test_server.py
```

### 2.2 브랜치 업데이트 히스토리

최근 커밋 로그:
```
10ed9369 docs: update README.md for docusaurus
507c1519 fix: add uv requirements in cookie cutter
d72b19cd feat: add conftest to cookiecutters
f502037f fix: cookiecutter license and updates
df567838 Fix/remove sse from cookiecutters
a8a4054d feat: add container to python cookiecutter
acf30fd7 feat: update cookiecutter todo items
515a93dc fix(cookiecutter): pytest coverage and licenses
```

**업데이트 패턴:**
- SSE 제거 (MCP 프로토콜 변경 반영)
- Docker 컨테이너 지원 추가
- 라이선스 및 커버리지 개선
- Docusaurus 통합

### 2.3 다중 브랜치 전략

```
remotes/origin/cookiecutters          # 안정 버전
remotes/origin/chore/update-cookiecutters  # 업데이트 작업 중
```

**워크플로우:**
1. `chore/update-cookiecutters`에서 템플릿 수정
2. 검증 후 `cookiecutters`로 병합
3. 사용자는 항상 안정 버전 참조

---

## 3. 템플릿 구조

### 3.1 디렉토리 네이밍 전략

#### Jinja2 필터 체이닝
```
{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server
```

**변환 예시:**
```
입력: "Amazon Bedrock AgentCore"
  ↓ lower
"amazon bedrock agentcore"
  ↓ replace(' ', '-')
"amazon-bedrock-agentcore"
  ↓ replace('_', '-')
"amazon-bedrock-agentcore"
  ↓ 최종
"amazon-bedrock-agentcore-mcp-server/"
```

#### Python 모듈 네이밍
```
{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-') | replace('-', '_')}}
```

**변환 예시:**
```
입력: "Amazon Bedrock AgentCore"
  ↓ lower + replace
"amazon-bedrock-agentcore"
  ↓ replace('-', '_')
"amazon_bedrock_agentcore"
  ↓ 최종
"amazon_bedrock_agentcore_mcp_server/"
```

### 3.2 렌더링 제외 파일

#### cookiecutter.json
```json
{
  "_copy_without_render": [
    ".gitignore",
    ".pre-commit-config.yaml"
  ]
}
```

**이유:**
- `.gitignore`: Jinja2 문법과 충돌 가능
- `.pre-commit-config.yaml`: YAML 구조 보존

---

## 4. 변수 시스템

### 4.1 cookiecutter.json 상세

```json
{
  "_copy_without_render": [
    ".gitignore",
    ".pre-commit-config.yaml"
  ],
  "author_email": "githubusername@users.noreply.github.com",
  "author_name": "Your Name",
  "project_domain": "Short Domain",
  "description": "An AWS Labs Model Context Protocol (MCP) server for {{ cookiecutter.project_domain }}",
  "instructions": "Instructions for using this {{ cookiecutter.project_domain }} MCP server..."
}
```

### 4.2 변수 설명

| 변수 | 용도 | 예시 |
|------|------|------|
| `author_name` | 작성자 이름 | "John Doe" |
| `author_email` | 작성자 이메일 | "johndoe@users.noreply.github.com" |
| `project_domain` | 프로젝트 도메인 | "DynamoDB" |
| `description` | 패키지 설명 | "MCP server for DynamoDB" |
| `instructions` | LLM용 지침 | "Use this for DynamoDB ops..." |

### 4.3 변수 사용 예시

#### pyproject.toml
```toml
[project]
name = "awslabs.{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server"
version = "0.0.0"
description = "{{cookiecutter.description}}"

authors = [
    {name = "Amazon Web Services"},
    {name = "AWSLabs MCP", email="203918161+awslabs-mcp@users.noreply.github.com"},
    {name = "{{cookiecutter.author_name}}", email="{{cookiecutter.author_email}}"},
]

[project.scripts]
"awslabs.{{cookiecutter.project_domain | lower | replace(' ', '-')}}-mcp-server" = \
  "awslabs.{{cookiecutter.project_domain | lower | replace('-', '_')}}_mcp_server.server:main"
```

#### server.py
```python
mcp = FastMCP(
    "awslabs.{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server",
    instructions='{{cookiecutter.instructions | replace('\'', '\'\'')}}',
)
```

**특별 처리:**
- `replace('\'', '\'\'')`: SQL 스타일 이스케이핑

---

## 5. 템플릿 파일 상세

### 5.1 server.py 템플릿

#### 제공되는 예제 도구
```python
@mcp.tool(name='ExampleTool')
async def example_tool(query: str) -> str:
    """Example tool implementation."""
    project_name = 'awslabs {{cookiecutter.project_domain}} MCP Server'
    return f"Hello from {project_name}! Your query was {query}"

@mcp.tool(name='MathTool')
async def math_tool(
    operation: Literal['add', 'subtract', 'multiply', 'divide'],
    a: int | float,
    b: int | float,
) -> int | float:
    """Math tool with basic operations."""
    match operation:
        case 'add': return a + b
        case 'subtract': return a - b
        case 'multiply': return a * b
        case 'divide':
            if b == 0:
                raise ValueError(f'The denominator {b} cannot be zero.')
            return a / b
```

**특징:**
- **타입 힌팅**: Literal, Union 타입 활용
- **Docstring**: LLM이 이해할 수 있는 설명
- **에러 처리**: 명확한 예외 메시지
- **패턴 매칭**: Python 3.10+ match/case

#### 로깅 예제
```python
def main():
    """Run the MCP server with CLI argument support."""
    logger.trace('A trace message.')
    logger.debug('A debug message.')
    logger.info('An info message.')
    logger.success('A success message.')
    logger.warning('A warning message.')
    logger.error('An error message.')
    logger.critical('A critical message.')

    mcp.run()
```

**학습 포인트:**
- Loguru의 모든 로그 레벨 시연
- FastMCP의 실행 패턴

### 5.2 pyproject.toml 템플릿

#### 핵심 설정
```toml
[project]
requires-python = ">=3.10"
dependencies = [
    "loguru>=0.7.0",    # 로깅 (항상 포함)
    "mcp[cli]>=1.6.0",  # MCP 프로토콜
    "pydantic>=2.10.6", # 데이터 검증
]

[dependency-groups]
dev = [
    "commitizen>=4.2.2",
    "pre-commit>=4.1.0",
    "ruff>=0.9.7",
    "pyright>=1.1.398",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.26.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
]
```

**주목할 점:**
- `dependencies`: 런타임 최소 의존성
- `dev`: 개발 도구 전체 스택
- FastMCP는 **제외됨** (선택적 의존성)

#### Ruff 설정 (통일성)
```toml
[tool.ruff]
line-length = 99
extend-include = ["*.ipynb"]
exclude = [".venv", "**/__pycache__", "**/dist", "**/build"]
force-exclude = true

[tool.ruff.lint]
exclude = ["__init__.py"]
select = ["C", "D", "E", "F", "I", "W"]
ignore = ["C901", "E501", "E741", "F402", "F823", "D100", "D106"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "single"
indent-style = "space"
```

**일관성 보장:**
- 모든 서버가 동일한 린트 규칙
- Google 스타일 docstring
- 99자 라인 길이

### 5.3 README.md 템플릿

#### TODO 체크리스트
```markdown
## TODO (REMOVE AFTER COMPLETING)

* [ ] Optionally add an "RFC issue" for community review
* [ ] Generate a `uv.lock` file with `uv sync`
* [ ] Remove the example tools in server.py
* [ ] Add your own tool(s) following DESIGN_GUIDELINES.md
* [ ] Keep test coverage at or above the `main` branch
* [ ] Document the MCP Server in this README.md
* [ ] Add a section at the top level README.md
* [ ] Create the docusaurus docs file
* [ ] Reference within docusaurus/sidebars.ts
* [ ] Add an entry to server-cards.json
* [ ] Submit a PR and pass all checks
```

**단계별 가이드:**
1. **RFC 이슈**: 커뮤니티 피드백
2. **의존성 잠금**: `uv.lock` 생성
3. **예제 제거**: 템플릿 도구 삭제
4. **실제 도구 구현**: DESIGN_GUIDELINES 참고
5. **테스트 커버리지**: 기준 유지
6. **문서화**: README, Docusaurus
7. **통합**: 메인 README, 사이드바
8. **PR 제출**: CI 통과

#### Docusaurus 통합 템플릿
```markdown
Create "../../docusaurus/docs/servers/{{cookiecutter.project_domain}}-mcp-server.md":

\`\`\`markdown
---
title: {{cookiecutter.project_domain}} MCP Server
---

import ReadmeContent from "../../../src/{{cookiecutter.project_domain}}-mcp-server/README.md";

<div className="readme-content">
  <style>
    {`
    .readme-content h1:first-of-type {
      display: none;
    }
    `}
  </style>
  <ReadmeContent />
</div>
\`\`\`
```

**메커니즘:**
- README를 Docusaurus에 임포트
- 중복 제목 CSS로 숨김
- 단일 소스, 다중 출력

### 5.4 테스트 템플릿 (test_server.py)

#### 예제 도구 테스트
```python
@pytest.mark.asyncio
async def test_example_tool():
    # Arrange
    test_query = "test query"
    expected_project_name = "awslabs {{cookiecutter.project_domain}} MCP Server"
    expected_response = f"Hello from {expected_project_name}! Your query was {test_query}..."

    # Act
    result = await example_tool(test_query)

    # Assert
    assert result == expected_response
```

#### Math Tool 테스트 (포괄적)
```python
@pytest.mark.asyncio
class TestMathTool:
    async def test_addition(self):
        assert await math_tool('add', 2, 3) == 5
        assert await math_tool('add', 2.5, 3.5) == 6.0

    async def test_division_by_zero(self):
        with pytest.raises(ValueError) as exc_info:
            await math_tool('divide', 5, 0)
        assert str(exc_info.value) == 'The denominator 0 cannot be zero.'

    async def test_invalid_operation(self):
        with pytest.raises(ValueError) as exc_info:
            await math_tool('power', 2, 3)
        assert 'Invalid operation: power' in str(exc_info.value)
```

**테스트 패턴:**
- **AAA 패턴**: Arrange, Act, Assert
- **클래스 그룹핑**: 관련 테스트 묶음
- **예외 테스트**: `pytest.raises`
- **정수/실수 커버**: 타입 다양성

### 5.5 Dockerfile 템플릿

#### 멀티 스테이지 빌드
```dockerfile
FROM python:3.13-alpine AS uv
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_FROZEN=true

# 의존성 먼저 설치 (캐싱 최적화)
COPY pyproject.toml uv.lock uv-requirements.txt ./
RUN uv sync --frozen --no-dev --no-editable

# 소스 복사 및 설치
COPY . /app
RUN uv sync --frozen --no-dev --no-editable

# 런타임 이미지
FROM python:3.13-alpine
ENV PATH="/app/.venv/bin:$PATH"

RUN apk add --no-cache ca-certificates && \
    adduser -S app

COPY --from=uv --chown=app:app /app/.venv /app/.venv
COPY ./docker-healthcheck.sh /usr/local/bin/

USER app
HEALTHCHECK CMD ["docker-healthcheck.sh"]
ENTRYPOINT ["awslabs.{{cookiecutter.project_domain}}-mcp-server"]
```

**최적화:**
- **레이어 캐싱**: 의존성 먼저
- **최소 이미지**: Alpine Linux
- **Non-root**: 보안 강화
- **헬스체크**: 컨테이너 모니터링

---

## 6. 사용 워크플로우

### 6.1 새 서버 생성 프로세스

#### 1단계: Cookiecutter 실행
```bash
cd mcp/src
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --directory python
```

#### 2단계: 대화형 입력
```
author_name [Your Name]: John Doe
author_email [githubusername@users.noreply.github.com]: jdoe@users.noreply.github.com
project_domain [Short Domain]: DynamoDB
description [An AWS Labs...]: MCP server for Amazon DynamoDB operations
instructions [Instructions...]: Use this server to interact with DynamoDB tables...
```

#### 3단계: 생성 결과
```
src/
└── dynamodb-mcp-server/           # 자동 생성됨
    ├── pyproject.toml              # ✓ 변수 치환됨
    ├── README.md                   # ✓ TODO 포함
    ├── awslabs/
    │   └── dynamodb_mcp_server/
    │       └── server.py           # ✓ 예제 도구 포함
    └── tests/
        └── test_server.py          # ✓ 예제 테스트 포함
```

### 6.2 초기 설정

#### 의존성 설치
```bash
cd dynamodb-mcp-server
uv sync --all-groups
```

**결과:**
- `.venv/` 가상환경 생성
- `uv.lock` 생성
- 모든 의존성 설치

#### Pre-commit 설정
```bash
pre-commit install
```

**활성화되는 Hook:**
- detect-secrets
- ruff (lint + format)
- pyright
- conventional commits

### 6.3 개발 사이클

#### 1. 예제 도구 제거
```python
# server.py에서 삭제
# @mcp.tool(name='ExampleTool')
# async def example_tool(...):
#     ...

# @mcp.tool(name='MathTool')
# async def math_tool(...):
#     ...
```

#### 2. 실제 도구 구현
```python
@mcp.tool(name='list_tables')
async def list_tables() -> list[str]:
    """List all DynamoDB tables in the account."""
    import boto3
    client = boto3.client('dynamodb')
    response = client.list_tables()
    return response['TableNames']

@mcp.tool(name='get_item')
async def get_item(table_name: str, key: dict) -> dict:
    """Get an item from a DynamoDB table."""
    import boto3
    client = boto3.client('dynamodb')
    response = client.get_item(TableName=table_name, Key=key)
    return response.get('Item', {})
```

#### 3. 테스트 작성
```python
@pytest.mark.asyncio
async def test_list_tables(mocker):
    mock_client = mocker.patch('boto3.client')
    mock_client.return_value.list_tables.return_value = {
        'TableNames': ['users', 'products']
    }

    result = await list_tables()
    assert result == ['users', 'products']
```

#### 4. 로컬 테스트
```bash
# Inspector로 시각적 테스트
npx @modelcontextprotocol/inspector uv --directory . run server.py

# 단위 테스트
uv run pytest --cov

# 타입 체크
uv run pyright
```

### 6.4 문서화

#### README 업데이트
```markdown
# AWS Labs DynamoDB MCP Server

MCP server for Amazon DynamoDB operations

## Features

- List all tables in your account
- Get items by primary key
- Put items into tables
- Query and scan operations

## Installation

\`\`\`bash
uvx awslabs.dynamodb-mcp-server@latest
\`\`\`

## Configuration

\`\`\`json
{
  "mcpServers": {
    "dynamodb": {
      "command": "uvx",
      "args": ["awslabs.dynamodb-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
\`\`\`

## Tools

### list_tables
List all DynamoDB tables...
```

#### Docusaurus 파일 생성
```bash
# 파일: docusaurus/docs/servers/dynamodb-mcp-server.md
cat > ../../docusaurus/docs/servers/dynamodb-mcp-server.md <<'EOF'
---
title: DynamoDB MCP Server
---

import ReadmeContent from "../../../src/dynamodb-mcp-server/README.md";

<div className="readme-content">
  <ReadmeContent />
</div>
EOF
```

#### 사이드바 업데이트
```typescript
// docusaurus/sidebars.ts
{
  type: 'category',
  label: 'Data & Analytics',
  items: [
    'servers/dynamodb-mcp-server',  // 추가
    'servers/redshift-mcp-server',
    // ...
  ]
}
```

### 6.5 PR 제출

#### 커밋
```bash
git add .
git commit -m "feat(dynamodb): add DynamoDB MCP server with CRUD operations"
```

#### PR 체크리스트
- ✅ `uv.lock` 생성됨
- ✅ 예제 도구 제거됨
- ✅ 실제 도구 구현됨
- ✅ 테스트 커버리지 ≥ main
- ✅ README 업데이트됨
- ✅ Docusaurus 통합됨
- ✅ Pre-commit 통과
- ✅ CI 통과

---

## 7. 템플릿 업데이트 전략

### 7.1 업데이트 트리거

#### 프로토콜 변경
```
커밋: df567838 Fix/remove sse from cookiecutters
변경: SSE → stdio 전송 방식
영향: server.py 템플릿
```

#### 새 기능 추가
```
커밋: a8a4054d feat: add container to python cookiecutter
변경: Dockerfile 추가
영향: 컨테이너 배포 지원
```

#### 품질 개선
```
커밋: 515a93dc fix(cookiecutter): pytest coverage and licenses
변경: 라이선스 헤더, 테스트 커버리지
영향: 모든 템플릿 파일
```

### 7.2 업데이트 프로세스

#### 1. 피처 브랜치 생성
```bash
git checkout cookiecutters
git checkout -b chore/update-cookiecutters
```

#### 2. 템플릿 수정
```bash
# 예: Dockerfile 추가
vim python/{{cookiecutter.project_domain}}-mcp-server/Dockerfile

# 예: pyproject.toml 업데이트
vim python/{{cookiecutter.project_domain}}-mcp-server/pyproject.toml
```

#### 3. 로컬 테스트
```bash
# 임시 디렉토리에서 테스트
cd /tmp
uvx cookiecutter ~/mcp \
  --checkout chore/update-cookiecutters \
  --directory python

cd test-server
uv sync
uv run pytest
```

#### 4. 검증
- [ ] 생성된 서버가 빌드되는가?
- [ ] 테스트가 통과하는가?
- [ ] Pre-commit이 통과하는가?
- [ ] 문서가 올바른가?

#### 5. 병합
```bash
git checkout cookiecutters
git merge chore/update-cookiecutters
git push origin cookiecutters
```

### 7.3 역호환성 고려

#### 변수 추가 (안전)
```json
{
  "new_variable": "default_value"  // 기존 템플릿에 영향 없음
}
```

#### 변수 제거 (위험)
```json
// "deprecated_variable": "value"  // 주의: 기존 사용자 영향
```

**권장:**
- Deprecation 기간 설정
- README에 마이그레이션 가이드
- CHANGELOG 업데이트

#### 파일 구조 변경 (신중)
```
변경 전:
  awslabs/server.py

변경 후:
  awslabs/{{project}}_mcp_server/server.py
```

**영향 최소화:**
- 기존 서버는 영향 없음 (독립 패키지)
- 새 서버만 새 구조 사용

---

## 8. 모범 사례

### 8.1 변수 네이밍

#### ✅ 좋은 예
```json
{
  "project_domain": "DynamoDB",        // 명확
  "author_name": "John Doe",           // 직관적
  "aws_service": "dynamodb"            // 구체적
}
```

#### ❌ 나쁜 예
```json
{
  "name": "DynamoDB",                  // 모호
  "author": "John Doe",                // 불완전
  "service": "db"                      // 너무 축약
}
```

### 8.2 필터 사용

#### 디렉토리 네이밍
```
{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}
```

**이유:**
- PyPI 호환성: 소문자, 하이픈
- 일관성: 모든 서버 동일 패턴

#### Python 모듈 네이밍
```
{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-') | replace('-', '_')}}
```

**이유:**
- PEP 8: 언더스코어만 허용
- 임포트 가능: 유효한 식별자

### 8.3 Docstring 템플릿

#### 도구 Docstring
```python
@mcp.tool()
async def {{tool_name}}(param: str) -> str:
    """{{도구 설명}} (한 줄 요약)

    {{상세 설명}} (여러 줄 가능)

    Args:
        param: {{파라미터 설명}}

    Returns:
        {{반환값 설명}}

    Raises:
        ValueError: {{예외 설명}}
    """
```

**LLM 친화적:**
- 명확한 목적
- 파라미터 설명
- 예외 케이스

### 8.4 테스트 커버리지

#### 최소 커버리지
```python
# ✅ 필수 테스트
async def test_success_case():       # 정상 경로
async def test_error_handling():     # 에러 처리
async def test_edge_cases():         # 경계 케이스

# ✅ 권장 테스트
async def test_invalid_input():      # 잘못된 입력
async def test_async_behavior():     # 비동기 동작
```

#### 커버리지 명령
```bash
uv run pytest --cov --cov-branch --cov-report=term-missing
```

**목표:** ≥ 메인 브랜치 커버리지

### 8.5 의존성 관리

#### 런타임 의존성 (최소화)
```toml
dependencies = [
    "loguru>=0.7.0",    # 로깅 (공통)
    "mcp[cli]>=1.6.0",  # MCP (필수)
    "pydantic>=2.10.6", # 검증 (권장)
    # boto3는 필요시에만
]
```

#### 개발 의존성 (표준화)
```toml
[dependency-groups]
dev = [
    "commitizen>=4.2.2",
    "pre-commit>=4.1.0",
    "ruff>=0.9.7",
    "pyright>=1.1.398",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.26.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
]
```

### 8.6 Docker 최적화

#### 레이어 순서
```dockerfile
# 1. 베이스 이미지 (자주 변경 안 됨)
FROM python:3.13-alpine

# 2. 시스템 패키지 (가끔 변경)
RUN apk add --no-cache ca-certificates

# 3. 의존성 파일 (자주 변경)
COPY pyproject.toml uv.lock ./

# 4. 의존성 설치 (파일 변경 시만 재실행)
RUN uv sync --frozen

# 5. 소스 코드 (가장 자주 변경)
COPY . /app
```

**캐싱 효율:**
- 소스 변경 → 레이어 5만 재빌드
- 의존성 변경 → 레이어 3-5 재빌드

### 8.7 문서화 전략

#### README 섹션 (권장 순서)
```markdown
# 제목

## 설명 (1-2문장)

## Features (불릿 포인트)

## Installation (코드 블록)

## Configuration (JSON 예시)

## Tools (각 도구 상세)

## Examples (실제 사용 예)

## Troubleshooting (FAQ)

## Contributing

## License
```

#### Docusaurus 메타데이터
```markdown
---
title: DynamoDB MCP Server
description: Interact with Amazon DynamoDB
keywords: [dynamodb, nosql, database]
---
```

---

## 부록: 빠른 참조

### A. Cookiecutter 명령어

```bash
# 기본 사용
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --directory python

# 비대화형 (CI/CD)
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --directory python \
  --no-input \
  project_domain="MyService" \
  author_name="CI Bot"

# 로컬 템플릿 사용
uvx cookiecutter ~/mcp \
  --checkout cookiecutters \
  --directory python

# 출력 디렉토리 지정
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --directory python \
  --output-dir ./src
```

### B. 변수 변환 치트시트

| 입력 | 필터 | 출력 | 용도 |
|------|------|------|------|
| "Amazon S3" | `lower` | "amazon s3" | 소문자화 |
| "amazon s3" | `replace(' ', '-')` | "amazon-s3" | 디렉토리명 |
| "amazon_s3" | `replace('_', '-')` | "amazon-s3" | 패키지명 |
| "amazon-s3" | `replace('-', '_')` | "amazon_s3" | 모듈명 |
| "O'Reilly" | `replace('\'', '\'\'')` | "O''Reilly" | SQL 이스케이프 |

### C. 체크리스트 템플릿

#### 새 서버 생성 후
- [ ] `uv sync` 실행
- [ ] `uv.lock` 생성 확인
- [ ] 예제 도구 제거
- [ ] 실제 도구 구현
- [ ] 테스트 작성
- [ ] `uv run pytest --cov` 통과
- [ ] `pre-commit run --all-files` 통과
- [ ] README 업데이트
- [ ] Docusaurus 파일 생성
- [ ] 사이드바 업데이트
- [ ] server-cards.json 추가
- [ ] PR 생성

#### 템플릿 업데이트 후
- [ ] 로컬 테스트 생성
- [ ] 생성된 서버 빌드 확인
- [ ] 테스트 통과 확인
- [ ] 문서 렌더링 확인
- [ ] CHANGELOG 업데이트
- [ ] cookiecutters 브랜치에 병합

---

**작성일**: 2025-10-21
**분석 대상**: awslabs/mcp cookiecutters 브랜치
**템플릿 버전**: Python MCP Server Template
