# PRD: 농협 대출 상품 Hybrid Search

## 개요
대출 상품 데이터에 대해 BM25 키워드 검색과 벡터 유사도 검색을 결합한 하이브리드 검색 시스템

## 기술 스택
- **언어/패키지 관리**: Python, uv
- **데이터베이스**: Neon PostgreSQL
  - 확장: pgvector, pg_search
  - 프로젝트명: nonghyup-loan
- **임베딩**: OpenAI text-embedding-3-small
- **DB 클라이언트**: psycopg2
- **MCP**: Neon MCP 서버

## 데이터 구조
### 테이블: loan_products
- 대출 상품 기본 정보
- `searchable_text`: 검색 대상 원본 텍스트
- `cleaned_searchable_text`: 특수문자 제거한 BM25 검색용 텍스트
- `searchable_text_embedding`: 벡터 검색용 임베딩 (1536차원)

## 핵심 기능

### 1. 데이터 초기화
- `loan_products.json` 파일에서 대출 상품 데이터 로드
- PostgreSQL 테이블에 저장
- 텍스트 정제 및 임베딩 생성

### 2. BM25 키워드 검색
- `cleaned_searchable_text`를 대상으로 전문 검색
- pg_search 확장의 BM25 알고리즘 활용
- 테이블 전체 대상 검색

### 3. 벡터 유사도 검색
- 쿼리 텍스트를 임베딩으로 변환
- `searchable_text_embedding`과 코사인 유사도 계산
- pgvector 확장 활용
- 테이블 전체 대상 검색

### 4. 하이브리드 검색
- BM25와 벡터 검색 결과를 RRF(Reciprocal Rank Fusion)로 결합
- ParadeDB 가이드 참조: https://docs.paradedb.com/documentation/guides/hybrid
- 최종 순위 통합 점수 반환

## CLI 인터페이스
```bash
uv run python [스크립트] "검색어"
```

**사용 예시:**
```bash
uv run python search.py "의사 전용 대출"
```

## 구현 가이드
- Neon MCP를 통해 DB 작업 수행
- 임베딩 생성은 OpenAI API 활용
- RRF 알고리즘은 ParadeDB 문서 참조
- 구체적인 SQL과 구현은 개발자/AI 판단에 위임
