"""Baut die statische Website aus content/<sprache>/… (Inhalt) und dem gemeinsamen Rahmen (Kopf, Fuß, SEO).

Jede Inhaltsdatei beginnt mit einer Zeile <!--META {...}--> (JSON):
  title, description          Pflicht – Seitentitel und Meta-Beschreibung
  type                        "home", "page" (Standard), "post" (Blogbeitrag)
  alt                         Pfad der Seite in der anderen Sprache, vom Repo-Stamm aus (z. B. "en/blog/x.html")
  date, updated, read, tags, lead   nur für Beiträge (Datum ISO, Lesezeit in Minuten)
Platzhalter im Inhalt: <!--POSTS--> = die drei neuesten Beiträge der Sprache.
Ausgabe: gleiche Pfade im Repo-Stamm (de) bzw. unter en/, dazu Blog-Übersichten, sitemap.xml, robots.txt.
Kontaktdaten stehen nur im Impressum (content/de/impressum.html) und werden von dort übernommen.
Aufruf: python3 build.py   (keine Abhängigkeiten)
"""
import html, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent
BASE = "https://marcelwagner-afk.github.io/stegarc-homepage/"
NAME = "Marcel Wagner – STEGARC"
_imp = (ROOT / "content" / "de" / "impressum.html").read_text(encoding="utf-8")
CONTACT = {"email": re.search(r'href="mailto:([^"?]+)', _imp).group(1), "telephone": re.search(r'href="tel:([^"]+)', _imp).group(1)}
LOGO = ('<svg width="30" height="30" viewBox="0 0 40 40" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b6a2ff"/>'
        '<stop offset="1" stop-color="#6a45f0"/></linearGradient></defs><path d="M31 11.5C28.8 8.6 25 7.5 20.5 7.5 14.4 7.5 10 10.3 10 14.4s4 5.9 10.3 6.9c6.3 1 10.2 2.8 10.2 7S26 34 19.7 34C15 34 11.3 32.8 9 30" '
        'fill="none" stroke="url(#lg)" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
MON = {"de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
       "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
T = {
    "de": {"nav": [("#leistungen", "Leistungen"), ("#vorgehen", "Vorgehen"), ("#projekte", "Projekte"), ("#plattform", "STEGARC"), ("#ueber", "Über mich")],
           "contact": "Kontakt", "anchor": "kontakt", "skip": "Zum Inhalt springen", "home": "Startseite",
           "legal": [("impressum.html", "Impressum"), ("datenschutz.html", "Datenschutz")],
           "blog_title": "Blog – SAP-Transformation, KI und Sonderlösungen",
           "blog_desc": "Fachbeiträge von Marcel Wagner zu SAP ECC und S/4HANA, RISE with SAP, Cutover, SAP-Lizenzen, KI im ERP und individuellen Lösungen.",
           "blog_lead": "Praxiswissen aus SAP-Transformationen – ehrlich, konkret und ohne Marketing-Nebel.",
           "read": "Min. Lesezeit", "by": "von Marcel Wagner", "more": "Weiterlesen", "related": "Weitere Beiträge", "updated": "aktualisiert",
           "cta_h": "Sie stehen vor einer ähnlichen Entscheidung?", "cta_p": "Schildern Sie kurz Ihre Ausgangslage – ich melde mich mit einem Vorschlag für ein erstes Gespräch.",
           "cta_b": "Gespräch vereinbaren", "menu_open": "Menü öffnen", "menu_close": "Menü schließen", "nav_label": "Hauptnavigation", "legal_label": "Rechtliches", "date": lambda d: f"{int(d[8:10])}. {MON['de'][int(d[5:7]) - 1]} {d[:4]}", "locale": "de_DE"},
    "en": {"nav": [("#services", "Services"), ("#approach", "Approach"), ("#projects", "Projects"), ("#platform", "STEGARC"), ("#about", "About me")],
           "contact": "Contact", "anchor": "contact", "skip": "Skip to content", "home": "Home",
           "legal": [("legal-notice.html", "Legal notice"), ("privacy.html", "Privacy")],
           "blog_title": "Blog – SAP transformation, AI and custom solutions",
           "blog_desc": "Articles by Marcel Wagner on SAP ECC and S/4HANA, RISE with SAP, cutover, SAP licensing, AI in ERP and custom solutions.",
           "blog_lead": "Practical knowledge from SAP transformations – honest, specific and free of marketing fog.",
           "read": "min read", "by": "by Marcel Wagner", "more": "Read more", "related": "More articles", "updated": "updated",
           "cta_h": "Facing a similar decision?", "cta_p": "Briefly describe your situation – I will get back to you with a proposal for a first conversation.",
           "cta_b": "Book a conversation", "menu_open": "Open menu", "menu_close": "Close menu", "nav_label": "Main navigation", "legal_label": "Legal", "date": lambda d: f"{int(d[8:10])} {MON['en'][int(d[5:7]) - 1]} {d[:4]}", "locale": "en_GB"},
}

def read(p):
    s = p.read_text(encoding="utf-8"); m = re.match(r"<!--META (\{.*?\})-->\n?", s, re.S)
    assert m, f"META fehlt: {p}"
    return json.loads(m.group(1)), s[m.end():]

def card(lang, rel_path, m, start):
    t = T[lang]; href = start + rel_path
    return (f'<li><a href="{href}"><time datetime="{m["date"]}">{t["date"](m["date"])}</time>'
            f'<div><h3>{html.escape(m["title"])}</h3><p>{html.escape(m["description"])}</p></div></a></li>')

def post_body(lang, out, m, body, posts, start):
    t = T[lang]
    upd = f', {t["updated"]} {t["date"](m["updated"])}' if m.get("updated", m["date"]) != m["date"] else ""
    others = "".join(card(lang, rp, mm, start) for o, rp, mm in posts[lang] if o != out)
    tags = "".join(f'<span class="tag">{html.escape(x)}</span>' for x in m.get("tags", []))
    return f'''<article class="wrap post">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{start}">{t["home"]}</a> / <a href="{start}blog/">Blog</a></nav>
  <header class="post-head">
    <div class="post-meta">{t["date"](m["date"])}{upd}, {m.get("read", 5)} {t["read"]}, {t["by"]}</div>
    <h1>{html.escape(m["title"])}</h1>
    <p class="lead">{html.escape(m.get("lead", m["description"]))}</p>
    <div class="tags">{tags}</div>
  </header>
  <div class="prose">
{body}
  </div>
  <aside class="post-cta"><h2>{t["cta_h"]}</h2><p>{t["cta_p"]}</p><a class="btn btn-primary" href="{start}#{t["anchor"]}">{t["cta_b"]}</a></aside>
</article>
<section class="related"><div class="wrap"><h2>{t["related"]}</h2><ul class="posts">{others}</ul></div></section>'''

def render(lang, out, m, body, posts):
    t = T[lang]; r = "../" * out.count("/"); start = r + ("" if lang == "de" else "en/") or "./"
    hp = "" if m.get("type") == "home" else start
    url = BASE + out.replace("index.html", ""); alt = m.get("alt"); other = "en" if lang == "de" else "de"
    body = body.replace("<!--POSTS-->", "".join(card(lang, rp, mm, start) for o, rp, mm in posts[lang][:3]))
    org = {"@context": "https://schema.org", "@type": "ProfessionalService", "@id": BASE + "#org", "name": NAME, "url": BASE, **CONTACT,
           "image": BASE + "assets/og.jpg", "logo": BASE + "assets/logo.svg", "founder": {"@type": "Person", "name": "Marcel Wagner", "jobTitle": "Inhaber"},
           "address": {"@type": "PostalAddress", "streetAddress": "Eichendorffstr. 38", "postalCode": "75031", "addressLocality": "Eppingen", "addressRegion": "Baden-Württemberg", "addressCountry": "DE"},
           "areaServed": ["DE", "AT", "CH", "EU"], "knowsLanguage": ["de", "en", "fr"],
           "knowsAbout": ["SAP S/4HANA", "SAP ECC", "RISE with SAP", "Cutover-Management", "SAP-Lizenzoptimierung", "SAP SuccessFactors", "Künstliche Intelligenz im ERP", "Individuelle Softwareentwicklung", "Systemintegration"]}
    ld = [org]
    if m.get("type") == "post":
        ld.append({"@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"], "description": m["description"], "datePublished": m["date"],
                   "dateModified": m.get("updated", m["date"]), "inLanguage": lang, "mainEntityOfPage": url, "author": {"@type": "Person", "name": "Marcel Wagner", "url": BASE},
                   "publisher": {"@id": BASE + "#org"}, "image": BASE + "assets/og.jpg", "keywords": ", ".join(m.get("tags", []))})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home"], "item": BASE + ("" if lang == "de" else "en/")},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + ("" if lang == "de" else "en/") + "blog/"},
            {"@type": "ListItem", "position": 3, "name": m["title"], "item": url}]})
        body = post_body(lang, out, m, body, posts, start)
    title = m["title"] if m.get("type") == "home" else f'{m["title"]} · {NAME}'
    alts = ""
    if alt:
        de_url, en_url = (url, BASE + alt.replace("index.html", "")) if lang == "de" else (BASE + alt.replace("index.html", ""), url)
        alts = f'<link rel="alternate" hreflang="de" href="{de_url}">\n<link rel="alternate" hreflang="en" href="{en_url}">\n<link rel="alternate" hreflang="x-default" href="{de_url}">\n'
    navs = "".join(f'<a class="link" href="{hp + h}">{n}</a>' for h, n in t["nav"])
    lsw = (f'<a class="lang" href="{r + alt}" hreflang="{other}" lang="{other}" title="{"English" if other == "en" else "Deutsch"}">'
           f'{other.upper()}</a>') if alt else ""
    legal = "".join(f'<a href="{start + h}">{n}</a>' for h, n in t["legal"])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(m["description"])}">
<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="{"article" if m.get("type") == "post" else "website"}">
<meta property="og:site_name" content="STEGARC">
<meta property="og:title" content="{html.escape(m["title"])}">
<meta property="og:description" content="{html.escape(m["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og.jpg">
<meta property="og:locale" content="{t["locale"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="author" content="Marcel Wagner">
<meta name="theme-color" content="#F8F9FA">
<link rel="icon" href="{r}assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="{r}assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/inter-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/style.css">
<script>document.documentElement.classList.add("js")</script>
<script src="{r}assets/site.js" defer></script>
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else org, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#inhalt">{t["skip"]}</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="{start}" aria-label="STEGARC – {t["home"]}">STEGARC</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-open="{t["menu_open"]}" data-close="{t["menu_close"]}"><span class="sr">{t["menu_open"]}</span><i></i><i></i></button>
    <nav class="nav" id="menu" aria-label="{t["nav_label"]}">{navs}{lsw}<a class="btn btn-primary" href="{hp}#{t["anchor"]}">{t["contact"]}</a></nav>
  </div>
</header>
<main id="inhalt">
{body}
</main>
<footer>
  <div class="wrap">
    <a class="brand" href="{start}">STEGARC</a><span>© 2026 {NAME}, Eichendorffstr. 38, 75031 Eppingen</span>
    <nav aria-label="{t["legal_label"]}">{legal}<a href="{start}blog/">Blog</a></nav>
  </div>
</footer>
</body>
</html>
'''

def main():
    pages = []
    for lang in ("de", "en"):
        for p in sorted((ROOT / "content" / lang).rglob("*.html")):
            m, b = read(p); rp = p.relative_to(ROOT / "content" / lang).as_posix()
            pages.append((lang, rp if lang == "de" else "en/" + rp, rp, m, b))
    posts = {l: sorted([(o, rp, m) for (ll, o, rp, m, b) in pages if ll == l and m.get("type") == "post"], key=lambda x: x[2]["date"], reverse=True) for l in ("de", "en")}
    for l in ("de", "en"):
        t = T[l]; out = "blog/index.html" if l == "de" else "en/blog/index.html"
        cards = "".join(card(l, rp, m, "../") for o, rp, m in posts[l])
        body = (f'<section class="sec page-head"><div class="wrap"><div class="head"><h1>Blog</h1><p class="intro">{t["blog_lead"]}</p></div>'
                f'<ul class="posts">{cards}</ul></div></section>')
        pages.append((l, out, "blog/index.html", {"title": t["blog_title"], "description": t["blog_desc"], "alt": "en/blog/index.html" if l == "de" else "blog/index.html"}, body))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang, out, rp, m, b in pages:
        f = ROOT / out; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(render(lang, out, m, b, posts), encoding="utf-8")
        u = BASE + out.replace("index.html", ""); x = ""
        if m.get("alt"):
            o = "de" if lang == "en" else "en"
            x = f'<xhtml:link rel="alternate" hreflang="{lang}" href="{u}"/><xhtml:link rel="alternate" hreflang="{o}" href="{BASE + m["alt"].replace("index.html", "")}"/>'
        sm.append(f'<url><loc>{u}</loc><lastmod>{m.get("updated", m.get("date", "2026-11-19"))}</lastmod>{x}</url>')
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    print(len(pages), "Seiten,", len(posts["de"]), "Beiträge DE,", len(posts["en"]), "Beiträge EN")

if __name__ == "__main__":
    main()
