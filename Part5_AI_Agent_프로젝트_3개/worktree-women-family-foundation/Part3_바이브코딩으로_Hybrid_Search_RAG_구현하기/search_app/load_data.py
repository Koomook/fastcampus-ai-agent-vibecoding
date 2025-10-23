"""
데이터 로드 스크립트
loan_products.json 파일을 읽어서 PostgreSQL에 저장하고 임베딩을 생성합니다.
"""
import json
import os
import re
from pathlib import Path
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
    # 한글, 영문, 숫자, 공백만 남기고 모두 제거
    cleaned = re.sub(r'[^\w\s가-힣]', ' ', text)
    # 연속된 공백을 하나로 변경
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


def get_embedding(text: str) -> list:
    """OpenAI API를 사용하여 텍스트 임베딩 생성"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def load_json_data(json_path: str) -> list:
    """JSON 파일 로드"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def insert_product(conn, product: dict):
    """제품 데이터를 데이터베이스에 삽입"""
    cursor = conn.cursor()

    # searchable_text 정제 및 임베딩 생성
    searchable_text = product.get('searchable_text', '')
    cleaned_searchable_text = clean_text(searchable_text)

    print(f"Processing: {product.get('product_name')} ({product.get('id')})")

    # 임베딩 생성
    embedding = get_embedding(searchable_text)

    # INSERT 쿼리
    insert_query = """
    INSERT INTO loan_products (
        id, product_code, product_name, product_summary, product_description,
        target_description, loan_limit_description, loan_period_guide, repayment_method,
        min_interest_rate, max_interest_rate, required_documents, customer_cost_info,
        early_repayment_info, overdue_interest_info, important_notices,
        is_available, is_sale_available, can_apply_online, can_apply_mobile,
        can_apply_branch, registered_at, last_modified_at, searchable_text,
        cleaned_searchable_text, searchable_text_embedding
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (id) DO UPDATE SET
        product_name = EXCLUDED.product_name,
        searchable_text = EXCLUDED.searchable_text,
        cleaned_searchable_text = EXCLUDED.cleaned_searchable_text,
        searchable_text_embedding = EXCLUDED.searchable_text_embedding
    """

    cursor.execute(insert_query, (
        product.get('id'),
        product.get('product_code'),
        product.get('product_name'),
        product.get('product_summary'),
        product.get('product_description'),
        product.get('target_description'),
        product.get('loan_limit_description'),
        product.get('loan_period_guide'),
        product.get('repayment_method'),
        product.get('min_interest_rate'),
        product.get('max_interest_rate'),
        product.get('required_documents'),
        product.get('customer_cost_info'),
        product.get('early_repayment_info'),
        product.get('overdue_interest_info'),
        product.get('important_notices'),
        product.get('is_available'),
        product.get('is_sale_available'),
        product.get('can_apply_online'),
        product.get('can_apply_mobile'),
        product.get('can_apply_branch'),
        product.get('registered_at'),
        product.get('last_modified_at'),
        searchable_text,
        cleaned_searchable_text,
        embedding
    ))

    conn.commit()
    cursor.close()


def main():
    """메인 함수"""
    import sys

    # JSON 파일 경로
    json_path = Path(__file__).parent.parent / "loan_products.json"

    if not json_path.exists():
        print(f"Error: {json_path} 파일을 찾을 수 없습니다.")
        return

    # JSON 데이터 로드
    print("Loading JSON data...")
    products = load_json_data(str(json_path))
    print(f"Total products: {len(products)}")

    # 제한된 개수만 로드 (선택적)
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
        products = products[:limit]
        print(f"Loading only first {limit} products...")

    # 데이터베이스 연결
    print("\nConnecting to database...")
    conn = psycopg2.connect(DATABASE_URL)

    # 데이터 삽입
    print("\nInserting products...")
    for i, product in enumerate(products, 1):
        try:
            insert_product(conn, product)
            print(f"  [{i}/{len(products)}] Inserted successfully")
        except Exception as e:
            print(f"  [{i}/{len(products)}] Error: {e}")
            conn.rollback()

    # 연결 종료
    conn.close()
    print("\nData loading completed!")


if __name__ == "__main__":
    main()
