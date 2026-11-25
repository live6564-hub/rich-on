#!/usr/bin/env python3
"""사진 1장 + 상세페이지 → 9:16 소개 영상 18초 (무료, 크레딧 0).

순서:
  1) 처음 실행: out/vNN/video/scene.html 이 없으면 템플릿을 복사하고 멈춘다 → {{ }} 칸을 채운다
  2) 다시 실행: 사진·상세페이지 통이미지·섹션 위치를 가져와 프레임마다 찍고 MP4로 묶는다

사용: python3 make_video.py out/vNN [파일이름=intro] [--seconds 18] [--fps 30]
필요: export_slices.py를 먼저 실행(export/smartstore/full.png, export/sections.json), ffmpeg
결과: out/vNN/video/<파일이름>.mp4  (1080×1920, H.264, 무음 트랙 포함)
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_DIR / "templates" / "video" / "scene.html"


def ffmpeg_path() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg  # noqa: PLC0415
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg가 없어요: pip install imageio-ffmpeg  (또는 ffmpeg 설치)")


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001
        return p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version_dir", type=Path)
    ap.add_argument("name", nargs="?", default="intro")
    ap.add_argument("--seconds", type=float, default=18.0)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    vdir = a.version_dir
    vid = vdir / "video"
    scene = vid / "scene.html"
    if not scene.exists():
        vid.mkdir(parents=True, exist_ok=True)
        shutil.copy(TEMPLATE, scene)
        sys.exit(f"📝 {scene} 를 만들었어요. {{{{ }}}} 칸을 상세페이지 문장으로 채운 뒤 다시 실행하세요.")
    if "{{" in scene.read_text(encoding="utf-8"):
        sys.exit(f"❌ {scene} 에 아직 채우지 않은 {{{{ }}}} 칸이 있어요.")

    photo = vdir / "img" / "product_hd.jpg"
    page = vdir / "export" / "smartstore" / "full.png"
    secs = vdir / "export" / "sections.json"
    for f in (photo, page, secs):
        if not f.exists():
            sys.exit(f"❌ {f} 가 없어요. upscale_photo.py / export_slices.py 를 먼저 실행하세요.")
    (vid / "assets").mkdir(exist_ok=True)
    shutil.copy(photo, vid / "assets" / "product_hd.jpg")
    shutil.copy(page, vid / "assets" / "page.png")
    sections = json.loads(secs.read_text(encoding="utf-8"))

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    frames = vid / "_frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    total = int(a.seconds * a.fps)
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        pg.add_init_script(f"window.SECTIONS={json.dumps(sections)};")
        pg.goto(scene.resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        for i in range(total):
            pg.evaluate(f"render({i / a.fps})")
            pg.screenshot(path=str(frames / f"{i:05d}.png"))
            if i % 90 == 0:
                print(f"  {i}/{total}", flush=True)
        b.close()

    out = vid / f"{a.name}.mp4"
    subprocess.run([ffmpeg_path(), "-y", "-loglevel", "error", "-framerate", str(a.fps),
                    "-i", str(frames / "%05d.png"), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(out)], check=True)
    shutil.rmtree(frames)
    print(f"✅ {out} · {a.seconds:g}초 · {a.fps}fps · 1080×1920 · 크레딧 0")


if __name__ == "__main__":
    main()
