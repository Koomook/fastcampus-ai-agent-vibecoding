# Seoul Cultural Events MCP Server

MCP (Model Context Protocol) server providing access to Seoul's cultural events through the Seoul Open Data Plaza API.

## Overview

This MCP server enables LLMs (like Claude) to search and retrieve information about cultural events in Seoul, Korea. It wraps the Seoul Open Data Plaza's cultural events API into a simple, easy-to-use MCP interface.

## Features

- 🔍 Search cultural events by category, date, or title
- 🎭 Support for multiple event types (Exhibition, Concert, Theater, Classical)
- 📍 Access to Seoul's 25 district information
- 🚀 Built with FastMCP for simple, fast development
- 🔄 Asynchronous API calls using httpx

## Tech Stack

- **Language**: Python 3.11+
- **Framework**: FastMCP 2.0
- **Package Manager**: uv
- **Communication**: STDIO
- **HTTP Client**: httpx (async)

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd seoul-culture-mcp

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env
```

### 2. Get API Key

1. Visit [Seoul Open Data Plaza](https://data.seoul.go.kr/)
2. Register and login
3. Request API key from your profile page
4. Add key to `.env`:
   ```
   SEOUL_API_KEY=your_api_key_here
   ```

### 3. Test Locally

```bash
uv run python run_server.py
```

Expected output:
```
╭────────────────────────────────────────────────╮
│        Seoul Cultural Events                   │
│        FastMCP 2.0                            │
╰────────────────────────────────────────────────╯
```

Press Ctrl+C to exit.

### 4. Connect to Claude Desktop

See [CLAUDE.md](./CLAUDE.md) for detailed setup instructions.

## Project Structure

```
seoul-culture-mcp/
├── run_server.py           # Entry point with path setup
├── pyproject.toml          # uv configuration
├── .env.example            # Environment template
├── src/seoul_culture_mcp/
│   ├── server.py           # MCP server (1 tool, 3 resources)
│   ├── api_client.py       # Seoul API client
│   └── models.py           # Pydantic models
└── tests/
    └── test_server.py      # Tests
```

## MCP Interface

### Tool: `search_cultural_events`

Search Seoul cultural events with flexible filters.

**Parameters**:
- `start_index` (int): Start position (default: 1)
- `end_index` (int): End position (default: 100, max: 1000)
- `codename` (str): Event category
- `title` (str): Search keyword
- `date` (str): Date in YYYY-MM-DD format

**Example Queries**:
```
"Find exhibitions this weekend"
"Search concerts in December"
"Show me Ghibli events"
```

### Resources

- **`seoul://culture/api-info`**: API metadata
- **`seoul://culture/categories`**: Available event categories
- **`seoul://culture/districts`**: Seoul's 25 districts

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## API Limitations

- Max 1000 results per request
- Sample key limited to 5 results
- Data updated daily

## Documentation

- [CLAUDE.md](./CLAUDE.md) - Setup guide, development commands, troubleshooting
- [.env.example](./.env.example) - Environment configuration template

## References

- [FastMCP](https://gofastmcp.com/) - Framework documentation
- [Seoul Open Data Plaza](https://data.seoul.go.kr/) - API source
- [MCP Specification](https://modelcontextprotocol.io/) - Protocol details

## License

MIT License
