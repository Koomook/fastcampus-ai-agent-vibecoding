"""Test server tools and functionality."""

import pytest

from data_seoul_mcp.{{cookiecutter.project_domain | lower | replace(' ', '_') | replace('-', '_')}}_mcp_server.server import (
    example_tool,
    search_events,
)


@pytest.mark.asyncio
async def test_example_tool(sample_query):
    """Test the example tool."""
    # Arrange
    expected_project_name = 'Data Seoul MCP {{cookiecutter.project_domain}} Server'
    expected_response = f'Hello from {expected_project_name}! Your query was {sample_query}'

    # Act
    result = await example_tool(sample_query)

    # Assert
    assert result == expected_response
    assert isinstance(result, str)
    assert sample_query in result


@pytest.mark.asyncio
class TestSearchEvents:
    """Test search_events tool."""

    async def test_search_with_keyword(self):
        """Test searching events with keyword."""
        # Arrange
        keyword = 'concert'

        # Act
        result = await search_events(keyword=keyword)

        # Assert
        assert result['status'] == 'success'
        assert result['params']['keyword'] == keyword
        assert 'results' in result

    async def test_search_with_date_range(self):
        """Test searching events with date range."""
        # Arrange
        start_date = '20250101'
        end_date = '20250131'

        # Act
        result = await search_events(start_date=start_date, end_date=end_date)

        # Assert
        assert result['status'] == 'success'
        assert result['params']['start_date'] == start_date
        assert result['params']['end_date'] == end_date

    async def test_search_with_limit(self):
        """Test searching events with custom limit."""
        # Arrange
        limit = 5

        # Act
        result = await search_events(limit=limit)

        # Assert
        assert result['status'] == 'success'
        assert result['params']['limit'] == limit

    async def test_search_with_all_params(self):
        """Test searching events with all parameters."""
        # Arrange
        keyword = 'music'
        start_date = '20250101'
        end_date = '20250131'
        limit = 20

        # Act
        result = await search_events(
            keyword=keyword, start_date=start_date, end_date=end_date, limit=limit
        )

        # Assert
        assert result['status'] == 'success'
        assert result['params']['keyword'] == keyword
        assert result['params']['start_date'] == start_date
        assert result['params']['end_date'] == end_date
        assert result['params']['limit'] == limit
