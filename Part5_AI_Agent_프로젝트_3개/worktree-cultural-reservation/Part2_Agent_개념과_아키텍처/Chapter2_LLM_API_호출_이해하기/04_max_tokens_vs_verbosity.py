"""
max_tokens vs verbosity 비교
Clip 2: 세부 파라미터 이해하기

이 파일은 max_tokens와 verbosity의 차이를 명확히 보여줍니다.
"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def compare_max_tokens_vs_verbosity():
    """max_tokens와 verbosity의 차이를 비교합니다."""

    print("="*70)
    print("요청: 5문단으로 에세이를 작성해주세요 (AI 에이전트에 대해)")
    print("="*70)

    # 1. max_completion_tokens=100: 하드 제한 (문장이 끊길 수 있음)
    print("\n=== max_completion_tokens=100 (하드 제한) ===\n")
    max_tokens_response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{
            'role': 'user',
            'content': 'AI 에이전트에 대해 5문단으로 에세이를 작성해주세요.'
        }],
        max_completion_tokens=200,
        reasoning_effort='minimal'
    )
    print(max_tokens_response.choices[0].message.content)
    print(f"\n⚠️ 100 토큰에서 강제로 종료됨 (문장이 끊김)")

    # 2. verbosity=low: 스타일 가이드 (형식은 보존)
    print("\n\n=== verbosity=low (스타일 가이드) ===\n")
    verbosity_response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{
            'role': 'user',
            'content': 'AI 에이전트에 대해 5문단으로 에세이를 작성해주세요.'
        }],
        verbosity='low',
        reasoning_effort='minimal'
    )
    print(verbosity_response.choices[0].message.content)
    print(f"\n✅ 5개의 단락이 모두 생성되지만, 각 단락이 짧음")


def practical_example():
    """실무에서 함께 사용하는 예시"""

    def create_product_description(style: str) -> str:
        """style: 'brief' 또는 'detailed'"""
        response = client.chat.completions.create(
            model='gpt-5',
            messages=[{
                'role': 'user',
                'content': '노트북 제품의 3가지 특징을 설명해주세요.'
            }],
            verbosity='low' if style == 'brief' else 'high',  # 스타일 조절
            reasoning_effort='minimal',
            max_completion_tokens=1000  # 안전장치: 절대 1000토큰 초과 불가
        )
        return response.choices[0].message.content

    print("\n\n" + "="*70)
    print("=== 실무 예시: verbosity + max_completion_tokens 함께 사용 ===")
    print("="*70)

    print("\n--- style='brief' (verbosity=low, max_completion_tokens=1000) ---\n")
    print(create_product_description('brief'))

    print("\n--- style='detailed' (verbosity=high, max_completion_tokens=1000) ---\n")
    print(create_product_description('detailed'))


if __name__ == "__main__":
    compare_max_tokens_vs_verbosity()
    practical_example()
