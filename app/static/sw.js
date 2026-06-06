const CACHE_NAME = 'studyhub-static-v1';
const ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  // Pass non-GET requests straight to the network (e.g., forms, POST dispatches)
  if (event.request.method !== 'GET') {
    return;
  }
  
  // Always fetch from network first to ensure student views, quizzes, and notification counts are fresh.
  // Fall back to cache only when offline.
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        return caches.match(event.request);
      })
  );
});
