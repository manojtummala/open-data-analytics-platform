import requests
import time
from typing import Optional

HEADERS = {
    "User-Agent": "OpenDataAnalyticsPlatform/1.0 (contact: manojt0120@gmail.com)"
}

def get_with_retry(url, retries=3, backoff=2, timeout=10):
    last_exc: Optional[Exception] = None

    attempts = max(1, retries)
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            if response.status_code == 200:
                return response
        except requests.RequestException as exc:
            last_exc = exc
        
        if attempt < retries - 1:
            time.sleep(backoff ** attempt)
    
    if last_exc:
        raise last_exc
    
    raise RuntimeError(f"Failed to fetch {url} after {retries} attempts")