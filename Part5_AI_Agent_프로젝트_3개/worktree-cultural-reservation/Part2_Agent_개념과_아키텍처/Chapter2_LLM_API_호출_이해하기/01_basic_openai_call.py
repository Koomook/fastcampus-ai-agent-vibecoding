"""
기본 OpenAI API 호출 예시
Clip 1: LLM API 이해하고 호출해보기

이 파일은 OpenAI API를 직접 호출하는 기본적인 방법을 보여줍니다.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경변수 로드
load_dotenv()


def call_openai():
    """
    OpenAI API를 호출하여 간단한 질문에 답변을 받습니다.

    환경변수 OPENAI_API_KEY가 설정되어 있어야 합니다.
    """
    # OpenAI 클라이언트 초기화
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    try:
        # API 호출
        # 참고: GPT-5 시리즈는 추론 모델로 temperature 파라미터를 지원하지 않습니다
        # reasoning_effort를 "minimal"로 설정하여 빠른 응답을 받습니다
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 친절한 AI 어시스턴트입니다."
                },
                {
                    "role": "user",
                    "content": "인공지능이란 무엇인가요?"
                }
            ],
            reasoning_effort="minimal",  # 추론 토큰 사용 최소화
            max_completion_tokens=2000
        )

        # 응답 추출 및 출력
        ai_message = response.choices[0].message.content
        print("AI 응답:", ai_message)

        # 사용된 토큰 정보
        if response.usage:
            print(f"\n사용 토큰 - Prompt: {response.usage.prompt_tokens}, "
                  f"Completion: {response.usage.completion_tokens}, "
                  f"Total: {response.usage.total_tokens}")

    except Exception as error:
        print(f"API 호출 오류: {error}")


if __name__ == "__main__":
    print("=== 기본 OpenAI API 호출 예시 ===\n")
    call_openai()
