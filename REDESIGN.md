# STEGARC Premium-Redesign

Branch: `feature/apple-inspired-premium-redesign`. Die Produktivversion (`main`) bleibt unverändert, bis Marcel Wagner die Veröffentlichung ausdrücklich freigibt.

## 1. Ausgangslage

- Statische Website, erzeugt mit `build.py` aus `content/<sprache>/…`. Die Startseiten kommen aus `tools/make_home.py`.
- Zwei Sprachen (DE und EN) mit hreflang, Sitemap, JSON-LD (ProfessionalService, BlogPosting, BreadcrumbList, FAQPage), 7 Blogbeiträge je Sprache, Impressum und Datenschutz.
- Vorheriges Design: Teal-Variante (main, Commit 98944c2) mit prozedural erzeugten Grafiken.

## 2. Referenz

Die Designvorlage (Light und Dark) ist verbindlich:
- Die helle Variante ist das Hauptdesign für Beratung, Leistungen, Projekte und Über mich.
- Die dunkle Variante gilt für STEGARC Technology, KI und Kontakt.

Bildmaterial kommt aus dem Ordner `stegarc_design_assets_pro`. Alle Motive stammen aus der STEGARC-Bildwelt; Stockfotos werden nicht verwendet.

## 3. Designsystem (`assets/style.css`)

| Token | Wert |
|---|---|
| Navy | `#07152B` |
| Hintergrund | `#F8F9FA` |
| Teal | `#00B8B0`; als Textfarbe auf Hell `#007A75` für den Kontrast nach WCAG AA |
| Text / Sekundär / Linie | `#111827` / `#64748B` / `#E5E7EB` |
| Dark Surface | `#0D2035` |
| Schrift | Inter 400/500/600/700, lokal ausgeliefert (OFL) |
| H1 / H2 / H3 / Body / Nav | `clamp()` von 40→72, 32→48, 23→28, 16→18 und 15 px |
| Breite | max. 1440 px, Abstände `--s1`–`--s8`, Radien, Schatten, Easing als Tokens |

## 4. Struktur der Startseite

| Nr. | Sektion | Variante | Anker |
|---|---|---|---|
| 1 | Hero „Wo andere Nein sagen, fange ich an.“ mit Bild `hero-enterprise` | hell | – |
| 2 | Praxis: Laptop mit HTML-Status-Mock und Karte „ERP-Transformation in der Praxis.“ | hell | – |
| 3 | Leistungen: 6 Karten mit `svc-*`-Bildern, dazu ergänzende Schwerpunkte und eine „Außerdem“-Zeile | hell | `#leistungen` |
| 4 | STEGARC Technology „Eine Plattform. Alle Systeme. Volle Kontrolle.“ mit dem echten Demo-Screenshot | dunkel | `#plattform` |
| 5 | KI mit Bild `ki-chip` und Freigabe-Beispiel | dunkel | `#ki` |
| 6 | Sonderlösungen | hell | – |
| 7 | Vorgehen | hell | – |
| 8 | Projekte | hell | – |
| 9 | Über mich | hell | – |
| 10 | Blog | hell | – |
| 11 | FAQ | hell | – |
| 12 | Kontakt | dunkel | – |

Interaktionen:
- Sticky-Navigation, die beim Scrollen den Hintergrund wechselt.
- Scrollspy über `aria-current`.
- Zugängliches Mobilmenü: `aria-expanded`, ESC schließt, Fokus wird geführt.
- Reveal beim Scrollen, Hover auf Karten, Übergänge an Buttons.
- Alle Animationen nur bei `prefers-reduced-motion: no-preference`.

## 5. Verschobene oder zusammengeführte Inhalte

Es wurde nichts gelöscht.
- Lizenzoptimierung, HR/SuccessFactors sowie Programmleitung und PE stehen jetzt in der Zeile „Außerdem“ unter den Leistungskarten.
- Das frühere Band „Komplexe Vorhaben“ ist in die Überschrift der Projektsektion eingeflossen.
- Die Kurztexte der Leistungskarten folgen dem Masterprompt. Die ausführlichen Texte bleiben in `make_home.py` (`svc`) erhalten.
- Auf Unterseiten verweisen die Navigationslinks jetzt auf die Startseite (`./#leistungen`). Vorher führten die Anker dort ins Leere.

## 6. Bilder (`assets/photo`)

- Ausschnitte aus der STEGARC-Bildwelt, je als WebP mit JPEG-Fallback, mit festen `width`/`height`.
- Alle Bilder außer dem Hero werden per Lazy Loading geladen.
- Dekorative Bilder haben `alt=""` und `aria-hidden`.

Bekannte Einschränkungen:
- Die gelieferten Dateien sind klein (Hero 741×268 px). Auf großen und Retina-Displays wirkt der Hero deshalb weich. Für die Veröffentlichung sollten größere Einzelrenderings her, mindestens 2400 px breit für Hero und Technology.
- Die Service-Bilder enthalten das Symbol bereits. Deshalb gibt es kein zusätzliches HTML-Icon.
- `dashboard-laptop` und `beratung` sind vorbereitet, aber nicht eingebunden:
  - Im Dashboard-Bild ist die Oberfläche unleserlich. Die HTML-Version bleibt deshalb lesbar und barrierefrei.
  - Die Beratungsszene zeigt eine KI-generierte Person, die Besucher für Marcel Wagner halten könnten. Sie wird nur nach Freigabe genutzt, und dann als Symbolbild gekennzeichnet.
- Die prozeduralen Grafiken (`tools/art`) werden nicht mehr verwendet. Die Werkzeuge bleiben für spätere Motive erhalten.

## 7. Tests

`python3 tools/test_site.py` prüft auf allen 22 Seiten:
- interne Links und Anker,
- dass Bilder laden und einen alt-Text haben,
- dass es genau eine h1 gibt,
- dass keine Konsolenfehler auftreten,
- dass bei 1920, 1440, 1024, 768, 390 und 375 px kein horizontales Scrollen entsteht.

Auf der Startseite (DE und EN) prüft es außerdem:
- Ankersprünge und Scrollspy,
- den Header-Zustand beim Scrollen,
- Reveal,
- mailto- und tel-Links,
- das Mobilmenü (öffnen, ESC, schließen nach Linkklick),
- Skip-Link und sichtbaren Fokus,
- Reduced Motion.

Ergebnisse vom 19.11.2026:
- Tests in Chromium: 0 Fehler. Firefox und WebKit sind in dieser Umgebung nicht installiert und wurden daher nicht getestet.
- Lighthouse 12, lokal gemessen:

| Seite | Performance | Accessibility | Best Practices | SEO | LCP | CLS |
|---|---|---|---|---|---|---|
| Startseite mobil | 98 | 100 | 100 | 100 | 2,3 s | 0 |
| Startseite Desktop | 100 | 100 | 100 | 100 | 0,5 s | 0 |
| EN-Startseite und Unterseiten | 98–100 | 100 | 100 | 100 | – | – |

## 8. Veröffentlichung

Erst nach ausdrücklicher Freigabe: `main` mergen und pushen. GitHub Pages veröffentlicht danach automatisch.
