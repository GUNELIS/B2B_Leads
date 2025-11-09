import os
from typing import List

import httpx
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .model import model
from .schemas import (
    CompanyIn,
    EvaluateResponse,
    HealthResponse,
    LeadBatchIn,
    ScoredLead,
    ScoreRequest,
    ScoreResponse,
    TrainResponse,
)
from .storage import store
from .train import _encode_pair  # reuse vectorization
from .train import train_model

MATCHES_POST_URL = os.getenv("MATCHES_POST_URL")
MATCHES_API_KEY = os.getenv("MATCHES_API_KEY")

app = FastAPI(title="Scoring Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    # model readiness will be wired after training is implemented
    return HealthResponse(status="ok", ingested_count=store.count(), model_ready=False)


@app.post("/ingest-cleaned-leads")
def ingest_cleaned_leads(payload: LeadBatchIn):
    if not payload.leads:
        raise HTTPException(status_code=400, detail="No leads provided")
    added = store.add_many_leads(payload.leads)
    return {"ingested": added, "total": store.count()}


@app.post("/train", response_model=TrainResponse)
def train():
    result = train_model()
    if not result["trained"]:
        raise HTTPException(status_code=400, detail="No data to train on")
    return TrainResponse(trained=True, n_samples=result["n_samples"])


@app.get("/evaluate", response_model=EvaluateResponse)
def evaluate():
    if not model.trained:
        return EvaluateResponse(metrics={"status": "model_not_trained"})
    return EvaluateResponse(metrics={"status": "ok"})


@app.post("/score")
def score(req: ScoreRequest):

    if not model.trained:
        raise HTTPException(status_code=400, detail="Model not trained")

    leads = req.leads
    companies = store.companies()
    if not leads or not companies:
        raise HTTPException(status_code=400, detail="Need both leads and companies")

    results = []
    for lead in leads:
        lead_scores = []
        for company in companies:
            X = [_encode_pair(lead, company)]
            prob = float(model.predict(X)[0])
            lead_scores.append(
                {
                    "company_id": company.id,
                    "company_name": company.name,
                    "score": round(prob, 3),
                }
            )
        # sort descending so best matches first
        lead_scores.sort(key=lambda x: x["score"], reverse=True)
        results.append({"lead_id": lead.id, "scores": lead_scores})

    return {"results": results}


@app.post("/ingest-companies")
def ingest_companies(payload: List[CompanyIn]):
    if not payload:
        raise HTTPException(status_code=400, detail="No companies provided")
    added = store.add_many_companies(payload)
    return {"ingested": added}


def _flatten_results(results):
    rows = []
    for item in results:
        lead_id = item.get("lead_id")
        for sc in item.get("scores", []):
            rows.append(
                {
                    "lead_id": lead_id,
                    "company_id": sc.get("company_id"),
                    "compatibility_score": sc.get("score"),
                }
            )
    return rows


@app.post("/forward-scored-leads")
def forward_scored_leads(payload: dict = Body(...)):
    """
    Forward scoring results to Django to persist LeadCompanyMatch.
    Expected payload shape is the output of /score:
      {"results":[{"lead_id":..., "scores":[{"company_id":...,"score":...}, ...]}, ...]}
    """
    if not MATCHES_POST_URL:
        raise HTTPException(status_code=500, detail="MATCHES_POST_URL not configured")

    rows = _flatten_results(payload.get("results", []))
    if not rows:
        raise HTTPException(status_code=400, detail="No rows to forward")

    headers = {"Content-Type": "application/json"}
    if MATCHES_API_KEY:
        headers["X-API-Key"] = MATCHES_API_KEY

    r = httpx.post(
        MATCHES_POST_URL, json={"matches": rows}, headers=headers, timeout=15.0
    )
    return {
        "forwarded": len(rows),
        "django_status": r.status_code,
        "django_body": (
            r.json()
            if r.headers.get("content-type", "").startswith("application/json")
            else r.text
        ),
    }
