/* 5S — فايف إس | site script (vanilla, no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Header: shrink 96→72 after 80px ---------- */
  var header = $(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 80); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Mobile full-screen menu + accordions ---------- */
  var toggle = $("#menu-toggle");
  var mobileMenu = $("#mobile-menu");
  function setMenu(open) {
    if (!header || !toggle) return;
    header.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "إغلاق القائمة" : "فتح القائمة");
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (toggle && mobileMenu) {
    toggle.addEventListener("click", function () { setMenu(!header.classList.contains("menu-open")); });
    $$("a", mobileMenu).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1024) setMenu(false); });
  }
  $$(".acc-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      var open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      if (panel) panel.classList.toggle("is-open", open);
    });
  });
  /* Desktop dropdown buttons (keyboard / touch) */
  $$(".dd-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.parentElement;
      var open = !li.classList.contains("is-open");
      $$(".has-dd.is-open").forEach(function (o) { o.classList.remove("is-open"); $(".dd-btn", o).setAttribute("aria-expanded", "false"); });
      li.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest || e.target.closest(".has-dd")) return;
    $$(".has-dd.is-open").forEach(function (o) { o.classList.remove("is-open"); $(".dd-btn", o).setAttribute("aria-expanded", "false"); });
  });

  /* ---------- Hero video crossfade (poster only if reduced motion) ---------- */
  var v1 = $("#heroVideo1"), v2 = $("#heroVideo2");
  function playSafe(v) { if (!v) return; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  if (v1 && reduceMotion) {
    [v1, v2].forEach(function (v) { if (v) { v.removeAttribute("autoplay"); v.pause(); } });
  } else if (v1 && v2) {
    var active = 1, switching = false;
    playSafe(v1);
    window.setInterval(function () {
      if (switching || document.hidden) return;
      switching = true;
      var show = active === 1 ? v2 : v1, hide = active === 1 ? v1 : v2;
      if (show.preload === "none") { show.preload = "auto"; show.load(); }
      show.currentTime = 0; playSafe(show);
      show.classList.add("is-active"); hide.classList.remove("is-active");
      active = active === 1 ? 2 : 1;
      window.setTimeout(function () { hide.pause(); switching = false; }, 1200);
    }, 10000);
  }

  /* ---------- Reveal (600ms, +24px, once) with 80ms stagger ---------- */
  $$(".stagger").forEach(function (group) {
    $$(":scope > .reveal", group).forEach(function (el, i) { el.style.setProperty("--d", (i * 80) + "ms"); });
  });
  var counters = $$("[data-count]");
  var particles = $$(".particles");
  function animateCount(el) {
    var target = parseFloat(el.getAttribute("data-count"));
    if (isNaN(target)) return;
    var suffix = el.getAttribute("data-suffix") || "";
    if (reduceMotion) { el.textContent = target + suffix; return; }
    var start = null, dur = 1500;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target;
        if (t.classList.contains("reveal")) t.classList.add("is-visible");
        if (t.hasAttribute("data-count")) animateCount(t);
        if (t.classList.contains("particles")) window.setTimeout(function () { t.classList.add("is-bonded"); }, 300);
        io.unobserve(t);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    $$(".reveal").concat(counters, particles).forEach(function (el) { io.observe(el); });
  } else {
    $$(".reveal").forEach(function (el) { el.classList.add("is-visible"); });
    counters.forEach(animateCount);
    particles.forEach(function (p) { p.classList.add("is-bonded"); });
  }

  /* ---------- Before / after slider (range input = touch + keyboard) ---------- */
  $$(".ba").forEach(function (ba) {
    var range = $("input[type=range]", ba);
    if (!range) return;
    var set = function () { ba.style.setProperty("--pos", range.value + "%"); };
    range.addEventListener("input", set);
    set();
  });

  /* ---------- Testimonials: manual slider only ---------- */
  $$(".tslider").forEach(function (sl) {
    var slides = $$(".tslide", sl), dotsBox = $(".dots", sl), i = 0;
    if (!slides.length) return;
    slides.forEach(function (_, n) {
      var b = document.createElement("button");
      b.type = "button"; b.setAttribute("aria-label", "الشهادة " + (n + 1));
      b.addEventListener("click", function () { go(n); });
      dotsBox.appendChild(b);
    });
    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle("is-active", k === i); s.setAttribute("aria-hidden", k === i ? "false" : "true"); });
      $$("button", dotsBox).forEach(function (d, k) { d.setAttribute("aria-current", k === i ? "true" : "false"); });
    }
    $(".prev", sl).addEventListener("click", function () { go(i - 1); });
    $(".next", sl).addEventListener("click", function () { go(i + 1); });
    go(0);
  });

  /* ---------- Material calculator ----------
     IMPORTANT: placeholder coefficients. The 5S technical team must supply the
     real consumption rate (litres of diluted product per m²) for each application.
     DUST 3.6 L/m² and WALK 6 L/m² are the rates published for the King Salman
     Energy City and AlUla Old Town projects — used only as provisional examples. */
  var CALC_COEFFICIENTS = {
    berm:  { label: "تثبيت الرمال والكثبان (5S BERM)", litresPerM2: 3,   depth: false, placeholder: true },
    road:  { label: "طرق ترابية (5S ROAD)",            litresPerM2PerCm: 1.0, depth: true, placeholder: true },
    slope: { label: "منحدرات وأكتاف طرق (5S SLOPE)",   litresPerM2: 4,   depth: false, placeholder: true },
    dust:  { label: "التحكم في الغبار (5S DUST)",       litresPerM2: 3.6, depth: false, placeholder: true },
    walk:  { label: "ممرات وأرصفة (5S WALK)",           litresPerM2: 6,   depth: false, placeholder: true }
  };
  var IBC_LITRES = 1000; // standard IBC tote capacity — confirm with 5S
  window.CALC_COEFFICIENTS = CALC_COEFFICIENTS;
  function estimate(type, area, depth) {
    var c = CALC_COEFFICIENTS[type];
    if (!c || !(area > 0)) return null;
    var litres = c.depth ? area * Math.max(depth || 10, 1) * c.litresPerM2PerCm : area * c.litresPerM2;
    return { litres: Math.round(litres), ibc: Math.max(1, Math.ceil(litres / IBC_LITRES)) };
  }
  var fmt = function (n) { return n.toLocaleString("en-US"); };
  var qs = new URLSearchParams(window.location.search);

  $$("[data-calc]").forEach(function (form) {
    var type = $("[name=type]", form), area = $("[name=area]", form), depth = $("[name=depth]", form), loc = $("[name=location]", form);
    var out = $(".calc-result", form.parentElement) || $(".calc-result");
    var depthField = depth ? depth.closest(".field") : null;
    if (qs.get("type") && type) type.value = qs.get("type");
    if (qs.get("area") && area) area.value = qs.get("area");
    function syncDepth() { if (depthField) depthField.hidden = !(CALC_COEFFICIENTS[type.value] || {}).depth; }
    function run() {
      syncDepth();
      var r = estimate(type.value, parseFloat(area.value), depth ? parseFloat(depth.value) : 0);
      if (!out) return;
      if (!r) { out.querySelector(".big").innerHTML = "أدخل نوع التطبيق والمساحة"; out.dataset.ready = ""; return; }
      out.querySelector(".big").innerHTML = "≈ <b>" + fmt(r.ibc) + "</b> حاوية IBC <small>(" + fmt(r.litres) + " لتر تقريبًا)</small>";
      out.dataset.ready = "1";
      var link = $("[data-quote-link]", out.parentElement) || $("[data-quote-link]");
      if (link) {
        var p = new URLSearchParams({ product: type.value, area: area.value, qty: r.ibc + " IBC (تقديري)" });
        if (loc && loc.value) p.set("location", loc.value);
        if (depth && !depthField.hidden && depth.value) p.set("depth", depth.value);
        link.href = link.getAttribute("data-base") + "?" + p.toString() + "#quote";
      }
      var full = $("[data-full-link]", form.parentElement);
      if (full) full.href = full.getAttribute("data-base") + "?type=" + encodeURIComponent(type.value) + "&area=" + encodeURIComponent(area.value);
    }
    form.addEventListener("input", run);
    form.addEventListener("change", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
    run();
  });

  /* ---------- Prefill contact form from query string ---------- */
  var cform = $("#quote-form");
  if (cform && qs.toString()) {
    var map = { product: "product", area: "area", location: "location", sector: "sector" };
    Object.keys(map).forEach(function (k) {
      var v = qs.get(k), f = cform.elements[map[k]];
      if (v && f) f.value = v;
    });
    var msg = cform.elements.message;
    if (msg && qs.get("qty")) {
      msg.value = "طلب عرض دقيق من حاسبة المواد:\nالكمية التقديرية: " + qs.get("qty") +
        (qs.get("depth") ? "\nعمق المعالجة: " + qs.get("depth") + " سم" : "") +
        (qs.get("location") ? "\nالموقع: " + qs.get("location") : "");
    }
  }

  /* ---------- Forms: inline Arabic validation + AJAX submit ---------- */
  var MSG = {
    required: "هذا الحقل مطلوب",
    email: "يرجى إدخال بريد إلكتروني صحيح، مثل name@company.com",
    phone: "يرجى إدخال رقم جوال سعودي صحيح يبدأ بـ 5 ويتكون من 9 أرقام",
    file: "حجم الملف يجب ألا يتجاوز 5 ميجابايت"
  };
  function fieldError(input) {
    var v = (input.value || "").trim();
    if (input.type === "checkbox" || input.type === "hidden" || input.classList.contains("hp")) return "";
    if (input.required && !v) return MSG.required;
    if (!v) return "";
    if (input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return MSG.email;
    if (input.dataset.phone !== undefined) {
      var d = v.replace(/[\s-]/g, "").replace(/^(\+?966|0)/, "");
      if (!/^5\d{8}$/.test(d)) return MSG.phone;
    }
    if (input.type === "file" && input.files && input.files[0] && input.files[0].size > 5 * 1024 * 1024) return MSG.file;
    return "";
  }
  function showError(input, msg) {
    var field = input.closest(".field");
    if (!field) return;
    var err = $(".err", field);
    if (!err) { err = document.createElement("span"); err.className = "err"; err.setAttribute("aria-live", "polite"); field.appendChild(err); }
    err.textContent = msg;
    field.classList.toggle("has-error", !!msg);
    input.setAttribute("aria-invalid", msg ? "true" : "false");
  }
  $$("form[data-validate]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    var inputs = $$("input, select, textarea", form);
    inputs.forEach(function (inp) {
      inp.addEventListener("blur", function () { showError(inp, fieldError(inp)); });
      inp.addEventListener("input", function () { if (inp.getAttribute("aria-invalid") === "true") showError(inp, fieldError(inp)); });
    });
    form.addEventListener("submit", function (e) {
      var first = null;
      inputs.forEach(function (inp) { var m = fieldError(inp); showError(inp, m); if (m && !first) first = inp; });
      if (first) { e.preventDefault(); first.focus(); return; }
      var hp = $(".hp input", form);
      if (hp && hp.value) { e.preventDefault(); return; }
      var hasFile = $$("input[type=file]", form).some(function (f) { return f.files && f.files.length; });
      if (hasFile || !window.fetch) return; // regular POST (supports attachments)
      e.preventDefault();
      var btn = $("button[type=submit]", form);
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "جارٍ الإرسال…"; }
      var action = form.getAttribute("action").replace("formsubmit.co/", "formsubmit.co/ajax/");
      fetch(action, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(form) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function () {
          var ok = $(".form-success", form.parentElement);
          form.reset();
          if (ok) { ok.classList.add("is-shown"); ok.setAttribute("tabindex", "-1"); ok.focus(); }
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        })
        .catch(function () { form.submit(); });
    });
  });

  /* ---------- Projects filter ---------- */
  var pf = $("#project-filters");
  if (pf) {
    var cards = $$("[data-project]");
    var empty = $("#projects-empty");
    var apply = function () {
      var s = pf.elements.sector.value, t = pf.elements.tech.value, c = pf.elements.country.value, shown = 0;
      cards.forEach(function (card) {
        var ok = (!s || card.dataset.sector === s) && (!t || card.dataset.tech === t) && (!c || card.dataset.country === c);
        card.hidden = !ok; if (ok) shown++;
      });
      if (empty) empty.classList.toggle("is-shown", shown === 0);
    };
    pf.addEventListener("change", apply);
    pf.addEventListener("reset", function () { window.setTimeout(apply, 0); });
    apply();
  }

  /* ---------- Technical data search ---------- */
  var td = $("#td-search");
  if (td) {
    var rows = $$("#td-table tbody tr");
    var typeSel = $("#td-type");
    var tdEmpty = $("#td-empty");
    var run2 = function () {
      var q = td.value.trim().toLowerCase(), ty = typeSel.value, n = 0;
      rows.forEach(function (r) {
        var ok = (!q || r.textContent.toLowerCase().indexOf(q) > -1) && (!ty || r.dataset.type === ty);
        r.hidden = !ok; if (ok) n++;
      });
      tdEmpty.classList.toggle("is-shown", n === 0);
    };
    td.addEventListener("input", run2);
    typeSel.addEventListener("change", run2);
  }

  /* ---------- Footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
