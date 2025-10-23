"""
reasoning_effort 파라미터 실험
Clip 2: 세부 파라미터 이해하기

이 파일은 reasoning_effort가 사고 깊이에 미치는 영향을 보여줍니다.
"""

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def solve_complex_problem(problem: str, effort: str):
    """
    복잡한 문제를 해결합니다.

    Args:
        problem: 풀어야 할 문제
        effort: 'low', 'medium', 또는 'high'
    """
    response = client.chat.completions.create(
        model='gpt-5',
        messages=[{
            'role': 'user',
            'content': problem
        }],
        reasoning_effort=effort
    )

    print(f"=== reasoning_effort: {effort} ===\n")
    print("응답:", response.choices[0].message.content)

    if response.usage:
        # reasoning_tokens는 내부 사고에 사용된 토큰
        reasoning = getattr(response.usage.completion_tokens_details, 'reasoning_tokens', 0) if hasattr(response.usage, 'completion_tokens_details') else 0
        completion = response.usage.completion_tokens

        print(f"\n토큰 사용량:")
        if reasoning:
            print(f"  - Reasoning tokens: {reasoning}")
        print(f"  - Completion tokens: {completion}")
        print(f"  - Total: {response.usage.total_tokens}")


def demonstrate_reasoning_effort():
    """reasoning_effort의 low, medium, high를 비교합니다."""

    # 복잡한 논리 문제
    complex_problem = """
다섯 명의 친구가 서로 다른 나라에 살고 있습니다:
- Alex는 프랑스나 독일에 살지 않습니다.
- Bob은 독일 옆 나라에 삽니다.
- Charlie는 Alex보다 동쪽에 삽니다.
- Diana는 가장 서쪽 나라에 삽니다.
- Emma는 Charlie 바로 옆 나라에 삽니다.

국가 옵션: 프랑스, 독일, 폴란드, 체코, 오스트리아

각자 어느 나라에 살고 있나요? 단계별로 추론해주세요.
"""

    print("복잡한 논리 문제 해결\n")
    print("="*70)

    # low: 빠른 추론
    solve_complex_problem(complex_problem, 'low')

    print("\n" + "="*70 + "\n")

    # high: 깊은 추론
    solve_complex_problem(complex_problem, 'high')


def use_case_examples():
    """작업 유형별 권장 설정 예시"""

    print("\n\n" + "="*70)
    print("=== 작업 유형별 권장 설정 ===")
    print("="*70)

    # 1. 간단한 질문 응답 (low)
    print("\n1. 간단한 질문 (reasoning_effort=low)\n")
    simple_response = client.chat.completions.create(
        model='gpt-5',
        messages=[{'role': 'user', 'content': 'Python이란?'}],
        reasoning_effort='low'
    )
    print(simple_response.choices[0].message.content)

    # 2. 복잡한 수학 문제 (high)
    print("\n2. 복잡한 수학 문제 (reasoning_effort=high)\n")
    math_response = client.chat.completions.create(
        model='gpt-5',
        messages=[{
            'role': 'user',
            'content': '한 상자에 사과가 x개 있습니다. 매일 20%를 먹고, 남은 것의 10%를 더 산다면, 5일 후 사과가 100개 남으려면 처음 몇 개가 필요한가요?'
        }],
        reasoning_effort='high'
    )
    print(math_response.choices[0].message.content)


if __name__ == "__main__":
    print("=== reasoning_effort 파라미터 실험 ===\n")
    demonstrate_reasoning_effort()
    use_case_examples()
