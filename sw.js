// Service Worker — offline-friendly caching for static assets.
// Strategy:
//   * Navigation (HTML page) requests → network-first, fall back to cached HTML.
//     Why: HTML must always be fresh after a deploy. Stale-while-revalidate on
//     navigation caused ERR_FAILED in some browsers when the cached response
//     became incompatible with a navigation request (e.g. cached redirect).
//   * Static asset GET requests → stale-while-revalidate (fast + auto refresh).
//   * Cross-origin requests, non-GET, sitemap/robots, /_routes/* → pass through.
//
// Bump CACHE_VERSION on each deploy that ships static asset changes.
const CACHE_VERSION = "akigawa-hanabi-v17";
const PRECACHE_URLS = [
  "/styles.css",
  "/ui.js",
  "/script.js",
  "/microcms-config.js",
  "/microcms-extras.js",
  "/sponsor-urls.js",
  "/analytics.js",
  "/manifest.json",
  "/assets/favicon.ico",
  "/assets/logo-npo.webp",
  "/assets/hero-fireworks-real.webp",
  "/assets/hero-fireworks-real-1280.webp",
  "/assets/hero-fireworks-real-800.webp",
  "/assets/keyvisual.jpg",
  "/assets/ogp-2026.jpg",
  "/assets/icon-192.png",
  "/assets/icon-512.png",
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches
      .open(CACHE_VERSION)
      .then(function (cache) {
        // Pre-cache critical assets, but don't fail install if some are missing
        return Promise.all(
          PRECACHE_URLS.map(function (url) {
            return cache.add(url).catch(function () { return null; });
          })
        );
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches
      .keys()
      .then(function (keys) {
        return Promise.all(
          keys
            .filter(function (key) {
              return key !== CACHE_VERSION;
            })
            .map(function (key) {
              return caches.delete(key);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

function isAssetRequest(url) {
  return /\.(?:css|js|mjs|webp|jpg|jpeg|png|svg|gif|ico|woff2?|ttf|otf|json)$/i.test(
    url.pathname
  );
}

self.addEventListener("fetch", function (event) {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  // Skip cross-origin (microCMS, Google Forms, Google Analytics, fonts, etc.)
  if (url.origin !== self.location.origin) return;
  // Don't cache analytics / sitemap / robots / Cloudflare runtime routes
  if (
    url.pathname.indexOf("/_") === 0 ||
    url.pathname.indexOf("sitemap") !== -1 ||
    url.pathname.indexOf("robots") !== -1
  ) {
    return;
  }

  // --- Navigation (HTML page) requests → network-first ---
  if (req.mode === "navigate" || (req.headers.get("accept") || "").indexOf("text/html") !== -1) {
    event.respondWith(
      fetch(req)
        .then(function (response) {
          // Only cache successful, non-redirected, basic responses
          if (response && response.ok && response.type === "basic" && !response.redirected) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then(function (cache) {
              cache.put(req, clone).catch(function () {});
            });
          }
          return response;
        })
        .catch(function () {
          // Network failed → try cache
          return caches.match(req).then(function (cached) {
            if (cached) return cached;
            // Last-resort fallback: cached homepage if available
            return caches.match("/index.html");
          });
        })
    );
    return;
  }

  // --- Asset requests → stale-while-revalidate ---
  if (!isAssetRequest(url)) return; // let the browser handle anything unknown

  event.respondWith(
    caches.match(req).then(function (cached) {
      const networkFetch = fetch(req)
        .then(function (response) {
          if (response && response.ok && response.type === "basic" && !response.redirected) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then(function (cache) {
              cache.put(req, clone).catch(function () {});
            });
          }
          return response;
        })
        .catch(function () {
          return cached; // network failed; if we have a cache, keep using it
        });
      return cached || networkFetch;
    })
  );
});
