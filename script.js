(function () {
  const config = window.MICROCMS_CONFIG || {};
  const newsList = document.querySelector("#cms-news-list");

  if (!newsList || !isConfigured(config)) {
    return;
  }

  const endpoint = `https://${config.serviceDomain}.microcms.io/api/v1/${config.endpoint}`;
  const url = new URL(endpoint);
  const limit = Number(config.limit) || 3;
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("orders", config.orders || "-publishedAt");

  loadNews(url, config.apiKey, newsList);
})();

function isConfigured(config) {
  return Boolean(
    config.serviceDomain &&
      config.apiKey &&
      config.endpoint &&
      !config.serviceDomain.includes("YOUR_") &&
      !config.apiKey.includes("YOUR_")
  );
}

async function loadNews(url, apiKey, target) {
  try {
    const response = await fetch(url, {
      headers: { "X-MICROCMS-API-KEY": apiKey },
    });
    if (!response.ok) {
      throw new Error("microCMS fetch failed: " + response.status);
    }
    const data = await response.json();
    const contents = Array.isArray(data.contents) ? data.contents : [];

    if (contents.length === 0) {
      target.innerHTML = '<p class="cms-status">現在、公開中のお知らせはありません。</p>';
      return;
    }
    target.innerHTML = contents.map(createNewsCard).join("");
  } catch (error) {
    console.warn("[news] microCMS fetch failed:", error.message);
    target.innerHTML =
      '<p class="cms-status cms-status-error">最新情報を読み込めませんでした。</p>';
  }
}

function extractThumbnail(item) {
  // 1) Dedicated image field if present (image type returns object with .url)
  if (item.thumbnail) {
    if (typeof item.thumbnail === "string") return item.thumbnail;
    if (item.thumbnail.url) return item.thumbnail.url;
  }
  if (item.image) {
    if (typeof item.image === "string") return item.image;
    if (item.image.url) return item.image.url;
  }
  // 2) Fall back to the first <img> inside body / description
  const body = String(item.body || item.description || "");
  const match = body.match(/<img[^>]+src=["']([^"']+)["']/i);
  return match ? match[1] : null;
}

function createNewsCard(item) {
  const title = escapeHtml(item.title || item.name || "お知らせ");
  const date = item.date || item.publishedAt || item.createdAt;
  const dateLabel = formatDate(date);
  const excerpt = escapeHtml(stripHtml(item.excerpt || item.description || item.body || ""));
  const href = item.url || item.link || "";
  const body = excerpt || "詳しい内容はmicroCMSで更新できます。";
  const thumb = extractThumbnail(item);
  const thumbHtml = thumb
    ? `<div class="info-card-thumb"><img src="${escapeHtml(thumb)}" alt="" loading="lazy"></div>`
    : "";

  const titleEl = href
    ? `<h3><a href="${escapeHtml(href)}">${title}</a></h3>`
    : `<h3>${title}</h3>`;

  return `
    <article class="info-card${thumb ? " has-thumb" : ""}">
      ${thumbHtml}
      <div class="info-card-body">
        <time datetime="${escapeHtml(date || "")}">${dateLabel}</time>
        ${titleEl}
        <p>${body}</p>
      </div>
    </article>
  `;
}

function formatDate(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return escapeHtml(String(value));
  }

  return new Intl.DateTimeFormat("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  })
    .format(date)
    .replaceAll("/", ".");
}

function stripHtml(value) {
  return String(value).replace(/<[^>]*>/g, "").slice(0, 80);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, function (char) {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    }[char];
  });
}
