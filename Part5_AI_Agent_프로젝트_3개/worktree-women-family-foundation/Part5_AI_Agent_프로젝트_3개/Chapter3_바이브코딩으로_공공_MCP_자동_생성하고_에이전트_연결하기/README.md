# 서울시 공공데이터 MCP 서버 생성기

바이브코딩(Vibe Coding)으로 서울시 공공데이터 API를 MCP(Model Context Protocol) 서버로 자동 생성하고, AI 에이전트와 연결하는 프로젝트입니다.

## 프로젝트 개요

이 프로젝트는 서울시 공공데이터 API를 MCP 서버로 변환하여 Claude와 같은 AI 에이전트가 실시간으로 서울시 공공데이터를 조회할 수 있도록 합니다.

### 공공데이터 API 예시

서울시에서 제공하는 다양한 공공데이터 중 이 프로젝트에서 다루는 서울시 공공데이터 예시입니다:

- **문화 정보**
  - 공공도서관 정보
  - 문화행사 정보
  - 문화시설 정보
  - 전시·공연 시설 현황

- **도시 인프라**
  - 공중화장실 위치정보
  - 주차장 운영정보
  - 공공자전거
  - 버스정류소 위치정보
  - 지하철 역사 정보

## 프로젝트 구조

```
.
├── README.md                          # 프로젝트 메인 가이드
├── CLAUDE.md                          # Claude 에이전트 개발 가이드
├── template/                          # Cookiecutter 템플릿
│   └── data-seoul-mcp/               # 서울공공데이터 MCP 템플릿
│       ├── cookiecutter.json         # 템플릿 설정
│       ├── README.md                 # 템플릿 사용 가이드
│       └── {{cookiecutter.project_domain}}-mcp-server/
│           ├── pyproject.toml        # Python 프로젝트 설정
│           ├── data_seoul_mcp/       # MCP 서버 구현
│           │   └── {{cookiecutter.project_domain}}_mcp_server/
│           │       └── server.py     # FastMCP 서버 구현
│           └── tests/                # 테스트 코드
├── culturalevents-mcp-server/        # 생성된 예제 서버
└── docs/                             # API 문서 및 참고자료
```

## 기술 스택

### 핵심 기술

- FastMCP 기반 서버 구조
- Pydantic 설정 관리
- 비동기 테스트 지원
- Ruff 린팅 및 포매팅
- Pyright 타입 체킹
- GitHub 공개 패턴 준수
- Apache 2.0 라이선스 적용
- Changelog 자동 관리

### 패턴 준수

AWS Labs MCP 패턴을 따릅니다:

- **패키지명**: `data-seoul-mcp.<domain>-mcp-server`
- **모듈명**: `data_seoul_mcp.<domain>_mcp_server`
- **스크립트명**: `data-seoul-mcp.<domain>-mcp-server`

예시:
- Input: `CulturalEvents`
- Package: `data-seoul-mcp.culturalevents-mcp-server`
- Module: `data_seoul_mcp.culturalevents_mcp_server`

## 빠른 시작 가이드

### 사전 요구사항

- Python 3.11+
- uv (Python 패키지 관리자)
- Node.js 18+ (MCP Inspector용)

### 1. MCP 서버 생성

Cookiecutter 템플릿으로 새로운 MCP 서버 생성:

```bash
uvx cookiecutter template/data-seoul-mcp
```

프롬프트 입력 예시:

```
author_name [Your Name]: Hong Gildong
author_email [githubusername@users.noreply.github.com]: gildong@users.noreply.github.com
api_name [Seoul Cultural Events]: Seoul Cultural Events
api_name_korean [문화행사정보]: 문화행사정보
api_description [Seoul city cultural events and space information]:
project_domain [CulturalEvents]: CulturalEvents
description [A Seoul Data MCP server for 문화행사정보 (Seoul Cultural Events)]:
instructions [Use this MCP server to search...]:
```

### 2. 의존성 설치

생성된 디렉토리로 이동하여 의존성 설치:

```bash
cd culturalevents-mcp-server
uv sync --all-groups
```

### 3. 테스트 실행

#### 테스트 실행

```bash
uv run pytest --cov
```

#### MCP Inspector로 테스트

```bash
npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/culturalevents_mcp_server/server.py
```

### 4. Claude Desktop 연동

`claude_desktop_config.json`에 MCP 서버 추가:

```json
{
  "mcpServers": {
    "data-seoul-cultural-events": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/culturalevents-mcp-server",
        "run",
        "data_seoul_mcp/culturalevents_mcp_server/server.py"
      ]
    }
  }
}
```

## API 구현 가이드

### 서울공공데이터 API 연동

`server.py`에서 서울시 API 연동 구현:

```python
import httpx
from typing import Any

@mcp.tool(name='SearchCulturalEvents')
async def search_cultural_events(
    keyword: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    district: str | None = None,
    genre: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """서울시 문화행사 검색

    Args:
        keyword: 검색어 (행사명, 장소명 등)
        start_date: 시작일자 (YYYYMMDD)
        end_date: 종료일자 (YYYYMMDD)
        district: 자치구명 (예: 강남구, 종로구)
        genre: 장르명 (예: 연극, 뮤지컬, 음악)
        limit: 최대 결과 수

    Returns:
        문화행사 검색 결과
    """
    # TODO: 서울시 공공데이터 API 호출
    api_key = os.getenv('SEOUL_API_KEY')
    base_url = 'http://openapi.seoul.go.kr:8088'

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{base_url}/{api_key}/json/culturalEventInfo/{start}/{end}/',
            params={
                'CODENAME': genre,
                'GUNAME': district,
            }
        )
        data = response.json()

    return {
        'status': 'success',
        'total_count': data.get('culturalEventInfo', {}).get('list_total_count', 0),
        'events': data.get('culturalEventInfo', {}).get('row', [])
    }
```

### 환경 변수 설정

`.env` 파일 생성:

```bash
SEOUL_API_KEY=your_api_key_here
```

## 템플릿 기능

### 주요 기능

- FastMCP 기반 서버 구조
- Pydantic 설정 관리
- 비동기 테스트 지원
- Ruff 린팅 및 포매팅
- Pyright 타입 체킹
- GitHub 공개 패턴 준수
- Apache 2.0 라이선스 적용
- Changelog 자동 관리

### 패턴 준수

AWS Labs MCP 패턴을 따릅니다:

- **패키지명**: `data-seoul-mcp.<domain>-mcp-server`
- **모듈명**: `data_seoul_mcp.<domain>_mcp_server`
- **스크립트명**: `data-seoul-mcp.<domain>-mcp-server`

예시:
- Input: `CulturalEvents`
- Package: `data-seoul-mcp.culturalevents-mcp-server`
- Module: `data_seoul_mcp.culturalevents_mcp_server`

## 사용 예시

### Claude Desktop에서 사용

```
사용자: 이번 주말 강남에서 열리는 뮤지컬 공연 있어?

Claude: 서울시 문화행사 정보를 검색하겠습니다.
[SearchCulturalEvents 도구 호출]
keyword: 뮤지컬
district: 강남구
start_date: 20250118
end_date: 20250119

결과:
1. 지킬앤 하이드 - 샤롯데씨어터
   - 일시: 2025-01-18 19:30
   - 장소: 샤롯데씨어터
   - 위치: 송파구 올림픽로 240 롯데월드타워 5층 강남구

2. 맘마미아 더뮤지컬 - 블루스퀘어
   - 일시: 2025-01-19 20:00
   - 장소: 블루스퀘어
   - 위치: 용산구 이태원로 294 블루스퀘어 3층 강남구
```

## 학습로드맵

### 1. 준비 단계
- API 키 발급
- 인프라 환경 설정
- 도구(Tool) 이해

### 2. 구현 단계
- Cookiecutter로 템플릿 생성
- API 명세서와 구현
- MCP 도구 구현
- 기능 확장하기

### 3. 테스트 단계
- 단위 테스트 작성
- MCP Inspector 테스트
- Claude Desktop 연동 테스트

### 4. 배포 단계
- 문서화
- GitHub 리포지토리
- Smithery 배포 (선택사항)

## 참고 자료

### 공식 문서
- [서울 열린데이터광장](https://data.seoul.go.kr/)
- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [FastMCP 문서](https://github.com/jlowin/fastmcp)

### 관련 오픈소스 템플릿
- [AWS MCP Servers](https://github.com/awslabs/mcp-servers)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## 라이선스

Apache-2.0

## 기여 가이드

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 문의

프로젝트 관련 문의사항은 Issue를 통해 남겨주세요.
