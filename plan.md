# Implementation Plan – Strategic Audit & "Artisan Magazine" Upgrade

This plan addresses the critical bugs and strategic improvements identified in the ChatGPT audit. The goal is to harden the SEO foundation and elevate the visual design to a world-class "Editorial Artisan" level.

## User Review Required

> [!IMPORTANT]
> **Sitemap Impact:** I will be forcing absolute URLs for all site links to satisfy Google Search Console. 
> **Design Pivot:** We are moving away from "Glassmorphism" toward a "Muted Paper/Artisan" aesthetic. This will significantly change the feel of the current site.

## Proposed Changes

### Phase 1: Critical SEO & Workflow Stability

#### [MODIFY] [weekly_audit.yml](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/.github/workflows/weekly_audit.yml)
- **Execution Audit:** Add visible logging and `set -e` safety.
- **Syntax Check:** Ensure all commands execute on schedule.

#### [MODIFY] [site_builder.py](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/modules/site_builder.py)
- **Sitemap Correctness:** Proper XML namespaces, safe URL joins, no double slashes. 
- **Full Metadata Pass:** Ensure `title`, `meta description`, `canonical`, and `og` tags are emitted for all page types.
- **Review Filter:** Select "Approved" reviews only with diversity weighting.

#### [MODIFY] [base.html](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/templates/base.html)
- **Metadata Hardening:** Standardize `title`, `description`, `canonical`, `og`, and `twitter` card emissions.

---

### Phase 2: Content Resilience & AI Voice

#### [MODIFY] [citation_builder.py](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/modules/citation_builder.py)
- **Image Bridge:** Convert relative paths to fully qualified `ishanlagrawal.github.io` URLs for Blogger.
- **Failure Safety:** Skip images if not public.

#### [MODIFY] [review_engine.py](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/modules/review_engine.py)
- **Artisan Persona:** Upgrade prompt to "Emotional Artisan Owner" style.
- **QC Layer:** Filter clichés and check for "AI-ish" patterns.

#### [MODIFY] [competitor_monitor.py](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/modules/competitor_monitor.py)
- **Parser Resilience:** Add error fallback and logging to prevent silent failures.

---

### Phase 3: "World-Class" Premium UX

#### [MODIFY] [style.css](file:///c:/Users/Admin/Desktop/Antigravity-MVP/05-Koicha-SEO/static/css/style.css)
- **Editorial Design:** Matcha-cream base, subtle brass accents, superior vertical rhythm.
- **Mobile CTA:** Sticky Lane 7 / Order dock.
- **Conversion UX:** WhatsApp prefilled intents, "Find us in Lane 7" map clarity.
- **Animations:** Opacity/translate-based reveal transitions.

## Verification Plan

### Automated Tests
- `python modules/site_builder.py`: Run and inspect `docs/sitemap.xml` for absolute URLs.
- `python modules/test_telegram_review.py`: Verify the new "Artisan Voice" response quality.

### Manual Verification
- Visual audit of the generated `index.html` to confirm the "Paper/Editorial" aesthetic.
- Check Metadata in browser for correct Canonical tags.
