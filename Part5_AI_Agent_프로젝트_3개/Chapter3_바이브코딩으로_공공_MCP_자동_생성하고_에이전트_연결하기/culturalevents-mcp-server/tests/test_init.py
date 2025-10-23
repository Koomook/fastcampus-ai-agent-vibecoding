"""Test module initialization."""

import data_seoul_mcp.culturalevents_mcp_server as module


def test_module_has_version():
    """Test that the module has a version attribute."""
    assert hasattr(module, '__version__')
    assert isinstance(module.__version__, str)
    assert module.__version__ == '0.0.0'
