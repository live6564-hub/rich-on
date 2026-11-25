#!/usr/bin/env python3
"""scene.html → 9:16 MP4 (무료, 이 컴퓨터 안에서만 처리).

render(t)를 프레임마다 호출해 1080×1920 스크린샷을 찍고 ffmpeg로 이어 붙인다.
사용: python3 render.py [길이초=18] [fps=30]
결과: video/cepolab-intro.mp4 (소리 없음 트랙 포함)
"""
import pathlib
import shutil
import subprocess
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 18.0
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
FRAMES = HERE / "_frames"
OUT = HERE / "cepolab-intro.mp4"


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001
        return p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])


def main() -> None:
    shutil.rmtree(FRAMES, ignore_errors=True)
    FRAMES.mkdir()
    total = int(DUR * FPS)
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.goto((HERE / "scene.html").as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        for i in range(total):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=str(FRAMES / f"{i:05d}.png"))
            if i % 90 == 0:
                print(f"  {i}/{total}", flush=True)
        b.close()
    ff = shutil.which("ffmpeg") or "ffmpeg"
    subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FRAMES / "%05d.png"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(OUT)], check=True)
    shutil.rmtree(FRAMES)
    print(f"✅ {OUT} ({DUR}s, {FPS}fps, 1080×1920)")


if __name__ == "__main__":
    main()
