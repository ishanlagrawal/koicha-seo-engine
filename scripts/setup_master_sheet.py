import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def setup_sheets():
    print("Initializing Koicha Master Command Center...")
    
    # Load Service Account
    sa_json = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
    creds = service_account.Credentials.from_service_account_info(sa_json)
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = os.getenv('KOICHA_SHEET_ID')

    # Define the 6 tabs and their headers
    TABS = {
        "Article_Log": ["Date", "Platform", "Title", "Link", "Status", "Keywords"],
        "Content_Planner": ["Draft_Topic", "Target_Date", "Strategy", "AI_Status"],
        "Review_Log": ["Date", "Reviewer", "Rating", "Review_Text", "Artisan_Draft", "Status"],
        "Competition_Tracker": ["Date", "Competitor", "Item", "Price", "Strategy_Insight"],
        "SEO_Pulse": ["Date", "Keyword", "Rank_Position", "Change", "Notes"],
        "Citation_Audit": ["Platform", "Status", "NAP_Confirmed", "Link", "Notes"]
    }

    try:
        # 1. Get current sheets
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        existing_tabs = [sheet.get('properties').get('title') for sheet in spreadsheet.get('sheets')]
        
        requests = []
        
        # 2. Add missing tabs
        for tab_name in TABS.keys():
            if tab_name not in existing_tabs:
                requests.append({
                    "addSheet": {
                        "properties": {"title": tab_name}
                    }
                })
        
        if requests:
            service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": requests}).execute()
            print(f"Added {len(requests)} new tabs.")

        # 3. Setup Headers for each tab
        header_requests = []
        for tab_name, headers in TABS.items():
            header_requests.append({
                "updateCells": {
                    "range": {
                        "sheetId": next(s['properties']['sheetId'] for s in service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()['sheets'] if s['properties']['title'] == tab_name),
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": len(headers)
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {"stringValue": h},
                                    "userEnteredFormat": {
                                        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True}
                                    }
                                } for h in headers
                            ]
                        }
                    ],
                    "fields": "userEnteredValue,userEnteredFormat"
                }
            })

        if header_requests:
            service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": header_requests}).execute()
            print("Successfully initialized all headers with premium styling.")

        print("\n[SUCCESS] Master Command Center is ready!")
        print(f"URL: {os.getenv('GOOGLE_SHEET_URL')}")

    except Exception as e:
        print(f"[ERROR] Failed to setup sheets: {e}")

if __name__ == "__main__":
    setup_sheets()
