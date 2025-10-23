"""MCP 서버 기능 테스트"""
import asyncio
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from seoul_culture_mcp.server import search_cultural_events
import json


async def test_mcp_tools():
    """MCP Tools 및 Resources 테스트"""

    print("=" * 70)
    print("서울시 문화행사 MCP Server - MCP Tools 테스트")
    print("=" * 70)
    print()

    print("📝 참고: MCP Resources는 FastMCP 프레임워크를 통해 제공됩니다.")
    print("   - seoul://culture/api-info (API 정보)")
    print("   - seoul://culture/categories (카테고리 목록)")
    print("   - seoul://culture/districts (자치구 목록)")
    print()

    # Test 1: Search All Events (Tool)
    print("1. 전체 행사 검색 (Tool: search_cultural_events)")
    print("-" * 70)
    result = await search_cultural_events(start_index=1, end_index=5)
    data = json.loads(result)

    if "error" in data:
        print(f"❌ 오류: {data['error']}")
    else:
        print(f"✅ 총 {data.get('total_count', 0)}개 중 {len(data.get('events', []))}개 조회")
        for event in data.get('events', [])[:3]:  # 처음 3개만 출력
            print(f"  - {event.get('TITLE', 'N/A')} ({event.get('CODENAME', 'N/A')})")
    print()

    # Test 2: Search by Category (Tool)
    print("2. 콘서트 검색 (Tool: search_cultural_events, codename='콘서트')")
    print("-" * 70)
    result = await search_cultural_events(start_index=1, end_index=5, codename="콘서트")
    data = json.loads(result)

    if "error" in data:
        print(f"❌ 오류: {data['error']}")
    else:
        print(f"✅ 총 {data.get('total_count', 0)}개 중 {len(data.get('events', []))}개 조회")
        for event in data.get('events', [])[:3]:
            print(f"  - {event.get('TITLE', 'N/A')} ({event.get('DATE', 'N/A')})")
    print()

    # Test 3: Search by Date (Tool)
    print("3. 날짜별 검색 (Tool: search_cultural_events, date='2025-12-13')")
    print("-" * 70)
    result = await search_cultural_events(start_index=1, end_index=5, date="2025-12-13")
    data = json.loads(result)

    if "error" in data:
        print(f"❌ 오류: {data['error']}")
    else:
        print(f"✅ 총 {data.get('total_count', 0)}개 중 {len(data.get('events', []))}개 조회")
        for event in data.get('events', [])[:3]:
            print(f"  - {event.get('TITLE', 'N/A')} ({event.get('PLACE', 'N/A')})")
    print()

    # Test 4: Search by Title (Tool)
    print("4. 제목 검색 (Tool: search_cultural_events, title='지브리')")
    print("-" * 70)
    result = await search_cultural_events(start_index=1, end_index=5, title="지브리")
    data = json.loads(result)

    if "error" in data:
        print(f"❌ 오류: {data['error']}")
    else:
        print(f"✅ 총 {data.get('total_count', 0)}개 중 {len(data.get('events', []))}개 조회")
        for event in data.get('events', []):
            print(f"  - {event.get('TITLE', 'N/A')}")
            print(f"    기간: {event.get('DATE', 'N/A')}")
            print(f"    장소: {event.get('PLACE', 'N/A')}")
    print()

    # Test 5: Invalid Range (Error Case)
    print("5. 잘못된 범위 테스트 (Tool: search_cultural_events, range > 1000)")
    print("-" * 70)
    result = await search_cultural_events(start_index=1, end_index=2000)
    data = json.loads(result)

    if "error" in data:
        print(f"✅ 예상된 오류 처리: {data['error']}")
        print(f"   코드: {data.get('code', 'N/A')}")
    else:
        print("❌ 오류가 감지되지 않았습니다.")
    print()

    print("=" * 70)
    print("✅ 모든 테스트 완료")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
