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

# Clip 2: Mock 스키마 만들고 데이터 합성해서 집어넣기

## 학습 목표
- Neon MCP를 활용하여 실습용 데이터베이스 구축하기
- 채용 서비스 도메인의 현실적인 테이블 스키마 설계하기
- Mock 데이터를 생성하고 데이터베이스에 삽입하기

## 프로젝트 시나리오

우리는 메이커 직군(개발자, 디자이너, 마케터, PM)을 위한 채용 서비스를 운영하는 회사입니다. 이 서비스에 가입한 후보자들의 정보를 관리하는 데이터베이스를 구축하고, AI 에이전트가 이 데이터를 쿼리할 수 있도록 MCP 서버를 만들 것입니다.

## Step 1: Neon 프로젝트 생성하기

### Neon MCP로 프로젝트 생성

먼저 Neon MCP를 사용하여 새로운 PostgreSQL 프로젝트를 생성합니다.

**바이브코딩 프롬프트**:
```
Neon에 "recruit-service-demo"라는 이름의 프로젝트를 만들어줘
```

**실행 결과**:
```
Project ID: mute-breeze-62635479
Branch: main
Database: neondb
Connection String: postgresql://neondb_owner:...
```

## Step 2: candidates 테이블 스키마 설계

### 테이블 구조

채용 후보자 정보를 저장하기 위한 `candidates` 테이블을 설계합니다.

```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,              -- 자동 증가 ID
    name TEXT NOT NULL,                 -- 후보자 이름
    position TEXT NOT NULL,             -- 직군 (Developer, Designer, PM, Marketer)
    skills TEXT[] NOT NULL,             -- 보유 스킬 (배열)
    company TEXT,                       -- 현재/이전 회사
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 등록 시간
);
```

### 스키마 설명

| 컬럼 | 타입 | 설명 | 제약조건 |
|------|------|------|----------|
| `id` | SERIAL | 고유 식별자 | PRIMARY KEY, 자동 증가 |
| `name` | TEXT | 후보자 이름 | NOT NULL |
| `position` | TEXT | 직군 | NOT NULL |
| `skills` | TEXT[] | 보유 스킬 목록 | NOT NULL, PostgreSQL 배열 타입 |
| `company` | TEXT | 소속 회사 | NULL 허용 |
| `created_at` | TIMESTAMP | 생성 시간 | 자동으로 현재 시간 설정 |

**바이브코딩 프롬프트**:
```
recruit-service-demo 프로젝트에 candidates 테이블을 만들어줘.
컬럼은 id, name, position, skills(배열), company, created_at
```

## Step 3: Mock 데이터 생성 및 삽입

### Mock 데이터 특징

실제 채용 서비스를 반영한 현실적인 데이터:
- **직군 분포**: Developer(39명), Designer(20명), PM(19명), Marketer(19명)
- **실제 회사명**: 네이버, 카카오, 토스, 쿠팡 등 국내 유명 IT 기업
- **현실적인 스킬셋**: 각 직군에 맞는 실제 기술 스택과 도구
- **한글 이름**: 국내 채용 서비스 시나리오에 적합한 이름

### 샘플 데이터 예시

```json
[
  {
    "name": "김민준",
    "position": "Developer",
    "skills": ["Python", "Django", "PostgreSQL"],
    "company": "네이버"
  },
  {
    "name": "이서윤",
    "position": "Designer",
    "skills": ["Figma", "Sketch", "Adobe XD"],
    "company": "카카오"
  },
  {
    "name": "박도윤",
    "position": "Developer",
    "skills": ["JavaScript", "React", "TypeScript"],
    "company": "토스"
  },
  {
    "name": "최서준",
    "position": "PM",
    "skills": ["Agile", "Jira", "Product Strategy"],
    "company": "쿠팡"
  }
]
```

### 직군별 스킬 예시

#### Developer
- Backend: Python/Django, Java/Spring Boot, Go/Kubernetes, Node.js
- Frontend: React, Vue.js, TypeScript, Next.js
- Mobile: Swift/iOS, Kotlin/Android, Flutter
- 특수: Machine Learning, Blockchain, Game Development

#### Designer
- UI/UX: Figma, Sketch, Adobe XD, Prototyping
- Visual: Branding, Illustration, Motion Graphics
- System: Design System, Component Library, Tokens
- Specialized: 3D Design, Game UI, Data Visualization

#### PM
- Method: Agile, Scrum, OKR, Lean Startup
- Analytics: SQL, Data Analysis, A/B Testing
- Domain: E-commerce, Fintech, Healthcare, Gaming

#### Marketer
- Digital: SEO, Google Analytics, Performance Marketing
- Content: Copywriting, Content Strategy, Brand Storytelling
- Growth: Growth Hacking, Viral Marketing, Community Management
- Channel: Social Media, Influencer, Email Marketing

## Step 4: 데이터 삽입 실행

### SQL 파일 사용

이 저장소에 포함된 `insert_candidates.sql` 파일을 사용하여 데이터를 삽입할 수 있습니다.

**파일 위치**: `Chapter4_우리_회사_DB를_쿼리하는_MCP_SERVER_구현하기/insert_candidates.sql`

**Neon MCP로 실행**:
```
recruit-service-demo 프로젝트에 insert_candidates.sql 파일의 내용을 실행해줘
```

또는 직접 SQL 실행:

**바이브코딩 프롬프트**:
```
insert_candidates.sql 파일을 읽어서 recruit-service-demo 프로젝트의 candidates 테이블에 데이터를 삽입해줘
```

## Step 5: 데이터 검증

### 데이터 확인 쿼리

삽입된 데이터를 확인해봅시다.

**전체 개수 확인**:
```sql
SELECT COUNT(*) as total_candidates
FROM candidates;
```

**결과**: 97명의 후보자

**직군별 분포 확인**:
```sql
SELECT position, COUNT(*) as count
FROM candidates
GROUP BY position
ORDER BY count DESC;
```

**결과**:
```
Developer: 39명
Designer: 20명
PM: 19명
Marketer: 19명
```

**샘플 데이터 조회**:
```sql
SELECT name, position, skills, company
FROM candidates
LIMIT 5;
```

### Connection String 저장

나중에 MCP 서버 구현에서 사용할 수 있도록 connection string을 저장해둡니다.

**바이브코딩 프롬프트**:
```
recruit-service-demo 프로젝트의 connection string을 알려줘
```

## 데이터베이스 활용 시나리오

이제 우리가 만든 데이터베이스로 다양한 쿼리를 실행할 수 있습니다:

### 시나리오 1: Python 개발자 찾기
```sql
SELECT name, company, skills
FROM candidates
WHERE position = 'Developer'
  AND 'Python' = ANY(skills);
```

### 시나리오 2: 카카오 출신 후보자
```sql
SELECT name, position, skills
FROM candidates
WHERE company = '카카오';
```

### 시나리오 3: 디자인 시스템 경험자
```sql
SELECT name, company, skills
FROM candidates
WHERE position = 'Designer'
  AND (
    'Design System' = ANY(skills) OR
    'Design Systems' = ANY(skills)
  );
```

### 시나리오 4: 풀스택 개발자 (프론트+백엔드)
```sql
SELECT name, company, skills
FROM candidates
WHERE position = 'Developer'
  AND (
    'React' = ANY(skills) OR
    'Vue.js' = ANY(skills)
  )
  AND (
    'Python' = ANY(skills) OR
    'Node.js' = ANY(skills) OR
    'Java' = ANY(skills)
  );
```

## 다음 단계

다음 Clip에서는 이 데이터베이스에 안전하게 접근할 수 있는 MCP 서버를 구현할 것입니다. 읽기 전용 기능 뿐만 아니라, 특정 필드만 업데이트할 수 있는 안전한 write tool도 설계해볼 것입니다.

## 실습 체크리스트

- [ ] Neon 프로젝트 생성 완료
- [ ] candidates 테이블 스키마 생성 완료
- [ ] mock 데이터 삽입 완료
- [ ] 데이터 검증 쿼리 실행 완료
- [ ] Connection string 저장 완료


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
