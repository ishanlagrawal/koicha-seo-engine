import json
import os
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import modules.sheet_utils as sheet_utils

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
TEMPLATES_DIR = Path("templates")
OUTPUT_DIR = Path("docs")
LOGO_PATH = "static/images/koicha_logo_round.png"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Using a higher-quality model for the official launch content
GROQ_MODEL = "llama-3.3-70b-versatile" 

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def groq_generate(prompt: str) -> str:
    print(f"  [AI] Inspiring new content...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": "You are a poetic, artisan food writer for Koicha, a Korean kitchen in Pune. Your tone is 'Homely', passionate, and sophisticated."}, 
                     {"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "The artisan is dreaming... please check back later."

def get_top_reviews():
    """Fetches the latest 3 reviews from the Master Google Sheet."""
    print("Fetching social proof from Master Sheet...")
    try:
        # We assume Review_Log tab has headers: Date | Name | Rating | Text | Reply | Status
        spreadsheet_id = os.getenv('KOICHA_SHEET_ID')
        service = sheet_utils.sheet_editor.service
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range="Review_Log!A2:E4"
        ).execute()
        rows = result.get('values', [])
        
        reviews = []
        for row in rows:
            if len(row) >= 4:
                reviews.append({
                    "name": row[1],
                    "rating": row[2],
                    "text": row[3]
                })
        return reviews
    except Exception as e:
        print(f"Fallback: Using dummy reviews. ({e})")
        return [
            {"name": "Ananya P.", "rating": 5, "text": "The Matcha Gimbap is legendary. Genuine artisan vibes!"},
            {"name": "Rahul S.", "rating": 5, "text": "Best Korean spot in Pune, Lane 7 just got better."}
        ]

def build_index(config: dict, env: Environment, reviews: list):
    print("Building index.html (with Social Proof)...")
    template = env.get_template("index.html")
    
    schema_path = Path("static/schema/koicha_schema.json")
    restaurant_schema = "{}"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            restaurant_schema = f.read()

    html = template.render(
        config=config,
        reviews=reviews,
        restaurant_schema=restaurant_schema,
        base_url=os.getenv("SITE_BASE_URL", ""),
        whatsapp_num=os.getenv("KOICHA_WHATSAPP"),
        logo_url=LOGO_PATH
    )
    with open(OUTPUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

def build_guide_page(config: dict, env: Environment, filename: str, title: str, prompt: str):
    print(f"Building Artisan Guide: {filename}...")
    content = groq_generate(prompt)
    
    html_content = content.replace('\n', '<br>')
    template = env.get_template("base.html")
    # Wrap content in a beautiful container
    styled_content = f"""
    <section class="guide-article container">
        <header class="guide-header">
            <h1>{title}</h1>
            <div class="artisan-line"></div>
        </header>
        <div class="guide-body">
            {html_content}
        </div>
    </section>
    """
    
    html = template.render(
        config=config,
        content=styled_content,
        base_url=os.getenv("SITE_BASE_URL", ""),
        whatsapp_num=os.getenv("KOICHA_WHATSAPP"),
        logo_url=LOGO_PATH
    )
    with open(OUTPUT_DIR / filename, "w", encoding="utf-8") as f:
        f.write(html)

def build_menu_page(config: dict, env: Environment):
    print("Building menu.html...")
    template = env.get_template("menu.html")

    schema_path = Path("static/schema/koicha_schema.json")
    menu_schema = "{}"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            menu_schema = f.read()

    html = template.render(
        config=config,
        menu_schema=menu_schema,
        base_url=os.getenv("SITE_BASE_URL", ""),
        whatsapp_num=os.getenv("KOICHA_WHATSAPP"),
        logo_url=LOGO_PATH
    )
    with open(OUTPUT_DIR / "menu.html", "w", encoding="utf-8") as f:
        f.write(html)

def build_sitemap():
    print("Building sitemap.xml...")
    base_url = os.getenv("SITE_BASE_URL", "").rstrip("/")
    pages = ["/", "/menu.html", "/matcha-pune.html", "/korean-food-pune-guide.html", "/faq.html"]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        xml.append(f'  <url><loc>{base_url}{page}</loc><lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod><changefreq>weekly</changefreq></url>')
    xml.append('</urlset>')
    
    with open(OUTPUT_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def run():
    print("\nKoicha Site Builder -- THE GRAND LAUNCH")
    print("=" * 45)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config = load_config()
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    reviews = get_top_reviews()

    # 1. Main Pages
    build_index(config, env, reviews)
    build_menu_page(config, env)
    
    # 2. Artisan Guides (AI Generated)
    build_guide_page(config, env, "matcha-pune.html", "The Soul of Matcha", "Write a soulful, 300-word guide to ceremonial matcha at Koicha Pune. Talk about the whisking process, the vibrant green color, and why sourcing from Shizuoka matters. Use an artisan tone.")
    build_guide_page(config, env, "korean-food-pune-guide.html", "Authentic Korean Street Food in Lane 7", "Write a vibrant, 300-word foodie guide to Korean food in Koregaon Park. Focus on Gimbap, Tteokbokki, and the 'limited batch' philosophy of Koicha.")
    
    # 3. Extras
    build_sitemap()
    print("\n[SUCCESS] The Grand Launch site is generated in /docs!")

if __name__ == "__main__":
    run()
