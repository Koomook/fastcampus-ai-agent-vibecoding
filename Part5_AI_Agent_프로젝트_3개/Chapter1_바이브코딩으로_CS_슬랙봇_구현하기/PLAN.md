# Slack Claude Bot 구현 계획서

## 목표
유저가 `@slackbot` 멘션으로 질문하면 Claude AI를 호출하여 스레드에 응답하는 슬랙봇을 구축합니다.
- 스레드 대화 맥락을 유지하여 연속적인 대화 지원
- Notion MCP를 통한 지식 검색 기능
- Google Cloud Run에 배포하여 서버리스로 운영

## 제약사항 및 원칙
- **단순함 우선**: 교육용 프로젝트이므로 프로덕션 레벨의 복잡한 아키텍처 지양
- **금지 사항**:
  - Pub-Sub 아키텍처
  - Secrets Manager (환경변수 `.env` 파일 사용)
  - Redis, Celery
  - Slack Socket Mode
- **허용 사항**:
  - 동기적 처리 (단순한 백그라운드 태스크는 가능)
  - FastAPI의 `BackgroundTasks` 또는 `asyncio.create_task`

## 기술 스택
- **언어**: Python 3.11+
- **웹 프레임워크**: FastAPI
- **LLM**: Claude Agent SDK (Haiku 4.5 - 비용 효율적)
- **패키지 관리**: uv (pip 금지)
- **컨테이너**: Docker
- **배포**: Google Cloud Run
- **Slack 라이브러리**: slack_sdk
- **MCP**: Notion MCP

## 아키텍처 개요

```
Slack Event Subscription → Cloud Run (FastAPI) → Slack Web API
                                ↓
                      Claude Agent SDK (Haiku 4.5)
                                ↓
                       Notion MCP (선택적 호출)
```

### 핵심 컴포넌트
1. **FastAPI 앱**: Slack 이벤트 수신 및 헬스체크 엔드포인트
2. **Slack 클라이언트**: `slack_sdk.WebClient`로 메시지 전송/업데이트
3. **Claude 서비스**: Agent SDK 래퍼, 대화 히스토리 관리
4. **Notion MCP**: Claude가 필요 시 호출하는 도구
5. **환경 설정**: `.env` 파일에서 비밀키 로드

## 요청 처리 흐름

1. **Slack 이벤트 수신**
   - FastAPI `/slack/events` 엔드포인트가 POST 요청 수신
   - Slack 서명 검증 (timestamp + HMAC)
   - 3초 이내에 HTTP 200 응답 반환

2. **URL 검증 처리** (초기 설정 시)
   - `type: url_verification` 이벤트 감지
   - `challenge` 파라미터 그대로 반환

3. **멘션 이벤트 처리**
   - HTTP 200 응답 후 백그라운드 태스크 시작
   - "Thinking..." 메시지를 스레드에 즉시 전송 (`chat.postMessage`)
   - 스레드 히스토리 조회 (`conversations.replies`, 최대 15개 메시지)
   - Claude Agent SDK 호출 (히스토리 + Notion MCP 도구)
   - Claude 응답 수신 후 "Thinking..." 메시지 업데이트 (`chat.update`)
   - MCP 도구 사용 시 별도 메시지로 호출 내용 표시

4. **에러 처리**
   - Claude/MCP 실패 시 사용자 친화적 에러 메시지 표시
   - 구조화된 로그 기록

## 단계별 구현 계획

### Phase 1: Hello Bot 배포 및 Event Subscriptions 설정

**목표**: Google Cloud Run에 간단한 "hello" 응답 봇을 배포하고 Slack Event Subscriptions 설정 완료

#### 구현 내용
1. **FastAPI 앱 스캐폴딩**
   - `/slack/events` POST 엔드포인트 (이벤트 수신)
   - `/health` GET 엔드포인트 (헬스체크)
   - Slack 서명 검증 미들웨어

2. **URL Verification Challenge 처리**
   - 참고: https://api.slack.com/events/url_verification
   - `type: url_verification` 이벤트 감지 시 `challenge` 반환
   - **주의사항**: JSON 형식으로 반환, Content-Type은 `application/json`

3. **Docker 컨테이너 구성**
   - `uv`를 사용한 의존성 관리
   - 참고: `uv` 공식 문서 - https://github.com/astral-sh/uv
   - 멀티스테이지 빌드 (빌드 → 런타임)
   - 포트 8080 노출 (Cloud Run 기본 포트)

4. **Cloud Run 배포**
   - 서비스 생성 및 환경변수 설정
   - 인증되지 않은 요청 허용 (Slack 웹훅용)
   - 최소 인스턴스 0, 최대 3 (비용 최적화)
   - 메모리 512MB

5. **Slack App 설정**
   - Slack App Manifest를 사용한 앱 생성 (manifest.json 제공)
   - Bot Token Scopes 설정:
     - `app_mentions:read` - 멘션 이벤트 수신
     - `chat:write` - 메시지 전송
     - `channels:history` - 채널 히스토리 조회
     - `groups:history` - 비공개 채널 히스토리 조회
     - `im:history` - DM 히스토리 조회
     - `mpim:history` - 그룹 DM 히스토리 조회
   - Event Subscriptions 설정:
     - Request URL: `https://<cloud-run-url>/slack/events`
     - Subscribe to bot events: `app_mention`
   - 워크스페이스에 앱 설치 후 Bot Token 획득

6. **기본 응답 구현**
   - `app_mention` 이벤트 수신 시 "Hello!" 정적 응답
   - 스레드에 응답하기 (`thread_ts` 사용)

#### 트러블슈팅 참고사항
- **Challenge 검증 실패**:
  - Slack은 JSON 본문으로 challenge를 전송
  - `application/json` Content-Type으로 응답 필요
  - 참고: https://stackoverflow.com/questions/72607095/

- **Slack 3초 타임아웃**:
  - 즉시 HTTP 200 응답 후 백그라운드 처리
  - 참고: https://dev.to/googlecloud/getting-around-api-timeouts-with-cloud-functions-and-cloud-pub-sub-47o3

- **Cloud Run Cold Start**:
  - 최소 인스턴스를 1로 설정하여 cold start 방지 가능 (비용 증가 트레이드오프)
  - 참고: https://cloud.google.com/run/docs/configuring/min-instances

#### 검증 방법
- Slack에서 `@slackbot hello` 멘션 시 "Hello!" 응답 확인
- 스레드에 답글이 달리는지 확인

---

### Phase 2: Claude Agent SDK 연동

**목표**: 유저의 질문에 Claude AI가 응답하도록 업그레이드

#### 구현 내용
1. **Claude Agent SDK 설치 및 설정**
   - 참고: https://github.com/anthropics/claude-agent-sdk-python
   - `uv add claude-agent-sdk` 로 설치
   - 환경변수에 `ANTHROPIC_API_KEY` 추가
   - 모델: `claude-haiku-4-5` (빠르고 비용 효율적)

2. **Claude 클라이언트 래퍼 작성**
   - 참고: https://github.com/anthropics/claude-agent-sdk-python/blob/main/README.md
   - `ClaudeSDKClient` 사용법 확인
   - 스트리밍 응답 처리 (`receive_response()` 메서드)
   - 대화 히스토리를 Claude 형식으로 변환

3. **스레드 컨텍스트 관리**
   - `conversations.replies` API 호출
   - 참고: https://api.slack.com/methods/conversations.replies
   - 최대 15개 메시지 조회 (rate limit 고려)
   - Slack 메시지 → Claude 메시지 형식 매핑:
     - 유저 메시지 → `user` role
     - 봇 메시지 → `assistant` role
   - **주의사항**: Rate limit (신규 앱 기준 1req/min, 15개 객체)
     - 429 에러 시 현재 메시지만 사용하도록 폴백
     - 로그에 경고 기록

4. **백그라운드 처리 흐름**
   - "Thinking..." 메시지 즉시 전송 (`chat.postMessage`)
   - 스레드 히스토리 조회
   - Claude Agent SDK 호출
   - 최종 응답으로 메시지 업데이트 (`chat.update`)
   - 메타데이터 로그 (소요시간, 토큰 수 등)

5. **응답 포맷팅**
   - Slack 마크다운 블록 사용
   - 섹션 구조:
     - 메인 답변
     - (옵션) 처리 시간, 모델 정보

6. **에러 처리**
   - Claude API 에러 시 사용자 친화적 메시지
   - 타임아웃 처리
   - 재시도 로직 (exponential backoff)

#### Claude Agent SDK 사용법 참고
```python
# 참고: https://github.com/anthropics/claude-agent-sdk-python/blob/main/README.md

# 기본 사용법
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write"],  # 필요한 도구만 허용
    max_turns=5,  # 최대 턴 수 제한
    permission_mode='acceptEdits'  # 자동 승인 모드
)

async with ClaudeSDKClient(options=options) as client:
    await client.query("Your question here")
    async for message in client.receive_response():
        # 메시지 처리
        pass
```

#### 검증 방법
- Slack에서 `@slackbot 2+2는?` 멘션 시 Claude의 답변 확인
- 여러 메시지를 연속으로 보내 컨텍스트가 유지되는지 확인
- 에러 시나리오 테스트 (잘못된 API 키 등)

---

### Phase 3: Notion MCP 연동

**목표**: Claude가 Notion 지식베이스를 검색하여 답변하도록 업그레이드

#### 구현 내용
1. **Notion MCP 설정**
   - Notion MCP 서버 선택 및 설치
   - 추천: 공식 Notion MCP 또는 커뮤니티 구현
   - Notion API 키 및 데이터베이스 ID 획득
   - 환경변수 추가: `NOTION_API_KEY`, `NOTION_DATABASE_ID`

2. **Claude Agent SDK에 MCP 도구 등록**
   - 참고: https://github.com/anthropics/claude-agent-sdk-python/blob/main/README.md
   - MCP 서버를 SDK에 연결하는 방법
   ```python
   # 참고 예시
   from claude_agent_sdk import create_sdk_mcp_server, ClaudeAgentOptions

   # MCP 서버 설정
   options = ClaudeAgentOptions(
       mcp_servers={
           "notion": {
               "type": "stdio",
               "command": "notion-mcp-server",  # 실제 명령어로 대체
               "args": []
           }
       },
       allowed_tools=["mcp__notion__search", "mcp__notion__get_page"]
   )
   ```

3. **도구 사용 가시성**
   - Claude가 MCP 도구 호출 시 스레드에 메시지 추가
   - 예: "Notion에서 '[검색어]' 검색 중..."
   - 도구 호출 결과를 포함한 답변 생성
   - 최종 응답에 "지식 출처" 섹션 추가:
     - Notion 페이지 제목 및 링크
     - "Notion MCP를 통해 검색됨" 표시

4. **Rate Limit 및 최적화**
   - MCP 호출을 1-2회로 제한
   - 동일 요청 내 중복 호출 방지 (인메모리 캐시)
   - 도구 사용 로그 기록 (비용 모니터링)

5. **메시지 포맷 개선**
   - Slack Block Kit 사용하여 시각적으로 개선
   - 섹션 구분:
     - 답변 본문
     - 지식 출처 (Notion 링크)
     - 메타정보 (모델, 처리 시간)

#### Notion 설정 가이드
- Notion Integration 생성: https://www.notion.so/my-integrations
- 데이터베이스에 Integration 연결 권한 부여
- API 키 및 데이터베이스 ID 확보

#### 검증 방법
- Notion 데이터베이스에 테스트 문서 추가
- Slack에서 `@slackbot [Notion에 있는 정보] 알려줘` 멘션
- 답변에 Notion 출처가 포함되는지 확인
- MCP 호출 로그 확인

---

## 공통 참고사항

### 환경변수 관리
`.env.example` 파일 제공:
```
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
ANTHROPIC_API_KEY=sk-ant-...
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...
```

### 로깅
- 구조화된 JSON 로깅
- 포함 항목: `request_id`, `thread_ts`, `user_id`, `latency`, `tool_calls`, `error`
- Cloud Run의 로그 탐색기에서 확인

### 로컬 개발
- ngrok을 사용한 Slack 터널링
- 참고: https://ngrok.com/docs
- 명령어: `ngrok http 8000`
- Slack Event Subscriptions URL을 ngrok URL로 업데이트

### 테스트
- 단위 테스트:
  - Slack 서명 검증
  - 이벤트 파싱
  - 메시지 포맷팅
- 통합 테스트:
  - Mock Slack 클라이언트
  - Mock Claude 응답
- 수동 테스트 체크리스트 제공

### Docker 설정
```dockerfile
# 참고용 구조
FROM python:3.11-slim

# uv 설치
RUN pip install uv

# 프로젝트 복사 및 의존성 설치
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# 앱 소스 복사
COPY . .

# 비루트 유저로 실행
USER nobody

# Cloud Run은 PORT 환경변수 사용
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Cloud Run 배포 명령어
```bash
# 참고: https://cloud.google.com/run/docs/deploying

# 이미지 빌드
docker build -t gcr.io/PROJECT_ID/slack-claude-bot .

# 이미지 푸시
docker push gcr.io/PROJECT_ID/slack-claude-bot

# Cloud Run 배포
gcloud run deploy slack-claude-bot \
  --image gcr.io/PROJECT_ID/slack-claude-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SLACK_BOT_TOKEN=... \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3
```

---

## Slack App Manifest

아래 JSON을 사용하여 Slack 앱을 빠르게 생성할 수 있습니다:

```json
{
  "display_information": {
    "name": "Claude CS Bot",
    "description": "AI-powered customer support bot using Claude",
    "background_color": "#2c2d30"
  },
  "features": {
    "bot_user": {
      "display_name": "Claude CS Bot",
      "always_online": true
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read",
        "chat:write",
        "channels:history",
        "groups:history",
        "im:history",
        "mpim:history"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "request_url": "https://YOUR-CLOUD-RUN-URL/slack/events",
      "bot_events": [
        "app_mention"
      ]
    },
    "org_deploy_enabled": false,
    "socket_mode_enabled": false,
    "token_rotation_enabled": false
  }
}
```

**사용 방법**:
1. https://api.slack.com/apps 접속
2. "Create New App" → "From an app manifest" 선택
3. 워크스페이스 선택 후 위 JSON 붙여넣기
4. `YOUR-CLOUD-RUN-URL`을 실제 URL로 변경
5. 앱 생성 후 "Install to Workspace"

---

## 핵심 트러블슈팅 가이드

### 1. Slack Event Subscriptions Challenge 실패
**증상**: "Your URL didn't respond with the value of the challenge parameter"

**원인**:
- JSON 형식이 아닌 plain text로 응답
- Content-Type이 `application/json`이 아님
- 서명 검증 실패

**해결책**:
```python
# 참고: https://api.slack.com/events/url_verification
if event_data.get("type") == "url_verification":
    return JSONResponse(content={"challenge": event_data["challenge"]})
```

### 2. Slack 3초 타임아웃 초과
**증상**: Slack에서 "operation_timeout" 에러

**해결책**:
- 즉시 HTTP 200 반환
- 백그라운드 태스크로 처리
- "Thinking..." 메시지 먼저 전송

```python
# FastAPI BackgroundTasks 사용
@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks):
    # 즉시 응답
    background_tasks.add_task(process_mention, event_data)
    return Response(status_code=200)
```

### 3. conversations.replies Rate Limit
**증상**: 429 Too Many Requests

**해결책**:
- Rate limit: 1 req/min (신규 앱 기준)
- 에러 발생 시 현재 메시지만 사용하도록 폴백
- 로그에 경고 기록
- Semaphore로 동시 요청 제한

```python
# 참고용 폴백 로직
try:
    history = slack_client.conversations_replies(
        channel=channel_id,
        ts=thread_ts,
        limit=15
    )
except SlackApiError as e:
    if e.response["error"] == "rate_limited":
        logger.warning("Rate limited, using current message only")
        history = [current_message]
```

### 4. Cloud Run Cold Start 지연
**증상**: 첫 요청이 느림

**해결책**:
- 최소 인스턴스를 1로 설정 (비용 증가)
- 또는 "Thinking..." 메시지로 사용자 경험 개선
- Cloud Run 시작 시간 최적화 (이미지 크기 감소)

---

## 참고 자료

### Claude Agent SDK
- GitHub: https://github.com/anthropics/claude-agent-sdk-python
- 공식 문서: https://docs.claude.com/en/api/agent-sdk/python
- Context7 문서: `/anthropics/claude-agent-sdk-python`

### Slack API
- Event Subscriptions: https://api.slack.com/events-api
- conversations.replies: https://api.slack.com/methods/conversations.replies
- Block Kit: https://api.slack.com/block-kit
- Slack Python SDK: https://slack.dev/python-slack-sdk/

### Google Cloud Run
- 공식 문서: https://cloud.google.com/run/docs
- 타임아웃 설정: https://cloud.google.com/run/docs/configuring/request-timeout
- 배포 가이드: https://cloud.google.com/run/docs/deploying

### 패키지 관리
- uv 문서: https://github.com/astral-sh/uv
- uv 사용법: https://docs.astral.sh/uv/

### 개발 도구
- ngrok: https://ngrok.com/docs
- FastAPI: https://fastapi.tiangolo.com/

---

## 성공 기준

### Phase 1 완료
- ✅ Cloud Run에 배포 완료
- ✅ Slack Event Subscriptions URL 검증 통과
- ✅ `@slackbot` 멘션 시 "Hello!" 응답

### Phase 2 완료
- ✅ Claude AI 응답 작동
- ✅ 스레드 컨텍스트 유지 확인
- ✅ "Thinking..." → 최종 답변 플로우 작동
- ✅ 에러 핸들링 테스트 완료

### Phase 3 완료
- ✅ Notion MCP 연동 완료
- ✅ Claude가 Notion 검색 수행
- ✅ 답변에 Notion 출처 표시
- ✅ 도구 호출 내용이 스레드에 표시

---

## 다음 단계 (선택사항)

교육 범위를 넘어서는 개선사항:
- 멀티턴 대화 상태 관리 (DB 저장)
- 사용자별 설정 (Notion 검색 on/off)
- 메트릭 수집 및 모니터링
- CI/CD 파이프라인 (GitHub Actions)
- A/B 테스트 (다양한 프롬프트)
- 비용 모니터링 대시보드
