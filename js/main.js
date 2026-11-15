/* 5S — فايف إس | Design v3 — vanilla JS */
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
      if (e.target === menu || e.target.closest('a')) setOpen(false);
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
    if (!reduce) {
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

  /* Before / after slider */
  document.querySelectorAll('.ba').forEach(function (ba) {
    var input = ba.querySelector('input[type="range"]');
    var set = function (v) { ba.style.setProperty('--pos', v + '%'); };
    if (input) { input.addEventListener('input', function () { set(input.value); }); set(input.value); }
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

  /* Materials calculator — coefficients are set by the technical team.
     Until a rate (litres of product per m²) is provided, the result stays "[—]". */
  var RATES = { road: null, berm: null, slope: null, dust: null, walk: null };
  var IBC_LITRES = 1000;
  var calc = document.getElementById('calc-form');
  if (calc) {
    var type = calc.querySelector('#calc-type');
    var area = calc.querySelector('#calc-area');
    var out = calc.querySelector('#calc-out');
    var update = function () {
      var r = RATES[type.value];
      var a = parseFloat(area.value);
      if (r && a > 0) {
        out.textContent = Math.max(1, Math.ceil((a * r) / IBC_LITRES)) + ' حاوية IBC';
      } else {
        out.textContent = '[—] حاوية IBC';
      }
    };
    type.addEventListener('change', update); area.addEventListener('input', update); update();
    calc.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('lead-msg');
      var hidden = document.getElementById('lead-details');
      var a = area.value ? area.value + ' م²' : 'غير محددة';
      if (hidden) hidden.value = 'حاسبة المواد — نوع التطبيق: ' + type.options[type.selectedIndex].text + ' | المساحة: ' + a;
      var target = document.getElementById('contact');
      if (target) target.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
      var first = document.getElementById('lead-name');
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, reduce ? 0 : 600);
      if (msg) msg.textContent = 'أضفنا تفاصيل الحاسبة لطلبك، أكمل بياناتك وسيرسل لك فريقنا عرضًا دقيقًا.';
    });
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
