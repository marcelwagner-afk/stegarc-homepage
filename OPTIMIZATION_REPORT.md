# STEGARC – Executive Website Optimization Report

| | |
|---|---|
| Branch | `feature/executive-optimization` |
| Starting point | `main` 78b7c4b, live since 20 Nov 2026 |
| Date | 22 Nov 2026 |
| Recoverable original | `main` stays untouched until approval; every earlier state is tagged in Git history |

## Decisions taken with the owner

- **Language:** English is the reference version of the executive narrative. German remains the default language for the DACH market and was rewritten to the same standard. Legal pages remain German, with courtesy English translations.
- **Voice:** STEGARC speaks as the brand. Trust, About and Contact are deliberately personal (Marcel Wagner). There is no "we" that would suggest a team that does not exist.
- **Headline:** chosen after evaluation (see section 3).

## 1. Executive audit of the previous version (scores 1–10)

| Perspective | First impression | Credibility | Clarity | Business relevance | Differentiation | Visual quality | Navigation | Conversion |
|---|---|---|---|---|---|---|---|---|
| CEO | 7 | 6 | 6 | 5 | 7 | 8 | 7 | 6 |
| CFO | 6 | 6 | 6 | 4 | 6 | 8 | 7 | 5 |
| CIO | 7 | 7 | 7 | 6 | 6 | 8 | 7 | 6 |
| CTO | 7 | 6 | 7 | 6 | 7 | 8 | 7 | 6 |
| COO | 6 | 6 | 6 | 5 | 6 | 8 | 7 | 5 |
| Private equity | 6 | 5 | 5 | 4 | 6 | 8 | 7 | 5 |
| Procurement | 6 | 6 | 6 | 5 | 5 | 8 | 7 | 5 |

### Strengths

- Strong, distinctive brand line: "Where others say no, I get started."
- Credible, anonymised programme list.
- Honest AI positioning with human approval.
- Clean design system and excellent technical quality: Lighthouse 98–100.

### Weaknesses

- The hero said what is *different* but not what is *delivered*, and for whom.
- The page was technology- and vendor-centred, organised by product name (SAP, Dynamics, Oracle) rather than by business problem.
- No connection between services and business value. CFO and investor questions went unanswered.
- The platform was presented next to consulting services without a clear development status, which risked it being read as a production product.
- Trust arguments were spread across About and FAQ; there was no single "why trust" answer.
- A concept dashboard with sample numbers ("82 %", "in 14 days") sat high on the page. It could be read as a client result, and it overloaded the first screen.
- CTAs were generic, with no contextual entry points per topic.

### Ten highest-impact improvements (all implemented)

1. Hero rewritten around *what, for whom and next step*, plus a verified proof bar.
2. Three executive value pillars (impact, technology, execution), each addressed to its audience.
3. Services restructured into six capability areas organised by business problem.
4. New section "From complexity to business value", clearly marked as illustrative.
5. Platform section states problem, solution, intended users and status, with a status badge per module.
6. A dedicated trust block with four verified reasons.
7. Contextual CTAs: mailto links with a pre-filled subject per topic, each a functioning destination.
8. Approach steps now name the deliverable of each phase.
9. New FAQ entries for "Who will I work with?" and "Is the platform production-ready?"
10. The concept dashboard with fictitious figures was removed from the top of the page.

## 2. Content architecture (home page, both languages)

| # | Section | Reading depth | Purpose |
|---|---|---|---|
| 1 | Hero: headline, supporting line, primary and secondary CTA, proof bar | 5 s | Who, what, why it matters, next step |
| 2 | Value pillars: Business impact · Technology excellence · Execution confidence | 30 s | Business relevance per audience |
| 3 | Capabilities: Strategic advisory · Enterprise transformation · Programme delivery and cutover · Data and migration · Engineering and integration · AI and intelligent automation | 30 s → 3 min | Find a relevant service |
| 4 | From complexity to business value: challenge / approach / intended value table | 30 s | Outcome narrative |
| 5 | STEGARC Technology: problem, solution, users, status, plus modules with status and demo | 3 min | Innovation without overstatement |
| 6 | Applied AI, with the human approval example | 3 min | Demonstrated principle |
| 7 | Custom solutions: "Not possible." → "Possible. Just not in the standard." | 30 s | Brand differentiation |
| 8 | Approach: five steps, each with its result | 3 min | Delivery model, predictability |
| 9 | Experience: four trust reasons and eight anonymised programmes | 30 s → 3 min | Why trust |
| 10 | About me | 3 min | Leadership expertise |
| 11 | Insights (blog) and FAQ | 3 min | Depth, objection handling |
| 12 | Contact | – | Conversion |

### CTA hierarchy

- **Primary:** "Discuss your transformation" / „Transformation besprechen". It appears in the hero and in the contact section.
- **Secondary:** "Explore capabilities" / „Leistungen ansehen".
- **Contextual**, as text links rather than buttons:
  - Discuss your ERP strategy
  - Discuss your data challenges
  - Talk about your architecture
  - Explore intelligent automation
  - Describe your requirement
  - Blog deep-dives

## 3. Headline evaluation

| Candidate | Assessment |
|---|---|
| "Where others say no, I get started." (previous) | Memorable and distinctive. It does not say *what* STEGARC delivers, so it fails the five-second test. |
| "Complex Transformation. Clear Business Outcomes." (brief) | Clear and executive, but generic: "transformation" could mean anything. |
| "ERP transformation that reaches go-live." | Concrete and credible, but narrow and less aspirational. |
| **"Complex ERP transformation. Clear business outcomes."** | **Chosen.** It names the field (ERP), the difficulty (complex) and the promise (outcomes), without a superlative. |

DE: „Komplexe ERP‑Transformation. Klare Ergebnisse."

The previous line is kept as the brand statement of the custom-solutions section.

## 4. Content changes

### Content removed (documented)

- **Concept dashboard ("ERP programme – status") with sample percentages.** The figures could be mistaken for client results; the brief also warns against overloaded dashboards. The `appmock` code and its CSS were deleted; the content is recoverable from `main`.
- **"Further focus areas" row and "Also:" line.** Their content was merged into the capability cards: licence optimisation → Strategic advisory, HR/SuccessFactors → Enterprise transformation, PE/carve-outs → Strategic advisory, data migration → Data and migration.

### New content (verified sources only)

- **Proof bar:** 20+ years, DAX groups and international rollouts, vendor independence. Source: owner statements and the existing About text.
- **Trust reasons:**
  - Area Deployment Manager role
  - Founder and MD 2011–2024
  - No partner programme
  - Personal delivery
- **Platform status:** "working prototype, public live demo on synthetic data, not yet in production use".
- **Outcome table:** labelled as *intended* value, explicitly "not a guaranteed result".

### Wording rules applied

- None of the brief's banned phrases are used.
- No superlatives without a source.
- No client names, logos, testimonials, certifications or revenue figures.

### SEO

- New titles and meta descriptions for both home pages.
- Existing anchors kept (`#services`, `#leistungen`, `#projects`, `#projekte`, `#contact`, `#kontakt`) so that blog links and external links keep working.

## 5. UX/UI changes

- **New components:**
  - Proof bar
  - Pillar cards with small explanatory graphics: bar chart, connected systems, milestone path
  - Topic lists in the capability cards
  - Responsive outcome table, which becomes labelled stacked cards on mobile
  - Platform fact grid
  - Module status badges
  - Trust grid
  - Contact checklist
- **Navigation:** Capabilities · Platform · Approach · Experience · About (DE: Leistungen · Plattform · Vorgehen · Erfahrung · Über mich).
- **Design system unchanged:** Inter, navy/teal tokens, light consulting sections and dark technology sections. The existing images are all kept.
- **Mobile:** the hero headline scales down at ≤480 px so that "ERP‑Transformation" never overflows (non-breaking hyphen).

## 6. Technical changes

- `tools/make_home.py`: new page structure, texts for EN and DE, a `mailto()` helper for contextual CTAs, inline SVG pillar visuals, and the mock dashboard removed.
- `assets/style.css`: new components added and obsolete styles removed (`.praxis`, `.app`, `.laptop`, `.feats`, `.extra`, `.also`).
- `build.py`:
  - New navigation.
  - The blog index has a visually hidden `h2`, which fixes the heading order: accessibility went from 98 to 100.
- `tools/test_site.py`:
  - Test width 430 px added.
  - New check for elements reaching past the viewport.
  - New check for contextual mailto CTAs.
- No new dependencies.

## 7. Executive validation (simulated, after implementation)

| Visitor | Offering clear? | Value clear? | Credible? | Technically convincing? | Relevant service? | Differentiated? | Would contact? | Main remaining objection |
|---|---|---|---|---|---|---|---|---|
| CEO | 9 | 8 | 7 | 8 | 8 | 8 | 7 | Single senior advisor: what if the programme needs a team? |
| CFO | 8 | 7 | 7 | 7 | 8 | 7 | 6 | No quantified case study, no engagement or pricing model. |
| CIO | 9 | 8 | 8 | 8 | 9 | 7 | 7 | Security and compliance not addressed. |
| CTO | 8 | 7 | 7 | 7 | 7 | 8 | 6 | Little detail on the platform architecture and stack. |
| COO | 9 | 8 | 8 | 8 | 8 | 7 | 7 | — |
| PE investor | 8 | 7 | 6 | 7 | 7 | 7 | 6 | No portfolio case; the PE Command Center is a prototype. |
| Procurement | 8 | 7 | 7 | 7 | 8 | 6 | 6 | Capacity of a sole proprietorship; no framework terms. |

Changes made in response:
- The FAQ now answers "Who will I work with?" openly.
- The platform status appears both in the section and in the FAQ.
- The experience headline was changed from "Why clients trust STEGARC" to "Why you can trust STEGARC", because STEGARC as a new firm must not imply its own client base.

## 8. Remaining recommendations (need input from the owner)

These are content placeholders; none of them were filled with invented content.

1. **[PLACEHOLDER] Two or three quotes from former clients or programme leads**, with their written consent. Name and company may stay anonymous.
2. **[PLACEHOLDER] One quantified case study** with numbers released by the client, for example cutover duration, downtime or migration volume.
3. **[PLACEHOLDER] Engagement models:** advisory day rate or fixed-price workshop. This answers the CFO and procurement questions.
4. **[PLACEHOLDER] Network or partners** for larger programmes, only if real and confirmed. This addresses the capacity objection.
5. **[PLACEHOLDER] Security and compliance approach**, if offered, for example GDPR, authorisation concepts or audit readiness.
6. **[PLACEHOLDER] Certifications**, only if they exist, for example SAP certifications.
7. **A real portrait photo of Marcel Wagner** for the About section. AI-generated people are not used.
8. **Optional: a custom domain** (e.g. stegarc.de) instead of github.io. This would strengthen credibility with enterprise IT.
