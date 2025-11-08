import asyncio

from app.rest_client import fetch_raw_leads
from fastapi import FastAPI
from app.cleaner import clean_lead

app = FastAPI(title="Cleaning Agent", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.api_route("/clean-leads", methods=["GET", "POST"])
async def clean_leads():
    leads = await fetch_raw_leads(limit=5)  # Fetch a small sample for demonstration
    cleaned = [clean_lead(l) for l in leads]  # Clean the leads
    return {"fetched": len(leads), "cleaned_sample": cleaned[:2]}  # Return a sample of cleaned leads
