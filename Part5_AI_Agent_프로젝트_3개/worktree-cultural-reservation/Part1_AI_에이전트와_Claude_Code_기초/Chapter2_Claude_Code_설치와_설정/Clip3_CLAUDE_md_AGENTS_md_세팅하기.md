# Clip 3: CLAUDE.md와 AGENTS.md 세팅하기 - AI 에이전트 메모리 설계

## 📋 학습 개요

### 🎯 학습 목표

- CLAUDE.md와 AGENTS.md의 생성해보기
- `/memory`와 `/init` 명령어를 활용한 메모리 자동 생성 방법 습득하기
- 효과적인 메모리 설계 베스트 프랙티스 적용하기

### 💡 실무 활용 사례

- 팀 전체가 공유하는 코딩 컨벤션과 개발 가이드라인 자동 적용
- 프로젝트별 커스텀 명령어와 워크플로우 자동 실행
- Git commit 메시지 포맷과 PR 가이드라인 자동 준수
- 패키지 매니저(uv, npm 등)와 개발 환경 설정 자동 인식

---

## 🗂️ STEP 1: CLAUDE.md vs AGENTS.md 이해하기

| 구분 | CLAUDE.md | AGENTS.md |
|------|-----------|-----------|
| **제작** | Anthropic (Claude 전용) | OpenAI, Google, Cursor 등 (범용) |
| **호환성** | Claude Code 전용 | 다양한 AI 코딩 도구 |
| **위치** | `.claude/CLAUDE.md` 또는 `CLAUDE.md` | `AGENTS.md` (루트) |
| **특수 기능** | Import 명령, memory 명령어 | Monorepo 중첩 지원 |
| **추천 사용** | Claude Code 메인 설정 | 범용 AI 에이전트 공통 문서 |

---

## 📝 STEP 2: CLAUDE.md 자동 생성하고 커스터마이징하기

### 2-1. memory 명령어로 메모리 열기

가장 간편한 방법은 Claude Code 세션에서 `/memory` 명령어를 사용하는 것입니다.

#### 프로젝트 메모리 열기

```bash
# Claude Code 세션에서
/memory
```

이 명령어 실행 시:
1. 현재 프로젝트에 `.claude/CLAUDE.md` 또는 `./CLAUDE.md` 파일이 있는지 확인
2. 없으면 생성할지 여부를 물어봄
3. 파일을 열어 내용을 확인하거나 수정

### 2-2. init 명령어로 자동 생성하기

Claude Code는 `/init` 명령어를 통해 프로젝트를 분석하여 **자동으로 CLAUDE.md를 생성**합니다.

#### 자동 생성 방법

```bash
# Claude Code 세션에서
/init
```

#### 생성된 CLAUDE.md 예시

```
# @CLAUDE.md 파일에서 확인
```

### 2-3. Claude Code 로 CLAUDE.md 파일 업데이트하기

```
CLAUDE.md 파일에 프로젝트의 파일 구조를 추가해줘.
```

```
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── users.py
│   │           ├── items.py
│   │           └── auth.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── repositories/        # Data access
├── tests/
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
├── alembic/                 # Database migrations
├── pyproject.toml           # Project dependencies
└── README.md
```

---

## 🌐 STEP 3: AGENTS.md 활용하기

AGENTS.md는 OpenAI, Google, Cursor 등 다양한 AI 코딩 도구가 공통으로 이해하는 범용 표준입니다.


### 3-1. Symbolic Link 사용해서 CLAUDE.md와 AGENTS.md 통합하기

```
claude -p "AGENTS.md 파일을 생성: CLAUDE.md 파일에 심볼링 링크를 걸어줘"
```

**Symbolic Link 장점**:
- 파일 내용을 실시간으로 동기화
- 중복 관리 불필요
- Git에서도 추적 가능

---

## 💬 STEP 4: 메모리에 메시지 즉석으로 추가하기

세션 중에 "즉석으로 기억시키고 싶은" 내용을 빠르게 기록할 때는 `#` 기호를 사용합니다.

### 4-1. # 기호로 메모리 추가

#### 사용 방법

Claude Code 세션에서 메시지 앞에 `#`을 붙입니다:

```
# 이 프로젝트는 반드시 uv를 사용해야 함 (pip는 사용 금지)
```

```
# API 테스트할 때는 항상 pytest test-database를 먼저 실행
```

```
# Git commit 메시지는 반드시 영문으로 작성하고, 한글은 절대 사용 금지
```

#### 메모리 저장 위치

`#` 메모리는 세션 종료 시 **자동으로 CLAUDE.md**에 저장됩니다:

### 4-2. 메모리 확인 및 정리

메모리가 쌓이면 정기적으로 확인하고 정리해야 합니다.

```bash
# 메모리 파일 열기
/memory

# 또는 직접 편집
code .claude/CLAUDE.md
```

**정리 원칙**:
1. 중복 내용 제거
2. 더 이상 유효하지 않은 내용 삭제

---

## 📖 참고 자료

### 공식 문서
- [Claude Code Memory 문서](https://docs.claude.com/en/docs/claude-code/memory)
- [AGENTS.md 공식 사이트](https://agents.md/)
- [AGENTS.md GitHub 저장소](https://github.com/openai/agents.md)
- [Claude Code 공식 문서](https://docs.claude.com/en/docs/claude-code/overview)
