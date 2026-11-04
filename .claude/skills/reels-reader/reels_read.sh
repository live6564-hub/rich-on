#!/usr/bin/env bash
# 릴스 읽어줘 — 다운로드 → 받아쓰기 → 장면 사진 추출
# 사용: bash reels_read.sh <릴스링크> [작업폴더]
set -euo pipefail
URL="${1:?릴스 링크를 넣어주세요}"
OUT="${2:-${TMPDIR:-/tmp}/reels_$(date +%Y%m%d_%H%M%S)}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT/frames"

# 0) 프로그램 확인 (없으면 설치)
command -v yt-dlp >/dev/null || pip install -q yt-dlp
command -v ffmpeg >/dev/null || { echo "ffmpeg 없음: https://ffmpeg.org/download.html 설치 필요"; exit 2; }
python3 -c "import faster_whisper" 2>/dev/null || pip install -q faster-whisper

# 1) 다운로드 (cookies.txt 가 스킬 폴더나 작업폴더에 있으면 사용)
COOKIE_ARGS=()
for c in "$OUT/cookies.txt" "$HERE/cookies.txt"; do
  [ -f "$c" ] && COOKIE_ARGS=(--cookies "$c") && break
done
if ! yt-dlp -q --no-warnings "${COOKIE_ARGS[@]}" -f "mp4/best" -o "$OUT/video.%(ext)s" \
     --write-info-json "$URL"; then
  echo "DOWNLOAD_FAILED"; exit 3
fi
VID="$(ls "$OUT"/video.* | grep -v '\.json$' | head -1)"

# 2) 받아쓰기 (한국어)
python3 -I - "$VID" "$OUT/transcript.txt" <<'PY'
import sys
from faster_whisper import WhisperModel
vid, out = sys.argv[1], sys.argv[2]
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(vid, language="ko", vad_filter=True)
with open(out, "w", encoding="utf-8") as f:
    for s in segs:
        f.write(f"[{s.start:06.2f}-{s.end:06.2f}] {s.text.strip()}\n")
PY

# 3) 장면 전환마다 사진 1장 (+ 첫 프레임). 장면이 너무 적으면 2초 간격으로 보충
ffmpeg -loglevel error -i "$VID" -vf "select='eq(n,0)+gt(scene,0.3)',showinfo,scale=540:-2" \
  -vsync vfr "$OUT/frames/scene_%03d.jpg" 2> "$OUT/scenes.log" || true
grep -o 'pts_time:[0-9.]*' "$OUT/scenes.log" | cut -d: -f2 > "$OUT/scene_times.txt" || true
if [ "$(ls "$OUT/frames" | wc -l)" -lt 3 ]; then
  rm -f "$OUT/frames"/*
  ffmpeg -loglevel error -i "$VID" -vf "fps=1/2,scale=540:-2" "$OUT/frames/scene_%03d.jpg"
  n=$(ls "$OUT/frames" | wc -l); seq 0 2 $(( (n-1)*2 )) > "$OUT/scene_times.txt"
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
echo "OUT=$OUT"; echo "DURATION=$DUR"; echo "FRAMES=$(ls "$OUT/frames" | wc -l)"
