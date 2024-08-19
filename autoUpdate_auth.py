from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import datetime
import pickle
import argparse

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
GOOGLE_DRIVE_FILE_ID = "1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA"

# Function to get the path from the file name.
def find_file(search_dir, file_name):
    for root, dirs, files in os.walk(search_dir):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {"installed":{"client_id":CLIENT_ID,
                              "project_id":PROJECT_ID,
                              "token_uri":"https://oauth2.googleapis.com/token",
                              "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                              "client_secret":CLIENT_SECRET,
                              "redirect_uris":["http://localhost"]}},
                
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds 
        
def check_file_update(path_file):
    try:
        creds = get_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        # Get local file modification time
        local_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(path_file))
        local_mod_time = local_mod_time.replace(microsecond=0)  # Remove microseconds for comparison
        
       # Get Google Drive file
        drive_file = service.files().get(fileId=GOOGLE_DRIVE_FILE_ID, fields="modifiedTime").execute()
        drive_mod_time = datetime.datetime.strptime(drive_file['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        drive_mod_time = drive_mod_time.replace(tzinfo=None, microsecond=0)  # Remove timezone and microseconds

        print(f"Local file last modified: {local_mod_time}")
        print(f"Google Drive file last modified: {drive_mod_time}")

        if local_mod_time > drive_mod_time:
            print("Local file is newer")
        elif local_mod_time < drive_mod_time:
            print("Google Drive file is newer")
        else:
            print("Both files have the same modification time")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("file_path", type=str, help="Path to the local file")
    args = parser.parse_args()
    
    LOCAL_FILE_PATH = args.file_path
    if os.path.exists(LOCAL_FILE_PATH):
        print("Path file: ", LOCAL_FILE_PATH)
        check_file_update(LOCAL_FILE_PATH)
    else:
        print("File not found")

if __name__ == "__main__":
    main()
