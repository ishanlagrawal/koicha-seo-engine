import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/business.manage']

def main():
    """Generates a token.pickle for Google Business Profile API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token_gbp.pickle'):
        with open('token_gbp.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # IMPORTANT: Use the credentials.json from your GCP Project
            # Ensure Google Business Profile API is enabled in GCP Console.
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            # Use console flow for remote authorization
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print("\n" + "="*60)
            print("REMOTE AUTHORIZATION REQUIRED (KOICHA OFFICIAL)")
            print("="*60)
            print(f"\n1. Send this URL to your friend:\n\n{auth_url}")
            print("\n2. Ask them to login with Koicha Official Gmail.")
            print("3. They will be redirected to a 'localhost' URL which will fail to load.")
            print("4. ASK THEM TO COPY THE FULL URL of that failed page and send it back to you.")
            print("\n" + "="*60)
            
            redirect_url = input("\nPASTE THE FULL REDIRECT URL HERE: ").strip()
            flow.fetch_token(authorization_response=redirect_url)
            creds = flow.credentials

        # Save the credentials for the next run
        with open('token_gbp.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    print("\n[SUCCESS] token_gbp.pickle generated successfully!")

if __name__ == '__main__':
    main()
