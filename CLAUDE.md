# 리치온(Rich-On) 프로젝트 규칙

## 💸 무료로 쓰기 위한 약속 (절대 규칙)

로아는 모든 AI·디자인·영상 도구를 무료 범위에서만 쓴다.

- 크레딧·결제가 들 수 있는 기능은 실행 전에 반드시 멈춘다.
- 먼저 남은 크레딧(잔액)을 확인해서 로아에게 알려준다.
- 이번 작업에 드는 예상 크레딧을 알려준다.
- 로아가 명확하게 허락한 뒤에만 실행한다. 허락 없이는 절대 실행하지 않는다.
- 무료로 할 수 있는 다른 방법이 있으면 먼저 제안한다.

특히 주의할 기능:

- vidIQ: 영상 만들기(generate_video, generate_broll, generate_clips), 음악 만들기(generate_music),
  썸네일 만들기(generate_thumbnail, refine_thumbnail), 목소리 만들기(voiceover_generate),
  영상 편집(edit_media, compose, motion_graphics). 잔액 확인은 vidiq_balance.
- Adobe: 일부 이미지·영상 편집 기능(Firefly 생성, 생성형 채우기·확장 등).
- fish.audio: 음성·이미지·영상 생성. estimate로 예상 비용을 확인한 뒤 승인을 받는다.
- Canva: 유료(왕관) 요소, AI 이미지 생성.
- Google Flow 영상 생성.
- 그 밖에 크레딧·결제가 생길 수 있는 모든 도구.

## 🛍️ 상세페이지 스킬 (고정 워크플로우)

- 로아가 "OOO 상세페이지"라고 하면 `.claude/skills/detail-page-maker` 스킬의 STEP 1~9를 그대로 한다:
  자료 검색(출처 필수) → 사진 무료 선명화 → AI 티 안 나는 잡지형 상세페이지 → 판매처 이미지 조각 → 사진 한 장 9:16 영상.
- "플로우로" 요청이면 STEP 7-B: 시작 이미지·프롬프트 준비 → 로아가 크레딧 승인 후 플로우 생성 → 받은 MP4 2개에 한글 자막 무료 합성.
- 판매 링크는 기본 쿠팡 파트너스 1개(https://link.coupang.com/a/ek5cwF) + 쿠팡 파트너스 규정 고지문.
  상품 전용 판매 링크는 로아가 나중에 준다.
- 결과는 `detail-pages/<제품-슬러그>/`에 둔다. 기준 예시: `detail-pages/cepolab-biogenic-essence/`.
- 다른 컴퓨터·코덱스 설치: 루트의 `detail-page-maker.zip`을 `~/.claude/skills/` 또는 `~/.codex/skills/`에 풀기.
