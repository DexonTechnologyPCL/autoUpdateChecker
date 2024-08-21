import os
import datetime
import requests
import argparse

# Google Drive public link
GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?export=download&id=1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA"

def download_file(url, destination):
    """
    Download a file from the given URL to the specified destination.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File successfully downloaded to {destination}")
        return True
    except Exception as e:
        print(f"An error occurred while downloading: {e}")
        return False

def check_file_update(file_path):
    """
    Compare a local file with a file on Google Drive.
    Returns True if Google Drive file is newer, False otherwise.
    """
    try:
        # Get local file modification time
        local_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        local_mod_time = local_mod_time.replace(microsecond=0)  # Remove microseconds for comparison
        
        # Get Google Drive file
        response = requests.head(GOOGLE_DRIVE_LINK, allow_redirects=True)
        if response.status_code == 200:
            drive_mod_time = datetime.datetime.strptime(response.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')
            drive_mod_time = drive_mod_time.replace(tzinfo=None)
            print(f"Local file last modified: {local_mod_time}")
            print(f"Google Drive file last modified: {drive_mod_time}")
            if local_mod_time > drive_mod_time:
                print("Local file is newer")
                return False
            elif local_mod_time < drive_mod_time:
                print("Google Drive file is newer")
                return True
            else:
                print("Both files have the same modification time")
                return False
        else:
            print(f"Failed to access Google Drive file. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred while checking for updates: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("file_path", type=str, help="Path to the local file")
    parser.add_argument("action", type=str, choices=['0', '1'], help="0 for check update, 1 for download")
    args = parser.parse_args()
    
    LOCAL_FILE_PATH = args.file_path
    
    if args.action == '0':
        print("Checking for updates...")
        if os.path.exists(LOCAL_FILE_PATH):
            check_file_update(LOCAL_FILE_PATH)
        else:
            print("Local file does not exist. Use action '1' to download.")
    elif args.action == '1':
        print("Downloading file...")
        download_file(GOOGLE_DRIVE_LINK, LOCAL_FILE_PATH)

if __name__ == "__main__":
    main()