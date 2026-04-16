import os
import pickle
import base64
import json
from googleapiclient.discovery import build
from pathlib import Path
from bs4 import BeautifulSoup
import modules.review_engine as review_engine

# Path to the token
TOKEN_PATH = Path("token.pickle")
REVIEWS_DIR = Path("data/reviews")
PROCESSED_FILE = REVIEWS_DIR / "processed_ids.json"

def get_gmail_service():
    if not TOKEN_PATH.exists():
        print("[ERROR] token.pickle not found. Run auth_blogger.py first.")
        return None
        
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
        
    return build('gmail', 'v1', credentials=creds)

def load_processed_ids():
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_id(msg_id):
    processed = list(load_processed_ids())
    processed.append(msg_id)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, 'w') as f:
        json.dump(processed, f)

def parse_review_email(payload):
    """
    Parses the HTML body of a Google Business Profile review notification.
    Expects typical patterns found in 'New review for [Business]' emails.
    """
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    elif 'body' in payload:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

    if not body:
        return None

    soup = BeautifulSoup(body, 'html.parser')
    text_content = soup.get_text(separator=' ')

    # Extract Name (Usually comes after "New review from" or near the top)
    # This is a heuristic and might need adjustment based on real emails
    name = "Valued Guest"
    if "review from" in text_content.lower():
        parts = text_content.lower().split("review from")
        if len(parts) > 1:
            name = parts[1].split("\n")[0].strip().split(" ")[0].title()

    # Extract Rating (Looking for stars or "X/5")
    rating = 5
    for i in range(1, 6):
        if f"{i}-star" in text_content.lower() or f"{i} star" in text_content.lower():
            rating = i
            break

    # Extract Review Text
    # Usually the block of text after the rating
    review_text = "No text provided."
    # Google emails often have the review text in a specific <td> or <div>
    # For now, we'll try to find the longest block or use a marker
    if "stars" in text_content.lower():
        review_parts = text_content.split("stars")
        if len(review_parts) > 1:
            review_text = review_parts[1].split("Reply")[0].strip().split("\n")[0]

    return {
        "name": name,
        "rating": rating,
        "text": review_text
    }

def load_counter():
    counter_file = Path("data/reviews/counter.json")
    if counter_file.exists():
        with open(counter_file, 'r') as f:
            return json.load(f).get("total_reviews", 0)
    return 0

def save_counter(count):
    counter_file = Path("data/reviews/counter.json")
    with open(counter_file, 'w') as f:
        json.dump({"total_reviews": count}, f)

import modules.sheet_utils as sheet_utils
from datetime import datetime

def load_processed_data():
    """Fetches already processed reviews from the Google Sheet to avoid duplicates."""
    print("Checking Cloud Memory for processed reviews...")
    # Column D is Review Text, Column B is Name. We use Text as a semi-unique ID.
    # In a full pro version, we'd log the Gmail Message ID.
    names = sheet_utils.sheet_editor.get_column_values("Review_Log", "B:B")
    texts = sheet_utils.sheet_editor.get_column_values("Review_Log", "D:D")
    return set(zip(names, texts))

def poll_for_reviews():
    service = get_gmail_service()
    if not service: return

    # Search for Google Business Profile notifications
    query = 'subject:"New review for KOICHA"'
    
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new review emails found.")
            return

        # Cloud Persistence - Fetch existing data
        processed_data = load_processed_data()
        current_total = sheet_utils.sheet_editor.get_row_count("Review_Log") - 1 # Subs header
        new_count = 0

        for msg in messages:
            msg_id = msg['id']
            # Fetch full message
            message = service.users().messages().get(userId='me', id=msg_id).execute()
            payload = message.get('payload', {})
            review_data = parse_review_email(payload)
            
            if review_data:
                # Deduplicate using name + text combo
                unique_key = (review_data['name'], review_data['text'])
                if unique_key in processed_data:
                    continue

                current_total += 1
                print(f"Detected new review #{current_total} from {review_data['name']}")
                
                # 1. Trigger the Review Engine Drafting
                config = review_engine.load_config()
                reply = review_engine.generate_reply(
                    review_data['name'], 
                    review_data['text'], 
                    review_data['rating'], 
                    config
                )
                
                # 2. Send to Telegram
                review_engine.send_telegram_draft(
                    review_data['name'], 
                    review_data['text'], 
                    review_data['rating'], 
                    reply,
                    review_num=current_total
                )
                
                # 3. Log to Master Google Sheet
                sheet_data = [
                    datetime.now().strftime("%Y-%m-%d"),
                    review_data['name'],
                    review_data['rating'],
                    review_data['text'],
                    reply,
                    "Ready for Approval"
                ]
                sheet_utils.sheet_editor.append_row("Review_Log", sheet_data)
                
                new_count += 1

        print(f"Watchdog cloud cycle complete. Processed {new_count} new review(s). Current Total: {current_total}")

    except Exception as e:
        print(f"Watchdog Error: {e}")

if __name__ == "__main__":
    print("Koicha Watchdog -- Manual Scan Initialized")
    poll_for_reviews()
