# Seoul Cultural Events MCP Server

A Model Context Protocol (MCP) server that provides access to Seoul's cultural events data through the Seoul Open Data API.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

This MCP server enables AI assistants like Claude to search and retrieve real-time information about cultural events in Seoul, including:

- 🎭 Performances (concerts, theater, musicals)
- 🎨 Exhibitions and art events
- 🎪 Cultural festivals
- 📍 Event locations and venues
- 💰 Ticket prices and booking information
- 📅 Event schedules and dates

**Data Source:** Seoul Open Data Portal - 서울시 문화행사 정보 (culturalEventInfo)
**Update Frequency:** Daily

## Features

- ✅ **23 Data Fields**: Comprehensive event information including title, venue, dates, fees, performers, and more
- ✅ **Flexible Filtering**: Search by category, title, or date
- ✅ **Pagination Support**: Handle large result sets efficiently (up to 1000 records per request)
- ✅ **Error Handling**: Graceful handling of API errors and validation
- ✅ **Type Safety**: Full Pydantic models for data validation
- ✅ **Async Support**: Built with async/await for optimal performance

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Seoul Open Data API key (free registration)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd culturalevents-mcp-server
   ```

2. **Install dependencies**
   ```bash
   uv sync --all-groups
   ```

3. **Get Seoul Open Data API Key**
   - Visit [Seoul Open Data Portal](https://data.seoul.go.kr)
   - Sign up for a free account
   - Navigate to 인증키 신청 (API Key Application)
   - Copy your API key

4. **Set up environment variable**
   ```bash
   export SEOUL_API_KEY="your-api-key-here"
   ```

## Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "seoul-culturalevents": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/culturalevents-mcp-server",
        "run",
        "data_seoul_mcp/culturalevents_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "your-seoul-api-key-here"
      }
    }
  }
}
```

**Important:**
- Replace `/absolute/path/to/culturalevents-mcp-server` with the actual absolute path
- Replace `your-seoul-api-key-here` with your API key
- Restart Claude Desktop after saving

### Other MCP Clients

For other MCP-compatible clients, use:

```json
{
  "mcpServers": {
    "seoul-culturalevents": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/culturalevents-mcp-server",
        "run",
        "data_seoul_mcp/culturalevents_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Available Tools

### SearchCulturalEvents

Search and filter Seoul cultural events.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `codename` | string | No | Event category filter (e.g., "콘서트", "전시/미술", "연극") |
| `title` | string | No | Event title search (partial match supported) |
| `date` | string | No | Date filter in YYYY-MM-DD format |
| `start_index` | integer | No | Pagination start (default: 1, min: 1) |
| `end_index` | integer | No | Pagination end (default: 100, max: 1000 records per request) |

**Response Fields:**

The tool returns comprehensive event information with 23 fields:

- `codename`: Category (콘서트, 전시/미술, 연극, etc.)
- `title`: Event/Performance name
- `date`: Event date/time range
- `place`: Venue location
- `guname`: District (자치구)
- `org_name`: Organizing institution
- `use_trgt`: Target audience
- `use_fee`: Ticket price
- `is_free`: Free/Paid status
- `player`: Performer information
- `program`: Program description
- `main_img`: Event poster image URL
- `org_link`: Official website
- `hmpg_addr`: Seoul Culture Portal detail URL
- `strtdate`: Start date (timestamp)
- `end_date`: End date (timestamp)
- `rgstdate`: Registration date
- `ticket`: Citizen/Institution
- `themecode`: Theme category
- `lat`: Latitude (X coordinate)
- `lot`: Longitude (Y coordinate)
- `etc_desc`: Additional information

**Example Usage:**

```javascript
// Search for all concerts
{
  "codename": "콘서트",
  "start_index": 1,
  "end_index": 10
}

// Search by title
{
  "title": "재즈",
  "start_index": 1,
  "end_index": 50
}

// Search by date
{
  "date": "2025-12-13",
  "start_index": 1,
  "end_index": 20
}

// Combined filters
{
  "codename": "전시/미술",
  "title": "현대미술",
  "date": "2025-11-01",
  "start_index": 1,
  "end_index": 100
}
```

**Example Response:**

```json
{
  "status": "success",
  "total_count": 156,
  "count": 10,
  "events": [
    {
      "codename": "콘서트",
      "title": "2025 카즈미 타테이시 트리오 내한공연 [지브리, 재즈를 만나다-서울]",
      "date": "2025-12-13~2025-12-13",
      "place": "용산아트홀 대극장 미르",
      "guname": "용산구",
      "use_fee": "VIP석 77,000원 R석 66,000원 A석 55,000원",
      "is_free": "유료",
      "org_link": "https://tickets.interpark.com/goods/25009778",
      "lat": "37.5324522944579",
      "lot": "126.990478820837"
    }
  ]
}
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_server.py

# Run with verbose output
uv run pytest -v
```

**Current Test Coverage:** 56% (11 tests passing)

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Auto-fix lint issues
uv run ruff check --fix .

# Type checking
uv run pyright
```

### Testing with MCP Inspector

The MCP Inspector provides a web interface to test your MCP server:

```bash
npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/culturalevents_mcp_server/server.py
```

Then open http://127.0.0.1:6274 in your browser to:
- View available tools
- Test tool calls with different parameters
- Inspect request/response payloads
- Debug server behavior

## API Details

**Endpoint:** `http://openapi.seoul.go.kr:8088/{API_KEY}/json/culturalEventInfo/{START}/{END}/{CODENAME?}/{TITLE?}/{DATE?}/`

**Rate Limits:**
- Maximum 1000 records per request
- Daily update frequency
- No explicit rate limiting (be respectful)

**Error Codes:**
- `INFO-000`: Success
- `ERROR-300`: Missing required parameters
- `INFO-100`: Invalid API key
- `ERROR-310`: Service not found
- `ERROR-331-336`: Pagination errors
- `ERROR-500`: Server error
- `ERROR-600-601`: Database errors
- `INFO-200`: No data found

## Project Structure

```
culturalevents-mcp-server/
├── data_seoul_mcp/
│   └── culturalevents_mcp_server/
│       ├── __init__.py
│       └── server.py              # Main MCP server implementation
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_init.py
│   ├── test_main.py
│   └── test_server.py             # Tool and API tests
├── pyproject.toml                 # Project configuration
├── uv.lock                        # Locked dependencies
├── README.md                      # This file
├── CHANGELOG.md                   # Version history
└── LICENSE                        # Apache 2.0 license
```

## Troubleshooting

### Server won't start

1. **Check the directory path** in your MCP client configuration
   ```bash
   # Verify you're using the absolute path
   pwd  # Should show: .../culturalevents-mcp-server
   ```

2. **Verify dependencies are installed**
   ```bash
   uv sync --all-groups
   ```

3. **Check Python version**
   ```bash
   python --version  # Should be 3.10+
   ```

### API Key Issues

1. **Verify API key is set**
   ```bash
   echo $SEOUL_API_KEY
   ```

2. **Test API key directly**
   ```bash
   curl "http://openapi.seoul.go.kr:8088/YOUR_API_KEY/json/culturalEventInfo/1/5/"
   ```

3. **Check for common errors:**
   - Key not activated (wait 5-10 minutes after registration)
   - Key contains extra spaces or quotes
   - Key has been revoked or expired

### No Data Returned

- Check if events exist for your search criteria
- Try broader search parameters
- Verify the API service is running at data.seoul.go.kr

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes using conventional commits
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Guidelines:**
- Follow TDD (Test-Driven Development)
- Maintain test coverage above 80%
- Use conventional commit messages
- Run all quality checks before submitting
- Update documentation for new features

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

This project allows commercial use, modification, distribution, and private use.

## Author

**Seoul Data Team**
Email: team@seoul-data.kr

## Acknowledgments

- Data provided by Seoul Metropolitan Government
- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Model Context Protocol](https://modelcontextprotocol.io)

## Related Links

- [Seoul Open Data Portal](https://data.seoul.go.kr)
- [Seoul Culture Portal](https://culture.seoul.go.kr)
- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
