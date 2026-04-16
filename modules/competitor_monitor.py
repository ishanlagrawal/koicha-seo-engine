"""
Module 5: Competitor Monitor
============================
Scrapes/Monitors competitor prices and SEO ranking.
Alerts via Telegram on significant changes.
"""

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv()

CONFIG_PATH = Path("config/koicha_config.json")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def send_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"Alert (No Telegram): {message}")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": f"🚨 COMPETITOR ALERT: {message}"}
    requests.post(url, json=payload)

def monitor_kini_zomato():
    # KINI link found: https://www.zomato.com/pune/kini-koregaon-park
    # Note: Zomato/Swiggy often block simple scraping. 
    # In a real engine, we'd use a proxy or specialized API (like SerpApi).
    # For now, we simulate the monitoring logic.
    print("Monitoring KINI on Zomato...")
    # Simulation:
    test_price_change = False 
    if test_price_change:
        send_alert("KINI (Koregaon Park) changed Gimbap prices from 280 to 250!")

def check_search_rankings(config):
    print("Checking SEO Rankings...")
    targets = config["seo_targets"]["primary"]
    # Logic: Search via Google Search API or Scraper
    # For now, print status
    for target in targets:
        print(f"Tracking ranking for: {target}")

def run():
    print("\nKoicha Competitor Monitor -- Module 5")
    print("=" * 45)
    config = load_config()
    
    monitor_kini_zomato()
    check_search_rankings(config)
    
    print("\nModule 5 Monitoring Cycle Complete.")

if __name__ == "__main__":
    run()
