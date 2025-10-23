# MCP Repository 분석 레포트

## 목차
1. [MCP 레포지토리 개요](#1-mcp-레포지토리-개요)
2. [하위 MCP Server 관리 방식](#2-하위-mcp-server-관리-방식)
3. [MCP Server 구조 분석 (amazon-bedrock-agentcore-mcp-server)](#3-mcp-server-구조-분석)
4. [개발 워크플로우](#4-개발-워크플로우)
5. [배포 및 패키징](#5-배포-및-패키징)
6. [결론](#6-결론)

---

## 1. MCP 레포지토리 개요

### 1.1 레포지토리 구조
AWS Labs의 MCP 레포지토리는 **모노레포(Monorepo)** 방식으로 구성되어 있으며, 60개 이상의 MCP 서버들을 통합 관리합니다.

```
mcp/
├── .github/                    # CI/CD 워크플로우
├── .devcontainer/              # 개발 컨테이너 설정
├── docusaurus/                 # 문서화 사이트
├── samples/                    # 샘플 프로젝트
└── src/                        # MCP 서버들
    ├── amazon-bedrock-agentcore-mcp-server/
    ├── amazon-kendra-index-mcp-server/
    ├── aws-api-mcp-server/
    ├── dynamodb-mcp-server/
    └── ... (60+ 서버들)
```

### 1.2 주요 MCP 서버 카테고리

**AI & Machine Learning:**
- amazon-bedrock-agentcore-mcp-server
- bedrock-kb-retrieval-mcp-server
- nova-canvas-mcp-server

**Database & Caching:**
- dynamodb-mcp-server
- aurora-dsql-mcp-server
- postgres-mcp-server
- mysql-mcp-server
- valkey-mcp-server
- elasticache-mcp-server

**Infrastructure & Deployment:**
- cdk-mcp-server
- cfn-mcp-server
- terraform-mcp-server
- aws-serverless-mcp-server
- eks-mcp-server
- ecs-mcp-server

**Developer Tools:**
- aws-documentation-mcp-server
- code-doc-gen-mcp-server
- git-repo-research-mcp-server

---

## 2. 하위 MCP Server 관리 방식

### 2.1 독립적 패키지 관리

각 MCP 서버는 **독립적인 Python 패키지**로 관리됩니다:

#### 패키지 네이밍 컨벤션
```
awslabs.<서버명>-mcp-server
```
예: `awslabs.amazon-bedrock-agentcore-mcp-server`

#### 디렉토리 구조 (표준화)
```
src/<서버명>-mcp-server/
├── pyproject.toml              # 패키지 메타데이터 및 의존성
├── uv.lock                     # 의존성 잠금 파일
├── uv-requirements.txt         # Docker용 요구사항
├── Dockerfile                  # 컨테이너화
├── README.md                   # 서버 문서
├── CHANGELOG.md                # 버전 히스토리
├── LICENSE                     # Apache 2.0
├── NOTICE                      # 저작권 고지
├── SECURITY.md                 # 보안 정책
├── docker-healthcheck.sh       # 헬스체크 스크립트
├── awslabs/                    # 소스 코드
│   └── <서버명>_mcp_server/
│       ├── __init__.py
│       ├── server.py           # FastMCP 서버 구현
│       ├── config.py           # 설정 관리
│       └── utils/              # 유틸리티 모듈
└── tests/                      # 단위 테스트
    ├── __init__.py
    ├── conftest.py
    └── test_*.py
```

### 2.2 의존성 관리 전략

#### UV (Python Package Manager) 사용
- **uv**: Rust로 작성된 초고속 Python 패키지 매니저
- **pyproject.toml**: 프로젝트 메타데이터 및 의존성 정의
- **uv.lock**: 정확한 버전 고정

#### 공통 의존성
모든 MCP 서버가 공유하는 핵심 의존성:
```toml
dependencies = [
    "loguru>=0.7.0",        # 로깅
    "mcp[cli]>=1.6.0",      # MCP 프로토콜
    "fastmcp>=0.1.0",       # FastMCP 프레임워크
    "pydantic>=2.10.6",     # 데이터 검증
]
```

#### 개발 의존성 그룹
```toml
[dependency-groups]
dev = [
    "commitizen>=4.2.2",    # 커밋 메시지 표준화
    "pre-commit>=4.1.0",    # Git hooks
    "ruff>=0.9.7",          # 린터/포매터
    "pyright>=1.1.398",     # 타입 체커
    "pytest>=8.0.0",        # 테스트 프레임워크
    "pytest-asyncio>=0.26.0",
    "pytest-cov>=4.1.0",    # 코드 커버리지
    "pytest-mock>=3.12.0",
]
```

### 2.3 품질 관리 시스템

#### Pre-commit Hooks (.pre-commit-config.yaml)
```yaml
- detect-secrets       # 시크릿 검출
- ruff (linting)       # 코드 린팅
- ruff-format          # 코드 포매팅
- pyright              # 타입 체크
- conventional commits # 커밋 메시지 검증
```

#### GitHub Actions 워크플로우
```
.github/workflows/
├── bandit.yml                  # 보안 취약점 검사
├── checkov.yml                 # IaC 보안 검사
├── cfn_nag.yml                 # CloudFormation 검증
├── check-license-header.yml    # 라이선스 헤더 검증
└── release.py                  # 자동 릴리스
```

#### 코드 커버리지
- 목표: **병합 시 커버리지 유지 또는 향상**
- 도구: pytest-cov
- 배지: Codecov 통합

### 2.4 문서화 전략

#### 다층 문서화 시스템
1. **서버별 README.md**: 각 서버의 사용법, 설치, 설정
2. **Docusaurus 문서 사이트**: 통합 문서 포털
   ```
   docusaurus/docs/servers/
   ├── amazon-bedrock-agentcore-mcp-server.md
   ├── dynamodb-mcp-server.md
   └── ...
   ```
3. **DESIGN_GUIDELINES.md**: 설계 원칙 및 가이드라인
4. **VIBE_CODING_TIPS_TRICKS.md**: 개발 팁 및 트릭
5. **DEVELOPER_GUIDE.md**: 기여자 가이드

#### 자동 생성 메커니즘
- Cookiecutter 템플릿으로 새 서버 스캐폴딩
- 문서 일관성 자동 검증
- README → Docusaurus 자동 동기화

### 2.5 버전 관리 및 릴리스

#### 시맨틱 버저닝
```toml
[tool.commitizen]
name = "cz_conventional_commits"
version_files = [
    "pyproject.toml:version",
    "awslabs/<서버명>/__init__.py:__version__"
]
update_changelog_on_bump = true
```

#### 릴리스 프로세스
1. **Conventional Commits**: feat, fix, chore, docs
2. **Commitizen**: 자동 버전 범프
3. **CHANGELOG.md**: 자동 생성
4. **GitHub Release**: 자동 퍼블리시
5. **Package Registry**: PyPI 업로드

---

## 3. MCP Server 구조 분석

`amazon-bedrock-agentcore-mcp-server`를 예시로 상세 분석합니다.

### 3.1 핵심 아키텍처

#### 계층 구조
```
awslabs/amazon_bedrock_agentcore_mcp_server/
├── server.py           # FastMCP 서버 + 도구 정의
├── config.py           # Pydantic 설정 모델
└── utils/              # 비즈니스 로직
    ├── __init__.py
    ├── cache.py        # 문서 캐싱 로직
    ├── doc_fetcher.py  # 문서 다운로드
    ├── indexer.py      # TF-IDF 검색 인덱스
    ├── text_processor.py # 텍스트 처리
    └── url_validator.py  # URL 검증
```

### 3.2 서버 구현 (server.py)

#### FastMCP 기반 서버
```python
from mcp.server.fastmcp import FastMCP

APP_NAME = 'amazon-bedrock-agentcore-mcp-server'
mcp = FastMCP(APP_NAME)

@mcp.tool()
def search_agentcore_docs(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """검색 도구 구현"""
    cache.ensure_ready()
    index = cache.get_index()
    results = index.search(query, k=k)
    # ... 결과 처리
    return return_docs

@mcp.tool()
def fetch_agentcore_doc(uri: str) -> Dict[str, Any]:
    """문서 가져오기 도구"""
    cache.ensure_ready()
    page = cache.ensure_page(uri)
    return {
        'url': page.url,
        'title': page.title,
        'content': page.content,
    }

def main() -> None:
    """엔트리 포인트"""
    cache.ensure_ready()
    mcp.run()
```

#### 주요 특징
1. **데코레이터 기반 도구 등록**: `@mcp.tool()`
2. **타입 힌팅**: 완전한 타입 안전성
3. **Docstring**: MCP 클라이언트에 자동 노출
4. **Lazy Loading**: 캐시 초기화는 필요 시에만

### 3.3 설정 관리 (config.py)

#### Pydantic 기반 검증
```python
from pydantic import BaseModel, Field, field_validator

class Config(BaseModel):
    llm_texts_url: List[str] = Field(
        default_factory=lambda: [
            'https://aws.github.io/bedrock-agentcore-starter-toolkit/llms.txt'
        ]
    )
    timeout: float = Field(default=30.0)
    user_agent: str = Field(default='agentcore-mcp-docs/1.0')

    @field_validator('llm_texts_url')
    @classmethod
    def validate_urls(cls, v: List[str]) -> List[str]:
        return validate_urls(v)

doc_config = Config()  # 글로벌 싱글톤
```

#### 장점
- **타입 안전성**: Pydantic이 자동 검증
- **기본값**: Field로 명시적 기본값
- **커스텀 검증**: field_validator 데코레이터

### 3.4 캐싱 전략 (cache.py)

#### 2단계 초기화 패턴
```python
# 전역 상태
_INDEX: IndexSearch | None = None
_URL_CACHE: Dict[str, Page | None] = {}
_URL_TITLES: Dict[str, str] = {}
_LINKS_LOADED = False

def load_links_only() -> None:
    """1단계: 제목만 로드 (빠른 시작)"""
    for src in doc_config.llm_texts_url:
        for title, url in doc_fetcher.parse_llms_txt(src):
            _URL_TITLES[url] = title
            _URL_CACHE.setdefault(url, None)  # placeholder
            _INDEX.add(Doc(uri=url, display_title=title, content=''))

def ensure_page(url: str) -> Page | None:
    """2단계: 요청 시 콘텐츠 로드 (Lazy)"""
    if _URL_CACHE.get(url) is not None:
        return _URL_CACHE[url]

    raw = doc_fetcher.fetch_and_clean(url)
    page = Page(url=url, title=raw.title, content=raw.content)
    _URL_CACHE[url] = page
    return page
```

#### 성능 최적화
- **빠른 시작**: 메타데이터만 로드 (~1초)
- **On-demand 페칭**: 실제 사용 시 콘텐츠 다운로드
- **영구 캐싱**: 한 번 로드된 페이지는 메모리에 유지

### 3.5 검색 인덱스 (indexer.py)

#### 커스텀 TF-IDF 구현
```python
class IndexSearch:
    def __init__(self):
        self.docs: list[Doc] = []
        self.doc_frequency: dict[str, int] = {}
        self.doc_indices: dict[str, list[int]] = {}

    def add(self, doc: Doc) -> None:
        """Markdown-aware 인덱싱"""
        # 헤더 추출 (높은 가중치)
        headers = ' '.join(_MD_HEADER.findall(doc.content))

        # 코드 블록 추출 (중간 가중치)
        code_blocks = ' '.join(_MD_CODE_BLOCK.findall(doc.content))

        # 링크 텍스트 추출
        link_text = ' '.join(_MD_LINK_TEXT.findall(doc.content))

        # 가중치 haystack 구성
        haystack = ' '.join([title, headers, link_text, code, content])

        # 토큰화 및 인덱싱
        for tok in _TOKEN.findall(haystack):
            self.doc_indices.setdefault(tok, []).append(idx)
            self.doc_frequency[tok] += 1

    def search(self, query: str, k: int = 8) -> list[tuple[float, Doc]]:
        """TF-IDF 스코어링"""
        for qt in query_tokens:
            for idx in self.doc_indices.get(qt, []):
                tf = _calculate_md_score(doc, qt)  # 가중치 TF
                idf = math.log((N + 1) / (1 + doc_freq)) + 1.0
                scores[idx] += tf * idf

        return sorted(scores, reverse=True)[:k]
```

#### 특별한 기능
1. **Markdown 인식**: 헤더, 코드, 링크 별도 처리
2. **적응형 제목 부스트**:
   - 빈 콘텐츠: 8x
   - 짧은 페이지: 5x
   - 긴 페이지: 3x
3. **구조 기반 가중치**:
   - 제목: 3-8x
   - 헤더: 4x
   - 코드/링크: 2x
   - 본문: 1x

### 3.6 테스트 전략

#### 포괄적 테스트 커버리지
```
tests/
├── test_server.py          # 도구 엔드포인트 테스트
├── test_cache.py           # 캐싱 로직 테스트
├── test_indexer.py         # 검색 알고리즘 테스트
├── test_doc_fetcher.py     # HTTP 페칭 테스트
├── test_text_processor.py  # 텍스트 처리 테스트
├── test_config.py          # 설정 검증 테스트
├── test_url_validator.py   # URL 검증 테스트
├── test_init.py            # 패키지 초기화 테스트
└── conftest.py             # Pytest fixtures
```

#### 테스트 실행
```bash
uv run --frozen pytest --cov --cov-branch --cov-report=term-missing
```

### 3.7 Docker 배포

#### 멀티 스테이지 빌드
```dockerfile
# Stage 1: 빌드
FROM python:3.13-alpine AS uv
WORKDIR /app

# UV 환경 변수
ENV UV_COMPILE_BYTECODE=1
ENV UV_FROZEN=true

# 의존성 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# 소스 복사 및 설치
COPY . /app
RUN uv sync --frozen --no-dev --no-editable

# Stage 2: 런타임
FROM python:3.13-alpine
ENV PATH="/app/.venv/bin:$PATH"

# 최소 런타임 설정
RUN apk add --no-cache ca-certificates
RUN adduser -S app

COPY --from=uv --chown=app:app /app/.venv /app/.venv
COPY ./docker-healthcheck.sh /usr/local/bin/

USER app
HEALTHCHECK CMD ["docker-healthcheck.sh"]
ENTRYPOINT ["awslabs.amazon-bedrock-agentcore-mcp-server"]
```

#### 보안 최적화
- **Non-root 사용자**: app 계정으로 실행
- **최소 이미지**: Alpine Linux
- **의존성 해싱**: `pip install --require-hashes`
- **헬스체크**: 60초 간격 자동 점검

---

## 4. 개발 워크플로우

### 4.1 새 MCP 서버 생성

#### Cookiecutter 템플릿 사용
```bash
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters \
  --output-dir ./src \
  --directory python
```

#### 자동 생성 항목
- 표준 디렉토리 구조
- pyproject.toml (사전 구성)
- README 템플릿
- Dockerfile
- 테스트 스캐폴드
- 라이선스 헤더

### 4.2 로컬 개발

#### MCP Inspector 사용
```bash
npx @modelcontextprotocol/inspector \
  uv \
  --directory /path/to/server \
  run \
  server.py
```

#### 브라우저 테스트
- URL: http://127.0.0.1:6274
- 실시간 도구 호출 테스트
- 프로토콜 메시지 검사

#### IDE 통합 테스트
```json
// .cursor/mcp.json
{
  "awslabs.aws-documentation-mcp-server": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/dev/mcp/src/aws-documentation-mcp-server",
      "run",
      "server.py"
    ],
    "env": {
      "FASTMCP_LOG_LEVEL": "ERROR"
    }
  }
}
```

### 4.3 품질 검증

#### Pre-commit 실행
```bash
pre-commit run --all-files
```

#### 단위 테스트
```bash
cd src/my-mcp-server
uv run pytest --cov --cov-branch
```

#### 타입 체크
```bash
uv run pyright
```

### 4.4 Pull Request 프로세스

#### 1. 커밋 메시지 (Conventional Commits)
```
feat(dynamodb): add query tool with pagination
fix(s3): handle bucket access errors
docs(readme): update installation instructions
chore(deps): bump pydantic to 2.10.6
```

#### 2. PR 체크리스트
- [ ] 단위 테스트 추가
- [ ] 코드 커버리지 유지/향상
- [ ] README.md 업데이트
- [ ] Docusaurus 문서 추가
- [ ] Pre-commit 통과
- [ ] CI 워크플로우 통과

#### 3. 자동 검증
- Bandit (보안)
- Checkov (IaC)
- License header
- Code coverage
- Type checking

---

## 5. 배포 및 패키징

### 5.1 PyPI 퍼블리싱

#### 빌드 시스템
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["awslabs"]
```

#### 네이밍
```
awslabs.amazon-bedrock-agentcore-mcp-server@latest
```

### 5.2 설치 방법

#### uvx (추천)
```bash
uvx awslabs.amazon-bedrock-agentcore-mcp-server@latest
```

#### Docker
```bash
docker run --rm -i \
  -e FASTMCP_LOG_LEVEL=ERROR \
  mcp/amazon-bedrock-agentcore:latest
```

### 5.3 MCP 클라이언트 통합

#### Cursor
```json
{
  "mcpServers": {
    "bedrock-agentcore": {
      "command": "uvx",
      "args": ["awslabs.amazon-bedrock-agentcore-mcp-server@latest"],
      "env": {"FASTMCP_LOG_LEVEL": "ERROR"},
      "autoApprove": ["search_agentcore_docs", "fetch_agentcore_doc"]
    }
  }
}
```

#### Amazon Q Developer CLI
```json
{
  "mcpServers": { /* ... */ },
  "tools": [
    "@awslabs.amazon-bedrock-agentcore-mcp-server"
  ]
}
```

#### Claude Code
```json
// .mcp.json
{
  "mcpServers": {
    "bedrock-agentcore": {
      "command": "uvx",
      "args": ["awslabs.amazon-bedrock-agentcore-mcp-server@latest"]
    }
  }
}
```

---

## 6. 결론

### 6.1 핵심 설계 원칙

#### 1. 모노레포 이점 극대화
- **코드 공유**: 공통 유틸리티 재사용
- **일관성**: 표준화된 구조 및 도구
- **원자적 변경**: 크로스-서버 리팩토링 용이
- **통합 CI/CD**: 단일 파이프라인

#### 2. 독립성과 응집력의 균형
- **독립 배포**: 각 서버는 독립적으로 버저닝
- **공통 의존성**: FastMCP, Pydantic, MCP SDK 공유
- **격리된 테스트**: 서버별 테스트 스위트

#### 3. 개발자 경험 우선
- **Cookiecutter**: 5분 내 새 서버 생성
- **Pre-commit**: 즉각적 피드백 루프
- **Inspector**: 시각적 디버깅
- **Docusaurus**: 통합 문서 포털

### 6.2 모범 사례 요약

| 영역 | 모범 사례 |
|------|----------|
| **의존성** | UV + pyproject.toml + 잠금 파일 |
| **린팅** | Ruff (린트 + 포맷 통합) |
| **타입 체크** | Pyright 100% 커버리지 |
| **테스트** | Pytest + asyncio + 코드 커버리지 |
| **보안** | Bandit + Checkov + detect-secrets |
| **배포** | Docker 멀티스테이지 + Non-root |
| **문서** | README + Docusaurus + API docs |

### 6.3 참고할 만한 패턴

#### Amazon Bedrock AgentCore MCP Server
- **Lazy Loading**: 빠른 시작 + On-demand 페칭
- **TF-IDF 검색**: 외부 의존성 없는 경량 구현
- **Markdown 인식**: 구조적 콘텐츠 가중치
- **Pydantic 검증**: 타입 안전 설정

#### 확장 가능한 아키텍처
```
server.py (FastMCP)
    ↓ 의존
config.py (Pydantic)
    ↓ 의존
utils/ (비즈니스 로직)
    ├── cache.py        # 상태 관리
    ├── indexer.py      # 검색 로직
    └── doc_fetcher.py  # 외부 API
```

### 6.4 공공 MCP 서버 개발 시사점

#### 1. 표준 준수
- **MCP 프로토콜**: stdio 전송 (SSE 제거됨)
- **FastMCP**: 빠른 개발을 위한 선택
- **Pydantic**: 데이터 검증 표준

#### 2. 보안 고려사항
- API 키 관리: 환경 변수
- 입력 검증: Pydantic validators
- 시크릿 검출: detect-secrets
- 최소 권한: Docker non-root

#### 3. 성능 최적화
- Lazy initialization
- 캐싱 전략
- Async/await 지원
- 경량 의존성

#### 4. 유지보수성
- 포괄적 테스트
- 타입 힌팅
- 명확한 문서
- Conventional commits

---

## 부록: 빠른 참조

### A. 주요 명령어

```bash
# 새 서버 생성
uvx cookiecutter https://github.com/awslabs/mcp.git \
  --checkout cookiecutters --output-dir ./src --directory python

# 의존성 설치
uv venv && uv sync --all-groups

# 로컬 실행
uv run server.py

# 테스트
uv run pytest --cov

# 린팅
uv run ruff check .

# 포맷
uv run ruff format .

# Pre-commit
pre-commit run --all-files

# Inspector
npx @modelcontextprotocol/inspector uv --directory . run server.py
```

### B. 디렉토리 템플릿

```
my-mcp-server/
├── pyproject.toml
├── uv.lock
├── README.md
├── Dockerfile
├── awslabs/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py
│       └── config.py
└── tests/
    ├── conftest.py
    └── test_server.py
```

### C. pyproject.toml 템플릿

```toml
[project]
name = "awslabs.my-mcp-server"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "loguru>=0.7.0",
    "mcp[cli]>=1.6.0",
    "fastmcp>=0.1.0",
    "pydantic>=2.10.6",
]

[project.scripts]
"awslabs.my-mcp-server" = "awslabs.my_mcp_server.server:main"

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.9.7",
    "pyright>=1.1.398",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

**작성일**: 2025-10-21
**분석 대상**: awslabs/mcp (GitHub)
**예시 서버**: amazon-bedrock-agentcore-mcp-server v0.0.3
