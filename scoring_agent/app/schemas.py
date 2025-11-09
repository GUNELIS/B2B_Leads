from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class LeadIn(BaseModel):
    """Schema for incoming lead data."""
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    region: Optional[str] = None  # e.g., "DACH", "EMEA"
    interest_area: Optional[str] = None
    budget_normalized_euro: Optional[float] = None
    first_contacted_at: Optional[datetime] = None
    source: Optional[str] = None
    consent_given: Optional[bool] = None
    status: Optional[str] = None


class LeadBatchIn(BaseModel):
    leads: List[LeadIn]


class ScoreRequest(BaseModel):
    leads: List[LeadIn]


class ScoredLead(BaseModel):
    id: Optional[int]
    score: float


class ScoreResponse(BaseModel):
    results: List[ScoredLead]


class TrainResponse(BaseModel):
    trained: bool
    n_samples: int


class EvaluateResponse(BaseModel):
    metrics: dict


class HealthResponse(BaseModel):
    status: str
    ingested_count: int
    model_ready: bool


class CompanyIn(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    industry: Optional[str] = None
    region: Optional[str] = None
    typical_project_budget_euro: Optional[float] = None
    tech_stack: Optional[List[str]] = None
    notes: Optional[str] = None


class LeadCompanyPair(BaseModel):
    lead: LeadIn
    company: CompanyIn
    compatibility_score: Optional[float] = None
