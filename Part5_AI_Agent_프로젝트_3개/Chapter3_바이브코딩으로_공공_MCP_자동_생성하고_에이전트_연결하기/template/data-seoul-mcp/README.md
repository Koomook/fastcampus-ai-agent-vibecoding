# Data Seoul MCP - Cookiecutter Template

Cookiecutter template for creating Seoul Open Data MCP servers.

## Usage

Generate a new MCP server for Seoul Open Data:

```bash
uvx cookiecutter template/data-seoul-mcp
```

You will be prompted for:
- **author_name**: Your name
- **author_email**: Your email (use GitHub noreply format)
- **api_name**: English name of the Seoul API (e.g., "Seoul Cultural Events")
- **api_name_korean**: Korean name of the API (e.g., "문화행사정보")
- **api_description**: Brief description of the API
- **project_domain**: Short domain name (e.g., "CulturalEvents")
- **description**: Full package description
- **instructions**: Instructions for LLM on how to use the server

## Example

```bash
uvx cookiecutter template/data-seoul-mcp

# Prompts:
author_name [Your Name]: Hong Gildong
author_email [githubusername@users.noreply.github.com]: gildong@users.noreply.github.com
api_name [Seoul Cultural Events]: Seoul Cultural Events
api_name_korean [문화행사정보]: 문화행사정보
api_description [Seoul city cultural events and space information]: Seoul city cultural events and space information
project_domain [CulturalEvents]: CulturalEvents
description [A Seoul Data MCP server for 문화행사정보 (Seoul Cultural Events)]:
instructions [Use this MCP server to search...]:
```

This will generate:

```
culturaleveents-mcp-server/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── .python-version
├── data_seoul_mcp/
│   ├── __init__.py
│   └── culturaleveents_mcp_server/
│       ├── __init__.py
│       └── server.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_init.py
    ├── test_main.py
    └── test_server.py
```

## After Generation

1. Navigate to the generated directory:
   ```bash
   cd <project-domain>-mcp-server
   ```

2. Install dependencies:
   ```bash
   uv sync --all-groups
   ```

3. Run tests:
   ```bash
   uv run pytest --cov
   ```

4. Test with MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory . run data_seoul_mcp/<module>/server.py
   ```

5. Implement your Seoul Open Data API integration in `server.py`

## Template Features

- ✅ FastMCP-based server structure
- ✅ Pydantic for configuration management
- ✅ Comprehensive test suite
- ✅ Ruff for linting and formatting
- ✅ Pyright for type checking
- ✅ GitHub-compatible naming conventions
- ✅ Apache 2.0 license
- ✅ Changelog management

## Naming Conventions

The template follows AWS Labs MCP naming patterns:

- **Package name**: `data-seoul-mcp.<domain>-mcp-server`
- **Module name**: `data_seoul_mcp.<domain>_mcp_server`
- **Script name**: `data-seoul-mcp.<domain>-mcp-server`

Examples:
- Input: `CulturalEvents`
- Package: `data-seoul-mcp.culturalevents-mcp-server`
- Module: `data_seoul_mcp.culturalevents_mcp_server`

## License

Apache-2.0
