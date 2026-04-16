import os
import pickle
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

def verify_gbp(target_id):
    if not os.path.exists('token.pickle'):
        print("[ERROR] token.pickle not found. Please run auth_blogger.py first.")
        return

    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

    # Use the Google Business Profile Information API
    # Note: This requires the API to be enabled in GCP!
    try:
        service = build('mybusinessbusinessinformation', 'v1', credentials=creds)
        
        # 1. Get Accounts
        accounts_service = build('mybusinessaccountmanagement', 'v1', credentials=creds)
        accounts_results = accounts_service.accounts().list().execute()
        accounts = accounts_results.get('accounts', [])
        
        if not accounts:
            print("[ERROR] No Google Business accounts found for this user.")
            return

        found = False
        for account in accounts:
            print(f"Searching in account: {account['name']} ({account['accountName']})...")
            # 2. List Locations for this account
            # The target_id might be the full resource name or just the ID
            locations_results = service.accounts().locations().list(
                parent=account['name'],
                readMask="name,title,storeCode"
            ).execute()
            
            locations = locations_results.get('locations', [])
            for loc in locations:
                loc_id = loc['name'].split('/')[-1]
                print(f" - Found Location: {loc['title']} (ID: {loc_id})")
                if loc_id == target_id:
                    print(f"\n✅ [SUCCESS] MATCH FOUND!")
                    print(f"Target ID {target_id} belongs to: {loc['title']}")
                    found = True
                    break
            if found: break
            
        if not found:
            print(f"\n❌ [FAILED] Could not find a business with ID {target_id} in your account.")
            print("Please double check the ID in Business Profile Settings > Advanced.")

    except Exception as e:
        print(f"\n[ERROR] API Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nTip: Make sure 'My Business Business Information API' and 'My Business Account Management API' are enabled in GCP Console.")

if __name__ == "__main__":
    test_id = os.getenv("GOOGLE_LOCATION_ID", "[YOUR_GOOGLE_LOCATION_ID]")
    verify_gbp(test_id)
