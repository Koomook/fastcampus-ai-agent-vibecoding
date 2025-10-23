"""Pytest configuration and fixtures for Seoul Cultural Events Reservation MCP Server."""

import pytest


@pytest.fixture
def sample_query():
    """Sample query fixture for testing."""
    return 'test query'


@pytest.fixture
def sample_event_data():
    """Sample event data fixture based on actual API response.

    Uses uppercase field names and string datetimes as returned by the Seoul Open Data API.
    Note: Datetime fields can be either strings or unix timestamps depending on the API response.
    """
    return {
        'SVCSTATNM': '접수중',
        'USETGTINFO': ' 제한없음',
        'GUBUN': '자체',
        'RCPTENDDT': '2025-10-30 17:00:00.0',
        'SVCOPNENDDT': '2025-11-01 17:00:00.0',
        'SVCID': 'S250220094425372104',
        'V_MAX': '17:00',
        'V_MIN': '10:00',
        'TELNO': '02-724-0200, 0232',
        'MINCLASSNM': '전시/관람',
        'PAYATNM': '무료',
        'SVCURL': 'https://yeyak.seoul.go.kr/web/reservation/selectReservView.do?rsv_svc_id=S250220094425372104',
        'REVSTDDAYNM': '이용일',
        'REVSTDDAY': '1',
        'PLACENM': '서울역사박물관>백인제가옥',
        'DTLCONT': '백인제가옥 전시해설 안내',
        'AREANM': '종로구',
        'RCPTBGNDT': '2024-12-20 00:00:00.0',
        'SVCOPNBGNDT': '2025-01-01 00:00:00.0',
        'SVCNM': '2025 백인제가옥 전시해설 예약',
        'Y': '37.580446301109994',
        'IMGURL': 'https://yeyak.seoul.go.kr/web/common/file/FileDown.do?file_id=1740012323501PI2FJLA29ZJ7LNKL9E2EYW0IZ',
        'MAXCLASSNM': '문화체험',
        'X': '126.98409156389061',
    }
