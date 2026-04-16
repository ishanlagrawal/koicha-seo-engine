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
    """Fetches top snippets from Google Search."""
    print(f"  [SPY] Searching signals for: '{query}'...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200: return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = [s.get_text() for s in soup.find_all('div', class_='VwiC3b')]
        return snippets[:5]
    except Exception as e:
        print(f"  [FAIL] Search error: {e}")
        return []

import google.generativeai as genai

def analyze_intelligence(name, snippets):
    """Uses the official Google AI library to extract data from snippets."""
    print(f"  [AI] Analyzing intelligence for {name}...")
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Analyze these search snippets for the competitor '{name}' (a Korean restaurant in Pune).
        EXTRACT ONLY STRUCTURED JSON:
        {{
          "avg_price_gimbap": (integer, estimate from text),
          "rating": (float, e.g. 4.2),
          "weakness": "one sentence on recent complaints or menu gaps found in text",
          "strategy": "one sentence strategic advice for Koicha to beat them"
        }}
        
        SNIPPETS: {snippets}
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Extract JSON from Markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "{" in text:
             text = "{" + text.split("{", 1)[1].rsplit("}", 1)[0] + "}"
        return json.loads(text.strip())
    except Exception as e:
        print(f"  [ERROR] AI Analysis failed for {name}: {e}")
        return {
            "avg_price_gimbap": 300,
            "rating": 4.0,
            "weakness": "Data unavailable; manual check recommended.",
            "strategy": "Maintenance mode."
        }
        return {
            "avg_price_gimbap": 300,
            "rating": 4.0,
            "weakness": "Data unavailable; manual check recommended.",
            "strategy": "Maintenance mode."
        }

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
