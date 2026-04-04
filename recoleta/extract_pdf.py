from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class PdfTextExtractionRequest:
    pdf_bytes: bytes
    diag: dict[str, Any] | None
    get_pymupdf_module: Callable[[], Any | None]
    get_pymupdf4llm_module: Callable[[], Any | None]
    pdf_has_text_layer: Callable[[Any], bool]
    extract_with_pymupdf4llm: Callable[..., str | None]
    markdown_looks_useful: Callable[[str | None], bool]


def _open_pdf_document(
    *,
    pdf_bytes: bytes,
    get_pymupdf_module: Callable[[], Any | None],
) -> tuple[Any | None, Any | None]:
    pymupdf = get_pymupdf_module()
    if pymupdf is None:
        return None, None
    try:
        return pymupdf.open(stream=pdf_bytes, filetype="pdf"), pymupdf
    except Exception:
        return None, pymupdf


def _set_pdf_backend(diag: dict[str, Any] | None, *, backend: str) -> None:
    if diag is not None:
        diag["pdf_backend"] = backend


def _open_pdf_extraction_context(
    *,
    pdf_bytes: bytes,
    get_pymupdf_module: Callable[[], Any | None],
    get_pymupdf4llm_module: Callable[[], Any | None],
) -> tuple[Any | None, Any | None]:
    pymupdf4llm = get_pymupdf4llm_module()
    doc, pymupdf = _open_pdf_document(
        pdf_bytes=pdf_bytes,
        get_pymupdf_module=get_pymupdf_module,
    )
    if pymupdf is None or pymupdf4llm is None or doc is None:
        return None, None
    return doc, pymupdf4llm


def _record_pdf_diag(
    *,
    diag: dict[str, Any] | None,
    doc: Any,
    pdf_has_text_layer: Callable[[Any], bool],
    markdown: str | None,
) -> None:
    if diag is None:
        return
    diag["pdf_has_text_layer"] = bool(pdf_has_text_layer(doc))
    diag["pymupdf4llm_md_chars"] = len(str(markdown or ""))


def _extract_markdown_from_doc(
    *,
    doc: Any,
    pymupdf4llm: Any,
    diag: dict[str, Any] | None,
    pdf_has_text_layer: Callable[[Any], bool],
    extract_with_pymupdf4llm: Callable[..., str | None],
) -> str | None:
    markdown = extract_with_pymupdf4llm(doc, pymupdf4llm=pymupdf4llm)
    _record_pdf_diag(
        diag=diag,
        doc=doc,
        pdf_has_text_layer=pdf_has_text_layer,
        markdown=markdown,
    )
    return markdown


def _close_doc_quietly(doc: Any) -> None:
    try:
        doc.close()
    except Exception:
        pass


def _empty_pdf_result(diag: dict[str, Any] | None) -> None:
    _set_pdf_backend(diag, backend="none")
    return None


def _extract_pdf_markdown(
    *,
    doc: Any,
    pymupdf4llm: Any,
    diag: dict[str, Any] | None,
    pdf_has_text_layer: Callable[[Any], bool],
    extract_with_pymupdf4llm: Callable[..., str | None],
) -> str | None:
    try:
        return _extract_markdown_from_doc(
            doc=doc,
            pymupdf4llm=pymupdf4llm,
            diag=diag,
            pdf_has_text_layer=pdf_has_text_layer,
            extract_with_pymupdf4llm=extract_with_pymupdf4llm,
        )
    finally:
        _close_doc_quietly(doc)


def extract_pdf_text_impl(
    *,
    request: PdfTextExtractionRequest,
) -> str | None:
    if not request.pdf_bytes:
        return _empty_pdf_result(request.diag)

    doc, pymupdf4llm = _open_pdf_extraction_context(
        pdf_bytes=request.pdf_bytes,
        get_pymupdf_module=request.get_pymupdf_module,
        get_pymupdf4llm_module=request.get_pymupdf4llm_module,
    )
    if doc is None or pymupdf4llm is None:
        return _empty_pdf_result(request.diag)
    pymupdf_markdown = _extract_pdf_markdown(
        doc=doc,
        pymupdf4llm=pymupdf4llm,
        diag=request.diag,
        pdf_has_text_layer=request.pdf_has_text_layer,
        extract_with_pymupdf4llm=request.extract_with_pymupdf4llm,
    )
    if not request.markdown_looks_useful(pymupdf_markdown):
        return _empty_pdf_result(request.diag)
    _set_pdf_backend(request.diag, backend="pymupdf4llm")
    return str(pymupdf_markdown).strip()
