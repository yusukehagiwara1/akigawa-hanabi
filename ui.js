// UI interactions: mobile nav toggle, header scroll shadow, fade-in animations.
(function () {
  // --- Highlight current page in nav ---
  const currentPath = window.location.pathname.split("/").pop() || "index.html";
  const navLinks = document.querySelectorAll(".nav a, .footer-nav a");
  navLinks.forEach(function (link) {
    const href = link.getAttribute("href") || "";
    const linkPath = href.split("?")[0].split("#")[0].split("/").pop();
    if (linkPath && linkPath === currentPath) {
      link.classList.add("is-active");
      link.setAttribute("aria-current", "page");
    }
  });

  // --- Mobile nav toggle ---
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#primary-nav");
  if (toggle && nav) {
    const closeNav = function (returnFocus) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "メニューを開く");
      document.body.style.overflow = "";
      if (returnFocus) {
        toggle.focus();
      }
    };
    const openNav = function () {
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "メニューを閉じる");
      document.body.style.overflow = "hidden";
    };
    toggle.addEventListener("click", function () {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      if (expanded) {
        closeNav();
      } else {
        openNav();
      }
    });
    // Close menu when a nav link is tapped
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
    // Close on Escape (returns focus to toggle for keyboard users)
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        closeNav(true);
      }
    });
    // Close when clicking the nav backdrop area (outside the link list)
    nav.addEventListener("click", function (e) {
      if (e.target === nav) {
        closeNav();
      }
    });
  }

  // --- Scroll progress bar ---
  const progressBar = document.createElement("div");
  progressBar.className = "scroll-progress";
  progressBar.setAttribute("aria-hidden", "true");
  document.body.appendChild(progressBar);

  // --- Header scroll shadow + scroll-to-top button + scroll-hint fadeout ---
  const header = document.querySelector(".site-header");
  const scrollTopBtn = document.querySelector(".scroll-top");
  const scrollHint = document.querySelector(".hero-scroll-hint");
  if (scrollTopBtn) {
    scrollTopBtn.removeAttribute("hidden");
    scrollTopBtn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
  if (header || scrollTopBtn || scrollHint || progressBar) {
    const onScroll = function () {
      const y = window.scrollY;
      if (header) {
        header.classList.toggle("is-scrolled", y > 12);
      }
      if (scrollTopBtn) {
        scrollTopBtn.classList.toggle("is-visible", y > 480);
      }
      if (scrollHint) {
        scrollHint.classList.toggle("is-hidden", y > 60);
      }
      if (progressBar) {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        const ratio = max > 0 ? Math.min(1, y / max) : 0;
        progressBar.style.transform = "scaleX(" + ratio + ")";
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    onScroll();
  }

  // --- Scroll fade-in animations ---
  if (
    "IntersectionObserver" in window &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    const fadeTargets = document.querySelectorAll(
      ".section, .notice, .program-card, .stats article, .ticket-card, .info-card, .past-tile, .sponsor-tile, .access-grid, .contact-card"
    );
    fadeTargets.forEach(function (el) {
      el.classList.add("fade-target");
    });
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );
    fadeTargets.forEach(function (el) {
      io.observe(el);
    });
  }
})();
