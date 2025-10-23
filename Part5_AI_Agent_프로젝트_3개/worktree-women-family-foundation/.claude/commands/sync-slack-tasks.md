# Slack Tasks Sync Command

어제 올라온 Slack 메시지를 스캔하여 중요한 태스크를 Notion DB에 자동으로 동기화합니다.

## 주요 기능

### 1. 채널 스캔 및 메시지 필터링
- 대상 채널: #engineering, #product, #support
- 어제 날짜의 메시지만 스캔
- 중요 메시지 기준:
  - 리액션 5개 이상
  - 긴급 키워드 포함: "urgent", "긴급", "asap", "장애"
  - @channel 또는 @here 멘션 포함
- ✅ 리액션이 있는 메시지는 제외 (이미 처리됨)

### 2. 자동 분류 시스템
**Priority 분류:**
- High: 긴급 키워드 포함 ("urgent", "긴급", "asap", "장애")
- Medium: 중요 키워드 포함 ("important", "중요", "blocker", "차단")
- Low: 그 외

**Category 분류:**
- Bug: "bug", "버그", "에러", "error", "장애"
- Feature: "feature", "기능", "개발", "추가"
- Improvement: "개선", "리팩토링", "refactor", "최적화"
- Other: 위 카테고리에 해당하지 않는 경우

### 3. Notion DB 연동
Notion 데이터베이스 URL: https://www.notion.so/koomook/d7ca1f0cc3c64dff9618932ee4ab95e7

생성되는 태스크 필드:
- **Title**: 메시지 첫 50자 요약
- **Category**: 자동 분류된 카테고리
- **Priority**: High/Medium/Low
- **Status**: 항상 "New"로 시작
- **Source Channel**: 메시지가 올라온 채널명
- **Source URL**: Slack 메시지 직접 링크
- **Content**: 메시지 전체 내용

### 4. Slack 피드백
각 처리된 메시지에:
- ✅ 리액션 추가 (중복 처리 방지)
- 스레드에 Notion 페이지 링크 답글

### 5. 일일 요약 보고서
#daily-standup 채널에 다음 내용 전송:
```
📊 **어제 Slack 태스크 동기화 결과**

**우선순위별:**
- 🔴 High: X개
- 🟡 Medium: Y개
- 🟢 Low: Z개

**카테고리별:**
- 🐛 Bug: A개
- ✨ Feature: B개
- 🔧 Improvement: C개
- 📌 Other: D개

**태스크 목록:**
[우선순위 High 태스크들...]
[우선순위 Medium 태스크들...]
[우선순위 Low 태스크들...]

📎 전체 보기: [Notion DB 링크]
```

## 실행 단계

1. **채널 정보 조회**: engineering, product, support 채널 ID 확인
2. **메시지 수집**: 각 채널에서 어제 메시지 가져오기
3. **필터링**: 중요도 기준으로 메시지 선별 (✅ 리액션 제외)
4. **분류**: Priority와 Category 자동 결정
5. **Notion DB 확인**: 데이터베이스 스키마 조회
6. **태스크 생성**: 필터링된 메시지를 Notion 페이지로 생성
7. **Slack 피드백**: 원본 메시지에 ✅ 리액션 + 스레드 답글
8. **보고서 전송**: daily-standup 채널에 요약 전송
