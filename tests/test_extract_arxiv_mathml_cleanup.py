from __future__ import annotations

from types import SimpleNamespace

import pytest

from recoleta.extract import extract_html_document_cleaned_with_references
import recoleta.extract as extract


def test_extract_html_document_preserves_mathml_namespace_and_tex_annotation() -> None:
    """Regression: arXiv MathML must keep namespace + TeX annotation attributes."""

    html = (
        "<html><body><main>"
        "<h1>Test</h1>"
        "<p>Intro</p>"
        '<math xmlns="http://www.w3.org/1998/Math/MathML">'
        "<semantics>"
        "<mrow><mi>a</mi><mo>=</mo><mn>1</mn></mrow>"
        '<annotation encoding="application/x-tex">a=1</annotation>'
        "</semantics>"
        "</math>"
        "<p>Outro</p>"
        "</main></body></html>"
    )

    cleaned, _refs, stats = extract_html_document_cleaned_with_references(html)

    assert cleaned is not None, stats
    assert 'xmlns="http://www.w3.org/1998/Math/MathML"' in cleaned
    assert 'encoding="application/x-tex"' in cleaned


def test_convert_html_document_to_markdown_replaces_mathml_with_tex_annotations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: Pandoc should receive TeX annotations instead of raw arXiv MathML."""

    html = (
        "<html><body><main>"
        "<p>Inline "
        '<math display="inline" xmlns="http://www.w3.org/1998/Math/MathML">'
        "<semantics>"
        "<mrow><mi>a</mi><mo>=</mo><mn>1</mn></mrow>"
        '<annotation encoding="application/x-tex">a=1</annotation>'
        "</semantics>"
        "</math>"
        " block"
        '<math display="block" xmlns="http://www.w3.org/1998/Math/MathML">'
        "<semantics>"
        "<mrow><mi>b</mi><mo>=</mo><mn>2</mn></mrow>"
        '<annotation encoding="application/x-tex">b=2</annotation>'
        "</semantics>"
        "</math>"
        "</p>"
        "</main></body></html>"
    )
    seen: dict[str, str] = {}

    monkeypatch.setattr(
        extract,
        "_ensure_pandoc_ready",
        lambda: (
            True,
            None,
            SimpleNamespace(get_pandoc_path=lambda: "/tmp/fake-pandoc"),
        ),
    )

    def fake_run_pandoc_html_to_markdown(
        *, pandoc_path: str, html: str
    ) -> tuple[str | None, str, str | None]:
        seen["pandoc_path"] = pandoc_path
        seen["html"] = html
        return (
            "# converted",
            "[WARNING] Could not convert TeX math a=1, rendering as TeX",
            None,
        )

    monkeypatch.setattr(
        extract,
        "_run_pandoc_html_to_markdown",
        fake_run_pandoc_html_to_markdown,
    )

    diag: dict[str, int] = {}
    markdown, _elapsed_ms, error = extract.convert_html_document_to_markdown(
        html, diag=diag
    )

    assert error is None
    assert markdown == "# converted"
    assert seen["pandoc_path"] == "/tmp/fake-pandoc"
    assert "<math" not in seen["html"]
    assert "$a=1$" in seen["html"]
    assert "$$\nb=2\n$$" in seen["html"]
    assert diag["pandoc_input_math_tags"] == 2
    assert diag["pandoc_math_replaced_total"] == 2
    assert diag["pandoc_math_inline_total"] == 1
    assert diag["pandoc_math_block_total"] == 1
    assert diag["pandoc_warning_count"] == 1
    assert diag["pandoc_warning_tex_math_convert_failed"] == 1


def test_extract_latex_text_files_from_tar_returns_empty_list_when_archive_open_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: broken LaTeX archives should degrade to an empty file list."""

    def fake_open(*args: object, **kwargs: object) -> object:
        _ = (args, kwargs)
        raise OSError("broken archive")

    monkeypatch.setattr(extract.tarfile, "open", fake_open)

    assert extract._extract_latex_text_files_from_tar(b"broken") == []
