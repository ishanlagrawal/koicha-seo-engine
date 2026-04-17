# Koicha Digital Footprint Engine — Project Roadmap

## 🎯 Strategic Purpose
To build a zero-cost, high-impact digital presence for Koicha (Koregaon Park, Pune) that dominates local search and AI-driven queries (Gemini/ChatGPT/SGE).

---

## 🏗️ Technical Architecture
- **Engine:** Python-based automation.
- **LLM:** Gemini 1.5 Flash (Primary) / Groq (Backup).
- **Deployment:** Cloudflare Pages (Static Site).
- **Social/Local:** Google Business Profile (GBP) integration.
- **Alerts:** Telegram Bot.

---

## 🏃 Implementation Modules

1.  **[x] M1: Menu Schema Engine** (Enriches menu with AI + Schema.org)
2.  **[x] M2: Static Site Builder** (Generates premium landing pages)
3.  **[ ] M3: GBP Automation** (On Hold - API Restricted. Workaround: Metricool)
4.  **[x] M4: Review Intelligence** (✅ Telegram Bridge Implemented)
5.  **[/] M5: Competitor Monitor** (Initialized/Simulation active)
6.  **[x] M6: Citation Builder** (✅ Blogger + Drive Sync Implemented)
7.  **[ ] M7: Analytics Dashboard** (Consolidated growth tracking)

---

## 🛠️ Discussion & Decisions Summary
- **Domain:** Starting with GitHub Pages (Zero-cost) -> Transfer to `koicha.in` later.
- **Models:** Verified Gemini 1.5 Flash is active and working.
- **Alerts:** Confirmed **Telegram Bot** (not WhatsApp) for simplicity and cost.
- **Monday:** The shop is **CLOSED** on Mondays.
- **Hours:** 2 PM – 11 PM.
- **Menu Updates:** System designed to regenerate everything from a new PDF anytime.

---

## ✅ Prerequisites Completed
- [x] Gemini & Groq API Keys verified.
- [x] Google Cloud Project configured (`[GCP_PROJECT_ID]`).
- [x] GitHub repository established.
- [x] Project scaffolding (folders/base templates) built.
- [x] Menu PDF uploaded to `data/`.
