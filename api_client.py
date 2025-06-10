import requests
import logging

class ApiClient:
    BASE_URL = "https://api.parkendd.de"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_cities(self):
        self.logger.debug("Fetching list of cities from Parkendd API")
        resp = requests.get(self.BASE_URL)
        resp.raise_for_status()
        return resp.json().get("cities", {})

    def get_city_lots(self, city_key):
        self.logger.debug(f"Fetching lots for city: {city_key}")
        resp = requests.get(f"{self.BASE_URL}/{city_key}")
        resp.raise_for_status()
        return resp.json().get("lots", [])
