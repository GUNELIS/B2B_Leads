import pytest
from app.cleaner import (
    canonical_industry,
    canonical_region,
    clean_lead,
    normalize_budget,
    normalize_date,
    normalize_phone,
)


def test_normalize_budget_basic():
    assert normalize_budget("€24000") == 24000
    assert normalize_budget("24,000 eur") == 24000
    assert normalize_budget("$25k") == pytest.approx(23000, rel=0.1)
    assert normalize_budget("unknown") is None


def test_normalize_date_formats():
    assert normalize_date("2025-07-14").startswith("2025-07-14")
    assert normalize_date("14-07-2025").startswith("2025-07-14")
    assert normalize_date("Jul 14 2025").startswith("2025-07-14")
    assert normalize_date(None) is None


def test_normalize_phone():
    p = normalize_phone("+31 6 12 34 56 78")
    assert p.startswith("+31")
    assert normalize_phone("invalid-number") is None


def test_canonical_region_and_industry():
    assert canonical_region("Germany") == "dach"
    assert canonical_region("Tokyo") == "other"
    assert canonical_industry("finteh") == "fintech"


def test_clean_lead_integration():
    raw = {
        "email": "EXAMPLE@TEST.COM",
        "rough_budget_raw": "$10k",
        "first_contacted_raw": "2025/01/01",
        "phone": "+1-555-234-9876",
        "region": "United Kingdom",
        "industry_raw": "saas",
    }
    cleaned = clean_lead(raw)
    assert cleaned["email"] == "example@test.com"
    assert cleaned["region"] == "uki"
    assert cleaned["rough_budget_normalized_euro"] > 0
