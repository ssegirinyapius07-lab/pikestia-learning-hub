(function () {
  function resolveTheme(mode) {
    if (mode === 'dark') return 'dark';
    if (mode === 'light') return 'light';

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function applyTheme(mode) {
    document.documentElement.setAttribute('data-theme', resolveTheme(mode));
    document.documentElement.dataset.stored = mode;
  }

  function updateActiveButton(mode) {
    document.querySelectorAll('.theme-option').forEach(function (button) {
      const form = button.closest('form');
      const input = form && form.querySelector('input[name="display_mode"]');
      const active = input && input.value === mode;

      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  }

  function getCsrfToken() {
    const tokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return tokenInput ? tokenInput.value : '';
  }

  function persistTheme(form) {
    const action = form.getAttribute('action');
    const data = new FormData(form);

    return fetch(action, {
      method: 'POST',
      body: data,
      credentials: 'same-origin',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken()
      }
    });
  }

  function setupSwitcher() {
    document.querySelectorAll('.theme-switcher form').forEach(function (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault();

        const input = form.querySelector('input[name="display_mode"]');
        if (!input) return;

        const nextMode = input.value;
        const previousMode = document.documentElement.dataset.stored || 'system';

        applyTheme(nextMode);
        updateActiveButton(nextMode);

        if (nextMode !== 'system') {
          document.cookie = 'display_mode=' + encodeURIComponent(nextMode)
            + '; Max-Age=31536000; Path=/; SameSite=Lax';
        }

        persistTheme(form).catch(function () {
          applyTheme(previousMode);
          updateActiveButton(previousMode);
        });
      });
    });
  }

  applyTheme(document.documentElement.dataset.stored || 'system');
  updateActiveButton(document.documentElement.dataset.stored || 'system');
  setupSwitcher();

  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQuery.addEventListener('change', function () {
    const stored = document.documentElement.dataset.stored || 'system';

    if (stored === 'system') {
      applyTheme('system');
    }
  });
})();
