"""Test main entry point."""

from data_seoul_mcp.womenfamilyfoundation_mcp_server.server import (
    APP_NAME,
    mcp,
)


def test_app_name():
    """Test that APP_NAME is correctly set."""
    expected_name = 'data-seoul-mcp.womenfamilyfoundation-mcp-server'
    assert APP_NAME == expected_name


def test_mcp_instance():
    """Test that mcp instance is created."""
    assert mcp is not None
    assert mcp.name == APP_NAME
