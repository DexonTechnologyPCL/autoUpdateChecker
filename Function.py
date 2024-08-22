import os
import datetime
import requests
import argparse
import io


def get_drive_file_info(file_id):
    """
    get file date modified on google drive
    """
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=modifiedTime&key=AIzaSyBSB78H_UW2AoC-o_hmFlT0tIS0zAvXoOM"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        file_info = response.json()
        modified_time = datetime.datetime.fromisoformat(file_info['modifiedTime'][:-1])  # Remove 'Z' from the end
        return modified_time
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_local_file_info(file_path):
    if os.path.exists(file_path):
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        return modified_time
    else:
        print(f"Error: Local file not found at {file_path}")
        return None

def download_file(url, destination):
    """
    Download a file from the given Google Drive URL to the specified destination.
    """
    # Extract the file ID from the URL
    file_id = url.split('/')[5]
    
    # Google Drive API endpoint for downloading files
    download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&key=AIzaSyBSB78H_UW2AoC-o_hmFlT0tIS0zAvXoOM"
    
    try:
        # Send a GET request to download the file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Open the destination file in binary write mode
        with open(destination, 'wb') as f:
            # Iterate over the response data and write it to the file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"File successfully downloaded to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing file: {e}")

def check_file_update(drive_time, local_time):
    """
    Compare a local file with a file on Google Drive.
    Returns True if Google Drive file is newer, False otherwise.
    """
    if drive_time and local_time:
        if drive_time > local_time:
            print(f"The Google Drive file is newer")
            print("Please update your local file.")
        elif local_time > drive_time:
            print(f"The local file is newer")
        else:
            print("Both files have the same modification time")
    else:
        print("Unable to compare modification dates due to missing information")

def runCheckAutoUpdate():
    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("file_path", type=str, help="Path to the local file")
    parser.add_argument("action", type=str, choices=['0', '1'], help="0 for check update, 1 for download")
    args = parser.parse_args()
    
    GOOGLE_DRIVE_URL = "https://drive.google.com/file/d/1cHShM97WtO5fkNKIUZCXWZqldlQZsFZ2/view?usp=sharing"
    file_id = GOOGLE_DRIVE_URL.split('/')[5]  # Extract file ID from the link

    LOCAL_FILE_PATH = args.file_path

    if args.action == '0':
        print("Checking for updates...")
        if os.path.exists(LOCAL_FILE_PATH):
            drive_file_info = get_drive_file_info(file_id)
            local_file_info = get_local_file_info(LOCAL_FILE_PATH)

            if drive_file_info:
                print(f"Google Drive file was last modified on: {drive_file_info}")
            else:
                print("Could not retrieve Google Drive file information.")

            if local_file_info:
                print(f"Local file was last modified on: {local_file_info}")
            else:
                print("Could not retrieve local file information.")

            check_file_update(drive_file_info, local_file_info)
        else:
            print("Local file does not exist. Use action '1' to download.")

    elif args.action == '1':
        print("Downloading file...")
        download_file(GOOGLE_DRIVE_URL, LOCAL_FILE_PATH)
    
def main():
    runCheckAutoUpdate()

if __name__ == "__main__":
    main()