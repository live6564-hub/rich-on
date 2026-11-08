#!/usr/bin/env python3
"""다음 버전 폴더(out/v01, v02 …)를 만든다.

- 처음이면: 템플릿 page.html → out/v01/index.html, 빈 img/ 폴더.
- 이미 있으면: 가장 최신 vNN을 통째로 복사해 vNN+1을 만든다(export/는 빼고).
  이전 버전은 절대 건드리지 않는다.

사용: python3 new_version.py [out 폴더]   → 새 폴더 경로를 출력
"""
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "page.html"


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    versions = sorted(
        int(m.group(1))
        for p in out.iterdir()
        if p.is_dir() and (m := re.fullmatch(r"v(\d+)", p.name))
    )
    nxt = out / f"v{(versions[-1] + 1 if versions else 1):02d}"

    if versions:
        prev = out / f"v{versions[-1]:02d}"
        shutil.copytree(prev, nxt, ignore=shutil.ignore_patterns("export", "changes.md"))
    else:
        nxt.mkdir()
        (nxt / "img").mkdir()
        shutil.copy(TEMPLATE, nxt / "index.html")
    print(nxt)


if __name__ == "__main__":
    main()
