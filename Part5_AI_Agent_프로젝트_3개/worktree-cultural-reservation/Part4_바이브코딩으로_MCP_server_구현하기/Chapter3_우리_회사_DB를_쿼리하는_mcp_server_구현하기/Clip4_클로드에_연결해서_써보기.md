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

# Clip 4: 클로드에 연결해서 써보기

## 학습 목표
- 로컬 MCP 서버를 Claude Desktop에 연결하는 방법 학습하기
- .mcp.json 설정 파일 작성 및 관리하기
- 실제 대화를 통해 데이터베이스와 상호작용하기
- MCP 서버 디버깅 및 문제 해결 능력 키우기

## 1. .mcp.json 설정 파일 작성

### 1.1 .mcp.json이란?

`.mcp.json`은 로컬 프로젝트에서 MCP 서버를 설정하는 파일입니다. Claude Code나 Claude Desktop이 이 파일을 읽어 자동으로 MCP 서버를 연결합니다.

**장점**:
- 프로젝트별로 독립적인 MCP 설정
- 버전 관리 가능 (git에 포함)
- 팀원들과 설정 공유 용이

### 1.2 .mcp.json 파일 생성

프로젝트 루트에 `.mcp.json` 파일을 생성합니다:

```bash
cd /Users/bong/github/fastcampus-lecture/Part5_AI_Agent_프로젝트_3개/Chapter4_우리_회사_DB를_쿼리하는_MCP_SERVER_구현하기
```

**.mcp.json 내용:**

```json
{
  "mcpServers": {
    "recruit-db": {
      "command": "uv",
      "args": [
        "--directory",
        "/경로/fastcampus-lecture/Part5_AI_Agent_프로젝트_3개/Chapter4_우리_회사_DB를_쿼리하는_MCP_SERVER_구현하기/recruit-mcp-server",
        "run",
        "server.py"
      ],
      "env": {
        "DATABASE_URL": "postgresql://neondb_owner:...@...c-2.us-east-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require"
      }
    }
  }
}
```

**설정 항목 설명**:

| 항목 | 설명 | 값 |
|------|------|-----|
| `mcpServers` | MCP 서버 목록 정의 | 객체 |
| `recruit-db` | 서버 이름 (고유 식별자) | 원하는 이름 |
| `command` | 실행할 명령어 | `uv` (Python 패키지 관리자) |
| `args` | 명령어 인자 | `--directory` + 절대 경로 + `run` + 파일명 |
| `env.DATABASE_URL` | 환경 변수 | Neon connection string |

**중요**:
- `--directory` 뒤에는 **절대 경로**를 사용해야 합니다
- `uv run`은 자동으로 의존성을 설치하므로 별도의 `pip install` 불필요


### 1.3 의존성 관리

`uv run`은 `pyproject.toml`의 의존성을 자동으로 확인하고 설치하므로 별도의 설치 과정이 필요하지 않습니다.

**프로젝트 의존성**:
- `mcp>=1.1.0` - MCP SDK
- `asyncpg>=0.29.0` - PostgreSQL 비동기 드라이버

**의존성 사전 설치** (선택사항, 첫 실행 속도 향상):
```bash
cd recruit-mcp-server
uv sync
```

### 1.4 .gitignore 설정

민감 정보 보호를 위해 `.gitignore`에 추가:

```gitignore
# MCP 설정 (개인 정보 포함)
.mcp.json

# Python 가상환경
venv/
__pycache__/
*.pyc

# 환경 변수
.env
.env.local
```

**대신 .mcp.json.example 제공**:

```json
{
  "mcpServers": {
    "recruit-db": {
      "command": "uv",
      "args": [
        "--directory",
        "/절대/경로/recruit-mcp-server",
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

**사용 방법**:
1. `.mcp.json.example`을 복사하여 `.mcp.json` 생성
2. 절대 경로를 실제 경로로 변경
3. `DATABASE_URL`을 실제 Neon connection string으로 변경

## 2. Claude Desktop에서 MCP 서버 연결하기

### 2.1 프로젝트에 MCP 서버 추가

**방법 1: claude Desktop UI 사용 (추천)**

1. 설정 > 개발자 > 구성 편집

### 2.2 연결 확인

Claude에게 다음과 같이 물어보세요:

```
사용 가능한 MCP 도구를 보여줘
```

**예상 응답**:
```
다음 도구를 사용할 수 있습니다:

1. query - 읽기 전용 SQL 쿼리 실행
2. update_candidate - 후보자 정보 안전하게 업데이트 (position, skills, company)
```

## 3. 실전 사용 예시

### 3.1 시나리오 1: Python 개발자 찾기

**사용자 질문**:
```
Python 개발자 후보자를 찾아줘
```

**Claude의 동작**:

```mermaid
sequenceDiagram
    participant User as 사용자
    participant Claude as Claude AI
    participant MCP as Recruit MCP Server
    participant DB as Neon PostgreSQL

    User->>Claude: "Python 개발자 후보자를 찾아줘"

    Note over Claude: 1. 스키마 확인
    Claude->>MCP: Read Resource (schema://candidates)
    MCP->>DB: SELECT column_name, data_type FROM information_schema.columns
    DB-->>MCP: 스키마 정보
    MCP-->>Claude: {columns: [...]}

    Note over Claude: 2. SQL 작성 및 실행
    Claude->>MCP: query Tool
    Note over MCP: SELECT * FROM candidates<br/>WHERE position = 'Developer'<br/>AND 'Python' = ANY(skills)
    MCP->>DB: BEGIN TRANSACTION READ ONLY
    MCP->>DB: Execute Query
    DB-->>MCP: Results (15 rows)
    MCP->>DB: ROLLBACK
    MCP-->>Claude: JSON 결과

    Claude-->>User: "Python 개발자 15명을 찾았습니다:<br/>1. 김민준 (네이버) - Python, Django, PostgreSQL<br/>2. 윤서현 (야놀자) - Python, FastAPI, Docker<br/>..."
```

**Claude의 실제 응답 예시**:

```
Python 개발자 후보자를 찾았습니다! 총 15명입니다:

🔹 **김민준** (네이버)
   - 스킬: Python, Django, PostgreSQL
   - ID: 1

🔹 **윤서현** (야놀자)
   - 스킬: Python, FastAPI, Docker
   - ID: 8

🔹 **신준우** (삼성전자)
   - 스킬: Python, Machine Learning, TensorFlow
   - ID: 13

🔹 **서지훈** (당근마켓)
   - 스킬: Python, Django, Redis
   - ID: 21

🔹 **빈태양** (쿠팡)
   - 스킬: Python, Data Engineering, Airflow
   - ID: 33

... (생략)
```

### 3.2 시나리오 2: 후보자 정보 업데이트

**사용자 질문**:
```
김민준 님이 카카오로 이직했어. 회사 정보를 업데이트해줘.
```

**Claude의 동작**:

**Step 1: ID 찾기**
```sql
-- Claude가 생성한 쿼리
SELECT id FROM candidates WHERE name = '김민준'
```

**Step 2: update_candidate tool 실행**
```python
# Tool 호출
{
    "candidate_id": 1,
    "company": "카카오"
}
```

**Step 3: 결과 확인**
```json
{
    "id": 1,
    "name": "김민준",
    "position": "Developer",
    "skills": ["Python", "Django", "PostgreSQL"],
    "company": "카카오"
}
```

**Claude의 응답**:
```
✅ 김민준 님의 회사 정보가 업데이트되었습니다!

**업데이트 내용**:
- 이름: 김민준
- 이전 회사: 네이버
- 새 회사: 카카오
- 직군: Developer
- 스킬: Python, Django, PostgreSQL
```

### 3.3 시나리오 3: 복잡한 조건으로 검색

**사용자 질문**:
```
풀스택 개발자를 찾아줘. 프론트엔드(React나 Vue.js)와 백엔드(Python이나 Node.js) 둘 다 할 수 있는 사람.
```

**Claude가 생성한 SQL**:
```sql
SELECT *
FROM candidates
WHERE position = 'Developer'
  AND (
    'React' = ANY(skills) OR
    'Vue.js' = ANY(skills)
  )
  AND (
    'Python' = ANY(skills) OR
    'Node.js' = ANY(skills)
  )
ORDER BY name
```

**결과**:
```
풀스택 개발자 3명을 찾았습니다:

🔹 **백서진** (넷플릭스코리아)
   - 스킬: JavaScript, Vue.js, Node.js
   - 프론트: Vue.js | 백엔드: Node.js

🔹 **서지훈** (당근마켓)
   - 스킬: Python, Django, Redis
   - 백엔드: Python, Django

🔹 **하준혁** (야놀자)
   - 스킬: TypeScript, Next.js, GraphQL
   - 프론트: Next.js | 백엔드: GraphQL
```

### 3.4 시나리오 4: 여러 필드 동시 업데이트

**사용자 질문**:
```
이서윤 님이 PM으로 직군을 변경하고 토스로 이직했어. 그리고 Product Strategy, Agile 스킬을 추가했어.
```

**Claude의 동작**:

**Step 1: 현재 정보 조회**
```sql
SELECT * FROM candidates WHERE name = '이서윤'
```

**현재 상태**:
```json
{
    "id": 2,
    "name": "이서윤",
    "position": "Designer",
    "skills": ["Figma", "Sketch", "Adobe XD"],
    "company": "카카오"
}
```

**Step 2: update_candidate tool 실행**
```python
{
    "candidate_id": 2,
    "position": "PM",
    "company": "토스",
    "skills": ["Product Strategy", "Agile", "Figma", "Sketch", "Adobe XD"]
}
```

**Claude의 응답**:
```
✅ 이서윤 님의 정보가 모두 업데이트되었습니다!

**변경 내용**:
┌─────────┬──────────┬──────────┐
│ 항목    │ 이전     │ 변경 후  │
├─────────┼──────────┼──────────┤
│ 직군    │ Designer │ PM       │
│ 회사    │ 카카오   │ 토스     │
│ 스킬    │ Figma, Sketch, Adobe XD │ Product Strategy, Agile, Figma, Sketch, Adobe XD │
└─────────┴──────────┴──────────┘
```

## 4. 실습 체크리스트

이 Chapter를 완료하면서 확인할 사항:

- [ ] .mcp.json 설정 파일 작성 완료
- [ ] "Python 개발자 찾기" 시나리오 테스트 완료
- [ ] "후보자 정보 업데이트" 시나리오 테스트 완료
- [ ] 에러 발생 시 디버깅 가능


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
