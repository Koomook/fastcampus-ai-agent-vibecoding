"""
모델 설정 검증 테스트

이 테스트는 코드에서 올바른 OpenAI 모델을 사용하고 있는지 확인합니다.
프로젝트 요구사항: gpt-5-mini 사용 필수
"""
import re
from pathlib import Path


def test_model_configuration():
    """hybrid_search.py에서 gpt-5-mini 모델 사용 여부 확인"""

    # hybrid_search.py 파일 읽기
    search_file = Path(__file__).parent / "hybrid_search.py"

    if not search_file.exists():
        print("❌ FAIL: hybrid_search.py 파일을 찾을 수 없습니다.")
        return False

    content = search_file.read_text(encoding='utf-8')

    # model= 패턴 찾기
    model_pattern = r'model\s*=\s*["\']([^"\']+)["\']'
    matches = re.findall(model_pattern, content)

    if not matches:
        print("❌ FAIL: 모델 설정을 찾을 수 없습니다.")
        return False

    # 결과 출력
    print(f"\n{'='*80}")
    print("모델 설정 검증 테스트")
    print(f"{'='*80}\n")

    errors = []
    warnings = []
    success_count = 0

    for i, model_name in enumerate(matches, 1):
        print(f"{i}. 발견된 모델: {model_name}")

        # 임베딩 모델은 text-embedding-3-small 허용
        if model_name == "text-embedding-3-small":
            print(f"   ✅ 임베딩 모델: 정상 (text-embedding-3-small)")
            success_count += 1
        # RAG 응답 생성은 반드시 gpt-5-mini
        elif model_name == "gpt-5-mini":
            print(f"   ✅ RAG 모델: 정상 (gpt-5-mini)")
            success_count += 1
        else:
            error_msg = f"   ❌ 잘못된 모델: {model_name} (gpt-5-mini를 사용해야 합니다)"
            print(error_msg)
            errors.append(error_msg)

    print(f"\n{'='*80}")
    print(f"검증 결과: {success_count}개 성공, {len(errors)}개 오류")
    print(f"{'='*80}\n")

    if errors:
        print("❌ 테스트 실패\n")
        print("오류 목록:")
        for error in errors:
            print(error)
        print("\n수정 필요:")
        print("1. hybrid_search.py 파일에서 잘못된 모델명을 찾으세요")
        print("2. RAG 응답 생성 함수(generate_rag_response)의 모델을 'gpt-5-mini'로 변경하세요")
        print("3. 임베딩 함수(get_embedding)는 'text-embedding-3-small' 유지")
        return False

    print("✅ 모든 테스트 통과: 올바른 모델이 설정되어 있습니다.\n")
    return True


def test_claude_md_guidelines():
    """CLAUDE.md에 모델 가이드라인이 명시되어 있는지 확인"""

    claude_md = Path(__file__).parent / "CLAUDE.md"

    if not claude_md.exists():
        print("⚠️  WARNING: CLAUDE.md 파일을 찾을 수 없습니다.")
        return True  # 경고만 출력하고 테스트는 통과

    content = claude_md.read_text(encoding='utf-8')

    if "gpt-5-mini" in content:
        print("✅ CLAUDE.md에 gpt-5-mini 가이드라인이 명시되어 있습니다.")
        return True
    else:
        print("⚠️  WARNING: CLAUDE.md에 gpt-5-mini 사용 가이드라인을 추가하는 것을 권장합니다.")
        return True


if __name__ == "__main__":
    print("OpenAI 모델 설정 검증을 시작합니다...\n")

    # 테스트 실행
    test1_passed = test_model_configuration()
    print()
    test2_passed = test_claude_md_guidelines()

    # 최종 결과
    print(f"\n{'='*80}")
    if test1_passed and test2_passed:
        print("✅ 모든 검증 통과")
        print(f"{'='*80}\n")
        exit(0)
    else:
        print("❌ 검증 실패 - 위의 오류를 수정하세요")
        print(f"{'='*80}\n")
        exit(1)
