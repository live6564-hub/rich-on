/* ==========================================================
   richon-shield.js v1.0
   리치온(Rich-On) 콘텐츠 보호 스크립트
   © 2026 Rich-On by Roa
   
   [사용법]
   각 HTML 파일 </body> 태그 바로 앞에 한 줄만 추가:
   <script src="richon-shield.js"></script>
   
   [예외 처리]
   복사 허용할 요소에는 data-shield-allow="true" 속성 추가
   예: <button class="copy-btn" data-shield-allow="true">📋 복사</button>
   
   [보호 기능]
   ✅ 우클릭 차단 (메뉴 안 뜸, 알림 X)
   ✅ 텍스트 드래그 선택 차단 (조용히)
   ✅ 이미지 드래그 저장 차단
   ✅ 키보드 단축키 차단 (Ctrl+S, Ctrl+U, Ctrl+Shift+I, F12 등)
   ✅ 개발자 도구 열기 차단
   ✅ 인쇄 차단
   ✅ 메타데이터 자동 삽입 (저작권자 기록)
   ✅ Console 경고 메시지
   ❌ 사용자에게 보이는 알림/팝업 없음
   ❌ data-shield-allow="true" 요소는 정상 작동
   ========================================================== */

(function(){
  'use strict';
  
  // ===== 1. 메타데이터 자동 삽입 (저작권자 기록) =====
  function injectMeta(){
    const metas = [
      {name:'author', content:'Rich-On by Roa'},
      {name:'copyright', content:'© 2026 Rich-On. All Rights Reserved.'},
      {name:'robots', content:'noimageindex'},
      {name:'rich-on-shield', content:'v1.0-protected'},
      {name:'rich-on-id', content:'RICHON-' + Date.now().toString(36).toUpperCase()},
      {property:'og:author', content:'Rich-On'}
    ];
    metas.forEach(m=>{
      if(document.querySelector(`meta[name="${m.name}"]`)) return;
      const tag = document.createElement('meta');
      Object.entries(m).forEach(([k,v])=>tag.setAttribute(k,v));
      document.head.appendChild(tag);
    });
  }
  
  // ===== 2. 예외 처리 헬퍼 (data-shield-allow="true" 체크) =====
  function isAllowed(el){
    if(!el) return false;
    while(el && el !== document.body){
      if(el.dataset && el.dataset.shieldAllow === 'true') return true;
      // 입력 필드는 자동 허용
      const tag = el.tagName;
      if(tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return true;
      el = el.parentElement;
    }
    return false;
  }
  
  // ===== 3. 우클릭 차단 (조용히) =====
  document.addEventListener('contextmenu', function(e){
    if(isAllowed(e.target)) return;
    e.preventDefault();
    return false;
  }, false);
  
  // ===== 4. 드래그 차단 =====
  document.addEventListener('dragstart', function(e){
    if(isAllowed(e.target)) return;
    e.preventDefault();
    return false;
  }, false);
  
  document.addEventListener('selectstart', function(e){
    if(isAllowed(e.target)) return;
    e.preventDefault();
    return false;
  }, false);
  
  // ===== 5. 키보드 단축키 차단 =====
  document.addEventListener('keydown', function(e){
    const k = e.key;
    const key = k ? k.toLowerCase() : '';
    
    // 입력 필드에서는 정상 작동
    if(isAllowed(e.target)) return;
    
    // F12 → 개발자 도구
    if(key === 'f12'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+S → 페이지 저장
    if(e.ctrlKey && key === 's'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+U → 소스 보기
    if(e.ctrlKey && key === 'u'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+Shift+I → 개발자 도구
    if(e.ctrlKey && e.shiftKey && key === 'i'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+Shift+C → 요소 검사
    if(e.ctrlKey && e.shiftKey && key === 'c'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+Shift+J → 콘솔
    if(e.ctrlKey && e.shiftKey && key === 'j'){
      e.preventDefault(); return false;
    }
    
    // Ctrl+P → 인쇄
    if(e.ctrlKey && key === 'p'){
      e.preventDefault(); return false;
    }
    
    // Mac: Cmd+Option+I, Cmd+Option+C, Cmd+Option+J
    if(e.metaKey && e.altKey){
      if(key === 'i' || key === 'c' || key === 'j'){
        e.preventDefault(); return false;
      }
    }
    
    // Mac: Cmd+S, Cmd+U, Cmd+P
    if(e.metaKey){
      if(key === 's' || key === 'u' || key === 'p'){
        e.preventDefault(); return false;
      }
    }
  }, false);
  
  // ===== 6. CSS로 텍스트 선택·드래그 강화 차단 =====
  function injectCSS(){
    const style = document.createElement('style');
    style.id = 'richon-shield-style';
    style.textContent = `
      *:not([data-shield-allow="true"]):not([data-shield-allow="true"] *) {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -webkit-user-drag: none;
        -webkit-touch-callout: none;
      }
      input, textarea, select,
      [data-shield-allow="true"],
      [data-shield-allow="true"] *,
      [contenteditable="true"]{
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
      }
      img {
        -webkit-user-drag: none !important;
        -khtml-user-drag: none !important;
        -moz-user-drag: none !important;
        -o-user-drag: none !important;
        user-drag: none !important;
        pointer-events: auto;
      }
      @media print {
        body { display: none !important; }
        body::before {
          content: "© 2026 Rich-On — 인쇄 권한이 없습니다.";
          display: block !important;
          font-size: 24px;
          padding: 100px;
        }
      }
    `;
    document.head.appendChild(style);
  }
  
  // ===== 7. 이미지 보호 강화 =====
  function protectImages(){
    const imgs = document.querySelectorAll('img');
    imgs.forEach(img=>{
      if(isAllowed(img)) return;
      img.setAttribute('draggable','false');
      img.setAttribute('oncontextmenu','return false;');
      img.style.webkitUserDrag = 'none';
      img.style.userSelect = 'none';
    });
  }
  
  // ===== 8. 개발자 도구 감지 (조용히 작동) =====
  function detectDevTools(){
    const threshold = 160;
    let warned = false;
    setInterval(()=>{
      const wDiff = window.outerWidth - window.innerWidth;
      const hDiff = window.outerHeight - window.innerHeight;
      if(wDiff > threshold || hDiff > threshold){
        if(!warned){
          warned = true;
          console.clear();
          console.log('%c⚠️ 리치온(Rich-On) 콘텐츠 보호', 'color:#B8843C;font-size:20px;font-weight:bold');
          console.log('%c© 2026 Rich-On by Roa. 무단 복제·도용 시 법적 책임을 물을 수 있습니다.', 'color:#C26060;font-size:14px');
        }
      } else {
        warned = false;
      }
    }, 1500);
  }
  
  // ===== 9. Console 경고 메시지 =====
  function consoleWarning(){
    setTimeout(()=>{
      console.clear();
      const css1 = 'color:#B8843C;font-size:24px;font-weight:bold;font-family:serif';
      const css2 = 'color:#1E2D4A;font-size:14px';
      const css3 = 'color:#C26060;font-size:13px;font-weight:bold';
      console.log('%c🌹 Rich-On', css1);
      console.log('%cCurated content by Roa', css2);
      console.log('%c© 2026 Rich-On. 무단 복제·도용 금지 (저작권법 제136조)', css3);
    }, 100);
  }
  
  // ===== 10. 실행 (DOM 준비되면) =====
  function run(){
    injectMeta();
    injectCSS();
    protectImages();
    detectDevTools();
    consoleWarning();
    
    // 동적으로 추가되는 이미지도 보호
    const observer = new MutationObserver(()=>{
      protectImages();
    });
    observer.observe(document.body, {childList:true, subtree:true});
  }
  
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
  
})();
