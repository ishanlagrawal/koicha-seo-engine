import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Ensure the project root is in PYTHONPATH
sys.path.append(os.getcwd())

import modules.review_engine as review_engine

load_dotenv()

def test_telegram_flow():
    print("Testing Telegram Review Bridge...")
    
    # 1. Setup dummy reviews in the inbox
    dummy_reviews = [
        {
            "name": "Arjun K.",
            "rating": 5,
            "text": "The Matcha Gimbap was incredible. The crunch and the quality of seaweed is top notch."
        },
        {
            "name": "Priya M.",
            "rating": 4,
            "text": "The Matcha was very authentic. I just wish the seating was a bit more cozy, but the food is great."
        },
        {
            "name": "Vikram S.",
            "rating": 2,
            "text": "Bhai, gimbap ka taste thoda off tha aaj. Seaweed was very soggy. Expected better from Koicha."
        }
    ]
    
    inbox_path = Path("data/reviews/inbox.json")
    os.makedirs(inbox_path.parent, exist_ok=True)
    
    with open(inbox_path, "w", encoding="utf-8") as f:
        json.dump(dummy_reviews, f)
        
    print(f"Created test reviews for {len(dummy_reviews)} customers.")
    
    # 2. Run the engine
    review_engine.run()
    
    print("\nCheck your Telegram! You should see a new draft message.")

if __name__ == "__main__":
    test_telegram_flow()
