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

# Clip 1: 클로드코드로 자동화하기 - 슬랙 메시지 읽고 Notion에 태스크 저장

## 📋 학습 개요

이 강의에서는 **Notion과 Slack MCP 서버**를 연결하여 실무 자동화 워크플로우를 구축합니다. Slack 채널의 중요한 메시지를 자동으로 감지하고, 이를 Notion 데이터베이스에 태스크로 저장하는 완전한 시스템을 만들어봅니다.

바이브 코딩을 하기 전에, Claude Code라는 에이전트를 잘 활용함으로써 AI 에이전트가 어떻게 동작하는 것인지 감을 잡는 것이 목표입니다.

### 🎯 학습 목표

- Notion MCP 서버를 프로젝트 범위로 연결하는 방법 익히기
- Slack MCP 서버 설정 및 Slack App 생성 방법 이해
- 두 MCP 서버를 연동한 자동화 워크플로우 구축
- Claude Code 프롬프트로 실무 자동화 구현

### 💡 실무 활용 사례

- 팀 채널의 긴급 요청을 자동으로 태스크화
- 고객 피드백을 자동으로 제품 백로그에 추가
- 버그 리포트를 이슈 트래커에 자동 등록
- 회의 액션 아이템을 자동으로 추출 및 할당

### 🏗️ 시스템 아키텍처

```mermaid
graph LR
    A[Slack Channel] -->|read| B[Slack MCP Server]
    B --> C[Claude Code]
    C -->|analyze & create| D[Notion MCP Server]
    D -->|write| E[Notion Database]

    C -->|notify| F[Slack Thread]

    style B fill:#4A154B
    style D fill:#000000
    style C fill:#4ECDC4
```

**처리 흐름**:
1. Slack MCP로 채널 메시지 읽기
2. Claude가 메시지 분석 및 태스크 여부 판단
3. Notion MCP로 데이터베이스에 페이지 생성
4. Slack에 완료 알림 전송

---

## 🗂️ STEP 1: Notion MCP 서버 연결하기

Notion MCP 서버는 Notion이 공식으로 호스팅하는 원격 MCP 서버로, Claude Code가 Notion 워크스페이스와 바로 상호작용할 수 있게 해줍니다.

### 1-1. MCP Scope 이해하기

MCP 서버를 추가하기 전에, **Scope**(범위)의 개념을 이해하는 것이 중요합니다.

| Scope | 저장 위치 | 사용 범위 | 팀 공유 |
|-------|----------|----------|---------|
| **Local** (기본) | 현재 프로젝트만 | 나만 사용 | ❌ |
| **Project** | `.mcp.json` (Git 추적) | 프로젝트 팀원 모두 | ✅ |
| **User** | 사용자 홈 디렉토리 | 내 모든 프로젝트 | ❌ |

이 강의에서는 **팀 협업을 위해 Project Scope**를 사용합니다.

### 1-2. Notion MCP 설치 (한 줄로 끝!)

#### ① 프로젝트 디렉토리로 이동

터미널에서 프로젝트 루트로 이동:

```bash
cd /path/to/your/project
```

#### ② Notion MCP 추가 명령어 실행

**단 한 줄의 명령어로 설치 완료:**

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp -s project
```

**명령어 설명**:
- `claude mcp add`: MCP 서버를 추가하는 명령어
- `--transport http`: HTTP 프로토콜 사용 (원격 서버 연결용)
  - 💡 SSE(Server-Sent Events)도 지원하지만, HTTP가 더 안정적입니다
- `notion`: MCP 서버 이름 (나중에 참조할 식별자)
- `https://mcp.notion.com/mcp`: Notion 공식 MCP 서버 URL
- `-s project`: 프로젝트 레벨 스코프로 설정 (`.mcp.json`에 저장)

#### ③ 생성된 `.mcp.json` 확인

프로젝트 루트에 자동 생성된 파일:

```json
{
  "mcpServers": {
    "notion": {
      "transport": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

✅ 이 파일은 Git에 커밋하여 팀원과 공유할 수 있습니다!

#### ④ OAuth 인증 진행

Claude Code를 재시작한 후, 대화창에서:

```
/mcp
```

명령어를 실행 후 notion mcp auth를 진행:
1. 브라우저가 자동으로 열림
2. Notion 로그인 페이지로 이동
3. 워크스페이스 선택 및 권한 승인
4. 인증 완료 후 자동으로 토큰 저장

⚠️ **중요**: 인증 토큰은 안전하게 암호화되어 저장되며, Git에 포함되지 않습니다.

### 1-3. Notion MCP 연결 테스트

Claude Code 대화창을 열고 간단한 테스트를 진행합니다:

```
Notion 워크스페이스에 있는 모든 페이지를 리스팅해줘
```

**예상 출력**:
```
✅ Found 5 pages:
1. Project Roadmap (Database)
2. Meeting Notes (Page)
3. Team Wiki (Page)
4. Sprint Planning (Database)
5. Personal Tasks (Database)
```

워크스페이스의 페이지 목록이 표시되면 Notion MCP 연결 완료! 🎉

---

## 📱 STEP 2: Slack MCP 서버 연결하기

Slack MCP 서버는 Claude Code가 Slack 워크스페이스의 메시지를 읽고, 전송하고, 리액션을 추가할 수 있게 해줍니다.

### 2-1. Slack App 생성

Slack App을 생성하는 방법은 두 가지가 있습니다: **매니페스트를 사용한 빠른 생성(권장)** 또는 수동 생성입니다.

#### 방법 1: App Manifest로 한 번에 생성하기 (권장) ⚡

App Manifest를 사용하면 모든 설정을 JSON으로 한 번에 정의하여 빠르게 앱을 생성할 수 있습니다.

**① Slack API 페이지 접속**

1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. **"Create New App"** 버튼 클릭
3. **"From an app manifest"** 선택
4. 워크스페이스 선택 후 **"Next"** 클릭

**② 매니페스트 입력**

아래 JSON 매니페스트를 복사하여 붙여넣기:

```json
{
  "display_information": {
    "name": "Claude Code Bot",
    "description": "Slack MCP Server for Claude Code automation",
    "background_color": "#4A154B"
  },
  "features": {
    "bot_user": {
      "display_name": "Claude Code Bot",
      "always_online": true
    }
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "channels:history",
        "channels:read",
        "chat:write",
        "reactions:write",
        "users:read",
        "users.profile:read"
      ]
    }
  },
  "settings": {
    "org_deploy_enabled": false,
    "socket_mode_enabled": false,
    "token_rotation_enabled": false
  }
}
```

**매니페스트 설명**:
- `display_information`: 앱 이름, 설명, 색상
- `features.bot_user`: Bot 사용자 설정
- `oauth_config.scopes.bot`: 필요한 권한 스코프
  - `channels:history`: 공개 채널 메시지 히스토리 읽기
  - `channels:read`: 공개 채널 정보 조회
  - `chat:write`: 메시지 전송
  - `reactions:write`: 리액션 추가
  - `users:read`: 사용자 기본 정보 조회
  - `users.profile:read`: 사용자 프로필 상세 정보

**③ 앱 생성**

1. **"Next"** 버튼 클릭
2. 설정 내용 확인
3. **"Create"** 버튼 클릭

---

#### 방법 2: 수동으로 생성하기

매니페스트를 사용하지 않고 직접 설정하는 방법입니다.

**① Slack API 페이지 접속**

1. [https://api.slack.com/apps](https://api.slack.com/apps) 접속
2. **"Create New App"** 버튼 클릭
3. **"From scratch"** 선택

**② App 기본 정보 입력**

```
App Name: Claude Code Bot
Pick a workspace: [당신의 워크스페이스 선택]
```

**"Create App"** 버튼 클릭!

**③ Bot Token Scopes 추가**

1. 왼쪽 메뉴에서 **"OAuth & Permissions"** 클릭
2. **"Scopes" > "Bot Token Scopes"** 섹션으로 스크롤
3. 다음 스코프들을 **"Add an OAuth Scope"** 버튼으로 추가:

| Scope | 설명 | 사용 예시 |
|-------|------|----------|
| `channels:history` | 공개 채널의 메시지 히스토리 읽기 | 과거 메시지 조회 |
| `channels:read` | 공개 채널 정보 조회 | 채널 목록 가져오기 |
| `chat:write` | 메시지 전송 | 알림 메시지 보내기 |
| `reactions:write` | 리액션 추가 | ✅ 리액션으로 완료 표시 |
| `users:read` | 사용자 기본 정보 조회 | 메시지 작성자 정보 |
| `users.profile:read` | 사용자 프로필 상세 정보 | 이메일, 이름 가져오기 |

---

### 2-2. App 설치 및 Bot Token 획득

#### ① Workspace에 App 설치

1. 같은 페이지 상단의 **"Install to Workspace"** 버튼 클릭
2. 권한 요청 화면에서 내용 확인
3. **"Allow"** 버튼 클릭

#### ② Bot User OAuth Token 복사

설치 완료 후 페이지 상단에 표시되는 토큰 복사:

```
Bot User OAuth Token
xoxb-your-bot-token-here
```

⚠️ **주의**: 이 토큰은 안전한 곳에 보관하세요! (영상에 나온 토큰은 삭제되었습니다)

### 2-3. Team ID 확인 (필수)

Slack MCP 서버를 사용하려면 워크스페이스의 **Team ID**가 필요합니다. 다음 방법 중 하나를 선택하세요.

#### 방법 1: Claude Code로 Slack API 호출

Bot Token이 있다면 Claude Code에서 직접 API를 호출하여 Team ID를 확인할 수 있습니다:

**Claude Code 실행**:
```
"Slack API를 호출해서 Team ID를 확인해줘. Bot Token은 xoxb-..."
```

**직접 curl 명령어 실행**:
```bash
curl -H "Authorization: Bearer xoxb-your-token-here" \
     https://slack.com/api/auth.test
```

**응답 예시**:
```json
{
  "ok": true,
  "url": "https://my-workspace.slack.com/",
  "team": "My Workspace",
  "team_id": "T01234ABCDE",
  "user": "claude_bot",
  "user_id": "U01234ABCDE"
}
```

여기서 `team_id` 값을 복사하세요.

#### 방법 2: Slack 앱 URL에서 추출

Slack 데스크톱 앱 또는 브라우저에서 워크스페이스를 열고 주소창 확인:

```
https://app.slack.com/client/T01234ABCDE/C01234567
                              ^^^^^^^^^^^
                              Team ID (T로 시작)
```

**예시**:
```
URL: https://app.slack.com/client/T07ABCDEF12/C123456789
Team ID: T07ABCDEF12
```

#### 방법 3: Slack 워크스페이스 설정에서 확인

[Slack 공식 가이드](https://slack.com/help/articles/221769328-Locate-your-Slack-URL-or-ID#find-your-workspace-or-org-id)를 참고하세요:

1. Slack 데스크톱 앱 또는 웹에서 워크스페이스 열기
2. 왼쪽 상단의 **워크스페이스 이름** 클릭
3. **설정 & 관리** → **워크스페이스 설정** 선택
4. 브라우저에서 새 탭이 열리면 URL 확인:
   ```
   https://my-workspace.slack.com/admin/settings
   ```
5. 페이지 하단으로 스크롤하여 **Workspace ID** 복사

⚠️ **주의**: Team ID는 항상 **T로 시작**하며, 채널 ID(C로 시작)나 사용자 ID(U로 시작)와는 다릅니다!

### 2-4. Claude Code에 Slack MCP 추가 (Project Scope)

#### ① `.mcp.json` 파일 수정

프로젝트 루트의 `.mcp.json` 파일을 열어 Slack 설정 추가:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp",
    },
    "slack": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-slack"
      ],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_TEAM_ID": "T01234ABCDE"
      }
    }
  }
}
```

#### ② 선택사항: 특정 채널만 접근 허용

보안을 위해 특정 채널만 접근하도록 제한:

```json
"env": {
  "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
  "SLACK_TEAM_ID": "T01234ABCDE",
  "SLACK_CHANNEL_IDS": "C01234ABCDE,C56789FGHIJ"
}
```

**채널 ID 확인 방법**:
1. Slack에서 채널 클릭
2. 채널 이름 옆 ⋮ 클릭
3. **"View channel details"** 선택
4. 하단의 Channel ID 복사

### 2-5. Slack 채널에 Bot 추가

자동화할 채널에서 Bot 초대:

#### 채널에서 직접 초대

```
/invite @Claude Code Bot
```

### 2-6. Slack MCP 연결 테스트

Claude Code를 재시작한 후:

```bash
# Claude Code 대화창에서 테스트
전체 슬랙 채널을 리스팅해줘
```

**예상 출력**:
```
✅ Available Slack Channels:
1. #general (C01234ABC)
2. #random (C56789DEF)
3. #engineering (C11111GHI)
4. #product-feedback (C22222JKL)
```

---

## 🤖 STEP 3: Notion 데이터베이스 준비 및 자동화 구현

이제 두 MCP 서버가 모두 연결되었으니, Slack 메시지를 저장할 Notion 데이터베이스를 만들고 자동화를 구현해봅시다.

### 3-1. Claude Code로 Notion 데이터베이스 생성하기

수동으로 Notion UI에서 데이터베이스를 만드는 대신, **Claude Code에게 자연어 명령**으로 한 번에 생성할 수 있습니다!

#### ① Claude Code에게 데이터베이스 생성 요청

Claude Code 대화창을 열고 다음 프롬프트를 입력하세요:

```
Notion 워크스페이스에 "Tasks from Slack"이라는 이름의 새 데이터베이스를 생성해줘.

다음 속성(Properties)들을 만들어야 해:

1. Name (타이틀 속성, 기본으로 있음)

2. Status (Select 타입)
   - 옵션: "To Do", "In Progress", "Done"

3. Priority (Select 타입)
   - 옵션: "Low", "Medium", "High", "Urgent"

4. Category (Select 타입)
   - 옵션: "Bug", "Feature", "Meeting", "Documentation", "Other"

5. Assignee (Text 타입)
   - 담당자 이름 저장용

6. Due Date (Date 타입)
   - 마감일 저장용

7. Source Channel (Text 타입)
   - Slack 채널명 저장용

8. Source URL (URL 타입)
   - Slack 메시지 링크 저장용

9. Tags (Multi-select 타입)
   - 자유롭게 태그 추가 가능하도록 빈 옵션으로 시작

데이터베이스를 생성한 후, 생성된 데이터베이스의 URL을 알려줘.
```

#### ② 실행 결과 확인

Claude Code가 다음과 같이 작업을 수행합니다:

```
✅ Notion 데이터베이스 생성 중...

📝 데이터베이스 생성 완료!
- 이름: Tasks from Slack
- 속성 9개 추가 완료:
  ✓ Name (Title)
  ✓ Status (Select: To Do, In Progress, Done)
  ✓ Priority (Select: Low, Medium, High, Urgent)
  ✓ Category (Select: Bug, Feature, Meeting, Documentation, Other)
  ✓ Assignee (Text)
  ✓ Due Date (Date)
  ✓ Source Channel (Text)
  ✓ Source URL (URL)
  ✓ Tags (Multi-select)

🔗 데이터베이스 URL: https://notion.so/workspace/1234567890abcdef...
```

#### ③ Notion에서 확인

1. Notion 워크스페이스를 열면 새로 생성된 "Tasks from Slack" 데이터베이스가 보입니다
2. 속성 탭을 확인하여 모든 필드가 정확히 생성되었는지 검증
3. Select 옵션들이 올바르게 설정되었는지 확인

💡 **프롬프트 작성 팁**:
- 속성 타입을 명확히 지정 (Select, Text, Date, URL 등)
- Select 타입은 옵션 값을 구체적으로 나열
- 각 속성의 용도를 간단히 설명하면 더욱 정확한 생성 가능

### 3-2. 기본 자동화 프롬프트

가장 간단한 형태의 프롬프트입니다.

```
#engineering 채널의 최근 메시지 10개를 읽어서,
"TODO", "TASK", "액션 아이템" 같은 키워드가 포함된 메시지를 찾아
Notion의 "Tasks from Slack" 데이터베이스에 저장해줘.

각 태스크는 다음 정보를 포함해야 해:
- Title: 메시지의 첫 줄 또는 요약
- Status: "To Do"로 설정
- Priority: "urgent", "asap" 같은 키워드가 있으면 "High", 없으면 "Medium"
- Source Channel: "#engineering"
- Source URL: Slack 메시지 링크
```

**실행 결과**:
```
✅ 3개의 태스크를 Notion에 생성했습니다:

1. "Fix critical bug in payment processing"
   - Priority: High
   - Source: https://slack.com/archives/C123/p1234567890

2. "Update API documentation for v2.0"
   - Priority: Medium
   - Source: https://slack.com/archives/C123/p1234567891

3. "Schedule code review meeting"
   - Priority: Medium
   - Source: https://slack.com/archives/C123/p1234567892
```
---

## 📖 참고 자료

### 공식 문서
- [Claude Code MCP 공식 문서 (한글)](https://docs.claude.com/ko/docs/claude-code/mcp)
- [MCP Protocol 명세](https://modelcontextprotocol.io/)
- [Notion API 문서](https://developers.notion.com/)
- [Slack API 문서](https://api.slack.com/)

### GitHub 저장소
- [MCP Servers (공식)](https://github.com/modelcontextprotocol/servers)
- [Slack MCP Server (Archived)](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/slack)


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
