(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  var toggle = document.getElementById("menu-toggle");
  var nav = document.getElementById("main-nav");
  var isHome = document.body.classList.contains("page-home");

  function closeMenu() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "فتح القائمة");
  }

  function openMenu() {
    if (!nav || !toggle) return;
    nav.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "إغلاق القائمة");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 760) closeMenu();
    });
  }

  // Header scroll state
  if (header) {
    var onScroll = function () {
      var scrolled = window.scrollY > 8;
      if (isHome) {
        header.classList.toggle("is-scrolled", scrolled);
      } else {
        header.style.boxShadow = scrolled
          ? "0 8px 24px rgba(17,24,39,0.06)"
          : "none";
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Hero video crossfade (matches old 5s-tech.org slider)
  var v1 = document.getElementById("heroVideo1");
  var v2 = document.getElementById("heroVideo2");
  var reduceMotion =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (v1 && v2 && !reduceMotion) {
    var active = 1;
    var switching = false;

    function playSafe(video) {
      var p = video.play();
      if (p && typeof p.catch === "function") p.catch(function () {});
    }

    function switchVideos() {
      if (switching) return;
      switching = true;
      var show = active === 1 ? v2 : v1;
      var hide = active === 1 ? v1 : v2;
      show.currentTime = 0;
      playSafe(show);
      show.classList.add("is-active");
      hide.classList.remove("is-active");
      active = active === 1 ? 2 : 1;
      window.setTimeout(function () {
        hide.pause();
        switching = false;
      }, 1200);
    }

    playSafe(v1);
    // Crossfade every ~10s (old site style)
    window.setInterval(switchVideos, 10000);
  } else if (v1 && !reduceMotion) {
    var p = v1.play();
    if (p && typeof p.catch === "function") p.catch(function () {});
  }

  // Reveal on scroll
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) {
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  // Smooth scroll for same-page anchors with sticky header offset
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var id = anchor.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var offset = header ? header.offsetHeight + 8 : 0;
      var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top: top, behavior: "smooth" });
      history.pushState(null, "", id);
    });
  });
})();
