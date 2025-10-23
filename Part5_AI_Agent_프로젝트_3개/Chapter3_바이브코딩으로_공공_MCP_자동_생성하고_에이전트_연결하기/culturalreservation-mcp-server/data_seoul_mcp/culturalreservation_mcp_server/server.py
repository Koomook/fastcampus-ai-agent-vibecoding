"""Seoul Cultural Events Reservation MCP Server.

This server provides tools to access Seoul Open Data API for 문화행사 공공서비스예약.
"""

import os
from typing import Any

import httpx
from loguru import logger
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

APP_NAME = 'data-seoul-mcp.culturalreservation-mcp-server'

# API Configuration
SEOUL_API_KEY = os.getenv('SEOUL_API_KEY', 'sample')
SEOUL_API_BASE_URL = 'http://openapi.seoul.go.kr:8088'
SERVICE_NAME = 'ListPublicReservationCulture'


class CulturalEvent(BaseModel):
    """Cultural event information model.

    Maps uppercase API field names to lowercase Python attributes.
    """

    model_config = {'populate_by_name': True}

    gubun: str | None = Field(None, alias='GUBUN', description='서비스구분 - Service type')
    svcid: str | None = Field(None, alias='SVCID', description='서비스ID - Service ID')
    maxclassnm: str | None = Field(
        None, alias='MAXCLASSNM', description='대분류명 - Main category name'
    )
    minclassnm: str | None = Field(
        None, alias='MINCLASSNM', description='소분류명 - Sub category name'
    )
    svcstatnm: str | None = Field(
        None, alias='SVCSTATNM', description='서비스상태 - Service status'
    )
    svcnm: str | None = Field(None, alias='SVCNM', description='서비스명 - Service name')
    payatnm: str | None = Field(None, alias='PAYATNM', description='결제방법 - Payment method')
    placenm: str | None = Field(None, alias='PLACENM', description='장소명 - Place name')
    usetgtinfo: str | None = Field(
        None, alias='USETGTINFO', description='서비스대상 - Service target'
    )
    svcurl: str | None = Field(None, alias='SVCURL', description='바로가기URL - Direct URL')
    x: str | None = Field(None, alias='X', description='장소X좌표 - Place X coordinate')
    y: str | None = Field(None, alias='Y', description='장소Y좌표 - Place Y coordinate')
    svcopnbgndt: str | int | None = Field(
        None,
        alias='SVCOPNBGNDT',
        description='서비스개시시작일시 - Service start datetime (string or unix timestamp)',
    )
    svcopnenddt: str | int | None = Field(
        None,
        alias='SVCOPNENDDT',
        description='서비스개시종료일시 - Service end datetime (string or unix timestamp)',
    )
    rcptbgndt: str | int | None = Field(
        None,
        alias='RCPTBGNDT',
        description='접수시작일시 - Reception start datetime (string or unix timestamp)',
    )
    rcptenddt: str | int | None = Field(
        None,
        alias='RCPTENDDT',
        description='접수종료일시 - Reception end datetime (string or unix timestamp)',
    )
    areanm: str | None = Field(None, alias='AREANM', description='지역명 - Area name')
    imgurl: str | None = Field(None, alias='IMGURL', description='이미지경로 - Image URL')
    dtlcont: str | None = Field(None, alias='DTLCONT', description='상세내용 - Detail content')
    telno: str | None = Field(None, alias='TELNO', description='전화번호 - Telephone number')
    v_min: str | None = Field(
        None, alias='V_MIN', description='서비스이용 시작시간 - Service usage start time'
    )
    v_max: str | None = Field(
        None, alias='V_MAX', description='서비스이용 종료시간 - Service usage end time'
    )
    revstddaynm: str | None = Field(
        None, alias='REVSTDDAYNM', description='취소기간 기준정보 - Cancellation period criteria'
    )
    revstdday: str | int | None = Field(
        None,
        alias='REVSTDDAY',
        description='취소기간 기준일까지 - Days until cancellation deadline (string or int)',
    )


class APIResponse(BaseModel):
    """Seoul Open Data API response model."""

    description: dict[str, str] | None = Field(None, alias='DESCRIPTION')
    data: list[CulturalEvent] | None = Field(None, alias='DATA')


mcp = FastMCP(
    APP_NAME,
    instructions="""Use this MCP server to search and retrieve Seoul cultural events and public service reservation information.

The server provides access to cultural events, exhibitions, performances, concerts, and other public service reservations in Seoul.

Available tools:
- search_cultural_events: Search for cultural events with filters (category, status, area)
- get_event_by_id: Get detailed information for a specific event by service ID
""",
)


async def fetch_api_data(
    start_index: int = 1,
    end_index: int = 100,
    minclassnm: str | None = None,
) -> dict[str, Any]:
    """Fetch data from Seoul Open Data API.

    Args:
        start_index: Start index for pagination
        end_index: End index for pagination
        minclassnm: Sub category name filter

    Returns:
        API response data
    """
    # Build URL
    url_parts = [
        SEOUL_API_BASE_URL,
        SEOUL_API_KEY,
        'json',
        SERVICE_NAME,
        str(start_index),
        str(end_index),
    ]

    if minclassnm:
        url_parts.append(minclassnm)

    url = '/'.join(url_parts)

    logger.info(f'Fetching data from Seoul Open Data API: {url}')

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            # Check for API errors
            service_data = data.get(SERVICE_NAME, {})
            result = service_data.get('RESULT', {})
            code = result.get('CODE', 'INFO-000')

            if code != 'INFO-000':
                error_msg = result.get('MESSAGE', 'Unknown error')
                logger.error(f'API Error: {code} - {error_msg}')
                return {'error': f'{code}: {error_msg}'}

            return data

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP error occurred: {e}')
        return {'error': f'HTTP error: {e.response.status_code}'}
    except httpx.RequestError as e:
        logger.error(f'Request error occurred: {e}')
        return {'error': f'Request error: {str(e)}'}
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return {'error': f'Unexpected error: {str(e)}'}


@mcp.tool(name='search_cultural_events')
async def search_cultural_events(
    minclassnm: str | None = None,
    svcstatnm: str | None = None,
    areanm: str | None = None,
    start_index: int = 1,
    end_index: int = 100,
) -> dict[str, Any]:
    """Search Seoul cultural events with various filters.

    Args:
        minclassnm: Sub category filter (e.g., "콘서트", "전시/관람", "교육체험")
        svcstatnm: Service status filter (e.g., "접수중", "접수종료", "예약마감")
        areanm: Area name filter (e.g., "종로구", "중구", "강남구")
        start_index: Start index for pagination (default: 1)
        end_index: End index for pagination (default: 100, max: 1000)

    Returns:
        Dictionary containing cultural events data with filters applied
    """
    # Validate pagination
    if end_index - start_index > 1000:
        return {'error': 'Cannot request more than 1000 items at once'}

    # Fetch data from API
    data = await fetch_api_data(start_index, end_index, minclassnm)

    if 'error' in data:
        return data

    # Parse response
    service_data = data.get(SERVICE_NAME, {})
    row_data = service_data.get('row', [])

    # Apply additional filters (API returns uppercase field names)
    filtered_events = row_data

    if svcstatnm:
        filtered_events = [
            event
            for event in filtered_events
            if event.get('SVCSTATNM', '').lower() == svcstatnm.lower()
        ]

    if areanm:
        filtered_events = [
            event for event in filtered_events if event.get('AREANM', '').lower() == areanm.lower()
        ]

    # Convert to Pydantic models for validation
    events = [CulturalEvent(**event) for event in filtered_events]

    return {
        'total_count': len(events),
        'list_total_count': service_data.get('list_total_count', 0),
        'filters': {
            'minclassnm': minclassnm,
            'svcstatnm': svcstatnm,
            'areanm': areanm,
        },
        'events': [event.model_dump() for event in events],
    }


@mcp.tool(name='get_event_by_id')
async def get_event_by_id(
    svcid: str,
) -> dict[str, Any]:
    """Get detailed information for a specific cultural event by service ID.

    Args:
        svcid: Service ID (e.g., "S250923140317295158")

    Returns:
        Dictionary containing detailed event information
    """
    # Fetch data (we need to search through all to find the specific ID)
    data = await fetch_api_data(1, 1000)

    if 'error' in data:
        return data

    # Parse response
    service_data = data.get(SERVICE_NAME, {})
    row_data = service_data.get('row', [])

    # Find event by ID (API returns uppercase field names)
    event_data = next(
        (event for event in row_data if event.get('SVCID') == svcid),
        None,
    )

    if not event_data:
        return {'error': f'Event with ID {svcid} not found'}

    # Convert to Pydantic model
    event = CulturalEvent(**event_data)

    return {
        'event': event.model_dump(),
    }


def main() -> None:
    """Run the MCP server with CLI argument support."""
    logger.info(f'Starting {APP_NAME}')
    logger.info(f'Using API key: {SEOUL_API_KEY[:10]}...' if len(SEOUL_API_KEY) > 10 else 'sample')

    mcp.run()


if __name__ == '__main__':
    main()
