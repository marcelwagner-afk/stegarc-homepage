# Auftrag: Blogbeiträge für die Website „Marcel Wagner – STEGARC“

## Wer schreibt, für wen
- Autor: Marcel Wagner, Einzelunternehmer aus Eppingen (Baden-Württemberg). 15+ Jahre SAP: S/4HANA-Transformationen, Cutover-Management (u. a. als globaler Cutover-Manager), SAP-Lizenzoptimierung, mehrere SAP-HCM-Transformationen nach Employee Central/SuccessFactors bis zum internationalen Rollout (auch als Programmleiter), Schulung/Training, KI-Lösungen auf SAP (z. B. Einkaufsautomatisierung rund um SAP Ariba). Entwickelt STEGARC, eine KI-native Plattform (Experience Layer über SAP, Microsoft 365, ServiceNow, Workday; PE Command Center; Business Suite) – Status: in Entwicklung, Live-Demo mit synthetischen Daten.
- Positionierung: „Wir bauen Sonderlösungen, wo andere Nein sagen“ und „KI dort, wo sie sich wirklich lohnt“. Herstellerunabhängig, pragmatisch, ehrlich.
- Leser: CIOs, CFOs, IT-Leiter, SAP-Verantwortliche und Geschäftsführer im Mittelstand und gehobenen Mittelstand (DACH), Private-Equity-Portfolio-Verantwortliche.

## Ton und Stil
- Deutsch: „Sie“-Form, klar, konkret, ohne Buzzwords und Superlative, kurze Absätze. Ich-Perspektive des Autors erlaubt („In Projekten erlebe ich …“), aber KEINE erfundenen Projektgeschichten, Kundennamen, Zahlen oder Zitate.
- Englisch: eigenständige, natürlich formulierte Fassung (British English), keine Wort-für-Wort-Übersetzung, gleiche Fakten.
- 900–1.400 Wörter je Beitrag und Sprache. Struktur: Einleitung (Problem), 4–6 Zwischenüberschriften (h2, ggf. h3), mindestens eine Liste oder Tabelle, ein Abschnitt „Checkliste“ oder „Nächste Schritte“, ein kurzer FAQ-Teil (2–3 Fragen als h3 mit Antwort), am Ende „Quellen“ (de) bzw. „Sources“ (en) als Liste mit Links.

## Fakten – nur Belegtes
- Keine erfundenen Statistiken, Prozentsätze, Studien, Einsparquoten oder Kundenaussagen. Wenn eine Zahl nötig ist, nur mit Quelle (Link) – sonst qualitativ formulieren.
- Prüfe Fakten bei Bedarf per Websuche und verlinke die Quelle. Bevorzugt: SAP selbst, DSAG, Fachmedien (e3mag, Computerwoche, SAPinsider, ERP Today), EU-Amtsblatt/EU-Kommission.
- Bereits geprüfte Fakten (Stand Nov. 2026):
  - SAP ECC 6.0 / Business Suite 7: Mainstream-Wartung endet Ende 2027; Extended Maintenance 2028–2030 gegen 2 Prozentpunkte Aufschlag auf die Wartungsbasis; „SAP ERP, private edition, transition option“: Nutzung 2031–2033, nur nach Umzug auf SAP ERP private edition auf HANA bis 31.12.2030, Mindestgröße 2 TB, gekoppelt an Max Success Plan, ausdrücklich keine Wartungsverlängerung für SAP ERP (Quelle: https://sapinsider.org/blogs/sap-support-deadlines-2027-2030-2033/). S/4HANA-Wartung (Releases ab 2023) bis mindestens 2040 laut SAP (Quelle bei Nutzung prüfen).
  - EU AI Act: Pflicht zur KI-Kompetenz (Art. 4) gilt seit 2. Februar 2025; Verbote bestimmter Praktiken seit 2. Februar 2025; für Hochrisiko-Systeme nach Anhang III gibt es eine politische Einigung (Mai 2026, „Digital Omnibus“) auf Verschiebung bis 2. Dezember 2027 (Quelle: https://www.boerse-express.com/news/articles/eu-ai-act-recruiting-ki-muss-erst-bis-dezember-2027-konform-sein-915211). Vorsichtig formulieren, keine Rechtsberatung.
  - SAP Digital Access (indirekte Nutzung): dokumentbasiertes Lizenzmodell (9 Dokumenttypen), seit 2018 (Quellen: https://www.computerwoche.de/article/2773378/sap-regelt-indirekte-nutzung-neu.html, https://e3mag.com/de/neues-sap-lizenzmodell-alte-herausforderungen/).
- Keine Rechts-, Steuer- oder Finanzberatung; bei rechtlichen Punkten Hinweis „keine Rechtsberatung“.
- Marken (SAP, S/4HANA …) korrekt schreiben; keine Aussage, dass Marcel SAP-Partner ist.

## SEO
- Ein klares Haupt-Keyword pro Beitrag (im Titel, in der ersten Passage, in einer h2, in der Meta-Beschreibung), verwandte Begriffe natürlich verwenden. Kein Keyword-Stuffing.
- Titel ≤ 65 Zeichen, Meta-Beschreibung 140–160 Zeichen.
- 2–3 interne Links: zu anderen Beiträgen (Pfade siehe unten, relativ: `sap-ecc-wartungsende-2027.html` usw.) und zur Startseite (`../#leistungen`, `../#kontakt`; Englisch: `../#services`, `../#contact`).
- Am Ende des Textes einen Satz mit Bezug zu einem Leistungsangebot (kein aggressives Verkaufen).

## Dateiformat
Pro Beitrag zwei Dateien, UTF-8:
- `content/de/blog/<slug-de>.html` und `content/en/blog/<slug-en>.html` (Basis: /home/claude/stegarc-homepage/)
- Erste Zeile exakt ein Kommentar mit JSON, z. B.:
  `<!--META {"type":"post","title":"…","description":"…","lead":"Ein bis zwei Sätze Teaser.","date":"2026-11-19","read":7,"tags":["SAP ECC","S/4HANA"],"alt":"en/blog/<slug-en>.html"}-->`
  (in der englischen Datei: `"alt":"blog/<slug-de>.html"`). `read` = Lesezeit in Minuten (Wörter/200, gerundet).
- Danach nur der Artikeltext als HTML-Fragment: `<h2>`, `<h3>`, `<p>`, `<ul>/<ol>/<li>`, `<table>` (mit `<thead>`), `<strong>`, `<em>`, `<a>`, `<blockquote>` für hervorgehobene Merksätze (nicht für Zitate Dritter). KEIN `<h1>` (kommt aus dem Rahmen), kein `<html>`, `<head>`, kein CSS, kein JS.
- Externe Links mit `rel="noopener"`.

## Beiträge und Slugs
| # | Deutsch (Slug) | Englisch (Slug) | Haupt-Keyword DE / EN |
|---|---|---|---|
| 1 | sap-ecc-wartungsende-2027 | sap-ecc-end-of-maintenance-2027 | SAP ECC Wartungsende 2027 / SAP ECC end of maintenance |
| 2 | rise-with-sap-oder-alternativen | rise-with-sap-or-alternatives | RISE with SAP Alternativen / RISE with SAP alternatives |
| 3 | cutover-planung-go-live | cutover-planning-go-live | Cutover-Planung SAP / SAP cutover planning |
| 4 | sap-hcm-zu-successfactors | sap-hcm-to-successfactors | SAP HCM Migration SuccessFactors / SAP HCM to SuccessFactors migration |
| 5 | sap-lizenzen-optimieren | optimise-sap-licences | SAP Lizenzoptimierung / SAP licence optimisation |
| 6 | ki-im-erp-sinnvoll-einsetzen | ai-in-erp-where-it-pays-off | KI im ERP / AI in ERP |
| 7 | sonderloesungen-wenn-der-standard-nein-sagt | custom-solutions-when-standard-says-no | individuelle Softwarelösung SAP / custom SAP solutions |

Inhaltliche Leitplanken:
1. ECC-Wartungsende: Fristen klar erklären (Tabelle), Optionen (Brownfield/Greenfield/Bluefield bzw. selektive Datenübernahme, RISE, Third-Party-Support, Weiterbetrieb mit Risiko, Alternative ERP), Entscheidungskriterien, realistischer Zeitbedarf qualitativ, Checkliste.
2. RISE vs. Alternativen: was RISE umfasst (Bündel aus S/4HANA Cloud Private Edition, Infrastruktur, Services), Vor-/Nachteile, Vertragspunkte, die man prüfen sollte, on-premise mit Kauflizenz, andere Anbieter, Kriterienkatalog (Tabelle). Neutral.
3. Cutover: Cutover-Plan, Generalproben (Mock Cutovers), Datenmigration und Abgleich, Freeze-Zeiten, Go/No-Go-Kriterien, Hypercare, Kommunikation, Rollenmodell; 10 praxisnahe Regeln.
4. HCM → SuccessFactors: Optionen (Employee Central, Side-by-Side, Core Hybrid, SAP HCM for S/4HANA als On-Prem-Alternative – nur nennen, wenn per Quelle bestätigt), Datenmodell, Payroll-Fragen, Länder-Rollout, Change & Training, typische Stolpersteine.
5. Lizenzen: Nutzertypen und tatsächliche Nutzung, Shelfware, Digital Access/indirekte Nutzung, Vorbereitung auf Audit und Verhandlung, Lizenzwechsel bei S/4/RISE; keine Einsparversprechen.
6. KI im ERP: wo KI sich lohnt (Dokumentenverarbeitung, Rechnungseingang, Abweichungsanalyse, Assistenten über mehrere Systeme, Einkauf/Verhandlungsvorbereitung, Wissenssuche), wo nicht (deterministische Buchungslogik, fehlende Datenqualität), menschliche Freigabe („KI bucht nichts ohne Freigabe“), Datenschutz/AI-Act-Kompetenzpflicht, Vorgehen in kleinen Piloten mit messbaren Zielen.
7. Sonderlösungen: wann der Standard an Grenzen stößt (Branchenprozesse, Schnittstellen, Altsysteme, Carve-outs, Konsolidierung), Clean-Core-Prinzip (Erweiterungen außerhalb des Kerns, z. B. Side-by-Side auf BTP oder eigenständige Services), Make-or-Buy-Kriterien, Wartbarkeit, wie man Sonderlösungen sauber dokumentiert und testet; Botschaft: „Nein“ ist oft nur „nicht im Standard“.
