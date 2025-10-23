# 스트리밍 문제 해결 방법

## 핵심 문제

현재 구현은 **도구 호출 후 LLM 재호출 로직이 누락**되었습니다.

### 현재 흐름 (불완전)
```
1. 사용자: "안녕"
2. LLM: "도구 필요 없음, 답변 생성"
3. 스트리밍: (None 값으로 인해 중단)
```

### 올바른 흐름 (원본 패턴)
```
1. 사용자: "의사 대출 추천해줘"
2. LLM: hybrid_search_tool 호출 결정
3. 도구 실행: [...결과...]
4. **LLM 재호출**: 도구 결과를 보고 최종 답변 생성
5. 스트리밍: 최종 답변 전송
```

## 해결 방법

### 옵션 1: 재귀 호출 패턴 (원본 방식)

```python
def stream_text(messages: List[ChatCompletionMessageParam], protocol: str = 'data'):
    draft_tool_calls = []
    draft_tool_calls_index = -1

    stream = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        stream=True,
        tools=[...]
    )

    for chunk in stream:
        # ... 스트리밍 처리 ...

        # 도구 호출 완료 시
        if finish_reason == "tool_calls":
            # 1. 도구 호출 정보 스트리밍
            for tool_call in draft_tool_calls:
                yield '9:{{...}}\n'

                # 2. 도구 실행
                tool_result = available_tools[tool_call["name"]](**json.loads(tool_call["arguments"]))
                yield 'a:{{...}}\n'

                # 3. 메시지에 추가
                messages.append({
                    "role": "assistant",
                    "tool_calls": [...도구 호출 정보...]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(tool_result)
                })

            # 4. LLM 재호출 (재귀)
            for next_chunk in stream_text(messages, protocol):
                yield next_chunk

            return  # 재귀 호출 후 종료
```

### 옵션 2: 간단한 비스트리밍 방식

```python
def stream_text(messages: List[ChatCompletionMessageParam], protocol: str = 'data'):
    # 첫 번째 LLM 호출
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o",
        tools=[...]
    )

    message = response.choices[0].message

    # 도구 호출이 있으면
    if message.tool_calls:
        for tool_call in message.tool_calls:
            # 도구 실행
            tool_result = available_tools[tool_call.function.name](
                **json.loads(tool_call.function.arguments)
            )

            # 스트리밍으로 전송
            yield '9:{{...}}\n'
            yield 'a:{{...}}\n'

            # 메시지에 추가
            messages.append({
                "role": "assistant",
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

        # 두 번째 LLM 호출 (최종 답변)
        final_stream = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            stream=True
        )

        for chunk in final_stream:
            if chunk.choices[0].delta.content:
                yield '0:{{...}}\n'

    # 도구 호출 없으면 바로 응답
    else:
        if message.content:
            yield '0:{{...}}\n'

    yield 'e:{{...}}\n'
```

## 권장 사항

**즉시 시도**: 옵션 2 (간단한 비스트리밍)
- 이해하기 쉬움
- 디버깅 용이
- 도구 호출 흐름 명확

**장기적 목표**: 옵션 1 (재귀 호출)
- 원본 샘플과 동일한 패턴
- 다중 도구 호출 지원
- 복잡한 에이전트 워크플로우 가능

## 테스트 시나리오

### 1. 단순 인사
```
입력: "안녕"
예상: 도구 없이 바로 응답
```

### 2. 대출 검색
```
입력: "의사 전용 대출 추천해줘"
예상: hybrid_search_tool 호출 → 결과 기반 답변
```

### 3. 웹 검색
```
입력: "2025년 기준금리는?"
예상: tavily_search_tool 호출 → 결과 기반 답변
```

### 4. 복합 질문
```
입력: "의사 대출과 현재 금리 동향"
예상: 두 도구 순차 호출 → 종합 답변
```

## 다음 단계

1. 옵션 2로 `api/index.py` 수정
2. 서버 재시작
3. 브라우저에서 테스트
4. 작동하면 옵션 1로 개선

---

**업데이트**: 2025-10-12 11:50 PM KST
