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

  // Subtle scroll reveal and header elevation.
  // CSS remains responsible for the visual effect; this only detects visibility.
  document.documentElement.classList.add('js-reveal');

  const revealItems = document.querySelectorAll(
    '[data-reveal], .editorial-section, .newsroom-card, .news-reading-header, .news-related-card'
  );

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReducedMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.setAttribute('data-reveal', entry.target.getAttribute('data-reveal') || 'soft');
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    revealItems.forEach(function (item) {
      if (!item.hasAttribute('data-reveal')) {
        item.setAttribute('data-reveal', 'soft');
      }
      revealObserver.observe(item);
    });
  } else {
    revealItems.forEach(function (item) {
      item.setAttribute('data-reveal', 'soft');
      item.classList.add('is-visible');
    });
  }

  const header = document.querySelector('.header');

  function updateHeaderOnScroll() {
    if (!header) return;
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  }

  updateHeaderOnScroll();
  window.addEventListener('scroll', updateHeaderOnScroll, { passive: true });

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
