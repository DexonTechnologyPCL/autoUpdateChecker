import os
import argparse
from Func_ReadContent import runReadContent
from Function import get_file_description, extract_version, version_tuple

def main():
    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("file_path", type=str, help="Path to the local file")
    parser.add_argument("action", type=str, choices=['0', '1'], help="0 for check update, 1 for download")
    args = parser.parse_args()
    LOCAL_FILE_PATH = args.file_path

    if args.action == '0':
        print("Checking for updates...")
        if os.path.exists(LOCAL_FILE_PATH):
            drive_file_info = runReadContent()
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

        else:
            print("Local file does not exist. Use action '1' to download.")

    elif args.action == '1':
        print("Downloading file...")
        # download_file(GOOGLE_DRIVE_URL, LOCAL_FILE_PATH)


if __name__ == "__main__":
    main()