// Google Analytics 4 setup + CTA click tracking.
// - Fires a generic `cta_click` event on every tracked link.
// - Fires dedicated conversion-style events for high-value clicks:
//     ticket_purchase_click  - KKday / asoview ticket reservation links
//     donation_click         - Donation form (Google Forms) + PDF requests
//     sponsor_click          - Sponsor form / sponsorship section CTA
//     furusato_click         - Furusato tax (satofull) link
//     sns_click              - Instagram / other social media links
//     sponsor_logo_click     - Sponsor company logo click-through
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

  // Donation form URL (Google Forms — separate ID from contact form)
  var DONATION_FORM_ID = "1FAIpQLSddeuL3e6SDr6FR1lnZyIxzXjp7xa8jFeddjWcKGvWrxDKoBA";

  // Detect a high-value conversion category for the click.
  // Returns the dedicated event name or null if no dedicated event applies.
  function classifyConversion(dest, label, link) {
    if (!dest) return null;
    // Ticket purchase: KKday and asoview
    if (/(?:kkday\.com|asoview\.com|urakata\.app)/i.test(dest)) {
      return { event: "ticket_purchase_click", provider: /kkday/i.test(dest) ? "kkday" : "asoview" };
    }
    // Furusato tax: satofull
    if (/satofull\.jp/i.test(dest)) {
      return { event: "furusato_click", provider: "satofull" };
    }
    // Donation form (Google Forms — donation form ID)
    if (dest.indexOf(DONATION_FORM_ID) !== -1) {
      // Distinguish 寄付 vs 協賛 by label / context
      var section = link.closest("[id]");
      var sectionId = section ? section.id : "";
      var isSponsor = /協賛|sponsor|10万/.test(label) || sectionId === "02";
      return {
        event: isSponsor ? "sponsor_click" : "donation_click",
        provider: "google_forms"
      };
    }
    // Donation PDF requests
    if (/寄付依頼書|donation/i.test(dest) || /寄付依頼書|寄付.*PDF/.test(label)) {
      if (/\.pdf/i.test(dest)) {
        return { event: "donation_click", provider: "pdf" };
      }
    }
    if (/協賛依頼書/i.test(dest) || /協賛.*PDF/.test(label)) {
      if (/\.pdf/i.test(dest)) {
        return { event: "sponsor_click", provider: "pdf" };
      }
    }
    // Support band on homepage (寄付 1万円から / 企業協賛 10万円から)
    if (
      link.closest && link.closest(".support-actions") &&
      /donation\.html/i.test(dest)
    ) {
      var isSponsor2 = /協賛|10万/.test(label) || /donation\.html#02/.test(dest);
      return {
        event: isSponsor2 ? "sponsor_click" : "donation_click",
        provider: "homepage_band"
      };
    }
    // Instagram + other SNS
    if (/instagram\.com/i.test(dest)) {
      return { event: "sns_click", provider: "instagram" };
    }
    if (/twitter\.com|x\.com|facebook\.com|line\.me|youtube\.com/i.test(dest)) {
      var prov = /twitter|x\.com/i.test(dest) ? "twitter" :
                 /facebook/i.test(dest) ? "facebook" :
                 /line\.me/i.test(dest) ? "line" : "youtube";
      return { event: "sns_click", provider: prov };
    }
    // Sponsor company logo clicks (added by sponsor-urls.js with data-ga-cta="sponsor:...")
    if ((link.dataset && link.dataset.gaCta || "").indexOf("sponsor:") === 0) {
      return {
        event: "sponsor_logo_click",
        provider: (link.dataset.gaCta.split(":")[1] || "").trim() || "unknown"
      };
    }
    return null;
  }

  document.addEventListener("click", function (e) {
    var link = e.target.closest && e.target.closest("a");
    if (!link) return;

    var trackedSelector =
      ".button, .header-cta, .footer-policy, .footer-social a, " +
      ".footer-nav a, .nav a, .page-back, .brand, " +
      ".swell-block-button__link, .wp-block-file__button, .wp-block-button__link, " +
      ".info-card a, .contact-actions a, .support-actions a, " +
      ".donation-cta-button, .donation-pdf-button, .contact-cta-button, " +
      ".ticket-card, .past-tile, " +
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

    // Common cta_click event (broad tracking for all key links)
    gtag("event", "cta_click", {
      cta_label: label,
      cta_destination: dest,
      cta_area: area,
      cta_type: type,
      page_path: window.location.pathname
    });

    // Dedicated conversion event for high-value categories
    var conversion = classifyConversion(dest, label, link);
    if (conversion) {
      gtag("event", conversion.event, {
        provider: conversion.provider,
        cta_label: label,
        cta_destination: dest,
        cta_area: area,
        page_path: window.location.pathname
      });
    }
  });
})();
