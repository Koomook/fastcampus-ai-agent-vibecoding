# Clip 2: Langgraph RAG 구현을 위한 PRD 프롬프트 만들기

## 학습 목표
- CLAUDE.md를 통한 기존 코드 컨텍스트 제공 방법 익히기
- Langgraph 기반 RAG 시스템의 요구사항 정리하기
- Routing 기반 워크플로우 설계 이해하기
- 바이브 코딩에 최적화된 간결한 PRD 작성 익히기

## 구현 목표

**Langgraph 기반 Routing RAG CLI 시스템**
- 질문 분석하여 검색 필요 여부 판단 (Routing)
- 필요시 Hybrid Search로 대출 상품 검색
- 불필요시 LLM 직접 답변
- Python CLI로 간편하게 실행

## CLAUDE.md로 기존 코드 알려주기

Chapter 2에서는 Chapter 1의 Hybrid Search 구현을 재사용합니다. Claude Code에게 기존 코드의 위치와 구조를 알려주기 위해 **CLAUDE.md**를 작성합니다.

### CLAUDE.md란?

**CLAUDE.md**는 Claude Code가 프로젝트를 이해하는 데 필요한 컨텍스트를 제공하는 프로젝트별 가이드 파일입니다.

**역할:**
- 프로젝트 구조와 핵심 파일 위치 안내
- 재사용할 코드와 함수 설명
- 기술 스택 및 데이터베이스 정보 제공
- 구현 시 주의사항 명시

### CLAUDE.md 초기화 및 작성

**1. CLAUDE.md 파일 생성**
```
/init
```

**2. CLAUDE.md 맥락 주입**

```markdown
- 데이터베이스 관련 정보
- OpenAI GPT-5-mini 모델 정보
   - (2025년 8월 출시)
- 프로젝트 목표를 RAG 개발로 수정
```

**3. Claude Code에서 CLAUDE.md 확인**

Claude Code는 프로젝트 디렉토리의 CLAUDE.md를 자동으로 인식하고 참고합니다.

```bash
# Claude Code 실행
claude

# CLAUDE.md 기반으로 작업 시작
# Claude가 자동으로 Chapter 1의 코드 구조를 이해하고 재사용할 수 있음
```

## PRD 작성 전략

### Chapter 1과의 차이점

**Chapter 1 (Hybrid Search):**
- 목표: Hybrid Search 엔진 구현
- 핵심: Vector Search + BM25 + RRF

**Chapter 2 (Langgraph RAG):**
- 목표: Routing 기반 RAG 워크플로우 구현
- 핵심: Langgraph + Routing + Hybrid Search 재사용

### 바이브 코딩용 PRD 작성법

**핵심 원칙:**
1. **간결성**: 핵심만 명시, 세부 구현은 AI에게
2. **명확성**: 기술 스택과 참고 자료 명확히
3. **맥락 제공**: CLAUDE.md로 기존 코드 위치와 재사용 방법 안내

## PRD: Langgraph RAG CLI 구현

### 스펙

- Python 3.10+, uv 패키지 매니저
- Langgraph (워크플로우 오케스트레이션)
- LangChain, langchain-openai
- hybrid_search.py 사용
- OpenAI GPT-5-mini (2025년 8월 출시, 라우팅 및 답변 생성)

### 워크플로우 설계

```
사용자 질문
    ↓
Route Node (검색 필요 여부 판단)
    ↓               ↓
검색 필요        일반 질문
    ↓               ↓
Retrieve Node    Generate Node
    ↓               ↓
Generate Node     답변
    ↓
  답변
```

**노드 정의:**

1. **Route Node**: 질문 분석
   - LLM으로 검색 필요 여부 판단
   - "search" 또는 "direct" 반환

2. **Retrieve Node**: 컨텍스트 검색
   - Chapter 1의 Hybrid Search 사용
   - Top-3 문서 검색

3. **Generate Node**: 답변 생성
   - search: 검색 결과 기반 RAG 답변
   - direct: LLM 직접 답변

### 핵심 기능

**1. Hybrid Search 통합**
   - Chapter 1의 Vector Search + BM25 + RRF 로직 재사용
   - Top-3 문서 검색

**2. Langgraph 워크플로우**
   - Route Node: LLM으로 검색 필요 여부 판단
   - Retrieve Node: Hybrid Search로 컨텍스트 수집
   - Generate Node: 최종 답변 생성

**3. State 관리**
   - 질문, 라우팅 결과, 검색 컨텍스트, 답변을 상태로 관리

### CLI 동작

```bash
# 검색이 필요한 질문
uv run python langgraph_rag.py "의사 전용 대출 상품 알려줘"
# → Route: search → Hybrid Search → RAG 답변

# 일반 질문
uv run python langgraph_rag.py "안녕하세요"
# → Route: direct → LLM 직접 답변

# 디버그 모드
uv run python langgraph_rag.py "질문" --debug
# → Routing 정보와 검색된 Context 표시
```

## PRD 프롬프트 완성본

### CLAUDE.md 없이 작성한 경우

```
스펙:
- Python 3.10+, uv
- Langgraph, LangChain, langchain-openai
- PostgreSQL (Chapter 1과 동일)
- GPT-5-mini (2025년 8월 출시)

목표:
Routing 기반 Langgraph RAG CLI 구현

워크플로우:
1. Route: 질문 분석 → search/direct 판단
2. Retrieve: Hybrid Search로 top-3 검색 (search인 경우)
3. Generate: 컨텍스트 기반 답변 또는 직접 답변

핵심 구현:
- StateGraph로 노드 정의 (route, retrieve, generate)
- conditional_edges로 routing
- Chapter 1의 Hybrid Search 로직 참고
- State: question, route, context, answer

CLI:
uv run python langgraph_rag.py "질문" [--debug]

참고:
- Langgraph: https://langchain-ai.github.io/langgraph/
- Chapter 1: hybrid_search/hybrid_search.py
```

### CLAUDE.md 작성 후 간결한 버전

CLAUDE.md에 기존 코드 정보를 제공했으므로, PRD는 훨씬 간결해집니다.

```
스펙:
- Langgraph, LangChain, langchain-openai
- GPT-5-mini

목표:
Routing 기반 Langgraph RAG CLI 구현

워크플로우:
1. Route: 질문 분석 → search/direct 판단
2. Retrieve: Hybrid Search로 top-3 검색
3. Generate: 답변 생성

핵심 구현:
- StateGraph로 노드 정의 (route, retrieve, generate)
- conditional_edges로 routing

CLI:
uv run python langgraph_rag.py "질문" [--debug]

참고:
- langgraph 구현할 때에는 context7으로 최신 개발 문서 확인
```

**개선 포인트:**
- PostgreSQL, Chapter 1 참조 등 CLAUDE.md에 명시된 정보 제거
- 워크플로우 설명 간소화 (세부 조건 제거)
- State 정의 생략 (구현 시 자동으로 파악 가능)
- 프롬프트 길이 약 40% 단축

---

**참고 자료:**
- Langgraph Documentation: https://langchain-ai.github.io/langgraph/
