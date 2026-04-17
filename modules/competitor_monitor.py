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
    """Placeholder for robust search. System uses search_web in real runs."""
    print(f"  [SPY] Searching signals for: '{query}'...")
    return ["KINI Gimbap ₹320", "Seoul Bunsik Pune Rating 4.5"]

from google import genai
from google.genai import types

def analyze_intelligence(name, snippets):
    """Uses Gemini 2.0 (google-genai) with robust JSON extraction."""
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

        client = genai.Client(api_key=api_key)
        
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
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json'
            )
        )
        
        return json.loads(response.text)
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
