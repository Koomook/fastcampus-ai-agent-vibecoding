#!/usr/bin/env python3
"""
Recruit Service MCP Server
채용 서비스 데이터베이스와 상호작용하는 MCP 서버

Features:
- 읽기 전용 쿼리 (query tool)
- 안전한 후보자 정보 업데이트 (update_candidate tool)
"""

import asyncio
import os
from typing import Any
import asyncpg
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import mcp.server.stdio
import mcp.types as types

# 환경 변수에서 데이터베이스 연결 정보 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable must be set")

# MCP 서버 인스턴스 생성
app = Server("recruit-mcp-server")

# 데이터베이스 연결 풀
db_pool: asyncpg.Pool | None = None


async def get_db_pool() -> asyncpg.Pool:
    """데이터베이스 연결 풀 가져오기"""
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return db_pool


@app.list_resources()
async def list_resources() -> list[Resource]:
    """
    사용 가능한 리소스 목록 반환
    - candidates 테이블의 스키마 정보
    """
    return [
        Resource(
            uri="schema://candidates",
            name="Candidates Table Schema",
            mimeType="application/json",
            description="채용 후보자 테이블의 스키마 정보",
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """
    리소스 읽기
    - candidates 테이블의 스키마 반환
    """
    if uri != "schema://candidates":
        raise ValueError(f"Unknown resource: {uri}")

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # 테이블 스키마 조회
        schema = await conn.fetch("""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = 'candidates'
            ORDER BY ordinal_position
        """)

        schema_info = {
            "table": "candidates",
            "columns": [
                {
                    "name": row["column_name"],
                    "type": row["data_type"],
                    "nullable": row["is_nullable"] == "YES",
                    "default": row["column_default"],
                }
                for row in schema
            ],
        }

        import json
        return json.dumps(schema_info, indent=2, ensure_ascii=False)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    사용 가능한 도구 목록 반환
    """
    return [
        Tool(
            name="query",
            description="읽기 전용 SQL 쿼리를 실행합니다. 데이터를 조회하는 용도로만 사용하세요.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "실행할 SQL SELECT 쿼리",
                    }
                },
                "required": ["sql"],
            },
        ),
        Tool(
            name="update_candidate",
            description="후보자의 정보를 안전하게 업데이트합니다. position, skills, company 필드만 수정 가능합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "candidate_id": {
                        "type": "integer",
                        "description": "업데이트할 후보자의 ID",
                    },
                    "position": {
                        "type": "string",
                        "description": "새로운 직군 (Developer, Designer, PM, Marketer)",
                    },
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "새로운 스킬 목록",
                    },
                    "company": {
                        "type": "string",
                        "description": "새로운 회사명",
                    },
                },
                "required": ["candidate_id"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    도구 실행
    """
    if name == "query":
        return await execute_query(arguments["sql"])
    elif name == "update_candidate":
        return await update_candidate(
            arguments["candidate_id"],
            arguments.get("position"),
            arguments.get("skills"),
            arguments.get("company"),
        )
    else:
        raise ValueError(f"Unknown tool: {name}")


async def execute_query(sql: str) -> list[TextContent]:
    """
    읽기 전용 SQL 쿼리 실행
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            # 읽기 전용 트랜잭션 시작
            async with conn.transaction(readonly=True):
                result = await conn.fetch(sql)

                # 결과를 JSON으로 변환
                import json
                rows = [dict(row) for row in result]

                # JSON 직렬화 시 datetime 처리
                def json_serial(obj):
                    """JSON serializer for datetime objects"""
                    from datetime import datetime
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    raise TypeError(f"Type {type(obj)} not serializable")

                result_json = json.dumps(rows, indent=2, ensure_ascii=False, default=json_serial)

                return [
                    TextContent(
                        type="text",
                        text=f"쿼리 실행 완료 ({len(rows)}개 행)\n\n{result_json}",
                    )
                ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"쿼리 실행 중 오류 발생: {str(e)}",
                )
            ]


async def update_candidate(
    candidate_id: int,
    position: str | None = None,
    skills: list[str] | None = None,
    company: str | None = None,
) -> list[TextContent]:
    """
    후보자 정보 업데이트
    name과 id는 변경 불가 (보안상의 이유)
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        try:
            # 업데이트할 필드 구성
            updates = []
            params = [candidate_id]
            param_idx = 2

            if position is not None:
                updates.append(f"position = ${param_idx}")
                params.append(position)
                param_idx += 1

            if skills is not None:
                updates.append(f"skills = ${param_idx}")
                params.append(skills)
                param_idx += 1

            if company is not None:
                updates.append(f"company = ${param_idx}")
                params.append(company)
                param_idx += 1

            if not updates:
                return [
                    TextContent(
                        type="text",
                        text="업데이트할 필드가 없습니다.",
                    )
                ]

            # UPDATE 쿼리 실행
            sql = f"""
                UPDATE candidates
                SET {', '.join(updates)}
                WHERE id = $1
                RETURNING id, name, position, skills, company
            """

            result = await conn.fetchrow(sql, *params)

            if result is None:
                return [
                    TextContent(
                        type="text",
                        text=f"ID {candidate_id}인 후보자를 찾을 수 없습니다.",
                    )
                ]

            import json
            result_dict = dict(result)
            result_json = json.dumps(result_dict, indent=2, ensure_ascii=False)

            return [
                TextContent(
                    type="text",
                    text=f"후보자 정보가 업데이트되었습니다:\n\n{result_json}",
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"업데이트 중 오류 발생: {str(e)}",
                )
            ]


async def main():
    """서버 시작"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
