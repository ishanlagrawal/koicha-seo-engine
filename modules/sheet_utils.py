import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class KoichaSheetEditor:
    def __init__(self):
        self.spreadsheet_id = os.getenv('KOICHA_SHEET_ID')
        # Load Service Account
        sa_json = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
        self.creds = service_account.Credentials.from_service_account_info(sa_json)
        self.service = build('sheets', 'v4', credentials=self.creds)

    def get_column_values(self, tab_name, column_range="A:A"):
        """Fetches all values from a specific column."""
        range_name = f"{tab_name}!{column_range}"
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            values = result.get('values', [])
            # Flatten to a simple list
            return [v[0] for v in values if v]
        except Exception as e:
            print(f"[SHEET ERROR] Failed to read column from {tab_name}: {e}")
            return []

    def get_row_count(self, tab_name):
        """Returns the total number of non-empty rows."""
        values = self.get_column_values(tab_name)
        return len(values)

    def append_row(self, tab_name, data_row):
        """Appends a single row to the specified tab."""
        range_name = f"{tab_name}!A:A"
        body = {
            'values': [data_row]
        }
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"[SHEET] Successfully logged data to {tab_name}.")
        except Exception as e:
            print(f"[SHEET ERROR] Failed to append to {tab_name}: {e}")

# Global instance for easy use
sheet_editor = KoichaSheetEditor()
