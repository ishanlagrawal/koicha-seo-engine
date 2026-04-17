import os
import json
import pickle
import requests
from pathlib import Path
from dotenv import load_dotenv
from google.auth.transport.requests import Request

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
TOKEN_PATH = "token_gbp.pickle"
# These will be set once user provides Location ID
# Format: accounts/{account_id}/locations/{location_id}
LOCATION_ID = os.getenv("GOOGLE_LOCATION_ID", "accounts/PLACEHOLDER/locations/PLACEHOLDER")

def load_config():
    if not CONFIG_PATH.exists(): return {"brand": {"name": "Koicha"}}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_credentials():
    """Loads and refreshes credentials from token_gbp.pickle."""
    if not os.path.exists(TOKEN_PATH):
        print(f"[FAIL] {TOKEN_PATH} not found. Run scripts/remote_auth_gbp.py first.")
        return None
        
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
        
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
            
    return creds

def create_local_post(summary, image_url=None):
    """Creates a 'What's New' post on Google Maps."""
    print(f"Drafting Maps post: {summary[:50]}...")
    
    creds = get_credentials()
    if not creds: return
    
    # API: https://developers.google.com/my-business/content/posts#creating_a_post
    url = f"https://mybusiness.googleapis.com/v4/{LOCATION_ID}/localPosts"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "languageCode": "en-US",
        "summary": summary,
        "topicType": "LOCAL_POST_TOPIC_TYPE_UNSPECIFIED",
        "callToAction": {
            "actionType": "LEARN_MORE",
            "url": "https://koicha-seo-engine.pages.dev/"
        }
    }
    
    if image_url:
        data["media"] = [{"mediaFormat": "PHOTO", "sourceUrl": image_url}]

    try:
        if "PLACEHOLDER" in LOCATION_ID:
            print("[SIM] Post draft created (waiting for REAL Location ID).")
            return
            
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("[SUCCESS] Post published to Google Maps!")
        else:
            print(f"[FAIL] GBP Error ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"[ERROR] GBP Post Exception: {e}")

def run():
    print("\nKoicha GBP Automation -- Module 3")
    print("=" * 45)
    config = load_config()
    
    # Best Answer Strategy: Daily Artisan Update
    update = "Fresh ceremonial matcha just arrived from Shizuoka! Limited batches daily in Koregaon Park. Visit us in Lane 7."
    create_local_post(update)
    
    print("\nModule 3 Automation Loop Complete.")

if __name__ == "__main__":
    run()
