/* ═════════════════════════════════════════════════════════════════
   FABS DATA WAREHOUSE — main.js
   Menu, scroll effects, reveal animations, counters, flash, toasts,
   CSRF-aware fetch helper.
   ═════════════════════════════════════════════════════════════════ */
(function () {
  "use strict";

  /* ─────────────────────────────────────────────────────────────
     1. MOBILE MENU TOGGLE
     ───────────────────────────────────────────────────────────── */
  function initMobileMenu() {
    const menuBtn    = document.getElementById("menuBtn");
    const mobileMenu = document.getElementById("mobileMenu");
    if (!menuBtn || !mobileMenu) return;

    menuBtn.addEventListener("click", () => {
      const isOpen = !mobileMenu.classList.contains("hidden");
      mobileMenu.classList.toggle("hidden");
      menuBtn.setAttribute("aria-expanded", String(!isOpen));
    });

    mobileMenu.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        mobileMenu.classList.add("hidden");
        menuBtn.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* ─────────────────────────────────────────────────────────────
     2. NAVBAR SHADOW ON SCROLL
     ───────────────────────────────────────────────────────────── */
  function initNavbarScroll() {
    const navbar = document.getElementById("navbar");
    if (!navbar) return;
    const navBox = navbar.querySelector("nav");
    if (!navBox) return;

    const onScroll = () => {
      if (window.scrollY > 20) {
        navBox.classList.add("shadow-2xl", "shadow-black/40");
      } else {
        navBox.classList.remove("shadow-2xl", "shadow-black/40");
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ─────────────────────────────────────────────────────────────
     3. SCROLL REVEAL
     ───────────────────────────────────────────────────────────── */
  function initScrollReveal() {
    const items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (!("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("in"));
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -60px 0px" }
    );

    items.forEach((el) => io.observe(el));
  }

  /* ─────────────────────────────────────────────────────────────
     4. ANIMATED COUNTERS  (data-count, data-suffix, data-prefix)
     ───────────────────────────────────────────────────────────── */
  function initCounters() {
    const counters = document.querySelectorAll("[data-count]");
    if (!counters.length) return;

    if (!("IntersectionObserver" in window)) {
      counters.forEach((el) => (el.textContent = el.dataset.count));
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const el     = e.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || "";
          const prefix = el.dataset.prefix || "";
          const dur    = 1600;
          const start  = performance.now();

          function step(now) {
            const p     = Math.min((now - start) / dur, 1);
            const eased = 1 - Math.pow(1 - p, 3);
            const val   = target * eased;
            el.textContent =
              prefix +
              (target % 1 !== 0
                ? val.toFixed(1)
                : Math.floor(val).toLocaleString()) +
              suffix;
            if (p < 1) requestAnimationFrame(step);
          }
          requestAnimationFrame(step);
          io.unobserve(el);
        });
      },
      { threshold: 0.5 }
    );

    counters.forEach((c) => io.observe(c));
  }

  /* ─────────────────────────────────────────────────────────────
     5. AUTO-DISMISS FLASH MESSAGES
     ───────────────────────────────────────────────────────────── */
  function initFlashAutoDismiss() {
    document.querySelectorAll("#flashZone .flash-item").forEach((el, i) => {
      setTimeout(() => {
        el.style.transition = "opacity .4s, transform .4s";
        el.style.opacity = "0";
        el.style.transform = "translateX(20px)";
        setTimeout(() => el.remove(), 400);
      }, 8000 + i * 400);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     6. SMOOTH ANCHOR SCROLL (with navbar offset)
     ───────────────────────────────────────────────────────────── */
  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", function (e) {
        const id = this.getAttribute("href");
        if (!id || id === "#") return;
        const el = document.querySelector(id);
        if (!el) return;
        e.preventDefault();
        const top = el.getBoundingClientRect().top + window.scrollY - 96;
        window.scrollTo({ top, behavior: "smooth" });
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     7. PASSWORD VISIBILITY TOGGLES  ([data-toggle-pw="id"])
     ───────────────────────────────────────────────────────────── */
  function initPasswordToggles() {
    document.querySelectorAll("[data-toggle-pw]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const input = document.getElementById(btn.dataset.togglePw);
        if (!input) return;
        const show = input.type === "password";
        input.type = show ? "text" : "password";
        btn.setAttribute("aria-label", show ? "Hide password" : "Show password");
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     8. CSRF-AWARE FETCH HELPER  →  window.fabsFetch
     ───────────────────────────────────────────────────────────── */
  window.fabsFetch = function (url, options = {}) {
    const token =
      document.querySelector('meta[name="csrf-token"]')?.content || "";
    const headers = Object.assign(
      {
        "X-CSRFToken": token,
        "X-Requested-With": "XMLHttpRequest",
      },
      options.headers || {}
    );

    if (options.body && !(options.body instanceof FormData)) {
      headers["Content-Type"] = headers["Content-Type"] || "application/json";
    }

    return fetch(
      url,
      Object.assign({}, options, { headers, credentials: "same-origin" })
    );
  };

  /* ─────────────────────────────────────────────────────────────
     9. TOAST HELPER  →  window.fabsToast(message, tone)
     tones: info | success | error | warning
     ───────────────────────────────────────────────────────────── */
  const TONES = {
    info:    "border-fabs-cyan/40 bg-fabs-cyan/10 text-fabs-cyan",
    success: "border-emerald-500/40 bg-emerald-500/10 text-emerald-300",
    error:   "border-red-500/40 bg-red-500/10 text-red-300",
    warning: "border-fabs-gold/40 bg-fabs-gold/10 text-fabs-gold",
  };

  window.fabsToast = function (message, tone = "info") {
    let zone = document.getElementById("flashZone");
    if (!zone) {
      zone = document.createElement("div");
      zone.id = "flashZone";
      zone.className =
        "fixed top-24 right-4 z-[60] space-y-2 w-[min(92vw,380px)]";
      document.body.appendChild(zone);
    }

    const el = document.createElement("div");
    el.className =
      "flash-item glass-strong border rounded-xl px-4 py-3 text-sm flex items-start gap-3 shadow-xl " +
      (TONES[tone] || TONES.info);

    const dot = document.createElement("span");
    dot.className = "mt-0.5";
    dot.textContent = "●";

    const msg = document.createElement("span");
    msg.className = "flex-1";
    msg.textContent = message;

    const close = document.createElement("button");
    close.type = "button";
    close.className = "opacity-60 hover:opacity-100";
    close.setAttribute("aria-label", "Dismiss");
    close.textContent = "✕";
    close.addEventListener("click", () => el.remove());

    el.append(dot, msg, close);
    zone.appendChild(el);

    setTimeout(() => {
      el.style.transition = "opacity .4s, transform .4s";
      el.style.opacity = "0";
      el.style.transform = "translateX(20px)";
      setTimeout(() => el.remove(), 400);
    }, 6000);
  };

  /* ─────────────────────────────────────────────────────────────
     10. PASSWORD STRENGTH METER  (signup)
     Uses [data-strength-input], [data-strength-meter],
     [data-strength-label]
     ───────────────────────────────────────────────────────────── */
  function initPasswordStrength() {
    const pw = document.querySelector("[data-strength-input]");
    const meter = document.querySelector("[data-strength-meter]");
    const label = document.querySelector("[data-strength-label]");
    if (!pw || !meter) return;

    const bars = meter.querySelectorAll("span");
    const colors = ["bg-red-500", "bg-orange-500", "bg-fabs-gold", "bg-emerald-400"];
    const texts = [
      "Weak — add more characters.",
      "Fair — add numbers or symbols.",
      "Good — almost there.",
      "Strong password.",
    ];

    pw.addEventListener("input", () => {
      const v = pw.value;
      let score = 0;
      if (v.length >= 8) score++;
      if (/[A-Z]/.test(v) && /[a-z]/.test(v)) score++;
      if (/\d/.test(v)) score++;
      if (/[^A-Za-z0-9]/.test(v)) score++;

      bars.forEach((b, i) => {
        b.className =
          "h-1 flex-1 rounded-full transition-colors " +
          (i < score ? colors[score - 1] : "bg-fabs-line");
      });

      label.textContent = v
        ? texts[Math.max(score - 1, 0)]
        : "Use 8+ characters with letters, numbers & symbols.";
    });
  }

  /* ─────────────────────────────────────────────────────────────
     11. PASSWORD MATCH CHECK  (signup confirm)
     Uses [data-match-warning]
     ───────────────────────────────────────────────────────────── */
  function initPasswordMatch() {
    const pw = document.getElementById("password");
    const confirm = document.getElementById("confirm_password");
    const warn = document.querySelector("[data-match-warning]");
    if (!pw || !confirm || !warn) return;

    const check = () =>
      warn.classList.toggle("hidden", confirm.value === pw.value);
    confirm.addEventListener("input", check);
    pw.addEventListener("input", () => {
      if (confirm.value) check();
    });
  }

  /* ─────────────────────────────────────────────────────────────
     12. FAQ SEARCH + CATEGORY FILTER
     ───────────────────────────────────────────────────────────── */
  function initFAQ() {
    const search = document.querySelector("[data-faq-search]");
    const items = document.querySelectorAll(".faq-item");
    const empty = document.querySelector("[data-faq-empty]");
    const tabButtons = document.querySelectorAll("[data-faq-tabs] [data-faq-cat]");

    if (search) {
      search.addEventListener("input", () => {
        const q = search.value.toLowerCase().trim();
        let visible = 0;
        items.forEach((el) => {
          const match = el.textContent.toLowerCase().includes(q);
          el.classList.toggle("hidden", !match);
          if (match) visible++;
        });
        if (empty) empty.classList.toggle("hidden", visible > 0);
      });
    }

    if (tabButtons.length) {
      tabButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
          const cat = btn.dataset.faqCat;
          tabButtons.forEach((b) => {
            b.className =
              "px-4 py-2 rounded-xl text-xs font-semibold border transition border-fabs-line text-slate-400 hover:text-white hover:border-fabs-cyan/40";
          });
          btn.className =
            "px-4 py-2 rounded-xl text-xs font-semibold border transition bg-fabs-cyan/15 border-fabs-cyan/40 text-fabs-cyan";

          items.forEach((el) => {
            el.classList.toggle("hidden", cat !== "All" && el.dataset.faqCat !== cat);
          });
        });
      });
    }
  }

  /* ─────────────────────────────────────────────────────────────
     13. ADMIN SIDEBAR TOGGLE
     ───────────────────────────────────────────────────────────── */
  function initAdminSidebar() {
    const sidebar = document.getElementById("adminSidebar");
    const overlay = document.getElementById("sidebarOverlay");
    const toggle  = document.getElementById("sidebarToggle");
    if (!sidebar || !toggle) return;

    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("-translate-x-full");
      if (overlay) overlay.classList.toggle("hidden");
    });

    overlay?.addEventListener("click", () => {
      sidebar.classList.add("-translate-x-full");
      overlay.classList.add("hidden");
    });
  }

  /* ─────────────────────────────────────────────────────────────
     14. AUTO-YEAR (footer copyright if [data-year] is present)
     ───────────────────────────────────────────────────────────── */
  function initAutoYear() {
    const nodes = document.querySelectorAll("[data-year]");
    const y = new Date().getFullYear();
    nodes.forEach((n) => (n.textContent = y));
  }

  /* ─────────────────────────────────────────────────────────────
     BOOTSTRAP EVERYTHING ON DOM READY
     ───────────────────────────────────────────────────────────── */
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    initMobileMenu();
    initNavbarScroll();
    initScrollReveal();
    initCounters();
    initFlashAutoDismiss();
    initSmoothAnchors();
    initPasswordToggles();
    initPasswordStrength();
    initPasswordMatch();
    initFAQ();
    initAdminSidebar();
    initAutoYear();
  });

  /* ─────────────────────────────────────────────────────────────
     EXPOSE MODULE FOR PAGE-SPECIFIC SCRIPTS
     ───────────────────────────────────────────────────────────── */
  window.Fabs = {
    initScrollReveal,
    initCounters,
    initPasswordStrength,
    initPasswordMatch,
    initFAQ,
  };
})();