"""MCP 서버 설정 검증 스크립트"""
import sys
import os

# src 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from seoul_culture_mcp.server import mcp

print("=" * 70)
print("서울시 문화행사 MCP Server - 설정 검증")
print("=" * 70)
print()

# 서버 정보 확인
print(f"✅ 서버 이름: {mcp.name}")
print(f"✅ 서버 설명: {mcp.instructions}")
print()

# 등록된 도구 확인
print("📦 등록된 Tools:")
if hasattr(mcp, '_tool_manager') and hasattr(mcp._tool_manager, 'tools'):
    tools = mcp._tool_manager.tools
    for tool_name, tool in tools.items():
        print(f"  - {tool_name}")
        if hasattr(tool, 'fn') and hasattr(tool.fn, '__doc__'):
            doc = tool.fn.__doc__
            if doc:
                first_line = doc.strip().split('\n')[0]
                print(f"    설명: {first_line}")
else:
    print("  (도구 목록을 확인할 수 없습니다)")
print()

# 등록된 리소스 확인
print("📚 등록된 Resources:")
if hasattr(mcp, '_resource_manager') and hasattr(mcp._resource_manager, 'resources'):
    resources = mcp._resource_manager.resources
    for resource_uri, resource in resources.items():
        print(f"  - {resource_uri}")
        if hasattr(resource, 'fn') and hasattr(resource.fn, '__doc__'):
            doc = resource.fn.__doc__
            if doc:
                print(f"    설명: {doc.strip()}")
else:
    print("  (리소스 목록을 확인할 수 없습니다)")
print()

print("=" * 70)
print("✅ MCP 서버가 올바르게 설정되었습니다!")
print("=" * 70)
print()
print("다음 단계:")
print("1. Claude Desktop 설정 파일에 이 서버를 추가하세요")
print("   경로: ~/Library/Application Support/Claude/claude_desktop_config.json")
print()
print("2. 설정 예시:")
print("""
{
  "mcpServers": {
    "seoul-culture": {
      "command": "uv",
      "args": ["run", "python", "-m", "seoul_culture_mcp.server"],
      "cwd": "%s",
      "env": {
        "SEOUL_API_KEY": "your_api_key_here"
      }
    }
  }
}
""" % os.path.dirname(os.path.abspath(__file__)))
print()
print("3. Claude Desktop을 재시작하세요")
print()
print("4. Claude에서 다음과 같이 요청할 수 있습니다:")
print("   - '이번 주말에 열리는 전시회 알려줘'")
print("   - '12월에 열리는 콘서트 정보 찾아줘'")
print("   - '강남구에서 열리는 무료 문화행사 알려줘'")
