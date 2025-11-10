"""Reporting Agent FastAPI application.

Exposes health and report-generation endpoints.
The report endpoint will fetch matches, compute simple trends, and
produce a short text summary via a lightweight LLM.
"""

from fastapi import FastAPI
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
    return ReportResponse(
        summary="Reporting Agent skeleton is live. Analysis and LLM summary pending.",
        stats={},
    )
