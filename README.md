# Koicha SEO Engine

## Overview
Zero-cost AI-powered Digital Footprint Engine for **Koicha** — Korean Food & Matcha pop-up in Koregaon Park, Pune.

**Goal:** Make Koicha the #1 recommendation when people ask Google, Gemini, ChatGPT, or Google Maps about Korean food in Pune.

## Tech Stack
- **Language:** Python 3.11+
- **LLM:** Gemini 1.5 Flash API (free tier)
- **Hosting:** GitHub Pages (free) → koicha.in (later)
- **Database:** Google Sheets (Sheets API)
- **Scheduling:** Python `schedule` library (→ Cloud Scheduler later)
- **Alerts:** Telegram Bot API
- **Frontend:** Vanilla HTML/CSS/JS (Jinja2 templated)
- **Schema:** Schema.org JSON-LD
- **Monitoring:** Google Search Console API

## Modules

| Module | File | Status |
|--------|------|--------|
| M1: Menu Schema Engine | `modules/menu_schema_engine.py` | 🔲 |
| M2: Static Micro-Site | `modules/site_builder.py` | 🔲 |
| M3: GBP Automation | `modules/gbp_automation.py` | 🔲 |
| M4: Review Intelligence | `modules/review_engine.py` | 🔲 |
| M5: Competitor Monitor | `modules/competitor_monitor.py` | 🔲 |
| M6: Citation Builder | `modules/citation_builder.py` | 🔲 |
| M7: Analytics Dashboard | `modules/dashboard_sync.py` | 🔲 |

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

### 3. Verify Config
```bash
python scripts/verify_setup.py
```

### 4. Run a Module
```bash
python modules/menu_schema_engine.py
```

## Project Structure
```
koicha-seo-engine/
├── modules/           # Core engine modules (M1-M7)
├── templates/         # Jinja2 HTML templates
├── static/            # CSS, images, schema JSON
├── scripts/           # Utility scripts
├── config/            # Business config
├── site/              # Generated static site (output)
├── data/              # Input data (menu PDF, photos)
├── .env               # API keys (never commit)
├── requirements.txt
└── README.md
```

## Brand Quick Reference
- **Color:** #3A9D8F (teal)
- **Tone:** Warm, artisan, slightly playful. Never corporate.
- **Signoff:** The Koicha Team 🍵
- **Hours:** 2 PM – 11 PM (Closed Mondays)
- **Location:** Easy Boba, Lane 7, Koregaon Park, Pune 411001
- **Swiggy:** https://www.swiggy.com/direct/brand/771805
