"""간단한 API 테스트 스크립트"""
import asyncio
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from seoul_culture_mcp.api_client import SeoulCultureAPIClient


async def test_api():
    """API 클라이언트 기본 테스트"""
    client = SeoulCultureAPIClient()

    print("=" * 50)
    print("서울시 문화행사 MCP Server - API 테스트")
    print("=" * 50)
    print()

    try:
        # 기본 검색 테스트 (샘플 키로 5개 조회)
        print("1. 기본 검색 테스트 (1-5번 조회)")
        print("-" * 50)
        response = await client.search_events(start_index=1, end_index=5)

        if "culturalEventInfo" in response:
            result = response["culturalEventInfo"]

            # 에러 체크
            if "RESULT" in result:
                result_info = result["RESULT"]
                print(f"응답 코드: {result_info.get('CODE')}")
                print(f"응답 메시지: {result_info.get('MESSAGE')}")
                print()

            # 행사 정보 출력
            if "row" in result:
                events = result["row"]
                print(f"총 {result.get('list_total_count', 0)}개 중 {len(events)}개 조회")
                print()

                for i, event in enumerate(events, 1):
                    print(f"{i}. {event.get('TITLE', 'N/A')}")
                    print(f"   분류: {event.get('CODENAME', 'N/A')}")
                    print(f"   기간: {event.get('DATE', 'N/A')}")
                    print(f"   장소: {event.get('PLACE', 'N/A')}")
                    print(f"   자치구: {event.get('GUNAME', 'N/A')}")
                    print()
            else:
                print("행사 정보가 없습니다.")
        else:
            print("예상치 못한 응답 형식:")
            print(response)

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

    finally:
        await client.close()

    print("=" * 50)
    print("✅ 테스트 완료")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_api())
