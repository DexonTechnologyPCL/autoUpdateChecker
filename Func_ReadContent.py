import requests

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
    
def runReadContent():
    # Usage
    file_id = '1tuEWr7LQ5_6CRzLxjghG4tNvvekKa0ZA'  # Replace with the actual file ID
    content = read_public_google_drive_file(file_id)

    if content:
        print(content)
    else:
        print("Failed to read the file.")

def main():
    runReadContent()

if __name__ == "__main__":
    main()


