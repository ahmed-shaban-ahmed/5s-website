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

  /* Hash-linked tabs (media centre): #videos / #photos / #articles */
  document.querySelectorAll('[data-hash-tabs]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    var ids = tabs.map(function (t) { return t.getAttribute('aria-controls'); });
    var fromHash = function (scroll) {
      var h = (location.hash || '').replace('#', '');
      var i = ids.indexOf(h);
      if (i < 0) return;
      tabs[i].click();
      if (scroll) list.scrollIntoView({ block: 'start' });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () {
        if (history.replaceState) history.replaceState(null, '', '#' + ids[i]);
      });
    });
    window.addEventListener('hashchange', function () { fromHash(false); });
    fromHash(true);
  });

  /* Lightbox: photos + YouTube videos (native <dialog>). RTL: ArrowLeft = next. */
  var lb = document.getElementById('lightbox');
  if (lb && lb.showModal) {
    var stage = lb.querySelector('.lb-stage');
    var cap = lb.querySelector('.lb-cap');
    var group = [], cur = 0, opener = null;
    var render = function () {
      var a = group[cur];
      stage.innerHTML = '';
      if (a.hasAttribute('data-yt')) {
        var f = document.createElement('iframe');
        f.src = 'https://www.youtube-nocookie.com/embed/' + a.getAttribute('data-yt') + '?autoplay=1&rel=0';
        f.title = a.getAttribute('data-title') || 'فيديو';
        f.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen';
        f.setAttribute('allowfullscreen', '');
        stage.appendChild(f);
        cap.textContent = a.getAttribute('data-title') || '';
      } else {
        var im = document.createElement('img');
        im.src = a.getAttribute('href');
        im.alt = a.getAttribute('data-caption') || '';
        stage.appendChild(im);
        cap.textContent = a.getAttribute('data-caption') || '';
      }
      if (group.length < 2) lb.setAttribute('data-single', ''); else lb.removeAttribute('data-single');
    };
    var step = function (d) { cur = (cur + d + group.length) % group.length; render(); };
    document.querySelectorAll('[data-lightbox], [data-yt]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey) return;
        e.preventDefault();
        var g = a.getAttribute('data-group');
        group = Array.prototype.slice.call(document.querySelectorAll('[data-group="' + g + '"]'));
        cur = group.indexOf(a); opener = a;
        render(); lb.showModal();
      });
    });
    lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lb-prev').addEventListener('click', function () { step(-1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { step(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); step(1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); step(-1); }
    });
    lb.addEventListener('close', function () { stage.innerHTML = ''; if (opener) opener.focus(); });
  }

  /* Technical data: category filter + gated PDF download */
  var pdfGrid = document.getElementById('pdf-grid');
  if (pdfGrid) {
    var chips = Array.prototype.slice.call(document.querySelectorAll('.filter-chip'));
    var cards = Array.prototype.slice.call(pdfGrid.querySelectorAll('.pdf-card'));
    var countEl = document.getElementById('pdf-count');
    var applyFilter = function (cat) {
      var n = 0;
      cards.forEach(function (c) { var on = cat === 'all' || c.getAttribute('data-cat') === cat; c.hidden = !on; if (on) n++; });
      chips.forEach(function (b) { var on = b.getAttribute('data-cat') === cat; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      if (countEl) countEl.textContent = 'عدد الملفات المعروضة: ' + n;
    };
    chips.forEach(function (b) {
      b.addEventListener('click', function () {
        var cat = b.getAttribute('data-cat');
        applyFilter(cat);
        if (history.replaceState) history.replaceState(null, '', cat === 'all' ? location.pathname : '#cat-' + cat);
      });
    });
    var hashFilter = function () {
      var h = location.hash || '';
      if (h.indexOf('#cat-') === 0) applyFilter(h.slice(5));
      else if (h.indexOf('#pdf-') === 0) { applyFilter('all'); var t = document.querySelector(h); if (t) t.scrollIntoView({ block: 'center' }); }
    };
    window.addEventListener('hashchange', hashFilter);
    hashFilter();

    var LEAD_KEY = '5s-lead-v1';
    var readLead = function () { try { return JSON.parse(localStorage.getItem(LEAD_KEY) || 'null'); } catch (e) { return null; } };
    var saveLead = function (d) { try { localStorage.setItem(LEAD_KEY, JSON.stringify(d)); } catch (e) {} };
    var known = document.getElementById('dl-known');
    var syncKnown = function () {
      var l = readLead();
      if (!known) return;
      known.hidden = !l;
      if (l) known.querySelector('[data-known-name]').textContent = l.name || '';
    };
    var forget = document.getElementById('dl-forget');
    if (forget) forget.addEventListener('click', function () { try { localStorage.removeItem(LEAD_KEY); } catch (e) {} syncKnown(); });
    syncKnown();

    var startDownload = function (url, title) {
      var a = document.createElement('a');
      a.href = url; a.download = url.split('/').pop(); a.rel = 'noopener';
      document.body.appendChild(a); a.click(); a.remove();
    };
    var modal = document.getElementById('dl-modal');
    var form = document.getElementById('dl-form');
    var status = document.getElementById('dl-status');
    var submit = document.getElementById('dl-submit');
    var pending = null, openerBtn = null;
    var setStatus = function (msg, err) { status.textContent = msg || ''; status.classList.toggle('is-error', !!err); };

    pdfGrid.addEventListener('click', function (e) {
      var btn = e.target.closest('.pdf-dl');
      if (!btn) return;
      var file = btn.getAttribute('data-file'), title = btn.getAttribute('data-title');
      if (readLead()) { startDownload(file, title); return; }
      pending = { file: file, title: title }; openerBtn = btn;
      document.getElementById('dl-file').textContent = title;
      setStatus('');
      if (modal && modal.showModal) { modal.showModal(); document.getElementById('dl-name').focus(); }
    });
    if (modal) {
      modal.querySelector('[data-close]').addEventListener('click', function () { modal.close(); });
      modal.addEventListener('click', function (e) { if (e.target === modal) modal.close(); });
      modal.addEventListener('close', function () { if (openerBtn) openerBtn.focus(); });
    }
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = {
        name: form.elements['name'].value.trim(),
        email: form.elements['email'].value.trim(),
        phone: form.elements['phone'].value.trim(),
        company: form.elements['company'].value.trim()
      };
      var payload = {
        'الاسم': data.name, 'البريد الإلكتروني': data.email, 'الجوال': data.phone, 'الشركة': data.company || '—',
        'الملف المطلوب': pending ? pending.title : '',
        '_subject': 'طلب تحميل ملف فني — موقع فايف إس', '_template': 'table', '_captcha': 'false',
        '_honey': form.elements['_honey'].value
      };
      submit.disabled = true; setStatus('جارٍ الإرسال…');
      fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (res) { return res.json().then(function (j) { return { ok: res.ok, j: j }; }); })
        .then(function (r) {
          var okFlag = r.ok && String(r.j && r.j.success) !== 'false';
          if (!okFlag) throw new Error('send failed');
          saveLead(data); syncKnown();
          setStatus('تم الإرسال، بدأ التحميل.');
          var p = pending; modal.close();
          if (p) startDownload(p.file, p.title);
        })
        .catch(function () { setStatus('تعذّر إرسال البيانات. تحقق من الاتصال وحاول مرة أخرى.', true); })
        .then(function () { submit.disabled = false; });
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
