"""HTTP client for Django API access.

Fetches LeadCompanyMatch entries for downstream analysis.
"""

import os

import httpx

DJANGO_BASE_URL = os.getenv("DJANGO_BASE_URL", "http://django:8000")
MATCHES_ENDPOINT = os.getenv("MATCHES_ENDPOINT", "/api/matches/")
TIMEOUT_SECONDS = float(os.getenv("TIMEOUT_SECONDS", "15"))


def get_top_matches(limit: int = 50) -> dict:
    """Fetch top-scoring LeadCompanyMatch entries from Django.

    The Django API is expected to support ordering and limit query params.

    Args:
        limit: Maximum number of matches to return.

    Returns:
        Parsed JSON payload from Django. Shape depends on your DRF serializer,
        typically a list or paginated dict containing match objects with fields
        like: lead, company, score, matched_at, and any normalized attributes.

    Raises:
        httpx.HTTPError: If the request fails or times out.
    """
    url = f"{DJANGO_BASE_URL.rstrip('/')}/{MATCHES_ENDPOINT.lstrip('/')}"
    params = {"ordering": "-score", "limit": limit}
    headers = {}
    api_key = os.getenv("DJANGO_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
        resp = client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp.json()
