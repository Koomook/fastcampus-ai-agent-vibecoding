---
description: 기존 슬래시 커맨드를 안전하게 수정하는 대화형 워크플로우
allowed-tools: Read, Write, Edit, Glob
---

# Update Slash Command - 대화형 커맨드 수정 워크플로우

기존 슬래시 커맨드를 안전하게 수정합니다.

## 📋 단계별 워크플로우

### 1단계: 커맨드 목록 조회 및 선택
- `.claude/commands/` 디렉토리의 모든 `.md` 파일 목록을 표시
- 각 커맨드의 `description` (frontmatter에서 추출) 함께 표시
- 사용자에게 수정할 커맨드 파일명 입력 받기 (예: `commit.md`)
- 잘못된 파일명 입력 시 목록 다시 표시하고 재입력 요청

### 2단계: 현재 커맨드 분석 및 요약
선택한 커맨드 파일을 읽고 다음 정보를 요약하여 표시:

**Frontmatter 분석:**
- `description`: 커맨드 설명
- `argument-hint`: 인자 힌트 (예: `[message]`, `[pr-number]`)
- `allowed-tools`: 허용된 도구 목록
- `model`: 사용 모델 (있는 경우)

**본문 분석:**
- 파일 크기 (라인 수)
- 사용된 변수: `$ARGUMENTS`, `$1`, `$2`, `$3` 등
- 주요 지시사항 요약 (첫 3-5줄)

**예시 출력:**
```
📄 현재 커맨드: commit.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Description: Create a git commit
Argument Hint: [message]
Allowed Tools: Bash(git add:*), Bash(git commit:*)
Model: claude-3-5-haiku-20241022
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
본문 (5 lines):
Create a git commit with message: $ARGUMENTS
Review changed files before committing.
```

### 3단계: 수정 내용 입력
사용자에게 수정할 내용을 물어보고 구체적인 변경사항 받기:
- "어떤 부분을 어떻게 수정하시겠습니까?"
- 예시 제공:
  - "description을 '커밋 생성'으로 변경"
  - "allowed-tools에 Bash(git status:*) 추가"
  - "본문에 코드 리뷰 단계 추가"
  - "$ARGUMENTS를 $1으로 변경하고 argument-hint를 [title] [body]로 수정"

### 4단계: 변경 전/후 비교 검토
변경사항을 시각적으로 비교 표시:

```
🔍 변경사항 검토
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Frontmatter 변경:
  description:
    🔴 변경 전: Create a git commit
    🟢 변경 후: 커밋 생성 [변경됨]

  allowed-tools:
    🔴 변경 전: Bash(git add:*), Bash(git commit:*)
    🟢 변경 후: Bash(git add:*), Bash(git status:*), Bash(git commit:*) [변경됨]

  model: claude-3-5-haiku-20241022 (변경 없음)

📌 본문 변경:
  🔴 변경 전 (Line 1):
    Create a git commit with message: $ARGUMENTS

  🟢 변경 후 (Line 1):
    Create a git commit with message: $ARGUMENTS [변경됨]
    First review changed files with git status.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5단계: 사용자 승인
변경사항을 저장할지 확인:
- **"yes"**: 파일 저장 후 6단계로 진행
- **"no"**: 3단계로 돌아가서 수정 내용 다시 받기
- **"cancel"**: 전체 작업 취소하고 원본 유지

### 6단계: 저장 및 완료
파일 저장 후 다음 정보 표시:

**변경 로그:**
```
✅ 저장 완료
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
파일: .claude/commands/commit.md
시간: 2025-10-07 14:30:22
변경:
  • description 한글화
  • allowed-tools에 git status 추가
  • 본문에 리뷰 단계 추가
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 참조
https://docs.claude.com/en/docs/claude-code/slash-commands
