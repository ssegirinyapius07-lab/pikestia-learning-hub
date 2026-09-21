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

  // Mobile header menu.
  const toggle = document.getElementById('mobileToggle');
  const menu = document.getElementById('mainMenu');
  const mobileResourceMenu = document.querySelector('.mobile-resource-menu');
  const mobileResourceToggle = mobileResourceMenu
    ? mobileResourceMenu.querySelector('.nav-dropdown-toggle')
    : null;

  function closeMobileResourceMenu() {
    if (!mobileResourceMenu || !mobileResourceToggle) return;
    mobileResourceMenu.classList.remove('is-open');
    mobileResourceToggle.setAttribute('aria-expanded', 'false');
  }

  function closeMenu() {
    if (!toggle || !menu) return;
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
    closeMobileResourceMenu();
  }

  if (mobileResourceMenu && mobileResourceToggle) {
    mobileResourceToggle.addEventListener('click', function () {
      const isOpen = !mobileResourceMenu.classList.contains('is-open');
      mobileResourceMenu.classList.toggle('is-open', isOpen);
      mobileResourceToggle.setAttribute('aria-expanded', String(isOpen));
    });

    mobileResourceMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });
  }

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      const isOpen = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.textContent = isOpen ? 'Close' : 'Menu';

      if (!isOpen) {
        closeMobileResourceMenu();
      }
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
