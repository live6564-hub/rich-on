#!/usr/bin/env python3
"""플로우 장면 2개 + 자막 레이어 + 무료 영상 뒷부분 → 세포랩 소개 영상 완성본 (무료, 크레딧 0).

[0~5.5]   src/scene1.mp4 (병+물방울)        + 자막: 세수하고 30초, / 당기기 전에 한 겹
[5.5~11.1] src/scene2.mp4 (호박색 방울)      + 자막: 92.8% 카운트업 / 수분이 아니라 원료 함량
[11.1~끝]  ../cepolab-intro.mp4 12.3초부터  (상세페이지 스크롤 + 끝 화면)
장면 사이는 0.5초·0.4초 겹쳐 넘어감. 소리: 플로우 효과음 그대로, 음악 없음.
사용: python3 compose.py  → ../cepolab-intro-flow.mp4
"""
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FPS = 30
OVER_SEC = 11.2
TAIL_FROM = 12.3          # 무료 영상에서 상세페이지 장면이 온전히 보이는 시점
X1, X1_DUR = 5.5, 0.5     # 장면1→2 겹침
X2, X2_DUR = 11.1, 0.4    # 장면2→상세페이지 겹침
OUT = HERE.parent / "cepolab-intro-flow.mp4"


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001
        return p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])


def main() -> None:
    frames = HERE / "_frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((HERE / "overlay.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        for i in range(int(OVER_SEC * FPS)):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=str(frames / f"{i:05d}.png"), omit_background=True)
        b.close()

    v = "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1"
    tail_len = 18.0 - TAIL_FROM
    total = X2 + tail_len
    fc = (
        f"[0:v]{v}[s1];[1:v]{v}[s2];[2:v]trim=start={TAIL_FROM},setpts=PTS-STARTPTS,{v}[s3];"
        f"[s1][s2]xfade=transition=fade:duration={X1_DUR}:offset={X1}[ab];"
        f"[ab][3:v]overlay=0:0:eof_action=pass[abo];"
        f"[abo][s3]xfade=transition=fade:duration={X2_DUR}:offset={X2},format=yuv420p[vout];"
        f"[0:a][1:a]acrossfade=d={X1_DUR}[a12];"
        f"[a12]afade=t=out:st={X2 - 0.6}:d=0.8,apad,atrim=0:{total}[aout]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(HERE / "src" / "scene1.mp4"), "-i", str(HERE / "src" / "scene2.mp4"),
        "-i", str(HERE.parent / "cepolab-intro.mp4"),
        "-framerate", str(FPS), "-i", str(frames / "%05d.png"),
        "-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", str(OUT)], check=True)
    shutil.rmtree(frames)
    print(f"✅ {OUT} · 약 {total:.1f}초 · 1080×1920 · 크레딧 0")


if __name__ == "__main__":
    main()
