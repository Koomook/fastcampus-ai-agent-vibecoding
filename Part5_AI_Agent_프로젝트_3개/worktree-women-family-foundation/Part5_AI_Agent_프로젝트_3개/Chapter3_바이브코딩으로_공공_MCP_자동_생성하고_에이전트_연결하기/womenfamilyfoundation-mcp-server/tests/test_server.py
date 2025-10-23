"""Test server tools and functionality."""

from unittest.mock import AsyncMock, patch

import pytest

from data_seoul_mcp.womenfamilyfoundation_mcp_server.server import (
    WomenFamilyEvent,
    _fetch_events,
    get_event_details,
    list_event_types,
    search_events,
)


class TestWomenFamilyEventModel:
    """Test WomenFamilyEvent Pydantic model."""

    def test_event_model_creation(self, sample_event):
        """Test creating an event model from sample data."""
        # Act
        event = WomenFamilyEvent(**sample_event)

        # Assert
        assert event.evt_reg_no == '30378'
        assert event.title == '[서울형 아이돌봄비] 독감예방접종 시기'
        assert event.evt_type == '기타'
        assert event.evt_place == '온라인'

    def test_event_model_validation(self):
        """Test event model validation with missing fields."""
        # Arrange
        incomplete_data = {
            'evt_reg_no': '12345',
            'title': 'Test Event',
        }

        # Act & Assert
        with pytest.raises(Exception):  # Pydantic ValidationError
            WomenFamilyEvent(**incomplete_data)


@pytest.mark.asyncio
class TestFetchEvents:
    """Test _fetch_events internal function."""

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server.httpx.AsyncClient')
    async def test_fetch_events_success(self, mock_client, sample_api_response):
        """Test successful event fetching."""
        # Arrange
        mock_response = AsyncMock()
        mock_response.json = lambda: sample_api_response  # Non-async method
        mock_response.raise_for_status = lambda: None

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        # Act
        result = await _fetch_events(start_index=1, end_index=5)

        # Assert
        assert result['list_total_count'] == 3
        assert len(result['row']) == 3
        assert result['RESULT']['CODE'] == 'INFO-000'

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server.httpx.AsyncClient')
    async def test_fetch_events_with_filters(self, mock_client, sample_api_response):
        """Test fetching events with filters."""
        # Arrange
        mock_response = AsyncMock()
        mock_response.json = lambda: sample_api_response  # Non-async method
        mock_response.raise_for_status = lambda: None

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        # Act
        result = await _fetch_events(
            start_index=1,
            end_index=5,
            evt_reg_no='30378',
            title='독감',
        )

        # Assert
        assert 'row' in result
        assert result['RESULT']['CODE'] == 'INFO-000'


@pytest.mark.asyncio
class TestSearchEvents:
    """Test search_events tool."""

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_search_basic(self, mock_fetch, sample_api_response):
        """Test basic event search."""
        # Arrange
        mock_fetch.return_value = sample_api_response['SeoulWomenPlazaEvent']

        # Act
        result = await search_events()

        # Assert
        assert result['status'] == 'success'
        assert result['total_count'] == 3
        assert len(result['events']) == 3
        assert 'evt_reg_no' in result['events'][0]

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_search_with_keyword(self, mock_fetch, sample_api_response):
        """Test searching events with keyword."""
        # Arrange
        mock_fetch.return_value = sample_api_response['SeoulWomenPlazaEvent']

        # Act
        result = await search_events(keyword='아이돌봄')

        # Assert
        assert result['status'] == 'success'
        assert result['total_count'] == 3

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_search_with_event_type(self, mock_fetch, sample_api_response):
        """Test searching events with event type filter."""
        # Arrange
        mock_fetch.return_value = sample_api_response['SeoulWomenPlazaEvent']

        # Act
        result = await search_events(event_type='기타')

        # Assert
        assert result['status'] == 'success'
        # Should filter to only '기타' type events
        for event in result['events']:
            assert event['evt_type'] == '기타'

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_search_pagination_limit(self, mock_fetch):
        """Test pagination limit validation."""
        # Act
        result = await search_events(start_index=1, end_index=1002)

        # Assert
        assert result['status'] == 'error'
        assert 'Maximum 1000 items' in result['message']
        assert mock_fetch.call_count == 0

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_search_api_error(self, mock_fetch, api_error_response):
        """Test handling API error response."""
        # Arrange
        mock_fetch.return_value = api_error_response['SeoulWomenPlazaEvent']

        # Act
        result = await search_events()

        # Assert
        assert result['status'] == 'error'
        assert '필수 값이 누락되어 있습니다' in result['message']
        assert result['total_count'] == 0


@pytest.mark.asyncio
class TestGetEventDetails:
    """Test get_event_details tool."""

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_get_event_success(self, mock_fetch, sample_api_response):
        """Test getting event details successfully."""
        # Arrange
        mock_fetch.return_value = sample_api_response['SeoulWomenPlazaEvent']

        # Act
        result = await get_event_details(evt_reg_no='30378')

        # Assert
        assert result['status'] == 'success'
        assert result['event']['evt_reg_no'] == '30378'
        assert result['event']['title'] == '[서울형 아이돌봄비] 독감예방접종 시기'

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_get_event_not_found(self, mock_fetch):
        """Test getting event details when event not found."""
        # Arrange
        mock_fetch.return_value = {
            'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다'},
            'row': [],
        }

        # Act
        result = await get_event_details(evt_reg_no='99999')

        # Assert
        assert result['status'] == 'error'
        assert 'not found' in result['message'].lower()
        assert result['event'] is None


@pytest.mark.asyncio
class TestListEventTypes:
    """Test list_event_types tool."""

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_list_event_types_success(self, mock_fetch, sample_api_response):
        """Test listing event types successfully."""
        # Arrange
        mock_fetch.return_value = sample_api_response['SeoulWomenPlazaEvent']

        # Act
        result = await list_event_types()

        # Assert
        assert result['status'] == 'success'
        assert len(result['event_types']) == 2  # '기타' and '컨설팅'
        assert '기타' in result['event_types']
        assert '컨설팅' in result['event_types']

    @patch('data_seoul_mcp.womenfamilyfoundation_mcp_server.server._fetch_events')
    async def test_list_event_types_api_error(self, mock_fetch, api_error_response):
        """Test listing event types when API returns error."""
        # Arrange
        mock_fetch.return_value = api_error_response['SeoulWomenPlazaEvent']

        # Act
        result = await list_event_types()

        # Assert
        assert result['status'] == 'error'
        assert result['event_types'] == []
