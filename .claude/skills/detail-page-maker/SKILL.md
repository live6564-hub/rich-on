---
name: detail-page-maker
description: >-
  상품 사진 폴더와 상품 설명(product-info.md 또는 아무 텍스트 파일)만으로 잘 팔리는 모바일 상세페이지를
  만드는 스킬. 잘 팔리는 판매 페이지의 섹션 순서·제목 모양을 따라 상품 정보로 채우고, 풀블리드 사진과
  큰 글자의 단일 HTML을 만든 뒤 스마트스토어(860px)·쿠팡(780px) 폭 이미지 조각으로 잘라 저장한다.
  받지 못한 정보(가격·후기·인증 등)는 지어내지 않고 open-items.md 빈칸 목록으로 남긴다. 만든 뒤에는
  말 한마디로 그 섹션만 고쳐 v02, v03…으로 새 버전을 만든다. 발동 — "detail-page-maker", "상세페이지
  만들어 줘", "이 폴더 상품 상세페이지", "스마트스토어용 이미지", "쿠팡 상세 이미지", "상세페이지 잘라 줘",
  "첫 화면 제목 바꿔 줘", "이 섹션만 고쳐 줘". (리치온 9컷 화보는 richon-9cut-detail-page, 9:16 단일
  상품소개 페이지는 richon-product-page가 우선이다.)
argument-hint: "[상품 폴더] [참고 페이지 링크] [수정 요청]"
---

# detail-page-maker — 잘 팔리는 상세페이지 자동 제작

요청: `$ARGUMENTS` (비어 있으면 대화에서 요청을 읽는다)

이 스킬 폴더 = `${CLAUDE_SKILL_DIR}` (펼쳐지지 않았으면 Claude Code가 알려 준 "Base directory for this skill"을 쓴다).

## 0. 절대 규칙 (매번 지킨다)

1. **지어내지 않는다.** 가격·할인율·후기·별점·판매량·인증·수상·성분 수치·효능은 입력 파일에 있는 것만 쓴다.
   없는 칸은 페이지에 `[확인 필요: 가격]`처럼 회색 빈칸으로 두고 `open-items.md`에 적는다.
2. **효능 과장 금지.** 식품·화장품·건강 제품은 "치료·예방·완치·100%" 같은 표현을 쓰지 않는다
   (식품표시광고법·화장품법). 애매하면 open-items.md에 "표현 확인 필요"로 남긴다.
3. **참고 페이지는 구조만 빌린다.** 섹션 순서·제목 길이·리듬만 따른다. 로고·상표·문장·원본 이미지는 절대 복사하지 않는다.
4. **무료 범위만.** 이미지 생성(Firefly·Canva AI·fish.audio·vidIQ·Google Flow 등)처럼 크레딧이 들 수 있는
   도구는 실행 전에 멈추고 → 남은 크레딧 확인 → 예상 소모량 안내 → 사용자가 "허락"한 뒤에만 쓴다.
   이미지 생성 도구가 없거나 허락이 없으면 연출컷을 만들지 않고, 그 자리에 "사진 필요" 빈칸을 둔다.
5. **이전 버전은 건드리지 않는다.** 수정은 항상 새 폴더(v02, v03…)에서 한다.

## 1. 입력 읽기

현재 폴더(또는 사용자가 말한 폴더)에서:

- 상품 설명: `product-info.md` → 없으면 `*.md`, `*.txt` 중 상품 설명으로 보이는 파일
- 사진: `assets/` → 없으면 폴더 안의 `*.jpg, *.jpeg, *.png, *.webp`
- 사진은 하나씩 직접 열어 본다(Read 도구로 이미지 확인). 무엇이 찍혔는지·밝기·여백·세로/가로를 메모해
  어느 섹션에 맞는지 정한다. 파일 이름만 보고 추측하지 않는다.

입력이 너무 적으면(상품명조차 없음) 그때만 짧게 물어본다. 나머지 빈 정보는 묻지 말고 open-items.md로 넘긴다.
양식은 `${CLAUDE_SKILL_DIR}/templates/product-info.example.md`를 참고(사용자에게 보여 줘도 된다).

## 2. 참고 페이지 정하기

- 사용자가 링크를 줬으면 그 페이지를 읽고(web-fetch 등), **섹션 순서와 제목 모양만** 뽑는다.
- 링크가 없으면 같은 카테고리의 잘 팔리는 상세페이지 2~3개를 웹 검색으로 찾아 공통 흐름을 뽑는다.
  검색이 막히면 `${CLAUDE_SKILL_DIR}/references/section-patterns.md`의 카테고리별 기본 흐름을 쓴다.
- 뽑은 결과를 `out/vNN/reference-notes.md`에 적는다: 참고 URL, 섹션 순서, 제목 글자 수, 강조 방식.

## 3. 섹션 설계

`references/section-patterns.md`의 섹션 사전에서 골라 8~12개 섹션으로 순서를 정한다. 기본 뼈대:

`hero → pain → solution → point-1 → point-2 → point-3 → proof → how-to → review → compare → spec → faq → cta`

- 정보가 없는 섹션은 빼거나(예: 후기 0개면 review 삭제) 빈칸으로 둔다. 빈칸이 페이지의 30%를 넘으면 빼는 쪽을 택한다.
- 제목은 **한 줄 12자 안팎, 최대 2줄**. 숫자·대비("당김은 빼고 촉촉함만")·질문형을 섞는다.
- 본문은 섹션당 2~3줄. 스크롤하며 읽히게 큰 글자(본문 30px 이상, 제목 56px 이상 — 860px 기준).

## 4. HTML 만들기

1. 버전 폴더 만들기:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/new_version.py" out
   ```
   → `out/v01/`(이미 있으면 다음 번호) 경로를 출력한다. 첫 버전이면 템플릿이 `index.html`로 복사된다.
2. `out/vNN/index.html`을 템플릿(`templates/page.html`) 규칙대로 채운다.
   - 모든 섹션은 `<section class="sec" data-section="이름">` — 이 이름이 수정·자르기의 기준이다.
   - 사진은 `assets/`를 상대 경로로 참조하지 말고 **`out/vNN/img/`로 복사**한 뒤 `img/파일명`으로 쓴다
     (버전 폴더만 따로 옮겨도 깨지지 않게).
   - 풀블리드 사진: `class="bleed"` (좌우 여백 0). 사진 위 글자는 `.over` + 어두운 그라데이션.
   - 색은 `:root`의 `--brand`, `--brand-soft`, `--ink`만 바꿔 테마를 맞춘다(색 바꾸기 요청도 여기만 수정).
   - 빈 정보: `<span class="todo">[확인 필요: 항목]</span>`, 빈 사진: `<div class="ph" data-need="설명">사진 필요 · 설명</div>`.
3. 리치온(Rich-On) 상품이면 마지막 cta 섹션에 파트너스 링크 4개와 고지문을 넣는다
   (`references/platform-specs.md`의 "리치온 파트너스 블록"). 일반 상품이면 넣지 않는다.

## 5. open-items.md 쓰기

`out/vNN/open-items.md`에 체크박스 목록으로:

```markdown
# 채워야 할 빈칸 (vNN)
## 정보
- [ ] 판매가 / 할인가 — 섹션: cta
- [ ] 실제 구매 후기 3개 이상 — 섹션: review (지금은 섹션 삭제됨)
## 사진
- [ ] 사용 장면 컷(손+제품, 세로) — 섹션: how-to
## 표현 확인
- [ ] "피부 장벽 강화" — 실증 자료 있으면 유지, 없으면 "피부 보습"으로
```

## 6. 이미지로 자르기 (판매처별)

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/export_slices.py" out/vNN/index.html
```

- 결과: `out/vNN/export/smartstore/01.jpg …` (860px), `out/vNN/export/coupang/01.jpg …` (780px),
  각 폴더의 `full.png`(통이미지).
- 섹션 경계에서 자르고, 한 조각이 너무 길면(기본 2000px) 그 안에서 나눈다. 옵션은 `--help`.
- Playwright가 없다는 오류가 나면: `pip install playwright pillow && playwright install chromium`.
  설치가 막힌 환경이면 HTML까지만 넘기고 그 사실을 알린다.
- 자른 뒤 **조각 1~2장을 직접 열어 확인**한다: 글자 잘림, 폰트 깨짐(□□□), 사진 비율 깨짐, 빈 화면.
  문제가 있으면 고치고 다시 자른다.

## 7. 고치기 (말 한마디 수정)

사용자가 "첫 화면 제목을 '당김은 빼고 촉촉함만'으로 바꾸고 색은 피치로" 같이 말하면:

1. `python3 "${CLAUDE_SKILL_DIR}/scripts/new_version.py" out` → 최신 버전을 통째로 복사한 `vNN+1` 생성.
2. 요청이 가리키는 섹션(`data-section`)만 수정한다. "첫 화면"=hero, "후기"=review, "사용법"=how-to,
   "색"=`:root` 변수(피치 예: `--brand:#F28C6B; --brand-soft:#FFE9DF`). 나머지 섹션 HTML은 한 글자도 바꾸지 않는다.
3. 다시 자르고, `out/vNN/changes.md`에 "무엇을 / 어느 섹션 / 왜"를 3줄로 남긴다.
4. 이전 버전 폴더는 그대로 둔다.

## 8. 끝낼 때 보고

마크다운 코드 블록 안에 정리해서 알려 준다:

```
✅ 상세페이지 vNN 완료
- HTML: out/vNN/index.html
- 스마트스토어 860px: N장 / 쿠팡 780px: N장 (out/vNN/export/)
- 섹션: hero → … → cta (총 N개)
- 빈칸: 정보 N개 · 사진 N개 · 표현확인 N개 → out/vNN/open-items.md
- 주의: 860·780px은 일반 권장값 — 올리기 전에 판매자센터 기준 한 번 확인
```

그리고 다음에 할 수 있는 수정 예시 2개를 한 줄씩 제안한다.
