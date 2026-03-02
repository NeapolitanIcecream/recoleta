from __future__ import annotations

from recoleta.extract import extract_html_document_cleaned_with_references


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
