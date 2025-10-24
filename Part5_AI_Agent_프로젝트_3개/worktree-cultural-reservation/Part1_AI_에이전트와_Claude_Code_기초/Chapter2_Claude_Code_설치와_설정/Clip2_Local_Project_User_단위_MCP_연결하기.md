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

# Clip 2: Local/Project/User 단위 MCP 연결하기

> **출처**: [Claude Code - MCP 공식 문서](https://docs.claude.com/ko/docs/claude-code/mcp)

## 학습 목표
- MCP 서버의 세 가지 스코프(Local, Project, User)를 이해합니다
- 각 스코프의 특징과 사용 시나리오를 파악합니다
- 프로젝트와 팀 협업에 적합한 스코프를 선택할 수 있습니다

## 핵심 요점
- **Local 스코프**: 현재 프로젝트에서만 사용하는 개인 설정
- **Project 스코프**: 팀 전체가 공유하는 프로젝트 도구 (추천)
- **User 스코프**: 모든 프로젝트에서 사용하는 공통 도구
- 스코프 우선순위: Local > Project > User

---

## 1. MCP 스코프란?

MCP(Model Context Protocol) 서버는 세 가지 스코프 레벨에서 설정할 수 있습니다. 각 스코프는 MCP 서버가 접근 가능한 범위와 저장 위치를 결정합니다.

### 스코프 비교표

| 스코프 | 범위 | 설정 파일 위치 | 주요 용도 |
|--------|------|---------------|----------|
| **Local** | 현재 프로젝트만 | 프로젝트 루트의 로컬 설정 | 개인 실험, 민감한 자격 증명 |
| **Project** | 프로젝트 내 팀 전체 | `.mcp.json` (버전 관리) | 팀 협업, 프로젝트별 도구 |
| **User** | 사용자의 모든 프로젝트 | `~/.config/claude/mcp.json` | 개인 유틸리티, 범용 도구 |

### 스코프 우선순위

```
Local > Project > User
```

동일한 이름의 MCP 서버가 여러 스코프에 정의되어 있으면, Local 설정이 가장 높은 우선순위를 가집니다. 이를 통해 개인 설정으로 팀 설정을 덮어쓸 수 있습니다.

---

## 2. Local 스코프: 개인 실험용

### 특징
- 현재 디렉토리에서만 접근 가능
- 현재 사용자에게만 비공개
- 실험적 구성이나 민감한 자격 증명에 적합

### 설치 명령어

```bash
# Local 스코프 MCP 서버 추가 (기본값)
claude mcp add --transport http stripe https://mcp.stripe.com
```

### 사용 시나리오
```python
# 예시: 개인적으로 테스트 중인 결제 시스템 연동
# - Stripe API를 로컬에서만 테스트
# - 팀에 공유하기 전 실험 단계
# - 개인 API 키 사용
```

**언제 사용할까?**
- 새로운 MCP 서버를 팀에 도입하기 전 개인적으로 테스트할 때
- 개인 API 키나 비밀번호가 필요한 서비스
- 프로젝트별로 다른 설정이 필요한 경우

---

## 3. Project 스코프: 팀 협업 권장 ⭐

### 특징
- `.mcp.json` 파일에 저장되어 버전 관리 가능
- 팀 전체가 동일한 MCP 도구 사용
- 사용 전 사용자 승인 필요 (보안)

### 추천 MCP 서버

#### 1. **Playwright** (E2E 테스트 자동화)
```bash
# Playwright MCP 추가
claude mcp add playwright npx @playwright/mcp@latest -s project
```

- 웹 브라우저 자동화 및 테스트
- 팀 전체가 동일한 테스트 환경 사용
- E2E 테스트 시나리오 작성 및 실행

#### 2. **Linear** (이슈 트래킹)
```bash
# Linear MCP 추가
claude mcp add --transport sse linear https://mcp.linear.app/sse -s project
```

- 프로젝트 이슈 및 작업 관리
- Linear 이슈 조회, 생성, 업데이트
- 팀 워크플로우 자동화

### `.mcp.json` 예시

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "linear": {
      "transport": {
        "type": "sse",
        "url": "https://mcp.linear.app/sse"
      }
    }
  }
}
```

**왜 Project 스코프를 추천할까?**
1. **협업 효율성**: 팀원 모두가 동일한 도구 환경
2. **버전 관리**: Git으로 MCP 설정 추적 가능
3. **온보딩 간소화**: 새 팀원이 자동으로 필요한 MCP 설치
4. **일관성**: 프로젝트별 도구가 명확하게 정의됨

---

## 4. User 스코프: 범용 도구

### 특징
- 사용자의 모든 프로젝트에서 접근 가능
- `~/.claude.json`에 저장
- 개인 유틸리티 서버와 자주 사용하는 서비스에 적합

### User 스코프 추천 MCP

모든 프로젝트에서 공통적으로 사용하고 토큰 소비가 적은 범용 도구만 User 스코프로 설치하세요.

#### 1. **Codex** (AI 코딩 에이전트)
```bash
claude mcp add codex --scope user codex mcp
```
- GPT-5를 같이 쓸 수 있다.
- 추가적인 API 사용 없이 구독 비용으로 사용할 수 있다.

#### 2. **Context7** (최신 라이브러리 문서)
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp -s user
```
- 최신 라이브러리 문서 자동 검색
- 모든 프로젝트에서 유용 (React, FastAPI, PyTorch 등)

**User 스코프에 적합한 MCP 특징**
- ✅ 모든 프로젝트에서 공통으로 사용
- ✅ 토큰 소비가 적어야 함 (중요!)
- ✅ 프로젝트별 특화 설정이 불필요
- ✅ 생산성 도구

---

## 5. 필요한 MCP 검색하기: Smithery.ai

### Smithery.ai란?

[Smithery.ai](https://smithery.ai/)는 MCP 서버의 공식 마켓플레이스로, 커뮤니티에서 만든 다양한 MCP를 검색하고 설치할 수 있습니다.

### 사용 방법

1. **웹사이트 방문**: https://smithery.ai/
2. **검색**: 필요한 기능 키워드 입력 (예: "youtube", "notion", "slack")
3. **설치 정보 확인**: 각 MCP의 설치 명령어와 설정 방법 제공

### 실전 예시: YouTube Transcript MCP

YouTube 동영상의 자막을 추출하는 MCP를 찾아보겠습니다.

#### Step 1: Smithery.ai에서 검색
- 검색어: `youtube transcript`
- 결과: `mcp-youtube-transcript` 패키지 발견

#### Step 2: 설치 정보 확인

Smithery.ai에서 제공하는 설정:
```json
{
  "youtube-transcript": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/jkawamoto/mcp-youtube-transcript",
      "mcp-youtube-transcript"
    ]
  }
}
```

#### 사용 예시

```python
# YouTube 자막 추출 및 요약 자동화
"""
프롬프트 예시:
'https://www.youtube.com/watch?v=fGKNUvivvnc 영상의 자막을 가져와서 핵심 내용을 요약해줘'

MCP가 자동으로:
1. YouTube 동영상 자막 추출
2. 텍스트를 AI가 분석
3. 핵심 내용 요약 제공
"""
```

## 참고
https://docs.claude.com/ko/docs/claude-code/mcp


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
