'use strict';

/**
 * Pikestia Learning Hub — Enhancements
 * Drop into static/js/ and add a <script src="/static/js/enhancements.js" defer></script>
 * in base.html before the closing </body>.
 *
 * Rules followed throughout:
 *  - No client-side validation as a security gate (server handles auth/input)
 *  - No sensitive class names in HTML
 *  - Modern JS (ES6+), no external dependencies
 *  - All DOM mutations are additive; nothing removes existing functionality
 */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Reading progress bar ─────────────────────────────── */
  (function setupReadingProgress() {
    if (!document.querySelector('.reading-content')) return;

    const bar = document.createElement('div');
    bar.className = 'reading-progress-bar';
    bar.setAttribute('role', 'presentation');
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);

    function updateBar() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0;
      bar.style.width = pct + '%';
    }

    updateBar();
    window.addEventListener('scroll', updateBar, { passive: true });
  })();


  /* ── Scroll-to-top button ─────────────────────────────── */
  (function setupScrollTop() {
    const btn = document.createElement('button');
    btn.className = 'scroll-top-btn';
    btn.setAttribute('aria-label', 'Scroll back to top');
    btn.setAttribute('title', 'Back to top');
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
    document.body.appendChild(btn);

    function toggleBtn() {
      const visible = window.scrollY > 400;
      btn.classList.toggle('is-visible', visible);
    }

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    toggleBtn();
    window.addEventListener('scroll', toggleBtn, { passive: true });
  })();


  /* ── Reading time estimator ───────────────────────────── */
  (function setupReadingTime() {
    const content = document.querySelector('.reading-content');
    const header = document.querySelector('.reading-header');
    if (!content || !header) return;

    const words = (content.textContent || '').trim().split(/\s+/).filter(Boolean).length;
    const minutes = Math.max(1, Math.round(words / 220));
    const label = minutes === 1 ? '1 min read' : minutes + ' min read';

    const strip = document.createElement('div');
    strip.className = 'reading-time-strip';
    strip.setAttribute('aria-label', 'Estimated reading time: ' + label);
    strip.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
        '<circle cx="12" cy="12" r="9"/>' +
        '<path d="M12 7v5l3 2"/>' +
      '</svg>' +
      '<span>' + label + '</span>';

    header.appendChild(strip);
  })();


  /* ── Keyboard shortcut: "/" focuses search ────────────── */
  (function setupSearchShortcut() {
    document.addEventListener('keydown', function (event) {
      const tag = document.activeElement ? document.activeElement.tagName.toLowerCase() : '';
      const isEditable = tag === 'input' || tag === 'textarea' || tag === 'select'
        || document.activeElement.isContentEditable;

      if (event.key === '/' && !isEditable && !event.ctrlKey && !event.metaKey) {
        const search = document.querySelector('.search-form input[type="search"]');
        if (search) {
          event.preventDefault();
          search.focus();
          search.select();
        }
      }

      if (event.key === 'Escape') {
        const active = document.activeElement;
        if (active && active.tagName.toLowerCase() === 'input' && active.type === 'search') {
          active.blur();
        }
      }
    });

    /* Add keyboard hint to search input */
    const searchInputs = document.querySelectorAll('.search-form input[type="search"]');
    searchInputs.forEach(function (input) {
      const wrapper = input.parentElement;
      if (!wrapper) return;
      if (wrapper.style.position === '' || wrapper.style.position === 'static') {
        wrapper.style.position = 'relative';
      }

      const hint = document.createElement('span');
      hint.className = 'search-shortcut-hint';
      hint.setAttribute('aria-hidden', 'true');
      hint.innerHTML = '<kbd>/</kbd>';

      input.addEventListener('focus', function () { hint.style.display = 'none'; });
      input.addEventListener('blur', function () {
        if (!input.value) hint.style.display = '';
      });

      if (input.value) hint.style.display = 'none';
      wrapper.appendChild(hint);
    });
  })();


  /* ── Code block: copy button ──────────────────────────── */
  (function setupCodeCopy() {
    if (!navigator.clipboard) return;

    document.querySelectorAll('.reading-content pre').forEach(function (pre) {
      pre.style.position = 'relative';
      const code = pre.querySelector('code');
      if (!code) return;

      const btn = document.createElement('button');
      btn.className = 'code-copy-btn';
      btn.textContent = 'Copy';
      btn.setAttribute('aria-label', 'Copy code to clipboard');

      btn.addEventListener('click', function () {
        navigator.clipboard.writeText(code.textContent || '').then(function () {
          btn.textContent = 'Copied';
          btn.classList.add('is-copied');
          window.setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('is-copied');
          }, 2000);
        }).catch(function () {
          btn.textContent = 'Failed';
          window.setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
        });
      });

      pre.appendChild(btn);
    });
  })();


  /* ── Heading anchor links (in reading content) ────────── */
  (function setupHeadingAnchors() {
    const content = document.querySelector('.reading-content');
    if (!content) return;

    const headings = content.querySelectorAll('h2, h3');
    headings.forEach(function (heading) {
      if (!heading.id) {
        const slug = heading.textContent.trim()
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '');
        heading.id = slug;
      }

      const anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = '#' + heading.id;
      anchor.setAttribute('aria-label', 'Link to section: ' + heading.textContent.trim());
      anchor.innerHTML =
        '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
          '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>' +
          '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>' +
        '</svg>';

      heading.appendChild(anchor);
    });
  })();


  /* ── Sidebar section progress tracker ────────────────────
     Requires a .reading-sidebar element (added by enhanced template).
     Highlights the sidebar nav item matching the visible heading. */
  (function setupSectionProgress() {
    const sidebar = document.querySelector('.reading-sidebar');
    const content = document.querySelector('.reading-content');
    if (!sidebar || !content) return;

    const headings = Array.from(content.querySelectorAll('h2[id], h3[id]'));
    if (!headings.length) return;

    const navList = document.createElement('ul');
    headings.forEach(function (h) {
      const li = document.createElement('li');
      li.dataset.target = h.id;

      const dot = document.createElement('span');
      dot.className = 'reading-progress-dot';
      dot.setAttribute('aria-hidden', 'true');
      li.appendChild(dot);
      li.appendChild(document.createTextNode(h.textContent.replace(/#$/, '').trim()));
      navList.appendChild(li);
    });

    const sidebarHeading = document.createElement('h3');
    sidebarHeading.textContent = 'In this material';
    sidebar.appendChild(sidebarHeading);
    sidebar.appendChild(navList);

    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navList.querySelectorAll('li').forEach(function (li) {
          li.classList.remove('is-active');
        });
        const active = navList.querySelector('[data-target="' + entry.target.id + '"]');
        if (active) active.classList.add('is-active');
      });
    }, {
      rootMargin: '-20% 0px -70% 0px',
      threshold: 0
    });

    headings.forEach(function (h) { observer.observe(h); });
  })();


  /* ── Deadline urgency colorizer ──────────────────────────
     Adds deadline-urgent / deadline-soon class to deadline spans
     based purely on visual emphasis; real enforcement is server-side. */
  (function setupDeadlineUrgency() {
    const now = Date.now();
    const ONE_WEEK = 7 * 24 * 60 * 60 * 1000;
    const TWO_WEEKS = 14 * 24 * 60 * 60 * 1000;

    document.querySelectorAll('[data-deadline]').forEach(function (el) {
      const deadlineTs = parseInt(el.dataset.deadline, 10);
      if (isNaN(deadlineTs)) return;
      const diff = deadlineTs - now;

      if (diff > 0 && diff < ONE_WEEK) {
        el.classList.add('deadline-urgent');
      } else if (diff >= ONE_WEEK && diff < TWO_WEEKS) {
        el.classList.add('deadline-soon');
      }
    });
  })();


  /* ── Print: auto-expand details elements ─────────────── */
  (function setupPrintExpand() {
    window.addEventListener('beforeprint', function () {
      document.querySelectorAll('details').forEach(function (d) {
        d.setAttribute('open', '');
        d.dataset.wasOpen = d.open ? '1' : '0';
      });
    });

    window.addEventListener('afterprint', function () {
      document.querySelectorAll('details[data-was-open]').forEach(function (d) {
        if (d.dataset.wasOpen !== '1') d.removeAttribute('open');
        delete d.dataset.wasOpen;
      });
    });
  })();


  /* ── Alert: auto-remove after delay (success/info) ──────
     Duplicates the logic in app.js but now also handles any alert
     injected dynamically after page load. */
  (function setupAlertAutoRemove() {
    function wireAlert(alert) {
      if (alert.dataset.wired) return;
      alert.dataset.wired = '1';

      const dismiss = alert.querySelector('.alert-dismiss');
      if (dismiss) {
        dismiss.addEventListener('click', function () { alert.remove(); });
      }

      if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
        window.setTimeout(function () { alert.remove(); }, 5000);
      }
    }

    document.querySelectorAll('.alert').forEach(wireAlert);

    /* Watch for dynamically added alerts */
    if ('MutationObserver' in window) {
      const stack = document.querySelector('.message-stack');
      if (stack) {
        new MutationObserver(function (mutations) {
          mutations.forEach(function (m) {
            m.addedNodes.forEach(function (node) {
              if (node.nodeType === 1 && node.classList.contains('alert')) {
                wireAlert(node);
              }
            });
          });
        }).observe(stack, { childList: true });
      }
    }
  })();


  /* ── Smooth scroll for in-page anchor links ─────────────
     Overrides default jump for heading anchors and any #hash link
     inside the reading content only. */
  (function setupSmoothAnchor() {
    document.querySelectorAll('.reading-content a[href^="#"], .heading-anchor').forEach(function (link) {
      link.addEventListener('click', function (event) {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;
        const target = document.querySelector(href);
        if (!target) return;
        event.preventDefault();
        const offset = 68 + 24; /* header height + gap */
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: top, behavior: 'smooth' });
        /* Update URL without triggering another scroll */
        history.pushState(null, '', href);
      });
    });
  })();


  /* ── Explore page: filter by discipline ─────────────────
     Client-side filter for the explore grid cards.
     Real data filtering is always server-side; this is purely cosmetic. */
  (function setupExploreFilter() {
    const grid = document.querySelector('.explore-grid');
    const pills = document.querySelectorAll('[data-discipline-filter]');
    if (!grid || !pills.length) return;

    pills.forEach(function (pill) {
      pill.addEventListener('click', function (event) {
        event.preventDefault();
        const target = pill.dataset.disciplineFilter;

        pills.forEach(function (p) { p.classList.remove('is-active'); });
        pill.classList.add('is-active');

        grid.querySelectorAll('.explore-card').forEach(function (card) {
          const discipline = card.dataset.discipline || '';
          const show = !target || discipline === target;
          card.style.display = show ? '' : 'none';
        });
      });
    });
  })();


  /* ── Bookmark button: optimistic visual toggle ──────────
     The real bookmark state is always set by the server POST.
     This only provides instant visual feedback. */
  (function setupBookmarkToggle() {
    document.querySelectorAll('[data-bookmark-toggle]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        btn.classList.toggle('btn-bookmarked');
        const isBookmarked = btn.classList.contains('btn-bookmarked');
        btn.textContent = isBookmarked ? 'Bookmarked' : 'Bookmark';
        btn.setAttribute('aria-pressed', isBookmarked ? 'true' : 'false');
      });
    });
  })();

});
