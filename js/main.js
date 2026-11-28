/* 5S — فايف إس | Design v5 — vanilla JS */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile menu */
  var menu = document.getElementById('mobile-menu');
  var openBtn = document.querySelector('.menu-toggle');
  if (menu && openBtn) {
    var closeBtn = menu.querySelector('.menu-close');
    var setOpen = function (open) {
      menu.classList.toggle('open', open);
      menu.setAttribute('aria-hidden', String(!open));
      openBtn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
      if (open && closeBtn) closeBtn.focus();
    };
    openBtn.addEventListener('click', function () { setOpen(true); });
    if (closeBtn) closeBtn.addEventListener('click', function () { setOpen(false); openBtn.focus(); });
    menu.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (e.target === menu || (a && a.hasAttribute('href') && a.getAttribute('aria-disabled') !== 'true')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) { setOpen(false); openBtn.focus(); }
    });
  }

  /* Desktop dropdowns: keyboard / touch toggle */
  document.querySelectorAll('.has-dd > .nav-link').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = !li.classList.contains('open');
      document.querySelectorAll('.has-dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
      li.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-dd')) document.querySelectorAll('.has-dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
  });

  /* Hero video: autoplay muted (unless reduced motion), play/pause button */
  document.querySelectorAll('.video-card').forEach(function (card) {
    var v = card.querySelector('video');
    var b = card.querySelector('.play-btn');
    if (!v || !b) return;
    var sync = function () {
      var playing = !v.paused;
      card.classList.toggle('playing', playing);
      b.setAttribute('aria-label', playing ? 'إيقاف الفيديو' : 'تشغيل الفيديو');
      b.innerHTML = playing
        ? '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
        : '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>';
    };
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    b.addEventListener('click', function () { if (v.paused) { v.play(); } else { v.pause(); } });
    if (!reduce && !card.closest('[data-slider]')) {
      var p = v.play();
      if (p && p.catch) p.catch(function () { sync(); });
    }
    sync();
  });

  /* Tabs (solutions on home) */
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowLeft') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowRight') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === 'Home') n = tabs[0];
        if (k === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
  });

  /* Sliders: home hero (autoplay) and project galleries (manual).
     RTL: the "next" arrow is on the left; ArrowLeft = next, ArrowRight = previous. */
  document.querySelectorAll('[data-slider]').forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('.slide'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('.sl-dot'));
    var prev = root.querySelector('.sl-prev');
    var next = root.querySelector('.sl-next');
    var pauseBtn = root.querySelector('.sl-pause');
    var live = root.querySelector('.slides');
    var delay = parseInt(root.getAttribute('data-autoplay') || '0', 10);
    var idx = 0, timer = null, userPaused = reduce, hover = false, focusIn = false;
    var count = slides.length;
    if (!count) return;

    var videoOf = function (s) { return s.querySelector('video'); };
    var show = function (n) {
      idx = (n + count) % count;
      slides.forEach(function (s, i) {
        var on = i === idx;
        s.classList.toggle('is-active', on);
        s.setAttribute('aria-hidden', String(!on));
        if ('inert' in s) s.inert = !on;
        var v = videoOf(s);
        if (v) {
          if (on) { if (!reduce && !userPaused && delay) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
          else { v.pause(); }
        }
      });
      dots.forEach(function (d, i) {
        d.classList.toggle('is-active', i === idx);
        if (i === idx) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
      });
    };
    var stop = function () { if (timer) { clearTimeout(timer); timer = null; } };
    var schedule = function () {
      stop();
      if (!delay || userPaused || hover || focusIn || document.hidden || count < 2) return;
      timer = setTimeout(function () { show(idx + 1); schedule(); }, delay);
    };
    var setLive = function () { if (live) live.setAttribute('aria-live', (delay && !userPaused && !hover && !focusIn) ? 'off' : 'polite'); };
    var syncPause = function () {
      if (!pauseBtn) return;
      pauseBtn.classList.toggle('is-paused', userPaused);
      pauseBtn.setAttribute('aria-label', userPaused ? 'تشغيل الشرائح تلقائيًا' : 'إيقاف التشغيل التلقائي للشرائح');
    };
    var go = function (n) { show(n); schedule(); };

    if (prev) prev.addEventListener('click', function () { go(idx - 1); });
    if (next) next.addEventListener('click', function () { go(idx + 1); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
    if (pauseBtn) pauseBtn.addEventListener('click', function () {
      userPaused = !userPaused; syncPause(); setLive();
      var v = videoOf(slides[idx]);
      if (v && userPaused) v.pause();
      schedule();
    });
    root.addEventListener('mouseenter', function () { hover = true; setLive(); stop(); });
    root.addEventListener('mouseleave', function () { hover = false; setLive(); schedule(); });
    root.addEventListener('focusin', function (e) {
      /* pause only for keyboard focus, not after a mouse/touch click */
      focusIn = !!(e.target.matches && e.target.matches(':focus-visible'));
      setLive(); if (focusIn) stop();
    });
    root.addEventListener('focusout', function () { focusIn = false; setLive(); schedule(); });
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx + 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(idx - 1); }
    });
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 48) go(dx < 0 ? idx + 1 : idx - 1);
    }, { passive: true });
    document.addEventListener('visibilitychange', schedule);

    syncPause(); setLive(); show(0); schedule();
  });

  /* Counters */
  var counters = document.querySelectorAll('[data-count]');
  var runCounter = function (el) {
    var end = parseFloat(el.getAttribute('data-count'));
    if (reduce || isNaN(end)) { el.textContent = el.getAttribute('data-count'); return; }
    var t0 = null, dur = 1400;
    var step = function (ts) {
      if (!t0) t0 = ts;
      var k = Math.min(1, (ts - t0) / dur);
      var eased = 1 - Math.pow(1 - k, 3);
      el.textContent = Math.round(end * eased);
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  /* Reveal on scroll + counters */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        if (el.hasAttribute('data-count')) runCounter(el); else el.classList.add('in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
    counters.forEach(function (el) { el.textContent = '0'; io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
  }

  /* Basic form validation message */
  document.querySelectorAll('form[data-validate]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!f.checkValidity()) { e.preventDefault(); f.reportValidity(); }
    });
  });

  /* Footer year */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear() > 2026 ? new Date().getFullYear() : 2026; });
})();
