"""
Module 1: Menu Schema Engine (Groq Edition)
===========================================
Reads Koicha menu data (from PDF or config), sends to Groq (Llama 3),
generates Schema.org JSON-LD and semantic HTML pages.
"""

import json
import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

# --- Config ---
CONFIG_PATH = Path("config/koicha_config.json")
OUTPUT_SCHEMA = Path("static/schema/koicha_schema.json")
OUTPUT_SITE = Path("site")
TEMPLATES_DIR = Path("templates")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def groq_generate(prompt: str) -> str:
    """Helper to call Groq API."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error: {response.status_code} - {response.text}")

def load_menu_from_pdf(pdf_path: str) -> str:
    """Extract raw text from menu PDF."""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text
    except Exception as e:
        print(f"[FAILED] PDF Error: {e}")
        return ""

def enrich_menu_with_groq(menu_text: str, config: dict) -> list:
    """Extract and structure menu items using Groq."""
    prompt = f"""
You are an expert menu analyst for Koicha, a Korean pop-up in Pune.
Extract ALL dishes and drinks from the text below. 

Menu text:
---
{menu_text}
---

Return ONLY a JSON array. Each object MUST contain:
- name: string
- price_inr: integer
- category: string
- is_veg: boolean
- description: string (40-word sensory description)
- dish_slug: string (lowercase-hyphenated)
- addons: array of {{"name": string, "price_inr": integer}}

Rules:
1. Matcha is Ceremonial Grade from Shizuoka, Japan.
2. If price is missing, use null.
3. Return raw JSON only.
    """
    raw = groq_generate(prompt)
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

def build_schema_json(config: dict, menu_items: list) -> dict:
    """Built same as before..."""
    brand = config["brand"]
    location = config["location"]
    hours = config["hours"]

    # Build opening hours spec
    opening_hours = []
    day_map = {
        "tuesday": "Tu", "wednesday": "We", "thursday": "Th",
        "friday": "Fr", "saturday": "Sa", "sunday": "Su"
    }
    for day, value in hours.items():
        if value != "CLOSED" and day in day_map:
            parts = value.split("-")
            if len(parts) == 2:
                opening_hours.append({
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": f"https://schema.org/{day.capitalize()}",
                    "opens": parts[0],
                    "closes": parts[1]
                })

    menu_sections = []
    categories = {}
    for item in menu_items:
        cat = item.get("category", "Other")
        if cat not in categories: categories[cat] = []
        categories[cat].append(item)

    for cat_name, items in categories.items():
        menu_items_schema = []
        for item in items:
            node = {
                "@type": "MenuItem",
                "name": item["name"],
                "description": item.get("description", ""),
                "offers": {
                    "@type": "Offer",
                    "price": str(item["price_inr"] or 0),
                    "priceCurrency": "INR"
                }
            }
            if item.get("is_veg"): node["suitableForDiet"] = "https://schema.org/VegetarianDiet"
            menu_items_schema.append(node)
        
        menu_sections.append({
            "@type": "MenuSection",
            "name": cat_name,
            "hasMenuItem": menu_items_schema
        })

    return {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": brand["name"],
        "address": {"@type": "PostalAddress", "streetAddress": location["full_address"]},
        "openingHoursSpecification": opening_hours,
        "hasMenu": {"@type": "Menu", "hasMenuSection": menu_sections}
    }

def build_dish_pages(menu_items: list, config: dict):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("dish.html")
    (OUTPUT_SITE / "menu").mkdir(parents=True, exist_ok=True)

    for item in menu_items:
        print(f"  Writing: {item['name']}...")
        # Generate better description
        desc_prompt = f"Write a 150-word SEO description for {item['name']} at Koicha Korean Pune. Include flavors and textures."
        description = groq_generate(desc_prompt)
        
        html = template.render(
            item=item,
            description=description,
            faqs=[],
            faq_schema="{}",
            item_schema="{}",
            config=config,
            base_url=os.getenv("SITE_BASE_URL", "")
        )
        with open(OUTPUT_SITE / "menu" / f"{item['dish_slug']}.html", "w", encoding="utf-8") as f:
            f.write(html)

def run(pdf_path: str):
    print("\nKoicha Menu Engine (Groq) -- Module 1")
    print("=" * 45)
    config = load_config()
    
    print(f"Reading: {pdf_path}")
    text = load_menu_from_pdf(pdf_path)
    if not text.strip():
        print("FAILED: No text extracted from PDF.")
        return

    print("Enriching with Groq...")
    menu_items = enrich_menu_with_groq(text, config)
    
    print("Saving Schema...")
    schema = build_schema_json(config, menu_items)
    with open(OUTPUT_SCHEMA, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    
    print("Building dish pages...")
    build_dish_pages(menu_items, config)
    print("\nModule 1 Complete!")

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
