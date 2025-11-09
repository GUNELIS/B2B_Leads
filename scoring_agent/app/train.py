import random

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .model import model
from .storage import store


def _encode_pair(lead, company):
    """Convert a lead-company pair into a feature vector.
    For simplicity, we use a very basic encoding based on budget and categorical matches.
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
    """Train the compatibility scoring model using stored leads and companies.
    We score highly if the lead and company share region and industry for this example.
    Returns training summary including accuracy metric.
    """
    leads = store.leads()
    companies = store.companies()
    if not leads or not companies:
        return {"trained": False, "n_samples": 0, "metrics": {}}

    X, y = [], []
    for lead in leads:
        for company in random.sample(companies, min(len(companies), 3)):
            X.append(_encode_pair(lead, company))
            # fake label: good fit if region and industry match
            good = (
                lead.region
                and company.region
                and lead.region.lower() == company.region.lower()
            ) and (
                lead.industry
                and company.industry
                and lead.industry.lower() == company.industry.lower()
            )
            y.append(1 if good else 0)

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
