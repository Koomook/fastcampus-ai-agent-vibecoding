"""
stream_text 함수를 직접 테스트하는 스크립트
"""
import sys
import os

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import stream_text

# 테스트 메시지
messages = [
    {"role": "user", "content": "안녕하세요"}
]

print("=== 단순 인사 테스트 ===")
print("입력:", messages[0]["content"])
print("\n응답:")
try:
    for chunk in stream_text(messages):
        print(chunk, end='')
    print("\n\n✅ 테스트 성공!")
except Exception as e:
    print(f"\n\n❌ 오류 발생: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# 도구 호출 테스트
print("\n" + "="*50)
print("=== 대출 검색 테스트 (도구 호출) ===")
messages2 = [
    {"role": "user", "content": "의사 전용 대출 추천해줘"}
]
print("입력:", messages2[0]["content"])
print("\n응답:")
try:
    for chunk in stream_text(messages2):
        print(chunk, end='')
    print("\n\n✅ 테스트 성공!")
except Exception as e:
    print(f"\n\n❌ 오류 발생: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
