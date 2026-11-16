---
name: video-watch
description: 유튜브 링크나 영상 파일을 클로드가 "진짜로 보게" 만드는 스킬. 영상을 자막(말, 타임스탬프 포함) + 타임스탬프 프레임 보드(화면)로 바꿔서 읽는다. 로아가 "이 영상 봐줘", "이 링크 분석해줘", "레퍼런스 영상", "영상 보고 정리", 유튜브/쇼츠 URL, mp4 파일을 주면 사용. 제목·설명만 보고 지어내기 절대 금지.
---

# video-watch — 클로드에게 '영상 보는 눈' (moongi diary EP.26 기반)

## 절대 규칙
- 링크만 보고 내용 지어내기 금지. 반드시 스크립트를 돌려 transcript.txt + board_*.jpg 를 **직접 읽은 뒤** 답한다.
- 다운로드가 막히면 솔직히 "못 봤다"고 말하고, 로아 PC에서 돌리는 방법을 안내한다.
- 전부 무료 도구(Python·ffmpeg·yt-dlp·faster-whisper·Pillow). 유료 기능(vidIQ video_watch 등)은 쓰기 전에 크레딧 확인·승인 필수.

## 어디서 실행하든 — 먼저 환경 판단
- **로아 PC의 Claude Code**: 이 스킬 폴더의 watch.py 를 바로 실행한다(아래 명령). 개인 스킬 폴더(~/.claude/skills/video-watch)에 있으면 어느 폴더에서든 쓸 수 있다.
- **claude.ai 채팅창·클라우드 세션**: 유튜브 다운로드가 막혀 있을 수 있다. 그럴 땐 ① 로아가 올린 영상 파일(mp4)로 실행하거나 ② 로아 PC에서 실행해 달라고 아래 명령 1줄을 주고, 결과(transcript.txt, board_*.jpg, info.txt 또는 .vtt)를 올려받아 읽는다.
- 로아가 결과 파일(.vtt / transcript.txt / board_*.jpg)만 올렸으면 스크립트 없이 바로 읽고 분석한다.

## 실행
```bash
python <이 스킬 폴더>/watch.py "<유튜브링크 또는 영상파일>" --out video-watch-out
# 옵션: --every 2  (프레임 간격 초, 생략 시 길이에 맞춰 자동 1/2/5/15초)
#       --whisper small (자막 없을 때 받아쓰기 모델: tiny/base/small/medium)
#       --lang ko
```
출력:
- `info.txt` — 제목·채널·길이·설명
- `transcript.txt` — `[00:00:03] 대사` 형식 (유튜브 자막 우선, 없으면 faster-whisper 받아쓰기)
- `board_01.jpg …` — 프레임 16장(4×4)씩, 각 칸 왼쪽 위에 타임스탬프

## 로아 PC 실행 명령 (복사용, 윈도우)
```
python $HOME\.claude\skills\video-watch\watch.py "실제 유튜브 주소" --out video-watch-out
explorer video-watch-out
```
※ 유튜브 주소의 `?si=...` 는 빼도 됨. 예시 글자를 그대로 넣지 않도록 실제 주소로 명령을 만들어 준다.

## 분석 규칙
- 대사 시간표 → 화면 시간표 → 둘을 맞춘 장면표 순서.
- 숫자가 나오면 직접 계산해서 검산 표를 만든다(전제가 안 나오면 "검산 불가"로 표시, 지어내지 않기).
- 자동 자막 오인식(예: "애니 딜러들은" = 애니 딜러드)을 짚어준다.
- 레퍼런스는 구조만 가져오고 문장은 베끼지 않는다.

## 읽는 순서
1. info.txt → 2. transcript.txt 전체 → 3. board_*.jpg 를 Read 로 하나씩 본다
4. 말(자막)과 화면(보드)을 타임스탬프로 맞춰서 장면별로 정리한다.

## 로아 PC 준비물 설치 (한 번만)
### 윈도우 (PowerShell)
```
winget install Python.Python.3.12
```
→ PowerShell 창 닫고 다시 열기 → 확인: `python --version`
```
pip install -U "yt-dlp[default,curl-cffi]" faster-whisper Pillow imageio-ffmpeg
winget install DenoLand.Deno
```
(ffmpeg는 imageio-ffmpeg 패키지 안에 들어 있어서 따로 설치·PATH 설정 필요 없음. PATH에 ffmpeg가 있으면 그걸 우선 사용)
(winget 없으면 python.org/downloads 에서 설치, "Add Python to PATH" 체크 필수)

### 맥 (터미널)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python ffmpeg
pip3 install -U "yt-dlp[default,curl-cffi]" faster-whisper Pillow imageio-ffmpeg
brew install deno
```
→ 확인: `python3 --version`, `ffmpeg -version`, `yt-dlp --version`

## 문제 해결
- 유튜브 다운로드 에러 → `pip install -U yt-dlp` (유튜브가 자주 바뀌어서 최신판 필요)
- 클라우드 세션(claude.ai/code)은 네트워크 정책상 youtube.com·huggingface.co 가 막혀 있을 수 있음 → 로아 PC의 Claude Code에서 실행하거나, 영상 파일을 직접 올려서 사용(파일은 프레임 보드 정상 작동).
- `HTTP Error 429 Too Many Requests` (자막) → 스크립트가 자막 실패를 건너뛰고 받아쓰기로 대체함. 영상 다운로드와 자막은 분리되어 있음.
- `No supported JavaScript runtime` 경고 → deno 설치(윈도우 `winget install DenoLand.Deno`, 맥 `brew install deno`) 후 창 다시 열기.
