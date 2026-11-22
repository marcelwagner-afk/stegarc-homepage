"""Erzeugt content/de/index.html und content/en/index.html (Startseite) aus einem Textsatz je Sprache.
Danach build.py ausführen. Icons als Inline-SVG, Bilder aus assets/photo."""
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

from urllib.parse import quote
MAIL = "marcel.wagner@w-dfs.de"
def mailto(subj): return f"mailto:{MAIL}?subject={quote(subj)}"

# kleine Bildsymbole für die drei Nutzen-Säulen (Inline-SVG, 64x64)
PILLAR = {
 "impact": '<svg viewBox="0 0 64 64" width="64" height="64" fill="none" aria-hidden="true"><rect x="1" y="1" width="62" height="62" rx="14" fill="#E6F7F6"/><path d="M14 46h36" stroke="#9FB3C8" stroke-width="1.5"/><rect x="17" y="34" width="6" height="12" rx="1.5" fill="#9FDCD8"/><rect x="27" y="28" width="6" height="18" rx="1.5" fill="#5CC9C3"/><rect x="37" y="22" width="6" height="24" rx="1.5" fill="#00B8B0"/><path d="M16 30 28 22l8 3 12-9" stroke="#07152B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="48" cy="16" r="2.5" fill="#07152B"/></svg>',
 "tech": '<svg viewBox="0 0 64 64" width="64" height="64" fill="none" aria-hidden="true"><rect x="1" y="1" width="62" height="62" rx="14" fill="#E6F7F6"/><path d="M32 32 18 20M32 32l14-12M32 32 18 44M32 32l14 12" stroke="#5CC9C3" stroke-width="1.8"/><rect x="25" y="25" width="14" height="14" rx="3" fill="#00B8B0"/><rect x="12" y="14" width="11" height="11" rx="2.5" fill="#fff" stroke="#07152B" stroke-width="1.6"/><rect x="41" y="14" width="11" height="11" rx="2.5" fill="#fff" stroke="#07152B" stroke-width="1.6"/><rect x="12" y="39" width="11" height="11" rx="2.5" fill="#fff" stroke="#07152B" stroke-width="1.6"/><rect x="41" y="39" width="11" height="11" rx="2.5" fill="#fff" stroke="#07152B" stroke-width="1.6"/></svg>',
 "exec": '<svg viewBox="0 0 64 64" width="64" height="64" fill="none" aria-hidden="true"><rect x="1" y="1" width="62" height="62" rx="14" fill="#E6F7F6"/><path d="M12 36h40" stroke="#9FB3C8" stroke-width="1.8" stroke-dasharray="2 3"/><path d="M12 36h26" stroke="#00B8B0" stroke-width="2.4" stroke-linecap="round"/><circle cx="14" cy="36" r="3.5" fill="#00B8B0"/><circle cx="26" cy="36" r="3.5" fill="#00B8B0"/><circle cx="38" cy="36" r="3.5" fill="#00B8B0"/><circle cx="50" cy="36" r="4.5" fill="#fff" stroke="#07152B" stroke-width="1.8"/><path d="M50 31V17l9 4-9 4" stroke="#07152B" stroke-width="1.8" stroke-linejoin="round"/></svg>',
}

def page(L, r):
    t = L; a = t["anchors"]
    proof = "".join(f'<li><b>{h}</b><span>{p}</span></li>' for h, p in t["proof"])
    pillars = "".join(f'<article class="card pillar reveal">{PILLAR[k]}<span class="for">{who}</span><h3>{h}</h3><p>{p}</p><p class="val"><b>{t["val_label"]}</b> {v}</p></article>'
                      for k, who, h, p, v in t["pillars"])
    svc = "".join(f'<article class="card reveal"><div class="band" aria-hidden="true">{photo(pic, "", r)}</div><div class="body"><h3>{h}</h3><p>{p}</p>'
                  f'<ul class="topics">{"".join(f"<li>{x}</li>" for x in topics)}</ul>'
                  f'<a class="more" href="{lk[0]}">{lk[1]} {ic("arrow", 16, "")}</a></div></article>'
                  for pic, h, p, topics, lk in t["caps"])
    rows = "".join(f'<tr><th scope="row">{c}</th><td data-l="{t["oc_cols"][1]}">{ap}</td><td data-l="{t["oc_cols"][2]}">{v}</td></tr>' for c, ap, v in t["oc_rows"])
    cases = "".join(f'<div class="card"><b>{h}</b><span>{p}</span></div>' for h, p in t["cases"])
    uses = "".join(f'<li>{ic("check", 18, "")}<span><b>{h}</b> {p}</span></li>' for h, p in t["uses"])
    steps = "".join(f'<li><b>{h}</b><span>{p}</span><em>{o}</em></li>' for h, p, o in t["steps"])
    why = "".join(f'<li>{ic(i, 26)}<span><b>{h}</b>{p}</span></li>' for i, h, p in t["why"])
    work = "".join(f'<li><span class="who">{w}</span><span class="what"><b>{h}</b><span>{p}</span></span><span class="role">{ro}</span></li>' for w, h, p, ro in t["work"])
    pf = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in t["pf_facts"])
    mods = "".join(f'<li>{ic("check", 20, "")}<span><b>{h}</b>{p}</span><em class="st st-{c}">{lbl}</em></li>' for h, p, c, lbl in t["mods"])
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
      <p class="lead">{t["lead"]}</p>
      <div class="cta"><a class="btn btn-primary" href="#{a["contact"]}">{t["cta"]} {ARROW}</a><a class="btn btn-secondary" href="#{a["services"]}">{t["cta2"]}</a></div>
    </div>
    <ul class="proof" aria-label="{t["proof_label"]}">{proof}</ul>
  </div>
</section>

<section class="section" id="{a["value"]}" aria-labelledby="val-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["val_eyebrow"]}</div><h2 id="val-h">{t["val_h"]}</h2><p class="intro">{t["val_p"]}</p></div>
    <div class="pillars">{pillars}</div>
  </div>
</section>

<section class="section alt" id="{a["services"]}" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["svc_eyebrow"]}</div><h2 id="svc-h">{t["svc_h"]}</h2><p class="intro">{t["svc_p"]}</p></div>
    <div class="svc">{svc}</div>
  </div>
</section>

<section class="section" id="{a["outcomes"]}" aria-labelledby="oc-h">
  <div class="wrap">
    <div class="head reveal"><div class="eyebrow">{t["oc_eyebrow"]}</div><h2 id="oc-h">{t["oc_h"]}</h2><p class="intro">{t["oc_p"]}</p></div>
    <div class="card outcomes reveal"><table><thead><tr><th scope="col">{t["oc_cols"][0]}</th><th scope="col">{t["oc_cols"][1]}</th><th scope="col">{t["oc_cols"][2]}</th></tr></thead><tbody>{rows}</tbody></table></div>
    <p class="fine">{t["oc_fine"]}</p>
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
        <dl class="pffacts">{pf}</dl>
      </div>
      <figure class="monitor reveal"><div class="screen"><img src="{r}assets/stegarc-demo-{t["lang"]}.jpg" width="1600" height="965" alt="{t["shot_alt"]}" loading="lazy" decoding="async"></div><div class="stand" aria-hidden="true"></div><figcaption>{t["shot_cap"]}</figcaption></figure>
    </div>
    <div class="modwrap reveal"><h3>{t["mods_h"]}</h3><ul class="caps mods">{mods}</ul>
      <div class="cta"><a class="btn btn-primary" href="https://marcelwagner-afk.github.io/stegarc-suite/index.html{t["demo_q"]}">{t["demo_b"]} {ARROW}</a><a class="btn btn-secondary" href="https://marcelwagner-afk.github.io/stegarc-suite/{t["product"]}">{t["product_b"]}</a></div></div>
  </div>
</section>

<section class="section dark" id="{a["ai"]}" aria-labelledby="ai-h" style="padding-top:0">
  <div class="wrap split">
    <div class="reveal"><div class="eyebrow">{t["ai_eyebrow"]}</div><h2 id="ai-h">{t["ai_h"]}</h2><p class="intro">{t["ai_p"]}</p><ul class="uses">{uses}</ul>
      <p class="ctx"><a href="{mailto(t["ai_subj"])}">{t["ai_cta"]} {ic("arrow", 16, "")}</a></p></div>
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
    <div class="cta reveal"><a class="btn btn-primary" href="{mailto(t["sl_subj"])}">{t["sl_cta"]} {ARROW}</a><a class="btn btn-secondary" href="blog/{t["sl_blog"]}">{t["more_blog"]}</a></div>
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
    <div class="head reveal"><div class="eyebrow">{t["pj_eyebrow"]}</div><h2 id="pj-h">{t["pj_h"]}</h2><p class="intro">{t["pj_p"]}</p></div>
    <ul class="why reveal">{why}</ul>
    <h3 class="subh reveal">{t["work_h"]}</h3>
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
    <div class="head rowhead reveal"><div><div class="eyebrow">{t["blog_eyebrow"]}</div><h2 id="bl-h">{t["blog_h"]}</h2></div><a class="btn btn-secondary" href="blog/">{t["blog_all"]}</a></div>
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
      <ul class="ctlist">{"".join(f"<li>{ic('check', 18, '')}<span>{x}</span></li>" for x in t["ct_list"])}</ul>
      <div class="cta"><a class="btn btn-primary" href="{mailto(t["ct_subj"])}">{t["ct_mail"]} {ARROW}</a><a class="btn btn-secondary" href="tel:+491791600252">{t["ct_call"]}</a></div></div>
    <dl class="reveal">{"".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in t["ct_dl"])}</dl>
  </div>
</section>
'''

# ------------------------------------------------------------------
# Texte. Englisch ist die Referenzfassung (Executive Narrative), Deutsch gleichwertig.
# Nur belegte Angaben; Zielnutzen ist als Ziel formuliert, nicht als Ergebnis.
# ------------------------------------------------------------------
CONTACT_DL = {
 "de": [("Ansprechpartner", "Marcel Wagner, Inhaber"), ("E-Mail", f'<a href="mailto:{MAIL}">{MAIL}</a>'), ("Mobil", '<a href="tel:+491791600252">0179 1600252</a>'), ("Anschrift", "Eichendorffstr. 38, 75031 Eppingen")],
 "en": [("Your contact", "Marcel Wagner, founder"), ("E-mail", f'<a href="mailto:{MAIL}">{MAIL}</a>'), ("Mobile", '<a href="tel:+491791600252">+49 179 1600252</a>'), ("Address", "Eichendorffstr. 38, 75031 Eppingen, Germany")],
}

EN = dict(lang="en",
  meta={"type": "home", "title": "STEGARC – Independent ERP Transformation Advisory | Marcel Wagner",
        "description": "Independent ERP transformation advisory led by Marcel Wagner: strategy, SAP S/4HANA, Microsoft Dynamics and Oracle programmes, cutover and go-live, custom engineering and applied AI.", "alt": "index.html"},
  anchors=dict(value="value", services="services", outcomes="outcomes", platform="platform", ai="ai", custom="custom", approach="approach", projects="projects", about="about", contact="contact"),
  eyebrow="Independent ERP transformation advisory",
  h1a="Complex ERP transformation.", h1b="Clear business outcomes.",
  lead="STEGARC connects business strategy, enterprise technology and hands-on engineering – from the first decision to a stable go-live. Vendor-independent and led personally by Marcel Wagner.",
  cta="Discuss your transformation", cta2="Explore capabilities",
  proof_label="Experience at a glance",
  proof=[("20+ years", "leading ERP and SAP programmes"), ("DAX groups", "and international multi-country rollouts"), ("Vendor-independent", "SAP, Microsoft Dynamics, Oracle")],

  val_eyebrow="Why it matters", val_h="Three things a transformation has to deliver.",
  val_p="Every programme is judged on business impact, sound technology and whether it actually reaches go-live. STEGARC works on all three at once.",
  val_label="Your value:",
  pillars=[("impact", "For CEO, CFO and investors", "Business impact", "Tie the transformation budget to operating performance, financial transparency and a business case that holds up after go-live.", "decisions based on cost, benefit and risk – not on vendor roadmaps."),
           ("tech", "For CIO and CTO", "Technology excellence", "Design, modernise and integrate ERP systems, data flows and intelligent applications – with a clean core and an architecture your team can run.", "a target landscape that is maintainable, upgradable and open to AI."),
           ("exec", "For COO and programme owners", "Execution confidence", "Close the gap between plan and production: governance, rehearsed cutovers, clear go/no-go criteria and a controlled handover to operations.", "fewer surprises on the way to go-live and a stable first month.")],

  svc_eyebrow="Capabilities", svc_h="Six capabilities. One accountable partner.",
  svc_p="From strategy to day-to-day operations. Each capability is backed by programme experience – not by a slide.",
  caps=[("svc-erp", "Strategic advisory", "ERP strategy, roadmaps and investment decisions for management and investors.", ["ECC end of maintenance 2027 and RISE options", "Business cases and licence optimisation", "Carve-outs and portfolio companies"], (mailto("Discuss your ERP strategy"), "Discuss your ERP strategy")),
        ("svc-s4", "Enterprise transformation", "ERP transformation on SAP S/4HANA, Microsoft Dynamics 365 and Oracle – vendor-independent.", ["SAP S/4HANA and Central Finance", "HR: SAP HCM to SuccessFactors", "Target architecture and clean core"], ("blog/rise-with-sap-or-alternatives.html", "RISE or alternatives?")),
        ("svc-cut", "Programme delivery and cutover", "Programme leadership, international deployment and a controlled path to production.", ["Programme governance and steering", "Multi-country rollouts", "Cutover, mock runs and hypercare"], ("blog/cutover-planning-go-live.html", "Ten cutover rules")),
        ("svc-ora", "Data and migration", "Reliable data as the basis for go-live, reporting and later AI use.", ["Data migration and reconciliation", "Integrated finance data with Central Finance", "Reporting across systems"], (mailto("Discuss your data challenges"), "Discuss your data challenges")),
        ("svc-dyn", "Engineering and integration", "Custom solutions beside the ERP core where the standard ends.", ["Extensions, interfaces and services", "Portals and cockpits across systems", "Legacy integration and special cases"], (mailto("Talk about your architecture"), "Talk about your architecture")),
        ("svc-ki", "AI and intelligent automation", "Applied AI in ERP processes – with a person approving every decision that matters.", ["Document processing and three-way match", "Variance explanations with sources", "Procurement automation around SAP Ariba"], ("blog/ai-in-erp-where-it-pays-off.html", "AI in ERP, done right"))],

  oc_eyebrow="From complexity to business value", oc_h="Where transformations get stuck – and what helps.",
  oc_p="Typical challenges in ERP programmes, the approach STEGARC takes and the value it is designed to create.",
  oc_cols=["Business challenge", "STEGARC approach", "Intended business value"],
  oc_rows=[("Fragmented systems after acquisitions or growth", "ERP modernisation and integration with a clear target architecture", "Consistent processes and one version of the numbers"),
           ("Limited financial transparency", "Integrated finance data (e.g. Central Finance) and management reporting", "Better-founded decisions for management and investors"),
           ("ECC end of maintenance 2027 approaching", "Option assessment: conversion, new implementation, RISE or alternatives", "A decision based on cost, risk and timing – not on pressure"),
           ("High manual effort in finance and procurement", "Automation and applied AI with human approval", "Less routine work, faster cycle times"),
           ("Risky go-live in a complex landscape", "Structured governance, rehearsed cutovers, go/no-go criteria", "Predictable go-live and a stable first month")],
  oc_fine="Illustrative examples. The value column describes the intended effect, not a guaranteed result; it depends on scope, starting point and collaboration.",

  tech_eyebrow="STEGARC Technology", tech_h=["One platform.", "All systems.", "Full control."],
  pf_p="People in finance, procurement and IT switch between SAP, Microsoft 365, ServiceNow and Workday all day. STEGARC is an AI-native layer on top of these systems – one inbox, one assistant and shared KPIs, without replacing what already runs.",
  pf_facts=[("Business problem", "Work and data spread across many systems; decisions wait for reports."), ("Solution", "One interface over existing systems, growing step by step into an ERP of its own."), ("Intended users", "Finance, procurement, IT and holding or private equity teams."), ("Status", "Working prototype with a public live demo on synthetic data. Not yet in production use.")],
  shot_alt="STEGARC demo: dashboard with KPIs and open approvals from SAP, ServiceNow and Microsoft 365", shot_cap="STEGARC demo with synthetic data of fictitious companies",
  mods_h="Modules in the live demo",
  mods=[("Experience Layer", "one inbox and one assistant across SAP, Microsoft 365, ServiceNow and Workday", "demo", "Prototype"),
        ("PE Command Center", "portfolio, consolidation and KPIs for investors and holdings", "demo", "Prototype"),
        ("Business Suite", "end-to-end processes from quote to accounting", "demo", "Prototype"),
        ("IT infrastructure", "sizing and operating models calculated transparently", "demo", "Prototype")],
  demo_q="?lang=en", demo_b="See the live demo", product="stegarc.en.html", product_b="Product page",

  ai_eyebrow="Applied AI", ai_h="AI where it pays off.", ai_p="AI is not an end in itself. It is used where it takes repetitive work away, prepares decisions or makes knowledge faster to find – and a classic rule is used where that is the better answer.",
  uses=[("Understanding documents:", "reading invoices, delivery notes and contracts and checking them against orders and goods receipts."), ("Explaining variances:", "why did the margin drop? Answers from the real data, with sources."), ("Preparing purchasing:", "comparing offers and preparing negotiations based on data."), ("One assistant for all systems:", "ERP, Microsoft 365, ServiceNow and Workday in one interface.")],
  ai_cta="Explore intelligent automation", ai_subj="Explore intelligent automation",
  dash_alt="Illustration: laptop showing a dashboard of charts, next to symbols for data, cloud and AI",
  ap_label="Example of an approval", ap_h="Assistant’s proposal", ap_msg="The invoice from Muster Metall GmbH matches the purchase order and goods receipt. Post it?",
  ap_dl=[("Amount", "€4,218.40"), ("Variance", "none"), ("Due", "12 Dec 2026")], ap_yes="Approve", ap_no="Reject",
  ap_note="Example with made-up data. Nothing is posted until a person approves – for postings, approvals and payments without exception.",

  sl_eyebrow="Custom solutions", sl_no="“Not possible.”", sl_yes="Possible. Just not in the standard.",
  sl_p="Many requirements do not fail on technology but because nobody takes responsibility for a solution outside the standard. STEGARC does – with an architecture that keeps the ERP core clean, with tests and with documentation your team can carry forward.",
  cases=[("Industry processes", "that no standard package covers"), ("Legacy systems and interfaces", "that will run for years"), ("Carve-outs and acquisitions", "with different ERP systems"), ("Portals and cockpits", "with data from several systems"), ("Migration special cases", "historical data, complex mappings"), ("Clean core", "extensions beside the core")],
  sl_cta="Describe your requirement", sl_subj="Requirement outside the standard", sl_blog="custom-solutions-when-standard-says-no.html", more_blog="More on the blog",

  st_eyebrow="Approach", st_h="Clear steps instead of endless projects.", st_p="In every phase you know what happens, what it costs and what has to be decided next.",
  steps=[("Understand", "First call and a compact workshop on goals, systems and risks.", "Result: shared picture of goals and risks"),
         ("Decide", "Options with effort, benefit and risk for management or investors.", "Result: decision paper"),
         ("Build", "Delivery in manageable stages with tests and visible progress.", "Result: tested increments"),
         ("Go live", "Cutover, training and go-live with clear go/no-go criteria.", "Result: controlled go-live"),
         ("Run", "Hypercare and handover to your team.", "Result: stable operations")],

  pj_eyebrow="Experience", pj_h="Why you can trust STEGARC with critical programmes.",
  pj_p="Experience from programmes at DAX-listed groups and international companies – and from special cases that had no standard answer.",
  why=[("flag", "Programme responsibility at scale", "Led the deployment of a region in one of the largest SAP S/4HANA rollouts and steered go-lives across countries and time zones."),
       ("users", "Business owner perspective", "Founder and managing director of an SAP consultancy from 2011 to 2024 – with responsibility for budgets and clients."),
       ("key", "Independent advice", "Not tied to a vendor partner programme: recommendations follow your requirements."),
       ("target", "Senior and direct", "You work with Marcel Wagner personally – no hand-off to a junior team after the sales meeting.")],
  work_h="Selected programmes",
  work=[("Energy technology group, Switzerland", "One of the largest SAP S/4HANA rollouts", "Responsible for the deployment of a region: rollout planning, alignment with local entities, testing, cutover and go-live", "Area Deployment Manager"),
        ("DAX-listed groups", "SAP programme leadership: S/4HANA, Central Finance and HR", "Steering large SAP programmes across functions, entities and service providers through to handover into operations", "Programme lead"),
        ("Reinsurance, DAX-listed", "Global cutover management", "Cutover planning across countries and time zones, mock cutovers, go/no-go steering and training concept", "Global Cutover Manager and Training Lead"),
        ("Energy technology group, international", "HR transformation: SAP HCM to SuccessFactors", "Migration to Employee Central and SuccessFactors from strategy to international rollout", "Programme lead"),
        ("Industrial group, Switzerland", "Finance optimisation and AI in procurement", "SAP programme in finance and AI-supported automation around SAP Ariba, with human approval", "SAP Program Manager"),
        ("Several companies", "Special cases beyond the standard", "Solution designed, delivered, documented and handed over into regular operations", "Design, delivery, handover"),
        ("Agriculture and seeds, listed", "SAP licence optimisation", "Usage and contract analysed, licence assignment cleaned up, vendor talks prepared", "Advisory"),
        ("Mid-sized company", "HR transformation", "Migration from SAP HCM to Employee Central including the introduction of SuccessFactors", "Advisory and delivery")],
  pj_fine="Clients are deliberately not named here. References and contacts with former clients are shared in a personal conversation.",

  ab_eyebrow="About me",
  about=["I am Marcel Wagner and I lead STEGARC personally – as consultant, programme lead and entrepreneur. For more than 20 years I have worked where ERP programmes are decided: in planning, in the cutover room and on the Monday after go-live.",
         "From 2011 to 2024 I founded and ran my own SAP consultancy. Alongside, I led SAP programmes at DAX-listed groups and international companies, with a focus on SAP S/4HANA, Central Finance and HR. Most recently I worked as ERP transformation advisor and solution architect.",
         "My conviction: projects rarely fail because of the software. They fail because of unclear decisions, because nobody owns the special cases, and because of plans that only work on slides. That is where STEGARC comes in.",
         "I live with my family in Eppingen in south-west Germany and chair and head-coach an artistic roller skating club – teamwork and performance under pressure beyond IT."],
  tl_h="Career", timeline=[("Today", "STEGARC: ERP transformation advisory, custom solutions, AI and the STEGARC platform"), ("Most recently", "ERP Transformation Advisor and Solution Architect at an internationally operating IT consultancy"),
                           ("Programmes", "SAP programme leadership at DAX-listed groups, Area Deployment Manager in one of the largest S/4HANA rollouts, Global Cutover Manager, SAP Program Manager Finance"),
                           ("2011 to 2024", "Founder and managing director of my own SAP consultancy"), ("Before", "SAP consulting and project work in industry, retail and services")],
  sk_h="Focus areas", skills=["SAP S/4HANA", "Central Finance", "SAP HCM and SuccessFactors", "Rollout and deployment", "Programme leadership", "Cutover", "ECC replacement", "RISE with SAP", "Microsoft Dynamics 365", "Oracle", "Licensing", "SAP Ariba", "AI and automation", "Custom solutions", "Data migration"],
  lg_h="Languages", lg="German, English, French",
  blog_eyebrow="Insights", blog_h="Articles for decision-makers", blog_all="All articles", faq_h="Frequently asked questions",
  faq=[("Who will I work with?", "With Marcel Wagner personally – from the first call to go-live. STEGARC is a focused advisory practice, not a large firm with changing teams.", "With Marcel Wagner personally, from the first call to go-live."),
       ("Do you only work with SAP?", "No. The background is mainly SAP, but STEGARC advises independently of vendors – including Microsoft Dynamics 365, Oracle and ERP systems for mid-sized companies.", "No. The background is mainly SAP, but STEGARC advises vendor-independently, including Microsoft Dynamics 365, Oracle and mid-market ERP."),
       ("What does the ECC end of maintenance in 2027 mean for us?", 'Mainstream maintenance for SAP ECC 6.0 ends at the end of 2027. Paid extensions run until 2030 and, under conditions, beyond. <a href="blog/sap-ecc-end-of-maintenance-2027.html">More on the blog</a>.', "Mainstream maintenance for SAP ECC 6.0 ends at the end of 2027; paid extensions run until 2030 and, under conditions, beyond."),
       ("Is the STEGARC platform ready for production?", "Not yet. It is a working prototype with a public live demo on synthetic data. Advisory and delivery services do not depend on it.", "Not yet; it is a working prototype with a public live demo on synthetic data."),
       ("How do you use AI?", "Where it measurably takes work away. Decisions with impact such as postings or payments are always confirmed by a person.", "Where it measurably takes work away; postings or payments are always confirmed by a person."),
       ("Are there references?", "Yes. Clients are deliberately not named on the website; references and contacts are shared in a personal conversation.", "Yes, references and contacts are shared in a personal conversation."),
       ("How does working together start?", "With a free first call. Then a compact start is proposed, usually a workshop with a clear result.", "With a free first call, usually followed by a workshop with a clear result.")],
  ct_eyebrow="Contact", ct_h="Discuss your transformation.", ct_p="An ERP decision, a programme at risk, a requirement outside the standard or an AI idea – a short message is enough.",
  ct_list=["First call free of charge and without obligation", "Directly with Marcel Wagner – no sales team", "References shared on request"],
  ct_subj="Enquiry via the website", ct_mail="Send an e-mail", ct_call="Call",
  ct_dl=CONTACT_DL["en"])

DE = dict(lang="de",
  meta={"type": "home", "title": "STEGARC – Unabhängige Beratung für ERP-Transformation | Marcel Wagner",
        "description": "Unabhängige Beratung für ERP-Transformation, persönlich geführt von Marcel Wagner: Strategie, SAP-S/4HANA-, Microsoft-Dynamics- und Oracle-Programme, Cutover und Go-live, Sonderlösungen und angewandte KI.", "alt": "en/index.html"},
  anchors=dict(value="nutzen", services="leistungen", outcomes="ergebnisse", platform="plattform", ai="ki", custom="sonderloesungen", approach="vorgehen", projects="projekte", about="ueber", contact="kontakt"),
  eyebrow="Unabhängige Beratung für ERP-Transformation",
  h1a="Komplexe ERP‑Transformation.", h1b="Klare Ergebnisse.",
  lead="STEGARC verbindet Unternehmensstrategie, Enterprise-Technologie und konkrete Umsetzung – von der ersten Entscheidung bis zum stabilen Go-live. Herstellerunabhängig und persönlich geführt von Marcel Wagner.",
  cta="Transformation besprechen", cta2="Leistungen ansehen",
  proof_label="Erfahrung auf einen Blick",
  proof=[("Über 20 Jahre", "Leitung von ERP- und SAP-Programmen"), ("DAX-Konzerne", "und internationale Rollouts über Länder hinweg"), ("Herstellerunabhängig", "SAP, Microsoft Dynamics, Oracle")],

  val_eyebrow="Worauf es ankommt", val_h="Drei Dinge, die eine Transformation liefern muss.",
  val_p="Jedes Programm wird am Geschäftsnutzen gemessen, an tragfähiger Technik und daran, ob es den Go-live wirklich erreicht. STEGARC arbeitet an allen dreien zugleich.",
  val_label="Ihr Nutzen:",
  pillars=[("impact", "Für Geschäftsführung, CFO und Investoren", "Geschäftsnutzen", "Das Transformationsbudget an Betriebsleistung, finanzielle Transparenz und einen Business Case knüpfen, der auch nach dem Go-live trägt.", "Entscheidungen nach Kosten, Nutzen und Risiko – nicht nach Hersteller-Roadmaps."),
           ("tech", "Für CIO und CTO", "Technische Exzellenz", "ERP-Systeme, Datenflüsse und intelligente Anwendungen entwerfen, modernisieren und integrieren – mit sauberem Kern und einer Architektur, die Ihr Team betreiben kann.", "eine Ziellandschaft, die wartbar, updatefähig und offen für KI ist."),
           ("exec", "Für COO und Programmverantwortliche", "Sichere Umsetzung", "Die Lücke zwischen Plan und Produktion schließen: Governance, geprobte Cutover, klare Go/No-Go-Kriterien und eine kontrollierte Übergabe an den Betrieb.", "weniger Überraschungen auf dem Weg zum Go-live und ein stabiler erster Monat.")],

  svc_eyebrow="Leistungen", svc_h="Sechs Leistungsfelder. Ein verantwortlicher Partner.",
  svc_p="Von der Strategie bis zum laufenden Betrieb. Hinter jedem Leistungsfeld steht Programmerfahrung – keine Folie.",
  caps=[("svc-erp", "Strategische Beratung", "ERP-Strategie, Roadmaps und Investitionsentscheidungen für Geschäftsführung und Investoren.", ["ECC-Wartungsende 2027 und RISE-Optionen", "Business Cases und Lizenzoptimierung", "Carve-outs und Portfoliounternehmen"], (mailto("ERP-Strategie besprechen"), "ERP-Strategie besprechen")),
        ("svc-s4", "ERP-Transformation", "ERP-Transformation auf SAP S/4HANA, Microsoft Dynamics 365 und Oracle – herstellerunabhängig.", ["SAP S/4HANA und Central Finance", "HR: SAP HCM zu SuccessFactors", "Zielarchitektur und Clean Core"], ("blog/rise-with-sap-oder-alternativen.html", "RISE oder Alternativen?")),
        ("svc-cut", "Programmsteuerung und Cutover", "Programmleitung, internationales Deployment und ein kontrollierter Weg in die Produktion.", ["Programm-Governance und Steuerung", "Rollouts über mehrere Länder", "Cutover, Generalproben und Hypercare"], ("blog/cutover-planung-go-live.html", "Zehn Regeln für den Cutover")),
        ("svc-ora", "Daten und Migration", "Belastbare Daten als Grundlage für Go-live, Reporting und späteren KI-Einsatz.", ["Datenmigration und Abstimmung", "Integrierte Finanzdaten mit Central Finance", "Reporting über Systemgrenzen"], (mailto("Datenthemen besprechen"), "Datenthemen besprechen")),
        ("svc-dyn", "Engineering und Integration", "Sonderlösungen neben dem ERP-Kern, wo der Standard endet.", ["Erweiterungen, Schnittstellen und Services", "Portale und Cockpits über mehrere Systeme", "Altsysteme und Sonderfälle"], (mailto("Architektur besprechen"), "Architektur besprechen")),
        ("svc-ki", "KI und intelligente Automatisierung", "Angewandte KI in ERP-Prozessen – jede Entscheidung mit Wirkung gibt ein Mensch frei.", ["Belegverarbeitung und Dreifachabgleich", "Abweichungen erklären, mit Quellen", "Einkaufsautomatisierung rund um SAP Ariba"], ("blog/ki-im-erp-sinnvoll-einsetzen.html", "KI im ERP sinnvoll einsetzen"))],

  oc_eyebrow="Von Komplexität zu Geschäftsnutzen", oc_h="Wo Transformationen hängen – und was hilft.",
  oc_p="Typische Herausforderungen in ERP-Programmen, der Ansatz von STEGARC und der Nutzen, auf den er zielt.",
  oc_cols=["Herausforderung", "Ansatz von STEGARC", "Angestrebter Nutzen"],
  oc_rows=[("Zersplitterte Systeme nach Zukäufen oder Wachstum", "ERP-Modernisierung und Integration mit klarer Zielarchitektur", "Einheitliche Prozesse und eine Version der Zahlen"),
           ("Zu wenig finanzielle Transparenz", "Integrierte Finanzdaten (z. B. Central Finance) und Management-Reporting", "Fundiertere Entscheidungen für Geschäftsführung und Investoren"),
           ("ECC-Wartungsende 2027 rückt näher", "Optionen bewerten: Conversion, Neueinführung, RISE oder Alternativen", "Eine Entscheidung nach Kosten, Risiko und Zeitpunkt – nicht unter Druck"),
           ("Viel Handarbeit in Finanzen und Einkauf", "Automatisierung und angewandte KI mit menschlicher Freigabe", "Weniger Routinearbeit, kürzere Durchlaufzeiten"),
           ("Riskanter Go-live in komplexer Landschaft", "Strukturierte Governance, geprobte Cutover, Go/No-Go-Kriterien", "Planbarer Go-live und ein stabiler erster Monat")],
  oc_fine="Beispiele zur Veranschaulichung. Die rechte Spalte beschreibt die angestrebte Wirkung, kein garantiertes Ergebnis; sie hängt von Umfang, Ausgangslage und Zusammenarbeit ab.",

  tech_eyebrow="STEGARC Technology", tech_h=["Eine Plattform.", "Alle Systeme.", "Volle Kontrolle."],
  pf_p="Menschen in Finanzen, Einkauf und IT wechseln den ganzen Tag zwischen SAP, Microsoft 365, ServiceNow und Workday. STEGARC ist eine KI-native Ebene über diesen Systemen – ein Posteingang, ein Assistent und gemeinsame Kennzahlen, ohne zu ersetzen, was bereits läuft.",
  pf_facts=[("Problem", "Arbeit und Daten verteilen sich auf viele Systeme; Entscheidungen warten auf Berichte."), ("Lösung", "Eine Oberfläche über bestehenden Systemen, die Schritt für Schritt zu einem eigenständigen ERP wächst."), ("Für wen", "Finanzen, Einkauf, IT sowie Holding- und Private-Equity-Teams."), ("Stand", "Funktionsfähiger Prototyp mit öffentlicher Live-Demo auf synthetischen Daten. Noch nicht im Produktiveinsatz.")],
  shot_alt="STEGARC-Demo: Dashboard mit Kennzahlen und offenen Freigaben aus SAP, ServiceNow und Microsoft 365", shot_cap="STEGARC-Demo mit synthetischen Daten fiktiver Unternehmen",
  mods_h="Module in der Live-Demo",
  mods=[("Experience Layer", "ein Posteingang und ein Assistent über SAP, Microsoft 365, ServiceNow und Workday", "demo", "Prototyp"),
        ("PE Command Center", "Portfolio, Konsolidierung und Kennzahlen für Investoren und Holdings", "demo", "Prototyp"),
        ("Business Suite", "durchgängige Prozesse von Angebot bis Buchhaltung", "demo", "Prototyp"),
        ("IT-Infrastruktur", "Dimensionierung und Betriebsmodelle transparent durchgerechnet", "demo", "Prototyp")],
  demo_q="", demo_b="Live-Demo ansehen", product="stegarc.html", product_b="Produktseite",

  ai_eyebrow="Angewandte KI", ai_h="KI dort, wo sie sich lohnt.", ai_p="KI ist kein Selbstzweck. Sie kommt dort zum Einsatz, wo sie wiederkehrende Arbeit abnimmt, Entscheidungen vorbereitet oder Wissen schneller auffindbar macht – und eine klassische Regel dort, wo sie die bessere Lösung ist.",
  uses=[("Dokumente verstehen:", "Rechnungen, Lieferscheine und Verträge auslesen und gegen Bestellung und Wareneingang prüfen."), ("Abweichungen erklären:", "Warum ist die Marge gesunken? Antworten aus den echten Daten, mit Quellen."), ("Einkauf vorbereiten:", "Angebote vergleichen und Verhandlungen auf Datenbasis vorbereiten."), ("Ein Assistent für alle Systeme:", "ERP, Microsoft 365, ServiceNow und Workday in einer Oberfläche.")],
  ai_cta="Automatisierung besprechen", ai_subj="Intelligente Automatisierung besprechen",
  dash_alt="Illustration: Laptop mit einem Dashboard aus Diagrammen, daneben Symbole für Daten, Cloud und KI",
  ap_label="Beispiel einer Freigabe", ap_h="Vorschlag des Assistenten", ap_msg="Die Rechnung von Muster Metall GmbH passt zu Bestellung und Wareneingang. Soll sie gebucht werden?",
  ap_dl=[("Betrag", "4.218,40 €"), ("Abweichung", "keine"), ("Fällig", "12.12.2026")], ap_yes="Freigeben", ap_no="Ablehnen",
  ap_note="Beispiel mit erfundenen Daten. Gebucht wird erst, wenn ein Mensch freigibt – bei Buchungen, Freigaben und Zahlungen ohne Ausnahme.",

  sl_eyebrow="Sonderlösungen", sl_no="„Geht nicht.“", sl_yes="Geht. Nur nicht im Standard.",
  sl_p="Viele Anforderungen scheitern nicht an der Technik, sondern daran, dass niemand die Verantwortung für eine Lösung außerhalb des Standards übernimmt. STEGARC übernimmt sie – mit einer Architektur, die den ERP-Kern sauber hält, mit Tests und mit einer Dokumentation, die Ihr Team weiterführen kann.",
  cases=[("Branchenprozesse", "die kein Standardpaket abbildet"), ("Altsysteme und Schnittstellen", "die noch Jahre laufen werden"), ("Carve-outs und Zukäufe", "mit unterschiedlichen ERP-Systemen"), ("Portale und Cockpits", "mit Daten aus mehreren Systemen"), ("Migrations-Sonderfälle", "historische Daten, komplexe Mappings"), ("Clean Core", "Erweiterungen neben dem Kern")],
  sl_cta="Anforderung schildern", sl_subj="Anforderung außerhalb des Standards", sl_blog="sonderloesungen-wenn-der-standard-nein-sagt.html", more_blog="Mehr im Blog",

  st_eyebrow="Vorgehen", st_h="Klare Schritte statt endloser Projekte.", st_p="Sie wissen in jeder Phase, was passiert, was es kostet und was als Nächstes entschieden werden muss.",
  steps=[("Verstehen", "Erstgespräch und kompakter Workshop zu Zielen, Systemen und Risiken.", "Ergebnis: gemeinsames Bild von Zielen und Risiken"),
         ("Entscheiden", "Optionen mit Aufwand, Nutzen und Risiken für Geschäftsführung oder Investoren.", "Ergebnis: Entscheidungsvorlage"),
         ("Bauen", "Umsetzung in überschaubaren Etappen mit Tests und sichtbaren Zwischenständen.", "Ergebnis: getestete Etappen"),
         ("Einführen", "Cutover, Schulung und Go-live mit klaren Go/No-Go-Kriterien.", "Ergebnis: kontrollierter Go-live"),
         ("Betreiben", "Hypercare und Übergabe an Ihr Team.", "Ergebnis: stabiler Betrieb")],

  pj_eyebrow="Erfahrung", pj_h="Warum Sie STEGARC kritische Programme anvertrauen können.",
  pj_p="Erfahrung aus Programmen in DAX-Konzernen und international tätigen Unternehmen – und aus Sonderfällen, für die es keine Standardantwort gab.",
  why=[("flag", "Programmverantwortung in großem Maßstab", "Deployment einer Region in einem der größten SAP-S/4HANA-Rollouts verantwortet und Go-lives über Länder und Zeitzonen gesteuert."),
       ("users", "Unternehmerische Perspektive", "Von 2011 bis 2024 Gründer und Geschäftsführer einer SAP-Beratung – mit Verantwortung für Budget und Kunden."),
       ("key", "Unabhängige Beratung", "Nicht an ein Partnerprogramm eines Herstellers gebunden: Empfehlungen richten sich nach Ihren Anforderungen."),
       ("target", "Senior und direkt", "Sie arbeiten persönlich mit Marcel Wagner – keine Übergabe an ein Junior-Team nach dem Vertriebstermin.")],
  work_h="Ausgewählte Programme",
  work=[("Energietechnik-Konzern, Schweiz", "Einer der größten SAP-S/4HANA-Rollouts", "Verantwortung für das Deployment einer Region: Rollout-Planung, Abstimmung mit den lokalen Gesellschaften, Tests, Cutover und Go-live", "Area Deployment Manager"),
        ("DAX-Konzerne", "SAP-Programmleitung S/4HANA, Central Finance und HR", "Steuerung großer SAP-Programme über Fachbereiche, Gesellschaften und Dienstleister hinweg bis zur Übergabe in den Betrieb", "Programmleitung"),
        ("Rückversicherung, DAX-Konzern", "Globales Cutover-Management", "Cutover-Planung über Länder und Zeitzonen, Generalproben, Go/No-Go-Steuerung und Schulungskonzept", "Global Cutover Manager und Training Lead"),
        ("Energietechnik-Konzern, international", "HR-Transformation: SAP HCM zu SuccessFactors", "Migration nach Employee Central und SuccessFactors von der Strategie bis zum internationalen Rollout", "Programmleitung"),
        ("Industriekonzern, Schweiz", "Finance-Optimierung und KI im Einkauf", "SAP-Programm im Finanzbereich sowie KI-gestützte Automatisierung rund um SAP Ariba, mit menschlicher Freigabe", "SAP Program Manager"),
        ("Mehrere Unternehmen", "Sonderfälle jenseits des Standards", "Lösung erarbeitet, umgesetzt, dokumentiert und in den Regelbetrieb übergeben", "Konzeption, Umsetzung, Übergabe"),
        ("Agrar und Saatgut, börsennotiert", "SAP-Lizenzoptimierung", "Nutzung und Vertrag analysiert, Lizenzzuordnung bereinigt, Herstellergespräche vorbereitet", "Beratung"),
        ("Mittelstand", "HR-Transformation", "Migration von SAP HCM nach Employee Central mit Einführung von SuccessFactors", "Beratung und Umsetzung")],
  pj_fine="Kunden werden hier bewusst nicht namentlich genannt. Referenzen und Kontakte zu früheren Auftraggebern teilt Marcel Wagner gern im persönlichen Gespräch.",

  ab_eyebrow="Über mich",
  about=["Ich bin Marcel Wagner und führe STEGARC persönlich – als Berater, Programmleiter und Unternehmer. Seit mehr als 20 Jahren arbeite ich dort, wo ERP-Programme entschieden werden: in der Planung, im Cutover-Raum und am Montag nach dem Go-live.",
         "Von 2011 bis 2024 habe ich mein eigenes SAP-Beratungsunternehmen gegründet und geführt. Parallel dazu habe ich SAP-Programme in DAX-Konzernen und international tätigen Unternehmen geleitet, mit den Schwerpunkten SAP S/4HANA, Central Finance und HR. Zuletzt war ich als ERP Transformation Advisor und Solution Architect tätig.",
         "Meine Überzeugung: Projekte scheitern selten an der Software. Sie scheitern an unklaren Entscheidungen, an fehlender Verantwortung für Sonderfälle und an Plänen, die nur auf Folien funktionieren. Genau dort setzt STEGARC an.",
         "Ich lebe mit meiner Familie in Eppingen im Kraichgau und führe ehrenamtlich als Vorsitzender und Cheftrainer einen Rollkunstlaufverein – Teamarbeit und Leistung unter Druck auch abseits der IT."],
  tl_h="Stationen", timeline=[("Heute", "STEGARC: Beratung für ERP-Transformation, Sonderlösungen, KI und die Plattform STEGARC"), ("Zuletzt", "ERP Transformation Advisor und Solution Architect in einer international tätigen IT-Beratung"),
                              ("Programme", "SAP-Programmleitung in DAX-Konzernen, Area Deployment Manager in einem der größten S/4HANA-Rollouts, Global Cutover Manager, SAP Program Manager Finance"),
                              ("2011 bis 2024", "Gründer und Geschäftsführer eines eigenen SAP-Beratungsunternehmens"), ("Davor", "SAP-Beratung und Projektarbeit in Industrie, Handel und Dienstleistung")],
  sk_h="Schwerpunkte", skills=["SAP S/4HANA", "Central Finance", "SAP HCM und SuccessFactors", "Rollout und Deployment", "Programmleitung", "Cutover", "ECC-Ablösung", "RISE with SAP", "Microsoft Dynamics 365", "Oracle", "Lizenzen", "SAP Ariba", "KI und Automatisierung", "Sonderlösungen", "Datenmigration"],
  lg_h="Sprachen", lg="Deutsch, Englisch, Französisch",
  blog_eyebrow="Fachbeiträge", blog_h="Beiträge für Entscheider", blog_all="Alle Beiträge", faq_h="Häufige Fragen",
  faq=[("Mit wem arbeite ich zusammen?", "Mit Marcel Wagner persönlich – vom Erstgespräch bis zum Go-live. STEGARC ist eine fokussierte Beratung, kein großes Haus mit wechselnden Teams.", "Mit Marcel Wagner persönlich, vom Erstgespräch bis zum Go-live."),
       ("Arbeiten Sie nur mit SAP?", "Nein. Der Schwerpunkt liegt historisch bei SAP, STEGARC berät aber herstellerunabhängig – auch zu Microsoft Dynamics 365, Oracle und ERP-Systemen für den Mittelstand.", "Nein. Der Schwerpunkt liegt bei SAP, STEGARC berät aber herstellerunabhängig, auch zu Microsoft Dynamics 365, Oracle und Mittelstands-ERP."),
       ("Was bedeutet das ECC-Wartungsende 2027 für uns?", 'Die Mainstream-Wartung für SAP ECC 6.0 endet Ende 2027. Danach gibt es kostenpflichtige Verlängerungen bis 2030 und unter Bedingungen darüber hinaus. <a href="blog/sap-ecc-wartungsende-2027.html">Ausführlich im Blog</a>.', "Die Mainstream-Wartung für SAP ECC 6.0 endet Ende 2027; danach gibt es kostenpflichtige Verlängerungen bis 2030 und unter Bedingungen darüber hinaus."),
       ("Ist die Plattform STEGARC produktiv einsetzbar?", "Noch nicht. Sie ist ein funktionsfähiger Prototyp mit öffentlicher Live-Demo auf synthetischen Daten. Beratung und Umsetzung hängen nicht von ihr ab.", "Noch nicht; sie ist ein funktionsfähiger Prototyp mit öffentlicher Live-Demo auf synthetischen Daten."),
       ("Wie setzen Sie KI ein?", "Dort, wo sie messbar Arbeit abnimmt. Entscheidungen mit Wirkung wie Buchungen oder Zahlungen bestätigt immer ein Mensch.", "Dort, wo sie messbar Arbeit abnimmt; Buchungen oder Zahlungen bestätigt immer ein Mensch."),
       ("Gibt es Referenzen?", "Ja. Kunden werden auf der Website bewusst nicht namentlich genannt; Referenzen und Ansprechpartner gibt es im persönlichen Gespräch.", "Ja, Referenzen und Ansprechpartner gibt es im persönlichen Gespräch."),
       ("Wie startet eine Zusammenarbeit?", "Mit einem kostenfreien Erstgespräch. Danach folgt ein Vorschlag für einen kompakten Einstieg, meist ein Workshop mit klarem Ergebnis.", "Mit einem kostenfreien Erstgespräch und danach meist einem Workshop mit klarem Ergebnis.")],
  ct_eyebrow="Kontakt", ct_h="Lassen Sie uns über Ihre Transformation sprechen.", ct_p="ERP-Entscheidung, Programm in Schieflage, Anforderung außerhalb des Standards oder eine KI-Idee – eine kurze Nachricht genügt.",
  ct_list=["Erstgespräch kostenfrei und unverbindlich", "Direkt mit Marcel Wagner – ohne Vertriebsteam", "Referenzen auf Anfrage"],
  ct_subj="Anfrage über die Website", ct_mail="E-Mail schreiben", ct_call="Anrufen",
  ct_dl=CONTACT_DL["de"])

(ROOT / "content/de/index.html").write_text(page(DE, ""), encoding="utf-8")
(ROOT / "content/en/index.html").write_text(page(EN, "../"), encoding="utf-8")
print("Startseiten erzeugt")
