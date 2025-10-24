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

# Clip 1: 강의를 통해 얻어갈 수 있는 것

## Clip 1: 강의를 통해 얻어갈 수 있는 것

### 학습 목표

* 바이브 코딩(AI Agent를 활용한 코딩)의 개념과 장점 이해하기
* 강의를 통해 만들게 될 실제 프로젝트 결과물 파악하기
* AI를 능숙하게 다루는 핵심 스킬 습득 방향 이해하기
* 효율적인 강의 수강 방법 알아보기

### 이 강의에서 배우는 것

#### 1. 바이브 코딩(Vibe Coding) = AI Agent 사용법

**Claude Code, Codex 같은 코딩 AI Agent를 사용하는 법**을 배웁니다.

```
전통적인 코딩:
개발자가 직접 코드 작성 → 테스트 → 디버깅

바이브 코딩:
개발자가 의도 전달 → AI가 코드 구현 → 개발자가 검증
```

**바이브 코딩의 의의:**

* AI Agent가 코드 구현을 담당
* 개발자는 설계와 테스트에 집중
* 여러 Agent를 동시에 사용해서 생산성을 극대화할 수 있음

#### 2. AI Agent 만드는 법

바이브 코딩을 통해 **AI Agent를 직접 구축**하는 방법을 배웁니다.

**왜 바이브 코딩으로 AI Agent를 배우는가?**

* AI Agent는 라이브 코딩으로 학습하는 것이 가장 효율적
* 바이브 코딩 도구 자체가 훌륭한 AI Agent
* Claude Code를 사용하면서 눈으로 직접 동작 방식 관찰
* 오픈소스 코드를 살펴보며 구체적 구현 학습

#### 3. 이 강의의 독특한 학습 방식

**재미있는 것부터 시작하는 역순 학습:**

```
기존 강의 방식:
이론 → 기초 → 응용 → 프로젝트

이 강의 방식:
재미있고 쉽게 동작하는 프로젝트(MCP client) → RAG → MCP server(점점 더 좁게)
```

**왜 이 방식인가?**

* 바이브코딩 덕분에 **재미있는 것(MCP client)부터 만들 수 있습니다**
* 동작하는 결과물을 먼저 보고, 나중에 더 근본적인 것을 배웁니다
* 동기부여를 유지하며 학습 효율을 극대화합니다

**단계별 코딩 접근법:**

```
Part 1~3: 맨땅에 헤딩 방식
- 빠르게 구현하고 결과를 확인
- 중간 커밋 없음
- TDD 없음
- 순수하게 바이브코딩으로 빌드

Part 4~6: 체계적 개발 방식
- Codex MCP 활용
- Linear MCP 티켓 관리
- 자동 git 커밋
- TDD 적용
```

**이렇게 나눈 이유:**

* 학습자마다 기본 코딩 수준 차이가 있습니다
* 초반에는 **결과물 만드는 재미**에 집중
* 후반에는 **실무 수준의 개발 프로세스** 학습
* 단계적으로 복잡도를 높여 학습 부담 감소

### 강의 결과물

이 강의를 완료하면 다음과 같은 Agent를 직접 구현하게 됩니다:

#### Part3: RAG 기반 농협 대출 상품 추천 AI Agent

<div data-with-frame="true"><figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure></div>

**주요 기능:**

* 실제 농협 대출 상품 검색
* RAG(Retrieval Augmented Generation) 기반 답변
* Agentic하게 도구 사용 결정

#### Part 5: LLM 기반 Slack Bot

<div data-with-frame="true"><figure><img src="../../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure></div>

**기능:**

* Slack 메시지 자동 응답
* LLM 기반 대화 처리
* 실시간 정보 제공

#### Part5: 공공 API 활용 MCP Server

<div data-with-frame="true"><figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure></div>

**특징:**

* 공공 데이터 API 활용
* 직접 구현한 MCP Server
* 내가 사용하는 모든 AI 도구에 연결 가능
  * Claude
  * Claude Code
  * Cursor
  * 기타 MCP 지원 도구

### AI Agent 의 Context를 능숙하게 다루는 방법

#### Claude Code의 핵심 개념 이해

**Claude Code의 구성 요소를 AI Agent 개념에 대입하여 학습:**

**1. Slash Commands (슬래시 커맨드)**

```
/commit → 특정 작업 실행
/test → 테스트 실행
```

→ AI Agent의 **Tool/Function 개념**

**2. Sub-Agent (서브 에이전트)**

```
작업 분담 → 병렬 처리 → 결과 통합
```

→ AI Agent의 **멀티 에이전트 시스템 개념**

**3. Output-Style**

```
출력 형식 지정 → 일관된 결과
```

→ AI Agent의 **프롬프트 엔지니어링 개념**

**학습 효과:**

* LLM이 컨텍스트를 사용하는 방식 이해
* AI Agent 구조와 동작 원리 파악
* 실전에서 바로 적용 가능한 패턴 습득

#### 이 강의 자료를 Claude Code에게 제공하고 같이 학습하세요

**PDF, PPT가 아닌 markdown 으로 강의 자료를 만들었습니다.**

```markdown
# Markdown 형식
- LLM이 가장 잘 이해하는 문서
- 구조화된 정보 전달
- 코드와 설명 통합
```

**활용 방법:**

1. 강의 영상 시청
2. 모르는 내용은 Markdown 문서 확인
3.  Claude Code에게 문서 기반 질문

    ```
    "이 문서를 읽고 Sub-Agent가 별도의 컨텍스트 윈도우를 가진다는 의미를 자세히 설명해줘"
    ```

**장점:**

* 영상보다 더 자세한 내용 포함
* LLM과 대화하며 깊이 있는 학습 가능
* 필요한 부분 빠르게 검색 가능

### 강의 구성

이 강의는 **4가지 주요 카테고리**로 구성되어 있습니다:

**효과적인 강의 수강:**

1. 각 강의마다 **카테고리 명확히 구분**
2. **필요한 강의부터 먼저** 수강
3. **순서에 구애받지 않고** 학습
4. 궁금한 부분은 **Markdown 문서 참고**

***

## 강의 클립별 카테고리 분류

| 클립    | 제목                                                         | 바이브코딩 | AI 리터러시 | AI Agent 이론 | AI Agent 실습 |
| ----- | ---------------------------------------------------------- | :---: | :-----: | :---------: | :---------: |
| 1-1-1 | 강의를 통해 얻어갈 수 있는 것                                          |   ☐   |    ☐    |      ☐      |      ☐      |
| 1-1-2 | CLI기반 Claude Code 와 Codex로 할 수 있는 것                        |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-1-3 | AI 에이전트 + MCP 기술이 주목받는 이유                                  |   ☐   |    ☑    |      ☐      |      ☐      |
| 1-1-4 | Docs와 실습코드(Github)                                         |   ☐   |    ☐    |      ☐      |      ☐      |
| 1-2-1 | 설치와 기본 사용법                                                 |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-2-2 | Local/Project/User 단위 mcp 연결하기                             |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-2-3 | CLAUDE.md, AGENTS.md 세팅하기                                  |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-3-1 | Slash Command 만들기                                          |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-3-2 | Sub Agent 만들기                                              |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-3-3 | Hooks, Output Styles 설계하기                                  |   ☑   |    ☐    |      ☐      |      ☐      |
| 1-4-1 | 클로드코드로 자동화하기                                               |   ☐   |    ☑    |      ☐      |      ☐      |
| 1-4-2 | 슬래쉬 커맨드를 자동으로 업데이트하기                                       |   ☐   |    ☑    |      ☐      |      ☐      |
| 2-1-1 | Agent vs Workflow 개념 이해하기                                  |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-1-2 | AI Agent architecture 자세히 살펴보기                             |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-2-1 | LLM api 이해하고 호출해보기                                         |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-2-2 | 세부 파라미터 (reasoning\_effort, verbosity, max\_token)         |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-2-3 | 프롬프트 작성                                                    |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-3-1 | Claude Code 등 에이전트가 어떻게 mcp를 활용하는지 보기                      |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-3-2 | 오픈소스 AI AGENT의 mcp 활용 코드 까보기                               |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-3-3 | Tool 이해하기                                                  |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-3-4 | MCP client 개념 이해하기                                         |   ☐   |    ☐    |      ☑      |      ☐      |
| 2-4-1 | mcp client 를 구현하기 위한 PRD 프롬프트 만들기                          |   ☐   |    ☐    |      ☐      |      ☑      |
| 2-4-2 | mcp client 구현하기                                            |   ☐   |    ☐    |      ☐      |      ☑      |
| 3-1-1 | Vector Search 이해하기                                         |   ☐   |    ☐    |      ☑      |      ☐      |
| 3-1-2 | BM25 이해하기                                                  |   ☐   |    ☐    |      ☑      |      ☐      |
| 3-1-3 | PRD 프롬프트 만들기                                               |   ☐   |    ☐    |      ☐      |      ☑      |
| 3-1-4 | Hybrid Search 구현하기                                         |   ☐   |    ☐    |      ☐      |      ☑      |
| 3-2-1 | RAG 개념 이해하기                                                |   ☐   |    ☐    |      ☑      |      ☐      |
| 3-2-2 | PRD 프롬프트 만들기                                               |   ☐   |    ☐    |      ☐      |      ☑      |
| 3-2-3 | Langgraph RAG 구현하기                                         |   ☐   |    ☐    |      ☐      |      ☑      |
| 3-3-1 | workflow -> Agentic의 개념 복기하기                               |   ☐   |    ☐    |      ☑      |      ☐      |
| 3-3-2 | Database와 Web Search를 툴로 사용하는 에이전트 구현하기                    |   ☐   |    ☐    |      ☐      |      ☑      |
| 4-1-1 | MCP server의 개념과 구조 이해하기                                    |   ☐   |    ☐    |      ☑      |      ☐      |
| 4-1-2 | MCP server 코드 까보기: sequential thinking, notion, playwright |   ☐   |    ☐    |      ☑      |      ☐      |
| 4-2-1 | dummy MCP server 구현하기                                      |   ☐   |    ☐    |      ☐      |      ☑      |
| 4-2-2 | Claude, Claude code 에 연결하기                                 |   ☐   |    ☐    |      ☐      |      ☑      |
| 4-3-1 | Postgresql mcp server 구현체 보기                               |   ☐   |    ☐    |      ☑      |      ☐      |
| 4-3-2 | mock 스키마 만들고 데이터 합성해서 집어넣기                                 |   ☐   |    ☐    |      ☐      |      ☑      |
| 4-3-3 | DB write tool 설계하기                                         |   ☐   |    ☐    |      ☐      |      ☑      |
| 4-3-4 | 클로드에 연결해서 써보기                                              |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-1-1 | 슬랙 커뮤니티 CS 내역을 LLM 으로 합성하기                                 |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-1-2 | 시스템 프롬프트 만들기                                               |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-1-3 | 슬랙봇 구현 프롬프트 작성하기                                           |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-1-4 | 슬랙봇 구현하고 AWS lambda 배포하기                                   |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-1-5 | 슬랙에서 사용하면서 업데이트하기                                          |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-2-1 | data.go.kr 에서 국민연금공단 api 살펴보기                              |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-2-2 | api -> mcp server 구현 프롬프트 작성하기                             |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-2-3 | mcp server 구현하기                                            |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-2-4 | Claude에 연결해서 사용하면서 업데이트하기                                  |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-3-1 | awslabs/mcp 구현체 이해하기                                       |   ☐   |    ☐    |      ☑      |      ☐      |
| 5-3-2 | mcp server 자동 생성하는 에이전틱 프로세스 만들기                           |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-3-3 | data.go.kr 에서 api 골라서 자동 생성하기                              |   ☐   |    ☐    |      ☐      |      ☑      |
| 5-3-4 | smithery 스타일의 웹페이지 구현하기                                    |   ☐   |    ☐    |      ☐      |      ☑      |
| 6-1-1 | best practice 찾아서 이해하기                                     |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-1-2 | 바이브코딩 팁을 자동화시키기                                            |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-1-3 | 클로드 코드 시스템 프롬프트 계층 이해하기                                    |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-2-1 | Context/Prompt Engineering 이해하기                            |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-2-2 | AI의 PM이 되기                                                 |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-3-1 | git worktree 이해                                            |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-3-2 | worktree 자동화 스크립트 생성하기                                     |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-3-3 | 티켓 자동 생성하고 병렬 처리하기                                         |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-4-1 | 바이브코딩의 리스크를 낮추기 위한 feature 선정 방법                           |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-4-2 | 바이브코딩으로 프로젝트를 시작하면 유리한 점                                   |   ☑   |    ☐    |      ☐      |      ☐      |
| 6-5-1 | 클로드코드를 나만의 AI 에이전트로 사용하기                                   |   ☐   |    ☑    |      ☐      |      ☐      |
| 6-5-2 | 메타 프롬프트                                                    |   ☐   |    ☑    |      ☐      |      ☐      |


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
