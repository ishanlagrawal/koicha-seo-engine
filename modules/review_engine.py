"""
Module 4: Review Intelligence
=============================
Generates keyword-rich, on-brand replies to Google Reviews.
Uses Groq (Llama 3) for warm, artisan tone.
"""

import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_reply(review_text, rating, config):
    print(f"Generating reply for {rating}-star review...")
    
    brand = config["brand"]["name"]
    voice = config["brand_voice"]
    targets = config["seo_targets"]["primary"]
    
    prompt = f"""
You are the owner of {brand}, a Korean food & matcha pop-up in Pune.
Write a warm, artisan reply to this {rating}-star review.

Review: "{review_text}"

Voice Guidelines:
- Tone: {voice["tone"]}
- Use: {", ".join(voice["use"])}
- NEVER use: {", ".join(voice["never_use"])}
- Max words: {voice["max_response_words"]}

SEO Goal: Naturally include one of these keywords if it fits: {", ".join(targets)}

Return ONLY the reply text.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    return "Error generating reply."

def run():
    print("\nKoicha Review Intelligence -- Module 4")
    print("=" * 45)
    config = load_config()
    
    # Simulation for now (Integration with GBP API in Module 3)
    test_review = "Loved the matcha latte! Best gimbap in Pune."
    reply = generate_reply(test_review, 5, config)
    
    print(f"\nSample Review: {test_review}")
    print(f"Generated Reply:\n{reply}")
    
    print("\nModule 4 Ready for API Integration.")

if __name__ == "__main__":
    run()
