import os

import httpx

DJANGO_BASE = os.getenv("DJANGO_API_BASE", "http://django:8000")
TIMEOUT = 10.0


async def fetch_raw_leads(limit: int = 100):
    """GET raw leads from Django."""
    url = f"{DJANGO_BASE}/api/leads/to-clean/?limit={limit}"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


async def post_cleaned_leads(cleaned: list):
    """Stub: will later POST to second agent."""
    # url = os.getenv("SECOND_AGENT_URL")
    # async with httpx.AsyncClient(timeout=TIMEOUT) as client:
    #     await client.post(url, json=cleaned)
    print(f"[DEBUG] Would post {len(cleaned)} cleaned leads")
