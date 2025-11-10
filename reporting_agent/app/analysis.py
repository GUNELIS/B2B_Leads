"""Basic analytics over LeadCompanyMatch data.

Provides small, transparent computations suitable for quick reporting.
"""

from typing import Any, Dict

import pandas as pd


def compute_basic_stats(matches_json: Any) -> Dict[str, Any]:
    """Compute simple trend metrics from match records.

    Expected input is either a list of match dicts or a paginated dict
    with a 'results' field. The function is defensive and will handle both.

    Args:
        matches_json: Raw JSON returned by the Django API.

    Returns:
        A dictionary of metrics, e.g.:
            {
              "count": 50,
              "score": {"mean": 0.71, "p90": 0.92, "max": 0.98},
              "top_industries": [{"industry":"saas","count":12}, ...],
              "top_regions": [{"region":"dach","count":9}, ...],
              "budget_bands": [{"band":"€0-5k","count":7}, ...]
            }
        Placeholder for now. Real logic will be added next.
    """
    # Placeholder implementation to keep the interface stable.
    return {}
