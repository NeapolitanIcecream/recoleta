from __future__ import annotations

from typing import Any

import pytest

import recoleta.extract as extract


def _build_pdf_bytes(*, text: str | None) -> bytes:
    try:
        import pymupdf  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover
        import fitz as pymupdf  # type: ignore[import-not-found]

    doc = pymupdf.open()
    try:
        page = doc.new_page()
        if isinstance(text, str) and text.strip():
            page.insert_textbox(
                pymupdf.Rect(72, 72, 540, 780),
                text,
                fontsize=11,
            )
        return doc.tobytes()
    finally:
        doc.close()


def test_extract_pdf_text_prefers_pymupdf4llm_for_text_layer_pdf(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakePyMuPDF4LLM:
        @staticmethod
        def to_markdown(_doc: Any) -> str:
            return "fast markdown from pymupdf4llm"

    text_pdf = _build_pdf_bytes(text="Readable text layer. " * 80)

    monkeypatch.setattr(extract, "_get_pymupdf4llm_module", lambda: FakePyMuPDF4LLM())

    extracted = extract.extract_pdf_text(text_pdf)

    assert extracted == "fast markdown from pymupdf4llm"


def test_extract_pdf_text_returns_none_for_blank_pdf_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakePyMuPDF4LLM:
        @staticmethod
        def to_markdown(_doc: Any) -> str:
            return ""

    blank_pdf = _build_pdf_bytes(text=None)

    monkeypatch.setattr(extract, "_get_pymupdf4llm_module", lambda: FakePyMuPDF4LLM())

    diag: dict[str, Any] = {}
    extracted = extract.extract_pdf_text(blank_pdf, diag=diag)

    assert extracted is None
    assert diag.get("pdf_backend") == "none"


def test_extract_pdf_text_uses_pymupdf4llm_even_when_text_layer_check_is_inconclusive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: don't treat sparse pages as a reason to fail early."""

    class FakePyMuPDF4LLM:
        @staticmethod
        def to_markdown(_doc: Any) -> str:
            return "markdown from pymupdf4llm despite sparse text"

    sparse_text_pdf = _build_pdf_bytes(text="Short text.\n" * 5)

    monkeypatch.setattr(extract, "_get_pymupdf4llm_module", lambda: FakePyMuPDF4LLM())

    extracted = extract.extract_pdf_text(sparse_text_pdf)

    assert extracted == "markdown from pymupdf4llm despite sparse text"
