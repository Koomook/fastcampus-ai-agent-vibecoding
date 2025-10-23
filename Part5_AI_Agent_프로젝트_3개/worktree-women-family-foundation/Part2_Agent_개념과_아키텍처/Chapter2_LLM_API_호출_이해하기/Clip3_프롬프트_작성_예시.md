# Clip 3: 최신 모델 사용 시 Knowledge Cutoff 극복하기

## 학습 목표
- AI 모델의 knowledge cutoff로 인한 문제점 이해하기
- CLAUDE.md를 활용한 최신 모델 정보 명시 방법 학습하기
- Context7 MCP를 활용한 최신 SDK/API 문서 참조 방법 익히기

## 핵심 개념

### Knowledge Cutoff 문제란?

AI 모델은 학습 데이터의 시간적 한계(knowledge cutoff)를 가지고 있습니다. 이로 인해 최신 모델이나 API를 사용하려고 할 때 다음과 같은 문제가 발생합니다:

- **문제 상황**: "GPT-5를 사용해줘"라고 명확히 요청했는데, 실제 코드에서는 GPT-4o를 사용
- **원인**: 모델의 학습 시점이 새로운 모델 출시 이전이기 때문
- **영향**: 바이브코딩 시 의도하지 않은 구버전 모델/API 사용

### 해결 방법: CLAUDE.md에 명시하기

최신 모델 정보를 CLAUDE.md에 체계적으로 기재하면 이 문제를 극복할 수 있습니다.

#### 필수 포함 정보

```markdown
## 최신 AI 모델 정보

### OpenAI
- Knowledge Cutoff: 2025년 1월
- 최신 모델:
  - GPT-5 (출시일: 2025년 8월)
- 공식 발표: https://openai.com/ko-KR/index/introducing-gpt-5/
- 새로운 파라미터:
  - `verbosity`: 응답 상세도 조절 (gpt-5 전용)

### Anthropic
- Knowledge Cutoff: 2025년 1월
- 최신 모델:
  - Claude Sonnet 4.5 (출시일: 2025년 9월)
- 공식 발표: https://www.anthropic.com/news/claude-sonnet-4-5
```

#### 작성 시 주의사항

1. **모델 이름만 명시하는 것은 불충분합니다**
   ```markdown
   ❌ 나쁜 예:
   - 최신 모델: GPT-5

   ✅ 좋은 예:
   - 최신 모델: GPT-5 (출시일: 2025년 8월)
   - Knowledge Cutoff: 2025년 1월
   - 공식 문서: https://openai.com/ko-KR/index/introducing-gpt-5/
   ```

2. **출시 날짜를 구체적으로 명시해야 합니다**
   - "최근에 나왔다" (X)
   - "2025년 8월에 출시" (O)

3. **공식 링크를 포함하세요**
   - Claude Code는 자동으로 WebFetch를 수행하여 내용을 검증합니다
   - 모델이 정보의 진위를 확인할 수 있게 됩니다

## 실전 예시

### 1. OpenAI GPT-5 사용 설정

**CLAUDE.md 작성**
```markdown
## OpenAI 최신 모델 정보
- 현재 최신 모델: gpt-5 (2025년 8월 출시)
- Knowledge Cutoff 이후 출시된 모델입니다
- 공식 발표: https://openai.com/ko-KR/index/introducing-gpt-5/
```

**바이브코딩 프롬프트**
```
OpenAI GPT-5 모델을 사용해서 간단한 챗봇 예제를 만들어줘.
verbosity 파라미터도 활용해서 간결한 응답을 받도록 설정해줘.
```

### 2. Context7 MCP 활용하기

최신 SDK/라이브러리를 사용할 때는 Context7 MCP를 함께 활용하는 것이 효과적입니다.

#### 바이브코딩 프롬프트 (Context7 활용)
```
@context7 OpenAI Python SDK 최신 문서를 참조해서
GPT-5의 verbosity 파라미터 사용 예제를 작성해줘.
```

**왜 Context7이 필요한가?**
- 새로운 모델 출시와 동시에 새로운 SDK/API가 추가되는 경우가 많음
- `verbosity` 같은 파라미터는 GPT-5 출시와 함께 추가됨
- AI 모델은 학습 시점 이후의 API 변경사항을 알 수 없음
- Context7을 통해 실시간 최신 문서를 참조할 수 있음


## 문제 해결 체크리스트

최신 모델 사용 시 문제가 발생한다면:

- [ ] CLAUDE.md에 모델 이름이 정확히 명시되어 있는가?
- [ ] 출시 날짜가 구체적으로 기재되어 있는가?
- [ ] Knowledge cutoff 날짜를 명시했는가?
- [ ] 공식 문서/발표 링크를 포함했는가?
- [ ] 새로운 파라미터가 있다면 설명을 추가했는가?
- [ ] Context7 MCP가 설치되어 있는가?
- [ ] 실제 생성된 코드에서 올바른 모델이 사용되고 있는가?

## 핵심 정리

1. **명시적 정보 제공이 핵심**
   - 모델 이름만으로는 부족
   - 날짜, 링크, 새로운 기능까지 상세히 기재

2. **CLAUDE.md 활용**
   - 프로젝트 전반에 걸쳐 일관된 모델 정보 제공
   - 바이브코딩 시 자동으로 참조됨

3. **Context7 MCP 병행 사용**
   - 최신 SDK/API 문서 실시간 참조
   - 새로운 파라미터 사용 시 필수

4. **검증 습관화**
   - 생성된 코드에서 실제 사용된 모델 확인
   - 작은 차이가 큰 성능 차이를 만듦

## 참고 자료
- OpenAI Platform Docs: https://platform.openai.com/docs
- Anthropic Claude Docs: https://docs.anthropic.com
- Context7 MCP: https://github.com/upstash/context7-mcp
