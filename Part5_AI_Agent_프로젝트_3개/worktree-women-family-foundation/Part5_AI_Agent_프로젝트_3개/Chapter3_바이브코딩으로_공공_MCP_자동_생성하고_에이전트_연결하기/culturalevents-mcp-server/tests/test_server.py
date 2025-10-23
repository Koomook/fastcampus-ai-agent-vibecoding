"""Test server tools and functionality."""

import os
from unittest.mock import patch

import pytest

from data_seoul_mcp.culturalevents_mcp_server.server import (
    ApiResponse,
    CulturalEvent,
    search_cultural_events,
)


@pytest.fixture
def sample_event_data():
    """Sample event data from Seoul API.

    Note: Seoul Open Data API returns fields in UPPERCASE.
    """
    return {
        'ORG_NAME': '기타',
        'USE_FEE': 'VIP석 77,000원 R석 66,000원 A석 55,000원',
        'PLAYER': None,
        'ORG_LINK': 'https://tickets.interpark.com/goods/25009778',
        'GUNAME': '용산구',
        'MAIN_IMG': 'https://culture.seoul.go.kr/cmmn/file/getImage.do?atchFileId=311fd9815943420c808f1a00933ae9fb&thumb=Y',
        'THEMECODE': '기타',
        'DATE': '2025-12-13~2025-12-13',
        'ETC_DESC': None,
        'END_DATE': '2025-12-13 00:00:00.0',
        'TITLE': '2025 카즈미 타테이시 트리오 내한공연 [지브리, 재즈를 만나다-서울]',
        'TICKET': '시민',
        'CODENAME': '콘서트',
        'USE_TRGT': '성인, 청소년',
        'PROGRAM': None,
        'LOT': '126.990478820837',
        'RGSTDATE': '2025-07-11',
        'STRTDATE': '2025-12-13 00:00:00.0',
        'PLACE': '용산아트홀 대극장 미르',
        'HMPG_ADDR': 'https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=154341&menuNo=200008',
        'LAT': '37.5324522944579',
        'IS_FREE': '유료',
    }


@pytest.fixture
def sample_api_response(sample_event_data):
    """Sample API response structure."""
    return {
        'culturalEventInfo': {
            'list_total_count': 1,
            'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다'},
            'row': [sample_event_data],
        }
    }


@pytest.fixture
def sample_api_error_response():
    """Sample API error response."""
    return {
        'culturalEventInfo': {
            'RESULT': {'CODE': 'ERROR-300', 'MESSAGE': '필수 값이 누락되어 있습니다'}
        }
    }


class TestCulturalEvent:
    """Test CulturalEvent model."""

    def test_cultural_event_creation(self, sample_event_data):
        """Test creating CulturalEvent from sample data."""
        # Act
        event = CulturalEvent(**sample_event_data)

        # Assert
        assert event.codename == '콘서트'
        assert event.title == '2025 카즈미 타테이시 트리오 내한공연 [지브리, 재즈를 만나다-서울]'
        assert event.guname == '용산구'
        assert event.place == '용산아트홀 대극장 미르'
        assert event.is_free == '유료'


class TestFetchCulturalEvents:
    """Test fetch_cultural_events function with mocked responses."""

    def test_url_building_logic(self):
        """Test URL building with various parameters."""
        # Test basic URL structure
        base_url = 'http://openapi.seoul.go.kr:8088'
        api_key = 'test_key'
        service_name = 'culturalEventInfo'
        start_index = 1
        end_index = 5

        # Build URL without filters
        path_parts = [api_key, 'json', service_name, str(start_index), str(end_index)]
        url = f'{base_url}/{"/".join(path_parts)}/'
        assert url == 'http://openapi.seoul.go.kr:8088/test_key/json/culturalEventInfo/1/5/'

        # Build URL with filters
        path_parts = [
            api_key,
            'json',
            service_name,
            str(start_index),
            str(end_index),
            '콘서트',
            '재즈',
            '2025-12-13',
        ]
        url = f'{base_url}/{"/".join(path_parts)}/'
        assert (
            url
            == 'http://openapi.seoul.go.kr:8088/test_key/json/culturalEventInfo/1/5/콘서트/재즈/2025-12-13/'
        )


@pytest.mark.asyncio
class TestSearchCulturalEvents:
    """Test search_cultural_events tool."""

    async def test_search_missing_api_key(self):
        """Test error when API key is missing."""
        # Arrange
        with patch.dict(os.environ, {}, clear=True):
            # Act
            result = await search_cultural_events()

            # Assert
            assert result['status'] == 'error'
            assert 'SEOUL_API_KEY' in result['error_message']

    async def test_search_invalid_start_index(self):
        """Test validation of start_index."""
        # Arrange
        with patch.dict(os.environ, {'SEOUL_API_KEY': 'test_key'}):
            # Act
            result = await search_cultural_events(start_index=0)

            # Assert
            assert result['status'] == 'error'
            assert 'start_index must be >= 1' in result['error_message']

    async def test_search_invalid_end_index(self):
        """Test validation of end_index."""
        # Arrange
        with patch.dict(os.environ, {'SEOUL_API_KEY': 'test_key'}):
            # Act
            result = await search_cultural_events(start_index=10, end_index=5)

            # Assert
            assert result['status'] == 'error'
            assert 'end_index must be >= start_index' in result['error_message']

    async def test_search_too_many_records(self):
        """Test validation of max records per request."""
        # Arrange
        with patch.dict(os.environ, {'SEOUL_API_KEY': 'test_key'}):
            # Act
            result = await search_cultural_events(start_index=1, end_index=1500)

            # Assert
            assert result['status'] == 'error'
            assert 'Cannot request more than 1000 records' in result['error_message']

    @patch('data_seoul_mcp.culturalevents_mcp_server.server.fetch_cultural_events')
    async def test_search_success(self, mock_fetch, sample_event_data):
        """Test successful search."""
        # Arrange
        with patch.dict(os.environ, {'SEOUL_API_KEY': 'test_key'}):
            mock_event = CulturalEvent(**sample_event_data)
            mock_fetch.return_value = ApiResponse(
                status='success', total_count=1, events=[mock_event]
            )

            # Act
            result = await search_cultural_events(codename='콘서트', start_index=1, end_index=10)

            # Assert
            assert result['status'] == 'success'
            assert result['total_count'] == 1
            assert result['count'] == 1
            assert len(result['events']) == 1
            assert result['events'][0]['codename'] == '콘서트'

    @patch('data_seoul_mcp.culturalevents_mcp_server.server.fetch_cultural_events')
    async def test_search_with_all_filters(self, mock_fetch):
        """Test search with all filter parameters."""
        # Arrange
        with patch.dict(os.environ, {'SEOUL_API_KEY': 'test_key'}):
            mock_fetch.return_value = ApiResponse(status='success', total_count=0, events=[])

            # Act
            result = await search_cultural_events(
                codename='콘서트', title='재즈', date='2025-12-13', start_index=1, end_index=50
            )

            # Assert
            assert result['status'] == 'success'
            mock_fetch.assert_called_once_with(
                api_key='test_key',
                start_index=1,
                end_index=50,
                codename='콘서트',
                title='재즈',
                date='2025-12-13',
            )
