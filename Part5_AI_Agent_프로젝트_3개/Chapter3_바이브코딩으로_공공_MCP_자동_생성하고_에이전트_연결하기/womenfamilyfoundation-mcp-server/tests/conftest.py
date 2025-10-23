"""Pytest configuration and fixtures for Seoul Women Family Foundation Events MCP Server."""

import pytest


@pytest.fixture
def sample_api_response():
    """Sample API response fixture based on actual API format."""
    return {
        'SeoulWomenPlazaEvent': {
            'list_total_count': 3,
            'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다'},
            'row': [
                {
                    'evt_reg_end_date': '2025-12-31',
                    'evt_contact': '02-810-5158',
                    'title': '[서울형 아이돌봄비] 독감예방접종 시기',
                    'evt_type': '기타',
                    'evt_date': '2025-10-20~2025-12-31',
                    'evt_reg_start_date': '2025-10-20',
                    'evt_place': '온라인',
                    'evt_reg_method': '온라인',
                    'evt_sponsor': '서울시여성가족재단',
                    'url': 'https://www.seoulwomen.or.kr/sfwf/contents/sfwf-event.do?schM=view&page=1&viewCount=4&id=30378',
                    'evt_reg_no': '30378',
                    'evt_target': '서울형 아이돌봄비 이용자 및 조력자',
                },
                {
                    'evt_reg_end_date': '2025-10-30',
                    'evt_contact': '서울형 키즈카페지원단(02-810-5053)',
                    'title': '2025년 서울형 키즈카페 운영 우수사례 공모전',
                    'evt_type': '기타',
                    'evt_date': '2025-10-17~2025-10-30',
                    'evt_reg_start_date': '2025-10-17',
                    'evt_place': '-',
                    'evt_reg_method': '자치구 제출',
                    'evt_sponsor': '서울시/서울시여성가족재단',
                    'url': 'https://www.seoulwomen.or.kr/sfwf/contents/sfwf-event.do?schM=view&page=1&viewCount=4&id=30377',
                    'evt_reg_no': '30377',
                    'evt_target': '서울형 키즈카페(시립, 구립)',
                },
                {
                    'evt_reg_end_date': '2025-12-31',
                    'evt_contact': '02-810-5442',
                    'title': '[서울시아이돌봄지원사업] 10월 아이돌보미 카드뉴스(적극적이고 전문성 있는 돌봄서비스)',
                    'evt_type': '컨설팅',
                    'evt_date': '2025-10-16~2025-12-31',
                    'evt_reg_start_date': '2025-10-16',
                    'evt_place': '-',
                    'evt_reg_method': '-',
                    'evt_sponsor': '서울시여성가족재단',
                    'url': 'https://www.seoulwomen.or.kr/sfwf/contents/sfwf-event.do?schM=view&page=1&viewCount=4&id=30374',
                    'evt_reg_no': '30374',
                    'evt_target': '-',
                },
            ],
        },
    }


@pytest.fixture
def sample_event():
    """Sample single event fixture."""
    return {
        'evt_reg_no': '30378',
        'title': '[서울형 아이돌봄비] 독감예방접종 시기',
        'evt_reg_start_date': '2025-10-20',
        'evt_reg_end_date': '2025-12-31',
        'evt_type': '기타',
        'evt_date': '2025-10-20~2025-12-31',
        'evt_place': '온라인',
        'evt_target': '서울형 아이돌봄비 이용자 및 조력자',
        'evt_reg_method': '온라인',
        'evt_sponsor': '서울시여성가족재단',
        'evt_contact': '02-810-5158',
        'url': 'https://www.seoulwomen.or.kr/sfwf/contents/sfwf-event.do?schM=view&page=1&viewCount=4&id=30378',
    }


@pytest.fixture
def api_error_response():
    """API error response fixture."""
    return {
        'SeoulWomenPlazaEvent': {
            'RESULT': {
                'CODE': 'ERROR-300',
                'MESSAGE': '필수 값이 누락되어 있습니다.',
            },
        },
    }
