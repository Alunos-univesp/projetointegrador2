const CACHE_NAME = 'controle-validade-cache-v1';
const FILES_TO_CACHE = [
  '/',
  '/manifest.json',
  '/static/css/styles.css',             // Altere se usar outro nome ou caminho
  '/static/js/main.js',                // Altere se usar outro nome ou caminho
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/icons/icon-maskable.png'
];

// Instala o Service Worker e faz cache dos arquivos essenciais
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Cache inicial criado');
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// Ativação: remove caches antigos
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Ativando e limpando caches antigos...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Deletando cache antigo:', cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Intercepta fetch e responde com cache ou rede
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
