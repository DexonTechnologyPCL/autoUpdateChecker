import os
import datetime
import requests
import argparse
from pathlib import Path
import pefile
import re
import tempfile
import gdown

# GOOGLE_DRIVE_API = "AIzaSyBSB78H_UW2AoC-o_hmFlT0tIS0zAvXoOM"
GOOGLE_DRIVE_API = ""
#********************************************************************************************************************************
def get_drive_file_info(file_id):
    """
    get file date modified on google drive
    """
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=modifiedTime&key={GOOGLE_DRIVE_API}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        file_info = response.json()
        modified_time = datetime.datetime.fromisoformat(file_info['modifiedTime'][:-1])  # Remove 'Z' from the end
        return modified_time
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    
#********************************************************************************************************************************
def get_local_file_info(file_path):
    if os.path.exists(file_path):
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        return modified_time
    else:
        print(f"Error: Local file not found at {file_path}")
        return None
    
#********************************************************************************************************************************
def download_file(file_id, destination):
    """
    Download a file from the given Google Drive URL to the specified destination.
    """
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

#********************************************************************************************************************************
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

#********************************************************************************************************************************
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

#********************************************************************************************************************************
def get_file_description(file_path):
    # Example path = Path('D:/Project/2024_026/DaconInspectionStudio/x64/Debug/DaconInspectionStudio.exe')
    path = Path(file_path)
    pe = pefile.PE(str(path))

    file_info = []

    # Extract the file description
    for fileinfo in pe.FileInfo:
        for entry in fileinfo:
            if entry.Key == b'StringFileInfo':
                for st in entry.StringTable:
                    for key, value in st.entries.items():
                        # if key.decode() == 'FileDescription':
                            # print(f"File Description: {value.decode()}")
                            # print(f"{key.decode()} : {value.decode()}")
                        file_info.append(f"{key.decode()}: {value.decode()}")

    # Join all the information into a single string
    return "\n".join(file_info)

#********************************************************************************************************************************
def extract_version(text, label):
    # Function to extract version number
    match = re.search(rf"{label}:\s*([\d\.]+)", text)
    if match:
        return match.group(1)
    return None

#********************************************************************************************************************************
def version_tuple(version_str):
    # Convert version string to a tuple of integers
    return tuple(map(int, version_str.split('.')))

#********************************************************************************************************************************
def DownloadDriveToTemp(url):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url.split('/')[-1])[1]) as temp_file:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=8192):
            temp_file.write(chunk)
        return temp_file.name, os.path.basename(temp_file.name)
    
#********************************************************************************************************************************
def download_file_to_temp(url, file_name=None):
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # If file_name is not provided, set a default name
        if not file_name:
            file_name = "downloaded_file"

        # Full path to save the file
        temp_file_path = os.path.join(temp_dir, file_name)

        # Use gdown to download the file to the specified path
        gdown.download(url, temp_file_path, quiet=True)

        # Return the path to the downloaded file
        return temp_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# downloaded_file_path = download_file_to_temp(
#     'https://drive.google.com/uc?id=1cHShM97WtO5fkNKIUZCXWZqldlQZsFZ2',
#     file_name="dex.exe"
# )
# print(f"File downloaded to: {downloaded_file_path}")

#********************************************************************************************************************************
def read_public_google_drive_file(file_id):
    # Construct the download URL
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Get the content as text
        content = response.text
        
        return content
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
#********************************************************************************************************************************
def runReadContent():
    # Usage
    file_id = '1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA'  # Replace with the actual file ID
    content = read_public_google_drive_file(file_id)

    if content:
        return content
    else:
        print("Failed to read the file.")
