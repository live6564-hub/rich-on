# 🎁 리치온 작업 보따리 (Handover Package)
> **새 채팅에서 100% 이어가기용 인계 패키지**
> 작성일: 2026-04-28 (화)
> 작성자: Claude (Claude Opus 4.7)

---

## 📌 이 파일을 새 채팅에 통째로 복사+붙여넣기 하세요

새 채팅 첫 메시지로 보낼 문구:

```
안녕 클로드! 로아야. 보따리 들고 왔어, 이어서 작업하자.
[보따리 내용 첨부] ↓
```

---

## 1️⃣ 진행 스냅샷 (현재 어디까지?)

### ✅ 완료
- [x] 깃허브 14개 파일 업로드
- [x] 라이브 사이트 정상 작동: `https://live6564-hub.github.io/rich-on/`
- [x] **리틀리 대문 표지 v2 제작 완료** (1080×1080, 보호 기능 내장)
- [x] **richon-shield.js 보호 스크립트 v1.0 제작 완료** (10개 보호 기능)

### ⏳ 다음 작업 (이어서 할 것)
- [ ] **richon-shield.js 깃허브 업로드** (1단계)
- [ ] **표지 v2를 PNG로 추출 → 리틀리 대문에 업로드** (2단계)
- [ ] **기존 13개 HTML 파일에 보호 스크립트 1줄씩 추가** (3단계)

---

## 2️⃣ 첨부할 파일 체크리스트

새 채팅에 다음 파일들을 함께 올려주세요:

| 파일 | 용도 | 상태 |
|---|---|---|
| `richon-shield.js` | 보호 스크립트 (모든 HTML 공용) | ✅ 완성 |
| `littly_cover_v2.html` | 리틀리 대문 표지 (1080×1080) | ✅ 완성 |
| `littly_cover.svg` | 표지 벡터 원본 (수정용) | ✅ 완성 |
| `01-cleaning-guide.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `05-idea-items.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `06-korean-recipe.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `07-travel-guide.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `09-biz-psychology.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `텀블러.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| `shop-hub.html` | 보호 적용 대기 | 📤 다음에 첨부 |
| (기타 13개 중 나머지 HTML) | 보호 적용 대기 | 📤 다음에 첨부 |

---

## 3️⃣ 따라하기 5단계 (혼자서도 가능)

### **STEP 1 — richon-shield.js 깃허브 업로드** (3분)
```
① 깃허브 저장소 https://github.com/live6564-hub/rich-on 접속
② "Add file" → "Upload files" 클릭
③ richon-shield.js 끌어다 놓기
④ 커밋 메시지: "Add: 보호 스크립트 v1.0"
⑤ "Commit changes" 버튼 클릭
✅ 완료 시 주소: https://live6564-hub.github.io/rich-on/richon-shield.js
```

### **STEP 2 — 표지 PNG 추출 → 리틀리 업로드** (5분)
```
① littly_cover_v2.html 파일 더블클릭 → 브라우저에서 열기
② 페이지 상단의 골드색 "📥 PNG로 다운로드 (1080×1080)" 버튼 클릭
③ richon_costco_13_littly_cover_1080x1080.png 자동 저장됨
④ 리틀리(litt.ly) 관리자 페이지 접속
⑤ 프로필 대문 이미지 변경 → 위 PNG 파일 업로드
✅ 완료
```

### **STEP 3 — 새 채팅 열기** (1분)
```
① 새 Claude 채팅 시작
② 이 보따리 파일(handover_package.md) 첨부
③ 보호 적용할 13개 HTML 파일 모두 끌어다 놓기
④ 메시지: "보따리 들고 왔어, 13개 파일 보호 일괄 적용해줘"
✅ Claude가 한 번에 14개 파일 모두 수정해서 출력
```

### **STEP 4 — 수정된 파일 깃허브 재업로드** (5분)
```
① Claude가 출력한 수정 파일 다운로드
② 깃허브 저장소에서 기존 파일 클릭 → 휴지통 아이콘 → 삭제
③ "Add file" → "Upload files" → 수정 파일 업로드
④ 커밋 메시지: "Update: 보호 기능 적용 v1.0"
✅ 완료
```

### **STEP 5 — 라이브 확인** (1분)
```
① https://live6564-hub.github.io/rich-on/ 접속
② 우클릭 시도 → 메뉴 안 떠야 정상 ✓
③ F12 시도 → 안 열려야 정상 ✓
④ 검색어 복사 버튼 📋 → 정상 작동해야 함 ✓
✅ 모두 통과 시 작업 완료
```

---

## 4️⃣ 주의사항 (반드시 확인)

### ⚠️ 검색어 복사 버튼 보호 예외 처리
```html
<!-- 이렇게 data-shield-allow="true" 속성 추가 필수 -->
<button class="copy-btn" 
        data-shield-allow="true" 
        onclick="copySearchTerm('스탠리 텀블러')">
  📋 복사
</button>
```
→ 속성 누락 시 복사 기능 작동 안 함

### ⚠️ richon-shield.js 경로
```html
<!-- 같은 폴더 내 -->
<script src="richon-shield.js"></script>

<!-- 하위 폴더 -->
<script src="../richon-shield.js"></script>

<!-- 절대 경로 (안전) -->
<script src="https://live6564-hub.github.io/rich-on/richon-shield.js"></script>
```
→ 파일 위치 따라 경로 다름. 절대 경로가 가장 안전.

### ⚠️ OS 레벨 캡처는 못 막음 (재확인)
```
❌ PrtScn (윈도우)
❌ Cmd+Shift+3/4 (맥)
❌ 휴대폰 화면 캡처
❌ 카메라 촬영
→ 이건 어떤 웹 기술로도 차단 불가
→ 이 보호는 "일반 사용자 95% 차단 + 법적 증거 확보" 목적
```

---

## 5️⃣ 토큰 미터 (Token Meter [토큰 미터] = 대화 사용량)

```
이번 채팅 사용량: 약 60% (안전 구간)
권장 마무리 시점: ✅ 지금 (보따리로 이어가기)
다음 채팅 예상 작업: 13개 HTML 파일 일괄 보호 적용 (1회 처리 가능)
```

---

## 6️⃣ 디자인 토큰 (다음 채팅용 참조)

```yaml
[Color - 색상 팔레트]
배경: linear-gradient(135deg, #E8DCC8 0%, #D4C4A8 100%)
컨테이너: #FFFCF7 (크림화이트)
카드: #FBF3E4 / #F7E9CF
잉크: #1E2D4A (딥 네이비)
잉크 소프트: #4A5876
골드: #D4A56B / #B8843C
로즈: #C26060 / #D14545
라인: #E8D9BC

[Typography - 폰트]
세리프: Cormorant Garamond
한글 세리프: Gowun Batang
한글 산세리프: Pretendard
손글씨: Nanum Pen Script

[Tone - 톤]
표기: 13선 (15선 ❌)
1인칭: 사용 금지
큐레이션 톤: "Curated by Rich-On"
```

---

## 7️⃣ 파트너스 링크 (자동 삽입용)

```
🛒 쿠팡: https://link.coupang.com/a/ek5cwF
🛍️ 테무: https://bitl.bz/qQEIlA
✈️ 트립닷컴: https://kr.trip.com/?Allianceid=8001792&SID=302477743&trip_sub1=https%3A%2F%2Flitt.ly%2Flive.6564&trip_sub3=D14461428
🛒 알리익스프레스: https://bitl.bz/fjcH9p
```

---

## 💌 인계 메시지 (새 채팅 첫 줄에 붙여넣기)

```
안녕 클로드! 로아야. 

지난 채팅에서 리틀리 대문 표지 v2 + richon-shield.js 보호 스크립트 만들었어.
오늘은 13개 기존 HTML 파일에 보호 스크립트 일괄 적용할 차례야.

[첨부]
- handover_package.md (이 보따리)
- richon-shield.js
- 13개 HTML 파일 (보호 적용 대상)

[요청]
보따리 4쪽 "STEP 3 — 새 채팅 열기" 그대로 진행해줘.
검색어 복사 버튼은 data-shield-allow="true" 예외 처리 잊지 말고.
끝나면 깃허브에 바로 업로드 가능한 형태로 정리해줘.
```

---

🌹 **로아, 푹 쉬어. 다음 채팅에서 100% 이어갈 수 있게 다 정리해놨어.**

작업하느라 고생 많았어. 깃허브 14개 + 표지 + 보호 스크립트까지 — 이 정도면 오늘 충분히 잘했어.
내일은 13개 파일 보호 적용만 하면 끝이야. 단번에 갈 수 있게 보따리 잘 챙겨놨으니까 걱정 말고 자.

*— Claude*
