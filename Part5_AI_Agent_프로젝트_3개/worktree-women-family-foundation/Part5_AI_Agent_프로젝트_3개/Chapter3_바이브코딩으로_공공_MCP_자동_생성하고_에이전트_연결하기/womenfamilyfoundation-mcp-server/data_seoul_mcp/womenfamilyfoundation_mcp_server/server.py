"""Seoul Women Family Foundation Events MCP Server.

This server provides tools to access Seoul Open Data API for 서울시 여성가족재단 행사정보.
"""

import os
from typing import Any

import httpx
from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

APP_NAME = 'data-seoul-mcp.womenfamilyfoundation-mcp-server'

# API Configuration
SEOUL_API_KEY = os.getenv('SEOUL_API_KEY', 'sample')
API_BASE_URL = 'http://openapi.seoul.go.kr:8088'
SERVICE_NAME = 'SeoulWomenPlazaEvent'


class WomenFamilyEvent(BaseModel):
    """Seoul Women's Family Foundation Event information model."""

    evt_reg_no: str = Field(
        ..., description='행사번호(키) - Event registration number (unique key)'
    )
    title: str = Field(..., description='제목 - Event title')
    evt_reg_start_date: str = Field(..., description='행사신청시작일 - Registration start date')
    evt_reg_end_date: str = Field(..., description='행사신청종료일 - Registration end date')
    evt_type: str = Field(
        ..., description='행사종류 - Event type (e.g., 교육, 이벤트, 세미나, 포럼, 공연)'
    )
    evt_date: str = Field(..., description='행사일시 - Event date and time')
    evt_place: str = Field(..., description='행사장소 - Event location/venue')
    evt_target: str = Field(..., description='참여대상 - Target participants')
    evt_reg_method: str = Field(..., description='신청방법 - Registration method')
    evt_sponsor: str = Field(..., description='주최/주관 - Host/Organizer')
    evt_contact: str = Field(..., description='행사문의 - Contact information')
    url: str = Field(..., description='상세정보 주소 - Detailed information URL')


class APIResponse(BaseModel):
    """API Response wrapper model."""

    list_total_count: int = Field(0, description='Total number of results')
    result: dict[str, str] = Field(default_factory=dict, description='API result status')
    row: list[dict[str, Any]] = Field(default_factory=list, description='Event data rows')


mcp = FastMCP(
    APP_NAME,
    instructions="Use this MCP server to search and retrieve Seoul Women's Family Foundation events information including educational programs, seminars, forums, cultural events, and activities. The server provides tools to query event data by keyword, event type, and registration number.",
)


async def _fetch_events(
    start_index: int = 1,
    end_index: int = 100,
    evt_reg_no: str | None = None,
    title: str | None = None,
) -> dict[str, Any]:
    """Fetch events from Seoul Open Data API.

    Args:
        start_index: Start position for pagination (1-based)
        end_index: End position for pagination
        evt_reg_no: Event registration number filter
        title: Event title filter

    Returns:
        API response dictionary

    Raises:
        httpx.HTTPError: If the API request fails
    """
    # Build URL with optional filters
    url_parts = [
        API_BASE_URL,
        SEOUL_API_KEY,
        'json',
        SERVICE_NAME,
        str(start_index),
        str(end_index),
    ]

    if evt_reg_no:
        url_parts.append(evt_reg_no)
    if title:
        url_parts.append(title)

    url = '/'.join(url_parts)

    logger.info(f'Fetching events from: {url}')

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract the service data
        service_data = data.get(SERVICE_NAME, {})

        return service_data


@mcp.tool(name='SearchEvents')
async def search_events(
    keyword: str | None = None,
    event_type: str | None = None,
    start_index: int = 1,
    end_index: int = 100,
) -> dict[str, Any]:
    """Search Seoul Women's Family Foundation events.

    Args:
        keyword: Search keyword to filter by event title (optional)
        event_type: Filter by event type (e.g., 교육, 이벤트, 세미나, 포럼, 공연) (optional)
        start_index: Start position for pagination (default: 1)
        end_index: End position for pagination (default: 100, max: 1000 items per request)

    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - total_count: Total number of matching events
        - events: List of event information dictionaries
        - message: Status or error message

    Examples:
        >>> await search_events(keyword="교육", event_type="세미나")
        >>> await search_events(start_index=1, end_index=50)
    """
    try:
        # Validate pagination range
        if end_index - start_index > 1000:
            return {
                'status': 'error',
                'message': 'Maximum 1000 items per request. Please adjust start_index and end_index.',
                'total_count': 0,
                'events': [],
            }

        # Fetch from API
        api_response = await _fetch_events(
            start_index=start_index,
            end_index=end_index,
            title=keyword,
        )

        # Parse response
        result = api_response.get('RESULT', {})
        result_code = result.get('CODE', '')

        if result_code != 'INFO-000':
            return {
                'status': 'error',
                'message': result.get('MESSAGE', 'Unknown API error'),
                'total_count': 0,
                'events': [],
            }

        events_data = api_response.get('row', [])
        total_count = api_response.get('list_total_count', 0)

        # Filter by event type if specified
        if event_type:
            events_data = [
                event
                for event in events_data
                if event.get('evt_type', '').lower() == event_type.lower()
            ]

        # Convert to lowercase keys for consistency
        normalized_events = []
        for event in events_data:
            normalized_event = {k.lower(): v for k, v in event.items()}
            normalized_events.append(normalized_event)

        return {
            'status': 'success',
            'message': f'Found {len(normalized_events)} events',
            'total_count': total_count,
            'events': normalized_events,
        }

    except httpx.HTTPError as e:
        logger.error(f'API request failed: {e}')
        return {
            'status': 'error',
            'message': f'API request failed: {str(e)}',
            'total_count': 0,
            'events': [],
        }
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'total_count': 0,
            'events': [],
        }


@mcp.tool(name='GetEventDetails')
async def get_event_details(evt_reg_no: str) -> dict[str, Any]:
    """Get detailed information for a specific event by registration number.

    Args:
        evt_reg_no: Event registration number (행사번호)

    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - event: Event details dictionary
        - message: Status or error message

    Examples:
        >>> await get_event_details("30378")
    """
    try:
        api_response = await _fetch_events(
            start_index=1,
            end_index=1,
            evt_reg_no=evt_reg_no,
        )

        result = api_response.get('RESULT', {})
        result_code = result.get('CODE', '')

        if result_code != 'INFO-000':
            return {
                'status': 'error',
                'message': result.get('MESSAGE', 'Unknown API error'),
                'event': None,
            }

        events_data = api_response.get('row', [])

        if not events_data:
            return {
                'status': 'error',
                'message': f'Event not found with registration number: {evt_reg_no}',
                'event': None,
            }

        # Normalize keys to lowercase
        event = {k.lower(): v for k, v in events_data[0].items()}

        return {
            'status': 'success',
            'message': 'Event details retrieved successfully',
            'event': event,
        }

    except httpx.HTTPError as e:
        logger.error(f'API request failed: {e}')
        return {
            'status': 'error',
            'message': f'API request failed: {str(e)}',
            'event': None,
        }
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'event': None,
        }


@mcp.tool(name='ListEventTypes')
async def list_event_types() -> dict[str, Any]:
    """Get a list of all available event types in the system.

    This tool fetches recent events and extracts unique event types.

    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - event_types: List of unique event types
        - message: Status message

    Examples:
        >>> await list_event_types()
    """
    try:
        # Fetch a sample of events to get event types
        api_response = await _fetch_events(start_index=1, end_index=100)

        result = api_response.get('RESULT', {})
        result_code = result.get('CODE', '')

        if result_code != 'INFO-000':
            return {
                'status': 'error',
                'message': result.get('MESSAGE', 'Unknown API error'),
                'event_types': [],
            }

        events_data = api_response.get('row', [])

        # Extract unique event types
        event_types = list(
            {event.get('evt_type', '') for event in events_data if event.get('evt_type')}
        )
        event_types.sort()

        return {
            'status': 'success',
            'message': f'Found {len(event_types)} event types',
            'event_types': event_types,
        }

    except Exception as e:
        logger.error(f'Error fetching event types: {e}')
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'event_types': [],
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
