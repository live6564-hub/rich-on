---
name: video-watch
description: 유튜브 링크나 영상 파일을 클로드가 "진짜로 보게" 만드는 스킬. 영상을 자막(말, 타임스탬프 포함) + 타임스탬프 프레임 보드(화면)로 바꿔서 읽는다. 로아가 "이 영상 봐줘", "이 링크 분석해줘", "레퍼런스 영상", "영상 보고 정리", "이 영상 검수해줘", "업로드 전 점검", 유튜브/쇼츠 URL, mp4 파일을 주면 사용. 작은 글씨·숫자는 돋보기(--at)로 원본 크기 확인 후 판단. 제목·설명만 보고 지어내기 절대 금지.
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

## 🔍 돋보기 (작은 글씨·숫자 확인) — 필수 규칙
보드 한 칸은 가로 360px라서 각주·계산식 같은 작은 글씨는 잘못 읽힌다(실제 사례: 53.4%를 "화면 계산과 안 맞는다"고 오판 → 원본 크기로 보니 3,312÷6,205=53.4% 정확).
- 숫자·계산식·각주가 **의심스럽거나 안 읽히면**, 그 시간 프레임을 원본 크기로 다시 뽑아서 Read 로 본다:
```bash
python <이 스킬 폴더>/watch.py "<같은 링크 또는 파일>" --out video-watch-out --at 16,20,1:02
```
  → `video-watch-out/zoom_000016.png …` (이미 받은 영상을 재사용, 다시 다운로드 안 함)
- **돋보기로 확인하기 전에는 "틀렸다"고 단정하지 않는다.** 보드만 보고 한 판단은 "확인 필요"로 표시한다.
- 숫자가 올라가는 애니메이션(카운트업) 중간값(예: 6,931 → 284,700)은 오류가 아니다. 다음 프레임에서 최종값을 확인한다.

## ✅ 업로드 전 검수 체크리스트 ("이 영상 검수해줘")
로아가 자기 영상 검수를 요청하면 아래 순서대로 전부 하고, 마지막에 표로 결과를 낸다.
1. **대사** — transcript 전체 읽기. 자동 자막 오인식 표시(예: "애니 딜러들은" = 애니 딜러드). 대사 속 숫자 목록화.
2. **화면** — 보드 전부 읽기. 대사와 시간 맞춘 장면표 작성.
3. **숫자 검산** — 대사·화면의 모든 숫자를 직접 계산. 계산식·전제(나이, 수면시간, 연 일수 등)가 화면에 있으면 돋보기로 읽고 그 전제로 검산. 전제가 없으면 "검산 불가 — 전제 화면 표기 추천".
4. **대사 ↔ 화면 일치** — 같은 시간에 말과 화면 숫자가 같은지.
5. **레이아웃** — 글자 잘림(특히 화면 오른쪽 끝 각주), 글자 겹침, 폰에서 안 읽히는 작은 글씨. 의심되면 돋보기.
6. **흐름** — 훅(0~3초), 톤 전환 시점, 마무리 행동 문장이 있는지.
7. **결과 표** — `항목 | 결과(✅/⚠️/❌) | 근거(시간·계산식) | 고칠 방법`. 확실한 것과 "확인 필요"를 구분.

실제 검수 예시 (에이로그원 #11월 #시간 #50대, 1:06):
- 82.5세 = 50세 남성 + 기대여명 32.5년(2024 생명표, 화면 각주) → 722,700 / 438,000 / 284,700시간 ✅
- 53.4% = 집 밖 3,312 ÷ 깨어 있는 6,205시간 ✅ / 55일×24 = 1,320시간 ✅ / 39.4% = 32.5÷82.5 ✅
- ⚠️ 하단 가정 각주가 오른쪽 끝에서 잘림("…바깥 약속 주 2"), 각주 글씨가 폰에서 거의 안 읽힘

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
