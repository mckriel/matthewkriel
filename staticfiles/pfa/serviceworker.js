const CACHE_NAME = 'V1.2.0';
const CACHE_URLS = [
    '/',
    '/pfa',
    '/pfa/',
    '/static/pfa/style.css',
    '/static/pfa/manifest.json',
    '/static/pfa/pfa-app-logo.png',
    '/static/pfa/pfa-logo.png',
    '/static/pfa/pfa-splash.png',
    '/static/pfa/script.js'
];

self.addEventListener('install', (event) => {
    event.waitUntil(preLoad());
});

const preLoad = async () => {
    console.log('Installing web app');
    const cache = await caches.open(CACHE_NAME);
    console.log('Caching index and important routes');
    await cache.addAll(CACHE_URLS);
};

self.addEventListener('fetch', (event) => {
    event.respondWith(checkResponse(event.request));
    event.waitUntil(addToCache(event.request));
});

const checkResponse = async (request) => {
    try {
        const response = await fetch(request);
        if (response.status === 404) {
            throw new Error('Not found');
        }
        return response;
    } catch (error) {
        return returnFromCache(request);
    }
};

const addToCache = async (request) => {
    const cache = await caches.open(CACHE_NAME);
    const response = await fetch(request);
    if (response.status === 200) {
        console.log(`${response.url} was cached`);
        await cache.put(request, response.clone());
    }
};

const returnFromCache = async (request) => {
    const cache = await caches.open(CACHE_NAME);
    const matching = await cache.match(request);
    if (!matching || matching.status === 404) {
        return cache.match('pfa/index.html');
    }
    return matching;
};

self.addEventListener('activate', (event) => {
    event.waitUntil(cleanupOldCaches());
});

const cleanupOldCaches = async () => {
    const cacheNames = await caches.keys();
    const oldCaches = cacheNames.filter(name => name !== CACHE_NAME);
    return Promise.all(oldCaches.map(cache => caches.delete(cache)));
};
