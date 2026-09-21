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

  function closeMenu() {
    if (!toggle || !menu) return;
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
  }

  if (toggle && menu) {
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

  // Professional toast notifications: dismissible immediately and auto-close
  // successful/info notices after a short reading period.
  document.querySelectorAll('.alert').forEach(function (alert) {
    const dismiss = alert.querySelector('.alert-dismiss');

    if (dismiss) {
      dismiss.addEventListener('click', function () {
        alert.remove();
      });
    }

    if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
      window.setTimeout(function () {
        alert.remove();
      }, 5000);
    }
  });
});
