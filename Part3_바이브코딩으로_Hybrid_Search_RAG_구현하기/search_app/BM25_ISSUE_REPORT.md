# BM25 검색 문제 리포트

## 문제 요약

Neon PostgreSQL의 pg_search 확장을 사용한 BM25 검색에서 특정 한글 키워드 검색이 실패하는 문제 발생.

## 환경

- **데이터베이스**: Neon PostgreSQL 17
- **확장**: pg_search (ParadeDB)
- **프로젝트**: nonghyup-loan (aged-hat-25164817)
- **테이블**: loan_products
- **검색 대상 컬럼**: cleaned_searchable_text (TEXT)

## 현상

### 작동하는 케이스

```sql
SELECT id, product_name, paradedb.score(id) as score
FROM loan_products
WHERE cleaned_searchable_text @@@ '공무원 대출'
ORDER BY score DESC LIMIT 5;
```

**결과**: ✅ 정상 작동 (6개 결과 반환)
- 공무원가계자금대출 (score: 3.67)
- NH햇살론15 (score: 0.55)
- 기타...

### 실패하는 케이스

```sql
SELECT id, product_name, paradedb.score(id) as score
FROM loan_products
WHERE cleaned_searchable_text @@@ '햇살론'
ORDER BY score DESC LIMIT 5;
```

**결과**: ❌ 0개 결과 반환

```sql
SELECT id, product_name, paradedb.score(id) as score
FROM loan_products
WHERE cleaned_searchable_text @@@ '서민금융'
ORDER BY score DESC LIMIT 5;
```

**결과**: ❌ 0개 결과 반환

```sql
SELECT id, product_name, paradedb.score(id) as score
FROM loan_products
WHERE cleaned_searchable_text @@@ '서민금융 햇살론'
ORDER BY score DESC LIMIT 5;
```

**결과**: ❌ 0개 결과 반환

## 데이터 검증

실제 데이터에는 해당 키워드가 존재함을 확인:

```sql
SELECT id, product_name,
       cleaned_searchable_text LIKE '%햇살론%' as has_hatsallon,
       cleaned_searchable_text LIKE '%서민금융%' as has_seomin
FROM loan_products
WHERE product_name LIKE '%햇살론%';
```

**결과**: ✅ 3개 제품 모두 true 반환
- NH햇살론119
- NH햇살론15(서민금융진흥원)
- NH햇살론뱅크

## BM25 인덱스 정보

```sql
CREATE INDEX idx_loan_products_bm25
ON public.loan_products
USING bm25 (id, cleaned_searchable_text)
WITH (key_field=id, text_fields='{"cleaned_searchable_text": {}}')
```

## 시도한 해결 방법

### 1. OR 연산자 사용
```sql
WHERE cleaned_searchable_text @@@ '햇살론 OR 서민금융'
```
**결과**: ❌ 여전히 0개

### 2. ParadeDB create_bm25 프로시저 사용 시도
```sql
CALL paradedb.create_bm25(
  index_name => 'idx_loan_products_bm25',
  table_name => 'loan_products',
  key_field => 'id',
  text_fields => paradedb.field('cleaned_searchable_text')
);
```
**결과**: ❌ 프로시저가 존재하지 않음

## 가설

### 1. 토크나이저 문제
pg_search의 BM25 인덱스가 한글 토큰화를 제대로 하지 못할 가능성
- "공무원 대출"은 작동 (띄어쓰기 포함)
- "햇살론" 단일 단어는 실패
- "서민금융" 단일 단어는 실패

### 2. 인덱스 생성 시점 문제
인덱스가 데이터 삽입 전에 생성되지 않아 일부 데이터가 인덱싱되지 않았을 가능성

### 3. pg_search 버전 또는 설정 문제
Neon의 pg_search 확장이 특정 한글 토큰에 대해 다른 동작을 할 가능성

## 영향

- **BM25 검색**: 부분적으로만 작동 (키워드 의존적)
- **벡터 검색**: ✅ 정상 작동
- **하이브리드 검색**: 부분적 결과 제공 (벡터 검색에 의존)

## 현재 상태

- 하이브리드 검색 자체는 작동하지만 BM25 부분이 불안정
- 벡터 검색이 대부분의 결과를 제공하고 있음
- RRF 통합 로직은 정상 작동

## 권장 해결 방안

### 단기 (즉시 적용 가능)
1. **PostgreSQL 기본 전문 검색 사용**
   - pg_search 대신 PostgreSQL의 `tsvector`와 `tsquery` 사용
   - 한글 지원이 더 안정적

2. **검색어 전처리 강화**
   - 형태소 분석기 추가 (예: mecab-ko)
   - n-gram 토큰화

### 중기 (추가 개발 필요)
1. **Elasticsearch 또는 OpenSearch 도입**
   - 더 강력한 한글 전문 검색 지원
   - 별도 검색 엔진 운영 필요

2. **pg_search 설정 최적화**
   - ParadeDB 공식 문서 참조하여 한글 토크나이저 설정
   - 커스텀 analyzer 설정

### 장기 (아키텍처 변경)
1. **벡터 검색 중심 전환**
   - 임베딩 기반 검색의 품질이 우수
   - BM25는 보조 수단으로만 활용

## 참고 자료

- ParadeDB 하이브리드 검색: https://docs.paradedb.com/documentation/guides/hybrid
- pg_search 문서: https://github.com/paradedb/paradedb/tree/dev/pg_search
- PostgreSQL 전문 검색: https://www.postgresql.org/docs/current/textsearch.html

## 테스트 로그

### 테스트 1: "공무원 대출"
- BM25: 6개 결과 ✅
- Vector: 10개 결과 ✅
- Hybrid: 10개 결과 (정확도 높음) ✅

### 테스트 2: "서민금융 햇살론"
- BM25: 0개 결과 ❌
- Vector: 10개 결과 ✅
- Hybrid: 10개 결과 (벡터에만 의존) ⚠️

## ✅ 해결 완료!

### 근본 원인
ParadeDB BM25 인덱스의 **기본 토크나이저**가 한글 단어를 제대로 토큰화하지 못함.

### 해결 방법
**ngram 토크나이저**로 변경:

```sql
CREATE INDEX idx_loan_products_bm25 ON loan_products
USING bm25 (id, cleaned_searchable_text)
WITH (
  key_field='id',
  text_fields='{
    "cleaned_searchable_text": {
      "tokenizer": {
        "type": "ngram",
        "min_gram": 2,
        "max_gram": 3,
        "prefix_only": false
      }
    }
  }'
);
```

### 테스트 결과 (해결 후)

#### "햇살론" 검색
```sql
SELECT id, product_name, paradedb.score(id) as score
FROM loan_products
WHERE cleaned_searchable_text @@@ '햇살론'
ORDER BY score DESC;
```
**결과**: ✅ 3개 결과 반환
- NH햇살론119 (score: 5.01)
- NH햇살론15 (score: 3.60)
- NH햇살론뱅크 (score: 3.50)

#### "서민금융 햇살론" 하이브리드 검색
- BM25: 3개 결과 ✅
- Vector: 10개 결과 ✅
- Hybrid: 정확한 순위로 통합 ✅

## 결론

**문제 완전 해결!** 🎉

ngram 토크나이저 적용으로 한글 검색이 완벽하게 작동합니다. 하이브리드 검색 시스템이 의도한 대로 BM25와 벡터 검색을 모두 활용하여 최적의 결과를 제공합니다.
