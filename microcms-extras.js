// Sponsors and gallery sections fetched from microCMS.
(function () {
  const cfg = window.MICROCMS_CONFIG || {};
  const extra = window.MICROCMS_EXTRA || {};

  if (!cfg.serviceDomain || !cfg.apiKey || cfg.serviceDomain.includes("YOUR_")) {
    return;
  }

  const sponsorList = document.querySelector("#cms-sponsor-list");
  const galleryList = document.querySelector("#cms-gallery-list");
  const testimonialList = document.querySelector("#cms-testimonial-list");
  const testimonialSection = document.querySelector("#testimonials");
  const pressList = document.querySelector("#cms-press-list");
  const pressSection = document.querySelector("#cms-press-section");
  const faqDynamicList = document.querySelector("#cms-faq-list");
  const faqDynamicSection = document.querySelector("#cms-faq-section");

  // Pattern: if the target element has data-has-fallback="true", a CMS-empty
  // response keeps the static fallback markup visible instead of hiding the
  // whole section. Sections without static fallback hide on empty.
  const hasFallback = function (el) {
    return Boolean(el && el.dataset && el.dataset.hasFallback === "true");
  };

  if (sponsorList && extra.sponsors) {
    loadList(extra.sponsors, sponsorList, renderSponsors);
  }
  if (galleryList && extra.gallery) {
    const galleryFallback = hasFallback(galleryList);
    const gallerySection = galleryList.closest("section");
    loadList(extra.gallery, galleryList, renderGallery, function (count) {
      // Empty CMS + no static fallback → hide section. (Gallery static
      // markup ships with index.html so this normally stays put.)
      if (count === 0 && gallerySection && !galleryFallback) {
        gallerySection.style.display = "none";
      }
    });
  }
  if (testimonialList && extra.testimonial) {
    const testimonialFallback = hasFallback(testimonialList);
    loadList(extra.testimonial, testimonialList, renderTestimonials, function (count) {
      if (count === 0 && testimonialSection && !testimonialFallback) {
        testimonialSection.style.display = "none";
      }
    });
  }
  if (pressList && extra.pressRelease) {
    const pressFallback = hasFallback(pressList);
    loadList(extra.pressRelease, pressList, renderPressReleases, function (count) {
      // count<=0 はデータ0件 または 取得失敗(-1)。フォールバックが無ければ
      // 見出しごとセクションを隠す（空グリッドの露出防止）。
      if (count <= 0 && pressSection && !pressFallback) {
        pressSection.style.display = "none";
      }
    });
  }
  if (faqDynamicList && extra.faqDynamic) {
    const faqFallback = hasFallback(faqDynamicList);
    loadList(extra.faqDynamic, faqDynamicList, renderFaqDynamic, function (count) {
      if (count === 0 && faqDynamicSection && !faqFallback) {
        faqDynamicSection.style.display = "none";
      }
    });
  }

  async function loadList(endpointCfg, target, renderer, onComplete) {
    const url = new URL(
      `https://${cfg.serviceDomain}.microcms.io/api/v1/${endpointCfg.endpoint}`
    );
    url.searchParams.set("limit", String(endpointCfg.limit || 30));
    if (endpointCfg.orders) url.searchParams.set("orders", endpointCfg.orders);

    // Mark as loading for screen readers
    target.setAttribute("aria-busy", "true");

    // 6-second hard timeout — see script.js for rationale.
    const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
    const timeoutId = controller
      ? setTimeout(function () { controller.abort(); }, 6000)
      : null;

    try {
      const res = await fetch(url, {
        headers: { "X-MICROCMS-API-KEY": cfg.apiKey },
        signal: controller ? controller.signal : undefined,
      });
      if (!res.ok) throw new Error("fetch failed: " + res.status);
      const data = await res.json();
      const items = Array.isArray(data.contents) ? data.contents : [];
      const html = renderer(items);
      if (html) {
        target.innerHTML = html;
      }
      if (typeof onComplete === "function") onComplete(items.length);
    } catch (err) {
      const wasAborted = err && err.name === "AbortError";
      console.warn("[microcms-extras]", endpointCfg.endpoint, wasAborted ? "timeout" : err.message);
      // Leave any pre-rendered fallback in place.
      if (typeof onComplete === "function") onComplete(-1);
    } finally {
      if (timeoutId) clearTimeout(timeoutId);
      target.setAttribute("aria-busy", "false");
    }
  }

  function renderSponsors(items) {
    if (!items.length) return "";
    return items
      .map(function (s) {
        const logo = mediaUrl(s.logo);
        const name = escapeHtml(s.name || "");
        const inner = `<img src="${escapeHtml(logo)}" alt="${name}" loading="lazy" decoding="async">`;
        if (s.url) {
          return `<div class="sponsor-tile"><a href="${escapeHtml(
            s.url
          )}" target="_blank" rel="noopener">${inner}</a></div>`;
        }
        return `<div class="sponsor-tile">${inner}</div>`;
      })
      .join("");
  }

  // Caption → local image overrides. Used when microCMS has stale/wrong images.
  // Edit this map to substitute specific captions with curated photos.
  const GALLERY_IMAGE_OVERRIDES = {
    "多彩な花火が秋の夜空に": "assets/wp/DSC_2664.webp",
    "クライマックスの大玉連発": "assets/wp/DSC_2569.webp",
    "夜空を埋め尽くす音楽花火": "assets/past-01.webp",
    "提灯と屋台が灯す秋の夜": "assets/past-02.webp",
    "屋台・キッチンカーのグルメ": "assets/past-03.webp",
    "地域のダンスでステージが沸く": "assets/past-04.webp",
  };

  function resolveGalleryImage(caption, fallbackUrl) {
    const trimmed = (caption || "").trim();
    if (GALLERY_IMAGE_OVERRIDES[trimmed]) {
      return GALLERY_IMAGE_OVERRIDES[trimmed];
    }
    // Detect Coming Soon / map placeholders in URL and substitute
    if (
      fallbackUrl &&
      (/coming[- ]?soon/i.test(fallbackUrl) ||
        /placeholder/i.test(fallbackUrl) ||
        /\/1-(?:1|2|9|10)\.webp/i.test(fallbackUrl))
    ) {
      return "assets/past-01.webp"; // fallback to a real fireworks photo
    }
    return fallbackUrl;
  }

  function renderGallery(items) {
    if (!items.length) return "";
    return items
      .map(function (g) {
        const rawImg = mediaUrl(g.image);
        const cap = g.caption || "";
        const img = resolveGalleryImage(cap, rawImg);
        const capEsc = escapeHtml(cap);
        return `<figure class="past-tile"><span class="zoom-hint" aria-hidden="true"></span><img src="${escapeHtml(
          img
        )}" alt="${capEsc}" loading="lazy" decoding="async"><figcaption>${capEsc}</figcaption></figure>`;
      })
      .join("");
  }

  function renderTestimonials(items) {
    if (!items.length) return "";
    return items
      .map(function (t) {
        const name = escapeHtml(t.name || "ご来場者");
        const role = escapeHtml(t.role || "");
        const comment = escapeHtml(t.comment || "");
        const year = escapeHtml(t.year ? String(t.year) : "");
        const avatar = mediaUrl(t.image);
        const avatarHtml = avatar
          ? `<img class="testimonial-avatar" src="${escapeHtml(
              avatar
            )}" alt="" loading="lazy" decoding="async">`
          : `<span class="testimonial-avatar testimonial-avatar-placeholder" aria-hidden="true"></span>`;
        const meta = [role, year ? year + "年" : ""].filter(Boolean).join("／");
        return `
          <article class="testimonial-card">
            <p class="testimonial-quote">${comment}</p>
            <div class="testimonial-footer">
              ${avatarHtml}
              <div>
                <p class="testimonial-name">${name}</p>
                ${meta ? `<p class="testimonial-meta">${escapeHtml(meta)}</p>` : ""}
              </div>
            </div>
          </article>
        `;
      })
      .join("");
  }

  function renderPressReleases(items) {
    if (!items.length) return "";
    return items
      .map(function (p) {
        const title = escapeHtml(p.title || "");
        const outlet = escapeHtml(p.outlet || "");
        const date = p.date || p.published_at || p.publishedAt;
        const href = p.url || "";
        const dateLabel = formatDateShort(date);
        const summary = escapeHtml(p.summary || "");
        const logo = mediaUrl(p.logo);
        const logoHtml = logo
          ? `<img class="press-card-logo" src="${escapeHtml(logo)}" alt="${outlet}" loading="lazy" decoding="async">`
          : "";
        const titleHtml = href
          ? `<a class="press-card-title" href="${escapeHtml(
              href
            )}" target="_blank" rel="noopener">${title}</a>`
          : `<span class="press-card-title">${title}</span>`;
        return `
          <article class="press-card">
            <div class="press-card-meta">
              ${logoHtml}
              <div>
                ${outlet ? `<p class="press-card-outlet">${outlet}</p>` : ""}
                ${dateLabel ? `<time class="press-card-date">${dateLabel}</time>` : ""}
              </div>
            </div>
            ${titleHtml}
            ${summary ? `<p class="press-card-summary">${summary}</p>` : ""}
          </article>
        `;
      })
      .join("");
  }

  function renderFaqDynamic(items) {
    if (!items.length) return "";
    return items
      .map(function (f) {
        const q = escapeHtml(f.question || "");
        const a = escapeHtml(f.answer || "");
        const cat = escapeHtml(f.category || "");
        return `
          <details class="faq-item-dynamic"${f.open ? " open" : ""}>
            <summary>
              ${cat ? `<span class="faq-item-cat">${cat}</span>` : ""}
              <span class="faq-item-q">${q}</span>
            </summary>
            <p>${a}</p>
          </details>
        `;
      })
      .join("");
  }

  function formatDateShort(value) {
    if (!value) return "";
    const d = new Date(value);
    if (isNaN(d.getTime())) return "";
    return new Intl.DateTimeFormat("ja-JP", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    })
      .format(d)
      .replaceAll("/", ".");
  }

  function mediaUrl(value) {
    if (!value) return "";
    if (typeof value === "string") return value;
    if (value.url) return value.url;
    return "";
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c];
    });
  }
})();
