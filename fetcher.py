# fetcher.py - Network Layer
# Responsible for all HTTP communication. Returns raw text.

import time
import requests

class FetchError(Exception):
    """Custom exception raised on permanent web request failures."""
    pass

def fetch_feed(url):
    """
    Performs an HTTP GET request with customized User-Agent headers
    and exponential backoff retry.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThreatScoutScraper/1.0 (Ethical Threat Research)"
    }
    
    timeout = 10
    retries = 3
    backoff = 2
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response.text
            else:
                print(f"[!] Warning: Received status code {response.status_code} for {url}. Retrying...")
        except requests.RequestException as e:
            print(f"[!] Request Exception: {e}. Retrying in {backoff} seconds...")
            
        time.sleep(backoff)
        backoff *= 2
        
    raise FetchError(f"Failed to fetch content from {url} after {retries} attempts.")
