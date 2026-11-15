// Bump CACHE when the file list changes. Pages use network-first, so code
// fixes reach installed phones on the next online launch without a bump.
const CACHE = "interest-calculator-v6";
const FILES = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;

  // Network first: fresh copy when online, cached copy when offline.
  // cache: "no-cache" makes the browser check the server every time instead of
  // reusing its own HTTP cache (servers like python http.server send no
  // Cache-Control, so the browser would otherwise guess and serve old files).
  event.respondWith(
    fetch(req.url, { cache: "no-cache", credentials: "same-origin" })
      .then(res => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(cache => cache.put(req, copy));
        }
        return res;
      })
      .catch(() => caches.match(req, { ignoreSearch: true })
        .then(hit => hit || (req.mode === "navigate" ? caches.match("./index.html") : undefined)))
  );
});
