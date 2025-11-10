import os

import httpx

DJANGO_BASE_URL = os.getenv("DJANGO_BASE_URL", "http://django:8000")
MATCHES_ENDPOINT = os.getenv("MATCHES_ENDPOINT", "/api/matches/")
TIMEOUT_SECONDS = float(os.getenv("TIMEOUT_SECONDS", "15"))


def get_top_matches(limit: int = 50):
    url = f"{DJANGO_BASE_URL.rstrip('/')}/{MATCHES_ENDPOINT.lstrip('/')}"
    params = {"ordering": "-score", "limit": limit}
    headers = {}
    api_key = os.getenv("DJANGO_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
        r = client.get(url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
