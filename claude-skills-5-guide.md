# 🧰 클로드 스킬 5개 — 리치온·에이로그원 맞춤 정리

> 원본: 인스타 @claude.archivist 자료 "무조건 같이 쓸 클로드 스킬 5개 가이드" (2026-11-22 확인 기준)
> 원본 페이지: https://claude-archivist.github.io/qavekzi6py/ · 릴스: https://www.instagram.com/reel/DgKlXn3BmFF/
> ✅ 2026-11-25 원본 페이지와 대조함 — 설치 명령 9줄이 원본과 똑같음.
> ⚠️ 별 수·명령어는 원본 자료를 옮긴 것이고, 각 깃허브 저장소는 따로 다시 확인하지 않았음. 안 되면 각 저장소 README [리드미] = 설명서 먼저 확인.

---

## 1. 한눈에 — 로아가 어디에 쓰나

| 스킬 | 하는 일 | 리치온·에이로그원 활용 | 무료 규칙 체크 |
|---|---|---|---|
| taste-skill [테이스트 스킬] | 홈페이지 한 장 디자인 + 4개 화면 폭 자동 검사 | 리틀리 대체 랜딩, 상품 소개 HTML 디자인 업그레이드 | 설치 무료 / 클로드 사용량 매우 큼(40분 걸림) → 작은 페이지만 |
| agent-browser [에이전트 브라우저] | 브라우저 열고 버튼 대신 눌러보고 캡처 | 상세페이지의 파트너스 링크 4개 버튼 실제로 눌리는지 검사 | 무료 |
| hyperframes [하이퍼프레임즈] | HTML 장면 → MP4 영상 렌더 | 9:16 상품 소개·자막 인포그래픽 5~10초 영상 (Flow 크레딧 아끼기) | 내 컴퓨터에서 렌더 → 크레딧 없음 (AI 영상 생성 아님) |
| grill-me [그릴 미] | 계획에 번호 질문 + 추천 답 | 월간 30개 기획·신상품 소싱 계획 점검 | 무료 |
| find-skills [파인드 스킬즈] | 필요한 스킬 검색 + 설치 명령 | 새 작업용 스킬 찾기 (설치 1,000 이상만) | 무료 / 남이 올린 스킬이라 README 먼저 |

📌 리치온 상품 페이지는 기존 `richon-product-page`, `richon-9cut-detail-page` 스킬이 우선. taste-skill은 "새 랜딩 한 장" 같은 별도 작업에만.

---

## 2. 어디서 되나 (중요)

- 다섯 개 모두 **클로드 코드** [Claude Code] = 터미널·데스크톱 앱 Code 탭·VS Code 에서 사용.
- claude.ai 채팅 창만으로는 4개(taste·agent-browser·hyperframes·find-skills)가 안 됨.
- 미리 깔 것: Node [노드] 22 이상(find-skills는 22.20 이상), 크롬/엣지, 영상 만들면 FFmpeg [에프에프엠펙] = 영상 변환 프로그램.

```bash
# 터미널에서 먼저 확인
node -v
claude --version
ffmpeg -version
```

---

## 3. 설치 순서 (필요한 것만 골라서)

```text
# ① taste-skill — 클로드 코드 입력 칸에
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill
```

```bash
# ② agent-browser — 터미널에
npm install -g agent-browser
agent-browser install
npx skills add vercel-labs/agent-browser
```

```bash
# ③ hyperframes — 터미널에
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
# 맥에서 FFmpeg 없으면
brew install ffmpeg
```

```bash
# ④ grill-me (묶음째 설치해야 질문 기능이 동작) — 터미널에
claude plugin install mattpocock-skills@claude-plugins-official
```

```bash
# ⑤ find-skills — 터미널에
npx skills add vercel-labs/skills --skill find-skills
```

✅ 다 깔고 나면 클로드 코드를 한 번 껐다 켜기.

---

## 4. 로아용 부탁 문장 (복사해서 쓰기)

### taste-skill — 랜딩 한 장
```text
리치온 소개 홈페이지 한 장만 작게 만들어 줘. 무자본·무재고로 살림 고수 꿀템을 소개하는 곳이고,
첫 화면 단추는 [쿠팡 / 테무 / 트립닷컴 / 알리] 4개 링크로 해 줘. 사진은 무료 공개 사진만 쓰고 출처 페이지도 만들어 줘.
```

### agent-browser — 파트너스 링크 버튼 검사
```text
[상세페이지 주소] 열어서 쿠팡·테무·트립닷컴·알리 버튼 4개가 각각 맞는 주소로 넘어가는지 확인하고 화면 찍어 줘.
구매·결제·로그인 버튼은 절대 누르지 마.
```

### hyperframes — 9:16 상품 소개 영상 (크레딧 없이)
```text
/hyperframes 리치온 [상품명] 소개 영상 만들어 줘. 9:16 세로, 5초, 제목 페이드인 + 장점 3줄 자막,
음악 없이. 내 컴퓨터에서 렌더만 하고 유료 AI 생성 기능은 쓰지 마.
```

### grill-me — 이번 달 기획 점검 (/grill-me 직접 입력해야 켜짐)
```text
/grill-me 12월 에이로그원 숏폼 30개를 12월 31일까지 올리려고 해. 리치온 상품 연계는 주 2회로 정했어. 이 계획 좀 봐 줘.
```
```text
1번 네, 2번 네, 3번은 [내 답].
```

### find-skills — 스킬 찾기
```text
유튜브 쇼츠 자막(SRT) 만들어 주는 스킬 있어? 설치 수 1,000 넘는 걸로 세 개만 알려 줘. 유료 API 키 필요한 건 빼 줘.
```

---

## 5. 체크리스트

```text
[설치 전]
[ ] claude 실행되는지   [ ] node -v 22 이상   [ ] 크롬/엣지   [ ] (영상) FFmpeg

[설치]
[ ] 필요한 것만   [ ] "입력 칸" 줄과 "터미널" 줄 구분   [ ] 클로드 코드 재시작

[첫 시험 — 리치온 버전]
[ ] 작은 랜딩 1장 (taste-skill)
[ ] 그 페이지 파트너스 버튼 4개 검사 (agent-browser)
[ ] 5초 9:16 상품 영상 (hyperframes)
[ ] /grill-me 로 이번 주 계획 점검
[ ] "~하는 스킬 있어?" 한 번 묻기 (find-skills)
```

---

## 6. 주의 사항 (무료 원칙 기준)

- 💸 다섯 개 모두 설치는 무료. 쓸 때는 **클로드 사용량**이 듦 — taste-skill이 특히 큼.
- 🎬 hyperframes는 HeyGen [헤이젠] 이 만든 도구지만 렌더는 내 컴퓨터에서 함. 배경 영상·음악을 AI로 "생성"하라고 시키면 유료 도구로 넘어갈 수 있으니 "음악 없이 / 내 소스만" 명시.
- 🖱️ agent-browser는 로그인된 사이트에서 진짜로 누름 → 무엇을 누를지·누르지 말지 먼저 말하기.
- 🔍 find-skills 검색 결과는 누구나 올린 스킬 → 설치 1,000 미만이면 조심, 깔기 전 README 읽기.
- 🗑️ 지우기: 플러그인은 `/plugin` → Installed 탭, npx로 깐 것은 `npx skills remove`.
