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

  // Desktop navigation dropdowns.
  // Each menu remains compact, anchored to its trigger, and closes with
  // a delay so slow pointer movement into the panel does not collapse it.
  const desktopNav = document.getElementById('desktopNav');

  if (desktopNav) {
    const dropdowns = Array.from(desktopNav.querySelectorAll('.nav-dropdown'));
    let closeTimer = null;

    function clearCloseTimer() {
      window.clearTimeout(closeTimer);
    }

    function closeDropdown(dropdown) {
      dropdown.classList.remove('is-open');
      const button = dropdown.querySelector('.nav-dropdown-toggle');
      if (button) button.setAttribute('aria-expanded', 'false');
    }

    function closeAll(except) {
      dropdowns.forEach(function (dropdown) {
        if (dropdown !== except) closeDropdown(dropdown);
      });
    }

    function scheduleClose(dropdown) {
      clearCloseTimer();
      closeTimer = window.setTimeout(function () {
        if (!dropdown.matches(':hover') && !dropdown.contains(document.activeElement)) {
          closeDropdown(dropdown);
        }
      }, 550);
    }

    dropdowns.forEach(function (dropdown) {
      const button = dropdown.querySelector('.nav-dropdown-toggle');
      const panel = dropdown.querySelector('.nav-dropdown-panel');

      dropdown.addEventListener('mouseenter', function () {
        if (!window.matchMedia('(min-width: 801px)').matches) return;
        clearCloseTimer();
        closeAll(dropdown);
        dropdown.classList.add('is-open');
        if (button) button.setAttribute('aria-expanded', 'true');
      });

      dropdown.addEventListener('mouseleave', function () {
        if (!window.matchMedia('(min-width: 801px)').matches) return;
        scheduleClose(dropdown);
      });

      if (panel) {
        panel.addEventListener('mouseenter', clearCloseTimer);
        panel.addEventListener('mouseleave', function () {
          if (!window.matchMedia('(min-width: 801px)').matches) return;
          scheduleClose(dropdown);
        });
      }

      if (button) {
        button.addEventListener('click', function () {
          if (!window.matchMedia('(min-width: 801px)').matches) return;

          clearCloseTimer();

          if (dropdown.classList.contains('is-open')) {
            scheduleClose(dropdown);
          } else {
            closeAll(dropdown);
            dropdown.classList.add('is-open');
            button.setAttribute('aria-expanded', 'true');
          }
        });
      }

      dropdown.addEventListener('focusin', function () {
        if (!window.matchMedia('(min-width: 801px)').matches) return;
        clearCloseTimer();
        closeAll(dropdown);
        dropdown.classList.add('is-open');
        if (button) button.setAttribute('aria-expanded', 'true');
      });
    });

    document.addEventListener('click', function (event) {
      if (!desktopNav.contains(event.target)) {
        clearCloseTimer();
        dropdowns.forEach(closeDropdown);
      }
    });

    window.addEventListener('resize', function () {
      if (!window.matchMedia('(min-width: 801px)').matches) {
        clearCloseTimer();
        dropdowns.forEach(closeDropdown);
      }
    });
  }

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
