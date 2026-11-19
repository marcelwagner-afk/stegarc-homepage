"""Funktionstests für die Homepage (Playwright, Chromium; Firefox/WebKit wenn installiert).

Aufruf: python3 tools/test_site.py
Startet einen lokalen Server auf dem Repo-Root, prüft alle Seiten auf
interne Links, Anker, Bilder, Konsolenfehler, horizontales Scrollen und
testet Navigation, Mobilmenü, Scrollspy und Reveal.
"""
import http.server, threading, functools, pathlib, re, sys
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.html")
               if not any(x in p.parts for x in ("tools", "content", "node_modules", ".git")))
WIDTHS = [1920, 1440, 1024, 768, 390, 375]
fails = []

def fail(msg):
    fails.append(msg); print("FEHLER:", msg)

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=str(ROOT))
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s, f"http://127.0.0.1:{s.server_port}/"

def run(pw, name, base):
    try:
        browser = getattr(pw, name).launch()
    except Exception as e:
        print(f"{name}: nicht verfügbar ({str(e).splitlines()[0][:80]})"); return False
    print(f"== {name} ==")
    ctx = browser.new_context()
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    seen = set()
    for p in PAGES:
        errors.clear()
        r = page.goto(base + p)
        if not r or r.status != 200: fail(f"{p}: Status {r and r.status}")
        for w in (1440, 390):
            page.set_viewport_size({"width": w, "height": 900})
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > w: fail(f"{p} @{w}: horizontaler Scroll ({sw}px)")
        imgs = page.evaluate("""[...document.images].filter(i=>{i.loading='eager';return true}).map(i=>i.currentSrc||i.src)""")
        page.wait_for_timeout(150)
        broken = page.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)")
        for b in broken: fail(f"{p}: Bild lädt nicht {b}")
        noalt = page.evaluate("[...document.images].filter(i=>!i.hasAttribute('alt')).length")
        if noalt: fail(f"{p}: {noalt} Bild(er) ohne alt")
        if page.evaluate("document.querySelectorAll('h1').length") != 1: fail(f"{p}: nicht genau eine h1")
        for href in page.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))"):
            if href.startswith(("mailto:", "tel:")):
                continue
            u = urljoin(base + p, href)
            if not u.startswith(base): continue
            path, _, frag = u.partition("#")
            key = (path, frag)
            if key in seen: continue
            seen.add(key)
            rel = urlparse(path).path.lstrip("/")
            f = ROOT / rel
            if f.is_dir() or rel == "": f = f / "index.html"
            if not f.exists(): fail(f"{p}: toter Link {href}"); continue
            if frag and f.suffix == ".html" and f'id="{frag}"' not in f.read_text(encoding="utf-8"):
                fail(f"{p}: Anker fehlt {href}")
        if errors: fail(f"{p}: Konsolenfehler {errors[:2]}")

    for start, lang in (("", "de"), ("en/", "en")):
        page.goto(base + start)
        for w in WIDTHS:
            page.set_viewport_size({"width": w, "height": 900})
            sw = page.evaluate("document.documentElement.scrollWidth")
            if sw > w: fail(f"{lang} @{w}: horizontaler Scroll ({sw}px)")
        # Desktop: Navigation, Scroll-Zustand, Scrollspy
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(base + start)
        if "scrolled" in (page.get_attribute("header.top", "class") or ""): fail(f"{lang}: Header vor dem Scrollen schon .scrolled")
        for a in page.query_selector_all(".nav a.link"):
            href = a.get_attribute("href"); tid = href.split("#")[1]
            a.click(); top, last = None, 1e9
            for _ in range(20):  # warten, bis Smooth-Scroll steht
                page.wait_for_timeout(200)
                top = page.evaluate(f"document.getElementById('{tid}').getBoundingClientRect().top")
                if abs(top - last) < 1: break
                last = top
            if not (-5 < top < 200): fail(f"{lang}: Ankersprung {href} landet bei {top:.0f}px")
            cur = page.evaluate("(document.querySelector('.nav a.link[aria-current]')||{}).getAttribute?.('href')")
            if cur != href: fail(f"{lang}: Scrollspy markiert {cur} statt {href}")
        if "scrolled" not in (page.get_attribute("header.top", "class") or ""): fail(f"{lang}: Header nach Scroll nicht .scrolled")
        # Reveal: alle Elemente sichtbar nach Durchscrollen
        page.evaluate("(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}})()")
        page.wait_for_timeout(2500)
        hidden = page.evaluate("[...document.querySelectorAll('.reveal')].filter(e=>!e.classList.contains('in')).length")
        if hidden: fail(f"{lang}: {hidden} Reveal-Elemente bleiben unsichtbar")
        # Kontakt
        if not page.query_selector('a[href^="mailto:"]') or not page.query_selector('a[href^="tel:+49"]'): fail(f"{lang}: mailto/tel fehlt")
        # Mobilmenü
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(base + start)
        btn = page.locator(".menu-btn")
        if not btn.is_visible(): fail(f"{lang}: Menüknopf mobil unsichtbar")
        btn.click(); page.wait_for_timeout(300)
        if btn.get_attribute("aria-expanded") != "true" or not page.locator("#menu a.link").first.is_visible(): fail(f"{lang}: Menü öffnet nicht")
        page.keyboard.press("Escape"); page.wait_for_timeout(300)
        if btn.get_attribute("aria-expanded") != "false": fail(f"{lang}: ESC schließt Menü nicht")
        btn.click(); page.wait_for_timeout(300)
        page.locator("#menu a.link").nth(1).click(); page.wait_for_timeout(900)
        if btn.get_attribute("aria-expanded") != "false": fail(f"{lang}: Menü schließt nach Linkklick nicht")
        # Tastatur: Skip-Link und sichtbarer Fokus
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(base + start)
        page.keyboard.press("Tab")
        if page.evaluate("document.activeElement.className") != "skip": fail(f"{lang}: Skip-Link nicht erstes Fokusziel")
        page.keyboard.press("Tab")
        ol = page.evaluate("getComputedStyle(document.activeElement).outlineStyle")
        if ol == "none": fail(f"{lang}: kein sichtbarer Fokusrahmen")
        # Reduced motion: keine versteckten Inhalte
        rm = browser.new_context(reduced_motion="reduce"); rp = rm.new_page(); rp.goto(base + start)
        op = rp.evaluate("Math.min(...[...document.querySelectorAll('.reveal')].map(e=>+getComputedStyle(e).opacity))")
        if op < 1: fail(f"{lang}: reduced-motion versteckt Inhalte (opacity {op})")
        rm.close()
    browser.close()
    return True

if __name__ == "__main__":
    srv, base = serve()
    with sync_playwright() as pw:
        ran = [n for n in ("chromium", "firefox", "webkit") if run(pw, n, base)]
    srv.shutdown()
    print(f"\nSeiten: {len(PAGES)}, Browser: {', '.join(ran)}, Fehler: {len(fails)}")
    sys.exit(1 if fails else 0)
