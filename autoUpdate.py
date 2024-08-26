import os
import argparse
from Function import get_file_description, extract_version, version_tuple, download_file_to_temp, download_file, GetFileIDFromFolderDrive

def main():
    parser = argparse.ArgumentParser(description="Check or download a file from Google Drive.")
    parser.add_argument("action", type=int, choices=[0, 1], 
                        help="0 for check update, 1 for download")
    parser.add_argument("local_path", type=str, help="Path to the local file")
    parser.add_argument("temp_path", type=str, nargs='?', default=None,
                        help="Path to the temporary file (optional)")
    args = parser.parse_args()

    files = GetFileIDFromFolderDrive()
    if files is not None:
        if not files:
            print('No files found.')
        else:
            for file in files:
                file_id = file["id"]

    if args.action == 0:
        print("Checking for updates...")
        if os.path.exists(args.local_path):
            try:
                # Use provided temp_path or generate one
                temp_path = args.temp_path or download_file_to_temp(
                    f"https://drive.google.com/uc?id={file_id}", 
                    file_name="DexonInspectionStudio.exe"
                )
                print(f"File downloaded to: {temp_path}")

                # Get file descriptions
                drive_file_info = get_file_description(temp_path)
                print("---Drive file Info---")
                print(drive_file_info)

                local_file_info = get_file_description(args.local_path)
                print("---Local file Info---")
                print(local_file_info)

                # Extract ProductVersion from both strings
                drive_version = extract_version(drive_file_info, "ProductVersion")
                local_version = extract_version(local_file_info, "ProductVersion")

                # Compare versions
                if drive_version and local_version:
                    drive_version_tuple = version_tuple(drive_version)
                    local_version_tuple = version_tuple(local_version)
                    print()
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

            finally:
                # Clean up the temporary file if it was auto-generated
                if not args.temp_path and temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                        temp_dir = os.path.dirname(temp_path)
                        if os.path.exists(temp_dir):
                            os.rmdir(temp_dir)
                    except Exception as cleanup_error:
                        print(f"Failed to clean up temporary files: {cleanup_error}")

        else:
            print("Local file does not exist. Use action '1' to download.")

    elif args.action == 1:
        if args.temp_path and os.path.exists(args.temp_path):
            print(f"Moving file from {args.temp_path} to {args.local_path}...")
            os.rename(args.temp_path, args.local_path)
        else:
            print("Downloading file...")
            download_file(file_id, args.local_path)

if __name__ == "__main__":
    main()