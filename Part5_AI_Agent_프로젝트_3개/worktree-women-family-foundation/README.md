# 강의 커리큘럼

## Part 1. AI 에이전트와 바이브코딩 입문

### Chapter 1. 바이브코딩으로 AI 에이전트 시작하기
- Clip 1: 강의를 통해 얻어갈 수 있는 것
- Clip 2: CLI기반 Claude Code 와 Codex로 할 수 있는 것
- Clip 3: AI 에이전트 + MCP 기술이 주목받는 이유
- Clip 4: Docs와 실습코드(Github)

### Chapter 2. Claude Code, Codex 기본 세팅하기
- Clip 1: 설치와 기본 사용법
- Clip 2: Local/Project/User 단위 mcp 연결하기
- Clip 3: CLAUDE.md, AGENTS.md 세팅하기

### Chapter 3. Claude Code 개발을 위한 커스텀 환경 세팅하기
- Clip 1: Slash Command 만들기
- Clip 2: Sub Agent 만들기
- Clip 3: Hooks, Output Styles 설계하기

### Chapter 4. <실습> 슬랙 메시지 읽고 notion 에 태스크 저장하는 커맨드 설계
- Clip 1: 클로드코드로 자동화하기
- Clip 2: 슬래쉬 커맨드를 자동으로 업데이트하기


## Part 2. 바이브코딩으로 AI 에이전트 구현하기

### Chapter 1. Agent 개념 이해하기
- Clip 1: Agent vs Workflow 개념 이해하기
- Clip 2: AI Agent architecture 자세히 살펴보기

### Chapter 2. LLM api 호출 이해하기
- Clip 1: LLM api 이해하고 호출해보기
- Clip 2: 세부 파라미터 (reasoning_effort, verbosity, max_token)
- Clip 3: 프롬프트 작성

### Chapter 3. mcp client 사용하기
- Clip 1: Claude Code 등 에이전트가 어떻게 mcp를 활용하는지 보기
- Clip 2: 오픈소스 AI AGENT의 mcp 활용 코드 까보기
- Clip 3: Tool 이해하기
- Clip 4: MCP client 개념 이해하기

### Chapter 4. <실습> 바이브코딩으로 mcp + AI 에이전트 만들기
- Clip 1: mcp client 를 구현하기 위한 PRD 프롬프트 만들기
- Clip 2: mcp client 구현하기


## Part 3. 바이브코딩으로 Hybrid Search RAG 구현하기

### Chapter 1. <실습> Postgresql 기반 Hybrid Search 구현하기
- Clip 1: Vector Search 이해하기
- Clip 2: BM25 이해하기
- Clip 3: PRD 프롬프트 만들기
- Clip 4: Hybrid Search 구현하기

### Chapter 2. <실습> Langgraph 기반 workflow RAG 구현하기
- Clip 1: RAG 개념 이해하기
- Clip 2: PRD 프롬프트 만들기
- Clip 3: Langgraph RAG 구현하기

### Chapter 3. <실습> 바이브코딩으로 Agentic RAG 구현하기
- Clip 1: workflow -> Agentic의 개념 복기하기
- Clip 2: Database와 Web Search를 툴로 사용하는 에이전트 구현하기


## Part 4. 바이브코딩으로 MCP server 구현하기

### Chapter 1. MCP server 이해하기
- Clip 1: MCP server의 개념과 구조 이해하기
- Clip 2: MCP server 코드 까보기: sequential thinking, notion, playwright

### Chapter 2. <실습> MCP server 구현하고 Claude에 연결하기
- Clip 1: dummy MCP server 구현하기
- Clip 2: Claude, Claude code 에 연결하기

### Chapter 3. <실습> 우리 회사 DB를 쿼리하는 mcp server 구현하기
- Clip 1: Postgresql mcp server 구현체 보기
- Clip 2: mock 스키마 만들고 데이터 합성해서 집어넣기
- Clip 3: DB write tool 설계하기
- Clip 4: 클로드에 연결해서 써보기


## Part 5. AI Agent 프로젝트 3개

### Chapter 1. <실습> 바이브코딩으로 CS 슬랙봇 구현하기
- Clip 1: 슬랙 커뮤니티 CS 내역을 LLM 으로 합성하기
- Clip 2: 시스템 프롬프트 만들기
- Clip 3: 슬랙봇 구현 프롬프트 작성하기
- Clip 4: 슬랙봇 구현하고 AWS lambda 배포하기
- Clip 5: 슬랙에서 사용하면서 업데이트하기

### Chapter 2. <실습> 바이브코딩으로 회사 정보 조회하는 MCP SERVER 만들기
- Clip 1: data.go.kr 에서 국민연금공단 api 살펴보기
- Clip 2: api -> mcp server 구현 프롬프트 작성하기
- Clip 3: mcp server 구현하기
- Clip 4: Claude에 연결해서 사용하면서 업데이트하기

### Chapter 3. <실습> 바이브코딩으로 공공 MCP 자동 생성하고 에이전트 연결하기
- Clip 1: awslabs/mcp 구현체 이해하기
- Clip 2: mcp server 자동 생성하는 에이전틱 프로세스 만들기
- Clip 3: data.go.kr 에서 api 골라서 자동 생성하기
- Clip 4: smithery 스타일의 웹페이지 구현하기


## Part 6. 바이브코딩과 AI agent best practice

### Chapter 1. CLAUDE.md, AGENTS.md best practice
- Clip 1: best practice 찾아서 이해하기
- Clip 2: 바이브코딩 팁을 자동화시키기
- Clip 3: 클로드 코드 시스템 프롬프트 계층 이해하기

### Chapter 2. 바이브코딩을 위한 Context/Prompt Engineering
- Clip 1: Context/Prompt Engineering 이해하기
- Clip 2: AI의 PM이 되기

### Chapter 3. <실습> 병렬 작업을 위한 git worktree
- Clip 1: git worktree 이해
- Clip 2: worktree 자동화 스크립트 생성하기
- Clip 3: 티켓 자동 생성하고 병렬 처리하기

### Chapter 4. Focus on "Leaf Nodes"
- Clip 1: 바이브코딩의 리스크를 낮추기 위한 feature 선정 방법
- Clip 2: 바이브코딩으로 프로젝트를 시작하면 유리한 점

### Chapter 5. <실습> 클로드코드를 활용해서 AI 리터러시 높이기 - 마지막 제언
- Clip 1: 클로드코드를 나만의 AI 에이전트로 사용하기
- Clip 2: 메타 프롬프트