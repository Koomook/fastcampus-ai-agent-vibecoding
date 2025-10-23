"""
Langgraph 기반 Routing RAG CLI
질문 분석 → 검색 필요 여부 판단 → Hybrid Search → 답변 생성
"""
import os
import sys
import argparse
from datetime import datetime
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from hybrid_search import hybrid_search

# 환경변수 로드
load_dotenv()

# LLM 초기화 (GPT-5-mini)
llm = ChatOpenAI(model="gpt-5-mini", temperature=0)


# ===== 개선된 시스템 프롬프트 =====

# 시스템 프롬프트: 농협 대출 상담 전문가 페르소나
SYSTEM_PROMPT = """당신은 농협 대출 상품 전문 상담사입니다.
검색된 대출 상품 정보를 바탕으로 고객의 질문에 정확하고 친절하게 답변합니다.

답변 원칙:
1. 제공된 문서 정보만을 기반으로 답변
2. 불확실한 정보는 명시적으로 표시
3. 상품 비교 시 핵심 차이점 강조
4. 구체적인 수치와 조건 명시
5. 추가 상담이 필요한 경우 안내
"""

# Few-shot 예시: 질문 유형별 모범 답변 패턴
FEW_SHOT_EXAMPLES = """
[좋은 답변 예시]
Q: 의사 전용 대출이 있나요?
A: 네, 농협에는 의사 전용 대출 상품이 있습니다. [상품1]
   - 상품명: 전문직종사자대출
   - 대상: 의사, 한의사, 치과의사 등 의료인
   - 한도: 최대 5억원
   - 특징: 소득 증빙 간소화, 우대금리 적용

Q: 이 상품은 누가 신청할 수 있나요?
A: 해당 상품의 신청 대상은 다음과 같습니다. [상품2]
   필수 조건:
   - 만 19세 이상 성인
   - 재직기간 6개월 이상

   우대 조건:
   - 농협 급여이체 고객
   - 신용등급 1~3등급

   정확한 심사 기준은 농협 지점(1588-2100)으로 문의하시기 바랍니다.

[피해야 할 답변]
- "아마도 ~일 것 같습니다" (모호한 추측)
- "일반적으로 ~합니다" (검색 결과에 없는 일반론)
- 출처 표시 없이 정보 제공
"""

# 인용 및 출처 명시 강제
CITATION_PROMPT = """
[답변 형식 규칙]
1. 각 정보 뒤에 [상품N] 형태로 출처를 반드시 표시하세요.
2. 여러 상품의 공통 정보는 [상품1,2,3] 형태로 표시하세요.
3. 검색 결과에 없는 정보는 "제공된 정보에서 확인되지 않습니다"라고 명시하세요.
4. 불확실한 경우 "정확한 정보는 농협 지점 또는 콜센터(1588-2100)로 문의하세요"라고 안내하세요.
"""

# 안전장치 및 면책 사항
DISCLAIMER_TEMPLATE = """
[중요 안내사항]
- 최종 대출 조건은 신용평가 및 담보 평가 결과에 따라 달라질 수 있습니다.
- 정확한 금리와 한도는 농협 지점 방문 또는 콜센터(1588-2100) 상담을 통해 확인하세요.
- 본 정보는 {current_date} 기준이며, 상품 내용은 변경될 수 있습니다.
"""


# State 정의
class State(TypedDict):
    """RAG 워크플로우 상태"""
    question: str
    route_decision: str  # "search" or "direct"
    documents: list
    answer: str
    debug: bool


def route_node(state: State) -> State:
    """
    Route 노드: 질문을 분석하여 검색 필요 여부 판단
    """
    question = state["question"]
    debug = state.get("debug", False)

    if debug:
        print("\n[DEBUG] Route Node: Analyzing question...")

    # LLM으로 질문 분석
    messages = [
        SystemMessage(content="""당신은 질문을 분석하는 전문가입니다.
사용자의 질문이 농협 대출 상품에 대한 구체적인 정보를 요구하는지 판단하세요.

- 대출 상품 검색이 필요한 경우: "search"
- 일반적인 질문이나 인사말: "direct"

예시:
- "의사 전용 대출이 있나요?" → search
- "공무원 대출 한도는?" → search
- "안녕하세요" → direct
- "대출이란 무엇인가요?" → direct

반드시 "search" 또는 "direct" 중 하나만 답변하세요."""),
        HumanMessage(content=question)
    ]

    response = llm.invoke(messages)
    route_decision = response.content.strip().lower()

    # "search" 또는 "direct"만 허용
    if "search" in route_decision:
        route_decision = "search"
    else:
        route_decision = "direct"

    if debug:
        print(f"[DEBUG] Route Decision: {route_decision}")

    return {**state, "route_decision": route_decision}


def retrieve_node(state: State) -> State:
    """
    Retrieve 노드: Hybrid Search로 top-3 문서 검색
    """
    question = state["question"]
    debug = state.get("debug", False)

    if debug:
        print("\n[DEBUG] Retrieve Node: Running hybrid search...")

    # Hybrid Search 실행 (top-3)
    results = hybrid_search(question, limit=3)

    if debug:
        print(f"[DEBUG] Found {len(results)} documents")
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc['product_name']} (score: {doc['rrf_score']:.4f})")

    return {**state, "documents": results}


def generate_node(state: State) -> State:
    """
    Generate 노드: 답변 생성
    검색이 필요한 경우 문서 기반 답변, 아니면 직접 답변
    개선된 프롬프트 적용 (Few-shot, Citation, Disclaimer)
    """
    question = state["question"]
    route_decision = state["route_decision"]
    documents = state.get("documents", [])
    debug = state.get("debug", False)

    if debug:
        print("\n[DEBUG] Generate Node: Creating answer...")

    if route_decision == "search":
        # 검색된 문서 기반 답변 생성
        if not documents:
            answer = "죄송합니다. 관련 대출 상품을 찾을 수 없습니다. 다른 검색어로 다시 시도해주세요."
        else:
            # 문서 정보를 개선된 컨텍스트로 구성
            context_parts = []
            for i, doc in enumerate(documents, 1):
                context_parts.append(f"""
[상품{i}] {doc['product_name']}
- 상품코드: {doc['product_code']}
- 요약: {doc['product_summary']}
- 대상: {doc.get('target_description', '정보 없음')}
- 한도: {doc.get('loan_limit_description', '정보 없음')}
- 검색 관련도(RRF): {doc['rrf_score']:.4f}
""".strip())

            context = "\n\n".join(context_parts)

            # 검색 메타데이터 추가
            max_score = max([doc['rrf_score'] for doc in documents])
            if max_score > 0.05:
                confidence = "높음"
                confidence_note = "검색 결과가 질문과 매우 관련성이 높습니다."
            elif max_score > 0.02:
                confidence = "보통"
                confidence_note = "검색 결과가 질문과 어느 정도 관련이 있습니다."
            else:
                confidence = "낮음"
                confidence_note = "검색 결과의 관련성이 낮을 수 있습니다. 보다 구체적인 질문이나 다른 검색어를 시도해보세요."

            metadata = f"""
[검색 정보]
- 검색 방법: 하이브리드 검색 (BM25 키워드 + 벡터 유사도)
- 검색된 상품 수: {len(documents)}
- 최고 관련도: {max_score:.4f}
- 검색 신뢰도: {confidence}
- 참고사항: {confidence_note}
""".strip()

            # 현재 날짜 및 면책 사항
            current_date = datetime.now().strftime("%Y년 %m월 %d일")
            disclaimer = DISCLAIMER_TEMPLATE.format(current_date=current_date)

            # 최종 프롬프트 구성
            user_prompt = f"""
{FEW_SHOT_EXAMPLES}

{CITATION_PROMPT}

{metadata}

[검색된 대출 상품 정보]
{context}

[사용자 질문]
{question}

위 정보를 바탕으로 정확하고 친절하게 답변해주세요.
반드시 출처([상품N])를 명시하고, 아래 안내사항을 답변 마지막에 포함하세요.

{disclaimer}
""".strip()

            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_prompt)
            ]

            response = llm.invoke(messages)
            answer = response.content
    else:
        # 직접 답변
        messages = [
            SystemMessage(content="당신은 친절한 농협 대출 상담사입니다. 사용자의 질문에 간단하고 친절하게 답변하세요."),
            HumanMessage(content=question)
        ]

        response = llm.invoke(messages)
        answer = response.content

    if debug:
        print(f"[DEBUG] Answer generated: {len(answer)} characters")

    return {**state, "answer": answer}


def should_retrieve(state: State) -> Literal["retrieve", "generate"]:
    """
    조건부 엣지: route_decision에 따라 retrieve 또는 generate로 라우팅
    """
    route_decision = state["route_decision"]
    if route_decision == "search":
        return "retrieve"
    return "generate"


def build_graph() -> StateGraph:
    """
    Langgraph 워크플로우 구성
    """
    # StateGraph 생성
    workflow = StateGraph(State)

    # 노드 추가
    workflow.add_node("route", route_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)

    # 엣지 정의
    workflow.add_edge(START, "route")

    # 조건부 엣지: route → retrieve or generate
    workflow.add_conditional_edges(
        "route",
        should_retrieve,
        {
            "retrieve": "retrieve",
            "generate": "generate"
        }
    )

    # retrieve → generate
    workflow.add_edge("retrieve", "generate")

    # generate → END
    workflow.add_edge("generate", END)

    # 컴파일
    return workflow.compile()


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(description="Langgraph Routing RAG CLI")
    parser.add_argument("question", type=str, help="질문 입력")
    parser.add_argument("--debug", action="store_true", help="디버그 모드")

    args = parser.parse_args()

    # 그래프 빌드
    app = build_graph()

    # 초기 상태
    initial_state = {
        "question": args.question,
        "route_decision": "",
        "documents": [],
        "answer": "",
        "debug": args.debug
    }

    # 워크플로우 실행
    if args.debug:
        print("="*80)
        print("Langgraph Routing RAG")
        print("="*80)
        print(f"\n질문: {args.question}\n")

    result = app.invoke(initial_state)

    # 결과 출력
    print("\n" + "="*80)
    print("답변")
    print("="*80)
    print(result["answer"])
    print()


if __name__ == "__main__":
    main()
