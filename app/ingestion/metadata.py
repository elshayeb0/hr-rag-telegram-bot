from pathlib import Path
from typing import Any

from app.config.constants import DEFAULT_ACCESS_LEVEL


POLICY_KEYWORDS = {
    "leave": "leave",
    "maternity": "leave",
    "paternity": "leave",
    "parental": "leave",
    "sickness": "absence",
    "absence": "absence",
    "disciplinary": "disciplinary",
    "grievance": "grievance",
    "harassment": "conduct",
    "bullying": "conduct",
    "alcohol": "conduct",
    "drugs": "conduct",
    "expenses": "expenses",
    "data-protection": "data_protection",
    "gdpr": "data_protection",
    "byod": "technology",
    "communications": "technology",
    "email": "technology",
    "social-media": "technology",
    "contract": "contract",
    "offer-letter": "contract",
    "new-starter": "onboarding",
    "probationary": "probation",
    "notice-periods": "employment_terms",
}


def normalize_title(file_path: Path) -> str:
    title = file_path.stem
    title = title.replace("-", " ").replace("_", " ")
    title = " ".join(title.split())
    return title.title()


def infer_document_type(file_path: Path) -> str:
    name = file_path.stem.lower()

    if "policy" in name:
        return "policy"

    if "contract" in name:
        return "contract"

    if "letter" in name:
        return "letter"

    if "form" in name:
        return "form"

    if "procedure" in name:
        return "procedure"

    return "document"


def infer_policy_category(file_path: Path) -> str | None:
    name = file_path.stem.lower()

    for keyword, category in POLICY_KEYWORDS.items():
        if keyword in name:
            return category

    return None


def build_document_metadata(file_path: Path) -> dict[str, Any]:
    return {
        "document_id": file_path.stem.lower().replace(" ", "_"),
        "document_title": normalize_title(file_path),
        "document_type": infer_document_type(file_path),
        "policy_category": infer_policy_category(file_path),
        "access_level": DEFAULT_ACCESS_LEVEL,
        "source": file_path.name,
    }
