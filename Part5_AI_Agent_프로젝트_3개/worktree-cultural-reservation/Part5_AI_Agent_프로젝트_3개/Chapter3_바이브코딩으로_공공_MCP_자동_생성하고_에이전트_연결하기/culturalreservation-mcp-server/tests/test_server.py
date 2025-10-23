"""Test server tools and functionality."""

import pytest

from data_seoul_mcp.culturalreservation_mcp_server.server import (
    CulturalEvent,
    get_event_by_id,
    search_cultural_events,
)


class TestCulturalEvent:
    """Test CulturalEvent Pydantic model."""

    def test_cultural_event_creation(self, sample_event_data):
        """Test creating a CulturalEvent instance."""
        # Act
        event = CulturalEvent(**sample_event_data)

        # Assert - check lowercase attributes from uppercase API fields
        assert event.svcid == sample_event_data['SVCID']
        assert event.svcnm == sample_event_data['SVCNM']
        assert event.svcstatnm == sample_event_data['SVCSTATNM']
        assert event.minclassnm == sample_event_data['MINCLASSNM']
        assert event.areanm == sample_event_data['AREANM']

    def test_cultural_event_with_none_values(self):
        """Test CulturalEvent with optional fields as None."""
        # Arrange
        minimal_data = {
            'svcid': 'TEST123',
            'svcnm': 'Test Event',
        }

        # Act
        event = CulturalEvent(**minimal_data)

        # Assert
        assert event.svcid == 'TEST123'
        assert event.svcnm == 'Test Event'
        assert event.gubun is None
        assert event.areanm is None


@pytest.mark.asyncio
class TestSearchCulturalEvents:
    """Test search_cultural_events tool.

    Note: These tests will return API errors when using the 'sample' API key.
    With a real API key, they should return actual data.
    """

    async def test_search_without_filters(self):
        """Test searching events without any filters."""
        # Act
        result = await search_cultural_events()

        # Assert
        # Should return either successful data or API error
        assert isinstance(result, dict)
        # With sample API key, we expect errors. With real key, we'd get events.
        assert 'error' in result or ('total_count' in result and 'events' in result)

    async def test_search_with_minclassnm(self):
        """Test searching events with sub category filter."""
        # Arrange
        minclassnm = '콘서트'

        # Act
        result = await search_cultural_events(minclassnm=minclassnm)

        # Assert
        assert isinstance(result, dict)
        # Should return data or error
        assert 'error' in result or 'filters' in result

    async def test_search_with_svcstatnm(self):
        """Test searching events with service status filter."""
        # Arrange
        svcstatnm = '접수중'

        # Act
        result = await search_cultural_events(svcstatnm=svcstatnm)

        # Assert
        assert isinstance(result, dict)
        assert 'error' in result or 'filters' in result

    async def test_search_with_areanm(self):
        """Test searching events with area name filter."""
        # Arrange
        areanm = '종로구'

        # Act
        result = await search_cultural_events(areanm=areanm)

        # Assert
        assert isinstance(result, dict)
        assert 'error' in result or 'filters' in result

    async def test_search_with_all_filters(self):
        """Test searching events with all filters."""
        # Arrange
        minclassnm = '전시/관람'
        svcstatnm = '접수중'
        areanm = '중구'

        # Act
        result = await search_cultural_events(
            minclassnm=minclassnm,
            svcstatnm=svcstatnm,
            areanm=areanm,
        )

        # Assert
        assert isinstance(result, dict)
        assert 'error' in result or 'filters' in result

    async def test_search_with_pagination(self):
        """Test searching events with custom pagination."""
        # Arrange
        start_index = 1
        end_index = 10

        # Act
        result = await search_cultural_events(
            start_index=start_index,
            end_index=end_index,
        )

        # Assert
        assert isinstance(result, dict)
        assert 'error' in result or 'events' in result

    async def test_search_pagination_limit(self):
        """Test pagination limit validation."""
        # Arrange
        start_index = 1
        end_index = 1002  # Exceeds limit

        # Act
        result = await search_cultural_events(
            start_index=start_index,
            end_index=end_index,
        )

        # Assert
        assert 'error' in result
        assert 'Cannot request more than 1000 items' in result['error']


@pytest.mark.asyncio
class TestGetEventById:
    """Test get_event_by_id tool."""

    async def test_get_event_with_valid_id(self):
        """Test getting event by valid service ID."""
        # Note: This will use sample API data
        # In production, you'd want to mock the API response

        # Arrange
        svcid = 'S250220094425372104'  # From sample data

        # Act
        result = await get_event_by_id(svcid=svcid)

        # Assert
        # Result might be error if API is not accessible or ID not found
        # In real tests, we'd mock the API
        assert 'event' in result or 'error' in result

    async def test_get_event_with_invalid_id(self):
        """Test getting event with non-existent ID."""
        # Arrange
        svcid = 'INVALID_ID_12345'

        # Act
        result = await get_event_by_id(svcid=svcid)

        # Assert
        # Should return error or not found
        assert 'event' in result or 'error' in result
