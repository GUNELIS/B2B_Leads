import asyncio

from app.cleaner import clean_lead
from app.rest_client import fetch_raw_leads, post_cleaned_leads
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Cleaning Agent", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.api_route("/clean-leads", methods=["GET", "POST"])
async def clean_leads(limit: int = 100):
    """Fetch raw leads, clean them, and post the cleaned leads."""
    try:
        leads = await fetch_raw_leads(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    cleaned = [clean_lead(l) for l in leads]
    await post_cleaned_leads(cleaned)

    return {
        "fetched": len(leads),
        "cleaned": len(cleaned),
        "posted": len(cleaned),
    }
