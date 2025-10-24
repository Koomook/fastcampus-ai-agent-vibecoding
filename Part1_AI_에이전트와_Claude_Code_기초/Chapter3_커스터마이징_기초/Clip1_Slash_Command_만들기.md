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

# Clip 1: Slash Command 만들기

## 학습 목표
- Slash Command의 개념과 동작 원리 이해
- 커스텀 명령어 생성 및 관리 방법 습득
- 실무에서 활용 가능한 명령어 구현

## Slash Command란?

### 🎯 개념 이해
- **정의**: `/`로 시작하는 특수 명령어로 특정 작업을 즉시 실행
- **장점**: 반복 작업 자동화, 일관된 작업 수행, 빠른 실행
- **활용**: 코드 리뷰, 배포, 테스트, 문서화 등

### 📌 반드시 알아야 할 기본 Slash 명령어

Claude Code는 기본적으로 여러 유용한 slash 명령어를 제공합니다:

| 명령어 | 설명 | 사용 예시 |
|--------|------|-----------|
| `/add-dir` | 작업 디렉토리에 새 폴더 추가 | `/add-dir src/components` |
| `/clear` | 대화 기록 초기화 | `/clear` |
| `/config` | Claude Code 설정 확인 및 수정 | `/config` |
| `/init` | 새 프로젝트 초기화 | `/init` |
| `/mcp` | MCP 서버 연결 관리 | `/mcp` |
| `/memory` | 장기 기억 기능 관리 | `/memory` |
| `/model` | 사용할 AI 모델 변경 | `/model` |
| `/review` | 코드 리뷰 수행 | `/review src/` |
| `/rewind` | 이전 대화 상태로 되돌리기 | `/rewind` |
| `/status` | 현재 작업 상태 확인 | `/status` |

이 기본 명령어들을 이해한 후, 프로젝트 요구사항에 맞는 커스텀 명령어를 만들 수 있습니다.


## Slash Command 구조

### 📁 파일 구조
```
.claude/
├── commands/
│   ├── review.md         # 코드 리뷰 명령어
│   ├── deploy.md         # 배포 명령어
│   ├── test.md          # 테스트 명령어
│   ├── optimize.md      # 최적화 명령어
│   └── document.md      # 문서화 명령어
└── settings.json  # 명령어 설정
```

## 사용자 정의 Slash Command 구현

### 예제: `/optimize` 명령어 만들기

간단한 코드 최적화 명령어를 단계별로 만들어보겠습니다.

# 프로젝트 명령어 생성
```
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

#### 4단계: 바이브코딩으로 Slash Command 생성

실제 사용 시에는 다음과 같이 간결하게 요청할 수 있습니다:

```
/optimize 명령어 만들어줘

대상 파일을 입력받고, 성능/메모리/번들사이즈 관점에서
최적화 제안을 코드와 함께 제공하는 명령어
```

## Slash Command 로 나만의 워크플로우를 설계

### 예제: `/create-linear-issues` 명령어

프로젝트 스코프에서 사용할 수 있는 Linear 이슈 생성 명령어를 만들어보겠습니다. 이 명령어는 Linear MCP를 활용하여 sub-issue로 연결된 이슈를 자동 생성합니다.

#### 📋 요구사항
- Linear MCP 서버 연결 필요
- fastcampus-seminar-02 팀에 이슈 생성
- Sub-issue로 연결되는 구조적인 이슈 생성

#### 바이브코딩 프롬프트

실제 사용 시 간결한 프롬프트:

```
linear mcp를 사용해서 linear team "fastcampus-seminar-02"에 구조화된 issue를 생성하는 /create-linear-issues 명령어 만들어줘

메인 이슈를 만들고 그 아래 sub-issue들을 자동으로 연결해

참조: https://docs.claude.com/ko/docs/claude-code/slash-commands#custom-slash-commands
```

#### 결과 예시
```markdown
# Linear Issues Creation Command

Linear MCP를 사용하여 fastcampus-seminar-02 팀에 이슈를 생성하고, 각 이슈를 서브 이슈로 연결합니다.

## 주요 기능

### 1. Linear 팀 확인
- 대상 팀: fastcampus-seminar-02
- Linear MCP를 통해 팀 ID 조회
- 팀 존재 여부 확인

### 2. 이슈 생성 전략
**계층적 구조:**
- 메인 이슈(Parent Issue): 프로젝트 전체 목표나 에픽(Epic)
- 서브 이슈(Sub Issues): 메인 이슈를 구성하는 세부 작업들
- 각 서브 이슈는 바로 이전 이슈를 parent로 설정하여 연결

**우선순위 설정:**
- Urgent (0): 긴급하고 중요한 작업
- High (1): 높은 우선순위
- Medium (2): 중간 우선순위 (기본값)
- Low (3): 낮은 우선순위

**상태 설정:**
- Backlog: 백로그 상태 (기본값)
- Todo: 할 일
- In Progress: 진행 중
- Done: 완료

### 3. 이슈 정보 수집
사용자로부터 다음 정보를 수집:
- 메인 이슈 제목 및 설명
- 서브 이슈 목록 (제목, 설명, 우선순위)
- 각 이슈의 라벨 및 상태

### 4. Linear MCP 활용
**사용할 MCP 도구:**
- `mcp__linear__search-teams`: 팀 검색
- `mcp__linear__create-issue`: 이슈 생성
- `mcp__linear__get-issue`: 생성된 이슈 정보 조회

**이슈 생성 프로세스:**
1. fastcampus-seminar-02 팀 ID 조회
2. 메인 이슈 생성 (parent 없음)
3. 첫 번째 서브 이슈 생성 (메인 이슈를 parent로 설정)
4. 두 번째 서브 이슈 생성 (첫 번째 서브 이슈를 parent로 설정)
5. n번째 서브 이슈 생성 (n-1번째 서브 이슈를 parent로 설정)

## 실행 단계

1. **팀 정보 조회**: fastcampus-seminar-02 팀 ID 확인
2. **이슈 정보 수집**: 사용자로부터 생성할 이슈 정보 수집
3. **메인 이슈 생성**: 최상위 이슈 생성
4. **서브 이슈 체인 생성**: 각 서브 이슈를 순차적으로 생성하며 이전 이슈에 연결
5. **결과 확인**: 생성된 모든 이슈 정보 조회 및 검증
6. **리포트 생성**: 생성된 이슈들의 요약 정보 출력

## 사용 예시

### 예시: MCP 서버 개발 프로젝트

메인 이슈: 새로운 MCP 서버 개발
- 서브 이슈 1: 요구사항 분석
- 서브 이슈 2: API 설계
- 서브 이슈 3: 코어 기능 구현
- 서브 이슈 4: 테스트 작성
- 서브 이슈 5: 문서화
```

#### 명령어 사용 예시

```bash
# 기본 사용 - AI가 자동으로 하위 작업 생성
/create-linear-issues 사용자 인증 시스템
```

---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
