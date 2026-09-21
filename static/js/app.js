document.addEventListener('DOMContentLoaded', ()=>{
  // debounce search
  const searchInputs = document.querySelectorAll('input[type=search][name=q]');
  searchInputs.forEach(inp=>{
    let t;
    inp.addEventListener('input', ()=>{
      clearTimeout(t);
      t = setTimeout(()=>{ /* future: live search */ }, 400);
    });
  });
});
