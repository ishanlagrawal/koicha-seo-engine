import os
import pickle
import base64
import json
import traceback
from googleapiclient.discovery import build
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import modules.review_engine as review_engine
import modules.sheet_utils as sheet_utils

# Cloud Persistence Paths
ROOT_DIR = Path(__file__).parent.parent
TOKEN_PATH = ROOT_DIR / "token.pickle"

def get_gmail_service():
    if not TOKEN_PATH.exists():
        print(f"[ERROR] token.pickle not found at {TOKEN_PATH}")
        return None
        
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
        
    return build('gmail', 'v1', credentials=creds)

def parse_review_email(payload):
    """Parses HTML body of a Google review notification."""
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    elif 'body' in payload:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

    if not body: return None

    soup = BeautifulSoup(body, 'html.parser')
    text_content = soup.get_text(separator=' ')

    name = "Valued Guest"
    if "review from" in text_content.lower():
        parts = text_content.lower().split("review from")
        if len(parts) > 1:
            name = parts[1].split("\n")[0].strip().split(" ")[0].title()

    rating = 5
    for i in range(1, 6):
        if f"{i}-star" in text_content.lower() or f"{i} star" in text_content.lower():
            rating = i
            break

    review_text = "No text provided."
    if "stars" in text_content.lower():
        review_parts = text_content.split("stars")
        if len(review_parts) > 1:
            review_text = review_parts[1].split("Reply")[0].strip().split("\n")[0]

    return {"name": name, "rating": rating, "text": review_text}

def load_processed_data():
    """Fetches already processed reviews from Google Sheet."""
    print("Checking Cloud Memory for processed reviews...")
    try:
        names = sheet_utils.sheet_editor.get_column_values("Review_Log", "B:B")
        texts = sheet_utils.sheet_editor.get_column_values("Review_Log", "D:D")
        return set(zip(names, texts))
    except Exception as e:
        print(f"[CLOUD ERROR] Persistence check failed: {e}")
        return set()

def poll_for_reviews():
    service = get_gmail_service()
    if not service: return

    query = 'review KOICHA'
    
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No new review emails found.")
            return

        processed_data = load_processed_data()
        current_total = sheet_utils.sheet_editor.get_row_count("Review_Log") - 1
        new_count = 0

        for msg in messages:
            msg_id = msg['id']
            message = service.users().messages().get(userId='me', id=msg_id).execute()
            payload = message.get('payload', {})
            review_data = parse_review_email(payload)
            
            if review_data:
                unique_key = (review_data['name'], review_data['text'])
                if unique_key in processed_data:
                    continue

                current_total += 1
                print(f"Detected new review #{current_total} from {review_data['name']}")
                
                config = review_engine.load_config()
                reply = review_engine.generate_reply(
                    review_data['name'], 
                    review_data['text'], 
                    review_data['rating'], 
                    config
                )
                
                review_engine.send_telegram_draft(
                    review_data['name'], 
                    review_data['text'], 
                    review_data['rating'], 
                    reply,
                    review_num=current_total
                )
                
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

        print(f"Watchdog cloud cycle complete. Processed {new_count} new review(s).")

    except Exception as e:
        print(f"Watchdog Core Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("\nKoicha Watchdog -- Cloud Active Scan")
    print("=" * 45)
    try:
        poll_for_reviews()
    except Exception:
        traceback.print_exc()
