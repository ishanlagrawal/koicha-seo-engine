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
    """Generates a high-SEO, artisan-grade reply to a review."""
    print(f"Drafting artisan reply for {name} ({rating}-stars)...")
    
    brand = config['brand']['name']

    system_prompt = f"""
    You are the real owner of {brand} in Koregaon Park, Pune.
    You care deeply about craft, freshness, and how people feel after eating with you.
    You are warm, observant, and grounded. Never sound corporate, polished-for-PR, or AI-written.

    Write a short reply to this review that feels like it came from a real human who remembers the place, the food, and the guest experience.

    Rules:
    - 1 to 3 short sentences.
    - Use natural spoken English. Light Hinglish is okay only if the guest used it first.
    - Match the guest’s energy: playful, quiet, excited, elegant, disappointed.
    - Thank them specifically for what they noticed, not with generic praise.
    - If the rating is low, acknowledge the issue plainly, take ownership, and invite them back without sounding defensive or scripted.
    - NEVER use clichés like "we are thrilled", "means a lot", "delighted", "serving customers", or "valued feedback".
    - Do not force SEO phrases. Only mention "Korean food in Pune", "matcha", "gimbap", or "Lane 7" if it fits naturally.
    - No emojis unless the original review uses them.
```python
    """
    
    user_prompt = f"Name: {name}\nRating: {rating}\nText: {review_text}"
    
    if not GROQ_API_KEY:
        return "Intelligence engine pending setup."

    # Using higher-tier model for Phase 2
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        "temperature": 0.7
    }
    
    import requests
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"].strip()
            
            # QC Layer: Strip out common AI signatures
            banned = ["excited to hear", "means the world", "valued customer", "delighted to"]
            for word in banned:
                if word in reply.lower():
                    reply = reply.split(".")[0] + "."
            return reply
        return "The artisan brain is resting. Please try again."
    except Exception as e:
        print(f"Reply Generation Error: {e}")
        return "The artisan is dreaming..."

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
