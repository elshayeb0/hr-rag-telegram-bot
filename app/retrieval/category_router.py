CATEGORY_TERMS = {
    "absence": {"sick", "sickness", "absence", "illness", "medical"},
    "leave": {"leave", "maternity", "paternity", "parental"},
    "technology": {"byod", "device", "email", "internet", "social media", "communications"},
    "conduct": {"harassment", "bullying", "alcohol", "drugs", "conduct"},
    "expenses": {"expense", "expenses", "travel", "reimbursement"},
    "data_protection": {"gdpr", "data protection", "privacy", "personal data"},
    "disciplinary": {"disciplinary", "misconduct", "warning"},
    "grievance": {"grievance", "complaint"},
    "employment_terms": {"notice", "notice period", "termination"},
}


def infer_policy_category(query: str) -> str | None:
    normalized = query.lower()

    for category, terms in CATEGORY_TERMS.items():
        if any(term in normalized for term in terms):
            return category

    return None
