#!/usr/bin/env python3
"""
서울시 문화행사 MCP Server 실행 스크립트

이 스크립트는 Claude Desktop에서 MCP 서버를 실행하기 위한 진입점입니다.
Python 모듈 경로를 명시적으로 설정하여 ModuleNotFoundError를 방지합니다.

사용법:
    uv run python run_server.py

Claude Desktop 설정:
    {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/project", "run", "python", "run_server.py"]
    }
"""
import sys
import os


def setup_python_path():
    """
    Python 모듈 경로를 설정합니다.

    src/ 디렉토리를 Python 경로의 최우선 순위에 추가하여
    seoul_culture_mcp 패키지를 import할 수 있게 합니다.
    """
    # 현재 스크립트의 절대 경로에서 프로젝트 루트 디렉토리 찾기
    project_root = os.path.dirname(os.path.abspath(__file__))

    # src 디렉토리 경로 생성
    src_path = os.path.join(project_root, 'src')

    # Python 경로의 맨 앞에 추가 (최우선 순위)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    return project_root


def load_environment_variables(project_root):
    """
    .env 파일에서 환경 변수를 로드합니다 (선택적).

    Args:
        project_root: 프로젝트 루트 디렉토리 경로
    """
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(project_root, '.env')

        if os.path.exists(env_path):
            load_dotenv(env_path)
            print(f"✓ Loaded environment variables from {env_path}", file=sys.stderr)
    except ImportError:
        # python-dotenv가 설치되지 않은 경우 무시
        pass


def main():
    """MCP 서버를 시작합니다."""
    # 1. Python 경로 설정
    project_root = setup_python_path()

    # 2. 환경 변수 로드
    load_environment_variables(project_root)

    # 3. MCP 서버 임포트 및 실행
    try:
        from seoul_culture_mcp.server import mcp
        mcp.run()
    except ImportError as e:
        print(f"❌ Error: Failed to import MCP server module", file=sys.stderr)
        print(f"   {e}", file=sys.stderr)
        print(f"   Project root: {project_root}", file=sys.stderr)
        print(f"   Python path: {sys.path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
