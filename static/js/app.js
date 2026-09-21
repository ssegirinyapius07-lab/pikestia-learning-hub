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

  // Responsive header menu and grouped dropdowns.
  const toggle = document.getElementById('mobileToggle');
  const menu = document.getElementById('mainMenu');
  const dropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));
  const mobileBreakpoint = window.matchMedia('(max-width: 800px)');

  function setDropdownState(dropdown, isOpen) {
    const dropdownToggle = dropdown.querySelector('.nav-dropdown-toggle');
    if (!dropdownToggle) return;

    dropdown.classList.toggle('is-open', isOpen);
    dropdownToggle.setAttribute('aria-expanded', String(isOpen));
  }

  function closeDropdowns(except) {
    dropdowns.forEach(function (dropdown) {
      if (dropdown !== except) {
        setDropdownState(dropdown, false);
      }
    });
  }

  function closeMenu() {
    if (!toggle || !menu) return;
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
    closeDropdowns(null);
  }

  function syncDropdownMode() {
    if (!mobileBreakpoint.matches) {
      closeDropdowns(null);
    }
  }

  dropdowns.forEach(function (dropdown) {
    const dropdownToggle = dropdown.querySelector('.nav-dropdown-toggle');
    if (!dropdownToggle) return;

    dropdownToggle.addEventListener('click', function () {
      if (!mobileBreakpoint.matches) return;

      const isOpen = !dropdown.classList.contains('is-open');
      closeDropdowns(dropdown);
      setDropdownState(dropdown, isOpen);
    });

    dropdown.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        closeDropdowns(null);
        if (mobileBreakpoint.matches && menu) {
          menu.classList.remove('open');
          if (toggle) {
            toggle.setAttribute('aria-expanded', 'false');
            toggle.textContent = 'Menu';
          }
        }
      });
    });
  });

  mobileBreakpoint.addEventListener('change', syncDropdownMode);

  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      const isOpen = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      toggle.textContent = isOpen ? 'Close' : 'Menu';

      if (!isOpen) {
        closeDropdowns(null);
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
