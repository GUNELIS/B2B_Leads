import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Reporting Agent", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


class ReportResponse(BaseModel):
    summary: str
    stats: dict


@app.get("/generate-report", response_model=ReportResponse)
def generate_report():
    # Placeholder. Next step will fetch matches, analyze, summarize.
    return ReportResponse(
        summary="Reporting Agent skeleton is live. Analysis and LLM summary pending.",
        stats={},
    )
