from typing import List

from fastapi import FastAPI, HTTPException
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


@app.post("/forward-scored-leads")
def forward_scored_leads():
    # stub to be wired to Agent 3 later
    return {"forwarded": 0, "status": "stub"}


@app.post("/ingest-companies")
def ingest_companies(payload: List[CompanyIn]):
    if not payload:
        raise HTTPException(status_code=400, detail="No companies provided")
    added = store.add_many_companies(payload)
    return {"ingested": added}
