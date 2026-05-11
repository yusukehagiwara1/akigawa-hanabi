// Sponsors and gallery sections fetched from microCMS.
(function () {
  const cfg = window.MICROCMS_CONFIG || {};
  const extra = window.MICROCMS_EXTRA || {};

  if (!cfg.serviceDomain || !cfg.apiKey || cfg.serviceDomain.includes("YOUR_")) {
    return;
  }

  const sponsorList = document.querySelector("#cms-sponsor-list");
  const galleryList = document.querySelector("#cms-gallery-list");

  if (sponsorList && extra.sponsors) {
    loadList(extra.sponsors, sponsorList, renderSponsors);
  }
  if (galleryList && extra.gallery) {
    loadList(extra.gallery, galleryList, renderGallery);
  }

  async function loadList(endpointCfg, target, renderer) {
    const url = new URL(
      `https://${cfg.serviceDomain}.microcms.io/api/v1/${endpointCfg.endpoint}`
    );
    url.searchParams.set("limit", String(endpointCfg.limit || 30));
    if (endpointCfg.orders) url.searchParams.set("orders", endpointCfg.orders);

    try {
      const res = await fetch(url, {
        headers: { "X-MICROCMS-API-KEY": cfg.apiKey },
      });
      if (!res.ok) throw new Error("fetch failed: " + res.status);
      const data = await res.json();
      const items = Array.isArray(data.contents) ? data.contents : [];
      const html = renderer(items);
      if (html) {
        target.innerHTML = html;
      }
    } catch (err) {
      console.warn("[microcms-extras]", endpointCfg.endpoint, err.message);
      // Leave any pre-rendered fallback in place.
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
