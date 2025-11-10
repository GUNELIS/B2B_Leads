import random

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .model import model
from .storage import store


def _encode_pair(lead, company):
    """
    Convert a (lead, company) pair into a numeric feature vector.

    Features:
      [0] lead budget (float)
      [1] company typical project budget (float)
      [2] region match flag (1.0 if equal else 0.0)
      [3] industry match flag (1.0 if equal else 0.0)

    Args:
        lead: Pydantic LeadIn with normalized fields (industry, region, budget_normalized_euro).
        company: Pydantic CompanyIn with normalized fields (industry, region, typical_project_budget_euro).

    Returns:
        list[float]: Fixed-length feature vector for the pair.
    """
    # Simple numeric vectorization
    budget_lead = lead.budget_normalized_euro or 0
    budget_company = company.typical_project_budget_euro or 0
    region_match = (
        1.0
        if (
            lead.region
            and company.region
            and lead.region.lower() == company.region.lower()
        )
        else 0.0
    )
    industry_match = (
        1.0
        if (
            lead.industry
            and company.industry
            and lead.industry.lower() == company.industry.lower()
        )
        else 0.0
    )
    return [budget_lead, budget_company, region_match, industry_match]


def train_model():
    """
    Train the logistic regression match model.

    Process:
      1) Read all ingested leads and companies from the in-memory store.
      2) For each lead, sample up to 3 companies and build feature vectors via _encode_pair.
      3) Create a probabilistic label from simple heuristics:
           - region match, industry match, and budget similarity,
         then add controlled randomness to avoid degenerate labels.
      4) Ensure both classes exist, split into train/test, fit the model, and compute accuracy.

    Returns:
        dict: {
          "trained": bool,            # True if model trained
          "n_samples": int,           # number of training samples used
          "metrics": {"accuracy": float}  # test accuracy (0..1)
        }
        If no data is available: {"trained": False, "n_samples": 0, "metrics": {}}
    """
    leads = store.leads()
    companies = store.companies()
    if not leads or not companies:
        return {"trained": False, "n_samples": 0, "metrics": {}}

    X, y = [], []
    for lead in leads:
        for company in random.sample(companies, min(len(companies), 3)):
            X.append(_encode_pair(lead, company))

            # heuristic label with slight randomness for diversity
            region_match = (
                lead.region
                and company.region
                and lead.region.lower() == company.region.lower()
            )
            industry_match = (
                lead.industry
                and company.industry
                and lead.industry.lower() == company.industry.lower()
            )

            # compute normalized budget difference
            lead_budget = lead.budget_normalized_euro or 0
            comp_budget = company.typical_project_budget_euro or 0
            budget_diff_ratio = 1 - abs(lead_budget - comp_budget) / (
                comp_budget + 1e-6
            )
            budget_score = max(0, min(1, budget_diff_ratio))

            # weighted heuristic score
            heuristic = (
                0.4 * int(region_match) + 0.4 * int(industry_match) + 0.2 * budget_score
            )

            # add controlled randomness so not all are identical
            if random.random() < heuristic:
                y.append(1)
            else:
                y.append(0)

    X, y = np.array(X), np.array(y)
    if len(np.unique(y)) < 2:
        y[random.randrange(len(y))] = (
            1 - y[random.randrange(len(y))]
        )  # ensure both classes

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.train(X_train, y_train)
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    acc = accuracy_score(y_test, y_pred)

    return {
        "trained": True,
        "n_samples": len(X_train),
        "metrics": {"accuracy": float(acc)},
    }
