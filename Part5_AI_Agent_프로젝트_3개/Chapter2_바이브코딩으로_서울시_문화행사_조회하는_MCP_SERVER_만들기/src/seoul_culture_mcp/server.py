from fastmcp import FastMCP
from .api_client import SeoulCultureAPIClient
from typing import Optional
import os
import json

# MCP 서버 초기화
mcp = FastMCP(
    name="Seoul Cultural Events",
    instructions="서울시 문화행사 정보를 제공하는 MCP 서버입니다. search_cultural_events 도구를 사용하여 다양한 조건으로 문화행사를 검색할 수 있습니다."
)

# API 클라이언트 초기화
api_client = SeoulCultureAPIClient()


@mcp.tool()
async def search_cultural_events(
    start_index: int = 1,
    end_index: int = 100,
    codename: Optional[str] = None,
    title: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """
    서울시 문화행사를 검색합니다.

    Args:
        start_index: 시작 인덱스 (기본값: 1, 1부터 시작)
        end_index: 종료 인덱스 (기본값: 100, 최대: 1000)
        codename: 행사 분류 (전시/미술, 콘서트, 클래식, 연극, 기타)
        title: 공연/행사명 검색어
        date: 날짜 (YYYY-MM-DD 형식)

    Returns:
        문화행사 목록 (JSON 형식 문자열)

    Examples:
        - 모든 행사 조회: search_cultural_events()
        - 콘서트만 조회: search_cultural_events(codename="콘서트")
        - 특정 날짜: search_cultural_events(date="2025-12-13")
        - 행사명 검색: search_cultural_events(title="지브리")
    """
    try:
        # 입력 검증
        if end_index - start_index > 1000:
            return json.dumps({
                "error": "한 번에 최대 1000건까지만 조회 가능합니다.",
                "code": "INVALID_RANGE"
            }, ensure_ascii=False)

        # API 호출
        response = await api_client.search_events(
            start_index=start_index,
            end_index=end_index,
            codename=codename,
            title=title,
            date=date
        )

        # API 응답에서 culturalEventInfo 추출
        if "culturalEventInfo" in response:
            result = response["culturalEventInfo"]

            # 에러 체크
            if "RESULT" in result:
                result_info = result["RESULT"]
                if result_info.get("CODE") != "INFO-000":
                    return json.dumps({
                        "error": result_info.get("MESSAGE"),
                        "code": result_info.get("CODE")
                    }, ensure_ascii=False)

            # 정상 응답
            return json.dumps({
                "total_count": result.get("list_total_count", 0),
                "events": result.get("row", [])
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "error": "예상치 못한 API 응답 형식",
            "response": response
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "code": "INTERNAL_ERROR"
        }, ensure_ascii=False)


@mcp.tool()
async def search_free_events(
    start_index: int = 1,
    end_index: int = 100,
    is_free: str = "무료",
    codename: Optional[str] = None,
    title: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """
    무료/유료 여부로 필터링된 서울시 문화행사를 검색합니다.

    Args:
        start_index: 시작 인덱스 (기본값: 1, 1부터 시작)
        end_index: 종료 인덱스 (기본값: 100, 최대: 1000)
        is_free: 유무료 구분 (무료/유료/무료,유료 중 선택, 기본값: 무료)
        codename: 행사 분류 (전시/미술, 콘서트, 클래식, 연극, 기타)
        title: 공연/행사명 검색어
        date: 날짜 (YYYY-MM-DD 형식)

    Returns:
        무료/유료로 필터링된 문화행사 목록 (JSON 형식 문자열)

    Examples:
        - 무료 행사 조회: search_free_events(is_free="무료")
        - 유료 행사 조회: search_free_events(is_free="유료")
        - 무료 콘서트 조회: search_free_events(is_free="무료", codename="콘서트")
        - 특정 날짜의 무료 행사: search_free_events(is_free="무료", date="2025-12-13")
    """
    try:
        # 입력 검증
        if end_index - start_index > 1000:
            return json.dumps({
                "error": "한 번에 최대 1000건까지만 조회 가능합니다.",
                "code": "INVALID_RANGE"
            }, ensure_ascii=False)

        # is_free 값 검증
        valid_is_free_values = ["무료", "유료", "무료,유료"]
        if is_free not in valid_is_free_values:
            return json.dumps({
                "error": f"is_free는 {', '.join(valid_is_free_values)} 중 하나여야 합니다.",
                "code": "INVALID_IS_FREE"
            }, ensure_ascii=False)

        # API 호출 (더 많은 데이터를 가져와서 필터링)
        response = await api_client.search_events(
            start_index=start_index,
            end_index=end_index,
            codename=codename,
            title=title,
            date=date
        )

        # API 응답에서 culturalEventInfo 추출
        if "culturalEventInfo" in response:
            result = response["culturalEventInfo"]

            # 에러 체크
            if "RESULT" in result:
                result_info = result["RESULT"]
                if result_info.get("CODE") != "INFO-000":
                    return json.dumps({
                        "error": result_info.get("MESSAGE"),
                        "code": result_info.get("CODE")
                    }, ensure_ascii=False)

            # 무료/유료 필터링
            events = result.get("row", [])

            # is_free 값에 따라 필터링
            if is_free == "무료,유료":
                # 모든 이벤트 포함
                filtered_events = events
            else:
                # 지정된 is_free 값으로 필터링
                filtered_events = [
                    event for event in events
                    if event.get("IS_FREE") == is_free
                ]

            # 정상 응답
            return json.dumps({
                "total_count": len(filtered_events),
                "original_count": result.get("list_total_count", 0),
                "filter": is_free,
                "events": filtered_events
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "error": "예상치 못한 API 응답 형식",
            "response": response
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "error": str(e),
            "code": "INTERNAL_ERROR"
        }, ensure_ascii=False)


@mcp.resource("seoul://culture/api-info")
def get_api_info() -> str:
    """API 메타정보를 제공합니다."""
    return json.dumps({
        "service_name": "서울시 문화행사 정보",
        "provider": "서울특별시",
        "department": "문화본부 문화정책과",
        "update_frequency": "매일 1회",
        "data_format": "JSON",
        "max_results_per_request": 1000,
        "base_url": "http://openapi.seoul.go.kr:8088",
        "documentation": "https://data.seoul.go.kr/"
    }, ensure_ascii=False, indent=2)


@mcp.resource("seoul://culture/categories")
def get_categories() -> str:
    """사용 가능한 행사 카테고리 목록을 제공합니다."""
    return json.dumps({
        "categories": [
            {"code": "전시/미술", "description": "미술 전시 및 갤러리 행사"},
            {"code": "콘서트", "description": "대중음악 공연"},
            {"code": "클래식", "description": "클래식 음악 공연"},
            {"code": "연극", "description": "연극 및 뮤지컬"},
            {"code": "기타", "description": "기타 문화행사"}
        ]
    }, ensure_ascii=False, indent=2)


@mcp.resource("seoul://culture/districts")
def get_districts() -> str:
    """서울시 25개 자치구 목록을 제공합니다."""
    return json.dumps({
        "districts": [
            "강남구", "강동구", "강북구", "강서구",
            "관악구", "광진구", "구로구", "금천구",
            "노원구", "도봉구", "동대문구", "동작구",
            "마포구", "서대문구", "서초구", "성동구",
            "성북구", "송파구", "양천구", "영등포구",
            "용산구", "은평구", "종로구", "중구", "중랑구"
        ]
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # STDIO 방식으로 서버 실행 (기본값)
    mcp.run()
