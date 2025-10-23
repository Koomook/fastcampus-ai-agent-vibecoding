"""{{cookiecutter.api_name}} MCP Server.

This server provides tools to access Seoul Open Data API for {{cookiecutter.api_name_korean}}.
"""

from typing import Any

from loguru import logger
from mcp.server.fastmcp import FastMCP

APP_NAME = 'data-seoul-mcp.{{cookiecutter.project_domain | lower | replace(' ', '-') | replace('_', '-')}}-mcp-server'

mcp = FastMCP(
    APP_NAME,
    instructions="{{cookiecutter.instructions}}",
)


@mcp.tool(name='ExampleTool')
async def example_tool(query: str) -> str:
    """Example tool implementation for {{cookiecutter.api_name}}.

    This is a placeholder tool. Replace this with actual API integration.

    Args:
        query: The search query string

    Returns:
        A greeting message with the query
    """
    project_name = 'Data Seoul MCP {{cookiecutter.project_domain}} Server'
    return f'Hello from {project_name}! Your query was {query}'


@mcp.tool(name='SearchEvents')
async def search_events(
    keyword: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """Search Seoul cultural events by keyword and date range.

    TODO: Implement actual API integration with Seoul Open Data API.

    Args:
        keyword: Search keyword for event title or description
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        limit: Maximum number of results to return

    Returns:
        Dictionary containing search results with event information
    """
    # Placeholder implementation
    return {
        'status': 'success',
        'message': 'TODO: Implement Seoul Open Data API integration',
        'params': {
            'keyword': keyword,
            'start_date': start_date,
            'end_date': end_date,
            'limit': limit,
        },
        'results': [],
    }


def main() -> None:
    """Run the MCP server with CLI argument support."""
    logger.trace('A trace message.')
    logger.debug('A debug message.')
    logger.info('An info message.')
    logger.success('A success message.')
    logger.warning('A warning message.')
    logger.error('An error message.')
    logger.critical('A critical message.')

    mcp.run()


if __name__ == '__main__':
    main()
