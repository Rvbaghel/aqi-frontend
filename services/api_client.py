import requests
import logging
import os

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# ---------------- BASE URL (LOCAL + CLOUD SAFE) ----------------
BASE_URL = os.getenv("BACKEND_BASE_URL", "https://skyguard-app.onrender.com")

# ---------------- SESSION (PERFORMANCE) ----------------
session = requests.Session()


def check_backend_health():
    try:
        response = session.get(f"{BASE_URL}/health/", timeout=5)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        logger.error(f"Health check failed: {e}")
        return None


def get_current_aqi(city="Ahmedabad"):
    try:
        response = session.get(
            f"{BASE_URL}/aqi/current",
            params={"city": city},
            timeout=5
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        logger.error(f"Current AQI fetch failed for {city}: {e}")
        return None


def get_cities():
    """Fetch list of city names."""
    try:
        response = session.get(f"{BASE_URL}/cities", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch cities: {e}")
        return []


def get_last_24_hours_aqi(city):
    """Fetch last 24 hours AQI data for a city."""
    try:
        response = session.get(
            f"{BASE_URL}/aqi/last-24-hours",
            params={"city": city},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"24h history fetch failed for {city}: {e}")
        return []
