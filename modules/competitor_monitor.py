import os
import json
import requests
import time
from bs4 import BeautifulSoup
import modules.sheet_utils as sheet_utils
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Targets
COMPETITORS = {
    "KINI": "Kini Koregaon Park Pune menu prices",
    "Seoul Bunsik": "Seoul Bunsik Pune menu price reviews"
}

def search_snippets(query):
    """Fetches top snippets from Google Search with multi-selector fallback."""
    print(f"  [SPY] Searching signals for: '{query}'...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: 
            print(f"  [WARN] Google blocked or error {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Google changes classes often; check multiple likely containers
        snippets = []
        for selector in ['div.VwiC3b', 'div.BNeawe.s3Eb9c.AP7Wnd', 'span.hgKElc']:
            found = [s.get_text() for s in soup.select(selector)]
            if found:
                snippets.extend(found)
        
        return list(set(snippets))[:5]
    except Exception as e:
        print(f"  [FAIL] Search error: {e}")
        return []

import google.generativeai as genai

def analyze_intelligence(name, snippets):
    """Uses Gemini 1.5 Flash with robust JSON extraction."""
    print(f"  [AI] Analyzing intelligence for {name}...")
    
    # Default fallback
    fallback = {
        "avg_price_gimbap": 300,
        "rating": 4.0,
        "weakness": "Direct observation needed (Parser Lag).",
        "strategy": "Maintain artisan exclusivity via limited batches."
    }

    if not snippets:
        return fallback

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key: return fallback

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Analyze these search snippets for competitor '{name}' in Pune.
        Extract JSON ONLY. No markdown.
        {{
          "avg_price_gimbap": int,
          "rating": float,
          "weakness": "short sentence",
          "strategy": "short tactical advice for Koicha"
        }}
        SNIPPETS: {snippets}
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean Markdown characters
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        
        return json.loads(text)
    except Exception as e:
        print(f"  [AI FAIL] Intelligent Parse failed: {e}")
        return fallback

def run():
    print("\nKoicha Intelligence Engine -- Real-Time Module 5")
    print("=" * 45)
    
    for name, query in COMPETITORS.items():
        # 1. Gather signals
        snippets = search_snippets(query)
        time.sleep(10) # Pause to avoid Google blocks
        
        # 2. Extract Data with AI
        intel = analyze_intelligence(name, snippets)
        
        # 3. Log to Master Command Center
        sheet_data = [
            datetime.now().strftime("%Y-%m-%d"),
            name,
            f"Gimbap (Real-Time Est: ₹{intel['avg_price_gimbap']})",
            f"{intel['rating']} / 5 Stars",
            intel['weakness'],
            intel['strategy']
        ]
        sheet_utils.sheet_editor.append_row("Competition_Tracker", sheet_data)
        
        print(f"[SUCCESS] {name} Intel sync'd to Master Sheet.")

if __name__ == "__main__":
    run()
