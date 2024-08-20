import os
import datetime
import requests
import argparse

# Google Drive public link
GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?export=download&id=1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA"

# Function to compare a local file with a file on Google Drive.
def check_file_update(file_path):
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
            elif local_mod_time < drive_mod_time:
                print("Google Drive file is newer")
            else:
                print("Both files have the same modification time")
        else:
            print(f"Failed to access Google Drive file. Status code: {response.status_code}")

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
