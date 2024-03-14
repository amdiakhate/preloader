import os
import requests
import schedule
import time
import logging
from dotenv import load_dotenv
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load environment from .env file
load_dotenv()

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Configuration
API_URL = os.getenv('API_URL', 'http://example.com/api/urls')
API_CUSTOM_HEADERS = os.getenv('API_CUSTOM_HEADERS', '')
FRONTEND_CUSTOM_HEADERS = os.getenv('FRONTEND_CUSTOM_HEADERS', '')
PRELOAD_INTERVAL = int(os.getenv('PRELOAD_INTERVAL', 15))
DISABLE_TQDM = os.getenv('DISABLE_TQDM', 'False').lower() in ('true', '1', 't')

# Default headers
DEFAULT_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'PreloadBot/1.0'
}

# Requests session with retry strategy
RETRY_STRATEGY = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"],
    backoff_factor=1
)
session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=RETRY_STRATEGY))
session.mount("https://", HTTPAdapter(max_retries=RETRY_STRATEGY))

def parse_custom_headers(headers_string):
    """Parse custom headers from a formatted string into a dictionary."""
    headers = {}
    if headers_string:
        for header in headers_string.split(','):
            if header.strip():
                try:
                    key, value = header.split('=')
                    headers[key.strip()] = value.strip()
                except ValueError:
                    logger.error(f"Invalid header format: {header}")
    return headers

def fetch_urls(api_url):
    """Fetch URLs from the API using API-specific custom headers."""
    api_headers = {**DEFAULT_HEADERS, **parse_custom_headers(API_CUSTOM_HEADERS)}
    urls = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        try:
            response = session.get(f"{api_url}&page={page}", headers=api_headers)
            response.raise_for_status()
            data = response.json()
            total_pages = data.get("total_pages", 1)
            urls.extend(item["url"] for item in data.get("items", []))
            page += 1
        except requests.RequestException as e:
            logger.error(f"Failed to fetch URLs: {e}")
            break
    return urls

def preload_urls(urls):
    """Preload each URL with frontend-specific custom headers."""
    frontend_headers = {**DEFAULT_HEADERS, **parse_custom_headers(FRONTEND_CUSTOM_HEADERS)}
    progress_bar = tqdm(urls, desc="Preloading URLs", disable=DISABLE_TQDM)
    for url in progress_bar:
        try:
            session.get(url, headers=frontend_headers)
        except requests.RequestException as e:
            logger.error(f"Error preloading {url}: {e}")

def start_preloading():
    logger.info("Starting preload script...")
    urls = fetch_urls(API_URL)
    preload_urls(urls)
    schedule.every(PRELOAD_INTERVAL).minutes.do(lambda: preload_urls(fetch_urls(API_URL)))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_preloading()
