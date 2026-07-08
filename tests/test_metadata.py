from pathlib import Path

from app.ingestion.metadata import build_document_metadata


def test_policy_metadata_inference():
    metadata = build_document_metadata(Path("Sickness-And-Absence-Policy.docx"))

    assert metadata["document_type"] == "policy"
    assert metadata["policy_category"] == "absence"
    assert metadata["access_level"] == "employee"
