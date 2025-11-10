"""Reporting Agent FastAPI application."""

import os

from app.analysis import compute_basic_stats
from app.client import get_top_matches
from app.summarizer import summarize
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Reporting Agent",
    version="0.1.0",
    description="Generates human-readable reports from LeadCompanyMatch data.",
)


class ReportResponse(BaseModel):
    """Response model for the /generate-report endpoint.

    Attributes:
        summary: LLM-generated textual summary of trends.
        stats: Dictionary of computed metrics for transparency and testing.
    """

    summary: str
    stats: dict


@app.get("/health")
def health() -> dict:
    """Liveness endpoint.

    Returns:
        A constant status payload to signal the service is up.
    """
    return {"status": "ok"}


@app.get("/generate-report", response_model=ReportResponse)
def generate_report() -> ReportResponse:
    """Generate a placeholder report.

        This stub will be replaced to:
        1) fetch top matches from Django,
        2) compute trends,
        3) summarize via a tiny LLM.

        Returns:
            ReportResponse with a placeholder summary and empty stats.
    """    
    try:
        limit = int(os.getenv("REPORT_TOP_N", "50"))
        matches = get_top_matches(limit=limit)
        stats = compute_basic_stats(matches)
        summary = summarize(stats)
        return ReportResponse(summary=summary, stats=stats)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
