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

  // ---- Section visibility tracking → GA4 ----
  // Fires `section_view` once per `<section id="...">` that becomes
  // visible (40%+ in viewport). Complements scroll_depth: tells the
  // team WHICH section the user saw, not just how far they scrolled.
  (function () {
    if (!("IntersectionObserver" in window)) return;
    var sections = document.querySelectorAll("section[id]");
    if (!sections.length) return;
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        if (seen[id]) return;
        seen[id] = true;
        try {
          gtag("event", "section_view", {
            section_id: id,
            page_path: window.location.pathname
          });
        } catch (e) {}
        io.unobserve(entry.target);
      });
    }, { threshold: 0.4 });
    sections.forEach(function (s) { io.observe(s); });
  })();

  // ---- Scroll depth tracking → GA4 ----
  // Fires `scroll_depth` events at 25/50/75/90% page scroll, once per
  // page session. Helps the analytics team see how far users read each
  // sub-page (engagement signal for long-form content like event.html).
  (function () {
    var milestones = [25, 50, 75, 90];
    var reached = {};
    var ticking = false;

    function check() {
      ticking = false;
      var doc = document.documentElement;
      var scrollTop = window.scrollY || doc.scrollTop;
      var docHeight = doc.scrollHeight - doc.clientHeight;
      if (docHeight <= 0) return;
      var pct = Math.min(100, Math.round((scrollTop / docHeight) * 100));
      milestones.forEach(function (m) {
        if (pct >= m && !reached[m]) {
          reached[m] = true;
          try {
            gtag("event", "scroll_depth", {
              percent: m,
              page_path: window.location.pathname
            });
          } catch (e) {}
        }
      });
    }

    addEventListener("scroll", function () {
      if (!ticking) {
        requestAnimationFrame(check);
        ticking = true;
      }
    }, { passive: true });
  })();

  // ---- Core Web Vitals tracking (LCP / FCP / CLS) → GA4 ----
  // Lightweight inline implementation — no external library. Sends each
  // metric once per page load, batched via the GA4 `web_vitals` event.
  // Use the Looker Studio dashboard to slice by page_path / device.
  (function () {
    if (typeof PerformanceObserver === "undefined") return;

    function sendVital(name, value, id) {
      try {
        gtag("event", "web_vitals", {
          metric_name: name,
          // GA4 only accepts numbers — keep millisecond precision for time,
          // 4 decimals for CLS (unitless score).
          metric_value: name === "CLS" ? Math.round(value * 10000) / 10000 : Math.round(value),
          metric_id: id || (name + "-" + Date.now()),
          page_path: window.location.pathname
        });
      } catch (e) {}
    }

    // Largest Contentful Paint — report the latest LCP at page hide.
    var lcpValue = 0;
    try {
      var lcpObserver = new PerformanceObserver(function (list) {
        var entries = list.getEntries();
        if (entries.length === 0) return;
        // The last entry is the most recent LCP candidate.
        lcpValue = entries[entries.length - 1].startTime;
      });
      lcpObserver.observe({ type: "largest-contentful-paint", buffered: true });
    } catch (e) {}

    // First Contentful Paint — fires once, can send immediately.
    try {
      new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          if (entry.name === "first-contentful-paint") {
            sendVital("FCP", entry.startTime);
          }
        });
      }).observe({ type: "paint", buffered: true });
    } catch (e) {}

    // Cumulative Layout Shift — accumulate excluding user-input shifts.
    var clsValue = 0;
    try {
      new PerformanceObserver(function (list) {
        list.getEntries().forEach(function (entry) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        });
      }).observe({ type: "layout-shift", buffered: true });
    } catch (e) {}

    // Flush LCP and CLS on visibility change (most reliable signal that the
    // user is leaving the page).
    var sent = false;
    function flush() {
      if (sent) return;
      sent = true;
      if (lcpValue > 0) sendVital("LCP", lcpValue);
      // CLS can legitimately be 0 — always report so Looker can graph it.
      sendVital("CLS", clsValue);
    }
    addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") flush();
    });
    // Fallback: also flush on pagehide in case visibilitychange didn't fire.
    addEventListener("pagehide", flush);
  })();

  // ---- Error monitoring (JS errors → GA4) ----
  // Dedup the same error message within a single session to avoid flooding.
  var reportedErrors = new Set ? new Set() : { has: function () { return false; }, add: function () {} };

  function reportError(payload) {
    var key = (payload.error_message || "") + "|" + (payload.error_source || "");
    if (reportedErrors.has && reportedErrors.has(key)) return;
    if (reportedErrors.add) reportedErrors.add(key);
    try {
      gtag("event", "js_error", payload);
    } catch (e) {}
  }

  window.addEventListener("error", function (e) {
    // Filter out resource load errors triggered for tracking pixels etc.
    var msg = (e && e.message) ? e.message : "unknown";
    var src = (e && e.filename) ? e.filename : "";
    // Skip cross-origin script errors with no info
    if (msg === "Script error." || msg === "Script error") return;
    reportError({
      error_message: String(msg).slice(0, 200),
      error_source: String(src).slice(0, 200),
      error_line: e && e.lineno ? e.lineno : 0,
      error_col: e && e.colno ? e.colno : 0,
      page_path: window.location.pathname,
      user_agent: navigator.userAgent.slice(0, 120)
    });
  });

  window.addEventListener("unhandledrejection", function (e) {
    var reason = (e && e.reason) ? (e.reason.message || String(e.reason)) : "unknown";
    reportError({
      error_message: ("[Promise] " + String(reason)).slice(0, 200),
      error_source: "unhandledrejection",
      page_path: window.location.pathname,
      user_agent: navigator.userAgent.slice(0, 120)
    });
  });
})();
