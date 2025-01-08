import os
import pytest

from src.pipeline.lg_pipeline import run_pipeline_on_pdf
from src.pdf_utils.extract import extract_text_from_pdf

def test_pipeline_on_pdf():
    """
    Basic integration test: ensures the pipeline runs on a real PDF
    and returns the keys we expect in the final dictionary.
    """
    pdf_path = "../papers/paper1.pdf"
    assert os.path.isfile(pdf_path), f"Test PDF not found at {pdf_path}"

    result = run_pipeline_on_pdf(pdf_path, extract_text_from_pdf)

    expected_keys = [
        "title",
        "authors",
        "publication_date",
        "methodology_findings",
        "global_summary",
        "keywords",
    ]
    for key in expected_keys:
        assert key in result, f"Missing '{key}' in pipeline result"

    assert len(result["global_summary"]) > 0, "Global summary is empty"
    assert len(result["keywords"]) > 0, "No keywords extracted"

    print("\nTest pipeline_on_pdf passed! Final result:\n", result)
