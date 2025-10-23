# Clip 3: Hybrid Search 구현을 위한 PRD 프롬프트 만들기

## 학습 목표
- PRD(Product Requirements Document) 기반 AI 프롬프트 작성법 이해하기
- Vector Search와 BM25를 결합한 Hybrid Search 요구사항 정리하기
- Context window 최대로 사용 가능한 PRD 프롬프트 작성 전략 익히기
- Neon MCP 서버 연결 및 ParadeDB 활용 방법 익히기

## PRD란 무엇인가?

**PRD(Product Requirements Document)**는 제품 개발 전 작성하는 요구사항 명세서입니다.

### AI 시대의 PRD 변화
```
전통: 기획자/PM → PRD 작성 → 개발자 → 코드 구현
AI 시대: 개발자 → PRD 프롬프트 작성 → AI 에이전트 → 코드 생성
```

**핵심 차이점:**
- 사람용 PRD: 배경, 목적, 비즈니스 맥락 중심
- AI용 PRD: 명확한 스펙, 입출력, 제약사항, 필요한 맥락 중심

## 왜 PRD 프롬프트가 중요한가?

AI 에이전트는 사람이 아니기 때문에 **필요한 모든 맥락을 명확하게 제공**해야 합니다.

**나쁜 예시:**
```
하이브리드 검색을 만들어줘
```

**좋은 예시:**
```
Neon PostgreSQL의 loan_products 테이블에서
pgvector(코사인 유사도)와 pg_search(paradedb)를
RRF 알고리즘으로 결합한 Python CLI 구현.
text-embedding-3-small 사용
```

## 실습 데이터 준비

### 농협 스마트마켓 대출 상품 데이터

실습을 위해 [농협 스마트마켓](https://smartmarket.nonghyup.com/servlet/BFLNW0000R.view)에서 대출 상품 데이터를 수집하고 정제했습니다.

**데이터 파일:** `loan_products.json`
- 농협의 다양한 대출 상품 정보 포함
- 상품명, 설명, 조건 등 검색에 필요한 텍스트 데이터 구조화
- Hybrid Search 실습에 최적화된 형태로 가공

이 데이터를 사용하면 별도의 크롤링이나 데이터 수집 없이 바로 Hybrid Search 구현에 집중할 수 있습니다.

## Neon MCP 서버 연결하기

Hybrid Search 구현을 위해 Neon PostgreSQL을 Claude Code와 연결합니다.

### 연결 방법

**Remote MCP Server (권장):**
```bash
claude mcp add --transport http neon https://mcp.neon.tech/mcp -s project
```

### 연결 확인

```bash
# Claude Code 시작
claude

# MCP 서버 목록 확인
/mcp
```

Neon MCP가 정상적으로 연결되면 프로젝트 조회, SQL 실행 등의 작업을 Claude Code에서 바로 수행할 수 있습니다.

**출처:** [Neon + Claude Code MCP Guide](https://neon.com/guides/claude-code-mcp-neon)

## ParadeDB Hybrid Search 가이드

### Hybrid Search란?

ParadeDB의 Hybrid Search는 **Full-text Search(BM25)와 Similarity Search(Vector)를 결합**한 검색 방식입니다.

### RRF (Reciprocal Rank Fusion) 알고리즘

Hybrid Search의 핵심은 두 검색 결과를 어떻게 결합하는가입니다. ParadeDB는 **RRF 알고리즘**을 사용합니다.

**RRF 동작 방식:**
```
1. BM25 점수와 Similarity 점수로 각각 문서의 상위 결과 계산
2. 각 검색 방식별로 문서 순위 매기기
3. Reciprocal Rank 계산: 1/(k + r)
   - k: 일반적으로 60 (조정 가능)
   - r: 해당 문서의 순위
4. 두 Reciprocal Rank를 합산하여 최종 Hybrid Search 점수 생성
```

### Hybrid Search SQL 예제

```sql
SELECT description,
       bm25_score,
       similarity_score,
       hybrid_score
FROM (
    -- BM25 텍스트 검색
    SELECT id,
           description,
           paradedb.score(id) AS bm25_score
    FROM products
    WHERE description @@@ 'keyboard'
) bm25_results
JOIN (
    -- Vector 유사도 검색
    SELECT id,
           1 - (embedding <=> '[1,2,3]'::vector) AS similarity_score
    FROM products
) vector_results USING (id)
-- RRF로 결합
ORDER BY (1.0 / (60 + bm25_rank)) + (1.0 / (60 + vector_rank)) DESC
LIMIT 5;
```

**핵심 장점:**
- 키워드 기반 검색과 의미 기반 검색의 장점 결합
- 보다 포괄적이고 정확한 검색 결과 제공
- 다양한 검색 모달리티에서 유연한 랭킹 가능

**출처:** [ParadeDB Hybrid Search Guide](https://docs.paradedb.com/documentation/guides/hybrid)

## PRD 작성 전략

### 1. 명확한 스펙 제공
- Python 버전, 데이터베이스, 임베딩 모델 등 구체적 명시
- 정확한 테이블 이름과 컬럼 구조 제공
- 구현할 때 참고할 페이지 제공

### 2. PRD 프롬프트
```
스펙:
- Python, uv 패키지 매니저
- Neon PostgreSQL (pgvector, pg_search 확장)
- OpenAI text-embedding-3-small
- psycopg2

데이터베이스:
- Neon MCP 사용
- 프로젝트: nonghyup-loan
- 테이블: loan_products

핵심 기능:
- 대출 상품 데이터 파일(loan_products.json)을 loan_products 테이블에 저장
- 대출 상품이 searchable_text 를 bm25로 검색하기 좋게 특수문자 제거하여 cleaned_searchable_text 생성 -> bm25 search
- searchable_text 를 embedding해서 searchable_text_embedding에 저장 -> vector search
- hybrid_search(): RRF로 vector, bm25 search 결합
  - https://docs.paradedb.com/documentation/guides/hybrid 참고 구현
  - bm25, vector search 할 때는 테이블 전체를 대상으로 계산

CLI 동작:
uv run python ... "의사 전용 대출"

주의:
- PRD는 핵심만 간략하게
- 구체적인 SQL 코드 작성하지 않기
- 구현 세부사항은 AI에게 맡기기
```

---

## PRD 작성 시 체크리스트

### AI가 좋아하는 PRD
✅ 정확한 기술 스택 (pgvector, OpenAI 모델명, PostgreSQL 확장)
✅ 명확한 입출력 정의 (CLI 명령어 예시)
✅ 구체적인 알고리즘 (RRF 공식, 코사인 거리)
✅ 실제 데이터 정보 (테이블명, 컬럼명, 데이터 개수)

### AI가 싫어하는 PRD
❌ "좋은 검색 시스템 만들어줘"
❌ "적당히 하이브리드 검색해줘"
❌ 버전 정보 없음
❌ 모호한 요구사항

---

**참고 자료:**
- pgvector GitHub: https://github.com/pgvector/pgvector
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- paradedb : https://docs.paradedb.com/documentation/guides/hybrid
