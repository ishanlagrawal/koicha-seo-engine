"""
Module 2: Static Micro-Site Builder (Groq Edition)
==================================================
Uses Jinja2 templates to build the main pages.
"""

import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
TEMPLATES_DIR = Path("templates")
OUTPUT_DIR = Path("docs")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant" # Faster model for short content

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def groq_generate(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return ""

def build_index(config: dict, env: Environment):
    print("Building index.html...")
    template = env.get_template("index.html")
    
    schema_path = Path("static/schema/koicha_schema.json")
    restaurant_schema = "{}"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            restaurant_schema = f.read()

    html = template.render(
        config=config,
        restaurant_schema=restaurant_schema,
        base_url=os.getenv("SITE_BASE_URL", "")
    )
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

def build_menu_page(config: dict, env: Environment):
    print("Building menu.html...")
    template = env.get_template("menu.html")

    # Load schema
    schema_path = Path("static/schema/koicha_schema.json")
    menu_schema = "{}"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            menu_schema = f.read()

    # Note: We'd normally pass enriched data here, but for simplicity 
    # we're using config. In a full engine, M1 would save a 'enriched_menu.json'
    html = template.render(
        config=config,
        menu_schema=menu_schema,
        base_url=os.getenv("SITE_BASE_URL", "")
    )
    with open(OUTPUT_DIR / "menu.html", "w", encoding="utf-8") as f:
        f.write(html)

def build_seo_pages(config: dict, env: Environment):
    # Stubs for now
    pages = [
        ("matcha-pune.html", "Matcha Guide"),
        ("korean-food-pune-guide.html", "Korean Food Guide"),
        ("faq.html", "FAQ")
    ]
    for filename, title in pages:
        print(f"Building {filename}...")
        with open(OUTPUT_DIR / filename, "w", encoding="utf-8") as f:
            f.write(f"<h1>{title}</h1><p>Content active and optimized.</p>")

def build_sitemap(config: dict):
    print("Building sitemap.xml...")
    base_url = os.getenv("SITE_BASE_URL", "").rstrip("/")
    
    pages = [
        "/", # index.html
        "/menu.html",
        "/matcha-pune.html",
        "/korean-food-pune-guide.html",
        "/faq.html"
    ]
    
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{page}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append('    <changefreq>weekly</changefreq>')
        xml.append('  </url>')
    
    xml.append('</urlset>')
    
    with open(OUTPUT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def run():
    print("\nKoicha Site Builder -- Module 2")
    print("=" * 45)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    build_index(config, env)
    build_menu_page(config, env)
    build_seo_pages(config, env)
    build_sitemap(config)

    print("\nModule 2 Complete!")
    print(f"Site generated in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    run()
