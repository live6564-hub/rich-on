#!/usr/bin/env python3
"""video-watch: 영상 → 자막(말) + 타임스탬프 프레임 보드(화면)
사용: python watch.py <유튜브링크 또는 영상파일> [--every 초] [--out 폴더] [--whisper small]
"""
import argparse, glob, json, os, re, subprocess, sys
from pathlib import Path

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

def find_ffmpeg():
    """PATH에 ffmpeg가 있으면 그걸, 없으면 pip 패키지 imageio-ffmpeg 안의 ffmpeg를 쓴다."""
    import shutil
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg를 찾을 수 없어요 → 이 명령을 먼저 실행하세요:  pip install imageio-ffmpeg")

FFMPEG = find_ffmpeg()

def duration(video):
    r = run([FFMPEG, "-i", video])
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", r.stderr or "")
    return int(m[1])*3600 + int(m[2])*60 + float(m[3]) if m else 0.0

def hms(t):
    t = int(t); return f"{t//3600:02d}:{t%3600//60:02d}:{t%60:02d}"

def vtt_to_text(path):
    lines, last = [], None
    cur = None
    for line in open(path, encoding="utf-8", errors="ignore"):
        line = line.strip()
        m = re.match(r"(\d+):(\d+):(\d+)[.,]\d+\s+-->", line) or re.match(r"(\d+):(\d+)[.,]\d+\s+-->", line)
        if m:
            g = [int(x) for x in m.groups()]
            cur = g[0]*3600+g[1]*60+g[2] if len(g) == 3 else g[0]*60+g[1]
            continue
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or line.isdigit():
            continue
        txt = re.sub(r"<[^>]+>", "", line).strip()
        if txt and txt != last and cur is not None:
            lines.append(f"[{hms(cur)}] {txt}"); last = txt
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--every", type=float, default=0)
    ap.add_argument("--out", default="video-watch-out"); ap.add_argument("--whisper", default="small")
    ap.add_argument("--lang", default="ko")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    video = a.src
    if not re.match(r"https?://", a.src) and not os.path.isfile(a.src):
        sys.exit(f"'{a.src}' 는 링크도 아니고 파일도 아니에요.\n→ https:// 로 시작하는 실제 유튜브 주소나, 있는 영상 파일 경로를 따옴표 안에 넣어 주세요.")
    sub_text = ""
    if re.match(r"https?://", a.src):
        for old in glob.glob(str(out/"video.*")): os.remove(old)
        print("1/4 영상 정보 확인 중...", flush=True)
        meta = run(["yt-dlp", "-J", "--no-playlist", a.src])
        if meta.returncode == 0:
            info = json.loads(meta.stdout)
            (out/"info.txt").write_text(f"제목: {info.get('title')}\n채널: {info.get('uploader')}\n길이: {hms(info.get('duration') or 0)}\n\n{info.get('description','')}", encoding="utf-8")
        print("2/4 영상 다운로드 중... (30초~2분)", flush=True)
        # 1) 영상만 먼저 받기 (자막 실패가 영상 다운로드를 막지 않게 분리)
        r = run(["yt-dlp", "--no-playlist", "-f", "bv*[height<=720]+ba/b[height<=720]/b",
                 "--merge-output-format", "mp4", "--ffmpeg-location", FFMPEG,
                 "-o", str(out/"video.%(ext)s"), a.src])
        vids = [p for p in glob.glob(str(out/"video.*")) if p.endswith((".mp4", ".webm", ".mkv"))]
        if r.returncode != 0 or not vids:
            sys.exit("다운로드 실패:\n" + r.stderr[-1500:])
        video = vids[0]
        print("3/4 자막 받는 중...", flush=True)
        # 2) 자막은 따로 시도 — 실패(429 등)해도 그냥 넘어가고 받아쓰기로 대체
        for lang in [a.lang, "en"]:
            run(["yt-dlp", "--no-playlist", "--skip-download", "--write-subs", "--write-auto-subs",
                 "--sub-langs", f"{lang}.*,{lang}", "--sub-format", "vtt", "--sleep-subtitles", "2",
                 "-o", str(out/"video.%(ext)s"), a.src])
            vtts = sorted(glob.glob(str(out/"*.vtt")), key=lambda p: "orig" not in p)
            if vtts:
                sub_text = vtt_to_text(vtts[0]); print(f"자막 사용: {os.path.basename(vtts[0])}")
                break
        else:
            print("유튜브 자막 못 받음 → 받아쓰기로 대체")
    dur = duration(video)
    if not sub_text:
        print("자막 없음 → faster-whisper 받아쓰기 중...")
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel(a.whisper, device="cpu", compute_type="int8")
            segs, _ = model.transcribe(video, language=a.lang or None, vad_filter=True)
            sub_text = "\n".join(f"[{hms(s.start)}] {s.text.strip()}" for s in segs)
        except Exception as e:
            print(f"⚠️ 받아쓰기 실패(모델 다운로드 차단 등): {e} → 화면 프레임만 진행")
            sub_text = "(받아쓰기 실패 — 화면 보드만 참고)"
    (out/"transcript.txt").write_text(sub_text or "(말소리 없음)", encoding="utf-8")
    every = a.every or (1 if dur <= 60 else 2 if dur <= 180 else 5 if dur <= 600 else 15)
    print("4/4 프레임 보드 만드는 중...", flush=True)
    fdir = out/"frames"; fdir.mkdir(exist_ok=True)
    for f in fdir.glob("*.jpg"): f.unlink()
    run([FFMPEG, "-y", "-loglevel", "error", "-i", video, "-vf", f"fps=1/{every},scale=360:-2", str(fdir/"f_%05d.jpg")])
    frames = sorted(fdir.glob("*.jpg"))
    from PIL import Image, ImageDraw, ImageFont
    try: font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except Exception: font = ImageFont.load_default()
    cols, per = 4, 16; boards = []
    for b in range(0, len(frames), per):
        chunk = frames[b:b+per]; ims = [Image.open(p).convert("RGB") for p in chunk]
        w, h = ims[0].size; rows = (len(ims)+cols-1)//cols
        board = Image.new("RGB", (w*cols, h*rows), "white"); d = ImageDraw.Draw(board)
        for i, im in enumerate(ims):
            x, y = i % cols*w, i//cols*h; board.paste(im, (x, y))
            label = hms((b+i)*every); d.rectangle([x, y, x+110, y+30], fill="black"); d.text((x+6, y+3), label, fill="yellow", font=font)
        bp = out/f"board_{b//per+1:02d}.jpg"; board.save(bp, quality=85); boards.append(bp)
    print(f"완료 ✅ 길이 {hms(dur)} / {every}초 간격 프레임 {len(frames)}장 / 보드 {len(boards)}장")
    print(f"자막: {out/'transcript.txt'}")
    for bp in boards: print(f"보드: {bp}")

if __name__ == "__main__":
    main()
