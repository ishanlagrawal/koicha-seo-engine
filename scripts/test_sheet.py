import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()

def test_sheet_access():
    sheet_id = os.getenv("KOICHA_SHEET_ID")
    service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open_by_key(sheet_id)
        print(f"[SUCCESS] Connected to sheet: {sheet.title}")
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")

if __name__ == "__main__":
    test_sheet_access()
