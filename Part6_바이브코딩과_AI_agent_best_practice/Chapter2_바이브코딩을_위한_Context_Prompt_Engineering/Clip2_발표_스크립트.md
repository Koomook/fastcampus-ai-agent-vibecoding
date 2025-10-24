---
## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent

---

# Clip 2 발표 스크립트: AI의 PM이 되기

## 🎬 오프닝 (30초)

"안녕하세요. 이번 클립은 Anthropic의 Erik Schulntz가 발표한 'Vibe coding in prod'를 바탕으로 구성했습니다.

여러분, 바이브코딩이 뭘까요?
Cursor 쓰는 거? Copilot 쓰는 거?

아닙니다. Andre Karpathy는 이렇게 말했죠.

'**코드가 존재한다는 것조차 잊는 것**'

오늘은 이게 무슨 뜻인지, 그리고 프로덕션에서 어떻게 안전하게 할 수 있는지 알아보겠습니다."

---

## 📊 섹션 1: 바이브코딩의 진짜 의미 (2분)

"먼저 일반 AI 코딩과 바이브코딩의 차이입니다.

[화면: 비교 표]

**Cursor나 Copilot**: 한 줄 쓰고, 리뷰하고, 또 한 줄 쓰고... 타이트한 피드백 루프입니다.

**바이브코딩**: 기능 전체를 맡기고, 결과물만 봅니다.

왜 이게 중요할까요?

[화면: 기하급수 그래프]

AI가 할 수 있는 작업 길이가 **7개월마다 2배**씩 늘고 있습니다.

지금은 1시간짜리 작업이지만, 1년 후엔? 1일짜리 작업입니다.
2년 후엔? 1주일짜리 작업이죠.

그때도 모든 코드를 다 리뷰할 건가요? 불가능합니다.
**우리가 병목**이 되는 겁니다."

---

## 🎯 섹션 2: AI의 PM이 되기 (3분)

"해법은 간단합니다. 우리가 **클로드의 PM**이 되는 겁니다.

'Ask not what Claude can do for you, but what you can do for Claude.'

[화면: 신입 직원 비유]

신입 직원한테 '이 버그 고쳐줘'만 하면 될까요? 안 됩니다.

- 코드베이스 투어
- 요구사항 명세
- 제약사항
- 참고 코드

이 모든 걸 줘야 합니다.

클로드도 마찬가지입니다!

[화면: Before/After 예시]

나쁜 예: '슬랙봇 만들어줘'

좋은 예:
```
목표: 슬랙봇 구현
기술 스택: Python, FastAPI, Slack Bolt
프로젝트 구조: /app/slack_bot.py, /app/llm.py
참고 코드: /examples/discord_bot.py 패턴 따르기
요구사항: 1) 멘션 이벤트 수신, 2) OpenAI 답변...
```

실전에서는 이런 프롬프트를 준비하는 데 **15-20분** 걸립니다.

하지만 이 15분 투자로 클로드는 거의 실패하지 않습니다."

---

## 🍃 섹션 3: Leaf Node 전략 (3분)

"하지만 모든 코드를 바이브코딩하면 안 됩니다.

[화면: 트리 구조 다이어그램]

이 그림을 보세요.

**빨간색**: 핵심 아키텍처 (Core)
**노란색**: 중간 레이어 (Branch)
**초록색**: 기능 끝단 (Leaf Node)

바이브코딩은 **초록색**, 즉 Leaf Node에만 하세요.

왜냐면 Leaf Node는:
- ✅ 다른 코드가 의존하지 않음
- ✅ 자주 변경되지 않음
- ✅ Tech Debt가 있어도 전파 안 됨

[화면: 코드 예시]

**바이브코딩 X:**
```python
# core/database.py - 모든 곳에서 사용
class DatabaseConnection:
    ...
```

**바이브코딩 O:**
```python
# features/export_excel.py - 아무도 의존 안 함
def export_users_to_excel():
    ...
```

현재 문제는 Tech Debt를 코드 안 읽고 검증할 방법이 없습니다.
그래서 Tech Debt가 허용되는 Leaf Node에만 집중하는 겁니다."

---

## ✅ 섹션 4: 검증 가능한 설계 (2분)

"핵심 질문입니다.

**'코드를 읽지 않고 이 기능이 올바른지 어떻게 알 수 있나?'**

세 가지 전략입니다.

**1) 명확한 입력/출력**
```python
def process(data: InputSchema) -> OutputSchema:
    ...
```
입력과 출력만 보고 검증 가능합니다.

**2) End-to-End 테스트**
```python
def test_user_registration():
    response = client.post('/api/register', ...)
    assert response.status_code == 201
```
구현 몰라도 이 테스트만 통과하면 OK.

**3) Stress Test**
```python
# 1000개 요청 보내서 99% 성공해야 함
```
안정성을 숫자로 검증합니다.

Anthropic은 이 방법으로 **22,000줄 변경**을 프로덕션에 병합했습니다.
2주 걸릴 일을 1일 만에 끝냈죠."

---

## 📈 섹션 5: 학습과 성장 (2분)

"'코딩 안 하면 어떻게 배우나요?'

좋은 질문입니다.

[화면: 부정적/긍정적 시각]

**부정적**: 옛날 교수님들도 그랬죠. '요즘 애들은 어셈블리 손으로 안 써서 못해'

**긍정적**:
1) **더 빠른 학습** - 클로드한테 물어볼 수 있습니다
   'Claude, 이 라이브러리 왜 선택했어?'

2) **더 많은 시도** - 2년에 1번 → 6개월에 1번 아키텍처 결정
   → **4배 빠르게 배움**

게으른 사람은 배우지 않겠지만,
성장하려는 사람은 오히려 4배 빠르게 성장합니다."

---

## 🎓 마무리 (1분)

"정리하겠습니다.

[화면: 체크리스트]

✅ **Claude의 PM이 되어라**
   → 15-20분 프롬프트 준비

✅ **Leaf Node에 집중하라**
   → 핵심 아키텍처는 직접 작성

✅ **검증 가능하게 설계하라**
   → 입력/출력, E2E 테스트, Stress Test

✅ **기하급수를 기억하라**
   → 7개월마다 2배 성장
   → 지금 안 배우면 미래에 병목

마지막으로 Erik의 말을 인용하겠습니다.

'Machines of Loving Grace는 SF가 아닙니다. **제품 로드맵**입니다.'

기하급수의 세계에서는 상상보다 빠르게 미래가 옵니다.

바이브코딩, 지금부터 연습하세요.

감사합니다!"

---

## 📝 발표 노트

**시간 배분:**
- 오프닝: 30초
- 섹션 1-5: 12분
- 마무리: 1분
- **총 13분 30초**

**강조 포인트:**
- 기하급수의 위력 (7개월마다 2배)
- PM 역할의 구체성 (15-20분 준비)
- Leaf Node vs Core 명확한 구분
- 22,000줄 실제 사례

**시각 자료:**
- 비교 표 (AI 코딩 vs 바이브코딩)
- 기하급수 그래프
- 트리 구조 다이어그램 (Leaf Node)
- 코드 예시 (Core vs Leaf)

**톤:**
- 에너지 있고 설득력 있게
- 실제 사례로 신뢰 구축
- 미래지향적이지만 현실적

**인용구 활용:**
- Andre Karpathy: "코드가 존재한다는 것조차 잊는 것"
- Erik Schulntz: "Ask not what Claude can do for you..."
- Dario Amodei: "Machines of Loving Grace는 제품 로드맵"

**데모/실습 제안:**
- 15-20분 프롬프트 준비 과정 실시간 시연
- Leaf Node 식별 연습
- 프롬프트 템플릿 활용 예시


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
