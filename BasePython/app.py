import os
import sys
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Custom headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def download_images(url, path):
    page_number = 1  # Starting page number
    while True:
        try:
            # Construct the URL with the page number
            page_url = f"{url}&page={page_number}"

            # Fetch HTML content of the URL with custom headers
            response = requests.get(page_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract image URLs
            image_urls = []
            for img_tag in soup.find_all('img', src=True):
                img_url = urljoin(url, img_tag['src'])
                if img_url.startswith('https://static1.e621.net/data/preview/'):
                    # Replace 'preview' with 'sample' in the URL
                    img_url = img_url.replace('/preview/', '/sample/')
                    image_urls.append(img_url)

            if not image_urls:
                print(f"No eligible images found on {page_url}")
                break  # No more images on this page

            # Download images
            for img_url in image_urls:
                filename = os.path.join(path, os.path.basename(img_url))
                if not os.path.exists(filename):
                    img_response = requests.get(img_url, headers=headers)
                    img_response.raise_for_status()
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Skipped already downloaded: {filename}")

            # Move to the next page
            page_number += 1

        except Exception as e:
            print(f"Error processing URL {page_url}: {str(e)}")
            break

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Detect urls.txt and path.txt in the script directory
    urls_file = os.path.join(script_dir, 'urls.txt')
    path_file = os.path.join(script_dir, 'path.txt')

    if not (os.path.exists(urls_file) and os.path.exists(path_file)):
        print("Error: urls.txt or path.txt not found in the script directory.")
        sys.exit(1)

    print("Starting e621 downloader...")

    # Read URLs from urls.txt
    with open(urls_file, 'r') as f:
        urls = f.read().splitlines()

    # Read download path from path.txt
    with open(path_file, 'r') as f:
        download_path = f.read().strip()

    print(f"Downloading to: {download_path}")

    for url in urls:
        print(f"Processing URL: {url}")
        download_images(url, download_path)

    print("Initial download completed. Monitoring for changes...")

    while True:
        # Recheck URLs every hour
        time.sleep(3600)
        print("Checking for updates...")
        for url in urls:
            print(f"Processing URL: {url}")
            download_images(url, download_path)

if __name__ == "__main__":
    main()
