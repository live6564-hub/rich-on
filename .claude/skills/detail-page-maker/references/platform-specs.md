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

## 3. 리치온 판매 링크 블록 (cta 섹션 끝에 항상)

**기본 = 쿠팡 파트너스 1개.** 로아님이 상품 전용 판매 링크를 주면 그때 href만 바꾸거나 버튼을 더한다.
(테무·알리·트립닷컴 링크는 로아님이 요청할 때만 넣는다.)

```html
<div class="partners">
  <a href="https://link.coupang.com/a/ek5cwF" target="_blank" rel="noopener">쿠팡에서 오늘 가격 보기</a>
</div>
<p class="disclosure">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다. 브랜드 공식 페이지가 아닌 리치온의 소개 페이지예요.</p>
```

- 고지 문구 첫 문장은 쿠팡 파트너스 규정 문구 그대로 쓴다(바꾸지 않는다).
- 이미지 조각 안의 버튼은 눌리지 않는다. 블로그·리틀리에 올릴 때는 이미지 아래에 같은 링크를 글자로 한 번 더 단다.
- 판매처(스마트스토어·쿠팡 판매자센터)에 상세 이미지로 올릴 때는 `export_slices.py --skip partners,disclosure`.

### 나중에 쓸 다른 제휴 링크 (요청 시에만)
- 테무 https://bitl.bz/qQEIlA · 알리익스프레스 https://bitl.bz/fjcH9p
- 트립닷컴 https://kr.trip.com/?Allianceid=8001792&SID=302477743&trip_sub1=https%3A%2F%2Flitt.ly%2Flive.6564&trip_sub3=D14461428
