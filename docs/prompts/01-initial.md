=======================================================================
SYSTEM MISSION: KOICHA DIGITAL FOOTPRINT ENGINE — FULL BUILD
AI-Growth Architect | Local SEO + AI Search Domination | Zero Cost
=======================================================================

BEFORE YOU WRITE A SINGLE LINE OF CODE — ASK THE OPERATOR FOR:
=======================================================================

Request the following information and wait for all answers before 
proceeding. Present this as a numbered checklist. Do not assume 
any values. If the operator cannot answer something, note it and 
flag what that blocks.

--- SECTION A: ACCESS & CREDENTIALS ---

A1. Google Business Profile
    - Is Koicha's GBP claimed and verified? (Yes/No)
    - What Google account email owns it?
    - Has Google Business Profile API been enabled in Google Cloud Console?

A2. Domain & Hosting
    - Does Koicha own a domain? (e.g. koicha.in)
    - Who is the registrar? (GoDaddy / Google Domains / Namecheap etc.)
    - Is there an existing website, even a basic one? If yes, URL?
    - Preferred hosting: Vercel / GitHub Pages / Google Sites / Firebase?

A3. Google Cloud Project
    - Is there an existing Google Cloud project for Koicha?
    - If yes, share project ID. If no, agent will guide setup.
    - APIs to enable (agent will walk through): Search Console API, 
      Business Profile API, Gemini API, Gmail API, Sheets API

A4. Google Search Console
    - Is Search Console set up for the domain? (Yes/No)
    - If yes, what property type? (Domain / URL prefix)

A5. Swiggy Partner Dashboard
    - Does the owner have login access to Swiggy Partner portal?
    - What is the Swiggy Brand ID? (Known: 771805 — confirm)
    - Is Zomato also active? If yes, Zomato restaurant ID?

A6. Telegram (for alert bot)
    - Does the owner have a Telegram account? (Yes/No)
    - Are they open to creating a Telegram Bot for alerts? (Yes/No)

A7. Instagram
    - Instagram handle: @koicha.india (confirm)
    - Does the owner have access to Instagram Basic Display API 
      or Meta Developer account? (Yes/No — nice to have, not blocking)
    - Can the owner export HQ food photos from Instagram 
      or provide a Google Drive folder link?

A8. Gemini API
    - Has a Gemini API key been generated at aistudio.google.com?
      (Free tier: 60 requests/min, 1500 req/day — sufficient)
    - If not, agent will provide exact setup steps.

--- SECTION B: BUSINESS DETAILS ---

B1. Full business name as it should appear everywhere: "Koicha"
B2. Tagline / one-liner: "The Art of Matcha & More" (confirm or update)
B3. Physical address: Easy Boba, Lane 7, Koregaon Park, Pune 411001
    - Confirm exact pin on Google Maps (share Maps link)
    - Is this location permanent for at least 6 months? (Yes/No)
B4. Operating hours: 2 PM – 11 PM daily (confirm, any days closed?)
B5. Phone number for GBP listing
B6. FSSAI License number (for GBP and Swiggy legitimacy)
B7. Is "Koicha" registered as a business entity? (Proprietorship/LLP etc.)

--- SECTION C: MENU DATA ---

C1. Confirm the following menu is current and complete:
    KOREAN FRIED CHICKEN:
      - K-fried Chicken ₹329
      - Yangnyeom Chicken ₹349
      - Soya Chicken ₹349
    KIMCHI SPECIALS:
      - Kimchi Fried Rice: Veg ₹289 / NV ₹349
      - Kimchi Soup Fried Rice: Veg ₹299 / NV ₹349
      - Add-ons: Chicken Sausage ₹60 / Egg ₹25 / Tofu ₹40
    GIMBAP:
      - Veg ₹239 / Egg ₹249 / Chicken ₹269 / Tuna ₹289
    TTEOKBOKKI:
      - Classic ₹349 / Cream & Cheese ₹389 / Chicken ₹389 / Fish ₹389
      - Add-ons: Cheese ₹30 / Egg ₹25 / Soy ₹15
    BAP BOWLS:
      - Bibimbap Veg ₹299 / Chicken ₹349
      - Chicken Bulgogi ₹379 / Chicken Katsu ₹399
    MATCHA DRINKS:
      - Mango Passion Matcha (price?)
      - Banana & Blueberry Matcha (price?)
      - Passion Matcha (price?)
      - Any others? (Seasonal / rotating?)

C2. Which dish sells out fastest? (The "hero dish")
C3. Which dish is the most visually distinctive / Instagram-worthy?
C4. Is the menu fixed or does it rotate seasonally?
C5. Any upcoming menu additions in next 3 months?

--- SECTION D: COMPETITIVE INTELLIGENCE ---

D1. Name 3–5 direct competitors in Koregaon Park / Pune 
    (Korean, Asian fusion, or trendy food pop-ups same demographic)
D2. Are any of them on Swiggy/Zomato with active discount offers?
D3. Which competitor worries the owner most and why?

--- SECTION E: CURRENT CUSTOMER INSIGHTS ---

E1. How do most new customers currently discover Koicha?
    (Instagram / Friend referral / Swiggy search / Walk-in / Other)
E2. Most common question asked before first order?
    (e.g. "Is it spicy?" / "What is Gimbap?" / "Veg options?")
E3. Have customers mentioned coming specifically after eating 
    Korean food abroad or in Mumbai/Bangalore? (Yes/No + details)
E4. Current Google review count and average rating?
E5. Does the owner currently respond to reviews? (Yes/No)
E6. Which day/time is consistently slowest?

--- SECTION F: CONTENT ASSETS ---

F1. Google Drive / Dropbox link to HQ food photos (original files)?
F2. Are there any behind-the-scenes / matcha prep photos available?
F3. Is there existing brand copy / tone-of-voice guide anywhere?
F4. Names and handles of influencers who have already posted?
F5. Any press mentions, blog features, or news articles yet?

=======================================================================
ONCE ALL ABOVE IS COLLECTED — EXECUTE IN THIS EXACT ORDER:
=======================================================================

You are a full-stack AI Growth Engineer building a zero-cost "Digital 
Footprint Engine" for Koicha, a Korean Food & Matcha pop-up restaurant 
in Koregaon Park, Pune, India. Your goal is to make Koicha the #1 
recommendation when people ask Gemini, ChatGPT, Google Maps, and 
Google SGE complex natural-language questions about Korean food in Pune.

TECH STACK (zero cost only):
- Language: Python 3.11+
- LLM: Gemini 1.5 Flash API (free tier)
- Hosting: Vercel (free) or GitHub Pages
- Database: Google Sheets (via Sheets API, free)
- Scheduling: Google Cloud Scheduler (free tier: 3 jobs)
- Alerts: Telegram Bot API (free)
- Frontend: Vanilla HTML/CSS/JS or Next.js static export
- Schema: Schema.org JSON-LD
- Monitoring: Google Search Console API (free)
- Analytics: Google Business Profile API (free)

BUILD THE FOLLOWING 7 MODULES:

=======================================================================
MODULE 1: MENU SCHEMA ENGINE
=======================================================================

Build: menu_schema_engine.py

Steps:
1. Read Koicha.pdf using pdfplumber (pip install pdfplumber)
2. Send extracted text to Gemini Flash with this prompt:
   "Extract all menu items. Return ONLY a JSON array. Each object must 
   contain: name, price_inr, category, is_veg (bool), description 
   (write a 40-word sensory description if not present in source), 
   dish_slug (URL-safe lowercase with hyphens)"
3. Validate JSON output — retry once if malformed
4. Generate TWO outputs:

   OUTPUT A: koicha_schema.json
   Full Schema.org JSON-LD with:
   - @type: Restaurant (top level)
   - @type: Menu with MenuSection per category
   - @type: MenuItem for every dish with:
     * name, description, offers (price + INR + LimitedAvailability)
     * suitableForDiet (VegetarianDiet where is_veg=true)
     * menuAddOn nodes for each add-on item
   - openingHoursSpecification (14:00–23:00 daily)
   - address (PostalAddress with full KP address)
   - servesCuisine: ["Korean", "Matcha", "Asian"]
   - geo coordinates (fetch from Google Maps API or hardcode)

   OUTPUT B: menu.html
   Semantic HTML page with:
   - <script type="application/ld+json"> embedding the schema
   - One <section> per menu category with id="[category-slug]"
   - One <article> per dish with itemprop microdata annotations
   - SEO meta: title, description, og:image per category
   - "Order on Swiggy" CTA button linking to brand page
   - Accessible: ARIA labels, semantic headings hierarchy

5. Validate at: https://validator.schema.org
   Target: 0 errors, 0 warnings
6. Create individual dish HTML pages at /menu/[dish-slug].html
   Each containing:
   - Full MenuItem schema for that dish
   - 150+ word keyword-rich description 
     (Gemini generates this from dish name + category)
   - Canonical URL tag
   - FAQ schema (Gemini generates 3 Q&As per dish:
     "Is [dish] vegetarian?", "How spicy is [dish]?", 
     "What does [dish] taste like?")
   - Breadcrumb schema: Home > Menu > [Category] > [Dish]

=======================================================================
MODULE 2: STATIC MICRO-SITE
=======================================================================

Build: /site/ directory → deploy to Vercel

Pages to create:
  /index.html — Homepage
    - Hero: "Korean Food & Matcha. Limited Batches. Koregaon Park."
    - Embedded Google Map (iframe, free)
    - Hours + Location prominently above fold
    - "Order on Swiggy" primary CTA
    - Top 3 dish cards with photos (use renamed HQ photos)
    - FAQ section with FAQ schema (top 5 customer questions from E2)
    - Restaurant JSON-LD schema in <head>
  
  /menu.html — Full menu (output from Module 1)
  
  /menu/[dish-slug].html — Individual dish pages (Module 1 output)
  
  /korean-food-pune-guide.html — SEO content page
    Gemini generates a 600-word guide:
    "A Guide to Korean Food in Pune — What to Order, What to Expect"
    Naturally mentions all dish names + Koicha + location
    This page targets informational queries that AI search engines
    pull for "what is Korean food" + "Pune" intent
  
  /matcha-pune.html — Matcha-specific landing page
    Targets: "matcha cafe Pune", "ceremonial matcha Pune", 
    "matcha drinks Koregaon Park"
    Gemini generates 400-word content + all matcha menu items
    Include: What is matcha, why Koicha sources quality matcha,
    the whisking process (use behind-the-scenes photos)

  Technical requirements for all pages:
  - PageSpeed score 90+ (no heavy JS, compress images)
  - sitemap.xml auto-generated listing all pages
  - robots.txt allowing full crawl
  - All images: renamed with formula 
    [brand]-[dish]-[cuisine]-[location]-[city].jpg
  - All images: alt text as full semantic sentence
  - Open Graph tags for all pages (for social sharing previews)
  - hreflang: en-IN

=======================================================================
MODULE 3: GOOGLE BUSINESS PROFILE AUTOMATION
=======================================================================

Build: gbp_automation.py

Uses: Google Business Profile API (free, OAuth 2.0)

3A. Weekly GBP Post Generator
  Schedule: Every Monday + Thursday at 1 PM
  Process:
  1. Pick post type from rotating schedule:
     Week A Mon: Dish spotlight (hero dish)
     Week A Thu: Behind-the-scenes (matcha prep)
     Week B Mon: Customer quote (pull from latest 5-star review)
     Week B Thu: "Today's batch" availability post
  2. Call Gemini Flash with post type + dish info
     Prompt includes Koicha brand voice rules:
     "Warm, artisan, slightly playful. Never corporate.
      Max 150 words. Always end with location + hours.
      Use food/matcha metaphors. Reference specific dish names."
  3. Generate post text + suggested photo filename
  4. Write to Google Sheet "Content Calendar" tab
     Columns: Date | Post Type | Copy | Photo Needed | Status
  5. Send Telegram alert to owner with draft + approval button
     If approved: auto-post via GBP API
     If no response in 4hrs: flag as "Needs Review" in Sheet

3B. GBP Photo Upload Scheduler
  Weekly: Remind owner via Telegram to upload 2-3 new photos
  Include in reminder:
  - Exact filenames to use (pre-generated with formula)
  - Which GBP category to upload under
  - Suggested caption for each photo description field

3C. Q&A Population
  One-time setup + monthly refresh:
  1. Generate 15 Q&A pairs using Gemini covering:
     - Dietary questions (veg options, halal, spice levels)
     - Dish explanations (what is gimbap, tteokbokki etc.)
     - Operational (parking, seating, delivery, pre-order)
     - Price range questions
  2. Post all Q&As to GBP via API (owner account)
  3. These appear in Knowledge Panel and are read by Gemini

=======================================================================
MODULE 4: REVIEW INTELLIGENCE SYSTEM
=======================================================================

Build: review_engine.py + Google Sheet "Review Dashboard"

4A. Review Response Generator
  Trigger: Owner pastes review text into Sheet Column A, 
           rating (1-5) in Column B
  Process:
  1. Apps Script calls Gemini API
  2. System prompt enforces Koicha brand voice:
     "Warm and personal. Reference specific dishes mentioned.
      Use matcha/food metaphors. For negative: acknowledge 
      genuinely, offer to make it right, never defensive.
      Max 80 words. Sign: The Koicha Team 🍵
      Never use: 'Thank you for your feedback', 
      'We apologize for any inconvenience'"
  3. Output draft to Column C
  4. One-click copy button → pastes to clipboard
  
  Response strategy by rating:
  - 5 star: Celebrate the specific dish, invite return
  - 4 star: Thank + ask what would make it 5 stars (gently)
  - 3 star: Acknowledge gap, explain limited-batch context, invite return
  - 2 star: Apologize specifically, offer direct DM resolution
  - 1 star: Prioritise — alert owner via Telegram immediately,
            generate response + flag for personal follow-up

4B. Semantic Review Prompting System
  Build: review_prompt_card_generator.py
  
  Generates printable "review prompt cards" as HTML/PDF:
  - QR code linking to Google review page (use qrcode Python lib)
  - Fill-in-the-blank sentence starter per dish:
    "I had the [DISH] and it tasted like ___"
  - One card design per dish category (4 card variants)
  - Koicha branding: teal color (#3A9D8F), logo positioning
  - Print-ready: A6 size, 300dpi equivalent CSS

4C. Review Keyword Tracker
  Monthly: Scrape Koicha's Google reviews (via GBP API)
  Extract: Which dish names, flavor words, experience words appear
  Output to Sheet: keyword frequency table
  Flag: dish names that NEVER appear in reviews 
        (= awareness gap → content opportunity)
  Flag: negative sentiment keywords appearing 3+ times
        (= operational issue to fix)

=======================================================================
MODULE 5: COMPETITOR INTELLIGENCE BOT
=======================================================================

Build: competitor_monitor.py

Schedule: Daily at 1 PM (1hr before Koicha opens)

5A. Swiggy/Zomato Offer Scraper
  For each competitor URL provided:
  1. Fetch page (requests + BeautifulSoup)
  2. Detect offer keywords: "free", "% off", "combo", "discount",
     "today only", "special", "buy one", "happy hour", "flat ₹"
  3. If offer detected: extract offer text + timestamp

5B. Instagram Activity Monitor (no API needed)
  Use: Instaloader library (pip install instaloader, free)
  For each competitor Instagram handle:
  1. Fetch last 3 posts (public profiles only)
  2. Check captions for offer keywords
  3. Check if posting frequency has spiked (>1 post/day = campaign)

5C. Counter-Strategy Generator
  If any offer detected:
  1. Call Gemini with competitor offer + Koicha brand rules:
     "Koicha is premium. Never discount. Respond with exclusivity.
      Suggest ONE Instagram action using Koicha's actual menu items.
      The response should make limited batches feel MORE desirable,
      not cheaper. Return: caption draft + Story CTA + best posting time"
  2. Send to Telegram with competitor name + their offer + Koicha's move
  3. Log to Sheet: "Competitor Activity" tab

5D. Weekly Competitor Summary
  Every Sunday 8 PM: Send Telegram digest
  - Which competitors posted most this week
  - Any new menu items spotted
  - Koicha's recommended focus for next week

=======================================================================
MODULE 6: ZERO-COST AI SEARCH CITATION BUILDER
=======================================================================

Build: citation_builder.py + content_publisher.py

This module builds the "digital nodes" that Gemini cites when
answering natural language questions about Korean food in Pune.

6A. Auto-Blog Publisher (Blogger API — free, Google-owned)
  Create a Blogger blog: "Korean Food Pune Guide" (separate from main site)
  
  Generate and publish 8 articles using Gemini:
  Article 1: "Complete Guide to Korean Food in Pune 2025"
  Article 2: "What is Gimbap? A Pune Food Lover's Introduction"
  Article 3: "Tteokbokki in Pune — Everything You Need to Know"
  Article 4: "Best Vegetarian Korean Food Options in Pune"
  Article 5: "Korean Fried Chicken vs Regular Fried Chicken — The Difference"
  Article 6: "What is Matcha? Why Ceremonial Grade Matters"
  Article 7: "Korean Food for Beginners — What to Order First"
  Article 8: "Koregaon Park Food Guide — Hidden Gems 2025"
  
  Each article must:
  - Be 600–900 words (Gemini generates, human reviews)
  - Mention Koicha naturally in context (not promotional tone)
  - Include FAQ schema
  - Link to koicha.in/menu
  - Use target keywords in H1, H2, first paragraph
  - Be submitted to Google Search Console for indexing

6B. Google Web Stories Generator
  Build 5 Web Stories (visual, swipeable — Google indexes these 
  separately and shows in Discover + SGE):
  
  Story 1: "What is Yangnyeom Chicken?" (5 slides)
  Story 2: "How Matcha is Prepared at Koicha" (5 slides)
  Story 3: "Korean Food Guide for Pune Beginners" (7 slides)
  Story 4: "Koicha — A Day in the Life of a Limited Batch" (6 slides)
  Story 5: "5 Korean Dishes to Try Before You Die" (6 slides)
  
  Build using: Web Stories WordPress plugin OR 
  amp-story HTML template (free, no plugin needed)
  Host on: koicha.in/stories/
  Submit all to Search Console

6C. Structured Q&A Content for AI Scraping
  Build: /faq.html on koicha.in
  
  Generate 25 Q&As covering:
  - "Is Korean food available in Pune?" 
  - "Where can I find authentic Gimbap in Pune?"
  - "Is there Korean food in Koregaon Park?"
  - "What is the best Korean restaurant in Pune?"
  - "Is Koicha vegetarian-friendly?"
  - [20 more generated by Gemini from keyword research]
  
  Each Q&A: Full FAQ schema markup
  This page is specifically designed to be cited by Gemini SGE
  when answering conversational queries about Korean food in Pune

6D. OpenStreetMap & Secondary Directory Listings
  Auto-generate listing data package (text file with all details)
  for manual submission to:
  - OpenStreetMap (cuisine=korean, matcha tags)
  - Justdial
  - Sulekha  
  - IndiaMart (for catering/bulk queries)
  - Magicpin (Pune-specific, high local SEO value)
  - Dineout
  Package includes: optimized description, keywords, hours, 
  photos list, category tags for each platform

=======================================================================
MODULE 7: ANALYTICS & GROWTH DASHBOARD
=======================================================================

Build: Google Sheet "Koicha Growth Dashboard" 
       + dashboard_sync.py (weekly cron)

Sheet Tabs:

TAB 1: Search Console Keywords
  Auto-pull via Search Console API weekly:
  - Query | Impressions | Clicks | CTR | Position
  - Filter: India / Pune geography
  - Highlight formula: CTR < 2% AND Impressions > 50 
    (= quick win — high visibility, low click — fix meta description)
  - Flag: Any query containing dish names with position > 10
    (= content gap — need dedicated page)

TAB 2: GBP Insights  
  Weekly pull via GBP API:
  - Map views | Search views | Direction requests | Call clicks
  - Photo views (owner vs customer breakdown)
  - Top search queries that triggered GBP listing

TAB 3: Review Tracker
  - Date | Rating | Reviewer | Key dish mentioned | Sentiment
  - Running average rating
  - Chart: rating trend over time
  - Semantic keyword frequency from reviews

TAB 4: Content Calendar
  - Date | Platform | Content Type | Copy Draft | Status | Photo
  - Auto-populated by Module 3 (GBP posts)
  - Manual rows for Instagram (owner fills)

TAB 5: Competitor Log
  - Date | Competitor | Activity | Koicha Counter | Status

TAB 6: Citation Tracker
  - Platform | Status | Date Added | Link | Indexing Status

TAB 7: Monthly Scorecard
  Auto-generated first Monday of each month:
  - GBP: Map views growth % MoM
  - Reviews: New reviews count, average rating change
  - Search: Top 5 rising keywords
  - Content: Posts published vs target
  - Citations: New citations added
  Gemini generates a 3-sentence "Month in Review" narrative
  + Top 3 recommended actions for next month
  Auto-email to owner via Gmail Apps Script

=======================================================================
TECHNICAL ARCHITECTURE OVERVIEW
=======================================================================

File structure to create:
  koicha-seo-engine/
  ├── modules/
  │   ├── menu_schema_engine.py      # Module 1
  │   ├── site_builder.py            # Module 2
  │   ├── gbp_automation.py          # Module 3
  │   ├── review_engine.py           # Module 4
  │   ├── competitor_monitor.py      # Module 5
  │   ├── citation_builder.py        # Module 6
  │   └── dashboard_sync.py          # Module 7
  ├── templates/
  │   ├── base.html
  │   ├── menu.html
  │   ├── dish.html
  │   ├── blog_post.html
  │   └── review_card.html
  ├── static/
  │   ├── css/style.css
  │   ├── images/ (renamed HQ photos)
  │   └── schema/koicha_schema.json
  ├── scripts/
  │   └── apps_script_review.js      # Google Apps Script
  ├── config/
  │   └── koicha_config.json         # All business data
  ├── site/                          # Generated static site
  ├── .env                           # API keys (never commit)
  ├── requirements.txt
  ├── cron_jobs.yaml                 # Cloud Scheduler config
  └── README.md

requirements.txt:
  pdfplumber==0.10.3
  google-generativeai==0.5.4
  requests==2.31.0
  beautifulsoup4==4.12.3
  python-telegram-bot==20.7
  instaloader==4.10.3
  schedule==1.2.1
  jinja2==3.1.3
  qrcode[pil]==7.4.2
  google-auth==2.28.1
  google-api-python-client==2.120.0
  python-dotenv==1.0.1

=======================================================================
SKILLS TO LOAD — FROM SKILLS.SH / GITHUB
=======================================================================

LOAD THESE SKILLS BEFORE STARTING ANY MODULE:

SKILL 1 (skills.sh): "google-business-profile-api"
  → Handles OAuth flow, token refresh, post creation, 
    photo upload, Q&A management for GBP
  URL: https://skills.sh/skills/google-business-profile-api

SKILL 2 (skills.sh): "schema-org-generator"
  → Generates valid JSON-LD for Restaurant, MenuItem, FAQ, 
    Breadcrumb, WebPage types with validation
  URL: https://skills.sh/skills/schema-org-generator

SKILL 3 (skills.sh): "telegram-bot-alerts"
  → Full Telegram Bot setup: send messages, inline keyboards,
    approval buttons, file uploads, scheduling
  URL: https://skills.sh/skills/telegram-bot-alerts

SKILL 4 (skills.sh): "google-search-console-api"
  → Query performance data, sitemap submission, 
    URL inspection, indexing requests
  URL: https://skills.sh/skills/google-search-console-api

SKILL 5 (GitHub): "py-schema-org" by Dan Fox
  → Python library for programmatic Schema.org generation
    with built-in validator
  Repo: https://github.com/dan-blanchard/python-schema-org
  Install: pip install schemaorg

SKILL 6 (GitHub): "local-seo-tools" 
  → Collection of local SEO audit scripts: GBP completeness
    checker, citation consistency auditor, review velocity tracker
  Repo: https://github.com/LocalSEOGuide/local-seo-python-tools

SKILL 7 (GitHub): "instaloader"
  → Instagram public data fetcher — posts, captions, 
    hashtags, follower counts. No API key needed.
  Repo: https://github.com/instaloader/instaloader
  Install: pip install instaloader

SKILL 8 (GitHub): "google-web-stories-python"
  → Programmatic AMP story builder — generate Web Stories
    from JSON data with templates
  Repo: https://github.com/GoogleForCreators/web-stories-wp
  (Use the AMP story HTML spec for non-WP implementation)

SKILL 9 (GitHub): "jinja2-static-site"
  → Static site generator using Jinja2 templates — 
    perfect for building the micro-site in Module 2
  Repo: https://github.com/eudicots/Cactus

SKILL 10 (GitHub): "py-qrcode"
  → QR code generator for review prompt cards
  Repo: https://github.com/lincolnloop/python-qrcode
  Install: pip install qrcode[pil]

=======================================================================
BRAND CONSTANTS — NEVER DEVIATE FROM THESE
=======================================================================

BRAND_CONFIG = {
  "name": "Koicha",
  "tagline": "The Art of Matcha & More",
  "cuisine": ["Korean Food", "Matcha", "Asian"],
  "format": "Pop-up (limited batches)",
  "location_full": "Easy Boba, Lane 7, Koregaon Park, Pune 411001",
  "location_short": "Koregaon Park, Pune",
  "hours": "2 PM – 11 PM daily",
  "swiggy_url": "https://www.swiggy.com/direct/brand/771805",
  "instagram": "@koicha.india",
  "primary_color": "#3A9D8F",
  "secondary_color": "#F5F0E8",
  "brand_voice": {
    "tone": "Warm, artisan, slightly playful. Never corporate.",
    "use": ["food metaphors", "matcha references", "limited-batch exclusivity"],
    "never_use": ["Thank you for your feedback", "We apologize for any inconvenience", 
                  "discount language", "cheap/affordable framing"],
    "signoff": "The Koicha Team 🍵",
    "max_response_words": 80
  },
  "seo_targets": {
    "primary": ["Korean food Pune", "Korean restaurant Koregaon Park"],
    "dish_level": ["Gimbap Pune", "Tteokbokki Pune", "Yangnyeom chicken Pune",
                   "Bibimbap Pune", "Korean fried chicken Pune"],
    "intent": ["matcha cafe Pune", "ceremonial matcha Pune", 
                "Korean food delivery Koregaon Park"],
    "ai_search": ["best Korean food in Pune", "where to find Gimbap in Pune",
                  "authentic Korean restaurant Pune", "vegetarian Korean food Pune"]
  }
}

=======================================================================
SUCCESS METRICS — TRACK THESE IN MODULE 7
=======================================================================

Month 1 Targets:
  - GBP profile completeness: 100%
  - Schema validation errors: 0
  - Pages indexed by Google: All /menu/[dish] pages
  - GBP posts published: 8 (2/week)
  - New Google reviews: +10
  - Directory citations created: 8 platforms
  - Blogger articles published: 8

Month 3 Targets:
  - Google Maps ranking: Top 3 for "Korean food Koregaon Park"
  - Dish-level keyword rankings: Page 1 for 5+ dish queries
  - GBP map views: +40% vs baseline
  - Total Google reviews: 30+
  - Gemini citation: Appear in at least 1 AI search answer
    (test by asking: "best Korean food in Pune" to Gemini)

Month 6 Targets:
  - #1 Google Maps result for "Korean food Koregaon Park"
  - All major dish names rank Page 1 Pune-local
  - 75+ Google reviews, 4.5+ average rating
  - Koicha cited by Gemini SGE without being asked directly

=======================================================================
FINAL INSTRUCTION TO AGENT
=======================================================================

Start NOW with the information-gathering checklist above.
Present all questions in Sections A–F as a clean numbered list.
Group by section with emoji headers for readability.
After receiving all answers, confirm what you have and what 
is still missing. Then begin Module 1.

Show your work at each step. After each module, output:
  ✅ What was built
  📁 Files created
  🔗 URLs to test/validate
  ⚠️ Any manual steps the owner must take
  ➡️ What Module comes next

Do not skip validation steps. Do not proceed to next module 
if current module has schema errors or broken links.

This is a long-term infrastructure build — prioritize 
correctness and maintainability over speed.
=======================================================================