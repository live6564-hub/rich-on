# 🛍️ detail-page-maker — 상세페이지 만드는 클로드·코덱스 스킬

상품 사진 폴더 + 상품 설명 파일 → 잘 팔리는 모바일 상세페이지(HTML) + 스마트스토어·쿠팡용 이미지 조각.

## 이 스킬이 하는 일 (2026-11 리치온 고정 워크플로우)
- **제품명만 말하면** 공식몰·공식스토어·언론을 검색해 출처 붙은 사실로 상세페이지를 채워요
- **AI 티 안 나는 잡지형 디자인**: 왼쪽 정렬·가는 선·명조 제목, 이모지·그라데이션·과장 단어 없음
- 단점을 먼저 말하는 **솔직 섹션**, **최저가~최고가 가격 섹션**, 상품정보고시까지 자동
- 작은 사진은 **무료 EDSR 모델로 4배 선명하게**
- 스마트스토어(860px)·쿠팡(780px) 이미지 조각으로 잘라 저장
- **사진 한 장으로 9:16 소개 영상 18초**까지 무료로 (크레딧 0)
- **플로우 고급 버전**: 플로우 실사 장면 2개를 받으면 정확한 한글 자막·숫자를 얹어 완성본으로 합성 (합성은 무료)
- 판매 링크는 기본 **쿠팡 파트너스 1개 + 규정 고지문**
- 말 한마디로 그 섹션만 고쳐요 (v02, v03…)
- 가격·후기처럼 확인 못 한 정보는 지어내지 않고 `open-items.md`에 남겨요

## 설치

### 클로드 코드
1. `detail-page-maker` 폴더를 `~/.claude/skills/` 안에 넣어요.
   (윈도우: `C:\Users\내이름\.claude\skills\`)
   리치온 저장소 안에서 쓸 때는 이미 `.claude/skills/detail-page-maker`에 들어 있어서 따로 옮길 필요 없어요.
2. 터미널에서 한 번만:
   ```
   pip install playwright pillow imageio-ffmpeg "opencv-contrib-python-headless<5"
   playwright install chromium
   ```
3. 클로드 코드를 새로 열고 `/skills` → `detail-page-maker`가 보이면 끝.

### 코덱스
1. 같은 폴더를 `~/.codex/skills/` 안에 넣어요.
2. 위 설치 명령 2줄 (클로드 코드에서 이미 했으면 건너뛰기)
3. 코덱스를 새로 열고 "detail-page-maker 스킬이 보이니?" 라고 물어 보기.

직접 옮기기 어렵다면:
```
내려받은 detail-page-maker 폴더를 스킬 폴더에 넣고
필요한 설치까지 해 줘.
```

## 가장 쉬운 요청문 (제품명만 바꿔서)
```
세포랩 바이오제닉 에센스 하이드레이션 90% 155ml 상세페이지 만들어 줘.
사진은 이거 한 장이야.
```
→ 자료 검색 → 상세페이지 → 이미지 조각 → 소개 영상까지 한 번에 나와요.

플로우 고급 버전:
```
플로우로 영상 만들 준비해 줘.          ← 시작 이미지 + 프롬프트 2개
(플로우에서 만든 영상 2개 첨부) 합쳐 줘. ← 한글 자막·숫자 얹어 완성본
```

## 쓰는 법 (자료를 직접 줄 때)
폴더 하나에 상품 사진(`assets/`)과 상품 설명(`product-info.md` 또는 아무 텍스트 파일)을 넣고, 그 폴더에서 붙여 넣기:
```
detail-page-maker 스킬로 이 폴더의 상품 상세페이지를 만들어 줘.
상품 설명은 product-info.md, 사진은 assets 폴더에 있어.
스마트스토어와 쿠팡용 이미지까지 내보내 줘.
```
- 참고할 판매 페이지는 알아서 찾아요. 직접 정하려면 링크를 한 줄 더 적어요.
- 상품 설명 양식: `templates/product-info.example.md`
- 결과: `out/v01/index.html` + `out/v01/export/smartstore/`, `out/v01/export/coupang/` + `open-items.md`

## 고치기
```
첫 화면 제목을 '당김은 빼고 촉촉함만'으로 바꾸고 색은 피치로 바꿔 줘.
```
→ `out/v02/`가 새로 생기고, 해당 섹션만 바뀌어요.

## 알아 둘 것
- 💸 무료 범위만: 이미지 생성처럼 크레딧이 드는 도구는 잔액·예상 소모량을 먼저 알려 주고, 허락받은 뒤에만 써요. 툴이 없거나 허락이 없으면 "사진 필요" 빈칸으로 남겨요.
- 860px·780px은 일반 권장값이에요. 올리기 전에 판매자센터 기준을 한 번 확인하세요.
- 참고한 페이지의 로고·상표·원본 이미지·문장은 쓰지 않아요. 구조만 참고해요.
- 판매 링크는 기본 쿠팡 파트너스 1개 + "이 포스팅은 쿠팡 파트너스 활동의 일환으로…" 고지문. 상품 전용 링크는 나중에 주시면 바꿔요.

## 폴더 구성
```
detail-page-maker/
├─ SKILL.md                       스킬 본체(클로드·코덱스가 읽는 작업 순서)
├─ references/section-patterns.md  잘 팔리는 섹션 사전·카테고리별 흐름·제목 규칙
├─ references/platform-specs.md    판매처 폭·상품정보고시·리치온 파트너스 블록
├─ references/no-ai-look.md        AI 티 안 나는 디자인·문장 규칙 + 점검표
├─ references/research.md          제품명만으로 자료 찾는 검색 순서·가격 정리 규칙
├─ templates/editorial.html        기본 상세페이지 틀(잡지형, 12섹션)
├─ templates/page.html             예전 기본형(풀블리드·큰 글자) — --basic
├─ templates/video/scene.html      사진 한 장 소개 영상 장면 틀(9:16·18초)
├─ templates/video/flow-prompts.md 플로우 장면 2개 프롬프트 틀
├─ templates/video/flow-overlay.html 플로우 영상 위 한글 자막 틀(투명 배경)
├─ templates/product-info.example.md  상품 설명 양식
└─ scripts/
   ├─ new_version.py               out/v01, v02 … 버전 폴더 만들기
   ├─ export_slices.py             HTML → 판매처별 이미지 조각 + 섹션 위치(sections.json)
   ├─ upscale_photo.py             작은 사진 무료 4배 선명화(EDSR)
   ├─ make_video.py                사진 + 상세페이지 → 9:16 MP4 (무료)
   └─ flow_compose.py              플로우 시작 이미지 준비 + 플로우 장면·자막 합성 (합성 무료)
```
