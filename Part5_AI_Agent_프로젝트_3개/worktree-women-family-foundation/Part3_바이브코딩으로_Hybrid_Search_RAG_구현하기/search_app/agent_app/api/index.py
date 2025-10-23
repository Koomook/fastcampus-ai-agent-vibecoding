import os
import json
from typing import List
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from openai import OpenAI
from .utils.prompt import ClientMessage, convert_to_openai_messages
from .utils.tools import hybrid_search_tool, tavily_search_tool


load_dotenv(".env.local")

app = FastAPI()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class Request(BaseModel):
    messages: List[ClientMessage]


# 사용 가능한 도구 정의
available_tools = {
    "hybrid_search_tool": hybrid_search_tool,
    "tavily_search_tool": tavily_search_tool,
}


def stream_text(messages: List[ChatCompletionMessageParam], protocol: str = 'data'):
    """
    OpenAI Chat Completions API를 사용하여 스트리밍 응답 생성
    Data Stream Protocol 형식으로 반환

    옵션 2: 간단한 비스트리밍 방식
    1. 첫 번째 LLM 호출 (비스트리밍) - 도구 필요 여부 판단
    2. 도구 호출 시 실행 후 메시지에 추가
    3. 두 번째 LLM 호출 (스트리밍) - 최종 답변 생성
    """
    # 도구 정의
    tools = [
        {
            "type": "function",
            "function": {
                "name": "hybrid_search_tool",
                "description": "농협 대출 상품을 검색합니다. 대출 상품 정보, 금리, 대상, 한도 등을 찾을 때 사용하세요.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "검색할 키워드 또는 질문 (예: '의사 전용 대출', '공무원 대출')",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "반환할 최대 결과 개수 (기본값: 3)",
                            "default": 3,
                        },
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "tavily_search_tool",
                "description": "웹에서 최신 금융 정보를 검색합니다. 기준금리, 시장 동향, 최신 뉴스 등을 찾을 때 사용하세요.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "검색할 키워드 또는 질문 (예: '2025년 기준금리', '대출 시장 동향')",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "반환할 최대 결과 개수 (기본값: 3)",
                            "default": 3,
                        },
                    },
                    "required": ["query"],
                },
            },
        },
    ]

    # 1단계: 첫 번째 LLM 호출 (도구 필요 여부 판단)
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        tools=tools
    )

    message = response.choices[0].message

    # 2단계: 도구 호출이 있으면 실행
    if message.tool_calls:
        # Assistant의 도구 호출 메시지 추가
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })

        # 각 도구 실행 및 결과 전송
        for tool_call in message.tool_calls:
            # 도구 호출 정보 스트리밍 전송
            yield '9:{{"toolCallId":"{id}","toolName":"{name}","args":{args}}}\n'.format(
                id=tool_call.id,
                name=tool_call.function.name,
                args=tool_call.function.arguments
            )

            # 도구 실행
            try:
                tool_result = available_tools[tool_call.function.name](
                    **json.loads(tool_call.function.arguments)
                )

                # 도구 결과 스트리밍 전송
                yield 'a:{{"toolCallId":"{id}","toolName":"{name}","args":{args},"result":{result}}}\n'.format(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    args=tool_call.function.arguments,
                    result=json.dumps(tool_result, ensure_ascii=False)
                )

                # 도구 결과를 메시지에 추가
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

            except Exception as e:
                # 도구 실행 오류 처리
                error_result = {"error": str(e)}
                yield 'a:{{"toolCallId":"{id}","toolName":"{name}","args":{args},"result":{result}}}\n'.format(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    args=tool_call.function.arguments,
                    result=json.dumps(error_result, ensure_ascii=False)
                )

                # 오류 결과도 메시지에 추가
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(error_result, ensure_ascii=False)
                })

        # 3단계: 두 번째 LLM 호출 (최종 답변 생성, 스트리밍)
        final_stream = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            stream=True
        )

        for chunk in final_stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            finish_reason = chunk.choices[0].finish_reason if chunk.choices else None

            # 텍스트 델타 처리
            if delta and delta.content:
                yield '0:{text}\n'.format(text=json.dumps(delta.content, ensure_ascii=False))

            # 스트림 종료
            if finish_reason == "stop":
                yield 'e:{{"finishReason":"stop","usage":{{"promptTokens":0,"completionTokens":0}},"isContinued":false}}\n'
                return

    # 도구 호출 없으면 바로 응답 (스트리밍)
    else:
        if message.content:
            # 내용을 단어별로 스트리밍 (실제 OpenAI 스트리밍 효과 재현)
            # 단순히 전체 내용을 한 번에 전송
            yield '0:{text}\n'.format(text=json.dumps(message.content, ensure_ascii=False))

        yield 'e:{{"finishReason":"stop","usage":{{"promptTokens":0,"completionTokens":0}},"isContinued":false}}\n'


@app.post("/api/chat")
async def handle_chat_data(request: Request, protocol: str = Query('data')):
    """
    채팅 엔드포인트
    Data Stream Protocol을 사용하여 스트리밍 응답 반환
    """
    messages = request.messages
    openai_messages = convert_to_openai_messages(messages)

    response = StreamingResponse(stream_text(openai_messages, protocol))
    response.headers['x-vercel-ai-data-stream'] = 'v1'
    return response
