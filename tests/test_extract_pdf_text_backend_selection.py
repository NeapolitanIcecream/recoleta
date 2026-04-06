from __future__ import annotations

from typing import Any

import pytest

import recoleta.extract as extract
import recoleta.extract_pdf as extract_pdf


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


def test_extract_pdf_text_does_not_open_doc_when_pymupdf4llm_is_unavailable() -> None:
    class FakeDoc:
        def close(self) -> None:
            raise AssertionError(
                "doc.close should not be needed when doc was never opened"
            )

    class FakePyMuPDF:
        open_called = False

        @classmethod
        def open(cls, *, stream: bytes, filetype: str) -> FakeDoc:
            assert stream == b"%PDF-test"
            assert filetype == "pdf"
            cls.open_called = True
            return FakeDoc()

    diag: dict[str, Any] = {}

    extracted = extract_pdf.extract_pdf_text_impl(
        request=extract_pdf.PdfTextExtractionRequest(
            pdf_bytes=b"%PDF-test",
            diag=diag,
            get_pymupdf_module=lambda: FakePyMuPDF,
            get_pymupdf4llm_module=lambda: None,
            pdf_has_text_layer=lambda _doc: True,
            extract_with_pymupdf4llm=lambda *_args, **_kwargs: "unused",
            markdown_looks_useful=lambda markdown: bool(markdown),
        )
    )

    assert extracted is None
    assert diag.get("pdf_backend") == "none"
    assert FakePyMuPDF.open_called is False
