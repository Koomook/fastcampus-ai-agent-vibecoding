"""
verbosity 파라미터 실험
Clip 2: 세부 파라미터 이해하기

이 파일은 verbosity 파라미터가 응답 길이에 미치는 영향을 보여줍니다.
"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def demonstrate_verbosity():
    """verbosity 파라미터의 low, medium, high 차이를 비교합니다."""
    question = "머신러닝이란 무엇인가요?"

    print(f"질문: {question}\n")
    print("="*70)

    # verbosity=low: 간결한 답변
    print("\n=== verbosity: low (간결) ===\n")
    low_response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{'role': 'user', 'content': question}],
        verbosity='low'
    )
    print(low_response.choices[0].message.content)

    # verbosity=medium: 보통 답변 (기본값)
    print("\n=== verbosity: medium (보통) ===\n")
    medium_response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{'role': 'user', 'content': question}],
        verbosity='medium'
    )
    print(medium_response.choices[0].message.content)

    # verbosity=high: 상세한 답변
    print("\n=== verbosity: high (상세) ===\n")
    high_response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{'role': 'user', 'content': question}],
        verbosity='high'
    )
    print(high_response.choices[0].message.content)


def fill_ui_card_example(bullet_points: int) -> str:
    """
    실무 사례: UI 카드 채우기
    bullet_points 수에 따라 verbosity를 조절합니다.
    """
    verbosity = 'high' if bullet_points == 1 else \
                'medium' if bullet_points == 3 else 'low'

    response = client.chat.completions.create(
        model='gpt-5-nano',
        messages=[{
            'role': 'user',
            'content': f'이 제품의 {bullet_points}가지 주요 특징을 설명해주세요: "AI 기반 코드 에디터"'
        }],
        verbosity=verbosity
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print("=== verbosity 파라미터 실험 ===\n")
    demonstrate_verbosity()

    print("\n\n" + "="*70)
    print("\n=== 실무 사례: UI 카드 채우기 ===\n")

    # 1개 포인트: 길게 설명
    print("bullet_points=1 (verbosity=high):")
    print(fill_ui_card_example(1))

    print("\n" + "-"*70 + "\n")

    # 5개 포인트: 짧게 설명
    print("bullet_points=5 (verbosity=low):")
    print(fill_ui_card_example(5))
