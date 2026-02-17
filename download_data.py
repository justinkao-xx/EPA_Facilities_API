import requests
import zipfile
import os
import subprocess
import sys

# URL for EPA FRS National Single File
EPA_URL = "https://ordsext.epa.gov/fla/www3/state_files/national_single.zip"
ZIP_FILENAME = "national_single.zip"
CSV_FILENAME = "national_single.csv"
PARQUET_FILENAME = "epa_facilities.parquet"

def download_file(url, filename):
    """Downloads a file from a URL with a progress bar."""
    print(f"Downloading {filename} from {url}...")
    # Add User-Agent to avoid being blocked by some servers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        total_length = r.headers.get('content-length')
        
        with open(filename, 'wb') as f:
            if total_length is None: # no content length header
                f.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl/1024/1024:.2f} MB")
                    sys.stdout.flush()
    print("\nDownload complete.")

def unzip_file(zip_filepath, extract_to="."):
    """Unzips a zip file."""
    print(f"Unzipping {zip_filepath}...")
    try:
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Unzip complete.")
    except zipfile.BadZipFile:
        print(f"\nERROR: {zip_filepath} is not a valid zip file.")
        print("Dumping first 500 bytes of file content for debugging:")
        with open(zip_filepath, 'rb') as f:
            print(f.read(500))
        raise

def main():
    if os.path.exists(PARQUET_FILENAME):
        print(f"{PARQUET_FILENAME} already exists. Skipping download.")
        return

    # 1. Download
    if not os.path.exists(ZIP_FILENAME) and not os.path.exists(CSV_FILENAME):
        download_file(EPA_URL, ZIP_FILENAME)

    # 2. Unzip
    if not os.path.exists(CSV_FILENAME):
        unzip_file(ZIP_FILENAME)

    # 3. Convert to Parquet
    print("Converting to Parquet...")
    # Update convert_data.py to use the current directory CSV if the hardcoded path is wrong
    # Or we can just import the logic. 
    # For now, let's assume convert_data.py needs a slight tweak or we run it as is.
    # The existing convert_data.py points to /Users/justinkao/Downloads/... which won't work in Docker.
    # We should update convert_data.py first to be relative.
    
    # We will invoke convert_data.py as a subprocess, but first we need to ensure it looks in the current dir.
    subprocess.run(["python3", "convert_data.py"], check=True)

    # 4. Cleanup
    print("Cleaning up temporary files...")
    if os.path.exists(ZIP_FILENAME):
        os.remove(ZIP_FILENAME)
    if os.path.exists(CSV_FILENAME):
        os.remove(CSV_FILENAME)
    
    print("Done! Data is ready for the API.")

if __name__ == "__main__":
    main()
