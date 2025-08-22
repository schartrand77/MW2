import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, NetworkFirst } from 'workbox-strategies';
import { Queue } from 'workbox-background-sync';

// @ts-ignore
precacheAndRoute(self.__WB_MANIFEST);

registerRoute(
  ({ request }) => request.mode === 'navigate',
  new StaleWhileRevalidate({ cacheName: 'pages' })
);

registerRoute(
  ({ url, request }) => url.pathname.startsWith('/api') && request.method === 'GET',
  new NetworkFirst({ cacheName: 'api-get' })
);

const bgQueue = new Queue('api-post');

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method === 'POST' && new URL(request.url).pathname.startsWith('/api')) {
    event.respondWith(
      fetch(request.clone()).catch(async () => {
        await bgQueue.pushRequest({ request });
        return new Response(null, { status: 503 });
      })
    );
  }
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'api-post') {
    event.waitUntil(bgQueue.replayRequests());
  }
});
