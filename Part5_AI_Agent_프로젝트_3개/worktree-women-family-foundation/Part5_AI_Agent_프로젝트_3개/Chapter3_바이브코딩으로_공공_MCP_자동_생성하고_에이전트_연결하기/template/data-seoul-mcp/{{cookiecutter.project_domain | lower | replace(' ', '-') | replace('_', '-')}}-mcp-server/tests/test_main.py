"""Test main entry point."""

from data_seoul_mcp.{{cookiecutter.project_domain | lower | replace(' ', '_') | replace('-', '_')}}_mcp_server.server import (
    APP_NAME,
    mcp,
)


def test_app_name():
    """Test that APP_NAME is correctly set."""
    expected_name = 'data-seoul-mcp.{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server'
    assert APP_NAME == expected_name


def test_mcp_instance():
    """Test that mcp instance is created."""
    assert mcp is not None
    assert mcp.name == APP_NAME
