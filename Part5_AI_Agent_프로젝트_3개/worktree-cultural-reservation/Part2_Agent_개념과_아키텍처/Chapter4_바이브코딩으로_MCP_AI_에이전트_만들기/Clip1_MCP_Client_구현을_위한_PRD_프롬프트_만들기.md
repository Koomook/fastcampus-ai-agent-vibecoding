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

# Clip 1: MCP Client 구현을 위한 PRD 프롬프트 만들기

## 학습 목표
- PRD(Product Requirements Document) 기반 AI 프롬프트 작성법 이해하기
- Context7 MCP를 활용한 정확한 기술 스택 정보 참조 방법 배우기
- Context window 최대로 사용 가능한 PRD 프롬프트 작성 전략 익히기

## PRD란 무엇인가?

**PRD(Product Requirements Document)**는 제품 개발 전 작성하는 요구사항 명세서입니다.

### AI 시대의 PRD 변화
```
전통: 기획자/PM → PRD 작성 → 개발자 → 코드 구현
AI 시대: 개발자 → PRD 프롬프트 작성 → AI 에이전트 → 코드 생성
```

**핵심 차이점:**
- 사람용 PRD: 배경, 목적, 비즈니스 맥락 중심
- AI용 PRD: 명확한 스펙, 입출력, 제약사항, 필요한 맥락 중심

## 왜 PRD 프롬프트가 중요한가?

AI 에이전트는 사람이 아니기 때문에 **필요한 모든 맥락을 명확하게 제공**해야 합니다.

**나쁜 예시:**
```
MCP client를 만들어줘
```

**좋은 예시:**
```
Python MCP SDK를 사용해서 stdio 방식으로 통신하는
weather-api MCP server에 연결하는 client를 구현해줘.
connect, list_tools, call_tool 메서드 필요.
```

## PRD 작성 전략

### 1. 명확한 스펙 제공
- Python 버전, SDK, 패키지 매니저 등 구체적 명시
- 정확한 링크 제공 (라이브러리 이름만 주는 것보다 효과적)

### 2. 필수 정보 구조화
```
스펙:
- Python 3.10+
- mcp Python SDK https://github.com/modelcontextprotocol/python-sdk
- uv 패키지 사용

요구사항:
- mcp server를 잘 사용할 수 있는 시스템 프롬프트 작성
- python cli로 동작
- 어떤 tool을 사용했는지 출력
- mcp server의 tool 만 사용하기
- 테스트코드 작성
- 핵심 요구사항만 수행할 수 있도록 단순한 형태로 구현

주의:
- PRD는 핵심만 간략하게
- PRD에는 코드 작성하지 않기
- todo 작성
```

### 3. Context7 MCP 활용
정확한 기술 문서를 참조하기 위해 Context7 MCP를 반드시 사용하도록 명시합니다.

```
context7 mcp 반드시 사용해
```

Context7이 최신 라이브러리 문서를 가져와 AI가 정확한 정보로 개발할 수 있습니다.

---

### PRD 프롬프트 실행 과정

1. **Context7 활용**: AI가 Context7 MCP를 사용해 최신 mcp Python SDK 문서 조회
2. **WebSearch 실행**: 필요한 추가 정보 검색
3. **PRD 작성**: 다음 구조로 PRD 문서 생성
   - 프로젝트 개요
   - 기술 스택 (Python 버전, SDK, uv 패키지 등)
   - 핵심 기능
     - MCP server 연결 및 초기화
     - Tool 목록 조회 및 실행
     - 실행된 tool 추적 및 출력
     - Python CLI 인터페이스
     - LLM용 시스템 프롬프트 생성
   - 구현 단계 (Todo)
   - 에러 처리 및 제약사항

---

## PRD 작성 후 구현

### 컨텍스트 초기화 → 구현

**왜 이렇게 해야 하나?**
- PRD 작성에 많은 컨텍스트 소모
- PRD 작성 후 `/clear`로 컨텍스트 초기화
- 완성된 PRD로 최대 컨텍스트 활용하여 구현

```bash
# Step 1: PRD 작성
claude
> [PRD 프롬프트 입력]
# PRD 문서가 생성됨

# Step 2: 컨텍스트 초기화
/clear

# Step 3: PRD 기반 구현
> @docs/prd.md 읽고 구현해주세요
```

이 방식으로 컨텍스트 윈도우를 효율적으로 활용할 수 있습니다.

### AI가 좋아하는 PRD
✅ 정확한 기술 스택 링크
✅ 명확한 입출력 정의
✅ 구체적인 제약사항
✅ Context7 등 MCP 도구 활용

### AI가 싫어하는 PRD
❌ "적당히 만들어줘"
❌ "잘 만들어줘"
❌ 버전 정보 없음
❌ 모호한 요구사항

---

## 참고 자료
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
