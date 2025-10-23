# 농협 대출 상품 Hybrid Search

BM25 키워드 검색과 벡터 유사도 검색을 RRF(Reciprocal Rank Fusion)로 결합한 하이브리드 검색 시스템

## 기술 스택

- **언어/패키지 관리**: Python, uv
- **데이터베이스**: Neon PostgreSQL
  - 확장: pgvector, pg_search
  - 프로젝트명: nonghyup-loan
- **임베딩**: OpenAI text-embedding-3-small
- **DB 클라이언트**: psycopg2

## 설치 및 설정

### 1. 환경 변수 설정

`.env.example`을 `.env`로 복사하고 값을 설정합니다:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
DATABASE_URL=postgresql://neondb_owner:npg_Rk1LrSXMqld9@ep-twilight-math-af4s6ie7-pooler.c-2.us-west-2.aws.neon.tech/neondb?channel_binding=require&sslmode=require
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. 의존성 설치

```bash
uv sync
```

### 3. 데이터 로드

loan_products.json 파일을 데이터베이스에 로드하고 임베딩을 생성합니다:

```bash
uv run python load_data.py
```

이 과정은 시간이 걸릴 수 있습니다 (OpenAI API 호출).

## 사용법

### 하이브리드 검색 실행

```bash
uv run python hybrid_search.py "검색어"
```

**예시:**

```bash
uv run python hybrid_search.py "의사 전용 대출"
uv run python hybrid_search.py "공무원 생활안정자금"
uv run python hybrid_search.py "농업인 운전자금"
```

## 구현 상세

### 1. BM25 키워드 검색

- `cleaned_searchable_text` 컬럼을 대상으로 전문 검색
- pg_search 확장의 BM25 알고리즘 활용
- 특수문자를 제거한 정제된 텍스트 사용
- **ngram 토크나이저** 사용으로 한글 검색 지원 (min_gram=2, max_gram=3)

### 2. 벡터 유사도 검색

- 쿼리 텍스트를 임베딩으로 변환 (OpenAI text-embedding-3-small)
- `searchable_text_embedding` 컬럼과 코사인 유사도 계산
- pgvector 확장 활용

### 3. RRF (Reciprocal Rank Fusion)

ParadeDB 가이드 참조: https://docs.paradedb.com/documentation/guides/hybrid

```python
RRF score = sum(1 / (k + rank))
```

- BM25와 벡터 검색 결과를 각각 순위로 변환
- 각 결과의 RRF 점수를 합산하여 최종 순위 결정
- k=60 (일반적인 기본값)

## 파일 구조

```
search_app/
├── pyproject.toml          # 프로젝트 설정 및 의존성
├── .env.example            # 환경 변수 템플릿
├── .gitignore              # Git 제외 파일
├── README.md               # 프로젝트 문서
├── load_data.py            # 데이터 로드 스크립트
└── hybrid_search.py        # 하이브리드 검색 구현
```

## 데이터베이스 스키마

### loan_products 테이블

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | TEXT | 기본키 |
| product_code | TEXT | 상품 코드 |
| product_name | TEXT | 상품명 |
| searchable_text | TEXT | 검색 대상 원본 텍스트 |
| cleaned_searchable_text | TEXT | 특수문자 제거한 BM25 검색용 텍스트 |
| searchable_text_embedding | vector(1536) | 벡터 검색용 임베딩 |
| ... | ... | 기타 상품 정보 필드 |

## 참고 자료

- [ParadeDB Hybrid Search Guide](https://docs.paradedb.com/documentation/guides/hybrid)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [pg_search Extension](https://github.com/paradedb/paradedb/tree/dev/pg_search)
