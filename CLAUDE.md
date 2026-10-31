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

## 📸 인스타그램 스킬 13개 (/ig-*)

- 출처: https://github.com/Jakeschincariol/instagram-agent-skill (MIT, 무료·API 키 없음). 위치: `.claude/skills/ig-*`
- 스킬은 글만 쓴다. 인스타 게시는 로아가 직접 한다. 자동 팔로우·자동 댓글·자동 게시 금지.
- 스킬 안내에 `~/.claude/instagram/voice.md` 가 나오면, 이 프로젝트의 `.claude/instagram/voice.md` 를 읽는다
  (클라우드 세션은 홈 폴더가 매번 지워지기 때문). swipe.md · log.md 도 같은 폴더에 저장한다.
- 해시태그는 게시물당 최대 5개.
- 한국어 패치: beats.py · hookscore.py · swipe.py 가 한글 어절을, caption.py 가 한글 해시태그를 센다.
  점수 기준(훅 공식·슬롭 단어)은 영어 기준이라 한국어 점수는 참고용으로만 본다.
