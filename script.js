(function () {
  const config = window.MICROCMS_CONFIG || {};
  const newsList = document.querySelector("#cms-news-list");

  if (!newsList || !isConfigured(config)) {
    return;
  }

  const endpoint = `https://${config.serviceDomain}.microcms.io/api/v1/${config.endpoint}`;
  const url = new URL(endpoint);
  url.searchParams.set("limit", String(config.limit || 3));
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
  target.dataset.fallback = "false";
  target.innerHTML = '<p class="cms-status">最新情報を読み込んでいます。</p>';

  try {
    const response = await fetch(url, {
      headers: {
        "X-MICROCMS-API-KEY": apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(createErrorMessage(response.status, url));
    }

    const data = await response.json();
    const contents = Array.isArray(data.contents) ? data.contents : [];

    if (contents.length === 0) {
      target.innerHTML = '<p class="cms-status">現在、公開中のお知らせはありません。</p>';
      return;
    }

    target.innerHTML = contents.map(createNewsCard).join("");
  } catch (error) {
    console.error(error);
    target.dataset.fallback = "true";
    target.innerHTML = `
      <p class="cms-status cms-status-error">
        ${escapeHtml(error.message || "最新情報を取得できませんでした。")}
      </p>
    `;
  }
}

function createErrorMessage(status, url) {
  if (status === 404) {
    return `microCMSのAPIが見つかりません。serviceDomain「${url.hostname.replace(".microcms.io", "")}」とendpoint「${url.pathname.replace("/api/v1/", "")}」を確認してください。`;
  }

  if (status === 401 || status === 403) {
    return "microCMSの認証に失敗しました。APIキーとGET権限を確認してください。";
  }

  return `microCMSから最新情報を取得できませんでした。HTTPステータス: ${status}`;
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
