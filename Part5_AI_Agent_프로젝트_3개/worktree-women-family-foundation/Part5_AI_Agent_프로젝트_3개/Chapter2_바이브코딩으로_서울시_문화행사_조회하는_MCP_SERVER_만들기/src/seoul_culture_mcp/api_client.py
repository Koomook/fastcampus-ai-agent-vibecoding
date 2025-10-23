import httpx
from typing import Optional, Dict, Any
import os
from urllib.parse import quote


class SeoulCultureAPIClient:
    """서울시 문화행사 API 클라이언트"""

    BASE_URL = "http://openapi.seoul.go.kr:8088"
    SERVICE_NAME = "culturalEventInfo"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SEOUL_API_KEY", "sample")
        self.client = httpx.AsyncClient(timeout=30.0)

    def _build_url(
        self,
        start_index: int,
        end_index: int,
        codename: Optional[str] = None,
        title: Optional[str] = None,
        date: Optional[str] = None
    ) -> str:
        """
        API URL 구성

        URL 형식: {BASE_URL}/{KEY}/{TYPE}/{SERVICE}/{START}/{END}/{CODENAME}/{TITLE}/{DATE}
        선택 파라미터는 순서대로 URL 경로에 포함되어야 함
        """
        # 기본 URL 구성
        url_parts = [
            self.BASE_URL,
            self.api_key,
            "json",  # TYPE
            self.SERVICE_NAME,
            str(start_index),
            str(end_index)
        ]

        # 선택 파라미터 추가 (순서 중요)
        if codename or title or date:
            url_parts.append(quote(codename) if codename else "")
        if title or date:
            url_parts.append(quote(title) if title else "")
        if date:
            url_parts.append(date)  # 날짜는 이미 YYYY-MM-DD 형식

        return "/".join(url_parts) + "/"

    async def search_events(
        self,
        start_index: int = 1,
        end_index: int = 100,
        codename: Optional[str] = None,
        title: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        문화행사 검색

        Args:
            start_index: 시작 인덱스 (1부터 시작)
            end_index: 종료 인덱스 (최대 1000)
            codename: 행사 분류 (전시/미술, 콘서트, 클래식, 연극, 기타)
            title: 공연/행사명 검색어
            date: 날짜 (YYYY-MM-DD 형식)

        Returns:
            API 응답 (JSON)
        """
        url = self._build_url(start_index, end_index, codename, title, date)

        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API 요청 실패: {e.response.status_code}")
        except httpx.RequestError as e:
            raise Exception(f"네트워크 오류: {str(e)}")

    async def close(self):
        """HTTP 클라이언트 종료"""
        await self.client.aclose()
