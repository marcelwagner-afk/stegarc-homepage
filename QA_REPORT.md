# STEGARC – Quality Assurance Report

| | |
|---|---|
| Branch | `feature/executive-optimization` |
| Date | 22 Nov 2026 |
| Test tool | `python3 tools/test_site.py` (Playwright) |

## Tested functionality (automated, all 22 pages)

| Check | Result |
|---|---|
| All internal links and anchors resolve (including blog → home anchors) | Pass |
| All images load and have an `alt` attribute | Pass |
| Exactly one `h1` per page | Pass |
| No console errors | Pass |
| No horizontal scrolling at 1440 and 390 px (all pages) | Pass |
| Home DE and EN: no horizontal scrolling at 1920, 1440, 1024, 768, 430, 390 and 375 px | Pass |
| Home DE and EN: no text, button or table reaching past the viewport at those widths | Pass |
| Navigation: every menu link scrolls to its section; scroll-spy marks it | Pass |
| Header state on scroll | Pass |
| Mobile menu: opens, closes with ESC, closes after a link click | Pass |
| Primary CTA leads to the contact section | Pass |
| Contextual CTAs: at least 5 `mailto:` links with a pre-filled subject per language | Pass |
| `mailto:` and `tel:` present in contact | Pass |
| Keyboard: skip link is the first focus target; visible focus ring | Pass |
| `prefers-reduced-motion: reduce`: no hidden content | Pass |
| Scroll-reveal: all elements visible after scrolling | Pass |

Result: 22 pages, 0 errors.

## Visual review

Screenshots were reviewed at 1440 px and at 390 px for the full DE home page and the EN home page.

Fixed during review:
- At 390 px the hero headline overflowed; the font size is now adjusted.
- On mobile the outcome table had a narrow first column; it now stacks.

## Lighthouse 12 (Chromium, local server, 22 Nov 2026)

| Page | Performance | Accessibility | Best practices | SEO | LCP | CLS |
|---|---|---|---|---|---|---|
| Home DE, mobile | 98 | 100 | 100 | 100 | 2.2 s | 0 |
| Home DE, desktop | 100 | 100 | 100 | 100 | 0.6 s | 0 |
| Home EN, mobile | 98 | 100 | 100 | 100 | 2.2 s | 0 |
| Home EN, desktop | 100 | 100 | 100 | 100 | 0.6 s | 0 |
| Impressum, mobile | 99 | 100 | 100 | 100 | 1.8 s | 0 |
| Impressum, desktop | 100 | 100 | 100 | 100 | 0.4 s | 0 |
| Blog index EN, before fix (mobile / desktop) | 99 / 100 | 98 | 100 | 100 | – | – |
| Blog index EN, after fix | – | 100 | – | – | – | – |

The blog index finding was a heading-order issue (`h1` → `h3`), now fixed with a visually hidden `h2`.

All targets are met: Performance ≥ 95, Accessibility 100, Best Practices 100, SEO 100. Mobile figures use Lighthouse's simulated slow 4G; the live site on GitHub Pages may vary by a few points.

## Accessibility findings

- Semantic structure: one `h1`, sections with `aria-labelledby`, a table with `th scope`.
- On mobile the table becomes stacked cards, labelled via `data-l`.
- Decorative images carry `alt=""` and `aria-hidden`; informative images have descriptive alt text.
- Colour contrast: teal text uses `#007A75` on light backgrounds (WCAG AA).
- Status badges are text, not colour only.
- Motion only with `prefers-reduced-motion: no-preference`.

## Known limitations

- **Browsers:** only Chromium is available in this environment. Firefox and WebKit/Safari were **not** tested. The code uses no browser-specific features beyond widely supported CSS (grid, clamp, mask-image with `-webkit-` prefix).
- **Real devices:** not tested on real devices; device emulation only.
- **Contact:** contact works via `mailto:` and `tel:`. Whether an e-mail actually arrives depends on the visitor's mail client and was not tested.
- **Live site:** the measurements above are from a local server, not from GitHub Pages.

## Remaining issues

None blocking. Content recommendations are listed in `OPTIMIZATION_REPORT.md`, section 8.
