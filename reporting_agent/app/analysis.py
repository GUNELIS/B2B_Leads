"""Basic analytics over LeadCompanyMatch data."""

from typing import Any, Dict, List

import pandas as pd


def _extract_results(matches_json: Any) -> List[dict]:
    if isinstance(matches_json, dict) and "results" in matches_json:
        return matches_json["results"]
    if isinstance(matches_json, list):
        return matches_json
    return []


def _first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first column name from candidates that exists in df."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def compute_basic_stats(matches_json: Any) -> Dict[str, Any]:
    """Compute numeric and categorical trends from reporting payload."""
    data = _extract_results(matches_json)
    if not data:
        return {"count": 0}

    df = pd.DataFrame(data)
    print("DEBUG columns:", list(df.columns), flush=True)

    out: Dict[str, Any] = {"count": len(df)}

    # --- numeric score ---
    score_field = _first_existing(df, ["score", "compatibility_score"])
    if score_field:
        df["score"] = pd.to_numeric(df[score_field], errors="coerce")
        out["score"] = {
            "mean": round(df["score"].mean(), 3),
            "median": round(df["score"].median(), 3),
            "p90": round(df["score"].quantile(0.9), 3),
            "max": round(df["score"].max(), 3),
        }

    # --- categorical fields (lead or company variants) ---
    industry_field = _first_existing(df, ["company_industry", "lead_industry"])
    region_field = _first_existing(df, ["company_region", "lead_region"])
    budget_field = _first_existing(
        df, ["company_budget_normalized_euro", "lead_budget_normalized_euro"]
    )

    for name, field in [
        ("industry", industry_field),
        ("region", region_field),
        ("budget_normalized_euro", budget_field),
    ]:
        if field and field in df:
            vc = (
                df[field]
                .dropna()
                .astype(str)
                .str.strip()
                .value_counts()
                .head(5)
                .reset_index()
            )
            vc.columns = [name, "count"]
            freq = vc.to_dict(orient="records")
            out[f"top_{name}s"] = freq

    return out
