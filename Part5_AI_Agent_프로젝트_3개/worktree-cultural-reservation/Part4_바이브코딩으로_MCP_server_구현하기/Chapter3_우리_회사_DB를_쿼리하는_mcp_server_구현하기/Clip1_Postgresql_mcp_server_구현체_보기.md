# Clip 1: PostgreSQL MCP Server 구현체 보기

## 학습 목표
- PostgreSQL MCP Server의 구조와 제공되는 기능 이해하기
- MCP의 Tools와 Resources 개념을 실제 구현을 통해 학습하기
- AI 에이전트가 데이터베이스와 상호작용하는 시나리오 이해하기

## PostgreSQL MCP Server란?

PostgreSQL MCP Server는 Model Context Protocol을 통해 PostgreSQL 데이터베이스에 안전하게 접근할 수 있도록 해주는 서버 구현체입니다. Claude와 같은 AI 에이전트가 데이터베이스 스키마를 이해하고, 쿼리를 실행할 수 있도록 도와줍니다.

**출처**: [MCP Servers - PostgreSQL](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres)

## 주요 구성 요소

### 1. Resources (리소스)

Resources는 AI 에이전트가 "참고할 수 있는 정보"를 제공합니다. PostgreSQL MCP Server는 두 가지 리소스를 제공합니다:

#### 1.1 ListResources - 테이블 목록 조회
- **기능**: 데이터베이스의 모든 public 스키마 테이블 목록을 반환
- **역할**: AI가 어떤 테이블이 있는지 파악할 수 있게 함

#### 1.2 ReadResource - 테이블 스키마 조회
- **기능**: 특정 테이블의 상세 스키마 정보 반환
- **반환 정보**:
  - 컬럼명 (column_name)
  - 데이터 타입 (data_type)
  - NULL 허용 여부
  - 기본값 등

### 2. Tools (도구)

Tools는 AI 에이전트가 "실행할 수 있는 작업"입니다. PostgreSQL MCP Server는 하나의 핵심 Tool을 제공합니다:

#### 2.1 query Tool
- **이름**: `query`
- **설명**: "Run a read-only SQL query"
- **입력 파라미터**:
  - `sql` (string, required): 실행할 SQL 쿼리문
- **특징**: 읽기 전용 트랜잭션으로 실행되어 데이터 안전성 보장

## 내부 동작 원리

### 연결 관리
```
PostgreSQL Pool을 사용한 효율적인 커넥션 관리
├── 연결 재사용으로 성능 향상
└── 자동 커넥션 해제로 리소스 관리
```

### 트랜잭션 처리
```
1. BEGIN TRANSACTION READ ONLY 시작
2. SQL 쿼리 실행
3. 결과 반환
4. 자동 ROLLBACK (읽기 전용이므로 변경사항 없음)
```

### 보안 메커니즘
- **읽기 전용 트랜잭션**: 데이터 변경 방지
- **에러 처리**: 롤백 실패 시에도 연결 안전하게 해제
- **격리된 실행**: 각 쿼리가 독립적인 트랜잭션에서 실행

## 실전 시나리오: 채용 후보자 정보 조회하기

채용 서비스를 운영하는 회사가 있고, `candidates` 테이블에 후보자 정보가 저장되어 있다고 가정해봅시다.

### 시나리오 흐름

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Claude as Claude AI
    participant MCP as PostgreSQL MCP
    participant DB as PostgreSQL DB

    User->>Claude: "Python 개발자 후보자 목록을 보여줘"

    Note over Claude: 1. 어떤 테이블이 있는지 확인 필요
    Claude->>MCP: ListResources 요청
    MCP->>DB: SELECT table_name FROM information_schema.tables
    DB-->>MCP: [candidates, companies, ...]
    MCP-->>Claude: 테이블 목록 반환

    Note over Claude: 2. candidates 테이블 구조 파악
    Claude->>MCP: ReadResource(candidates) 요청
    MCP->>DB: SELECT column_name, data_type FROM information_schema.columns
    DB-->>MCP: 스키마 정보
    MCP-->>Claude: {name, position, skills, company}

    Note over Claude: 3. 적절한 SQL 쿼리 작성
    Claude->>MCP: query Tool 실행
    Note over MCP: BEGIN TRANSACTION READ ONLY
    MCP->>DB: SELECT * FROM candidates WHERE position = 'Developer' AND skills LIKE '%Python%'
    DB-->>MCP: 쿼리 결과
    Note over MCP: ROLLBACK
    MCP-->>Claude: JSON 형태의 결과

    Claude-->>User: "Python 개발자 후보자 15명을 찾았습니다:<br/>1. 김철수 - Python, Django, 5년 경력..."
```

### 단계별 상세 설명

#### Step 1: 테이블 탐색 (ListResources)
사용자가 "Python 개발자 후보자 목록을 보여줘"라고 요청하면, Claude는 먼저 어떤 테이블이 있는지 확인합니다.

**MCP가 실행하는 쿼리**:
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
```

**반환 결과**:
```json
[
  "candidates",
  "companies",
  "job_postings"
]
```

#### Step 2: 스키마 이해 (ReadResource)
`candidates` 테이블이 있다는 것을 확인한 Claude는 해당 테이블의 구조를 파악합니다.

**MCP가 실행하는 쿼리**:
```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'candidates'
```

**반환 결과**:
```json
{
  "columns": [
    {"name": "id", "type": "integer", "nullable": "NO"},
    {"name": "name", "type": "text", "nullable": "NO"},
    {"name": "position", "type": "text", "nullable": "NO"},
    {"name": "skills", "type": "text[]", "nullable": "YES"},
    {"name": "company", "type": "text", "nullable": "YES"}
  ]
}
```

#### Step 3: 쿼리 실행 (query Tool)
스키마를 이해한 Claude는 적절한 SQL 쿼리를 작성하고 실행합니다.

**Claude가 작성한 SQL**:
```sql
SELECT name, position, skills, company
FROM candidates
WHERE position = 'Developer'
  AND 'Python' = ANY(skills)
ORDER BY name
```

**query Tool의 내부 동작**:
```typescript
// 1. 읽기 전용 트랜잭션 시작
await client.query('BEGIN TRANSACTION READ ONLY');

try {
  // 2. 사용자 쿼리 실행
  const result = await client.query(sql);

  // 3. 결과 반환
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result.rows, null, 2)
      }
    ]
  };
} finally {
  // 4. 트랜잭션 롤백 (읽기 전용이므로 변경사항 없음)
  await client.query('ROLLBACK');
}
```

**실행 결과**:
```json
[
  {
    "name": "김철수",
    "position": "Developer",
    "skills": ["Python", "Django", "PostgreSQL"],
    "company": "테크스타트업"
  },
  {
    "name": "이영희",
    "position": "Developer",
    "skills": ["Python", "FastAPI", "Docker"],
    "company": "클라우드컴퍼니"
  }
]
```

## 왜 읽기 전용(Read-Only)인가?

PostgreSQL MCP Server가 읽기 전용 트랜잭션만 지원하는 이유:

1. **데이터 안전성**: AI가 실수로 데이터를 삭제하거나 수정하는 것을 방지
2. **예측 가능성**: 쿼리 실행이 데이터베이스 상태를 변경하지 않음을 보장
3. **동시성**: 여러 AI 에이전트가 동시에 쿼리해도 락(lock) 경합 최소화

만약 데이터 수정이 필요하다면, 별도의 write tool을 안전하게 설계해야 합니다. (다음 Clip에서 다룰 예정)

## 다음 학습 내용

다음 Clip에서는 실제로 채용 서비스 데이터베이스를 Neon에 구축하고, mock 데이터를 생성하여 이 시나리오를 직접 실습해볼 것입니다.
