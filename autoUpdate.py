import os
import argparse
from Function import get_file_description, extract_version, version_tuple, download_file_to_temp, download_file

GOOGLE_DRIVE_URL = "https://drive.google.com/file/d/1cHShM97WtO5fkNKIUZCXWZqldlQZsFZ2/view?usp=sharing"

def main():
    file_id = GOOGLE_DRIVE_URL.split('/')[5]  # Extract file ID from the link

    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("file_path", type=str, help="Path to the local file")
    parser.add_argument("action", type=str, choices=['0', '1'], help="0 for check update, 1 for download")
    args = parser.parse_args()
    LOCAL_FILE_PATH = args.file_path

    temp_path = None

    if args.action == '0':
        print("Checking for updates...")
        if os.path.exists(LOCAL_FILE_PATH):
            try:
                # Download the file to a temporary location
                temp_path = download_file_to_temp(
                    f"https://drive.google.com/uc?id={file_id}", 
                    file_name="tempFile.exe"
                )
                print(f"File downloaded to: {temp_path}")

                # Get file descriptions
                drive_file_info = get_file_description(temp_path)
                print("---Drive file Info---")
                print(drive_file_info)

                local_file_info = get_file_description(LOCAL_FILE_PATH)
                print("---Local file Info---")
                print(local_file_info)

                # Extract ProductVersion from both strings
                drive_version = extract_version(drive_file_info, "ProductVersion")
                local_version = extract_version(local_file_info, "ProductVersion")

                # Compare versions
                if drive_version and local_version:
                    drive_version_tuple = version_tuple(drive_version)
                    local_version_tuple = version_tuple(local_version)
                    
                    if drive_version_tuple > local_version_tuple:
                        print(f"Drive version {drive_version} is newer than Local version {local_version}.")
                    elif drive_version_tuple < local_version_tuple:
                        print(f"Local version {local_version} is newer than Drive version {drive_version}.")
                    else:
                        print(f"Both versions are the same: {drive_version}.")
                else:
                    print("One of the version strings is missing.")

            except Exception as e:
                print(f"An error occurred during version checking: {e}")

            else:
                print("Version comparison completed successfully.")

            finally:
                # Clean up the temporary file and directory
                if temp_path and os.path.exists(temp_path):
                    try:
                        # Remove the temporary file
                        os.remove(temp_path)
                        print(f"Temporary file {temp_path} has been deleted.")
                        
                        # Remove the directory
                        temp_dir = os.path.dirname(temp_path)
                        if os.path.exists(temp_dir):
                            os.rmdir(temp_dir)
                            print(f"Temporary directory {temp_dir} has been deleted.")

                    except Exception as cleanup_error:
                        print(f"Failed to clean up temporary files: {cleanup_error}")

        else:
            print("Local file does not exist. Use action '1' to download.")

    elif args.action == '1':
        print("Downloading file...")
        download_file(file_id, LOCAL_FILE_PATH)

if __name__ == "__main__":
    main()