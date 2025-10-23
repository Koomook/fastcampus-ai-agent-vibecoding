"""Pytest configuration and fixtures for {{cookiecutter.api_name}} MCP Server."""

import pytest


@pytest.fixture
def sample_query():
    """Sample query fixture for testing."""
    return 'test query'


@pytest.fixture
def sample_event_data():
    """Sample event data fixture for testing."""
    return {
        'title': 'Sample Cultural Event',
        'start_date': '20250101',
        'end_date': '20250131',
        'location': 'Seoul Cultural Center',
        'genre': 'Music',
    }
