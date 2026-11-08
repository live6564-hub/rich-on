# 판매처 규격 · 고지문

## 1. 내보내기 폭 (일반 권장값 — 올리기 전에 판매자센터 기준 확인)

| 판매처 | 폴더 | 폭 | 조각 최대 높이(기본) | 형식 |
|---|---|---|---|---|
| 네이버 스마트스토어 | export/smartstore | 860px | 2000px | JPG 품질 90 |
| 쿠팡 | export/coupang | 780px | 2000px | JPG 품질 90 |

- 폭·높이는 `export_slices.py --targets smartstore:860,coupang:780 --max-height 2000`으로 바꿀 수 있다.
- 한 장 용량이 크면 `--quality 85`로 낮춘다.
- 판매처 정책은 자주 바뀐다. 이 표는 출발점일 뿐이다.

## 2. 상품 정보 고시 (spec 섹션 기본 항목)

공통: 품명·모델명 / 제조사(수입자) / 제조국 / 용량·수량 / 소비자상담 연락처
- 식품: 원재료·함량, 알레르기 유발물질, 보관 방법, 소비기한
- 화장품: 전성분, 사용상 주의사항, 사용기한
- 전기제품: KC 인증번호, 정격전압·소비전력, 출시연월, AS 책임자

모르는 칸은 `[확인 필요]`로 두고 open-items.md에 적는다.

## 3. 리치온 파트너스 블록 (리치온 상품일 때만 cta 섹션 끝에)

```html
<div class="partners">
  <a href="https://link.coupang.com/a/ek5cwF" target="_blank" rel="noopener">🛒 쿠팡에서 보기</a>
  <a href="https://bitl.bz/qQEIlA" target="_blank" rel="noopener">🛍️ 테무에서 보기</a>
  <a href="https://bitl.bz/fjcH9p" target="_blank" rel="noopener">🛒 알리익스프레스에서 보기</a>
  <a href="https://kr.trip.com/?Allianceid=8001792&amp;SID=302477743&amp;trip_sub1=https%3A%2F%2Flitt.ly%2Flive.6564&amp;trip_sub3=D14461428" target="_blank" rel="noopener">✈️ 트립닷컴</a>
</div>
<p class="disclosure">이 페이지는 쿠팡 파트너스·제휴 마케팅 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
```

- 이미지로 자른 조각에서는 링크가 눌리지 않는다. 판매처에 올리는 이미지에는 파트너스 블록을 빼고
  (`export_slices.py --skip partners`), 블로그·리틀리용 HTML에만 남긴다.
