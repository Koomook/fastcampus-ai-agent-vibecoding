## Part 1. AI 에이전트와 바이브코딩 입문

### Chapter 1. 바이브코딩으로 AI 에이전트 시작하기
- Clip 1: 강의를 통해 얻어갈 수 있는 것
  - 1가지: 클로드코드를 활용해 바이브코딩하는 방법, Multi Clauding
  - 2가지: AI AGENT에 대한 이해
  - 결과물 예시: 농협, MCP SERVER, 서브에이전트를 통한 자동화, 
  - AI를 능숙하게 다루는 방법
  - 강의를 볼 때 DOCS, GITHUB 을 클로드코드한테 먹여라
  - 강의는 이렇게 한다.
    - 하나 하나 만드는 건 재미없다. 바이브코딩 덕분에 재밌는 것(mcp client)부터 만들고, RAG, mcp server 등 더 근본적인 걸 만들러 간다.
  - 기본 코딩 수준 차이가 있기 때문에 
    - Part3 까지는 맨땅에 헤딩하는 방식으로 바이브코딩합니다. 중간 커밋이나 TDD 는 없습니다.
    - Part4 부터는 codex, linear, 자동 커밋, TDD 등을 적용합니다.
- Clip 2: CLI기반 Claude Code 와 Codex로 할 수 있는 것
  - 뭐든지 할 수 있다. 코딩, PRD, ...
  - system prompt 튜닝
  - 코드를 안 보게 된다.
  - CLI 는 CLAUDE CODE 에서 말했듯(https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built) 내 컴퓨터의 파일 시스템과 배쉬를 다룰 수 있다.
  - 그래서 할 수 있는 일이 무궁무진하다.
- Clip 3: AI 에이전트 + MCP 기술이 주목받는 이유
  - OPENAI DEV DAY에서 발표한 APPS sdk는 Chat GPT라는 AI Agent에 MCP를 붙이는 것
    - https://developers.openai.com/apps-sdk/
      https://developers.openai.com/apps-sdk/plan/use-case
      https://developers.openai.com/apps-sdk/build/mcp-server
  - 얼마나 중요하냐면 KIMI K2 에서는 MCP를 잘 사용할 수 있게 학습했다. -> Web Search
  - 우리가 쓰는 모든 AI 툴은 AI AGENT
    - LLM을 사용하는 앱. 에이전트는 목표 달성을 위해 자율적으로 작업을 수행한다. 이걸 바이브코딩으로 만들기 위한 지식 학습
  - MCP 는 모델이 사용할 수 있는 도구임. 최근 모델은 발표할 때마다 도구 사용 벤치마크를 알려준다. 현 시점 가장 중요한 벤치 -> web search

- Clip 4: Docs와 실습코드(Github)
  - Claude Code한테 모르는 부분 물어보기.
    - "사용자 정의 슬래쉬 커맨드 실전 예제 찾아줘"
  - 강의 자료를 탐색하기 위한 나만의 CLAUDE.md 를 만들어서 사용하세요
  - ChaptGPT 를 사용하고 계시면 이렇게 해도 된다.
    - 강의를 켜고 챗지피티 녹음 버튼 사용. 모르는 부분에서 멈추기. 강의 md 파일을 제공하고 모르겠는 부분 물어보기

### Chapter 2. Claude Code, Codex 기본 세팅하기
- Clip 1: 설치와 기본 사용법
- Clip 2: Local/Project/User 단위 mcp 연결하기
  - https://docs.claude.com/ko/docs/claude-code/mcp 참고
  - project 스코프를 추천
    - playwright
      - claude mcp add playwright npx @playwright/mcp@latest -s project
    - linear
      - claude mcp add --transport sse linear https://mcp.linear.app/sse -s project

  - user 스코프로 설치하는 것: codex, context7
    - claude mcp add --transport http context7 https://mcp.context7.com/mcp -s user
    - claude mcp add codex --scope user codex mcp
    - 모든 프로젝트에서 공통적으로 사용하는 mcp
    - token 을 많이 먹지 않아야 함
  
  - 필요한 mcp 를 검색해서 사용하기: youtube transcript
    - https://smithery.ai/
    - "youtube-transcript": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jkawamoto/mcp-youtube-transcript",
        "mcp-youtube-transcript"
      ]
    }
- Clip 3: CLAUDE.md, AGENTS.md 세팅하기

### Chapter 3. Claude Code 개발을 위한 커스텀 환경 세팅하기
- Clip 1: Slash Command 만들기
  - slash 명령어 중에 반드시 알아야 할 슬래쉬 명령어
    - /add-dir, /clear, /config, /init, /mcp, /memory, /model, /review, /rewind, /status
  - 다음 예제에서는 /optimize 명령어를 생성합니다 섹션 추가
  - project scope slash command 생성: "/create-linear-issues"

  linear mcp 를 사용해서 linear team fastcampus-seminar-02 에
  linear issue를 생성해

  issue 를 만들 때에는 sub issue 로 그 다음 issue 를 연결해

  참조:
  https://docs.claude.com/ko/docs/claude-code/slash-commands#cus
  tom-slash-commands
- Clip 2: Sub Agent 만들기: https://docs.claude.com/ko/docs/claude-code/sub-agents
  - subagent: linear issue 와 코드베이스를 조사해서 issue 해결할 적절한 context만 골라서 출력
    - 사용 방법: @ultimate-planner {issue-id or issue description}

  1. linear 조회
  linear team: fastcampus-seminar-02
  관련 이슈 검색해서 issue title, description, comment 조회
  해당 이슈의 parent 혹은 sub 이슈가 있다면 그 이슈의 내용도 조사

  1. 코드베이스 탐색
  2. git log 검색
  
  결과물: 이슈 해결 plan, 수정하거나 참조해야 하는 파일 위치, todo

  transcript:
    0:03 이번 시간은 서브에이전트를 실제로 만들어보고 사용해보겠습니다. 서브에이전트는, 서브에이전트, 서브에이전트는요, 전문화된 AI 어시스턴트입니다.
0:24 AI 아이전트, 특정 도메인이나 작업에 특화된 AI 아이전트 이고, 이 중요한 특징은 자체 컨텍스트에서 작동하기 때문에 메인 대화에 오염을 방지한다는 것입니다.
0:49 컨텍스트 보존이 되고 재사용할 수 있고 세부지침으로 특정 전문성 이 두가지를 사실 가장 중요하게 사용하시면 좋구요 그래서 커스텀 커맨드랑 다른 점을 자체 컨텍스트 창을 사용한다는 것입니다.
1:17 그 점을 이용해서 서브에이전트를 사용하는 것을 저는 굉장히 추천을 드립니다. 예를 들어서 어떤 구성인지 CLI 기반 이런 방식들은 사실 그렇게까지 지금 중요한데요.
1:39 대신에 agent를 만들 때 slash-agent라는 명령으로 들어가서 클러드한테 직접 만들어 달라고 하는게 좋습니다.
1:53 효과적으로 사용할 때에는 명시적으로 호출할 수도 있구요. 혹은 블러셔 사용 할 수도 있는데 이런식으로 에이전트를 체이닝 할 수도 있습니다 그래서 제가 추천드리는 방식은 저희가 코딩을 할 때에 리뉴얼 이제 코딩을 할 때에는 초반에 제대로 된 컨텍스트를 넣어주는 게 중요하거든요.
2:31 그런데 전체 세션에서 어떤 플래닝을 할 때에 너무 많은 파일들을 읽게 되면 그 파일들로 이미 컨텍스트가 다 차버려요.
2:43 그게 제일 큰 문제입니다. 그래서 클러드한테 딱 선별된 파일을 넣어주는 컨텍스트만 제공을 하기 위해서 제가 추천드리는 서브에이전트를 활용하는 방식은 이건데요 많은 컨텍스트를 서브에이전트가 읽고 꼭 필요한 컨텍스트만 꼭 필요한 컨텍스트만 이제 만들어라 라고 하는 겁니다 그래서 Linear Monday 먼저 저는 보통 리니어를 이용해서 이슈 관리, 테스트 관리를 하니까 리니어에서 리니어 팀을 미리 알려주고 타이틀, 디스크립션, 코멘트까지 조회를 한 다음에 관련된 그 해당 이슈의 프렌트워크는 서브 이슈가 있다면 그 이슈의 내용도 조사해야 
4:01 합니다. 그리고 코드베이스를 탐색해라. 마지막으로는 git log도 검색해라. 결과물은 이슈 해결 플랜과 투두 이렇게 만들어 줘서 이 에이전트는 최대한 많은 컨텍스트를 이제 읽게 되고 이 컨텍스트를 사용해서 이 컨텍스트 그 엄청나게 많은 컨텍스트들 중에 내가 이슈를 해결하는데 필요한 내용만 출력을 하게 됩니다.
4:48 플랜으로요. plan 수정하거나 참조해야 하는 파일 위치 이렇게 되면 훌륭한 플래너가 됩니다 궁극의 플래너라고 붙이겠습니다 리니어도 쓰고 이 서브 에이전트를 만들어라 project 범위에서 만들어라 라고 합니다 이것을 만들어 줄 거고 초후 강의에서 그것들을 사용해 보겠습니다.
- Clip 3: Hooks, Output Styles 설계하기

### Chapter 4. <실습> 슬랙 메시지 읽고 notion 에 태스크 저장하는 커맨드 설계
- Clip 1: 클로드코드로 자동화하기
- Clip 2: 슬래쉬 커맨드를 자동으로 업데이트하기


### Chapter 1. Agent 개념 이해하기
- Clip 1: Agent vs Workflow 개념 이해하기
  - https://langchain-ai.github.io/langgraph/tutorials/workflows/#set-up 에서 개념 가져오기. (코드는 가져오지 마라)
- Clip 2: AI Agent architecture 자세히 살펴보기
  - https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/ 에서 개념 가져오기.
  - https://www.anthropic.com/engineering/building-effective-agents 참고
출처를 명확히 밝히기

### Chapter 2. LLM api 호출 이해하기
- Clip 1: LLM api 이해하고 호출해보기
  - openai api 코드 예시 추가
  - langchain 코드 예시 추가 (openai)
  - 이해를 위한 자세한 설명
- Clip 2: 세부 파라미터 (reasoning_effort, verbosity, max_token)
  - openai api 에서 제공하는 3가지 파라미터에 대해 설명하기
  - @docs/gpt-5에 새로 등장한 verbosity, max_tokens와 다른 점.md 에서 내용 가져오기
- Clip 3: 프롬프트 작성
  - LLM api 를 호출하는 코드를 작성하는 프롬프트 예시와 결과물 코드 설명

### Chapter 3. mcp client 사용하기
- Clip 1: Claude Code 등 에이전트가 어떻게 mcp를 활용하는지 보기
  - claude code 실행했을 때 실행되는 화면을 보면서 tool 사용을 눈으로 확인하기
- Clip 2: 오픈소스 AI AGENT의 mcp 활용 코드 까보기
  - https://github.com/sst/opencode 를 clone 해서 claude code 로 물어보기: "시스템 프롬프트와 MCP 사용 방법을 코드레벨로 자세히 설명"
- Clip 3: Tool 이해하기
  - 아래 페이지에서 보편적인 설명을 가져오기
    - https://platform.openai.com/docs/guides/function-calling
    - https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
    - https://modelcontextprotocol.io/docs/getting-started/intro
    - https://modelcontextprotocol.io/docs/learn/architecture
- Clip 4: MCP client 개념 이해하기
  - https://modelcontextprotocol.io/docs/learn/client-concepts
  - https://modelcontextprotocol.io/docs/develop/build-client

### Chapter 4. <실습> 바이브코딩으로 mcp + AI 에이전트 만들기
- Clip 1: mcp client 를 구현하기 위한 PRD 프롬프트 만들기
- Clip 2: mcp client 구현하기

---

## Part 3. 바이브코딩으로 Hybrid Search RAG 구현하기

### Chapter 1. <실습> Postgresql 기반 Hybrid Search 구현하기
- Clip 1: Vector Search 이해하기
  - Vector Search 개념 검색해서 출처와 함께 설명
  - pg_vector 검색해서 개념 설명
  - 200줄 이하로 생성
- Clip 2: BM25 이해하기
  - BM25 개념 검색해서 출처와 함께 설명. full text search와 다른 점
  - pg_search(paradedb) 검색해서 개념 설명
  - 200줄 이하 생성
- Clip 3: PRD 프롬프트 만들기
  - Neon(supabase 대체재) 에서 Postgresql 기반 paradedb pg_search를 native로 지원함. 그래서 사용
  - neon mcp 연동해서 project 만들고 세팅. https://github.com/neondatabase/mcp-server-neon
    - {
        "mcpServers": {
          "Neon": {
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.neon.tech/mcp"]
          }
        }
      }
  - python, uv, paradedb(/documentation/guides/hybrid#expected-response), openai embedding small(pg_vector)
  - Hybrid Search 를 구현할 때 필요한 30줄 아래의 프롬프트를 만드는 과정을 설명하기
    - @Clip1_MCP_Client_구현을_위한_PRD_프롬프트_만들기.md 확인해서 비슷하게 구성
- Clip 4: Hybrid Search 구현하기
  - 바이브코딩하면서 트러블 슈팅. 이곳에는 문서가 거의 없어도 됨

## Part 3. 바이브코딩으로 Hybrid Search RAG 구현하기
### Chapter 2. <실습> Langgraph 기반 workflow RAG 구현하기
- Clip 1: RAG 개념 이해하기
  - 검색해서 RAG가 무엇인지 출처와 함께 설명
    https://python.langchain.com/docs/concepts/
    https://python.langchain.com/docs/concepts/retrievers/
  - 200줄 이하로 생성
- Clip 2: PRD 프롬프트 만들기
  - Langgraph 를 활용해서 ROUTING 기반 hybrid search 를 사용하거나 그냥 대답하는 python cli 생성
  - Chapter 1에서 만든 hybrid search 사용
  - PRD 프롬프트는 chapter 1 - clip 3 참고
- Clip 3: Langgraph RAG 구현하기
  - 빈 파일

### Chapter 3. <실습> 바이브코딩으로 Agentic RAG 구현하기
- Clip 1: workflow -> Agentic의 개념 복기하기
  - Part2 chapter 1 개념 복기해서 workflow, Agent 비교
  - 구현한 workflow 의 장단점: (search_app/ 확인해서 아래 내용 작성)
    - 장점: 대출 상품을 추천할 때 내가 의도한대로 정확하게 동작하게 하는데는 탁월함
    - 단점: 유연성 부족, 다양한 상황에 대응하려면 노드, 엣지를 계속 추가해야 함, LLM의 성능을 끝까지 활용하지 못함
  - Agent로 해볼 것
    - routing 기반의 rag workflow 대신 hybrid search 를 툴로 사용하는 Agent 구현
    - https://github.com/vercel-labs/ai-sdk-preview-python-streaming 의 프론트엔드 활용하고 백엔드 업데이트
- Clip 2: Database와 Web Search를 툴로 사용하는 에이전트 구현하기
  - 빈 파일 생성

---

## Part 4. 바이브코딩으로 MCP server 구현하기

### Chapter 1. MCP server 이해하기
- Clip 1: MCP server의 개념과 구조 이해하기
  - 참고: https://modelcontextprotocol.io/docs/learn/server-concepts
  - tool 의 구성 요소
  - resource, prompt 의 역할
  - 연결 방식: stdio / http
  - npx, uvx 로 설치하는게 뭘 뜻하는지
- Clip 2: MCP server 코드 까보기: sequential thinking, notion, playwright
  - https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
  - https://github.com/makenotion/notion-mcp-server
  - https://github.com/microsoft/playwright-mcp
  - 각각의 mcp server 들이 어떤 TOOL 을 가지고 있는지 CLONE해서 조회한 다음 설명 작성
    - DESCRIPTION 을 통해 언제 사용하는지, 선택됐을 때 TOOL 이 동작하는 것은 무엇인지 설명

### Chapter 2. <실습> MCP server 구현하고 Claude에 연결하기
- Clip 1: dummy MCP server 구현하기
  - 
- Clip 2: Claude, Claude code 에 연결하기

### Chapter 3. <실습> 우리 회사 DB를 쿼리하는 mcp server 구현하기
- Clip 1: Postgresql mcp server 구현체 보기
  - https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres
  - https://github.com/modelcontextprotocol/servers-archived/blob/main/src/postgres/index.ts
  - 예, 직접적인 타입 스크립트 코드보다는 어떤 툴의 목록이 있는지, 그리고 그 툴들은 어떤 방식으로 동작을 하는지를 설명해줘. 예를 들어서 어, 시나리오를 통해서 시나리오를 작성해서, 어, 내가 어떤 테이블에 뭐를 만들어줘 라고 했을 때 이제. 네. 했을 때. 어떤 툴을 이제 연쇄적으로 클로드가 사용하게 되는지. 그런 것들을 시나리오 딱 한 개 만들ㅇ어서 강의 자료를 작성해.
- Clip 2: mock 스키마 만들고 데이터 합성해서 집어넣기
  - 강의를 위한 예시 데이터를 네온 엠씨피를 사용해서, 채용 서비스를 운영하는 회사의 디비 테이블을 가짜로 만들어보자.
  - table: candidates
    - 개발자, 디자이너, 마케터, 피엠 등 메이커 직군을 위한 채용 서비스와 그 채용 서비스에 가입한 후보자들의 메타 데이터가 적혀 있는 테이블. 여기에는 후보자의 어, 음, 이름, 포지션, 관련 스킬, 그리고 다녔던 회사가 포함되어 있습니다.
    - mock data 를 row 기준으로 100개 생성
  - 강의 자료와 inject할 수 있는 sql도 생성
  - neon mcp 로 project와 테이블 생성하기
- Clip 3: DB write tool 설계하기
  - Python implement
  - update 설계: position, skill, company 를 변경할 수 있는 tool 추가
    - delete, create 는 불가능
  - 이름은 고유한 값이니까 변경하지 않음. tool 은 변경할 수 있는 것만 사용하기. 모든 걸 다 변경할 수 있는 write tool 은 위험하다.
  - https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres 을 그대로 가져와서 코드를 수정하기
- Clip 4: 클로드에 연결해서 써보기
  - 로컬 mcp를 claude.ai 에 추가할 수 있게 .mcp.json 에 절대 경로로 작성: part4 chapter 2 clip1 강의 자료 확인

중요: 실제로 코드를 실행해보면서 강의 자료를 작성한다.
---

## Part 5. AI Agent 프로젝트 3개

### Chapter 1. <실습> 바이브코딩으로 CS 슬랙봇 구현하기
- Clip 1: 슬랙 커뮤니티 CS 내역을 LLM 으로 합성하기
  - slack mcp 사용해서 생성: Part 1 chapter 4 참조
- Clip 2: 시스템 프롬프트 만들기
  - claude.ai 의 시스템 프롬프트 https://docs.claude.com/en/release-notes/system-prompts#september-29-2025 를 확인해서 구조를 파악해서 그 원리대로 CS봇을 위한 다음 시스템 프롬프트를 작성
- Clip 3: 슬랙봇 구현 프롬프트 작성하기
  - koomook/agent-josh 를 clone 해서 여기 구현된 fastapi 기반 slackbot 을 참고해서 이것과 동일하게 구현하기 위해 PRD 문서를 작성해라
- Clip 4: 슬랙봇 구현하고 GCP CloudRun 배포하기
  - GCP CloudRun 설명
  - 문서는 짧아도 됨
- Clip 5: 슬랙에서 사용하면서 업데이트하기
  - 바이브코딩으로 변경해볼 간단한 태스크들 실행해보기

### Chapter 2. <실습> 바이브코딩으로 회사 정보 조회하는 MCP SERVER 만들기
https://github.com/Koomook/mcp_NPS_BusinessEnrollment 을 밑바닥부터 구현
클로드코드에게 프롬프트만 입력해서 바이브코딩으로
이 구현체가 없다고 생각하고 차근차근 강의하는 마음가짐으로 강의 자료를 만들어야 함

- Clip 1: data.go.kr 에서 국민연금공단 api 살펴보기
- Clip 2: api -> mcp server 구현 프롬프트 작성하기
- Clip 3: mcp server 구현하기
- Clip 4: Claude에 연결해서 사용하면서 업데이트하기

### Chapter 3. <실습> 바이브코딩으로 공공 MCP 자동 생성하고 에이전트 연결하기
https://github.com/Koomook/data-go-mcp-servers 을 밑바닥부터 구현
클로드코드에게 프롬프트만 입력해서 바이브코딩으로
이 구현체가 없다고 생각하고 차근차근 강의하는 마음가짐으로 강의 자료를 만들어야 함

- Clip 1: awslabs/mcp 구현체 이해하기
- Clip 2: mcp server 자동 생성하는 에이전틱 프로세스 만들기
- Clip 3: data.go.kr 에서 api 골라서 자동 생성하기
- Clip 4: smithery 스타일의 웹페이지 구현하기

---
## Part 6. 바이브코딩과 AI agent best practice

### Chapter 1. best practice
- Clip 1: CLAUDE.md AGENTS.md best practice 찾아서 이해하기
  - best practice들 읽고 각각의 파일 내용 가져오고 패턴 정리:
  - https://github.com/anthropics/claude-code-action/blob/main/CLAUDE.md
    https://github.com/daangn/stackflow/blob/55934da0cd4d47073dc4395e5e4967f662095e49/AGENTS.md
    https://github.com/openai/codex/blob/main/AGENTS.md
    https://github.com/apache/airflow/blob/main/AGENTS.md

- Clip 2: 바이브코딩 팁
  - https://www.youtube.com/watch?v=BJjsfNO5JTo transcript 가져와서 읽고 요약 작성하기
  - 1. `바이브코딩은 “새로운” 프로젝트에서 훨씬 효과적이에요.` 왜냐면 이미 사람이 짜놓은 코드베이스는 사람한테 맥락이 있는 경우가 많잖아요? 문서화도 생략했고, 주석도 안 달았고, 특히 제가 경험한 바로는 인프라가 치명적이었어요. 일부는 IaC, 일부는 GUI로 설정한 aws 리소스들이 있었는데 이걸 LLM에 이해시키는게 힘들었고, 그래서 전부 IaC로 바꿨습니다. 하지만 놀랍게도 전부 IaC로 바꾸는 고민을 한 시간보다 구현하는 시간이 더 짧았습니다..
  1. `기존 코드베이스에 클로드코드를 사용할 때는 하루치 토큰을 전부 문서화, 주석을 다는데 사용하시는 걸 추천드립니다.` 또 그냥 코드만 보고 문서화를 시키는게 아니라 코드에는 안 담겨있는 인간이 알고 있는 비즈니스로직도 다 알려주세요.
  2. `기존 코드베이스에 바이브코딩을 할 때는 의존성이 최대한 적은 것들부터 시작하세요`. 그걸 이 영상에서는 Leaf nodes 라고 부르는데 영상이 너무 설명을 잘해줘서 [영상을 추천드립니다!](https://youtu.be/fHWFF_pnqDk?si=cUyV0sJEhiC_l60g&t=549) 코어 아키텍처에 적용하는 코드를 내가 검토하지 않고 적용하는 건 너무 위험합니다! 
  3. 개발자분들 중에 커서나 copilot를 이미 사용하고 있다면 클로드코드를 사용하는데 어려움이 없을 거에요. 근데 꼭 꼭 써보셔야돼요. `Bash를 기가막히게 써요`. 괜히 LLM provider들이 CLI만 만드는게 아니에요. 이게 미래..
  4. CC를 써보셨다면 부차적인 팁은 큰 의미가 없는 것 같아요 사실. mcp 를 여러 개 연결해라, super claude를 써라, subagents 이런 것들이요. 이런 건 CC의 효과를 느끼면 알아서 찾아보고 적용하시더라구요.
  5. 오히려 저는 CC를 사용하면서 Deep한 `나만의 개발 환경`을 만드는게 더 중요하다고 생각합니다. git worktree 를 저는 CC를 사용하기 전에는 알지도 못했어요. CC를 병렬로 쓰려고 LLM이랑 대화하다보니까 알게 됐어요. 
      1. `저는 linear issue 이름으로 worktree를 생성하면 자동으로 linear issue 내용을 불러와서 [task.md](http://task.md) 파일을 생성`하고 이 파일을 분석하면서 세션을 시작하는 워크플로우를 만들었어요. 병렬로 여러 작업을 돌려버리기 너무 편합니다.
- Clip 3: AI Agent가 사용할 툴은 AI로 만들어야 하는 이유
  - https://www.anthropic.com/engineering/writing-tools-for-agents 읽고 강의자료로 만들기

### Chapter 2. 바이브코딩을 위한 Context/Prompt Engineering
- Clip 1: Context/Prompt Engineering 이해하기
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents 읽고 강의 자료 작성
  - single turn prompting
- Clip 2: AI의 PM이 되기
  - https://www.youtube.com/watch?v=fHWFF_pnqDk transcript 읽고 강의 자료로 만들기

### Chapter 3. <실습> 병렬 작업을 위한 git worktree
- Clip 1: git worktree 이해
  참고: 
  ```
  Run parallel Claude Code sessions with Git worktrees
Suppose you need to work on multiple tasks simultaneously with complete code isolation between Claude Code instances.
1
Understand Git worktrees

Git worktrees allow you to check out multiple branches from the same repository into separate directories. Each worktree has its own working directory with isolated files, while sharing the same Git history. Learn more in the official Git worktree documentation.
2
Create a new worktree


Copy
# Create a new worktree with a new branch 
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123
This creates a new directory with a separate working copy of your repository.
3
Run Claude Code in each worktree


Copy
# Navigate to your worktree 
cd ../project-feature-a

# Run Claude Code in this isolated environment
claude
4
Run Claude in another worktree


Copy
cd ../project-bugfix
claude
5
Manage your worktrees


Copy
# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
Tips:
Each worktree has its own independent file state, making it perfect for parallel Claude Code sessions
Changes made in one worktree won’t affect others, preventing Claude instances from interfering with each other
All worktrees share the same Git history and remote connections
For long-running tasks, you can have Claude working in one worktree while you continue development in another
Use descriptive directory names to easily identify which task each worktree is for
Remember to initialize your development environment in each new worktree according to your project’s setup. Depending on your stack, this might include:
JavaScript projects: Running dependency installation (npm install, yarn)
Python projects: Setting up virtual environments or installing with package managers
Other languages: Following your project’s standard setup process
  ```
- Clip 2: worktree 자동화 스크립트 생성하기
  claude 에게 요구사항 전달:
  1. ./wt {branch-name} worktree 사용하는 간단한 script 생성
  2. npm install or uv sync 자동 실행
  3. ../{branch-name} 으로 이동
- Clip 3: 티켓 자동 생성하고 병렬 처리하기
  - linear mcp 사용해서 태스크 자동 생성
  - linear task 업데이트하는 sub agent 생성
  - worktree 마다 task 실행

### Chapter 4. Focus on "Leaf Nodes"
https://www.youtube.com/watch?v=fHWFF_pnqDk 참고: youtube transcript mcp 활용해서 leaf nodes 관련 부분 추출해서 작성하기
- Clip 1: 바이브코딩의 리스크를 낮추기 위한 feature 선정 방법
- Clip 2: 바이브코딩으로 프로젝트를 시작하면 유리한 점
  - claude code가 코딩할 때 파일, 변수 찾는 법
  - 농협 예시

### Chapter 5. <실습> 업무 자동화 바이브코딩하는 Agent Skill
- Clip 1: Claude Skills 의 프롬프트와 코드를 동시에 사용하는 자동화 살펴보기
  - 자료: https://www.youtube.com/watch?v=IoqpBKrNaZI
        https://www.anthropic.com/news/skills
        https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
        https://github.com/anthropics/skills?tab=readme-ov-file
        https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Clip 2: Skill 만들고 Claude.ai 에 추가하기
  - https://support.claude.com/en/articles/12512198-how-to-create-custom-skills