import asyncio

from app.rest_client import fetch_raw_leads
from fastapi import FastAPI

app = FastAPI(title="Cleaning Agent", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/clean-leads")
async def clean_leads():
    leads = await fetch_raw_leads(limit=10)
    return {"fetched": len(leads)}
