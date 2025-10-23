# 농협 대출 상담 Agent

농협 대출 상품 검색과 최신 금융 정보를 제공하는 AI Agent입니다.

## 주요 기능

### 🔍 하이브리드 검색 (Hybrid Search)
- 농협 대출 상품 데이터베이스 검색
- BM25 키워드 검색 + 벡터 유사도 검색을 RRF로 결합
- 대출 상품명, 대상, 금리, 한도 등을 정확하게 검색

### 🌐 웹 검색 (Tavily Search)
- 최신 금융 정보, 기준금리, 시장 동향 검색
- Tavily API를 사용한 고품질 웹 검색
- 실시간 뉴스 및 최신 정책 정보 제공

### 🤖 Agent 자율 실행
- LLM이 질문에 따라 자동으로 적절한 도구 선택
- 필요시 여러 도구를 조합하여 답변 생성
- 사용자에게 자연스러운 대화 경험 제공

## 설치 및 실행

### 1. 환경 설정

`.env.local` 파일을 생성하고 API 키를 설정하세요:

```bash
# OpenAI API Key (필수)
OPENAI_API_KEY=your_openai_api_key_here

# Database URL (필수)
DATABASE_URL=your_database_url_here

# Tavily API Key (선택)
# https://tavily.com/ 에서 무료 API 키 발급 (월 1000건 무료)
TAVILY_API_KEY=tvly-your_tavily_api_key_here
```

### 2. 의존성 설치

**Python 패키지 (백엔드):**
```bash
# 상위 디렉토리에서 실행 (hybrid_search.py가 있는 위치)
cd ..
uv sync
```

**Node.js 패키지 (프론트엔드):**
```bash
# agent_app 디렉토리에서 실행
cd agent_app
pnpm install
```

### 3. 데이터베이스 설정

대출 상품 데이터를 로드합니다:

```bash
cd ..
uv run python load_data.py
```

### 4. 개발 서버 실행

```bash
cd agent_app
pnpm dev
```

브라우저에서 `http://localhost:3000` 접속

## Agent 도구 설명

### hybrid_search_tool
- **용도**: 농협 대출 상품 검색
- **입력**:
  - `query`: 검색 키워드 (예: "의사 전용 대출")
  - `limit`: 결과 개수 (기본값: 3)
- **예시 질문**:
  - "의사 전용 대출 상품 추천해줘"
  - "공무원 대출 금리가 어떻게 되나요?"
  - "중소기업 대출 한도는?"

### tavily_search_tool
- **용도**: 웹에서 최신 금융 정보 검색
- **입력**:
  - `query`: 검색 키워드 (예: "2025년 기준금리")
  - `max_results`: 결과 개수 (기본값: 3)
- **예시 질문**:
  - "2025년 기준금리는 어떻게 되나요?"
  - "최근 대출 시장 동향은?"
  - "한국은행 금리 인상 소식 알려줘"

## Agent vs Workflow 차이점

### Workflow (langgraph_rag.py)
- **고정된 경로**: Route → Retrieve → Generate
- **명시적 제어**: 코드로 모든 단계 정의
- **예측 가능**: 항상 동일한 흐름

### Agent (이 프로젝트)
- **동적 도구 선택**: LLM이 필요한 도구를 자율적으로 선택
- **유연한 대응**: 예상치 못한 질문에도 적응
- **확장 용이**: 새 도구 추가 시 코드 수정 최소

## 기술 스택

- **백엔드**: FastAPI, OpenAI Function Calling
- **프론트엔드**: Next.js, Vercel AI SDK
- **데이터베이스**: PostgreSQL (Neon), pgvector, pg_search
- **검색**: BM25 + Vector Search (RRF)
- **웹 검색**: Tavily API

## 프로젝트 구조

```
agent_app/
├── api/
│   ├── index.py              # FastAPI 메인 엔드포인트
│   └── utils/
│       ├── tools.py          # Agent 도구 (hybrid_search, tavily_search)
│       └── prompt.py         # 프롬프트 변환 유틸
├── app/                      # Next.js 페이지
├── components/               # React 컴포넌트
└── .env.local               # 환경 변수
```

## 참고 자료

- [Vercel AI SDK](https://sdk.vercel.ai/docs)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Tavily Search API](https://docs.tavily.com/)
- [LangGraph Agents vs Workflows](https://langchain-ai.github.io/langgraph/tutorials/workflows/)
