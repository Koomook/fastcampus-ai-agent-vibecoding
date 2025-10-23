"""Seoul Cultural Events MCP Server.

This server provides tools to access Seoul Open Data API for 서울시 문화행사 정보.
"""

import os
from typing import Any

import httpx
from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

APP_NAME = 'data-seoul-mcp.culturalevents-mcp-server'

mcp = FastMCP(
    APP_NAME,
    instructions='Use this MCP server to search and retrieve Seoul city cultural events information including event schedules, locations, cultural spaces, and transportation information. The server provides tools to query event data by genre, date range, district, and other filters.',
)


class CulturalEvent(BaseModel):
    """Seoul cultural event information model.

    Note: API returns fields in UPPERCASE, but we use lowercase names with aliases
    for better Python naming conventions.
    """

    model_config = ConfigDict(populate_by_name=True)

    codename: str | None = Field(None, alias='CODENAME', description='분류 (Category)')
    guname: str | None = Field(None, alias='GUNAME', description='자치구 (District)')
    title: str | None = Field(None, alias='TITLE', description='공연/행사명 (Event/Performance Name)')
    date: str | None = Field(None, alias='DATE', description='날짜/시간 (Date/Time)')
    place: str | None = Field(None, alias='PLACE', description='장소 (Venue)')
    org_name: str | None = Field(None, alias='ORG_NAME', description='기관명 (Organization Name)')
    use_trgt: str | None = Field(None, alias='USE_TRGT', description='이용대상 (Target Audience)')
    use_fee: str | None = Field(None, alias='USE_FEE', description='이용요금 (Fee)')
    player: str | None = Field(None, alias='PLAYER', description='출연자정보 (Performer Information)')
    program: str | None = Field(None, alias='PROGRAM', description='프로그램소개 (Program Introduction)')
    etc_desc: str | None = Field(None, alias='ETC_DESC', description='기타내용 (Other Details)')
    org_link: str | None = Field(None, alias='ORG_LINK', description='홈페이지 주소 (Homepage URL)')
    main_img: str | None = Field(None, alias='MAIN_IMG', description='대표이미지 (Main Image)')
    rgstdate: str | None = Field(None, alias='RGSTDATE', description='신청일 (Registration Date)')
    ticket: str | None = Field(None, alias='TICKET', description='시민/기관 (Citizen/Organization)')
    strtdate: str | None = Field(None, alias='STRTDATE', description='시작일 (Start Date)')
    end_date: str | None = Field(None, alias='END_DATE', description='종료일 (End Date)')
    themecode: str | None = Field(None, alias='THEMECODE', description='테마분류 (Theme Category)')
    lot: str | None = Field(None, alias='LOT', description='위도 Y좌표 (Latitude)')
    lat: str | None = Field(None, alias='LAT', description='경도 X좌표 (Longitude)')
    is_free: str | None = Field(None, alias='IS_FREE', description='유무료 (Free/Paid)')
    hmpg_addr: str | None = Field(None, alias='HMPG_ADDR', description='문화포털상세URL (Culture Portal Detail URL)')


class ApiResponse(BaseModel):
    """Seoul Open Data API response model."""

    status: str = Field(..., description='Response status')
    total_count: int = Field(0, description='Total number of results')
    events: list[CulturalEvent] = Field(
        default_factory=list, description='List of cultural events'
    )
    error_message: str | None = Field(None, description='Error message if any')


async def fetch_cultural_events(
    api_key: str,
    start_index: int = 1,
    end_index: int = 100,
    codename: str | None = None,
    title: str | None = None,
    date: str | None = None,
) -> ApiResponse:
    """Fetch cultural events from Seoul Open Data API.

    Args:
        api_key: Seoul Open Data API key
        start_index: Start index for pagination (1-based)
        end_index: End index for pagination
        codename: Filter by category (분류)
        title: Filter by event title (공연/행사명)
        date: Filter by date in YYYY-MM-DD format

    Returns:
        ApiResponse containing the fetched events

    Raises:
        httpx.HTTPError: If API request fails
    """
    # Build URL
    base_url = 'http://openapi.seoul.go.kr:8088'
    service_name = 'culturalEventInfo'

    # Build path with optional filters
    path_parts = [api_key, 'json', service_name, str(start_index), str(end_index)]

    if codename:
        path_parts.append(codename)
    if title:
        path_parts.append(title)
    if date:
        path_parts.append(date)

    url = f'{base_url}/{"/".join(path_parts)}/'

    logger.info(f'Fetching cultural events from: {url}')

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            # Check for API errors
            if 'RESULT' in data.get('culturalEventInfo', {}):
                result = data['culturalEventInfo']['RESULT']
                error_code = result.get('CODE', '')
                error_message = result.get('MESSAGE', '')

                if error_code != 'INFO-000':
                    logger.error(f'API Error: {error_code} - {error_message}')
                    return ApiResponse(
                        status='error',
                        total_count=0,
                        events=[],
                        error_message=f'{error_code}: {error_message}',
                    )

            # Parse successful response
            event_info = data.get('culturalEventInfo', {})
            total_count = event_info.get('list_total_count', 0)
            row_data = event_info.get('row', [])

            events = [CulturalEvent(**event) for event in row_data]

            logger.success(f'Successfully fetched {len(events)} events (total: {total_count})')

            return ApiResponse(status='success', total_count=total_count, events=events)

        except httpx.HTTPError as e:
            logger.error(f'HTTP error occurred: {e}')
            return ApiResponse(status='error', total_count=0, events=[], error_message=str(e))
        except Exception as e:
            logger.error(f'Unexpected error occurred: {e}')
            return ApiResponse(status='error', total_count=0, events=[], error_message=str(e))


@mcp.tool(name='SearchCulturalEvents')
async def search_cultural_events(
    codename: str | None = None,
    title: str | None = None,
    date: str | None = None,
    start_index: int = 1,
    end_index: int = 100,
) -> dict[str, Any]:
    """Search Seoul cultural events from Seoul Culture Portal.

    This tool queries the Seoul Open Data API to retrieve cultural event information
    including performances, exhibitions, and other cultural activities.

    Args:
        codename: Filter by event category (분류) e.g., "콘서트", "전시/미술", "연극"
        title: Filter by event title (공연/행사명) - partial match supported
        date: Filter by date in YYYY-MM-DD format (날짜/시간)
        start_index: Start index for pagination (default: 1, must be >= 1)
        end_index: End index for pagination (default: 100, max 1000 records per request)

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - total_count: Total number of matching events
        - count: Number of events returned in this response
        - events: List of event objects with details (category, title, date, venue, etc.)
        - error_message: Error description if status is "error"

    Example:
        Search for concerts:
        {"codename": "콘서트", "start_index": 1, "end_index": 10}

        Search by title:
        {"title": "재즈", "start_index": 1, "end_index": 50}

        Search by date:
        {"date": "2025-12-13", "start_index": 1, "end_index": 20}
    """
    # Get API key from environment
    api_key = os.getenv('SEOUL_API_KEY', '')

    if not api_key:
        logger.error('SEOUL_API_KEY environment variable is not set')
        return {
            'status': 'error',
            'total_count': 0,
            'count': 0,
            'events': [],
            'error_message': 'SEOUL_API_KEY environment variable is required. Please set it with your Seoul Open Data API key.',
        }

    # Validate pagination parameters
    if start_index < 1:
        return {
            'status': 'error',
            'total_count': 0,
            'count': 0,
            'events': [],
            'error_message': 'start_index must be >= 1',
        }

    if end_index < start_index:
        return {
            'status': 'error',
            'total_count': 0,
            'count': 0,
            'events': [],
            'error_message': 'end_index must be >= start_index',
        }

    if (end_index - start_index + 1) > 1000:
        return {
            'status': 'error',
            'total_count': 0,
            'count': 0,
            'events': [],
            'error_message': 'Cannot request more than 1000 records at once',
        }

    # Fetch events from API
    result = await fetch_cultural_events(
        api_key=api_key,
        start_index=start_index,
        end_index=end_index,
        codename=codename,
        title=title,
        date=date,
    )

    # Convert to dict for MCP response
    return {
        'status': result.status,
        'total_count': result.total_count,
        'count': len(result.events),
        'events': [event.model_dump() for event in result.events],
        'error_message': result.error_message,
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
