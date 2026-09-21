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

  // Desktop navigation uses one continuous mega surface.
  // Moving between top-level items changes the contents in place instead
  // of closing one dropdown and opening another.
  const desktopNav = document.getElementById('desktopNav');
  const desktopNavShell = document.getElementById('desktopNavShell');
  const megaPanel = document.getElementById('desktopMegaPanel');
  const megaPanelInner = document.getElementById('desktopMegaPanelInner');

  if (desktopNav && desktopNavShell && megaPanel && megaPanelInner) {
    const dropdowns = Array.from(desktopNav.querySelectorAll('.nav-dropdown'));
    let activeDropdown = null;
    let closeTimer = null;

    function clearCloseTimer() {
      window.clearTimeout(closeTimer);
    }

    function closeMegaPanel() {
      clearCloseTimer();
      activeDropdown = null;
      dropdowns.forEach(function (item) {
        item.classList.remove('is-open');
        const button = item.querySelector('.nav-dropdown-toggle');
        if (button) button.setAttribute('aria-expanded', 'false');
      });
      megaPanel.classList.remove('is-open');
      megaPanel.setAttribute('aria-hidden', 'true');
    }

    function showMegaPanel(dropdown) {
      clearCloseTimer();
      activeDropdown = dropdown;

      dropdowns.forEach(function (item) {
        item.classList.toggle('is-open', item === dropdown);
        const button = item.querySelector('.nav-dropdown-toggle');
        if (button) button.setAttribute('aria-expanded', item === dropdown ? 'true' : 'false');
      });

      const sourcePanel = dropdown.querySelector('.nav-dropdown-panel');
      if (!sourcePanel) return;

      megaPanelInner.innerHTML = sourcePanel.innerHTML;
      megaPanel.classList.add('is-open');
      megaPanel.setAttribute('aria-hidden', 'false');
    }

    function scheduleClose() {
      clearCloseTimer();
      closeTimer = window.setTimeout(function () {
        if (!desktopNavShell.matches(':hover') && !megaPanel.matches(':hover')) {
          closeMegaPanel();
        }
      }, 500);
    }

    dropdowns.forEach(function (dropdown) {
      const button = dropdown.querySelector('.nav-dropdown-toggle');

      dropdown.addEventListener('mouseenter', function () {
        if (!window.matchMedia('(min-width: 801px)').matches) return;
        showMegaPanel(dropdown);
      });

      dropdown.addEventListener('focusin', function () {
        if (!window.matchMedia('(min-width: 801px)').matches) return;
        showMegaPanel(dropdown);
      });

      if (button) {
        button.addEventListener('click', function () {
          if (!window.matchMedia('(min-width: 801px)').matches) return;

          if (activeDropdown === dropdown && megaPanel.classList.contains('is-open')) {
            scheduleClose();
          } else {
            showMegaPanel(dropdown);
          }
        });
      }
    });

    desktopNavShell.addEventListener('mouseenter', clearCloseTimer);
    desktopNavShell.addEventListener('mouseleave', scheduleClose);
    megaPanel.addEventListener('mouseenter', clearCloseTimer);
    megaPanel.addEventListener('mouseleave', scheduleClose);

    document.addEventListener('click', function (event) {
      if (!desktopNavShell.contains(event.target) && !megaPanel.contains(event.target)) {
        closeMegaPanel();
      }
    });

    window.addEventListener('resize', function () {
      if (!window.matchMedia('(min-width: 801px)').matches) {
        closeMegaPanel();
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
