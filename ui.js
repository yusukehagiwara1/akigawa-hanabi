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
      nav.classList.remove("is-open");
      document.body.style.overflow = "";
      if (returnFocus) {
        toggle.focus();
      }
    };
    const openNav = function () {
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "メニューを閉じる");
      nav.classList.add("is-open");
      document.body.style.overflow = "hidden";
    };
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
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

  // --- Event countdown (days until 第8回) ---
  const countdownNodes = document.querySelectorAll("[data-countdown-target]");
  countdownNodes.forEach(function (node) {
    const target = node.getAttribute("data-countdown-target");
    if (!target) return;
    const targetDate = new Date(target);
    if (Number.isNaN(targetDate.getTime())) return;

    const update = function () {
      const now = new Date();
      const diffMs = targetDate.getTime() - now.getTime();
      const daysEl = node.querySelector("[data-countdown-days]");
      const valueEl = node.querySelector(".notice-countdown-value");

      if (diffMs <= 0) {
        // Event has started/ended — switch to a celebratory message
        if (valueEl) valueEl.textContent = "本日開催！";
        node.classList.add("is-today");
        return;
      }

      const days = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
      if (daysEl) daysEl.textContent = String(days);

      // Add urgency class as we get closer
      if (days <= 7) {
        node.classList.add("is-urgent");
      } else if (days <= 30) {
        node.classList.add("is-soon");
      }
    };

    update();
    // Refresh once per hour in case the user keeps the tab open
    setInterval(update, 60 * 60 * 1000);
  });

  // --- Share: copy URL button (with fallback) ---
  const copyButtons = document.querySelectorAll(".share-btn-copy");
  copyButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const url = btn.getAttribute("data-share-url") || window.location.href;
      const showCopied = function () {
        const original = btn.querySelector("span");
        const originalText = original ? original.textContent : "";
        if (original) original.textContent = "コピーしました ✓";
        btn.classList.add("is-copied");
        setTimeout(function () {
          if (original) original.textContent = originalText;
          btn.classList.remove("is-copied");
        }, 2000);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(showCopied).catch(function () {
          window.prompt("以下のURLをコピーしてください:", url);
        });
      } else {
        // Fallback for older browsers
        const textarea = document.createElement("textarea");
        textarea.value = url;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "absolute";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand("copy");
          showCopied();
        } catch (e) {
          window.prompt("以下のURLをコピーしてください:", url);
        }
        document.body.removeChild(textarea);
      }
    });
  });

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

  // --- Past-gallery lightbox ---
  const galleryGrid = document.querySelector(".past-grid");
  if (galleryGrid && "HTMLDialogElement" in window) {
    const dialog = document.createElement("dialog");
    dialog.className = "lightbox";
    dialog.innerHTML =
      '<button class="lightbox-close" type="button" aria-label="閉じる">&times;</button>' +
      '<figure><img alt="" /><figcaption></figcaption></figure>';
    document.body.appendChild(dialog);
    const lbImg = dialog.querySelector("img");
    const lbCap = dialog.querySelector("figcaption");
    const lbClose = dialog.querySelector(".lightbox-close");

    galleryGrid.addEventListener("click", function (e) {
      const fig = e.target.closest(".past-tile");
      if (!fig) return;
      const img = fig.querySelector("img");
      const cap = fig.querySelector("figcaption");
      if (!img) return;
      lbImg.src = img.currentSrc || img.src;
      lbImg.alt = img.alt || "";
      lbCap.textContent = cap ? cap.textContent : "";
      dialog.showModal();
    });

    lbClose.addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (e) {
      if (e.target === dialog) dialog.close();
    });
  }

  // --- Food vendor cards: separate vendors WITHOUT photos into a text-list at the bottom ---
  (function rearrangeFoodVendors() {
    const placeholderPattern = /\/(?:1-1|1-2|1-9|1-10)\.webp$/i;
    // Find vendor columns (must contain an image AND a heading)
    const allColumns = document.querySelectorAll(".prose .wp-block-column");
    const noPhotoVendors = [];
    allColumns.forEach(function (col) {
      const img = col.querySelector(":scope > figure.wp-block-image > img");
      const heading = col.querySelector(":scope > h4");
      if (!img || !heading) return;
      const src = img.getAttribute("src") || "";
      if (!placeholderPattern.test(src)) return;
      // This vendor uses a Coming Soon placeholder image
      const name = heading.textContent.trim();
      const descEl = col.querySelector(":scope > p:not(.placeholder-tba)");
      const desc = descEl ? descEl.textContent.trim() : "";
      // Skip pure placeholder entries (name like "（詳細未掲載）" should already be removed)
      if (!name || name.indexOf("（詳細未掲載）") !== -1) {
        col.style.display = "none";
        return;
      }
      noPhotoVendors.push({ name: name, desc: desc });
      col.style.display = "none";
    });

    if (noPhotoVendors.length === 0) return;

    // Find the food booth section's content wrapper and append a clean text list
    const foodHeading = Array.from(document.querySelectorAll(".prose h3")).find(
      function (h) { return h.textContent.trim() === "出店店舗"; }
    );
    if (!foodHeading) return;

    // Walk forward to find the last vendor columns block, then append a list right after
    let insertAfter = foodHeading.nextElementSibling;
    while (insertAfter && insertAfter.nextElementSibling) {
      // Stop at the next h3 or end of parent content
      const next = insertAfter.nextElementSibling;
      if (next.tagName === "H3" || next.tagName === "H2") break;
      insertAfter = next;
    }

    const list = document.createElement("div");
    list.className = "vendor-text-list";
    const listTitle = document.createElement("p");
    listTitle.className = "vendor-text-list-title";
    listTitle.textContent = "そのほかの出店店舗（写真準備中）";
    list.appendChild(listTitle);
    const ul = document.createElement("ul");
    noPhotoVendors.forEach(function (v) {
      const li = document.createElement("li");
      const strong = document.createElement("strong");
      strong.textContent = v.name;
      li.appendChild(strong);
      if (v.desc) {
        const span = document.createElement("span");
        span.textContent = v.desc;
        li.appendChild(span);
      }
      ul.appendChild(li);
    });
    list.appendChild(ul);
    insertAfter.parentNode.insertBefore(list, insertAfter.nextSibling);
  })();

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
