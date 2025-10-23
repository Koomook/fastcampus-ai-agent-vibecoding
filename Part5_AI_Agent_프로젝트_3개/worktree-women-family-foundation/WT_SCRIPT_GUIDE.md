# Git Worktree 자동화 스크립트 (`wt`)

## 📋 개요

이 스크립트는 Git worktree를 자동으로 생성하고 설정하는 도구입니다. 새로운 작업 환경을 빠르게 준비할 수 있습니다.

## ✨ 주요 기능

- ✓ 새로운 worktree 자동 생성
- ✓ 패키지 자동 설치 (uv 사용)
- ✓ .env 파일 자동 복사
- ✓ 진행 상황 실시간 표시
- ✓ 명확한 에러 메시지
- ✓ 완료 후 다음 단계 가이드 제공

## 🚀 사용법

### 기본 사용법

```bash
./wt <브랜치명>
```

### 예시

```bash
# 새 기능 개발용 worktree 생성
./wt feature/new-feature

# 버그 수정용 worktree 생성
./wt bugfix/critical-issue

# 실험용 worktree 생성
./wt experiment/try-new-approach
```

## 📋 동작 절차

### 1단계: 유효성 검사
- 현재 디렉토리가 git 저장소인지 확인
- 브랜치가 이미 사용 중인지 확인
- worktree 경로가 이미 존재하는지 확인

### 2단계: Worktree 생성
```
새 경로: ../프로젝트명-브랜치명
예시: ../fastcampus-lecture-feature/new-feature
```

### 3단계: .env 파일 복사
- 기존 .env 파일이 있으면 새 worktree로 자동 복사

### 4단계: 패키지 설치
- `uv sync` 명령어로 의존성 자동 설치

## 🔧 실행 권한 설정

스크립트를 처음 다운로드했을 때는 실행 권한이 없을 수 있습니다.

### 방법 1: chmod 명령어 (권장)

```bash
chmod +x wt
```

권한 확인:
```bash
ls -la wt
# -rwxr-xr-x@ 1 bong  staff  3536 Oct 19 15:36 wt
```

### 방법 2: Git 커밋 속성 설정

```bash
git config core.fileMode true
git add wt
git commit -m "Add executable permission to wt script"
```

### 방법 3: 다른 방식으로 실행

실행 권한이 없다면:
```bash
bash wt <브랜치명>
# 또는
sh wt <브랜치명>
```

## 📊 출력 메시지 해석

### 성공 메시지
```
✓ worktree 생성 완료
✓ .env 파일 복사 완료
✓ 패키지 설치 완료
```

### 진행 중 메시지
```
⟳ 새 worktree 생성 중...
⟳ .env 파일 복사 중...
⟳ 패키지 설치 중...
```

### 정보 메시지
```
ℹ .env 파일이 없습니다.
```

### 에러 메시지
```
❌ 에러: 현재 디렉토리가 git 저장소가 아닙니다.
❌ 에러: worktree가 이미 존재합니다.
❌ 에러: uv가 설치되어 있지 않습니다.
```

## ⚠️ 에러 상황별 해결 방법

### "uv가 설치되어 있지 않습니다"

```bash
# macOS (Homebrew)
brew install uv

# Linux
pip install uv

# 또는 공식 설치 스크립트
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "worktree가 이미 존재합니다"

```bash
# 기존 worktree 제거
git worktree remove ../fastcampus-lecture-feature/new-feature

# 또는 강제 제거
rm -rf ../fastcampus-lecture-feature/new-feature
```

### "브랜치가 이미 worktree에서 사용 중입니다"

```bash
# 현재 worktree 목록 확인
git worktree list

# 해당 worktree 확인 및 제거
git worktree remove <worktree-path>
```

## 🔄 Worktree 관리 명령어

### Worktree 목록 확인
```bash
git worktree list
```

출력 예시:
```
/Users/bong/github/fastcampus-lecture (main)
/Users/bong/github/fastcampus-lecture-feature/new-feature (feature/new-feature)
```

### Worktree로 이동
```bash
cd ../fastcampus-lecture-feature/new-feature
```

### Worktree 삭제
```bash
git worktree remove ../fastcampus-lecture-feature/new-feature
```

### Worktree 정리 (손상된 링크 제거)
```bash
git worktree prune
```

## 💡 팁과 주의사항

### ✅ 권장 사항

1. **명확한 브랜치명 사용**: `feature/user-auth`, `bugfix/api-error`
2. **주기적인 정리**: 작업 완료 후 worktree 제거
3. **메인 브랜치 유지**: main/master 브랜치는 worktree로 사용하지 않기
4. **.env 관리**: 민감한 정보가 있으면 수동으로 추가

### ⚠️ 주의사항

1. **동시에 같은 브랜치 사용 금지**: 같은 브랜치를 여러 worktree에서 체크아웃할 수 없음
2. **디스크 공간**: 각 worktree는 전체 코드베이스 복사본이므로 디스크 공간 필요
3. **의존성 버전**: 다른 worktree에서 다른 버전이 필요하면 별도로 설치

## 🐛 문제 해결

### 스크립트가 실행되지 않음

```bash
# 1. 파일이 존재하는지 확인
ls -la wt

# 2. 실행 권한 확인
chmod +x wt

# 3. bash로 직접 실행
bash wt <브랜치명>
```

### uv 설치 확인

```bash
# uv 설치 확인
which uv

# uv 버전 확인
uv --version

# 설치 안 됨 경우 설치
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 권한 에러 발생

```bash
# 권한 확인
ls -l wt

# rwx 권한이 없으면
chmod +x wt

# sudo를 사용하지 말 것 (불필요하고 권장하지 않음)
```

## 📝 스크립트 커스터마이징

### 워크트리 경로 변경

기본값: `../프로젝트명-브랜치명`

스크립트의 이 줄을 수정:
```bash
WORKTREE_PATH="../${PROJECT_NAME}-${BRANCH_NAME}"
```

예시:
```bash
WORKTREE_PATH="$HOME/worktrees/${PROJECT_NAME}-${BRANCH_NAME}"
```

### 추가 설정 파일 복사

`.env` 외에 다른 파일도 복사하려면 스크립트에 추가:

```bash
# .env 복사 후에 추가
if [ -f ".env.local" ]; then
    cp .env.local "$WORKTREE_PATH/.env.local"
fi
```

## 🎯 일반적인 워크플로우 예시

```bash
# 1. 새 기능 개발용 worktree 생성
./wt feature/user-dashboard

# 2. 새 worktree로 이동 (스크립트가 안내함)
cd ../fastcampus-lecture-feature/user-dashboard

# 3. 작업 수행
# ... 코드 작성 및 테스트 ...

# 4. 변경 사항 커밋 및 푸시
git add .
git commit -m "Add user dashboard feature"
git push -u origin feature/user-dashboard

# 5. Pull Request 생성

# 6. 작업 완료 후 main으로 돌아가기
cd ../fastcampus-lecture

# 7. Worktree 삭제
git worktree remove ../fastcampus-lecture-feature/user-dashboard
```

## 📞 추가 도움말

문제가 발생하면 다음 명령어로 Git worktree 공식 문서를 확인할 수 있습니다:

```bash
git worktree help
man git-worktree
```

---

**스크립트 버전**: 1.0
**마지막 업데이트**: 2025-10-19
