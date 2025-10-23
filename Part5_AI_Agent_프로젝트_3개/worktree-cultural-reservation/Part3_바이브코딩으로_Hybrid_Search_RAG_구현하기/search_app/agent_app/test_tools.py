"""
Agent 도구 테스트 스크립트
hybrid_search_tool과 tavily_search_tool의 동작을 확인합니다.
"""
import sys
import os

# 경로 설정
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agent_app.api.utils.tools import hybrid_search_tool, tavily_search_tool


def test_hybrid_search():
    """하이브리드 검색 도구 테스트"""
    print("\n" + "="*80)
    print("1. Hybrid Search Tool 테스트")
    print("="*80)

    query = "의사 전용 대출"
    print(f"\n검색어: {query}")

    try:
        results = hybrid_search_tool(query, limit=3)
        print(f"검색 결과: {len(results)}개")

        for i, result in enumerate(results, 1):
            print(f"\n[상품 {i}]")
            print(f"  상품명: {result.get('product_name', 'N/A')}")
            print(f"  상품코드: {result.get('product_code', 'N/A')}")
            print(f"  RRF 점수: {result.get('rrf_score', 0):.4f}")
            print(f"  요약: {result.get('product_summary', 'N/A')[:100]}...")

        return True
    except Exception as e:
        print(f"오류 발생: {e}")
        return False


def test_tavily_search():
    """Tavily 웹 검색 도구 테스트"""
    print("\n" + "="*80)
    print("2. Tavily Search Tool 테스트")
    print("="*80)

    query = "2025년 한국 기준금리"
    print(f"\n검색어: {query}")

    try:
        results = tavily_search_tool(query, max_results=3)
        print(f"검색 결과: {len(results)}개")

        for i, result in enumerate(results, 1):
            print(f"\n[결과 {i}]")
            print(f"  제목: {result.get('title', 'N/A')}")
            print(f"  URL: {result.get('url', 'N/A')}")
            print(f"  점수: {result.get('score', 0):.4f}")
            print(f"  내용: {result.get('content', 'N/A')[:150]}...")

        return True
    except Exception as e:
        print(f"오류 발생: {e}")
        return False


def main():
    """메인 테스트 실행"""
    print("\n" + "="*80)
    print("Agent 도구 테스트")
    print("="*80)

    # 1. Hybrid Search 테스트
    hybrid_ok = test_hybrid_search()

    # 2. Tavily Search 테스트
    tavily_ok = test_tavily_search()

    # 결과 요약
    print("\n" + "="*80)
    print("테스트 결과 요약")
    print("="*80)
    print(f"Hybrid Search: {'✅ 성공' if hybrid_ok else '❌ 실패'}")
    print(f"Tavily Search: {'✅ 성공' if tavily_ok else '❌ 실패'}")

    if hybrid_ok and tavily_ok:
        print("\n모든 테스트가 성공했습니다! 🎉")
        print("\n다음 단계:")
        print("  1. cd agent_app")
        print("  2. pnpm install")
        print("  3. pnpm dev")
        print("  4. 브라우저에서 http://localhost:3000 접속")
    else:
        print("\n일부 테스트가 실패했습니다. 설정을 확인해주세요.")
        print("  - DATABASE_URL이 .env.local에 올바르게 설정되었는지 확인")
        print("  - TAVILY_API_KEY가 .env.local에 올바르게 설정되었는지 확인")


if __name__ == "__main__":
    main()
