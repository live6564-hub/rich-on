---
name: detail-page-maker
description: >-
  제품명 하나(+사진 1장)만 주면 AI 티 안 나는 잡지형 모바일 상세페이지와 사진 한 장 소개 영상(9:16·18초)까지
  무료로 한 번에 만드는 리치온 고정 워크플로우. 공식몰·공식스토어·언론을 검색해 출처 붙은 사실만 쓰고,
  상품정보고시를 채우고, 최저가~최고가 가격 섹션과 단점을 먼저 말하는 솔직 섹션을 넣는다. 작은 사진은
  무료 EDSR 모델로 선명하게 키우고, 스마트스토어 860px·쿠팡 780px 이미지 조각으로 자르며, 판매 링크는
  기본 쿠팡 파트너스 1개 + 규정 고지문. 원하면 앞부분을 구글 플로우 실사 장면으로 바꾸고 한글 자막만 무료 합성하는
  플로우 고급 버전(STEP 7-B)도 만든다. 받지 못한 정보는 지어내지 않고 open-items.md에 남기고, 수정은
  v02·v03 새 버전으로 섹션만 고친다. 발동 — "상세페이지", "OOO 상세페이지 만들어 줘", "제품명만 바꿔서",
  "AI 티 안 나게", "detail-page-maker", "사진 한 장으로 영상", "소개 영상", "스마트스토어용 이미지",
  "쿠팡 상세 이미지", "이 섹션만 고쳐 줘", "가격 최저 최고", "플로우로 영상", "플로우 영상 합쳐 줘". (9컷 화보는 richon-9cut-detail-page,
  9:16 단일 소개 카드는 richon-product-page가 우선.)
argument-hint: "[제품명] [사진 경로] [참고 링크] [수정 요청]"
---

# detail-page-maker — 리치온 상세페이지 + 사진 한 장 영상 고정 워크플로우

요청: `$ARGUMENTS` (비어 있으면 대화에서 읽는다)
스킬 폴더 = `${CLAUDE_SKILL_DIR}` (펼쳐지지 않았으면 "Base directory for this skill" 경로)
기준 결과물(이대로 만든다): 리치온 저장소 `detail-pages/cepolab-biogenic-essence/` — v02 상세페이지 + video/

> **로아님이 제품명만 바꿔 말하면 아래 STEP 1~9를 처음부터 끝까지 그대로 한다.** 중간에 묻지 않는다.
> 예외: 사진이 하나도 없을 때만 "사진 1장만 주세요"라고 한 번 묻는다(그동안 글·표로 먼저 만든다).

## 0. 절대 규칙
1. **지어내지 않는다.** 가격·후기·별점·판매량·인증·효능 수치는 출처가 있는 것만. 출처는 각주로 단다.
2. **효능 과장 금지.** 치료·예방·완치·100% 금지(화장품법·식품표시광고법). 브랜드 시험 결과는 "브랜드 인체적용시험" 같이 주체를 밝힌다.
3. **참고 글은 흐름만.** 남의 문장·사진·로고 디자인 복사 금지. 사진은 로아님이 준 것만 쓴다.
4. **무료만.** 이 워크플로우 전체가 크레딧 0이다. 크레딧이 드는 도구(플로우·Higgsfield·vidIQ·fish.audio·Firefly·Canva AI)는
   쓰지 않는다. 로아님이 따로 원하면 → 잔액 확인 → 예상 소모량 안내 → 명확한 허락 후에만.
5. **AI 티 금지.** `references/no-ai-look.md`를 매번 지킨다(로아님이 말하지 않아도).
6. **판매 링크 = 쿠팡 파트너스 1개 기본.** 상품 전용 링크는 로아님이 나중에 준다. 받으면 href만 바꾼다.
7. **이전 버전은 건드리지 않는다.** 수정은 항상 새 vNN.

## STEP 1. 작업 폴더
리치온 저장소 안이면 `detail-pages/<영문-제품-슬러그>/`를 만들고 그 안에서 작업한다.
```
detail-pages/<slug>/
├─ assets/            로아님이 준 원본 사진
├─ product-info.md    STEP 2에서 내가 만든다(출처 포함)
└─ out/v01/ …         결과
```

## STEP 2. 자료 찾기 → product-info.md
`references/research.md` 순서대로 웹 검색(여러 검색을 한 번에 보낸다):
① 공식몰 설명 ② 네이버 브랜드 공식스토어 상품정보고시(제조업자·사용기한) ③ 언론 숫자 ④ 단점(구입 전 참고사항·Q&A)
⑤ 같은 브랜드 다른 라인 비교 ⑥ 단품 가격 최저·공식 최저·공식몰·최고(정가).
로아님이 참고 링크를 줬으면 그 글의 흐름(섹션 순서)만 `reference-notes.md`에 적는다.
양식: `templates/product-info.example.md`. 모든 줄 끝에 출처.

## STEP 3. 사진 준비 (무료 선명화)
1. 사진을 Read로 직접 열어 본다: 무엇이 찍혔는지, 배경색, 크기.
2. `python3 "${CLAUDE_SKILL_DIR}/scripts/new_version.py" out` → `out/v01/` (에디토리얼 템플릿 복사)
3. `python3 "${CLAUDE_SKILL_DIR}/scripts/upscale_photo.py" assets/<사진> out/v01/img/product_hd.jpg`
   - 1600px 미만이면 EDSR ×4(무료 공개 모델, 약 1분). 필요: `pip install "opencv-contrib-python-headless<5" pillow`
   - 실패해도 자동으로 기본 확대로 대체된다. 결과 로고 부분을 열어 선명한지 확인.
4. 사진에서 대표색 1개를 뽑아 `:root --brand`에 넣는다(예: 원액 호박색 #A8681A).

## STEP 4. 상세페이지 HTML (out/v01/index.html)
템플릿 `templates/editorial.html`의 `{{ }}`를 product-info.md 사실로 채운다. 섹션 순서 고정:

| 섹션 | 내용 | 자료 없으면 |
|---|---|---|
| hero | 장면형 후킹 2줄(명조) + 흰 배경 사진 | 필수 |
| pain | 불편 장면 3개(행동으로) | 필수 |
| solution | 어디에 쓰는지 + 루틴 4칸 | 필수 |
| point-1 | 핵심 숫자 1개를 크게 + 그 숫자의 진짜 뜻 | 숫자 없으면 삭제 |
| point-2 | 전성분/구성/소재 번호 목록 | 필수 |
| proof | 숫자 3개(판매량·재구매율·시험) + 출처 | 출처 없으면 삭제 |
| honest | 단점·오해·처음 쓰는 요령 3줄 | 필수 |
| how-to | 4단계 | 필수 |
| compare | 같은 브랜드 다른 라인 비교표 | 없으면 삭제 |
| price | 최저~최고 막대 + 4줄 표 + 정품 확인 안내 | 필수 |
| spec | 상품정보고시(공식스토어 표기 우선) | 필수 |
| cta | 쿠팡 파트너스 버튼 1개 + 규정 고지문 + RICH-ON | 필수 |

- 다 채운 뒤 `grep -n "{{" out/v01/index.html` 결과가 비어 있어야 한다.
- 문장 규칙·금지 단어: `references/no-ai-look.md`. 판매 링크 블록: `references/platform-specs.md` 3절.

## STEP 5. open-items.md + reference-notes.md
`out/vNN/open-items.md`: 정보 / 사진 / 표현 확인으로 나눈 체크박스. 채운 것은 `[x]`, 남은 것은 `[ ]`.
항상 넣을 것: "가격은 올리기 직전 다시 확인", "쿠팡 링크를 상품 전용 링크로 교체(로아님 요청 대기)".

## STEP 6. 판매처 이미지 조각
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_slices.py" out/v01/index.html
```
→ `export/smartstore/`(860px) · `export/coupang/`(780px) · `full.png` · `sections.json`(영상용 섹션 위치).
조각 2~3장(hero·price·spec)을 직접 열어 확인: 글자 잘림, □□□ 폰트 깨짐, 흐린 사진, `[확인 필요]` 남음.

## STEP 7. 사진 한 장 소개 영상 (9:16 · 18초 · 무료)
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/make_video.py" out/v01 <slug>-intro   # 1회차: video/scene.html 생성 후 멈춤
# scene.html의 {{ }}를 상세페이지와 같은 문장으로 채움 (hero 2줄, point-1 숫자·제목, 칩 2개, 출처, 최저·최고가, 날짜)
python3 "${CLAUDE_SKILL_DIR}/scripts/make_video.py" out/v01 <slug>-intro   # 2회차: MP4 생성 (약 1분)
```
장면: [0~6초] 사진 천천히 확대 + 후킹 자막 → [6~12초] 핵심 숫자 카운트업 + 칩 → [12~17초] 상세페이지가
가격 섹션까지 스크롤, 최저·최고가 → [17~18초] "정품 판매처에서 오늘 가격 확인하세요 · 제휴 링크 포함".
- 색은 scene.html의 `#A8681A`·`#E2B56A`를 상세페이지 --brand에 맞춰 바꾼다.
- ffmpeg로 프레임 3~5장 뽑아 직접 확인(사진 뒤 흰 네모, 자막 겹침).
- 소리 없음(무음 트랙 포함). 목소리·음악은 넣지 않는다 → 올릴 때 앱 무료 음악 안내.

## STEP 7-B. 플로우 고급 버전 (로아가 "플로우로", "플로우 영상"이라고 할 때만)
앞 0~11초를 구글 플로우 실사 장면으로 바꾸고, 한글 자막·숫자는 내가 무료로 정확하게 얹는다.
기준 결과물: 리치온 저장소 `detail-pages/cepolab-biogenic-essence/video/cepolab-intro-flow.mp4`

1. 준비(무료): `python3 "${CLAUDE_SKILL_DIR}/scripts/flow_compose.py" out/vNN --start-frame`
   → `video/flow/start-frame-9x16.jpg`(상품은 아래, 위쪽은 자막 자리) + `prompts.md` + `overlay.html` 템플릿
2. `prompts.md`의 `{{ }}`를 영어로 채운다. 원칙:
   - 장면 1 = 이미지→영상, 시작 이미지 첨부, **카메라 고정**, 상품은 움직이지 않고 주변(물방울·빛)만 움직임
   - 장면 2 = 글→영상, **상품 없이** 원료·질감 장면(로고 변형 위험 0), 아래 1/3에만, 위쪽은 빈 배경
   - 둘 다 "No subtitles, no text", "NO music", 끝에 고정 방어 태그
3. **플로우 생성은 크레딧이 든다** → `flow-video-credit-approval` 규칙: 설정만 하고 멈춤 → 화면의 이번 크레딧·남은 크레딧
   확인 → 로아 "승인" 후에만 생성. 크롬 연결이 없는 클라우드 대화면 프롬프트·시작 이미지만 주고 로아가 직접 생성.
4. 로아가 준 MP4 2개 → `video/flow/src/scene1.mp4`, `scene2.mp4` (채팅 첨부 경로에서 복사)
5. 프레임 5장씩 뽑아 확인: 로고·병 변형, 위쪽 자막 자리 비었는지, 구글 ✦ 표시(지우지 않는다)
6. `overlay.html`의 `{{ }}`를 STEP 7 무료 영상과 같은 문장으로 채우고 합성(무료):
   `python3 "${CLAUDE_SKILL_DIR}/scripts/flow_compose.py" out/vNN --name <slug>-intro-flow`
   → 장면1(최대 6초)+자막 → 장면2+숫자 카운트업 → 무료 영상 12.3초~끝(상세페이지 스크롤·끝 화면). 약 16.8초.
   플로우 효과음은 살리고(없으면 무음) 음악은 넣지 않는다. 무료 영상(STEP 7)이 먼저 있어야 한다.
7. 보고 때 알릴 것: 플로우 원본이 720p면 1080p로 키워 조금 부드러움 / ✦는 AI 영상 표시라 남김 / 무료 버전도 함께 있음.

## STEP 8. 고치기 (말 한마디 수정)
1. `new_version.py out` → 최신 버전 통째 복사(영상·export 제외)한 vNN+1
2. 요청한 섹션(`data-section`)만 수정. "첫 화면"=hero, "가격"=price, "색"=`:root`. 나머지는 한 글자도 안 바꾼다.
3. STEP 6 다시, 영상에 영향 있으면 STEP 7 다시(scene.html은 새 버전 폴더로 복사돼 있음).
4. `changes.md`에 무엇을/어느 섹션/왜 3줄.

## STEP 9. 보고 (코드 블록으로)
```
✅ <제품명> 상세페이지 vNN + 소개 영상 완료 (크레딧 0)
- HTML: …/out/vNN/index.html
- 스마트스토어 860px N장 / 쿠팡 780px N장
- 영상: …/out/vNN/video/<slug>-intro.mp4 (9:16 · 18초)
- 섹션: hero → … → cta
- 채운 정보 출처: 공식몰 / 공식스토어 고시 / 언론(날짜)
- 가격: 최저 …원(판매처) ~ 최고 …원(정가) · 기준 연월
- 남은 할 일: open-items.md (가격 재확인, 쿠팡 상품 전용 링크)
```
보낸 뒤 hero 조각·price 조각·영상을 SendUserFile로 보여 주고, 다음 수정 예시 2개를 제안한다.
리치온 저장소 안이면 지정된 브랜치에 커밋·푸시한다.
