# Claude Developer Guide

This document provides essential information for developing and troubleshooting the Seoul Cultural Events MCP Server.

## Project Overview

**Purpose**: Enable Claude to search Seoul's cultural events through MCP (Model Context Protocol)

**Architecture**:
- FastMCP 2.0 server running via STDIO
- Single API endpoint wrapper (`search_cultural_events`)
- 3 resource endpoints for metadata
- Async HTTP client for API calls

## Project Structure

```
seoul-culture-mcp/
├── run_server.py                # Entry point with path setup
├── pyproject.toml               # uv dependencies
├── .env.example                 # Environment template
└── src/seoul_culture_mcp/
    ├── server.py                # MCP server (1 tool, 3 resources)
    ├── api_client.py            # Seoul API client
    └── models.py                # Pydantic models
```

### Key Files

**`run_server.py`** - Critical entry point that:
- Adds `src/` to Python path (`sys.path.insert(0, src_path)`)
- Loads `.env` environment variables
- Handles module import issues
- Starts MCP server

**Why `run_server.py` is necessary**:
- Claude Desktop doesn't always respect `cwd` settings
- Python needs explicit path setup to find `seoul_culture_mcp` module
- Provides consistent entry point across environments

## Development Commands

### Local Testing

```bash
# Test server startup
uv run python run_server.py

# Expected output:
# ╭────────────────────────────────────────────────╮
# │        Seoul Cultural Events                   │
# │        FastMCP 2.0                            │
# ╰────────────────────────────────────────────────╯

# Test with directory flag (simulates Claude Desktop)
uv --directory /path/to/project run python run_server.py

# Run tests
uv run pytest

# Code formatting
uv run ruff format .

# Linting
uv run ruff check .
```

### Environment Setup

```bash
# Install dependencies
uv sync

# Create environment file
cp .env.example .env

# Edit .env and add your API key
# SEOUL_API_KEY=your_key_here
```

## Claude Desktop Setup

### Configuration File Location

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Working Configuration

```json
{
  "mcpServers": {
    "seoul-culture": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/seoul-culture-mcp",
        "run",
        "python",
        "run_server.py"
      ],
      "env": {
        "SEOUL_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Configuration Explained

| Setting | Value | Why | Must Change? |
|---------|-------|-----|--------------|
| `command` | `"uv"` | Use uv package manager | No |
| `args[0-1]` | `"--directory", "/path"` | Specify project directory | **Yes** |
| `args[2-4]` | `"run", "python", "run_server.py"` | Execute entry script | No |
| `env.SEOUL_API_KEY` | API key | Seoul API authentication | **Yes** |

**Critical**:
- Use **absolute path** for `--directory`
- Use `--directory` flag (not `cwd` field)
- Path can contain Korean characters or spaces

### Verification Steps

1. **Local test**:
   ```bash
   uv run python run_server.py
   ```
   Should show FastMCP banner without errors.

2. **Restart Claude Desktop**:
   - Quit completely (Cmd+Q on macOS)
   - Restart application
   - Start new conversation

3. **Test in Claude**:
   ```
   Can you search Seoul cultural events?
   ```
   Claude should recognize the `search_cultural_events` tool.

4. **Check logs** (if issues):
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

## Troubleshooting

### Problem: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'seoul_culture_mcp'
```

**Causes**:
- `run_server.py` not being used
- Incorrect project path in configuration
- Missing dependencies

**Solutions**:

1. Verify `run_server.py` exists in project root
2. Check Claude Desktop config uses correct absolute path
3. Install dependencies:
   ```bash
   cd /path/to/project
   uv sync
   ```
4. Test locally:
   ```bash
   uv run python run_server.py
   ```

### Problem: Server Transport Closed

```
Server transport closed unexpectedly
```

**Causes**:
- Server crashes during startup
- API key missing or invalid
- Python or dependency errors

**Solutions**:

1. **Test locally** to see actual error:
   ```bash
   uv run python run_server.py
   ```

2. **Check API key**:
   - Verify key in Claude Desktop config
   - Or verify `.env` file has `SEOUL_API_KEY`

3. **Check logs**:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

4. **Verify dependencies**:
   ```bash
   uv sync
   ```

### Problem: Tool Not Recognized

Claude doesn't see the `search_cultural_events` tool.

**Solutions**:

1. **Restart Claude Desktop** properly:
   - Fully quit (Cmd+Q)
   - Wait 2-3 seconds
   - Reopen

2. **Check config syntax**:
   - Valid JSON (no trailing commas)
   - Correct quotes (double quotes)
   - Proper nesting

3. **Verify in logs**:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```
   Look for:
   - ✅ "Server started and connected successfully"
   - ✅ "Server name: Seoul Cultural Events"

## API Information

### Endpoint

```
http://openapi.seoul.go.kr:8088/{KEY}/{TYPE}/culturalEventInfo/{START}/{END}/{CODENAME}/{TITLE}/{DATE}
```

### Parameters

- **Required**: KEY, TYPE, START, END
- **Optional** (URL path): CODENAME, TITLE, DATE
- **Note**: Optional params are URL path segments, not query strings

### Getting API Key

1. Visit [Seoul Open Data Plaza](https://data.seoul.go.kr/)
2. Register account and login
3. Go to My Page → Request API Key
4. Use key in config or `.env`

### Limitations

- Max 1000 results per request
- Sample key: max 5 results
- Daily data updates
- API key required for production use

## Implementation Notes

### Why `--directory` Instead of `cwd`?

The `cwd` field in Claude Desktop config doesn't work reliably:
- May be ignored in some environments
- uv might not find the correct project
- `--directory` explicitly tells uv where to run

### Why `run_server.py` Instead of `-m`?

Direct module execution (`python -m seoul_culture_mcp.server`) requires:
- Current directory to be project root
- `src/` to be in PYTHONPATH
- Neither is guaranteed in Claude Desktop

`run_server.py` explicitly sets up the environment before importing.

### Path Setup Logic

```python
# In run_server.py
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)  # Highest priority
```

This ensures Python can find `seoul_culture_mcp` regardless of:
- Where Claude Desktop runs the command
- What the current working directory is
- What PYTHONPATH contains

## Deployment to Other Machines

1. **Clone repository**:
   ```bash
   git clone <repo-url>
   cd seoul-culture-mcp
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Setup environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

4. **Test locally**:
   ```bash
   uv run python run_server.py
   ```

5. **Configure Claude Desktop**:
   - Update `--directory` path to new machine's path
   - Update `SEOUL_API_KEY` if needed

## Extension Patterns

This project's pattern (`run_server.py` + `--directory`) works for any FastMCP project:

```python
#!/usr/bin/env python3
"""Generic MCP Server Entry Point"""
import sys, os

def setup_python_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, src_path)
    return project_root

def main():
    project_root = setup_python_path()

    # Load environment (optional)
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(project_root, '.env'))
    except: pass

    # Import and run server
    from your_package.server import mcp
    mcp.run()

if __name__ == "__main__":
    main()
```

Claude Desktop config:
```json
{
  "command": "uv",
  "args": [
    "--directory", "/absolute/path",
    "run", "python", "run_server.py"
  ]
}
```

## Resources

- [FastMCP Docs](https://gofastmcp.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Seoul Open Data](https://data.seoul.go.kr/)
- [uv Documentation](https://github.com/astral-sh/uv)
