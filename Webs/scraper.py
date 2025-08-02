import requests
from cloudscraper import create_scraper
from asyncio import to_thread
from loguru import logger


class Scraper:
    def __init__(self):
        self.scraper = create_scraper()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        }

    async def get(self, url, rjson=None, cs=None, *args, **kwargs):
        try:
            if cs:
                response = await to_thread(
                    self.scraper.get, url, headers=self.headers, *args, **kwargs
                )
            else:
                response = await to_thread(
                    requests.get, url, headers=self.headers, *args, **kwargs
                )
            
            if response.status_code == 403:
                logger.error(f"403 Forbidden: {url}")
                return None

            response.raise_for_status()

            return response.json() if rjson else response.text

        except requests.RequestException as e:
            logger.error(f"GET request failed: {e} -> {url}")
            return None

    async def post(self, url, rjson=None, cs=None, *args, **kwargs):
        try:
            if cs:
                response = await to_thread(
                    self.scraper.post, url, headers=self.headers, *args, **kwargs
                )
            else:
                response = await to_thread(
                    requests.post, url, headers=self.headers, *args, **kwargs
                )

            if response.status_code == 403:
                logger.error(f"403 Forbidden (POST): {url}")
                return None

            response.raise_for_status()

            return response.json() if rjson else response.text

        except requests.RequestException as e:
            logger.error(f"POST request failed: {e} -> {url}")
            return None
    
    
    
#──────────────────────
#────────ᴊᴇғғʏ ᴅᴇᴠ─────────
#──────────────────────
  
