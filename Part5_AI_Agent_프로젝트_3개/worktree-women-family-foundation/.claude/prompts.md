# 지난 세미나 피드백
- 대화창 더 많이 보기
- 질문하기 1번 vs 2번

# 모두를 위한 Research Agent

## MCP 연결
MCP란? - explanatory output style
notion mcp 연결 명령어 찾아줘
youtube mcp 찾아줘

## 프롬프트
목표: 리포트 작성

claude sonnet 4.5 가 발표됐다. 동시에 많은 기능이 같이 release 됐는데, 아래 자료를 모두 읽고 한국어로 리포트를 작성해.

웹 자료
- https://www.anthropic.com/news/claude-sonnet-4-5
- https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- https://docs.claude.com/en/docs/about-claude/models/whats-new-sonnet-4-5
- https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

youtube
https://www.youtube.com/watch?v=BER3EhUIyz0
https://www.youtube.com/watch?v=dGiqrsv530Y
https://www.youtube.com/watch?v=IypXvHej9eY

최종 결과물은 Notion 에 저장

Notion DB에는 레포트 작성 날짜, 핵심 source를 포함할 것

---

# PM 을 위한 프로젝트 관리 Agent

## change log 작성
agent-josh: 최근 일주일 git commit 이력을 조사해서 스프린트 문서를 노션에 작성해라
노션 문서: https://www.notion.so/koomook/27e2b37d07c480b08c36f6b99efe56db?source=copy_link


## 자동 태스크 생성

```
목표:
web fetch, youtube transcript sdk 를 사용해서 youtube 채널을 입력하면 채널에 있는 모든 youtube 영상을 분석해서 notion 에 저장하는 자동화 파이프라인을 만든다.

linear team: fastcampus-seminar-02

언어: python
패키지 관리: uv
배포: Cloud Run, Dockerize 필수

동작 가이드:
linear mcp 를 사용해서 issue 를 최대 5개 생성하라. 이슈간의 dependency 를 만들어서 parent-sub 로 연결해라
```

## 데이터 수집 자동화
https://smartmarket.nonghyup.com/servlet/BFBCW0001R.view 의
웹페이지를 이동하면서
퇴직, 연금, 대출, 외환, 보험, 카드, ISA

어떤 상품들이 있는지 데이터 모으기

playwright mcp를 사용해서 데이터를 직접 읽고 파일로 저장

저장 위치: data/

## Sub Agent

## output style
업무 자동화 에이전트