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

CONFIG_PATH = Path(__file__).parent.parent / "config/koicha_config.json"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

def load_config():
    if not CONFIG_PATH.exists():
        return {"brand": {"name": "Koicha"}}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_reply(name, review_text, rating, config):
    print(f"Drafting artisan reply for {name} ({rating} stars)...")
    
    brand = config["brand"]["name"]
    # The 'Artisan' Persona with TONE MIMICRY
    prompt = f"""
You are the owner and lead artisan of {brand}, a boutique Korean food & matcha kitchen in Pune.
Task: Write a short, warm, and authentic reply that feels "Homely" and personal.

Customer Name: {name}
Rating: {rating}-star
Review: "{review_text}"

Voice Guidelines:
1. Tone Mimicry (CRITICAL): Analyze the reviewer's tone. If they are casual and enthusiastic, be casual and enthusiastic. If they are brief and professional, match that elegance. 
2. Persona: Maintain your "Artisan" identity (first-person, passionate about ingredients).
3. If Rating is 1-3: Switch to "Humble Resolution" voice (Sincere apology, ownership of standards).
4. Language: If they use Hinglish/Hindi phrases, feel free to mirror that warmth in your English response.

Mandatory SEO: Naturally include "Korean food in Pune" or "Artisan Gimbap".
Length: 35-45 words.

Return ONLY the reply text. No quotes.
    """
    
    if not GROQ_API_KEY:
        return "Intelligence engine pending setup."
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    import time
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                print(f"[RETRY {attempt+1}] Groq returned status {response.status_code}")
        except Exception as e:
            print(f"[RETRY {attempt+1}] Connection Error: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2) 
            
    return "The artisan brain is resting. Please try again in a moment."

def send_telegram_draft(name, review_text, rating, reply_text, review_num=None):
    """Sends the context (with stars and #) and the reply."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("[SKIP] Telegram credentials missing.")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    stars = "⭐" * int(rating)
    review_label = f" #{review_num}" if review_num else ""
    
    # Message 1: The Context (Now with Stars and #)
    context_msg = (
        f"👤 *Reviewer:* {name}\n"
        f"⭐ *Rating:* {stars}\n"
        f"📍 *Review {review_label}*\n"
        f"💬 \"{review_text}\""
    )
    
    # Message 2: The Artisan Reply
    reply_msg = f"{reply_text}"
    
    try:
        requests.post(url, json={"chat_id": chat_id, "text": context_msg, "parse_mode": "Markdown"})
        requests.post(url, json={"chat_id": chat_id, "text": reply_msg})
        print(f"[SUCCESS] {rating}-star draft sent for {name}.")
    except Exception as e:
        print(f"Telegram Error: {e}")

def run():
    print("\nKoicha Review Intelligence -- Module 4")
    print("=" * 45)
    config = load_config()
    
    inbox_path = Path("data/reviews/inbox.json")
    outbox_path = Path("data/reviews/outbox.json")
    
    if not inbox_path.exists() or os.stat(inbox_path).st_size == 0:
        print("Inbox is empty. No reviews to process.")
        return

    with open(inbox_path, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    if not reviews:
        print("No new reviews in inbox.")
        return

    outbox = []
    print(f"Processing {len(reviews)} review(s)...")
    
    for rev in reviews:
        name = rev.get("name", "valued guest")
        text = rev.get("text", "")
        rating = rev.get("rating", 5)
        
        reply = generate_reply(name, text, rating, config)
        
        # 1. Send to Telegram (Passing Rating)
        send_telegram_draft(name, text, rating, reply)
        
        # 2. Add to Outbox
        outbox.append({
            "reviewer": name,
            "rating": rating,
            "review": text,
            "draft": reply,
            "status": "ready"
        })

    # Save to Outbox
    with open(outbox_path, "w", encoding="utf-8") as f:
        json.dump(outbox, f, indent=4)
        
    print(f"\n[DONE] {len(outbox)} drafts saved to data/reviews/outbox.json")

if __name__ == "__main__":
    run()
