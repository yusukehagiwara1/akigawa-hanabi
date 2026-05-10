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

  function renderGallery(items) {
    if (!items.length) return "";
    return items
      .map(function (g) {
        const img = mediaUrl(g.image);
        const cap = escapeHtml(g.caption || "");
        return `<figure class="past-tile"><img src="${escapeHtml(
          img
        )}" alt="${cap}" loading="lazy" decoding="async"><figcaption>${cap}</figcaption></figure>`;
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
