# STEGARC – Homepage

Statische Website von Marcel Wagner – STEGARC (Einzelunternehmen, Eppingen) auf Deutsch und Englisch: Startseite, Blog, Impressum, Datenschutzerklärung.

- **Inhalte bearbeiten:** in `content/de/…` bzw. `content/en/…` (erste Zeile: `<!--META {…}-->` mit Titel, Beschreibung, Gegenstück in der anderen Sprache). Danach `python3 build.py` – erzeugt die Seiten im Stamm und unter `en/`, die Blog-Übersichten, `sitemap.xml` und `robots.txt`. Die erzeugten HTML-Dateien werden mit eingecheckt (GitHub Pages liefert sie direkt aus).
- **Neuer Blogbeitrag:** eine Datei je Sprache unter `content/de/blog/` und `content/en/blog/` mit `"type":"post"`, Datum, Lesezeit und Tags. Er erscheint automatisch in der Übersicht, auf der Startseite und in der Sitemap.
- **Datenschutz:** keine externen Ressourcen, keine Cookies, kein Tracking. Schrift lokal (SIL OFL 1.1, `assets/fonts/`).
- **Veröffentlichung:** GitHub Pages, Branch `main`, Ordner `/ (root)`. Adresse: https://marcelwagner-afk.github.io/stegarc-homepage/
- Bei Änderungen an Anschrift, Kontakt oder Hosting Impressum und Datenschutzerklärung (beide Sprachen) mitziehen.
