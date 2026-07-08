from app.retrieval.retriever import _contains_restricted_term


def test_restricted_terms_detect_ceo_query():
    assert _contains_restricted_term("What is the CEO policy?") is True


def test_normal_policy_query_is_not_restricted():
    assert _contains_restricted_term("What is the sick leave policy?") is False
