import os
import requests
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configure logging to write messages to app.log
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def download_images(url, path):
    try:
        # Fetch HTML content of the URL
        response = requests.get(url)
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

        # Download images
        for img_url in image_urls:
            filename = os.path.join(path, os.path.basename(img_url))
            if not os.path.exists(filename):
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                logger.info(f"Downloaded: {filename}")
            else:
                logger.info(f"Skipped already downloaded: {filename}")

    except Exception as e:
        logger.error(f"Error processing URL {url}: {str(e)}")

def main():
    urls_file = 'urls.txt'
    path_file = 'path.txt'

    # Read URLs from urls.txt
    with open(urls_file, 'r') as f:
        urls = f.read().splitlines()

    # Read download path from path.txt
    with open(path_file, 'r') as f:
        download_path = f.read().strip()

    for url in urls:
        download_images(url, download_path)

    while True:
        # Recheck URLs every hour
        time.sleep(3600)
        for url in urls:
            download_images(url, download_path)

if __name__ == "__main__":
    main()
