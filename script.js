(function () {
  const config = window.MICROCMS_CONFIG || {};
  const newsList = document.querySelector("#cms-news-list");

  if (!newsList || !isConfigured(config)) {
    return;
  }

  // Capture the fallback cards already rendered in HTML so we can pad with them
  // when microCMS has fewer items than the desired limit.
  const fallbackCards = Array.from(newsList.querySelectorAll(".info-card")).map(
    function (c) { return c.outerHTML; }
  );

  const endpoint = `https://${config.serviceDomain}.microcms.io/api/v1/${config.endpoint}`;
  const url = new URL(endpoint);
  const limit = Number(config.limit) || 3;
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("orders", config.orders || "-publishedAt");

  loadNews(url, config.apiKey, newsList, limit, fallbackCards);
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

async function loadNews(url, apiKey, target, limit, fallbackCards) {
  try {
    const response = await fetch(url, {
      headers: { "X-MICROCMS-API-KEY": apiKey },
    });
    if (!response.ok) {
      throw new Error("microCMS fetch failed: " + response.status);
    }
    const data = await response.json();
    const contents = Array.isArray(data.contents) ? data.contents : [];

    const microCmsCards = contents.map(createNewsCard);
    const needed = Math.max(0, limit - microCmsCards.length);
    const padding = needed > 0 ? fallbackCards.slice(0, needed) : [];
    const combined = microCmsCards.concat(padding);

    if (combined.length > 0) {
      target.innerHTML = combined.join("");
      target.dataset.fallback = microCmsCards.length === 0 ? "true" : "false";
    }
  } catch (error) {
    // Network/API error: silently keep the original hardcoded fallback that's already in DOM.
    console.warn("[news] microCMS fetch failed, keeping fallback:", error.message);
  }
}

function createNewsCard(item) {
  const title = escapeHtml(item.title || item.name || "お知らせ");
  const date = item.date || item.publishedAt || item.createdAt;
  const dateLabel = formatDate(date);
  const excerpt = escapeHtml(stripHtml(item.excerpt || item.description || item.body || ""));
  const href = item.url || item.link || "";
  const body = excerpt || "詳しい内容はmicroCMSで更新できます。";

  if (href) {
    return `
      <article class="info-card">
        <time datetime="${escapeHtml(date || "")}">${dateLabel}</time>
        <h3><a href="${escapeHtml(href)}">${title}</a></h3>
        <p>${body}</p>
      </article>
    `;
  }

  return `
    <article class="info-card">
      <time datetime="${escapeHtml(date || "")}">${dateLabel}</time>
      <h3>${title}</h3>
      <p>${body}</p>
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
