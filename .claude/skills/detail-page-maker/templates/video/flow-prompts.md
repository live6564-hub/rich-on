# {{상품명}} 소개 영상 — 구글 플로우 장면 2개 (0~11초)
<!-- 기준 예시: detail-pages/cepolab-biogenic-essence/video/flow/prompts.md. {{ }}만 상품에 맞게 바꾼다. 장면 2는 상품이 안 나오는 "원료·질감" 장면으로 (로고 변형 위험 0) -->

- 시작 이미지: `start-frame-9x16.jpg` (1080×1920, 위쪽은 자막 자리로 비워 둠)
- 한글 자막·숫자(92.8%)는 플로우에 맡기지 않는다 → 완성 클립을 받은 뒤 무료로 합성(make_video 방식)
- 크레딧: 생성 버튼 누르기 전 플로우 화면의 "생성 시 ○○ 크레딧" + 남은 크레딧을 확인하고 로아 승인 후에만 생성

## 장면 1 (0~6초) — 이미지→영상, 시작 이미지 첨부
```
Vertical 9:16 product video. Use the attached image as the exact first frame.
{{Product description in English: container, material, color, cap, logo — e.g. A clear glass bottle of golden amber essence with a black cap and embossed "cépoLAB" lettering}} stands at the bottom of the frame on a pure white seamless studio background.
EYE-LEVEL locked static camera, no zoom, no pan, no camera movement.
{{Gentle ambient motion around the product only — e.g. Small clear water droplets float and drift slowly upward around the bottle in gentle slow motion.}}
A soft white studio light sweeps slowly from left to right across the product.
The product itself never moves, rotates, or changes shape. Keep the exact shape, colors, and logo lettering.
The upper half of the frame stays clean, empty white space.
No hands, no people.
Audio: {{soft matching foley, e.g. water droplets}} only, NO music.
No subtitles, no text, no new logos.
Static camera, Keep exact facial features, No morphing, Maintain original image details, Consistent character
```

## 장면 2 (6~12초) — 글→영상 (병 없음, 로고 변형 위험 0)
```
Vertical 9:16 macro shot on a pure warm cream background, color #F6F1E8.
{{Ingredient / texture moment in the lower third, no product — e.g. A single drop of clear golden amber liquid falls in smooth slow motion into a shallow, still pool of the same amber liquid, makes a small soft crown splash, then gentle concentric ripples settle.}}
EYE-LEVEL locked static camera, no zoom, no pan.
Warm soft light, glossy highlights.
The upper two thirds of the frame stays clean, empty cream space.
No bottle, no logo, no hands, no people.
Audio: {{one matching soft foley sound}} only, NO music.
No subtitles, no text.
Static camera, Keep exact facial features, No morphing, Maintain original image details, Consistent character
```

## 받은 뒤
- 로아가 만든 MP4 2개 → `out/vNN/video/flow/src/scene1.mp4`, `scene2.mp4`
- 자막·숫자·상세페이지 스크롤은 `flow_compose.py`가 무료로 합성 (SKILL.md STEP 7-B)
