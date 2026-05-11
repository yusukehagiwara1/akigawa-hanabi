// Service Worker — basic offline support + stale-while-revalidate caching.
// Bump CACHE_VERSION on each deploy that ships static asset changes.
const CACHE_VERSION = "akigawa-hanabi-v1";
const PRECACHE_URLS = [
  "/",
  "/index.html",
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
  "/assets/keyvisual.jpg",
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches
      .open(CACHE_VERSION)
      .then(function (cache) {
        // Pre-cache critical resources, but don't fail install if some are missing
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

self.addEventListener("fetch", function (event) {
  const req = event.request;
  // Only handle GET
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  // Skip cross-origin (microCMS, Google Forms, analytics, fonts)
  if (url.origin !== self.location.origin) return;
  // Don't cache analytics / sitemap / robots
  if (
    url.pathname.indexOf("/_") === 0 ||
    url.pathname.indexOf("sitemap") !== -1 ||
    url.pathname.indexOf("robots") !== -1
  ) {
    return;
  }

  event.respondWith(
    caches.match(req).then(function (cached) {
      const fetchPromise = fetch(req)
        .then(function (response) {
          // Only cache OK responses
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_VERSION).then(function (cache) {
              cache.put(req, responseClone).catch(function () {});
            });
          }
          return response;
        })
        .catch(function () {
          // Network failed; return cached if available
          if (cached) return cached;
          throw new Error("offline");
        });

      // Stale-while-revalidate: return cached immediately, update in background
      return cached || fetchPromise;
    })
  );
});
