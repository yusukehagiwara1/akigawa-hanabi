// Sponsor logo → URL mapping. Scans <img> elements within sponsor sections
// and wraps them with anchors so logos are clickable.
//
// To add or edit URLs: insert/modify entries in SPONSOR_URL_MAP. The key is a
// substring of the image src; the first match wins. Add accurate URLs here.

(function () {
  const SPONSOR_URL_MAP = {
    // --- 特別協力 ---
    "サマーランド": "https://www.summerland.co.jp/",
    "summerland": "https://www.summerland.co.jp/",
    "イオン": "https://www.aeon.jp/sc/hinode/",
    "aeon": "https://www.aeon.jp/sc/hinode/",

    // --- ゴールドスポンサー ---
    "ヒューマンテクノス": "https://www.humantec.co.jp/",
    "humantech": "https://www.humantec.co.jp/",
    "シーウイング": "https://www.sea-wing.jp/",
    "ゼンコー": "https://www.zenko-group.co.jp/",
    "立花工業": "https://tachibana-kougyou.com/",
    "tachibana": "https://tachibana-kougyou.com/",
    "内田電気": "http://uchidadenki.net/",
    "uchida": "http://uchidadenki.net/",

    // --- シルバー以下 ---
    "森電気": "https://mks-moridenki.com/",
    "mori": "https://mks-moridenki.com/",
    "シンヨー": "https://www.sinyo.com/",
    "ジュン企画": "https://junkikaku.jp/",
    "jun": "https://junkikaku.jp/",
    "カネショウ": "https://kanesho.info/",
    "kyowa": "http://www.j-kyowa.com/",
    "KYOWA": "http://www.j-kyowa.com/",
    "2-2-1024x341": "http://www.j-kyowa.com/", // 協和 (KYOWA) corporation logo
    // YANAGI と GA-1 (GOAHEAD) は公式 URL 未確定のためリンク無し
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
