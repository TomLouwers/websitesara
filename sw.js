/**
 * Service Worker for OefenPlatform
 *
 * Features:
 * - Cache static assets for offline use
 * - Cache-first strategy for performance
 * - Automatic cache versioning
 * - Intelligent cache management
 *
 * @version 1.0.0
 * @date 2026-01-07
 */

const CACHE_VERSION = 'sara-v1.0.1-phase1';
const CACHE_NAME = `sara-exercises-${CACHE_VERSION}`;

// Static assets to cache on install
const STATIC_ASSETS = [
  'index.html',
  'quiz.html',
  'level-selector.html',

  // CSS
  'static/css/styles.min.css',
  'static/css/rewards.css',
  'static/css/gamification.css',
  'static/css/verhoudingstabel-widget.min.css',

  // JavaScript - Core
  'static/js/app.min.js',
  'static/js/config.min.js',
  'static/js/utils.min.js',

  // JavaScript - Features
  // (using source files for gamification; no minified bundle present)
  'static/src/gamification.js',
  'static/src/gamification-ui.js',
  'static/js/session-rewards.min.js',
  'static/js/card-morph-feedback.min.js',
  'static/js/accessibility.min.js',
  'static/js/streak-animations.min.js',

  // Fonts (Google Fonts - will be cached when loaded)
  'https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap',
  'https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap',
  'https://fonts.googleapis.com/icon?family=Material+Icons&display=swap'
];

// Exercise files to cache (most commonly used)
const EXERCISE_CACHE = [
  'data-v2/exercises/bl/bl_groep4_m4_1_core.json',
  'data-v2/exercises/bl/bl_groep4_m4_1_support.json',
  'data-v2/exercises/gb/gb_groep4_m4_core.json',
  'data-v2/exercises/gb/gb_groep4_m4_support.json'
];

// ============================================================================
// INSTALL EVENT - Cache static assets
// ============================================================================
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...', CACHE_NAME);

  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching static assets');

        // Cache static assets
        return cache.addAll(STATIC_ASSETS)
          .then(() => {
            console.log('[Service Worker] Static assets cached');

            // Cache exercise files (non-blocking)
            return cache.addAll(EXERCISE_CACHE).catch((err) => {
              console.warn('[Service Worker] Some exercise files failed to cache:', err);
              // Don't fail the install if exercise caching fails
            });
          });
      })
      .then(() => {
        console.log('[Service Worker] Install complete');
        // Skip waiting to activate immediately
        return self.skipWaiting();
      })
      .catch((err) => {
        console.error('[Service Worker] Install failed:', err);
      })
  );
});

// ============================================================================
// ACTIVATE EVENT - Clean up old caches
// ============================================================================
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...', CACHE_NAME);

  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => {
              // Delete old cache versions
              return name.startsWith('sara-exercises-') && name !== CACHE_NAME;
            })
            .map((name) => {
              console.log('[Service Worker] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[Service Worker] Activation complete');
        // Take control of all pages immediately
        return self.clients.claim();
      })
  );
});

// ============================================================================
// FETCH EVENT - Serve from cache with network fallback
// ============================================================================
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip cross-origin requests (except Google Fonts)
  if (url.origin !== location.origin && !url.origin.includes('googleapis.com')) {
    return;
  }

  // Different strategies for different resource types
  if (request.url.includes('/data-v2/exercises/')) {
    // Exercise files: Cache-first (fast), network fallback
    event.respondWith(cacheFirstStrategy(request));
  } else if (request.url.endsWith('.json')) {
    // Other JSON: Network-first (fresh data), cache fallback
    event.respondWith(networkFirstStrategy(request));
  } else {
    // Static assets: Cache-first (performance)
    event.respondWith(cacheFirstStrategy(request));
  }
});

/**
 * Cache-first strategy: Check cache first, fallback to network
 * Best for: Static assets, exercise files
 */
async function cacheFirstStrategy(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);

    if (cached) {
      console.log('[Service Worker] Serving from cache:', request.url);
      return cached;
    }

    // Not in cache, fetch from network
    console.log('[Service Worker] Fetching from network:', request.url);
    const response = await fetch(request);

    // Cache successful responses
    if (response.ok) {
      cache.put(request, response.clone());
    }

    return response;
  } catch (err) {
    console.error('[Service Worker] Fetch failed:', err);

    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      return caches.match('/index.html');
    }

    throw err;
  }
}

/**
 * Network-first strategy: Try network first, fallback to cache
 * Best for: Dynamic content, API calls
 */
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);

    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }

    return response;
  } catch (err) {
    console.warn('[Service Worker] Network failed, trying cache:', request.url);

    // Network failed, try cache
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }

    throw err;
  }
}

// ============================================================================
// MESSAGE EVENT - Handle messages from app
// ============================================================================
self.addEventListener('message', (event) => {
  console.log('[Service Worker] Message received:', event.data);

  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }

  // Cache specific exercise on demand
  if (event.data.type === 'CACHE_EXERCISE') {
    const exerciseUrl = event.data.url;
    caches.open(CACHE_NAME).then((cache) => {
      cache.add(exerciseUrl);
      console.log('[Service Worker] Cached exercise on demand:', exerciseUrl);
    });
  }

  // Clear all caches (for debugging)
  if (event.data.type === 'CLEAR_CACHE') {
    caches.keys().then((names) => {
      names.forEach((name) => caches.delete(name));
      console.log('[Service Worker] All caches cleared');
    });
  }
});

// ============================================================================
// BACKGROUND SYNC (Future enhancement)
// ============================================================================
// Uncomment when ready to implement background sync for stats
/*
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-stats') {
    event.waitUntil(syncStats());
  }
});

async function syncStats() {
  // Sync gamification stats to backend when online
  console.log('[Service Worker] Syncing stats...');
}
*/

console.log('[Service Worker] Loaded successfully');
