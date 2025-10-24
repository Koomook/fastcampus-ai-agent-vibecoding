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

# Clip 2: 고급 자동화 - 스마트 분석과 슬래시 커맨드

## 📋 학습 개요

Clip 1에서 기본적인 Slack-Notion 자동화를 구현했다면, 이제 **실무 수준의 고급 자동화**를 만들어봅니다. 메시지 분석, 자동 분류, 그리고 반복 작업을 슬래시 커맨드로 만드는 방법을 학습합니다.

### 🎯 학습 목표

- 조건부 로직을 포함한 복잡한 자동화 프롬프트 작성
- 자연어 처리를 활용한 메시지 분류 및 우선순위 추출
- 슬래시 커맨드로 반복 작업 자동화

---

## 🧠 STEP 1: 스마트 분석 프롬프트

### 1-1. 고급 자동화 프롬프트: 스마트 분석 및 분류

더 정교한 분석을 위한 프롬프트입니다. Clip 1에서 배운 기본 자동화에 **조건부 로직**과 **자연어 처리**를 추가합니다.

#### 프롬프트 전문

```
Slack #product-feedback 채널의 최근 24시간 메시지를 분석해서 Notion 태스크로 등록해줘.

필터링 조건 (하나라도 만족하면 선택):
- 리액션 3개 이상 또는 스레드 답글 5개 이상
- @channel, @here 멘션 포함
- ✅ 리액션이 이미 있는 메시지는 제외 (중복 방지)

카테고리 자동 분류:
- 🐛 Bug: "버그", "오류", "안됨" 키워드
- ✨ Feature: "기능", "추가", "만들어주세요" 키워드
- 🔧 Improvement: "개선", "최적화" 키워드

우선순위 자동 추출:
- High: "urgent", "긴급", "asap" 키워드
- Medium: "important", "중요" 키워드
- Low: 그 외

Notion DB (https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7)에 생성:
- Title: 메시지 요약 (50자 이내)
- Category, Priority, Status: "New"
- Source Channel, Source URL

완료 후 원본 메시지에 ✅ 리액션 추가하고 스레드에 Notion 링크 답글 작성
```

#### 실행 결과 예시

```
✅ 작업 완료!

📊 분석 결과:
- 총 메시지: 47개
- 조건 만족: 12개
- 카테고리 분류:
  * 🐛 Bug: 4개
  * ✨ Feature: 6개
  * 🔧 Improvement: 2개

📝 Notion에 생성된 태스크:

1. [Bug] 로그인 후 프로필 이미지 안 보임
   Priority: High | Assignee: @개발자A (예시)
   URL: https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7?pvs=...

2. [Feature] 다크 모드 지원 요청
   Priority: Medium | Assignee: -
   URL: https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7?pvs=...

3. [Feature] 검색 결과 필터링 기능
   Priority: Low | Assignee: @개발자B (예시)
   URL: https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7?pvs=...

...

✅ 12개 메시지에 체크 리액션 추가 완료
✅ 12개 스레드에 알림 메시지 작성 완료
```

> **참고**: 위 예시의 채널명(#product-feedback)과 사용자명(@개발자A, @개발자B)은 설명을 위한 가상의 데이터입니다. 실제 실행 시에는 여러분의 Slack 워크스페이스에 있는 실제 채널과 사용자를 사용하세요.

### 1-2. 프롬프트 설계 원칙

이 프롬프트가 효과적인 이유:

#### ① 단계별 명확한 지시

각 단계가 순서대로 나열되어 있어 Claude가 작업을 체계적으로 수행합니다:
- 1단계: 데이터 수집
- 2단계: 필터링
- 3단계: 분류
- 4단계: 정보 추출
- 5단계: 저장
- 6단계: 피드백

#### ② 구체적인 조건 명시

모호한 표현 대신 명확한 기준을 제시:
- ❌ "중요한 메시지만"
- ✅ "리액션이 3개 이상이거나 스레드 답글이 5개 이상"

#### ③ 예시 키워드 제공

분류 기준에 실제 키워드 예시를 포함:
- Bug: "버그", "오류", "안됨", "작동하지 않음"
- Feature: "기능", "추가", "만들어주세요"

#### ④ 피드백 루프 구현

작업 완료 후 Slack에 알림을 보내 투명성 확보:
- 원본 메시지에 리액션
- 스레드에 Notion 링크 공유


---

## 🔄 STEP 2: 반복 자동화 - 슬래시 커맨드 만들기

### 2-1. 슬래시 커맨드란?

슬래시 커맨드는 반복적인 작업을 **한 줄 명령어**로 실행할 수 있게 해주는 기능입니다.

**예시**:
```bash
# 긴 프롬프트 대신
/sync-slack-tasks

# 이 한 줄로 자동화 실행!
```

### 2-2. 슬래시 커맨드 생성 프롬프트

```
/sync-slack-tasks 슬래시 커맨드 만들어줘:

#engineering, #product, #support 채널의 어제 메시지 스캔해서 중요한 것만 선별:
- 리액션 5개 이상 또는 긴급 키워드("urgent", "긴급", "asap", "장애")
- @channel/@here 멘션 포함
- ✅ 리액션 있는 메시지는 제외 (중복 방지)

자동 분류:
- Priority: High(긴급 키워드), Medium(중요 키워드), Low(나머지)
- Category: Bug, Feature, Improvement 등 키워드 기반

Notion DB (https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7)에 생성:
- Title: 메시지 요약 (50자)
- Category, Priority, Status: "New"
- Source Channel, Source URL

각 메시지에 ✅ 리액션 + 스레드에 Notion 링크 답글

#daily-standup에 요약 보고서 전송:
- 우선순위별 개수 및 태스크 목록
- 카테고리별 분포
- Notion DB 링크

```

### 2-3. 슬래시 커맨드 실행

Claude Code 대화창에서 슬래시 커맨드를 실행:

```bash
# 대화창에서
/sync-slack-tasks
```

**실행 결과**:
```
🔄 작업 시작...

📥 메시지 수집 중...
- #engineering: 23개 메시지
- #product: 15개 메시지
- #support: 31개 메시지

📬 #daily-standup에 보고서 전송 완료

✅ 모든 작업 완료!
```

### 2-4. 슬래시 커맨드 수정하기

생성된 슬래시 커맨드를 수정할 때는 **의도하지 않은 변경을 방지**하는 것이 중요합니다. 단순히 "수정해줘"라고 요청하면 요청한 내용 외에 다른 부분도 변경될 수 있습니다.

#### 문제점: 일반적인 수정 요청

```
/sync-slack-tasks 커맨드를 수정해줘.
#customer-feedback 채널도 추가하고, 리액션 기준을 3개 이상으로 낮춰줘.
```

**위 방식의 리스크**:
- ❌ 요청하지 않은 다른 워크플로우도 변경될 수 있음
- ❌ 기존 동작이 의도치 않게 수정될 위험
- ❌ 변경 전후 비교가 어려움

#### 해결책: 안전한 수정 프로세스

**`/update-slash-command`** 슬래시 커맨드를 만들어 체계적으로 수정합니다.

---

### 2-5. `/update-slash-command` 슬래시 커맨드 만들기

#### Step 1: 슬래시 커맨드 생성 프롬프트

```
/update-slash-command 슬래시 커맨드 만들어줘:

기존 슬래시 커맨드를 안전하게 수정하는 대화형 워크플로우:

1. 현재 등록된 슬래시 커맨드 목록 보여주고 수정할 커맨드 선택 받기
2. 선택한 커맨드의 현재 내용 분석해서 요약 보여주기
3. 사용자에게 수정 내용 물어보기
4. 변경 전/후를 나란히 비교하며 검토 (변경된 부분 표시)
5. 사용자 승인 받기 (yes면 저장, no면 3단계로)
6. 저장 완료 후 변경 로그와 테스트 방법 안내

검토 시 예시 형식:
🔴 변경 전: 리액션 5개 이상
🟢 변경 후: 리액션 3개 이상 [변경됨]
```

#### Step 2: `/update-slash-command` 실행 예시

```bash
# Claude Code 대화창에서
/update-slash-command
```

**실행 결과**:

```
🔧 슬래시 커맨드 수정 도구

📋 현재 등록된 슬래시 커맨드:
1. /sync-slack-tasks - Slack 메시지를 Notion 태스크로 동기화
2. /weekly-report - 주간 리포트 생성
3. /deploy-check - 배포 전 체크리스트 실행

❓ 어떤 커맨드를 수정하시겠습니까? (번호 입력)
> 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 현재 /sync-slack-tasks 워크플로우
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

주요 기능:
- 대상 채널: #engineering, #product, #support
- 필터 기준: 리액션 5개 이상 또는 긴급 키워드
- 저장 위치: Notion "Daily Tasks" DB
- 보고서: #daily-standup 채널

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ 어떤 부분을 수정하시겠습니까?
> #customer-feedback 채널 추가하고, 리액션 기준을 3개로 낮춰줘

🔄 수정 내용을 분석 중...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 변경 사항 검토
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[변경 전후 비교 출력...]

⚠️  이대로 수정할까요? (yes/no)
> yes

✅ 슬래시 커맨드 업데이트 완료!

📝 변경 로그:
- 채널 추가: #customer-feedback
- 리액션 기준: 5개 → 3개

🧪 테스트 방법:
/sync-slack-tasks

테스트 후 문제가 있으면 /update-slash-command로 다시 수정할 수 있습니다.
```

---

### 2-6. `/update-slash-command`의 장점

#### ✅ 안전성 보장

1. **변경 전 확인**: 수정 전 전체 워크플로우를 보여줌
2. **차이점 하이라이트**: 변경된 부분만 명확히 표시
3. **승인 단계**: 사용자가 최종 확인 후 적용

#### ✅ 추적 가능성

- 변경 로그 자동 생성
- 어떤 부분이 왜 변경되었는지 기록
- 문제 발생 시 롤백 가능

#### ✅ 학습 효과

- 슬래시 커맨드의 내부 구조 이해
- 체계적인 변경 관리 프로세스 학습
- AI 에이전트 개발 시 베스트 프랙티스 체험

---

## 📖 참고 자료

### 공식 문서
- [Claude Code Slash Commands 가이드](https://docs.claude.com/ko/docs/claude-code/slash-commands)


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
