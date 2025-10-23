# Seoul Cultural Events Reservation MCP Server

A Seoul Data MCP server for 문화행사 공공서비스예약 (Seoul Cultural Events Reservation)

## TODO (REMOVE AFTER COMPLETING)

* [ ] Generate a `uv.lock` file with `uv sync`
* [ ] Remove the example tools in server.py
* [ ] Add your own tool(s) for Seoul Open Data API integration
* [ ] Implement API authentication and configuration
* [ ] Keep test coverage high
* [ ] Document the MCP Server in this README.md
* [ ] Test with MCP Inspector
* [ ] Test with Claude Code or other MCP clients

## Overview

This MCP server provides tools to access Seoul Open Data API for **문화행사 공공서비스예약** (Seoul Cultural Events Reservation).

### Features

- 🔍 Search cultural events by keyword and date range
- 📅 Filter events by genre and location
- 🚇 Access transportation information for cultural spaces
- 🏛️ Browse cultural space information

## Installation

### Using uvx (Recommended)

```bash
uvx data-seoul-mcp.culturalreservation-mcp-server@latest
```

### Using uv pip

```bash
uv pip install data-seoul-mcp.culturalreservation-mcp-server
```

## Configuration

### Option 1: Using Published Package (uvx)

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "seoul-culturalreservation": {
      "command": "uvx",
      "args": ["data-seoul-mcp.culturalreservation-mcp-server@latest"],
      "env": {
        "SEOUL_API_KEY": "your-api-key-here",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

### Option 2: Using Local Development Version

For local development and testing, add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "seoul-culturalreservation": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/culturalreservation-mcp-server",
        "run",
        "data_seoul_mcp/culturalreservation_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "your-api-key-here",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/culturalreservation-mcp-server` with the actual absolute path to your project directory.

**Example:**
```json
{
  "mcpServers": {
    "seoul-culturalreservation": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/projects/culturalreservation-mcp-server",
        "run",
        "data_seoul_mcp/culturalreservation_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "12345678-abcd-efgh-ijkl-1234567890ab",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Tools

### ExampleTool

Example tool for testing the server setup.

**Parameters:**
- `query` (string): Test query string

### SearchEvents

Search Seoul cultural events.

**Parameters:**
- `keyword` (string, optional): Search keyword for event title or description
- `start_date` (string, optional): Start date in YYYYMMDD format
- `end_date` (string, optional): End date in YYYYMMDD format
- `limit` (integer, default: 10): Maximum number of results

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd culturalreservation-mcp-server

# Install dependencies
uv sync --all-groups

# Install pre-commit hooks (if using)
pre-commit install
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov --cov-report=term-missing

# Run type checking
uv run pyright
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/culturalreservation_mcp_server/server.py
```

Then open http://127.0.0.1:6274 in your browser.

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Run all pre-commit hooks
pre-commit run --all-files
```

## API Integration

This server is designed to integrate with Seoul Open Data API:

- API Name: 문화행사 공공서비스예약
- Description: Seoul city cultural events and public service reservation information

### TODO: Add API Configuration

1. Obtain API key from Seoul Open Data Portal
2. Add environment variable configuration
3. Implement API client
4. Add error handling for API responses

## License

Apache-2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

FastCampus Lecture (lecture@fastcampus.com)
