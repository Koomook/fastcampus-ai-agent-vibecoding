# Seoul Women Family Foundation Events MCP Server

A Seoul Data MCP server for **서울시 여성가족재단 행사정보** (Seoul Women's Family Foundation Events)

## Overview

This MCP server provides tools to access the Seoul Open Data API for Seoul Women's Family Foundation events, including educational programs, seminars, forums, cultural events, and community activities.

### Features

- 🔍 **Search Events**: Search events by keyword and event type
- 📋 **Event Details**: Get detailed information for specific events by registration number
- 📊 **Event Types**: List all available event types in the system
- 🔐 **API Integration**: Seamless integration with Seoul Open Data API
- ✅ **High Coverage**: 79% test coverage with comprehensive test suite

## Installation

### Using uvx (Recommended)

```bash
uvx data-seoul-mcp.womenfamilyfoundation-mcp-server@latest
```

### Using uv pip

```bash
uv pip install data-seoul-mcp.womenfamilyfoundation-mcp-server
```

## Configuration

### Option 1: Using Published Package (uvx)

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "seoul-womenfamilyfoundation": {
      "command": "uvx",
      "args": ["data-seoul-mcp.womenfamilyfoundation-mcp-server@latest"],
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
    "seoul-womenfamilyfoundation": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/womenfamilyfoundation-mcp-server",
        "run",
        "data_seoul_mcp/womenfamilyfoundation_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "your-api-key-here",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/womenfamilyfoundation-mcp-server` with the actual absolute path to your project directory.

**Example:**
```json
{
  "mcpServers": {
    "seoul-womenfamilyfoundation": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/projects/womenfamilyfoundation-mcp-server",
        "run",
        "data_seoul_mcp/womenfamilyfoundation_mcp_server/server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "12345678-abcd-efgh-ijkl-1234567890ab",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    }
  }
}
```

## Available Tools

### SearchEvents

Search Seoul Women's Family Foundation events with flexible filtering options.

**Parameters:**
- `keyword` (string, optional): Search keyword to filter by event title
- `event_type` (string, optional): Filter by event type (e.g., 교육, 이벤트, 세미나, 포럼, 공연, 컨설팅)
- `start_index` (integer, default: 1): Start position for pagination
- `end_index` (integer, default: 100): End position for pagination (max: 1000 items per request)

**Returns:**
```json
{
  "status": "success",
  "total_count": 3,
  "events": [
    {
      "evt_reg_no": "30378",
      "title": "[서울형 아이돌봄비] 독감예방접종 시기",
      "evt_type": "기타",
      "evt_date": "2025-10-20~2025-12-31",
      "evt_place": "온라인",
      "evt_target": "서울형 아이돌봄비 이용자 및 조력자",
      "evt_reg_method": "온라인",
      "evt_sponsor": "서울시여성가족재단",
      "evt_contact": "02-810-5158",
      "url": "https://www.seoulwomen.or.kr/..."
    }
  ]
}
```

### GetEventDetails

Get detailed information for a specific event by registration number.

**Parameters:**
- `evt_reg_no` (string, required): Event registration number (행사번호)

**Returns:**
```json
{
  "status": "success",
  "event": {
    "evt_reg_no": "30378",
    "title": "[서울형 아이돌봄비] 독감예방접종 시기",
    "evt_reg_start_date": "2025-10-20",
    "evt_reg_end_date": "2025-12-31",
    ...
  }
}
```

### ListEventTypes

Get a list of all available event types in the system.

**Returns:**
```json
{
  "status": "success",
  "event_types": ["교육", "이벤트", "세미나", "포럼", "공연", "컨설팅", "기타"]
}
```

## Usage Examples

### Search for Educational Events

```
Use the SearchEvents tool to find educational programs:
- keyword: "교육"
- event_type: "교육"
```

### Get Details for a Specific Event

```
Use the GetEventDetails tool with:
- evt_reg_no: "30378"
```

### Browse All Event Types

```
Use the ListEventTypes tool to see all available event categories
```

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd womenfamilyfoundation-mcp-server

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
npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/womenfamilyfoundation_mcp_server/server.py
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

This server integrates with the Seoul Open Data API:

- **API Name**: 서울시 여성가족재단 행사정보 (SeoulWomenPlazaEvent)
- **Service Description**: Seoul Women's Family Foundation events, education, and activities information
- **Base URL**: http://openapi.seoul.go.kr:8088
- **Format**: JSON

### Getting an API Key

1. Visit [Seoul Open Data Portal](https://data.seoul.go.kr)
2. Sign up or log in
3. Request an API key for the service
4. Set the key in your environment: `SEOUL_API_KEY=your-api-key`

### API Response Structure

All API responses follow this structure:

```json
{
  "SeoulWomenPlazaEvent": {
    "list_total_count": 3,
    "RESULT": {
      "CODE": "INFO-000",
      "MESSAGE": "정상 처리되었습니다"
    },
    "row": [...]
  }
}
```

### Event Data Fields

| Field | Korean | Description |
|-------|--------|-------------|
| evt_reg_no | 행사번호(키) | Event registration number (unique key) |
| title | 제목 | Event title |
| evt_reg_start_date | 행사신청시작일 | Registration start date |
| evt_reg_end_date | 행사신청종료일 | Registration end date |
| evt_type | 행사종류 | Event type |
| evt_date | 행사일시 | Event date and time |
| evt_place | 행사장소 | Event location/venue |
| evt_target | 참여대상 | Target participants |
| evt_reg_method | 신청방법 | Registration method |
| evt_sponsor | 주최/주관 | Host/Organizer |
| evt_contact | 행사문의 | Contact information |
| url | 상세정보 주소 | Detailed information URL |

## License

Apache-2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Dave Goobong Jeong (bongbonggg97@gmail.com)
