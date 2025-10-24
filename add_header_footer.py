#!/usr/bin/env python3
"""
Add header and footer to all clip markdown files
"""

import os
from pathlib import Path

HEADER = """---
## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent

---

"""

FOOTER = """

---

## 강사 정보
- 작성자: 정구봉
- LinkedIn: https://www.linkedin.com/in/gb-jeong/
- 이메일: bong@dio.so

## 강의 자료
- 강의 자료: https://goobong.gitbook.io/fastcampus
- Github: https://github.com/Koomook/fastcampus-ai-agent-vibecoding
- FastCampus 강의 주소: https://fastcampus.co.kr/biz_online_vibeagent
"""


def find_clip_files(root_dir):
    """Find all clip markdown files"""
    clip_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().startswith('clip') and file.endswith('.md'):
                clip_files.append(os.path.join(root, file))
    return clip_files


def has_header_footer(content):
    """Check if file already has header and footer"""
    return '## 강사 정보' in content and 'bong@dio.so' in content


def add_header_footer(file_path):
    """Add header and footer to a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has header/footer
        if has_header_footer(content):
            print(f"⏭️  Skipped (already has info): {file_path}")
            return False

        # Add header and footer
        new_content = HEADER + content + FOOTER

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Updated: {file_path}")
        return True

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    root_dir = Path(__file__).parent

    print("🔍 Finding all clip markdown files...\n")
    clip_files = find_clip_files(root_dir)

    print(f"📝 Found {len(clip_files)} clip files\n")
    print("=" * 80)

    updated_count = 0
    skipped_count = 0

    for file_path in sorted(clip_files):
        if add_header_footer(file_path):
            updated_count += 1
        else:
            skipped_count += 1

    print("=" * 80)
    print(f"\n✨ Complete!")
    print(f"   Updated: {updated_count} files")
    print(f"   Skipped: {skipped_count} files")
    print(f"   Total: {len(clip_files)} files")


if __name__ == "__main__":
    main()
