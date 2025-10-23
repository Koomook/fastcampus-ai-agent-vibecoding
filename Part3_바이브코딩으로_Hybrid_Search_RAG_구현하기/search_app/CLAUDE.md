# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요
농협 대출 상품에 대한 하이브리드 검색 기반 RAG(Retrieval-Augmented Generation) 시스템입니다. BM25 키워드 검색과 벡터 유사도 검색을 RRF(Reciprocal Rank Fusion)로 결합하여 최적의 문서를 검색하고, 이를 기반으로 LLM이 사용자 질문에 답변을 생성합니다.

**프로젝트는 두 가지 구현을 포함합니다:**
1. **Langgraph Workflow RAG** (`langgraph_rag.py`): 고정된 경로를 따르는 워크플로우 방식
2. **Agent RAG** (`agent_app/`): LLM이 자율적으로 도구를 선택하는 에이전트 방식

## 필수 명령어

### 의존성 설치
```bash
uv sync
```

### 데이터 로드
데이터베이스에 loan_products.json을 로드하고 임베딩 생성:
```bash
uv run python load_data.py
```

선택적으로 처음 N개만 로드:
```bash
uv run python load_data.py 10
```

### 하이브리드 검색 실행
```bash
uv run python hybrid_search.py "검색어"
```

예시:
```bash
uv run python hybrid_search.py "의사 전용 대출"
uv run python hybrid_search.py "공무원 생활안정자금"
```

RAG 답변 생성:
```bash
uv run python hybrid_search.py "의사 전용 대출" --rag
```

### Langgraph 기반 Routing RAG 실행
Langgraph를 사용한 고급 RAG 시스템으로, 질문을 자동으로 분석하여 검색이 필요한지 판단합니다.

기본 실행:
```bash
uv run python langgraph_rag.py "의료인 대출 상품 추천해줘"
```

디버그 모드로 실행 (워크플로우 과정 확인):
```bash
uv run python langgraph_rag.py "공무원 전용 대출" --debug
```

**Langgraph RAG의 특징**:
- **자동 라우팅**: 질문이 검색이 필요한지 자동 판단 (route → retrieve → generate)
- **Few-shot 프롬프트**: 모범 답변 예시를 통한 고품질 응답
- **출처 명시**: 모든 정보에 [상품N] 형태로 출처 표시
- **검색 신뢰도**: 하이브리드 검색 점수 기반 신뢰도 평가
- **면책 사항**: 답변에 자동으로 최신 정보 확인 안내 포함

### Agent RAG 실행 (agent_app/)
OpenAI Function Calling을 사용하여 LLM이 자율적으로 도구를 선택하는 Agent 시스템입니다.

**도구 테스트:**
```bash
cd agent_app
uv run python test_tools.py
```

**프론트엔드 실행:**
```bash
cd agent_app
pnpm install  # 최초 1회만
pnpm dev      # 개발 서버 실행
```

서버 실행 후 브라우저에서 `http://localhost:3000` 접속

**Agent RAG의 특징**:
- **동적 도구 선택**: LLM이 상황에 따라 적절한 도구 자동 선택
- **Hybrid Search Tool**: 농협 대출 상품 검색 (내부 DB)
- **Tavily Search Tool**: 최신 금융 정보 웹 검색
- **유연한 확장**: 새 도구 추가 시 코드 수정 최소
- **실시간 스트리밍**: Data Stream Protocol로 답변 실시간 생성

### 모델 설정 검증 테스트
**중요**: 코드를 수정한 후 반드시 아래 테스트를 실행하여 올바른 모델이 설정되었는지 확인하세요.

```bash
uv run python test_model_config.py
```

이 테스트는 다음을 검증합니다:
- RAG 응답 생성에 `gpt-5-mini` 모델이 사용되는지 확인
- 임베딩 생성에 `text-embedding-3-small` 모델이 사용되는지 확인
- 잘못된 모델명이 사용된 경우 오류 출력 및 수정 가이드 제공

## 아키텍처

### 핵심 구성 요소

1. **데이터 로드 파이프라인** (`load_data.py`)
   - JSON 파일을 읽어 PostgreSQL에 저장
   - `clean_text()`: 특수문자를 제거하여 BM25 검색용 텍스트 생성
   - `get_embedding()`: OpenAI text-embedding-3-small 모델로 임베딩 생성
   - 각 대출 상품에 대해 `searchable_text`와 `cleaned_searchable_text`, `searchable_text_embedding` 생성

2. **하이브리드 검색 시스템** (`hybrid_search.py`)
   - **BM25 검색** (`bm25_search()`): pg_search의 BM25 인덱스 사용, ngram 토크나이저로 한글 지원
   - **벡터 검색** (`vector_search()`): pgvector의 코사인 유사도 사용
   - **RRF 결합** (`reciprocal_rank_fusion()`): 두 검색 결과를 k=60으로 결합

3. **Langgraph 기반 Routing RAG** (`langgraph_rag.py`)
   - **Route Node**: LLM으로 질문 분석 후 검색 필요 여부 자동 판단
   - **Retrieve Node**: 검색이 필요한 경우 `hybrid_search()` 호출하여 top-3 문서 검색
   - **Generate Node**: Few-shot 프롬프트와 검색된 문서 기반으로 답변 생성
   - **개선된 프롬프트 엔지니어링**:
     - 농협 대출 상담 전문가 페르소나
     - Few-shot 예시로 답변 품질 향상
     - 출처 명시 강제 ([상품N] 형태)
     - 검색 신뢰도 평가 및 메타데이터 제공
     - 면책 사항 자동 포함

4. **Agent 기반 RAG** (`agent_app/`)
   - **FastAPI 백엔드** (`api/index.py`): OpenAI Function Calling 기반 스트리밍 API
   - **도구 시스템** (`api/utils/tools.py`):
     - `hybrid_search_tool`: 농협 대출 상품 검색 (기존 hybrid_search.py 활용)
     - `tavily_search_tool`: Tavily API를 통한 웹 검색 (최신 금융 정보)
   - **Next.js 프론트엔드**: Vercel AI SDK 기반 채팅 UI
   - **Data Stream Protocol**: 실시간 스트리밍 응답 (`0:text`, `9:tool_call`, `a:tool_result`)
   - **자율적 도구 선택**: LLM이 질문에 따라 적절한 도구를 자동으로 선택하고 조합

### 데이터베이스 구조

- **데이터베이스**: Neon PostgreSQL
- **확장**: pgvector (벡터 검색), pg_search (BM25 전문 검색)
- **테이블**: `loan_products`
  - `searchable_text`: 원본 검색 대상 텍스트
  - `cleaned_searchable_text`: 특수문자 제거된 BM25 검색용 텍스트
  - `searchable_text_embedding`: vector(1536) 임베딩

## 환경 변수

**루트 디렉토리** (`./.env`):
- `DATABASE_URL`: Neon PostgreSQL 연결 문자열
- `OPENAI_API_KEY`: OpenAI API 키

**Agent 앱** (`agent_app/.env.local`):
- `DATABASE_URL`: Neon PostgreSQL 연결 문자열
- `OPENAI_API_KEY`: OpenAI API 키
- `TAVILY_API_KEY`: Tavily 웹 검색 API 키 (선택사항, https://tavily.com/ 에서 무료 발급 가능)

## 데이터 소스

`loan_products.json` 파일은 상위 디렉토리(`../loan_products.json`)에 위치해야 합니다.

## 중요 구현 세부사항

- **한글 검색 지원**: BM25 인덱스에서 ngram 토크나이저(min_gram=2, max_gram=3) 사용
- **인덱스 자동 생성**: `bm25_search()` 실행 시 BM25 인덱스가 없으면 자동 생성
- **텍스트 정제**: 한글, 영문, 숫자, 공백만 남기고 특수문자 제거
- **코사인 유사도**: pgvector의 `<=>` 연산자 사용

## NOTES
- **OpenAI 모델은 반드시 gpt-5-mini를 사용해라.** 이 모델은 2025년 8월 출시된 최신 모델이다. 너의 지식 컷오프는 2025년 1월이다.
- **코드 수정 후 필수 작업**: `uv run python test_model_config.py`를 실행하여 올바른 모델(gpt-5-mini)이 설정되었는지 반드시 검증하라.
- 임베딩 모델은 `text-embedding-3-small`을 사용한다. 이것은 변경하지 말 것.

## Agent vs Workflow 차이점

### Workflow (langgraph_rag.py)
- **고정된 경로**: Route → Retrieve → Generate 순서로 실행
- **명시적 제어**: 각 단계가 코드로 명확히 정의됨
- **예측 가능**: 같은 입력에 항상 같은 경로 실행
- **확장 제한**: 새 기능 추가 시 노드와 엣지 수정 필요

### Agent (agent_app/)
- **동적 선택**: LLM이 상황에 따라 도구를 자율적으로 선택
- **유연한 대응**: 예상치 못한 질문에도 적절한 도구 조합 사용
- **확장 용이**: 새 도구 추가 시 tools 배열에만 등록하면 됨
- **자연스러운 대화**: 도구 호출이 대화 흐름에 자연스럽게 통합

**사용 시나리오:**
- 단순 대출 검색: Workflow와 Agent 모두 적합
- 복합 질문 (대출 + 시장 동향): Agent가 더 유연하게 대응
- 다단계 추론: Agent가 필요에 따라 여러 도구를 순차적으로 사용