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

# Clip 1 발표 스크립트: Context/Prompt Engineering 이해하기

## 🎬 오프닝 (30초)

"안녕하세요. 이번 클립에서는 Context Engineering에 대해 알아보겠습니다.

여러분, 클로드와 긴 대화를 하다 보면 갑자기 이전에 했던 이야기를 까먹거나, 엉뚱한 답변을 하는 경험 해보셨나요? 이게 바로 오늘 다룰 **Context Rot** 현상입니다."

---

## 📚 섹션 1: Context Engineering이란? (2분)

"먼저 Prompt Engineering과 Context Engineering의 차이를 보겠습니다.

**Prompt Engineering**은 '좋은 질문 하나'를 만드는 것입니다.
**Context Engineering**은 '대화 전체'를 관리하는 것이죠.

[화면: 비교 표 보여주기]

바이브코딩에서는 단발성 질문이 아니라 긴 대화를 하게 됩니다. 그래서 Context Engineering이 훨씬 중요합니다."

---

## 🔍 섹션 2: Context Rot 문제 (2분)

"LLM은 인간처럼 집중력을 잃습니다.

컨텍스트가 길어질수록 - 즉, 대화가 길어질수록 - 이전 정보를 놓치기 시작합니다. 이게 Context Rot이에요.

[화면: Mermaid 다이어그램]

왜 이런 일이 생길까요?

트랜스포머 아키텍처의 한계입니다. 모든 토큰이 다른 모든 토큰에 주의를 기울여야 하는데, 토큰이 많아질수록 주의가 분산되는 거죠.

n개 토큰이면 n² 관계가 생깁니다. 엄청난 복잡도죠."

---

## 💡 섹션 3: 효과적인 프롬프트 구조 (3분)

"그럼 어떻게 해야 할까요?

첫 번째는 **적절한 추상화 수준**입니다.

[화면: 3가지 예시]

너무 구체적이면? 'Python FastAPI만 쓰고, 비동기만 쓰고...' 이러면 나중에 다른 프레임워크가 필요할 때 막힙니다.

너무 추상적이면? '유용한 코딩 어시스턴트입니다' 이건 아무 정보가 없죠.

**적절한 높이**는 이겁니다:
'소프트웨어 개발 어시스턴트입니다. 사용자 요구사항에 맞는 기술 스택을 선택하고, 모범 사례를 따르는 코드를 작성합니다.'

유연하면서도 명확합니다."

---

## 🧹 섹션 4: 컨텍스트 정리 전략 (2분)

"두 번째는 **컨텍스트 정리**입니다.

언제 정리해야 할까요?

[화면: 정리 타이밍]

1. 단계 완료 후
2. 에러 해결 후
3. 방향 전환 시

어떻게 정리할까요?

'✅ 슬랙 이벤트 수신 구현 완료
 ✅ OpenAI 연동 완료

 다음 단계: GCP Cloud Run 배포
 이전 단계의 에러 로그는 제외하고 진행해줘.'

이렇게 명시적으로 '완료' 선언하고, '이제 다음'이라고 말하는 겁니다."

---

## 🎯 섹션 5: 실전 팁 (2분)

"실전에서 바로 쓸 수 있는 팁입니다.

**나쁜 프롬프트:**
'슬랙봇 만들어줘'

**좋은 프롬프트:**
[화면: 구조화된 예시]

보세요. 기술 스택, 기능, 배포 환경, 프로젝트 구조까지 다 명시했습니다.

이게 Context Engineering입니다. 클로드가 성공할 수 있는 모든 정보를 미리 주는 거예요."

---

## 🎓 마무리 (30초)

"정리하겠습니다.

1. **Context = 프롬프트 이상**: 전체 대화 상태 관리
2. **Context Rot 인식**: 길어질수록 LLM 성능 저하
3. **적절한 추상화**: 유연하면서도 명확하게
4. **정기적 정리**: 단계 완료 시마다 명시적 선언

다음 클립에서는 이걸 실전에서 어떻게 쓰는지, 'AI의 PM이 되는 법'을 알아보겠습니다.

감사합니다!"

---

## 📝 발표 노트

**시간 배분:**
- 오프닝: 30초
- 섹션 1-5: 11분
- 마무리: 30초
- **총 12분**

**강조 포인트:**
- Context Rot은 실제로 존재하는 문제
- 추상화 수준의 예시 대비
- 명시적 컨텍스트 정리의 중요성

**시각 자료:**
- 비교 표 (Prompt vs Context Engineering)
- Mermaid 다이어그램 (Context Rot)
- Before/After 프롬프트 예시

**톤:**
- 친근하고 대화체
- 기술적이지만 쉽게 설명
- 실전 예시로 공감대 형성


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
