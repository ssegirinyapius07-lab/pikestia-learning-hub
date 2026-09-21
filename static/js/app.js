document.addEventListener('DOMContentLoaded', function () {
  // Debounce search.
  const searchInputs = document.querySelectorAll('input[type="search"][name="q"]');

  searchInputs.forEach(function (input) {
    let timeout;

    input.addEventListener('input', function () {
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        // Reserved for future live-search behavior.
      }, 400);
    });
  });

  // Responsive header menu.
  const toggle = document.getElementById('mobileToggle');
  const menu = document.getElementById('mainMenu');
  const resourceMenu = document.querySelector('.resource-menu');
  const resourceToggle = resourceMenu
    ? resourceMenu.querySelector('.nav-dropdown-toggle')
    : null;
  const mobileBreakpoint = window.matchMedia('(max-width: 800px)');

  function closeResourceMenu() {
    if (!resourceMenu || !resourceToggle) return;
    resourceMenu.classList.remove('is-open');
    resourceToggle.setAttribute('aria-expanded', 'false');
  }

  function syncResourceMenuMode() {
    if (!mobileBreakpoint.matches) {
      closeResourceMenu();
    }
  }

  if (resourceMenu && resourceToggle) {
    resourceToggle.addEventListener('click', function () {
      if (!mobileBreakpoint.matches) return;

      const isOpen = resourceMenu.classList.toggle('is-open');
      resourceToggle.setAttribute('aria-expanded', String(isOpen));
    });

    resourceMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeResourceMenu);
    });

    mobileBreakpoint.addEventListener('change', syncResourceMenuMode);
  }

  if (toggle && menu) {
    function closeMenu() {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Menu';
      closeResourceMenu();
    }

    toggle.addEventListener('click', function () {
      const isOpen = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.textContent = isOpen ? 'Close' : 'Menu';
    });

    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closeMenu();
      }
    });

    document.addEventListener('click', function (event) {
      if (!menu.contains(event.target) && !toggle.contains(event.target)) {
        closeMenu();
      }
    });
  }
});
