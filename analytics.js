// Google Analytics 4 setup + CTA click tracking.
// 1) Replace MEASUREMENT_ID below with your GA4 measurement ID (format: G-XXXXXXXXXX).
// 2) The script auto-loads gtag.js and tracks "cta_click" events on key links.
(function () {
  var MEASUREMENT_ID = "G-GWF9DQCZQ3"; // GA4 measurement ID

  if (!MEASUREMENT_ID || MEASUREMENT_ID.indexOf("XXXX") !== -1) {
    if (typeof console !== "undefined") {
      console.warn("[analytics] MEASUREMENT_IDが未設定です。analytics.jsを編集してください。");
    }
    return;
  }

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () {
    window.dataLayer.push(arguments);
  };
  gtag("js", new Date());
  gtag("config", MEASUREMENT_ID, {
    page_path: window.location.pathname,
    page_title: document.title
  });

  document.addEventListener("click", function (e) {
    var link = e.target.closest && e.target.closest("a");
    if (!link) return;

    var trackedSelector =
      ".button, .header-cta, .footer-policy, .footer-social a, " +
      ".footer-nav a, .nav a, .page-back, .brand, " +
      ".swell-block-button__link, .wp-block-file__button, .wp-block-button__link, " +
      ".info-card a, .contact-actions a, .support-actions a, " +
      "a[data-ga-cta]";
    if (!link.matches(trackedSelector)) return;

    var label = (link.dataset.gaCta || link.innerText || link.textContent || "").trim();
    if (label.length > 80) label = label.slice(0, 77) + "...";

    var dest = link.getAttribute("href") || "";
    var section =
      link.closest("section[id], header, footer, nav") || link.closest("section, header, footer, nav");
    var area = "unknown";
    if (section) {
      area =
        section.id ||
        (section.className && typeof section.className === "string"
          ? section.className.split(" ")[0]
          : "") ||
        section.tagName.toLowerCase();
    }

    var isExternal =
      /^https?:\/\//.test(dest) && dest.indexOf(window.location.hostname) === -1;
    var isAnchor = dest.charAt(0) === "#";
    var isPdf = /\.pdf(\?|$)/i.test(dest);
    var isMail = /^mailto:/i.test(dest);
    var isTel = /^tel:/i.test(dest);

    var type = "internal";
    if (isAnchor) type = "anchor";
    else if (isExternal) type = "external";
    else if (isPdf) type = "pdf";
    else if (isMail) type = "mail";
    else if (isTel) type = "tel";

    gtag("event", "cta_click", {
      cta_label: label,
      cta_destination: dest,
      cta_area: area,
      cta_type: type,
      page_path: window.location.pathname
    });
  });
})();
