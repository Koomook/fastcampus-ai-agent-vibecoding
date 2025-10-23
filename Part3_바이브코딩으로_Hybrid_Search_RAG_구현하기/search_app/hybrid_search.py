"""
하이브리드 검색 구현
BM25 키워드 검색과 벡터 유사도 검색을 RRF로 결합합니다.
"""
import os
import re
from typing import List, Dict, Tuple
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)


def clean_text(text: str) -> str:
    """특수문자를 제거하여 BM25 검색용 텍스트 생성"""
    if not text:
        return ""
    cleaned = re.sub(r'[^\w\s가-힣]', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def get_embedding(text: str) -> list:
    """OpenAI API를 사용하여 텍스트 임베딩 생성"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def bm25_search(conn, query: str, limit: int = 20) -> List[Tuple[str, float]]:
    """
    BM25 키워드 검색
    pg_search의 BM25 인덱스 사용
    Returns: [(product_id, score), ...]
    """
    cursor = conn.cursor()

    # BM25 인덱스가 없으면 생성
    # ngram 토크나이저 사용: 한글 검색을 위해 필수
    try:
        cursor.execute("""
            SELECT indexname FROM pg_indexes
            WHERE tablename = 'loan_products' AND indexname = 'idx_loan_products_bm25'
        """)
        if cursor.fetchone() is None:
            print("Creating BM25 index with ngram tokenizer...")
            cursor.execute("""
                CREATE INDEX idx_loan_products_bm25
                ON loan_products
                USING bm25(id, cleaned_searchable_text)
                WITH (key_field='id', text_fields='{"cleaned_searchable_text": {"tokenizer": {"type": "ngram", "min_gram": 2, "max_gram": 3, "prefix_only": false}}}');
            """)
            conn.commit()
            print("BM25 index created successfully with ngram tokenizer")
    except Exception as e:
        print(f"Index check/creation note: {e}")
        conn.rollback()

    # cleaned_searchable_text에 대한 BM25 검색
    # pg_search는 검색어를 그대로 전달
    search_query = """
    SELECT
        id,
        paradedb.score(id) as bm25_score
    FROM loan_products
    WHERE cleaned_searchable_text @@@ %s
    ORDER BY bm25_score DESC
    LIMIT %s
    """

    cleaned_query = clean_text(query)
    cursor.execute(search_query, (cleaned_query, limit))
    results = cursor.fetchall()
    cursor.close()

    return [(row[0], float(row[1])) for row in results]


def vector_search(conn, query: str, limit: int = 20) -> List[Tuple[str, float]]:
    """
    벡터 유사도 검색
    코사인 유사도 사용 (1 - cosine_distance)
    Returns: [(product_id, similarity), ...]
    """
    cursor = conn.cursor()

    # 쿼리 임베딩 생성
    query_embedding = get_embedding(query)

    # 벡터 검색 (코사인 유사도)
    search_query = """
    SELECT
        id,
        1 - (searchable_text_embedding <=> %s::vector) as similarity
    FROM loan_products
    WHERE searchable_text_embedding IS NOT NULL
    ORDER BY searchable_text_embedding <=> %s::vector
    LIMIT %s
    """

    cursor.execute(search_query, (query_embedding, query_embedding, limit))
    results = cursor.fetchall()
    cursor.close()

    return [(row[0], float(row[1])) for row in results]


def reciprocal_rank_fusion(
    bm25_results: List[Tuple[str, float]],
    vector_results: List[Tuple[str, float]],
    k: int = 60
) -> List[Tuple[str, float]]:
    """
    RRF (Reciprocal Rank Fusion) 알고리즘
    ParadeDB 가이드 참조: https://docs.paradedb.com/documentation/guides/hybrid

    RRF score = sum(1 / (k + rank))
    k는 일반적으로 60을 사용
    """
    rrf_scores = {}

    # BM25 결과 처리
    for rank, (product_id, _) in enumerate(bm25_results, start=1):
        if product_id not in rrf_scores:
            rrf_scores[product_id] = 0
        rrf_scores[product_id] += 1 / (k + rank)

    # 벡터 검색 결과 처리
    for rank, (product_id, _) in enumerate(vector_results, start=1):
        if product_id not in rrf_scores:
            rrf_scores[product_id] = 0
        rrf_scores[product_id] += 1 / (k + rank)

    # 점수 기준으로 정렬
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results


def hybrid_search(query: str, limit: int = 10) -> List[Dict]:
    """
    하이브리드 검색 실행
    BM25와 벡터 검색을 RRF로 결합
    """
    conn = psycopg2.connect(DATABASE_URL)

    # BM25 검색
    print("Running BM25 search...")
    bm25_results = bm25_search(conn, query, limit=20)
    print(f"  Found {len(bm25_results)} results")

    # 벡터 검색
    print("Running vector search...")
    vector_results = vector_search(conn, query, limit=20)
    print(f"  Found {len(vector_results)} results")

    # RRF 결합
    print("Combining with RRF...")
    rrf_results = reciprocal_rank_fusion(bm25_results, vector_results)

    # 상위 limit개 결과의 상세 정보 조회
    top_ids = [product_id for product_id, _ in rrf_results[:limit]]

    cursor = conn.cursor()
    detail_query = """
    SELECT
        id, product_code, product_name, product_summary,
        target_description, loan_limit_description
    FROM loan_products
    WHERE id = ANY(%s)
    """
    cursor.execute(detail_query, (top_ids,))
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    # 결과를 딕셔너리로 변환
    product_dict = {
        row[0]: {
            'id': row[0],
            'product_code': row[1],
            'product_name': row[2],
            'product_summary': row[3],
            'target_description': row[4],
            'loan_limit_description': row[5]
        }
        for row in products
    }

    # RRF 순서대로 결과 반환
    results = []
    for product_id, rrf_score in rrf_results[:limit]:
        if product_id in product_dict:
            result = product_dict[product_id].copy()
            result['rrf_score'] = rrf_score
            results.append(result)

    return results


def print_results(results: List[Dict]):
    """검색 결과 출력"""
    print(f"\n{'='*80}")
    print(f"검색 결과: {len(results)}개")
    print(f"{'='*80}\n")

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['product_name']}")
        print(f"   상품코드: {result['product_code']}")
        print(f"   RRF 점수: {result['rrf_score']:.4f}")
        print(f"   요약: {result['product_summary'][:100]}...")
        print(f"   대상: {result['target_description'][:100] if result['target_description'] else 'N/A'}...")
        print(f"   한도: {result['loan_limit_description'][:100] if result['loan_limit_description'] else 'N/A'}...")
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: uv run python hybrid_search.py \"검색어\"")
        sys.exit(1)

    query = sys.argv[1]
    print(f"검색어: {query}\n")

    results = hybrid_search(query)
    print_results(results)
