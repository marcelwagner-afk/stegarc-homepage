"""Erzeugt content/de/index.html und content/en/index.html (Startseite) aus einem Textsatz je Sprache.
Danach build.py ausführen. Icons als Inline-SVG, Bilder aus assets/img (hell/dunkel)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
I = {  # Strichsymbole 24x24
 "cube": '<path d="M12 2.5 3.5 7v10L12 21.5 20.5 17V7z"/><path d="M3.5 7 12 11.5 20.5 7M12 11.5v10"/>',
 "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/><path d="m3 17.5 9 5 9-5" opacity=".6"/>',
 "grid": '<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/><path d="M12 3.5v17M3.5 12h17"/>',
 "db": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13"/><path d="M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
 "play": '<path d="M7 4.5v15l12-7.5z"/>',
 "chip": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9.5 2.5v3.5M14.5 2.5v3.5M9.5 18v3.5M14.5 18v3.5M2.5 9.5H6M2.5 14.5H6M18 9.5h3.5M18 14.5h3.5"/><rect x="9.5" y="9.5" width="5" height="5"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
 "code": '<path d="m8 7-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.2 2.8 2.8L16.5 9"/>',
 "key": '<circle cx="8" cy="15" r="4.5"/><path d="m11.2 11.8 8.3-8.3M16.5 6.5l2.5 2.5M14 9l2 2"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 4.8a3.2 3.2 0 0 1 0 6.3M21 20c0-2.6-1.6-4.8-4-5.6"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}
def ic(n, s=26, cls="ic"): return f'<svg class="{cls}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'
ARROW = ic("arrow", 18, "")
PHOTO = {"svc-erp": (487, 108), "svc-s4": (480, 108), "svc-dyn": (485, 108), "svc-ora": (487, 110), "svc-cut": (480, 110), "svc-ki": (485, 110)}
BIG = {"hero": 1441 / 2560, "platform": 1707 / 2560, "connect": 1707 / 2560, "dashboard": 1441 / 2560}

def photo(name, alt, r, eager=False, sizes="100vw"):
    """Bild aus der STEGARC-Bildwelt (assets/photo): WebP, bei großen Motiven mit srcset, JPEG-Fallback."""
    if name in BIG:
        ss = ", ".join(f"{r}assets/photo/{name}-{w}.webp {w}w" for w in (960, 1600, 2560))
        w, h = 1600, round(1600 * BIG[name])
        src = f'<source type="image/webp" srcset="{ss}" sizes="{sizes}">'
    else:
        (w, h), src = PHOTO[name], f'<source type="image/webp" srcset="{r}assets/photo/{name}.webp">'
    return (f'<picture>{src}<img src="{r}assets/photo/{name}.jpg" alt="{alt}" width="{w}" height="{h}"'
            f'{" fetchpriority=\"high\"" if eager else " loading=\"lazy\""} decoding="async"></picture>')

def appmock(t):
    m = t["mock"]
    rows = "".join(f'<div><span>{n}</span><span class="bar"><i style="width:{v}%"></i></span><span>{v} %</span></div>' for n, v in m["rows"])
    nav = "".join(f'<span{" class=\"on\"" if i == 0 else ""}>{x}</span>' for i, x in enumerate(m["nav"]))
    return (f'<div class="app" role="img" aria-label="{m["aria"]}"><aside><b>STEGARC</b>{nav}</aside><main><p class="ttl">{m["title"]}</p>'
            f'<div class="tile"><small>{m["k1"]}</small><strong>82 %</strong><span class="bar"><i style="width:82%"></i></span></div>'
            f'<div class="tile"><small>{m["k2"]}</small><strong>{m["k2v"]}</strong></div>'
            f'<div class="tile"><small>{m["k3"]}</small><strong>98 % <span class="ok"><svg width="9" height="9" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 6.2 5 8.5 9.5 3.5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span></strong></div>'
            f'<div class="tile wide"><small>{m["k4"]}</small><div class="rows">{rows}</div></div>'
            f'<div class="tile"><small>{m["k5"]}</small><svg class="spark" viewBox="0 0 120 60" aria-hidden="true"><path d="M0 52 L15 46 L28 48 L40 38 L55 40 L68 28 L80 30 L92 18 L106 20 L120 6" fill="none" stroke="#00B8B0" stroke-width="2.5" stroke-linejoin="round"/><path d="M0 52 L15 46 L28 48 L40 38 L55 40 L68 28 L80 30 L92 18 L106 20 L120 6 L120 60 L0 60Z" fill="rgba(0,184,176,.12)"/></svg></div>'
            f'</main></div>')

def page(L, r):
    t = L; a = t["anchors"]
    svc = "".join(f'<article class="card reveal"><div class="band" aria-hidden="true">{photo(pic.replace("card-", "svc-"), "", r)}</div><div class="body"><h3>{h}</h3><p>{p}</p>{f"""<a class="more" href="{lk[0]}">{lk[1]} {ic("arrow", 16, "")}</a>""" if lk else ""}</div></article>'
                  for icon, pic, h, p, lk in t["svc2"])
    extra = '<div class="card extra reveal"><h3>' + t["extra_label"] + '</h3>' + "".join(f'<div>{ic(i, 28)}<span><b>{h}</b>{p}</span></div>' for i, h, p in t["extra1"]) + '</div>'
    also = t["also"] + " " + ", ".join(f"<b>{h}</b>" for i, h, p in t["extra2"]) + "."
    feats = "".join(f'<div class="feat">{ic(i, 32)}<span><b>{h}</b>{p}</span></div>' for i, h, p in t["feats"])
    cases = "".join(f'<div class="card"><b>{h}</b><span>{p}</span></div>' for h, p in t["cases"])
    uses = "".join(f'<li>{ic("check", 18, "")}<span><b>{h}</b> {p}</span></li>' for h, p in t["uses"])
    steps = "".join(f'<li><b>{h}</b><span>{p}</span></li>' for h, p in t["steps"])
    work = "".join(f'<li><span class="who">{w}</span><span class="what"><b>{h}</b><span>{p}</span></span><span class="role">{ro}</span></li>' for w, h, p, ro in t["work"])
    caps = "".join(f'<li>{ic("check", 20, "")}<span><b>{h.rstrip(":")}</b>{p}</span></li>' for h, p in t["mods"])
    tl = "".join(f'<li><b>{h}</b><span>{p}</span></li>' for h, p in t["timeline"])
    skills = "".join(f"<span>{x}</span>" for x in t["skills"])
    faq = "".join(f"<details><summary>{q}</summary><p>{ans}</p></details>" for q, ans, _ in t["faq"])
    faqld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": s}} for q, ans, s in t["faq"]]}, ensure_ascii=False)
    about = "".join(f'<p{" class=\"first\"" if i == 0 else ""}>{x}</p>' for i, x in enumerate(t["about"]))
    h2 = "".join(f"<span>{x}</span>" for x in t["tech_h"])
    return f'''<!--META {json.dumps(t["meta"], ensure_ascii=False)}-->
<section class="hero" aria-labelledby="hero-h">
  <div class="art" aria-hidden="true">{photo("hero", "", r, eager=True)}</div>
  <div class="wrap">
    <div class="copy">
      <div class="eyebrow">{t["eyebrow"]}</div>
      <h1 id="hero-h">{t["h1a"]}<br><span class="accent">{t["h1b"]}</span></h1>
      <p class="lead">{t["lead2"]}</p>
      <div class="cta"><a class="btn btn-primary" href="#{a["contact"]}">{t["cta"]} {ARROW}</a><a class="btn btn-secondary" href="#{a["services"]}">{t["cta2"]}</a></div>
    </div>
    <div class="feats">{feats}</div>
  </div>
</section>

<section class="praxis" aria-labelledby="praxis-h">
  <div class="wrap">
    <figure class="laptop reveal"><div class="lid">{appmock(t)}</div><div class="base" aria-hidden="true"></div><figcaption>{t["mock"]["cap"]}</figcaption></figure>
    <div class="card reveal"><div class="rule" aria-hidden="true"></div><h2 id="praxis-h">{t["praxis_h"]}</h2><p>{t["praxis_p2"]}</p><div class="cta"><a class="btn btn-secondary" href="#{a["approach"]}">{t["praxis_b"]}</a></div></div>
  </div>
</section>

<section class="section" id="{a["services"]}" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["svc_eyebrow"]}</div><h2 id="svc-h">{t["svc_h"]}</h2><p class="intro">{t["svc_p"]}</p></div>
    <div class="svc">{svc}</div>
    {extra}
    <p class="also reveal">{also}</p>
  </div>
</section>

<section class="section dark tech" id="{a["platform"]}" aria-labelledby="tech-h">
  <div class="bgart" aria-hidden="true">{photo("platform", "", r)}</div>
  <div class="wrap">
    <div class="grid">
      <div class="reveal">
        <div class="eyebrow">{t["tech_eyebrow"]}</div>
        <h2 id="tech-h">{h2}</h2>
        <p class="intro">{t["pf_p"]}</p>
        <ul class="caps">{caps}</ul>
        <div class="cta"><a class="btn btn-primary" href="https://marcelwagner-afk.github.io/stegarc-suite/index.html{t["demo_q"]}">{t["demo_b"]} {ARROW}</a><a class="btn btn-secondary" href="https://marcelwagner-afk.github.io/stegarc-suite/{t["product"]}">{t["product_b"]}</a></div>
      </div>
      <figure class="monitor reveal"><div class="screen"><img src="{r}assets/stegarc-demo-{t["lang"]}.jpg" width="1600" height="965" alt="{t["shot_alt"]}" loading="lazy" decoding="async"></div><div class="stand" aria-hidden="true"></div><figcaption>{t["shot_cap"]}</figcaption></figure>
    </div>
  </div>
</section>

<section class="section dark" id="{a["ai"]}" aria-labelledby="ai-h" style="padding-top:0">
  <div class="wrap split">
    <div class="reveal"><div class="eyebrow">{t["ai_eyebrow"]}</div><h2 id="ai-h">{t["ai_h"]}</h2><p class="intro">{t["ai_p"]}</p><ul class="uses">{uses}</ul></div>
    <div class="kiside reveal"><figure class="dash">{photo("dashboard", t["dash_alt"], r, sizes="(max-width:960px) 92vw, 600px")}</figure><div class="card approve" role="group" aria-label="{t["ap_label"]}">
      <div class="msg"><b>{t["ap_h"]}</b>{t["ap_msg"]}</div>
      <dl>{"".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in t["ap_dl"])}</dl>
      <div class="acts" aria-hidden="true"><span class="yes">{t["ap_yes"]}</span><span>{t["ap_no"]}</span></div>
      <p class="note">{t["ap_note"]}</p>
    </div></div>
  </div>
</section>

<section class="section" id="{a["custom"]}" aria-labelledby="sl-h">
  <div class="wrap">
    <div class="reveal"><div class="eyebrow">{t["sl_eyebrow"]}</div>
      <h2 id="sl-h" class="no"><s>{t["sl_no"]}</s><em>{t["sl_yes"]}</em></h2>
      <p class="intro" style="margin-top:24px">{t["sl_p"]}</p></div>
    <div class="cases reveal">{cases}</div>
    <div class="cta reveal"><a class="btn btn-primary" href="#{a["contact"]}">{t["sl_cta"]} {ARROW}</a><a class="btn btn-secondary" href="blog/{t["sl_blog"]}">{t["more_blog"]}</a></div>
  </div>
</section>

<section class="section alt" id="{a["approach"]}" aria-labelledby="st-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["st_eyebrow"]}</div><h2 id="st-h">{t["st_h"]}</h2><p class="intro">{t["st_p"]}</p></div>
    <ol class="steps reveal">{steps}</ol>
  </div>
</section>

<section class="section" id="{a["projects"]}" aria-labelledby="pj-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["fx_eyebrow"]}</div><h2 id="pj-h">{t["fx_h"]}</h2><p class="intro">{t["pj_p2"]}</p></div>
    <div class="card work reveal"><ul>{work}</ul></div>
    <p class="fine">{t["pj_fine"]}</p>
  </div>
</section>

<section class="section alt" id="{a["about"]}" aria-labelledby="ab-h">
  <div class="wrap about">
    <div class="body reveal"><div class="eyebrow">{t["ab_eyebrow"]}</div><h2 id="ab-h" style="margin-bottom:24px">Marcel Wagner</h2>{about}</div>
    <aside class="card side reveal">
      <div><h3>{t["tl_h"]}</h3><ol class="timeline">{tl}</ol></div>
      <div><h3>{t["sk_h"]}</h3><div class="skills">{skills}</div></div>
      <div><h3>{t["lg_h"]}</h3><p style="color:var(--ink-2)">{t["lg"]}</p></div>
    </aside>
  </div>
</section>

<section class="section" id="blog-teaser" aria-labelledby="bl-h">
  <div class="wrap">
    <div class="head rowhead reveal"><div><div class="eyebrow">Blog</div><h2 id="bl-h">{t["blog_h"]}</h2></div><a class="btn btn-secondary" href="blog/">{t["blog_all"]}</a></div>
    <ul class="posts"><!--POSTS--></ul>
  </div>
</section>

<section class="section" id="faq" aria-labelledby="faq-h" style="padding-top:0">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">FAQ</div><h2 id="faq-h">{t["faq_h"]}</h2></div>
    <div class="faq">{faq}</div>
  </div>
  <script type="application/ld+json">{faqld}</script>
</section>

<section class="section dark contactsec" id="{a["contact"]}" aria-labelledby="ct-h">
  <div class="bgart" aria-hidden="true">{photo("connect", "", r)}</div>
  <div class="wrap contact">
    <div class="reveal"><div class="eyebrow">{t["ct_eyebrow"]}</div><h2 id="ct-h">{t["ct_h"]}</h2><p class="intro">{t["ct_p"]}</p>
      <div class="cta"><a class="btn btn-primary" href="mailto:marcel.wagner@w-dfs.de?subject={t["ct_subj"]}">{t["ct_mail"]} {ARROW}</a><a class="btn btn-secondary" href="tel:+491791600252">{t["ct_call"]}</a></div></div>
    <dl class="reveal">{"".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in t["ct_dl"])}</dl>
  </div>
</section>
'''

DE = dict(lang="de", meta={"type": "home", "title": "ERP-Transformation, Sonderlösungen und KI · Marcel Wagner – STEGARC",
  "description": "Premium-B2B-Beratung für ERP-Transformation: SAP S/4HANA, Microsoft Dynamics, Oracle, Cutover und Go-live, Sonderlösungen und KI. Über 20 Jahre Erfahrung, Eppingen.", "alt": "en/index.html"},
  anchors=dict(services="leistungen", custom="sonderloesungen", ai="ki", approach="vorgehen", projects="projekte", platform="plattform", about="ueber", contact="kontakt"),
  eyebrow="Premium-B2B-Consulting", h1a="Wo andere Nein sagen,", h1b="fange ich an.",
  lead="Herstellerunabhängige ERP-Transformation, SAP S/4HANA, Microsoft Dynamics, Oracle, komplexe Cutover und Go-live sowie KI-Lösungen – mit Umsetzungskraft, über 20 Jahren Erfahrung und klarem Ergebnisfokus.",
  cta="Erstgespräch vereinbaren",
  feats=[("layers", "ERP-Expertise", "herstellerunabhängig"), ("target", "Transformation", "von Strategie bis Go-live"), ("chip", "KI und Daten", "mit messbarem Nutzen")],
  shot_alt="STEGARC-Demo: Dashboard mit Kennzahlen und offenen Freigaben aus SAP, ServiceNow und Microsoft 365", shot_cap="STEGARC-Demo mit synthetischen Daten fiktiver Unternehmen",
  praxis_h="ERP-Transformation in der Praxis.", praxis_p="Transparente Steuerung, belastbare Daten und messbarer Projektfortschritt für einen sicheren Go-live. Mit STEGARC sehen Sie Aufgaben, Freigaben und Kennzahlen aus allen Systemen in einer Oberfläche.",
  demo_q="", demo_b="Live-Demo ansehen", product="stegarc.html", product_b="Produktseite",
  svc_eyebrow="Leistungen", svc_h="ERP, Daten und KI – aus einer Hand.", svc_p="Sechs Kernleistungen für erfolgreiche Transformationen, ergänzt um Datenmigration, Sonderentwicklungen und die STEGARC-Plattform.",
  svc=[("cube", "card-erp", "ERP-Transformation", "Strategie, Zielbild, Architektur und Umsetzung – herstellerunabhängig und end-to-end.", ("blog/rise-with-sap-oder-alternativen.html", "RISE oder Alternativen?")),
       ("layers", "card-s4", "SAP S/4HANA", "Planung, Einführung, Conversion und Rollout – inklusive Central Finance und internationaler Deployments.", ("blog/sap-ecc-wartungsende-2027.html", "ECC-Wartungsende 2027")),
       ("grid", "card-dyn", "Microsoft Dynamics", "Auswahl, Einführung und Harmonisierung von Unternehmensprozessen auf Dynamics 365.", None),
       ("db", "card-ora", "Oracle", "Migration und Integration in komplexen Systemlandschaften – stabil und zukunftssicher.", None),
       ("play", "card-cut", "Cutover und Go-live", "Planung, Generalproben und Orchestrierung für einen sicheren Produktivstart mit minimalem Risiko.", ("blog/cutover-planung-go-live.html", "Zehn Regeln für den Cutover")),
       ("chip", "card-ki", "KI-Lösungen", "Pragmatische KI-Anwendungsfälle mit menschlicher Freigabe und messbarem Mehrwert für Ihre Prozesse.", ("blog/ki-im-erp-sinnvoll-einsetzen.html", "KI im ERP sinnvoll einsetzen"))],
  extra_label="Ergänzende Schwerpunkte",
  extra1=[("db", "Datenmigration", "Sicher, effizient und revisionsfest."), ("code", "Sonderentwicklungen", "Individuelle Lösungen für spezifische Anforderungen."), ("layers", "STEGARC KI-Plattform", "Eine Oberfläche über allen Systemen.")],
  extra2=[("key", "Lizenzoptimierung", "Nutzung und Vertrag transparent machen."), ("users", "HR und SuccessFactors", "Von SAP HCM bis zum globalen Rollout."), ("flag", "Programmleitung und PE", "Interim-Rollen, Carve-outs, Portfolio.")],
  fx_eyebrow="ERP-Projekte, die wirklich liefern", fx_h="Komplexe Vorhaben. Klare Ergebnisse.", fx_p="Strukturiertes Vorgehen, starke Umsetzung und messbarer Nutzen – von der Konzeption bis zum Go-live. Aus über 20 Jahren Programmen in DAX-Konzernen und im Mittelstand.",
  sl_eyebrow="Sonderlösungen", sl_no="„Geht nicht.“", sl_yes="Geht. Nur nicht im Standard.",
  sl_p="Viele Anforderungen scheitern nicht an der Technik, sondern daran, dass niemand die Verantwortung für eine Lösung außerhalb des Standards übernehmen will. Ich übernehme sie – mit einer Architektur, die den ERP-Kern sauber hält, mit Tests und mit einer Dokumentation, die Ihr Team weiterführen kann.",
  cases=[("Branchenprozesse", "die kein Standardpaket abbildet"), ("Altsysteme und Schnittstellen", "die noch Jahre laufen werden"), ("Carve-outs und Zukäufe", "mit unterschiedlichen ERP-Systemen"), ("Portale und Cockpits", "mit Daten aus mehreren Systemen"), ("Migrations-Sonderfälle", "historische Daten, komplexe Mappings"), ("Clean Core", "Erweiterungen neben dem Kern")],
  sl_cta="Anforderung schildern", sl_blog="sonderloesungen-wenn-der-standard-nein-sagt.html", more_blog="Mehr im Blog",
  ai_eyebrow="Künstliche Intelligenz", ai_h="KI dort, wo sie sich lohnt.", ai_p="KI ist kein Selbstzweck. Ich setze sie ein, wo sie wiederkehrende Arbeit abnimmt, Entscheidungen besser vorbereitet oder Wissen schneller auffindbar macht – und sage ehrlich, wann eine klassische Regel die bessere Lösung ist.",
  uses=[("Dokumente verstehen:", "Rechnungen, Lieferscheine und Verträge auslesen und gegen Bestellung und Wareneingang prüfen."), ("Abweichungen erklären:", "Warum ist die Marge gesunken? Antworten aus den echten Daten, mit Quellen."), ("Einkauf vorbereiten:", "Angebote vergleichen und Verhandlungen auf Datenbasis vorbereiten."), ("Ein Assistent für alle Systeme:", "ERP, Microsoft 365, ServiceNow und Workday in einer Oberfläche.")],
  ap_label="Beispiel einer Freigabe", ap_h="Vorschlag des Assistenten", ap_msg="Die Rechnung von Muster Metall GmbH passt zu Bestellung und Wareneingang. Soll sie gebucht werden?",
  ap_dl=[("Betrag", "4.218,40 €"), ("Abweichung", "keine"), ("Fällig", "12.12.2026")], ap_yes="Freigeben", ap_no="Ablehnen",
  ap_note="Beispiel mit erfundenen Daten. Gebucht wird erst, wenn ein Mensch freigibt – bei Buchungen, Freigaben und Zahlungen ohne Ausnahme.",
  st_eyebrow="Vorgehen", st_h="Klare Schritte statt endloser Projekte", st_p="Sie wissen in jeder Phase, was passiert, was es kostet und was als Nächstes entschieden werden muss.",
  steps=[("Verstehen", "Erstgespräch und kompakter Workshop zu Zielen, Systemen und Risiken."), ("Entscheiden", "Optionen mit Aufwand, Nutzen und Risiken für Geschäftsführung oder Investoren."), ("Bauen", "Umsetzung in überschaubaren Etappen mit Tests und sichtbaren Zwischenständen."), ("Einführen", "Cutover, Schulung und Go-live mit klaren Go/No-Go-Kriterien."), ("Live", "Hypercare und Übergabe an Ihr Team.")],
  pj_eyebrow="Projekterfahrung", pj_h="Aus über 20 Jahren Praxis", pj_p="Programme in DAX-Konzernen und international tätigen Unternehmen – und Sonderfälle im Mittelstand, für die es keine Standardantwort gab.",
  work=[("Energietechnik-Konzern, Schweiz", "Einer der größten SAP-S/4HANA-Rollouts", "Verantwortung für das Deployment einer Region: Rollout-Planung, Abstimmung mit den lokalen Gesellschaften, Tests, Cutover und Go-live", "Area Deployment Manager"),
        ("DAX-Konzerne", "SAP-Programmleitung S/4HANA, Central Finance und HR", "Steuerung großer SAP-Programme über Fachbereiche, Gesellschaften und Dienstleister hinweg bis zur Übergabe in den Betrieb", "Programmleitung"),
        ("Rückversicherung, DAX-Konzern", "Globales Cutover-Management", "Cutover-Planung über Länder und Zeitzonen, Generalproben, Go/No-Go-Steuerung und Schulungskonzept", "Global Cutover Manager und Training Lead"),
        ("Energietechnik-Konzern, international", "HR-Transformation: SAP HCM zu SuccessFactors", "Migration nach Employee Central und SuccessFactors von der Strategie bis zum internationalen Rollout", "Programmleitung"),
        ("Industriekonzern, Schweiz", "Finance-Optimierung und KI im Einkauf", "SAP-Programm im Finanzbereich sowie KI-gestützte Automatisierung rund um SAP Ariba, mit menschlicher Freigabe", "SAP Program Manager"),
        ("Mehrere Unternehmen", "Sonderfälle jenseits des Standards", "Lösung erarbeitet, umgesetzt, dokumentiert und in den Regelbetrieb übergeben", "Konzeption, Umsetzung, Übergabe"),
        ("Agrar und Saatgut, börsennotiert", "SAP-Lizenzoptimierung", "Nutzung und Vertrag analysiert, Lizenzzuordnung bereinigt, Herstellergespräche vorbereitet", "Beratung"),
        ("Mittelstand", "HR-Transformation", "Migration von SAP HCM nach Employee Central mit Einführung von SuccessFactors", "Beratung und Umsetzung")],
  pj_fine="Kunden nenne ich hier bewusst nicht namentlich. Für einen persönlichen Austausch teile ich gern Referenzen und stelle den Kontakt zu Ansprechpartnern her.",
  pf_eyebrow="Eigene Plattform", pf_h="STEGARC – eine Oberfläche über Ihren Systemen", pf_p="Meine KI-native Plattform, entstanden aus den Problemen, die ich in Transformationen immer wieder gesehen habe. Sie legt sich über bestehende Systeme und wächst Schritt für Schritt zu einem eigenständigen ERP.",
  mods=[("Experience Layer:", "ein Posteingang und ein Assistent über SAP, Microsoft 365, ServiceNow und Workday"), ("PE Command Center:", "Portfolio, Konsolidierung und Kennzahlen für Investoren und Holdings"), ("Business Suite:", "durchgängige Prozesse von Angebot bis Buchhaltung"), ("IT-Infrastruktur:", "Dimensionierung und Betriebsmodelle transparent durchgerechnet")],
  pf_cap="PE Command Center in der Live-Demo, mit synthetischen Daten", pf_alt="STEGARC PE Command Center: Kennzahlen eines Demo-Portfolios",
  ab_eyebrow="Über mich",
  about=["Ich bin Berater, Umsetzer und Unternehmer. Seit mehr als 20 Jahren bin ich dort, wo ERP-Projekte entschieden werden: in der Planung, im Cutover-Raum und am Montag nach dem Go-live.",
         "Ich komme aus der SAP-Beratung. 2011 habe ich mein eigenes Beratungsunternehmen gegründet und bis 2024 als Geschäftsführer geführt. In dieser Zeit und darüber hinaus leite ich SAP-Programme in DAX-Konzernen und international tätigen Unternehmen, mit den Schwerpunkten SAP S/4HANA, Central Finance und HR.",
         "In der Schweiz habe ich als Area Deployment Manager das Deployment einer Region in einem der größten SAP-S/4HANA-Rollouts verantwortet. Als Global Cutover Manager habe ich Go-lives über Länder und Zeitzonen hinweg gesteuert, als Programmleiter HR-Transformationen von SAP HCM nach SuccessFactors bis zum internationalen Rollout geführt. Und immer wieder habe ich Unternehmen in Sonderfällen begleitet: Lösung erarbeitet, umgesetzt und sauber in den Regelbetrieb übergeben. Zuletzt war ich als ERP Transformation Advisor und Solution Architect tätig.",
         "Dabei habe ich gelernt, dass Projekte selten an der Software scheitern. Sie scheitern an unklaren Entscheidungen, an fehlender Verantwortung für Sonderfälle und an Plänen, die nur auf Folien funktionieren. Genau dort setze ich an.",
         "Sie sprechen immer direkt mit mir. Meine Empfehlungen richten sich nach Ihrem Bedarf, nicht nach einem Partnerprogramm. Referenzen und Kontakte zu früheren Auftraggebern teile ich gern im persönlichen Gespräch.",
         "Ich lebe mit meiner Familie in Eppingen im Kraichgau. Ehrenamtlich führe ich als Vorsitzender und Cheftrainer einen Rollkunstlaufverein – Teamarbeit, Geduld und Leistung unter Druck kenne ich also auch abseits der IT."],
  tl_h="Stationen", timeline=[("Heute", "Marcel Wagner – STEGARC: ERP-Beratung, Sonderlösungen, KI und die Plattform STEGARC"), ("Zuletzt", "ERP Transformation Advisor und Solution Architect in einer international tätigen IT-Beratung"),
                              ("Programme", "SAP-Programmleitung in DAX-Konzernen, Area Deployment Manager in einem der größten S/4HANA-Rollouts, Global Cutover Manager, SAP Program Manager Finance"),
                              ("2011 bis 2024", "Gründer und Geschäftsführer eines eigenen SAP-Beratungsunternehmens"), ("Davor", "SAP-Beratung und Projektarbeit in Industrie, Handel und Dienstleistung")],
  sk_h="Schwerpunkte", skills=["SAP S/4HANA", "Central Finance", "SAP HCM und SuccessFactors", "Rollout und Deployment", "Programmleitung", "Cutover", "ECC-Ablösung", "RISE with SAP", "Microsoft Dynamics 365", "Oracle", "Lizenzen", "SAP Ariba", "KI und Automatisierung", "Sonderlösungen", "Datenmigration"],
  lg_h="Sprachen", lg="Deutsch, Englisch, Französisch",
  blog_h="Fachbeiträge", blog_all="Alle Beiträge", faq_h="Häufige Fragen",
  faq=[("Arbeiten Sie nur mit SAP?", "Nein. Mein Schwerpunkt liegt historisch bei SAP, ich berate aber herstellerunabhängig – auch zu Microsoft Dynamics 365, Oracle und ERP-Systemen für den Mittelstand.", "Nein. Mein Schwerpunkt liegt bei SAP, ich berate aber herstellerunabhängig, auch zu Microsoft Dynamics 365, Oracle und Mittelstands-ERP."),
       ("Was bedeutet das ECC-Wartungsende 2027 für uns?", 'Die Mainstream-Wartung für SAP ECC 6.0 endet Ende 2027. Danach gibt es kostenpflichtige Verlängerungen bis 2030 und unter Bedingungen darüber hinaus. <a href="blog/sap-ecc-wartungsende-2027.html">Ausführlich im Blog</a>.', "Die Mainstream-Wartung für SAP ECC 6.0 endet Ende 2027; danach gibt es kostenpflichtige Verlängerungen bis 2030 und unter Bedingungen darüber hinaus."),
       ("Bauen Sie auch Lösungen außerhalb des Standards?", "Ja, das ist ein Schwerpunkt: Erweiterungen, Schnittstellen, Portale und Services neben dem ERP-Kern – getestet, dokumentiert und updatefähig.", "Ja: Erweiterungen, Schnittstellen, Portale und Services neben dem ERP-Kern, getestet, dokumentiert und updatefähig."),
       ("Wie setzen Sie KI ein?", "Dort, wo sie messbar Arbeit abnimmt. Entscheidungen mit Wirkung wie Buchungen oder Zahlungen bestätigt immer ein Mensch.", "Dort, wo sie messbar Arbeit abnimmt; Buchungen oder Zahlungen bestätigt immer ein Mensch."),
       ("Gibt es Referenzen?", "Ja. Kunden nenne ich auf der Website bewusst nicht namentlich, teile Referenzen und Ansprechpartner aber gern im persönlichen Gespräch.", "Ja, Referenzen und Ansprechpartner teile ich gern im persönlichen Gespräch."),
       ("Wie startet eine Zusammenarbeit?", "Mit einem kostenfreien Erstgespräch. Danach schlage ich einen kompakten Einstieg vor, meist einen Workshop mit klarem Ergebnis.", "Mit einem kostenfreien Erstgespräch und danach meist einem Workshop mit klarem Ergebnis.")],
  ct_eyebrow="Kontakt", ct_h="Erzählen Sie mir, woran es gerade hakt.", ct_p="ERP-Entscheidung, laufendes Projekt, Sonderanforderung oder KI-Idee: Ich melde mich mit einem Vorschlag für ein erstes, kostenfreies Gespräch.",
  ct_subj="Anfrage%20%C3%BCber%20die%20Website", ct_mail="E-Mail schreiben", ct_call="Anrufen",
  ct_dl=[("Name", "Marcel Wagner"), ("E-Mail", '<a href="mailto:marcel.wagner@w-dfs.de">marcel.wagner@w-dfs.de</a>'), ("Mobil", '<a href="tel:+491791600252">0179 1600252</a>'), ("Anschrift", "Eichendorffstr. 38, 75031 Eppingen")])

EN = dict(lang="en", meta={"type": "home", "title": "ERP transformation, custom solutions and AI · Marcel Wagner – STEGARC",
  "description": "Premium B2B consulting for ERP transformation: SAP S/4HANA, Microsoft Dynamics, Oracle, cutover and go-live, custom solutions and AI. More than 20 years of experience.", "alt": "index.html"},
  anchors=dict(services="services", custom="custom", ai="ai", approach="approach", projects="projects", platform="platform", about="about", contact="contact"),
  eyebrow="Premium B2B consulting", h1a="Where others say no,", h1b="I get started.",
  lead="Vendor-independent ERP transformation, SAP S/4HANA, Microsoft Dynamics, Oracle, complex cutovers and go-lives, and AI solutions – with delivery strength, more than 20 years of experience and a clear focus on results.",
  cta="Book a first call",
  feats=[("layers", "ERP expertise", "vendor-independent"), ("target", "Transformation", "from strategy to go-live"), ("chip", "AI and data", "with measurable benefit")],
  shot_alt="STEGARC demo: dashboard with KPIs and open approvals from SAP, ServiceNow and Microsoft 365", shot_cap="STEGARC demo with synthetic data of fictitious companies",
  praxis_h="ERP transformation in practice.", praxis_p="Transparent steering, reliable data and measurable progress for a safe go-live. With STEGARC you see tasks, approvals and KPIs from all systems in one interface.",
  demo_q="?lang=en", demo_b="See the live demo", product="stegarc.en.html", product_b="Product page",
  svc_eyebrow="Services", svc_h="ERP, data and AI – from one hand.", svc_p="Six core services for successful transformations, complemented by data migration, custom development and the STEGARC platform.",
  svc=[("cube", "card-erp", "ERP transformation", "Strategy, target picture, architecture and delivery – vendor-independent and end-to-end.", ("blog/rise-with-sap-or-alternatives.html", "RISE or alternatives?")),
       ("layers", "card-s4", "SAP S/4HANA", "Planning, implementation, conversion and rollout – including Central Finance and international deployments.", ("blog/sap-ecc-end-of-maintenance-2027.html", "ECC end of maintenance 2027")),
       ("grid", "card-dyn", "Microsoft Dynamics", "Selection, implementation and harmonisation of business processes on Dynamics 365.", None),
       ("db", "card-ora", "Oracle", "Migration and integration in complex system landscapes – stable and future-proof.", None),
       ("play", "card-cut", "Cutover and go-live", "Planning, mock cutovers and orchestration for a safe production start with minimal risk.", ("blog/cutover-planning-go-live.html", "Ten cutover rules")),
       ("chip", "card-ki", "AI solutions", "Pragmatic AI use cases with human approval and measurable value for your processes.", ("blog/ai-in-erp-where-it-pays-off.html", "AI in ERP, done right"))],
  extra_label="Further focus areas",
  extra1=[("db", "Data migration", "Secure, efficient and audit-proof."), ("code", "Custom development", "Individual solutions for specific requirements."), ("layers", "STEGARC AI platform", "One interface across all systems.")],
  extra2=[("key", "Licence optimisation", "Making usage and contract transparent."), ("users", "HR and SuccessFactors", "From SAP HCM to global rollout."), ("flag", "Programme leadership and PE", "Interim roles, carve-outs, portfolio.")],
  fx_eyebrow="ERP projects that really deliver", fx_h="Complex programmes. Clear results.", fx_p="A structured approach, strong delivery and measurable benefit – from concept to go-live. From more than 20 years of programmes at DAX-listed groups and mid-sized companies.",
  sl_eyebrow="Custom solutions", sl_no="“Not possible.”", sl_yes="Possible. Just not in the standard.",
  sl_p="Many requirements do not fail on technology but because nobody wants to take responsibility for a solution outside the standard. I do – with an architecture that keeps the ERP core clean, with tests and with documentation your team can carry forward.",
  cases=[("Industry processes", "that no standard package covers"), ("Legacy systems and interfaces", "that will run for years"), ("Carve-outs and acquisitions", "with different ERP systems"), ("Portals and cockpits", "with data from several systems"), ("Migration special cases", "historical data, complex mappings"), ("Clean core", "extensions beside the core")],
  sl_cta="Describe your requirement", sl_blog="custom-solutions-when-standard-says-no.html", more_blog="More on the blog",
  ai_eyebrow="Artificial intelligence", ai_h="AI where it pays off.", ai_p="AI is not an end in itself. I use it where it takes repetitive work away, prepares decisions better or makes knowledge faster to find – and I say honestly when a classic rule is the better answer.",
  uses=[("Understanding documents:", "reading invoices, delivery notes and contracts and checking them against orders and goods receipts."), ("Explaining variances:", "why did the margin drop? Answers from the real data, with sources."), ("Preparing purchasing:", "comparing offers and preparing negotiations based on data."), ("One assistant for all systems:", "ERP, Microsoft 365, ServiceNow and Workday in one interface.")],
  ap_label="Example of an approval", ap_h="Assistant’s proposal", ap_msg="The invoice from Muster Metall GmbH matches the purchase order and goods receipt. Post it?",
  ap_dl=[("Amount", "€4,218.40"), ("Variance", "none"), ("Due", "12 Dec 2026")], ap_yes="Approve", ap_no="Reject",
  ap_note="Example with made-up data. Nothing is posted until a person approves – for postings, approvals and payments without exception.",
  st_eyebrow="Approach", st_h="Clear steps instead of endless projects", st_p="In every phase you know what happens, what it costs and what has to be decided next.",
  steps=[("Understand", "First call and a compact workshop on goals, systems and risks."), ("Decide", "Options with effort, benefit and risk for management or investors."), ("Build", "Delivery in manageable stages with tests and visible progress."), ("Go live", "Cutover, training and go-live with clear go/no-go criteria."), ("Live", "Hypercare and handover to your team.")],
  pj_eyebrow="Project experience", pj_h="From more than 20 years of practice", pj_p="Programmes at DAX-listed groups and internationally operating companies – and special cases in mid-sized businesses that had no standard answer.",
  work=[("Energy technology group, Switzerland", "One of the largest SAP S/4HANA rollouts", "Responsible for the deployment of a region: rollout planning, alignment with local entities, testing, cutover and go-live", "Area Deployment Manager"),
        ("DAX-listed groups", "SAP programme leadership: S/4HANA, Central Finance and HR", "Steering large SAP programmes across functions, entities and service providers through to handover into operations", "Programme lead"),
        ("Reinsurance, DAX-listed", "Global cutover management", "Cutover planning across countries and time zones, mock cutovers, go/no-go steering and training concept", "Global Cutover Manager and Training Lead"),
        ("Energy technology group, international", "HR transformation: SAP HCM to SuccessFactors", "Migration to Employee Central and SuccessFactors from strategy to international rollout", "Programme lead"),
        ("Industrial group, Switzerland", "Finance optimisation and AI in procurement", "SAP programme in finance and AI-supported automation around SAP Ariba, with human approval", "SAP Program Manager"),
        ("Several companies", "Special cases beyond the standard", "Solution designed, delivered, documented and handed over into regular operations", "Design, delivery, handover"),
        ("Agriculture and seeds, listed", "SAP licence optimisation", "Usage and contract analysed, licence assignment cleaned up, vendor talks prepared", "Advisory"),
        ("Mid-sized company", "HR transformation", "Migration from SAP HCM to Employee Central including the introduction of SuccessFactors", "Advisory and delivery")],
  pj_fine="I deliberately do not name clients here. For a personal exchange I am happy to share references and put you in touch with contacts.",
  pf_eyebrow="Own platform", pf_h="STEGARC – one interface over your systems", pf_p="My AI-native platform, born from the problems I kept seeing in transformations. It sits on top of existing systems and grows step by step into an ERP of its own.",
  mods=[("Experience Layer:", "one inbox and one assistant across SAP, Microsoft 365, ServiceNow and Workday"), ("PE Command Center:", "portfolio, consolidation and KPIs for investors and holdings"), ("Business Suite:", "end-to-end processes from quote to accounting"), ("IT infrastructure:", "sizing and operating models calculated transparently")],
  pf_cap="PE Command Center in the live demo, with synthetic data", pf_alt="STEGARC PE Command Center: KPIs of a demo portfolio",
  ab_eyebrow="About me",
  about=["I am a consultant, a doer and an entrepreneur. For more than 20 years I have been where ERP programmes are decided: in planning, in the cutover room and on the Monday after go-live.",
         "I come from SAP consulting. In 2011 I founded my own consulting company and ran it as managing director until 2024. During that time and beyond, I have been leading SAP programmes at DAX-listed groups and internationally operating companies, with a focus on SAP S/4HANA, Central Finance and HR.",
         "In Switzerland I was responsible, as Area Deployment Manager, for the deployment of a region in one of the largest SAP S/4HANA rollouts. As Global Cutover Manager I steered go-lives across countries and time zones; as programme lead I took HR transformations from SAP HCM to SuccessFactors through to international rollout. And again and again I have supported companies in special cases: solution designed, delivered and cleanly handed over into regular operations. Most recently I worked as ERP transformation advisor and solution architect.",
         "One thing I have learned is that projects rarely fail because of the software. They fail because of unclear decisions, because nobody owns the special cases, and because of plans that only work on slides. That is where I come in.",
         "You always talk to me directly. My recommendations follow your needs, not a partner programme. I am happy to share references and contacts with former clients in a personal conversation.",
         "I live with my family in Eppingen in south-west Germany. In my spare time I chair and head-coach an artistic roller skating club – so teamwork, patience and performance under pressure are familiar to me beyond IT as well."],
  tl_h="Career", timeline=[("Today", "Marcel Wagner – STEGARC: ERP consulting, custom solutions, AI and the STEGARC platform"), ("Most recently", "ERP Transformation Advisor and Solution Architect at an internationally operating IT consultancy"),
                           ("Programmes", "SAP programme leadership at DAX-listed groups, Area Deployment Manager in one of the largest S/4HANA rollouts, Global Cutover Manager, SAP Program Manager Finance"),
                           ("2011 to 2024", "Founder and managing director of my own SAP consulting company"), ("Before", "SAP consulting and project work in industry, retail and services")],
  sk_h="Focus areas", skills=["SAP S/4HANA", "Central Finance", "SAP HCM and SuccessFactors", "Rollout and deployment", "Programme leadership", "Cutover", "ECC replacement", "RISE with SAP", "Microsoft Dynamics 365", "Oracle", "Licensing", "SAP Ariba", "AI and automation", "Custom solutions", "Data migration"],
  lg_h="Languages", lg="German, English, French",
  blog_h="Articles", blog_all="All articles", faq_h="Frequently asked questions",
  faq=[("Do you only work with SAP?", "No. My background is mainly SAP, but I advise independently of vendors – including Microsoft Dynamics 365, Oracle and ERP systems for mid-sized companies.", "No. My background is mainly SAP, but I advise vendor-independently, including Microsoft Dynamics 365, Oracle and mid-market ERP."),
       ("What does the ECC end of maintenance in 2027 mean for us?", 'Mainstream maintenance for SAP ECC 6.0 ends at the end of 2027. Paid extensions run until 2030 and, under conditions, beyond. <a href="blog/sap-ecc-end-of-maintenance-2027.html">More on the blog</a>.', "Mainstream maintenance for SAP ECC 6.0 ends at the end of 2027; paid extensions run until 2030 and, under conditions, beyond."),
       ("Do you build solutions outside the standard?", "Yes, that is a core focus: extensions, interfaces, portals and services beside the ERP core – tested, documented and update-safe.", "Yes: extensions, interfaces, portals and services beside the ERP core, tested, documented and update-safe."),
       ("How do you use AI?", "Where it measurably takes work away. Decisions with impact such as postings or payments are always confirmed by a person.", "Where it measurably takes work away; postings or payments are always confirmed by a person."),
       ("Are there references?", "Yes. I deliberately do not name clients on the website, but I am happy to share references and contacts in a personal conversation.", "Yes, references and contacts are shared in a personal conversation."),
       ("How does working together start?", "With a free first call. Then I propose a compact start, usually a workshop with a clear result.", "With a free first call, usually followed by a workshop with a clear result.")],
  ct_eyebrow="Contact", ct_h="Tell me where things are stuck.", ct_p="An ERP decision, a running project, a special requirement or an AI idea: I will get back to you with a proposal for a first, free conversation.",
  ct_subj="Enquiry%20via%20the%20website", ct_mail="Send an e-mail", ct_call="Call",
  ct_dl=[("Name", "Marcel Wagner"), ("E-mail", '<a href="mailto:marcel.wagner@w-dfs.de">marcel.wagner@w-dfs.de</a>'), ("Mobile", '<a href="tel:+491791600252">+49 179 1600252</a>'), ("Address", "Eichendorffstr. 38, 75031 Eppingen, Germany")])


DE.update(dash_alt="Illustration: Laptop mit einem Dashboard aus Diagrammen, daneben Symbole für Daten, Cloud und KI", 
  lead2="Herstellerunabhängige ERP-Transformation, komplexe Systemlandschaften, Datenintegration, Cutover und produktive KI-Lösungen – mit Erfahrung, Umsetzungskraft und messbaren Ergebnissen.",
  cta2="Leistungen ansehen",
  svc2=[("cube", "card-erp", "ERP-Transformation", "Strategie, Zielbild, Architektur und Umsetzung.", ("blog/rise-with-sap-oder-alternativen.html", "RISE oder Alternativen?")),
        ("layers", "card-s4", "SAP S/4HANA", "Planung, Einführung, Conversion und Optimierung.", ("blog/sap-ecc-wartungsende-2027.html", "ECC-Wartungsende 2027")),
        ("grid", "card-dyn", "Microsoft Dynamics", "Einführung, Harmonisierung und skalierbarer Rollout.", None),
        ("db", "card-ora", "Oracle", "Einführung, Migration und Integration.", None),
        ("play", "card-cut", "Cutover &amp; Go-live", "Planung, Orchestrierung und sicherer Produktivstart.", ("blog/cutover-planung-go-live.html", "Zehn Regeln für den Cutover")),
        ("chip", "card-ki", "KI-Lösungen", "Pragmatische KI-Anwendungen mit messbarem Geschäftsnutzen.", ("blog/ki-im-erp-sinnvoll-einsetzen.html", "KI im ERP sinnvoll einsetzen"))],
  also="Außerdem:",
  praxis_p2="Transparente Steuerung, belastbare Daten und messbarer Projektfortschritt – für einen sicheren Go-live. Jeder Workstream, jede Datenmigration und jede Entscheidung bleibt nachvollziehbar.",
  praxis_b="So arbeite ich",
  mock=dict(aria="Konzeptdarstellung eines ERP-Programm-Cockpits mit Beispielwerten", title="ERP-Programm – Status", nav=["Übersicht", "Prozesse", "Daten", "Migration", "Cutover", "KI-Plattform", "Reporting"],
            k1="Projektfortschritt", k2="Go-live", k2v="in 14 Tagen", k3="Datenmigration", k4="Fortschritt nach Workstream", k5="System-Readiness",
            rows=[("S/4HANA", 85), ("Microsoft Dynamics", 79), ("Oracle", 90), ("Cutover", 80)], cap="Konzeptdarstellung mit Beispielwerten"),
  tech_eyebrow="STEGARC Technology", tech_h=["Eine Plattform.", "Alle Systeme.", "Volle Kontrolle."],
  pj_p2="Über 20 Jahre Programme in DAX-Konzernen und international tätigen Unternehmen – strukturiertes Vorgehen, starke Umsetzung und messbarer Nutzen, von der Konzeption bis zum Go-live. Und Sonderfälle im Mittelstand, für die es keine Standardantwort gab.")
EN.update(dash_alt="Illustration: laptop showing a dashboard of charts, next to symbols for data, cloud and AI", 
  lead2="Vendor-independent ERP transformation, complex system landscapes, data integration, cutover and productive AI solutions – with experience, delivery strength and measurable results.",
  cta2="See services",
  svc2=[("cube", "card-erp", "ERP transformation", "Strategy, target picture, architecture and delivery.", ("blog/rise-with-sap-or-alternatives.html", "RISE or alternatives?")),
        ("layers", "card-s4", "SAP S/4HANA", "Planning, implementation, conversion and optimisation.", ("blog/sap-ecc-end-of-maintenance-2027.html", "ECC end of maintenance 2027")),
        ("grid", "card-dyn", "Microsoft Dynamics", "Implementation, harmonisation and scalable rollout.", None),
        ("db", "card-ora", "Oracle", "Implementation, migration and integration.", None),
        ("play", "card-cut", "Cutover &amp; go-live", "Planning, orchestration and a safe production start.", ("blog/cutover-planning-go-live.html", "Ten cutover rules")),
        ("chip", "card-ki", "AI solutions", "Pragmatic AI applications with measurable business value.", ("blog/ai-in-erp-where-it-pays-off.html", "AI in ERP, done right"))],
  also="Also:",
  praxis_p2="Transparent steering, reliable data and measurable progress – for a safe go-live. Every workstream, every data migration and every decision stays traceable.",
  praxis_b="How I work",
  mock=dict(aria="Concept illustration of an ERP programme cockpit with sample values", title="ERP programme – status", nav=["Overview", "Processes", "Data", "Migration", "Cutover", "AI platform", "Reporting"],
            k1="Project progress", k2="Go-live", k2v="in 14 days", k3="Data migration", k4="Progress by workstream", k5="System readiness",
            rows=[("S/4HANA", 85), ("Microsoft Dynamics", 79), ("Oracle", 90), ("Cutover", 80)], cap="Concept illustration with sample values"),
  tech_eyebrow="STEGARC Technology", tech_h=["One platform.", "All systems.", "Full control."],
  pj_p2="More than 20 years of programmes at DAX-listed groups and internationally operating companies – a structured approach, strong delivery and measurable benefit, from concept to go-live. And special cases in mid-sized businesses that had no standard answer.")

(ROOT / "content/de/index.html").write_text(page(DE, ""), encoding="utf-8")
(ROOT / "content/en/index.html").write_text(page(EN, "../"), encoding="utf-8")
print("Startseiten erzeugt")
