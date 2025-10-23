# Recruit MCP Server

채용 서비스를 위한 Model Context Protocol (MCP) 서버입니다.

## 기능

### Resources
- `schema://candidates` - candidates 테이블의 스키마 정보

### Tools
- `query` - 읽기 전용 SQL 쿼리 실행
- `update_candidate` - 후보자 정보 안전하게 업데이트 (position, skills, company만 수정 가능)

## 의존성

`uv`를 사용하면 의존성이 자동으로 관리됩니다:
- `mcp>=1.1.0` - MCP SDK
- `asyncpg>=0.29.0` - PostgreSQL 비동기 드라이버

## 환경 설정

데이터베이스 연결 정보는 환경 변수로 설정합니다:

```bash
export DATABASE_URL="postgresql://user:password@host:port/database?sslmode=require"
```

## 실행

```bash
# uv로 직접 실행
uv run server.py
```

`uv run`은 자동으로 의존성을 확인하고 설치합니다.

## MCP 설정

`.mcp.json` 파일에 다음을 추가하세요:

```json
{
  "mcpServers": {
    "recruit-db": {
      "command": "uv",
      "args": [
        "--directory",
        "/절대경로/recruit-mcp-server",
        "run",
        "server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://user:password@host:port/database?sslmode=require"
      }
    }
  }
}
```

**중요**: `--directory` 뒤에는 이 디렉토리의 **절대 경로**를 입력하세요.

## 사용 예시

### 후보자 조회
```
"Python 개발자를 찾아줘"
```

Claude가 다음과 같이 동작합니다:
1. `schema://candidates` 리소스로 테이블 구조 파악
2. `query` tool로 적절한 SQL 작성 및 실행
3. 결과 반환

### 후보자 정보 업데이트
```
"ID 1번 후보자의 회사를 '토스'로 변경해줘"
```

Claude가 `update_candidate` tool을 사용하여 안전하게 업데이트합니다.

## 보안 고려사항

- `query` tool은 읽기 전용 트랜잭션으로 실행되어 데이터 변경 방지
- `update_candidate`는 position, skills, company 필드만 수정 가능
- `name`과 `id` 필드는 보안상 수정 불가
