# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server implementation for the Korea National Pension Service Business Enrollment API. It provides three main tools for querying business enrollment data from the Korean public data portal.

## File Structure

```
mcp_NPS_BusinessEnrollment/
├── src/mcp_nps_business_enrollment/
│   ├── __init__.py           # Package initialization
│   ├── server.py             # MCP server with three tools (search, detail, period_status)
│   ├── api_client.py         # HTTP client for Korean government API
│   └── models.py             # Pydantic models for data validation
├── tests/
│   └── test_api.py           # API integration tests
├── pyproject.toml            # UV project configuration & dependencies
├── setup.py                  # Legacy setup file for backwards compatibility
├── README.md                 # User-facing documentation (Korean)
└── CLAUDE.md                 # This file - development guidance
```

## Package Management with UV

This project uses **UV** for package management, NOT pip directly. All dependency operations should use UV commands:

```bash
# Install dependencies
uv sync

# Add new dependencies
uv add <package>

# Add dev dependencies
uv add --dev <package>

# Run commands within UV environment
uv run <command>

# Build the package
uv run python -m build

# Upload to PyPI
uv run twine upload dist/*
```

## Common Development Commands

### Testing
```bash
# Run tests (note: may fail due to SSL issues with Korean government API)
uv run python tests/test_api.py

# Run with pytest
uv run pytest tests/
```

### MCP Server Development
```bash
# Run MCP server in dev mode
uv run mcp dev src/mcp_nps_business_enrollment/server.py

# Install to Claude Desktop
uv run mcp install src/mcp_nps_business_enrollment/server.py

# Run the installed server command
uv run mcp-nps-server
```

### PyPI Publishing
```bash
# Build package
uv run python -m build

# Check package
uv run twine check dist/*

# Upload to PyPI (requires API token)
uv run twine upload dist/* -u __token__ -p <pypi-token>
```

## Architecture

### Core Components

1. **MCP Server (`server.py`)**: Implements three tools using FastMCP framework
   - `search_business`: Search businesses by various criteria
   - `get_business_detail`: Get detailed info for a specific business
   - `get_period_status`: Get monthly acquisition/loss statistics

2. **API Client (`api_client.py`)**: Handles communication with Korean government API
   - Manages SSL/TLS issues (Korean government API uses HTTP)
   - Converts between snake_case and camelCase parameters
   - Requires API key to be set via environment variable

3. **Data Models (`models.py`)**: Pydantic models for request/response validation
   - Uses field aliases for camelCase conversion
   - Handles optional fields gracefully

### Key Implementation Details

- **HTTP vs HTTPS**: The Korean government API only supports HTTP, not HTTPS. The API client is configured with `verify=False` to handle this.
- **API Key Handling**: The client requires environment variable `API_KEY` to be set (mandatory).
- **Parameter Naming**: The API uses camelCase, but the Python code uses snake_case. The client automatically converts between them.
- **Salary Calculation**: The server calculates estimated average monthly salary using: `당월고지금액 ÷ 가입자수 ÷ 0.09 (보험료율)`

## Known Issues and Workarounds

### SSL/TLS Connection Errors
The Korean government API has SSL certificate issues. The current workaround:
- API endpoint uses HTTP instead of HTTPS
- httpx client configured with `verify=False`
- This is not ideal but necessary for the API to work

### Testing Challenges
- Direct API tests may fail due to SSL issues
- Consider mocking API responses for unit tests
- Integration tests require valid API keys in `.env`

### API Limitations
- **Max results per request**: 100 items (API returns CLIENT_ERROR if > 100)
- **Time-series data**: Each month has different `seq` for same business - cannot track historical data easily
- **Business registration number**: Only first 6 digits provided (last 4 masked)
- **Data freshness**: Updated monthly around 15th of each month
- **Large corporations**: May not appear in search (divided by regional offices)

## MCP Protocol Understanding

To understand and extend this MCP server implementation:

1. **MCP Python SDK Documentation**: https://github.com/modelcontextprotocol/python-sdk
   - FastMCP framework for simplified server creation
   - Tool decorators for exposing functions
   - Async/await patterns for I/O operations

2. **MCP Protocol Specification**: https://modelcontextprotocol.io/docs/getting-started/intro
   - Understanding tools vs resources vs prompts
   - Client-server communication patterns
   - Integration with Claude Desktop/Code

## Environment Configuration

Required environment variables in `.env`:
```
# API Key (required)
API_KEY="<your-api-key>"
```

## Version Control Best Practices

**IMPORTANT: Commit changes to git after every significant modification**
- Make atomic commits for each logical change
- Write clear, descriptive commit messages
- Commit before moving to the next feature or fix
- Never leave uncommitted changes when switching tasks

## Publishing Updates

The package is published on PyPI: https://pypi.org/project/mcp-nps-business-enrollment/

To publish updates:
1. Update version in `pyproject.toml`
2. Build with `uv run python -m build`
3. Upload with `uv run twine upload dist/*`
4. Tag release in git: `git tag v0.1.x && git push origin v0.1.x`
- 기능 추가가 있을 때 git commit