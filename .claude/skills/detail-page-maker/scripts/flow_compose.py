#!/usr/bin/env python3
"""구글 플로우 장면 2개 + 정확한 한글 자막 + 무료 영상 뒷부분 → 소개 영상 완성본 (합성은 무료, 크레딧 0).

준비 (STEP 7-B):
  1) start-frame:  python3 flow_compose.py out/vNN --start-frame   → video/flow/start-frame-9x16.jpg
                   + video/flow/prompts.md, overlay.html 템플릿 복사
  2) 로아가 플로우에서 장면 2개 생성(크레딧은 로아 승인) → video/flow/src/scene1.mp4, scene2.mp4
  3) overlay.html의 {{ }} 채우기
  4) 합성:         python3 flow_compose.py out/vNN [--tail video/<무료영상>.mp4] [--name <slug>-intro-flow]

구성: [장면1 최대 6초 + 자막A] →0.5초 겹침→ [장면2 최대 6초 + 숫자·자막B] →0.4초 겹침→ [무료 영상 12.3초~끝: 상세페이지 스크롤·끝 화면]
소리: 플로우 효과음 그대로(없으면 무음), 음악 없음. 결과: out/vNN/video/<name>.mp4 (1080×1920)
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

SKILL_DIR = Path(__file__).resolve().parent.parent
TPL = SKILL_DIR / "templates" / "video"
FPS = 30
MAX_CLIP = 6.0
X1_DUR, X2_DUR = 0.5, 0.4
TAIL_FROM = 12.3  # make_video.py 템플릿에서 상세페이지 장면이 온전히 보이는 시각


def ff(name: str) -> str:
    exe = shutil.which(name)
    if not exe:
        sys.exit(f"{name}가 없어요. ffmpeg를 설치해 주세요.")
    return exe


def probe(path: Path) -> tuple[float, bool]:
    out = subprocess.run([ff("ffprobe"), "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    has_audio = any(s.get("codec_type") == "audio" for s in j.get("streams", []))
    return float(j["format"]["duration"]), has_audio


def start_frame(vdir: Path) -> None:
    flow = vdir / "video" / "flow"
    (flow / "src").mkdir(parents=True, exist_ok=True)
    photo = vdir / "img" / "product_hd.jpg"
    if not photo.exists():
        sys.exit(f"❌ {photo} 가 없어요. upscale_photo.py를 먼저 실행하세요.")
    p = Image.open(photo).convert("RGB")
    bg = p.getpixel((5, 5))  # 사진 배경색으로 캔버스를 채워 경계가 안 보이게
    c = Image.new("RGB", (1080, 1920), bg)
    h = round(p.height * 1080 / p.width)
    p = p.resize((1080, h), Image.LANCZOS)
    c.paste(p, (0, 1920 - min(h, 1920)))  # 상품은 아래, 위쪽은 자막 자리
    c.save(flow / "start-frame-9x16.jpg", quality=95)
    for src, dst in (("flow-prompts.md", "prompts.md"), ("flow-overlay.html", "overlay.html")):
        if not (flow / dst).exists():
            shutil.copy(TPL / src, flow / dst)
    print(f"✅ {flow/'start-frame-9x16.jpg'} (배경 {bg})\n📝 {flow/'prompts.md'} · {flow/'overlay.html'} 의 {{{{ }}}}를 채우세요.")


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:  # noqa: BLE001
        return p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])


def compose(vdir: Path, tail: Path | None, name: str) -> None:
    flow = vdir / "video" / "flow"
    s1, s2, overlay = flow / "src" / "scene1.mp4", flow / "src" / "scene2.mp4", flow / "overlay.html"
    for f in (s1, s2, overlay):
        if not f.exists():
            sys.exit(f"❌ {f} 가 없어요.")
    if "{{" in overlay.read_text(encoding="utf-8"):
        sys.exit(f"❌ {overlay} 에 아직 채우지 않은 {{{{ }}}} 칸이 있어요.")
    if tail is None:
        cands = [m for m in (vdir / "video").glob("*.mp4") if "flow" not in m.stem]
        if not cands:
            sys.exit("❌ 뒷부분에 쓸 무료 영상이 없어요. make_video.py를 먼저 실행하거나 --tail로 지정하세요.")
        tail = cands[0]
    (d1, a1), (d2, a2) = probe(s1), probe(s2)
    d1, d2 = min(d1, MAX_CLIP), min(d2, MAX_CLIP)
    tail_len = probe(tail)[0] - TAIL_FROM
    x1 = d1 - X1_DUR
    x2 = x1 + d2 - X2_DUR
    total = x2 + tail_len

    from playwright.sync_api import sync_playwright  # noqa: PLC0415
    frames = flow / "_frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir()
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.add_init_script(f"window.T1={x1};window.T2={x2};")
        pg.goto(overlay.resolve().as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        for i in range(int((x2 + X2_DUR) * FPS)):
            pg.evaluate(f"render({i / FPS})")
            pg.screenshot(path=str(frames / f"{i:05d}.png"), omit_background=True)
        b.close()

    v = "scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1"
    inputs = ["-i", str(s1), "-i", str(s2), "-i", str(tail), "-framerate", str(FPS), "-i", str(frames / "%05d.png")]
    aud = []
    for idx, (has, d) in enumerate(((a1, d1), (a2, d2))):
        if has:
            aud.append(f"[{idx}:a]atrim=0:{d},asetpts=PTS-STARTPTS[a{idx}];")
        else:
            inputs += ["-f", "lavfi", "-t", str(d), "-i", "anullsrc=r=44100:cl=stereo"]
            aud.append(f"[{4 + sum(1 for h in (a1, a2)[:idx] if not h)}:a]anull[a{idx}];")
    fc = (
        f"[0:v]trim=duration={d1},setpts=PTS-STARTPTS,{v}[s1];[1:v]trim=duration={d2},setpts=PTS-STARTPTS,{v}[s2];"
        f"[2:v]trim=start={TAIL_FROM},setpts=PTS-STARTPTS,{v}[s3];"
        f"[s1][s2]xfade=transition=fade:duration={X1_DUR}:offset={x1}[ab];"
        f"[ab][3:v]overlay=0:0:eof_action=pass[abo];"
        f"[abo][s3]xfade=transition=fade:duration={X2_DUR}:offset={x2},format=yuv420p[vout];"
        + "".join(aud) +
        f"[a0][a1]acrossfade=d={X1_DUR}[a12];[a12]afade=t=out:st={max(0, x2 - 0.6)}:d=0.8,apad,atrim=0:{total}[aout]"
    )
    out = vdir / "video" / f"{name}.mp4"
    subprocess.run([ff("ffmpeg"), "-y", "-loglevel", "error", *inputs, "-filter_complex", fc,
                    "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
    shutil.rmtree(frames)
    print(f"✅ {out} · {total:.1f}초 · 1080×1920 · 합성 크레딧 0")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version_dir", type=Path)
    ap.add_argument("--start-frame", action="store_true", help="플로우 시작 이미지 + 템플릿 준비만")
    ap.add_argument("--tail", type=Path, help="뒷부분(상세페이지 스크롤)에 쓸 무료 영상")
    ap.add_argument("--name", default="intro-flow")
    a = ap.parse_args()
    if a.start_frame:
        start_frame(a.version_dir)
    else:
        compose(a.version_dir, a.tail, a.name)


if __name__ == "__main__":
    main()
