// Sponsor logo → URL mapping. Scans <img> elements within sponsor sections
// and wraps them with anchors so logos are clickable.
//
// To add or edit URLs: insert/modify entries in SPONSOR_URL_MAP. The key is a
// substring of the image src; the first match wins. Add accurate URLs here.

(function () {
  // URLs verified as accessible (2026-05-11). Sites that returned 404, expired
  // certificates, or pointed at a different company are intentionally excluded.
  const SPONSOR_URL_MAP = {
    // --- 特別協力 ---
    "サマーランド": "https://www.summerland.co.jp/",
    "summerland": "https://www.summerland.co.jp/",
    "イオン": "https://hinode-aeonmall.com/",
    "aeon": "https://hinode-aeonmall.com/",

    // --- ゴールドスポンサー ---
    "ヒューマンテクノス": "https://www.humantechnos.com/",
    "humantech": "https://www.humantechnos.com/",
    "シーウイング": "https://www.sea-wing.jp/",
    "ゼンコー": "https://www.zenko-group.co.jp/",
    "立花工業": "https://tachibana-kougyou.com/",
    "tachibana": "https://tachibana-kougyou.com/",

    // --- シルバー以下 ---
    "森電気": "https://mks-moridenki.com/",
    "mori": "https://mks-moridenki.com/",
    "シンヨー": "https://www.sinyo.com/",
    "ジュン企画": "https://junkikaku.jp/",
    "jun": "https://junkikaku.jp/",
    "カネショウ": "https://kanesho.info/",

    // --- 未リンク（404 / 証明書エラー / 公式URL未確定） ---
    // "内田電気": uchidadenki.net は証明書期限切れのためリンク無し
    // "協和 (KYOWA)": j-kyowa.com は TLS証明書エラーのためリンク無し
    // "YANAGI" / "GA-1 (GOAHEAD)": 公式 URL 未確定のためリンク無し
  };

  function findUrl(src) {
    if (!src) return null;
    for (const key in SPONSOR_URL_MAP) {
      if (src.indexOf(key) !== -1) return SPONSOR_URL_MAP[key];
    }
    return null;
  }

  function wrapLogo(img) {
    if (!img || img.parentElement && img.parentElement.tagName === "A") return;
    const url = findUrl(img.getAttribute("src") || "");
    if (!url) return;
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener";
    link.setAttribute("data-ga-cta", "sponsor:" + (img.alt || ""));
    img.parentNode.insertBefore(link, img);
    link.appendChild(img);
  }

  function run() {
    // Homepage sponsor tiles (static fallback + CMS-rendered)
    document
      .querySelectorAll(".sponsor-tile > img, .sponsor-tile > a > img")
      .forEach(wrapLogo);

    // Sponsor sub-page: WP-migrated logos in columns
    document
      .querySelectorAll(".prose .wp-block-columns figure.wp-block-image > img")
      .forEach(wrapLogo);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }

  // Re-run after microCMS replaces sponsor-tile content (delayed)
  setTimeout(run, 1500);
  setTimeout(run, 3500);
})();
