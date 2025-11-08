import re
from datetime import datetime
from dateutil import parser
import phonenumbers
from rapidfuzz import process

CANONICAL_REGIONS = {
    "dach": ["germany", "austria", "switzerland", "dach"],
    "uki": ["uk", "united kingdom", "ireland", "london"],
    "emea": ["europe", "middle east", "africa", "emea"],
    "north america": ["usa", "us", "canada", "na", "north america"],
}

CANONICAL_INDUSTRIES = [
    "saas", "fintech", "ecommerce", "healthcare",
    "manufacturing", "telecom", "energy", "education", "government", "other"
]

def normalize_budget(budget_str: str):
    """Extract numeric amount and convert to euros (rough)."""
    if not budget_str:
        return None
    s = budget_str.lower().strip()
    if any(x in s for x in ["tbd", "unknown"]):
        return None

    match = re.findall(r"[\d,.]+", s)
    if not match:
        return None
    amount = float(match[0].replace(",", "").replace("k", "000"))

    # currency handling
    if "€" in s or "eur" in s:
        rate = 1
    elif "$" in s or "usd" in s:
        rate = 0.92
    elif "£" in s or "gbp" in s:
        rate = 1.15
    else:
        rate = 1
    return round(amount * rate, 2)

def normalize_date(date_str: str):
    """Parse date string to ISO format."""
    if not date_str:
        return None
    try:
        dt = parser.parse(date_str, dayfirst=True)
        return dt.isoformat()
    except Exception:
        return None

def normalize_phone(phone_str: str, default_region="NL"):
    """Normalize phone number to E.164 format."""
    if not phone_str:
        return None
    try:
        p = phonenumbers.parse(phone_str, default_region)
        if phonenumbers.is_valid_number(p):
            return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        pass
    return None

def canonical_region(region_raw: str):
    """Map raw region to canonical region."""
    if not region_raw:
        return None
    text = region_raw.lower()
    for canon, variants in CANONICAL_REGIONS.items():
        if any(v in text for v in variants):
            return canon
    return "other"

def canonical_industry(industry_raw: str):
    """Map raw industry to canonical using fuzzy matching."""
    if not industry_raw:
        return None
    match, score, _ = process.extractOne(industry_raw.lower(), CANONICAL_INDUSTRIES)
    return match if score > 80 else "other"

def clean_lead(lead: dict):
    """Return normalized fields merged onto the raw lead."""
    cleaned = lead.copy()
    cleaned["email"] = lead["email"].strip().lower()
    cleaned["rough_budget_normalized_euro"] = normalize_budget(lead.get("rough_budget_raw"))
    cleaned["first_contacted_at"] = normalize_date(lead.get("first_contacted_raw"))
    cleaned["phone"] = normalize_phone(lead.get("phone"))
    cleaned["region"] = canonical_region(lead.get("region"))
    cleaned["industry_raw"] = canonical_industry(lead.get("industry_raw"))
    return cleaned
