(function(){
  function applyTheme(stored){
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    let theme = stored;
    if(stored === 'system' || !stored) theme = prefersDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
  }
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', ()=>{
    const stored = document.documentElement.dataset.stored || 'system';
    if(stored === 'system') applyTheme('system');
  });
})();
