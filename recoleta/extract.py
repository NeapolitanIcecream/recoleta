from __future__ import annotations

import tempfile
from typing import Any

import httpx
import trafilatura
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter


_MARKER_PDF_CONVERTER: Any | None = None


def _should_retry_httpx(exc: BaseException) -> bool:
    if isinstance(exc, httpx.RequestError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status >= 500 or status == 429
    return False


@retry(
    retry=retry_if_exception(_should_retry_httpx),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=6.0),
    reraise=True,
)
def fetch_url_html(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    return response.text


@retry(
    retry=retry_if_exception(_should_retry_httpx),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=6.0),
    reraise=True,
)
def fetch_url_bytes(client: httpx.Client, url: str) -> bytes:
    response = client.get(url)
    response.raise_for_status()
    return response.content


def extract_html_maintext(html: str) -> str | None:
    extracted = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        include_formatting=False,
        deduplicate=True,
    )
    if not extracted:
        return None
    stripped = extracted.strip()
    return stripped or None


def _get_marker_pdf_converter() -> Any:
    global _MARKER_PDF_CONVERTER
    if _MARKER_PDF_CONVERTER is not None:
        return _MARKER_PDF_CONVERTER

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict

    _MARKER_PDF_CONVERTER = PdfConverter(artifact_dict=create_model_dict())
    return _MARKER_PDF_CONVERTER


def extract_pdf_text(pdf_bytes: bytes) -> str | None:
    if not pdf_bytes:
        return None

    converter = _get_marker_pdf_converter()
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        rendered = converter(tmp.name)

    markdown = getattr(rendered, "markdown", None)
    if isinstance(markdown, str) and markdown.strip():
        return markdown.strip()

    try:
        from marker.output import text_from_rendered

        text, _, _ = text_from_rendered(rendered)
        if isinstance(text, str) and text.strip():
            return text.strip()
    except Exception:
        return None
    return None

