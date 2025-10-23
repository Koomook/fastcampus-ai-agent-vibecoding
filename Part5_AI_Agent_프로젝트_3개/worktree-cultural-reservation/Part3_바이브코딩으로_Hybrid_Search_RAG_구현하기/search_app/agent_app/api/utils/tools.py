"""
Agent 도구 구현
- hybrid_search_tool: 농협 대출 상품 검색 (내부 DB)
- tavily_search_tool: 웹 검색 (최신 금융 정보)
"""
import os
import sys
import requests
from typing import List, Dict
from dotenv import load_dotenv

# 환경변수 로드 - 절대 경로로 .env.local 파일 지정
# tools.py의 위치: agent_app/api/utils/tools.py
# .env.local의 위치: agent_app/.env.local
env_path = os.path.join(os.path.dirname(__file__), '../../.env.local')
load_dotenv(env_path)

# uvicorn은 "cd .. && uvicorn agent_app.api.index:app"로 실행되므로
# 작업 디렉토리는 Part3_바이브코딩으로_Hybrid_Search_RAG_구현하기입니다.
# search_app 폴더를 sys.path에 추가하여 hybrid_search 모듈을 임포트합니다.
search_app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if search_app_dir not in sys.path:
    sys.path.insert(0, search_app_dir)

from hybrid_search import hybrid_search as execute_hybrid_search

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def hybrid_search_tool(query: str, limit: int = 3) -> List[Dict]:
    """
    농협 대출 상품 하이브리드 검색 도구

    Args:
        query: 검색할 질문 또는 키워드
        limit: 반환할 최대 결과 개수 (기본값: 3)

    Returns:
        검색된 대출 상품 목록
        각 상품은 id, product_name, product_summary, target_description 등을 포함
    """
    try:
        results = execute_hybrid_search(query, limit=limit)
        return results
    except Exception as e:
        print(f"Hybrid search error: {e}")
        return []


def tavily_search_tool(query: str, max_results: int = 3) -> List[Dict]:
    """
    Tavily 웹 검색 도구
    최신 금융 정보, 기준금리, 시장 동향 등을 검색

    Args:
        query: 검색할 질문 또는 키워드
        max_results: 반환할 최대 결과 개수 (기본값: 3)

    Returns:
        웹 검색 결과 목록
        각 결과는 title, url, content, score를 포함
    """
    if not TAVILY_API_KEY or TAVILY_API_KEY == "tvly-YOUR_API_KEY_HERE":
        return [{
            "title": "Tavily API Key Required",
            "url": "https://tavily.com/",
            "content": "Tavily API 키가 설정되지 않았습니다. .env.local 파일에 TAVILY_API_KEY를 설정해주세요.",
            "score": 0.0
        }]

    try:
        # Tavily Search API 호출
        url = "https://api.tavily.com/search"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",  # "basic" or "advanced"
            "include_answer": False,  # 요약 답변 포함 여부
            "include_raw_content": False  # 원본 HTML 포함 여부
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        return results

    except requests.RequestException as e:
        print(f"Tavily search error: {e}")
        return [{
            "title": "Search Error",
            "url": "",
            "content": f"웹 검색 중 오류가 발생했습니다: {str(e)}",
            "score": 0.0
        }]
