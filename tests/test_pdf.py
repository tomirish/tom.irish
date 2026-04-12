import os
import pytest
from pypdf import PdfReader

PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'resume.pdf')


@pytest.mark.skipif(
    not os.path.exists(PDF_PATH),
    reason="resume.pdf not found (generated in CI only)"
)
def test_pdf_is_one_page():
    reader = PdfReader(PDF_PATH)
    assert len(reader.pages) == 1, f"Expected 1 page, got {len(reader.pages)}"
