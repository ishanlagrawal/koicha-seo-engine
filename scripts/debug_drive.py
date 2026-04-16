import os
import pickle
from googleapiclient.discovery import build

def list_drive_files(folder_id):
    if not os.path.exists('token.pickle'):
        print("token.pickle not found!")
        return
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)"
    ).execute()
    
    files = results.get('files', [])
    if not files:
        print("No files found in this folder.")
    else:
        for f in files:
            print(f"- {f['name']} ({f['mimeType']})")

if __name__ == "__main__":
    list_drive_files('1btA4R9L-coFjiwbgc8GhpIbT6u14QNyH')
