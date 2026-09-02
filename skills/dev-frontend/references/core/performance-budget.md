# Performance Budget

## Core Web Vitals Targets

| Metric | Good | Needs Work | Poor | Measures |
|--------|------|------------|------|----------|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s | Hero load time |
| INP | ≤ 200ms | ≤ 500ms | > 500ms | Input responsiveness |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 | Visual stability |

- Every page targets "Good" on all three
- LCP element: identify early, preload it
- INP: never block main thread > 50ms
- CLS: every image/video/embed needs explicit `width`+`height` or `aspect-ratio`

## Bundle Size Budgets

| Resource | Budget (compressed) |
|----------|-------------------|
| Total page weight | ≤ 500KB first load |
| JavaScript (per route) | ≤ 150KB |
| CSS (total) | ≤ 50KB |
| Hero image | ≤ 100KB |
| Images (above fold) | ≤ 200KB |
| Web fonts | ≤ 100KB |

- Measure compressed (gzip/brotli) sizes
- Tree-shake: `import { x } from 'lib'`, never `import lib`
- Dynamic import for below-fold: `lazy(() => import('./Modal'))`
- Bundle analyzer mandatory for builds > 200KB JS

## Font Loading

```html
<link rel="preload" href="/fonts/primary.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Primary';
  src: url('/fonts/primary.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0020-007F, U+AC00-D7AF;
}
```

- `font-display: swap` for body, `optional` for decorative
- Preload only the primary font file
- Subset: Latin + target script only
- Max 2 families, 4 weights total
- Self-host when possible

## Image Optimization

| Format | Use For | Quality |
|--------|---------|---------|
| WebP | Photos, complex | 75-85% |
| AVIF | Photos (modern) | 65-75% |
| SVG | Icons, logos | N/A |
| PNG | Screenshots, transparency | Lossless |

- `<picture>` with AVIF → WebP → fallback for hero
- `loading="lazy"` below-fold, `loading="eager" fetchpriority="high"` for hero
- Max 2x display size for retina
- Responsive `srcset` + `sizes` for content images

## Build-Time Gates

- Lighthouse Performance ≥ 90
- Bundle regression: fail if JS increases > 10KB
- Image audit: flag > 200KB
- Unused CSS: flag > 5KB dead CSS

## Runtime Rules

- No `querySelectorAll` in scroll/resize handlers
- Debounce scroll: 100ms min, `requestAnimationFrame` for visual
- Intersection Observer for lazy loading
- `content-visibility: auto` on below-fold sections

## Pre-flight

- [ ] Hero image ≤ 100KB, `fetchpriority="high"`, explicit dimensions
- [ ] Below-fold images have `loading="lazy"`
- [ ] No JS bundle > 150KB compressed
- [ ] `font-display: swap` + `preload` on primary font
- [ ] Every `<img>`/`<video>` has `width`+`height`
- [ ] Lighthouse Performance ≥ 90

## Browser Connection Budgets (moved from SKILL.md §6, 2026-07-02)

| Protocol | Limit |
|---|---|
| HTTP/1.1 | 6 connections per domain (Chrome/Firefox) |
| HTTP/2 | 1 TCP connection, ~100 concurrent streams |
| WebSocket | Shares the HTTP/1.1 connection pool |

Rules: never open >2 SSE/WebSocket connections to the same origin from one page; use
connection multiplexing (single WebSocket with channel/topic routing); if >6 parallel
requests needed use HTTP/2, batched endpoints, or domain sharding (last resort);
preflight OPTIONS counts against the limit — consolidate CORS-heavy calls.
Banned: unbounded per-component WebSockets; independent polling from multiple components
(centralize into one subscription, fan out via state); SSE re-created on every remount
without cleanup. Ownership: browser-side budgets live here (dev-frontend); server-side
connection lifecycle (heartbeats, drain, registry) is `dev-backend` §1.

## Motion Media Budget Exemption (FE-MEDIA-BUDGET-01, DEFAULT)

On LANDING/EXPERIENCE-bucket surfaces (see `motion.md` FE-MOTION-BUCKET-01), motion
media is exempt from the byte-cap rows above with no byte ceiling: autoplay loop
video, scroll-scrub video, frame sequences, and large hero imagery.

**Budget freedom is not correctness freedom.** The Core Web Vitals field gates remain
supreme — LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 — and the exemption applies only when
the loading mechanics hold:

- Poster-first LCP; the poster itself counts toward the hero image budget.
- Lazy or Intersection Observer-gated loading outside first paint.
- `prefers-reduced-motion` and `prefers-reduced-data` fallbacks to poster or still.
- Stable layout; no CLS from the media swap.
- The still is useful before the heavy media arrives.
- An explicit skip or pause control for authored playback.
- Adaptive quality selected from device, network, and reduced-data capability.
- Primary copy and the primary CTA are never blocked on media readiness.
- **Measured** LCP meets the field gate — do not infer it from asset size.
- **Measured** interaction cost meets the INP field gate during choreography.

The two "measured" lines are the ones that make this an exemption rather than a
loophole. Byte size was the proxy; once you drop the proxy you owe the real
measurement, and inferring LCP from how big the file is is how a page ships heavy
media and a failing field gate at the same time.

Heavy media still needs a product reason on top of the mechanics above.
