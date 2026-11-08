#!/usr/bin/env python3
"""상세페이지 HTML → 판매처별 이미지 조각.

860px 기준으로 한 번(2배 해상도) 찍고, 판매처 폭으로 줄인 뒤
섹션(data-section) 경계에서 자른다. 한 섹션이 너무 길면 그 안에서 나눈다.

사용:
  python3 export_slices.py out/v01/index.html
  python3 export_slices.py out/v01/index.html --targets smartstore:860,coupang:780 \
      --max-height 2000 --quality 90 --skip partners

결과: <html 폴더>/export/<판매처>/01.jpg … 와 full.png
필요: pip install playwright pillow && playwright install chromium
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

BASE_WIDTH = 860
SCALE = 2  # 선명하게 찍고 줄인다

try:
    from PIL import Image
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("필요한 도구가 없어요: pip install playwright pillow && playwright install chromium")

Image.MAX_IMAGE_PIXELS = None


def launch(p):
    """기본 크로미움 → 실패하면 알려진 경로로 다시 시도."""
    try:
        return p.chromium.launch()
    except Exception as first:  # noqa: BLE001
        for exe in (os.environ.get("CHROMIUM_PATH"), "/opt/pw-browsers/chromium"):
            if exe and Path(exe).exists():
                return p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        sys.exit(f"크로미움을 열 수 없어요. 'playwright install chromium'을 실행해 주세요.\n{first}")


def capture(html: Path, skip: list[str]):
    """전체 스크린샷(PIL)과 섹션 경계(CSS px, 860 기준)를 돌려준다."""
    with sync_playwright() as p:
        browser = launch(p)
        page = browser.new_page(viewport={"width": BASE_WIDTH, "height": 1200}, device_scale_factor=SCALE)
        page.goto(html.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        for cls in skip:
            page.add_style_tag(content=f".{cls}{{display:none!important}}")
        page.wait_for_timeout(300)
        info = page.evaluate(
            """() => {
              const root = document.querySelector('.page') || document.body;
              const top = root.getBoundingClientRect().top + scrollY;
              const secs = [...document.querySelectorAll('[data-section]')].map(s => {
                const r = s.getBoundingClientRect();
                return {name: s.dataset.section, top: r.top + scrollY - top, bottom: r.bottom + scrollY - top};
              });
              const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
              return {height: root.scrollHeight, secs, broken,
                      todos: document.querySelectorAll('.todo, .ph').length};
            }"""
        )
        box = (page.query_selector(".page") or page.query_selector("body")).bounding_box()
        # 긴 페이지는 한 번에 찍으면 깨질 수 있어 3000px씩 나눠 찍고 이어 붙인다
        h = info["height"]
        img = Image.new("RGB", (round(BASE_WIDTH * SCALE), round(h * SCALE)), "white")
        tmp = html.parent / "export" / "_part.png"
        tmp.parent.mkdir(parents=True, exist_ok=True)
        y, step = 0.0, 3000.0
        while y < h:
            ch = min(step, h - y)
            page.screenshot(path=str(tmp), full_page=True,
                            clip={"x": box["x"], "y": box["y"] + y, "width": BASE_WIDTH, "height": ch})
            with Image.open(tmp) as part:
                img.paste(part.convert("RGB"), (0, round(y * SCALE)))
            y += ch
        tmp.unlink()
        browser.close()
    return img, info


def plan_cuts(height: float, secs: list[dict], max_h: float) -> list[tuple[float, float]]:
    """섹션 경계 기준으로 [시작, 끝] 조각 목록(CSS px)."""
    bounds = sorted({0.0, float(height), *(s["top"] for s in secs), *(s["bottom"] for s in secs)})
    bounds = [b for b in bounds if 0 <= b <= height]
    cuts, start = [], 0.0
    for i, b in enumerate(bounds[1:], 1):
        if b - start > max_h:
            prev = bounds[i - 1]
            if prev > start:  # 이전 경계에서 끊는다
                cuts.append((start, prev))
                start = prev
            while b - start > max_h:  # 그래도 길면 강제로 나눈다
                cuts.append((start, start + max_h))
                start += max_h
    if height - start > 1:
        cuts.append((start, height))
    return cuts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html", type=Path)
    ap.add_argument("--targets", default="smartstore:860,coupang:780", help="이름:폭,이름:폭")
    ap.add_argument("--max-height", type=int, default=2000, help="판매처 폭 기준 조각 최대 높이(px)")
    ap.add_argument("--quality", type=int, default=90)
    ap.add_argument("--skip", default="", help="이미지에서 숨길 class (쉼표). 예: partners,disclosure")
    a = ap.parse_args()

    if not a.html.exists():
        sys.exit(f"파일이 없어요: {a.html}")
    skip = [s.strip().lstrip(".") for s in a.skip.split(",") if s.strip()]
    full, info = capture(a.html, skip)
    css_h = info["height"]
    px_per_css = full.width / BASE_WIDTH

    out_root = a.html.parent / "export"
    report = []
    for spec in a.targets.split(","):
        name, w = spec.split(":")
        w = int(w)
        ratio = w / BASE_WIDTH
        max_css = a.max_height / ratio
        d = out_root / name
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        scaled_full = full.resize((w, round(full.height * w / full.width)), Image.LANCZOS)
        scaled_full.save(d / "full.png", optimize=True)
        cuts = plan_cuts(css_h, info["secs"], max_css)
        for n, (s, e) in enumerate(cuts, 1):
            piece = full.crop((0, round(s * px_per_css), full.width, min(full.height, round(e * px_per_css))))
            piece = piece.resize((w, max(1, round(piece.height * w / piece.width))), Image.LANCZOS)
            piece.save(d / f"{n:02d}.jpg", quality=a.quality, optimize=True, progressive=True)
        report.append(f"  {name}: {w}px × {len(cuts)}장 → {d}")

    print("✅ 내보내기 완료")
    print("\n".join(report))
    print(f"  섹션 {len(info['secs'])}개: " + " → ".join(s["name"] for s in info["secs"]))
    if info["todos"]:
        print(f"  ⚠ 빈칸 표시 {info['todos']}곳이 이미지에 남아 있어요 (open-items.md 확인)")
    if info["broken"]:
        print("  ❌ 깨진 사진: " + ", ".join(info["broken"]))


if __name__ == "__main__":
    main()
