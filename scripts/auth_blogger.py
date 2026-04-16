import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# The scope for Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Look for the JSON file we just downloaded
            if not os.path.exists('client_secrets.json'):
                print("Error: 'client_secrets.json' not found in project root!")
                return
                
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    print("\n[SUCCESS] Authentication complete! 'token.pickle' has been generated.")
    print("You can now run the Citation Builder to post automatically.")

if __name__ == '__main__':
    main()
