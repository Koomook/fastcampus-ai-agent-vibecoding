"""
LangChain 기본 사용 예시
Clip 1: LLM API 이해하고 호출해보기

이 파일은 LangChain을 사용하여 LLM을 호출하는 방법을 보여줍니다.
"""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# .env 파일에서 환경변수 로드
load_dotenv()


def call_with_langchain():
    """LangChain으로 OpenAI 모델 호출 기본 예시"""
    # ChatOpenAI 모델 초기화
    # 참고: GPT-5 시리즈는 추론 모델로 temperature 파라미터를 지원하지 않습니다
    # reasoning_effort를 "minimal"로 설정하여 빠른 응답을 받습니다
    model = ChatOpenAI(
        model="gpt-5-mini",
        max_completion_tokens=2000,
        model_kwargs={"reasoning_effort": "minimal"},
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    try:
        # 메시지 배열로 호출
        messages = [
            SystemMessage(content="당신은 친절한 AI 어시스턴트입니다."),
            HumanMessage(content="인공지능이란 무엇인가요?")
        ]

        response = model.invoke(messages)
        print("AI 응답:", response.content)

    except Exception as error:
        print(f"LangChain 호출 오류: {error}")


def use_prompt_template():
    """프롬프트 템플릿을 사용한 고급 예시"""
    # 모델 초기화
    # 참고: GPT-5 시리즈는 추론 모델로 temperature 파라미터를 지원하지 않습니다
    model = ChatOpenAI(
        model="gpt-5-mini",
        model_kwargs={"reasoning_effort": "minimal"}
    )

    # 프롬프트 템플릿 정의
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "당신은 {role}입니다."),
        ("human", "{topic}에 대해 {style} 스타일로 설명해주세요.")
    ])

    # 출력 파서 정의 (문자열로 변환)
    output_parser = StrOutputParser()

    # 체인 구성: 프롬프트 -> 모델 -> 파서
    chain = prompt_template | model | output_parser

    # 체인 실행
    response = chain.invoke({
        "role": "전문 강사",
        "topic": "머신러닝",
        "style": "초보자도 이해하기 쉬운"
    })

    print("AI 응답:", response)


if __name__ == "__main__":
    print("=== LangChain 기본 호출 ===\n")
    call_with_langchain()

    print("\n" + "="*50 + "\n")

    print("=== 프롬프트 템플릿 사용 ===\n")
    use_prompt_template()
