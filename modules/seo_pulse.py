import os
import requests
from bs4 import BeautifulSoup
import modules.sheet_utils as sheet_utils
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Strategy: Key terms we want to dominate in Pune
KEYWORDS = [
    "Best Matcha in Pune",
    "Korean food Koregaon Park",
    "Artisan Gimbap Pune",
    "Koicha Pune Reviews"
]

def check_rank(keyword, target_domain="ishanlagrawal.github.io"):
    """
    Simulates a Google Search search to find the ranking of the target_domain.
    We'll use a specific User-Agent to mimic a human search.
    """
    print(f"Tracking Rank for: '{keyword}'...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    # We use 'google.co.in' for local Indian context
    search_url = f"https://www.google.co.in/search?q={keyword.replace(' ', '+')}&num=20"
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            print(f"[FAIL] Google blocked the search (Status {response.status_code})")
            return "N/A"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Google result links are usually in <div> -> <a> -> <h3>
        links = soup.find_all('div', class_='yuRUbf') # This class often changes, but is common
        
        for i, link in enumerate(links, 1):
            url = link.find('a')['href']
            if target_domain in url or "koicha" in url.lower():
                return i
                
        return ">20" # Not found in top 20
        
    except Exception as e:
        print(f"Ranking Error: {e}")
        return "Error"

def run_pulse():
    print("\nKoicha SEO Pulse -- Weekly Ranking Audit")
    print("=" * 45)
    
    results = []
    for kw in KEYWORDS:
        rank = check_rank(kw)
        print(f"Keyword: {kw} | Current Rank: {rank}")
        
        # Log to Master Sheet
        sheet_data = [
            datetime.now().strftime("%Y-%m-%d"),
            kw,
            rank,
            "Check Log", # Placeholder for 'Change' logic if we want to compare with yesterday
            "Automated weekly scan"
        ]
        sheet_utils.sheet_editor.append_row("SEO_Pulse", sheet_data)
        
    print("\n[SUCCESS] SEO Pulse Audit complete. Check your Master Sheet!")

if __name__ == "__main__":
    run_pulse()
