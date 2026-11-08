# 🛍️ detail-page-maker — 상세페이지 만드는 클로드·코덱스 스킬

상품 사진 폴더 + 상품 설명 파일 → 잘 팔리는 모바일 상세페이지(HTML) + 스마트스토어·쿠팡용 이미지 조각.

## 이 스킬이 하는 일
- 잘 팔리는 상세페이지의 섹션 순서와 제목 모양을 따라 상품 정보로 채워요
- 풀블리드 사진과 큰 글자의 모바일 상세페이지(HTML)를 한 번에 만들어요
- 스마트스토어(860px)·쿠팡(780px) 폭에 맞춰 이미지 조각으로 잘라 저장해요
- 말 한마디로 그 섹션만 고쳐요 (이전 결과는 두고 v02, v03…으로 새로 만들어요)
- 가격·후기처럼 받지 못한 정보는 지어내지 않고 `open-items.md`에 빈칸 목록으로 남겨요

## 설치

### 클로드 코드
1. `detail-page-maker` 폴더를 `~/.claude/skills/` 안에 넣어요.
   (윈도우: `C:\Users\내이름\.claude\skills\`)
   리치온 저장소 안에서 쓸 때는 이미 `.claude/skills/detail-page-maker`에 들어 있어서 따로 옮길 필요 없어요.
2. 터미널에서 한 번만:
   ```
   pip install playwright pillow
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

## 쓰는 법
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
- 리치온 상품이면 마지막 섹션에 파트너스 링크 4개 + 고지문을 넣어요(판매처 이미지에서는 `--skip partners`로 빼기).

## 폴더 구성
```
detail-page-maker/
├─ SKILL.md                       스킬 본체(클로드·코덱스가 읽는 작업 순서)
├─ references/section-patterns.md  잘 팔리는 섹션 사전·카테고리별 흐름·제목 규칙
├─ references/platform-specs.md    판매처 폭·상품정보고시·리치온 파트너스 블록
├─ templates/page.html             상세페이지 HTML 뼈대(풀블리드·큰 글자·빈칸 표시)
├─ templates/product-info.example.md  상품 설명 양식
└─ scripts/
   ├─ new_version.py               out/v01, v02 … 버전 폴더 만들기
   └─ export_slices.py             HTML → 판매처별 이미지 조각(섹션 경계에서 자르기)
```
