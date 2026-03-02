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

    def fail_if_marker_called() -> Any:
        raise AssertionError("marker converter should not be used for text-layer PDF")

    text_pdf = _build_pdf_bytes(text="Readable text layer. " * 80)

    monkeypatch.setattr(extract, "_get_pymupdf4llm_module", lambda: FakePyMuPDF4LLM())
    monkeypatch.setattr(extract, "_get_marker_pdf_converter", fail_if_marker_called)

    extracted = extract.extract_pdf_text(text_pdf)

    assert extracted == "fast markdown from pymupdf4llm"


def test_extract_pdf_text_falls_back_to_marker_for_blank_pdf_pages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRendered:
        markdown = "ocr result from marker"

    class FakeMarkerConverter:
        def __call__(self, _path: str) -> Any:
            return FakeRendered()

    blank_pdf = _build_pdf_bytes(text=None)

    def fail_if_pymupdf4llm_called(_pdf_bytes: bytes) -> str | None:
        raise AssertionError("pymupdf4llm path should be skipped for blank PDF")

    monkeypatch.setattr(
        extract,
        "_extract_pdf_text_with_pymupdf4llm",
        fail_if_pymupdf4llm_called,
    )
    monkeypatch.setattr(
        extract, "_get_marker_pdf_converter", lambda: FakeMarkerConverter()
    )

    extracted = extract.extract_pdf_text(blank_pdf)

    assert extracted == "ocr result from marker"
