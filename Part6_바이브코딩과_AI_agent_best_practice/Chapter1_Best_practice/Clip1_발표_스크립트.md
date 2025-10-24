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

# Clip 1 발표 스크립트: CLAUDE.md와 AGENTS.md Best Practice

> **예상 소요 시간**: 8-10분

---

## 🎬 오프닝 (1분)

안녕하세요! 오늘은 AI 에이전트와 효과적으로 협업하기 위한 핵심 파일, **CLAUDE.md**와 **AGENTS.md**에 대해 알아보겠습니다.

여러분, 혹시 Claude Code나 GitHub Copilot을 사용할 때 AI가 프로젝트의 컨벤션을 모르거나 엉뚱한 코드를 생성한 경험 있으신가요?

오늘 배울 내용이 바로 그 문제의 해결책입니다.

---

## 📖 Section 1: CLAUDE.md/AGENTS.md란? (2분)

### 핵심 개념

CLAUDE.md와 AGENTS.md는 **AI 에이전트를 위한 프로젝트 메모리**입니다.

README.md가 인간 개발자를 위한 문서라면, 이 파일들은 AI가 읽는 개발 가이드입니다.

### 실제 사례

화면을 보시면, claude-code-action 프로젝트의 CLAUDE.md가 있습니다.
- 개발 환경: Bun 1.2.11, TypeScript strict mode
- 테스트: `bun test`
- 포맷팅: `bun run format`

이렇게 **복사해서 바로 실행 가능한 명령어**를 제공합니다.

---

## 🔍 Section 2: 4개 프로젝트 분석 (3분)

실제 오픈소스 프로젝트 4개를 분석했습니다.

### 1️⃣ Anthropic - claude-code-action (TypeScript)

**특징:** 2단계 워크플로우
- Preparation Phase: 인증, 검증, 데이터 수집
- Execution Phase: 4단계 순차 실행

**Execution Phase 상세:**
1. MCP 서버 설정 → `~/.claude/mcp/github-action-server/` 자동 설치
2. 프롬프트 생성 → `data/fetcher.ts`가 GitHub 데이터 조회
3. Claude 통합 → Anthropic/AWS Bedrock/Google Vertex AI 지원
4. 결과 처리 → 코멘트 업데이트, 브랜치/PR 생성

**배울 점:**
- 정확한 파일 위치 명시 (`data/fetcher.ts`)
- MCP 서버 표준 설치 경로 문서화
- 다중 AI 프로바이더 지원으로 유연성 확보

### 2️⃣ 당근마켓 - Stackflow (JavaScript)

**특징:** 플러그인 라이프사이클
- onInit → onBeforePush → onPushed

**주요 용어 정의:**
- Activity = 화면/페이지
- Stack = Activity 컬렉션
- Event = 상태 변경 트리거 (Pushed, Popped, Replaced)
- Plugin = 라이프사이클 훅
- Effect = 부수 효과
- Step = 하위 네비게이션

**Common Tasks 코드 예시:**
```typescript
// Stack 설정
const { Stack, useFlow } = stackflow({
  activities: { MainActivity, DetailActivity }
});

// 네비게이션
flow.push("DetailActivity", { id: "123" });
flow.pop();
```

**배울 점:**
- 주요 용어를 명확히 정의해서 AI가 올바른 구조로 코드 생성
- Common Tasks에 실제 코드 스니펫 제공
- ⚠️ Important Note: "항상 yarn 사용 (npm X)"

### 3️⃣ OpenAI - Codex (Rust)

**특징:** 엄격한 TUI 코딩 컨벤션

**TUI Code Conventions (ratatui):**
```rust
// ❌ 나쁜 예: 수동 Style 생성
let style = Style::default().fg(Color::Cyan);
let span = Span::styled("text", style);

// ✅ 좋은 예: Stylize trait 헬퍼
use ratatui::style::Stylize;
let span = "text".cyan().bold();

// ❌ 금지: 하드코딩된 white
let text = "Error".white();

// ✅ 권장: 기본 foreground
let text = "Error".into();
```

**Snapshot Tests (insta):**
```bash
# 1. 테스트 실행
cargo test -p codex-tui

# 2. 스냅샷 검토
cargo insta show

# 3. 의도된 변경이면 수락
cargo insta accept
```

**배울 점:**
- TUI 스타일링 컨벤션을 명확히 가이드 (Stylize trait 강제)
- 금지 패턴 명시 (white 색상 하드코딩 X)
- Snapshot 테스트 워크플로우 3단계 제시
- 텍스트 래핑 도구 구분 (textwrap vs wrapping.rs)

### 4️⃣ Apache - Airflow (Python)

**특징:** 환경 선택권 + 케이스별 문서 링크
- Option 1: `uv venv` + `uv sync`
- Option 2: Breeze Docker

**케이스별 참고 문서:**
| 케이스 | 문서 |
|--------|------|
| 로컬 환경 설정 | `07_local_virtualenv.rst` |
| 환경 비교 | `06_development_environments.rst` |
| 테스팅 | `03b_contributors_quick_start_seasoned_developers.rst` |
| 문서 빌드 | `11_documentation_building.rst` |
| PR 워크플로우 | `05_pull_requests.rst` |
| Provider 패키징 (고급) | `12_provider_distributions.rst` |
| API 버저닝 (고급) | `19_execution_api_versioning.rst` |

**문서 링크 패턴 예시:**
```markdown
"로컬 환경 설정 → contributing-docs/07_local_virtualenv.rst 참조"
"테스트 실행 → contributing-docs/03b_... 참조"
```

**배울 점:**
- 개발자에게 여러 환경 옵션 제공 (로컬 vs Docker)
- **케이스별 문서 링크**: "X 하려면 Y 문서 읽기" 패턴
- 9개 작업 유형별 정확한 문서 경로 제시
- 기본 작업 vs 고급 작업 구분

---

## 📊 Section 3: 공통 패턴 (2분)

모든 프로젝트에서 발견한 공통 구조:

```
1. 개발 환경 (Runtime, 언어, 버전)
2. 핵심 명령어 (빌드, 테스트, 포맷팅)
3. 코딩 컨벤션 (스타일, Best Practices)
4. 테스트 방법 (실행, 검증)
```

### 명령어 작성 원칙

**✅ 좋은 예:**
```bash
# Run all tests
cargo test --all-features

# Run specific project
cargo test -p codex-tui
```

**❌ 나쁜 예:**
```
테스트를 실행하려면 cargo를 사용하세요.
```

**차이점:** 복사-붙여넣기 가능 여부!

---

## ✅ Section 4: 체크리스트 (1분)

여러분이 프로젝트에 적용할 체크리스트:

**문서 구조:**
- [ ] 개발 환경 명시
- [ ] 필수 도구 설치 방법
- [ ] 핵심 명령어 목록
- [ ] 코딩 컨벤션
- [ ] 테스트 프로토콜

**명령어 작성:**
- [ ] 복사-붙여넣기 가능
- [ ] 각 명령어 목적 설명
- [ ] 예상 결과 표시

**코드 예시:**
- [ ] 실행 가능한 완전한 코드
- [ ] 좋은 예 vs 나쁜 예 대조

---

## 🎯 마무리 (1분)

### 핵심 요약

1. **CLAUDE.md/AGENTS.md = AI를 위한 프로젝트 메모리**
2. **공통 패턴: 환경 → 명령어 → 컨벤션 → 테스트**
3. **핵심은 "복사 가능한 명령어"**
4. **좋은 예/나쁜 예 대조가 효과적**

### 다음 단계

다음 클립에서는 이 패턴들을 자동화하는 방법을 배웁니다.
- 바이브코딩 팁 자동화
- 프로젝트 템플릿 생성
- Claude Code 시스템 프롬프트 커스터마이징

오늘 배운 내용을 바탕으로 여러분의 프로젝트에도 CLAUDE.md를 만들어보세요!

감사합니다! 🙏

---

## 💬 Q&A 예상 질문

**Q1: CLAUDE.md와 AGENTS.md 중 어떤 걸 써야 하나요?**
- A: 둘 다 같은 목적입니다. Anthropic은 CLAUDE.md를 선호하고, 다른 프로젝트는 AGENTS.md를 씁니다. 파일명보다 내용이 중요합니다.

**Q2: README.md에 통합하면 안 되나요?**
- A: 가능하지만 분리를 추천합니다. README는 마케팅/소개용, CLAUDE.md는 개발 가이드용으로 목적이 다릅니다.

**Q3: 얼마나 자주 업데이트해야 하나요?**
- A: 개발 환경, 도구, 컨벤션이 변경될 때마다 업데이트하세요. 코드 리뷰 시 함께 검토하는 것을 추천합니다.

**Q4: 팀원들도 이 파일을 읽나요?**
- A: 네! AI뿐만 아니라 신규 팀원의 온보딩 자료로도 유용합니다. 명령어가 구체적이라 학습 곡선이 낮습니다.


---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
