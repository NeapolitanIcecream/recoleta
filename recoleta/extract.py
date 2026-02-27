from __future__ import annotations

import gzip
from io import BytesIO
import os
import tarfile
import tempfile
from contextlib import contextmanager
from typing import Any

from bs4 import BeautifulSoup
import httpx
import trafilatura
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter


_MARKER_PDF_CONVERTER: Any | None = None
_ARXIV_LATEX_MAX_CHARS = 200_000
_HTML_DOCUMENT_MAX_CHARS = 200_000
_LATEX_TEXT_SUFFIXES = (".tex", ".bib", ".bbl", ".txt", ".cls", ".sty")


_EXTERNAL_PROGRESS_ENV: dict[str, str] = {
    # HuggingFace Hub tqdm progress bars (used by many model download paths).
    "HF_HUB_DISABLE_PROGRESS_BARS": "1",
    # tqdm supports env overrides via the TQDM_ prefix (envwrap). Use a boolean-ish value.
    "TQDM_DISABLE": "True",
}


@contextmanager
def _external_progress_disabled() -> Any:
    """Disable third-party progress bars for clean Rich TUI output."""

    previous: dict[str, str | None] = {key: os.environ.get(key) for key in _EXTERNAL_PROGRESS_ENV}
    os.environ.update(_EXTERNAL_PROGRESS_ENV)
    tqdm_patches: list[tuple[object, str, object]] = []
    hf_prev_disabled: bool | None = None
    try:
        try:
            import huggingface_hub.utils as hf_utils

            are_disabled = getattr(hf_utils, "are_progress_bars_disabled", None)
            disable = getattr(hf_utils, "disable_progress_bars", None)
            if callable(are_disabled):
                hf_prev_disabled = bool(are_disabled())
            if callable(disable):
                disable()
        except Exception:
            pass

        try:
            def force_disable_tqdm(tqdm_cls: object) -> None:
                original_init = getattr(tqdm_cls, "__init__")

                def patched_init(self, *args, **kwargs):  # type: ignore[no-untyped-def]
                    # Some libraries explicitly pass disable=False. Override unconditionally.
                    kwargs["disable"] = True
                    return original_init(self, *args, **kwargs)

                tqdm_patches.append((tqdm_cls, "__init__", original_init))
                setattr(tqdm_cls, "__init__", patched_init)

            import tqdm.std as tqdm_std

            force_disable_tqdm(tqdm_std.tqdm)

            # Best-effort: patch common frontends that might define their own tqdm class.
            try:
                import tqdm.auto as tqdm_auto

                force_disable_tqdm(tqdm_auto.tqdm)
            except Exception:
                pass
            try:
                import tqdm.notebook as tqdm_notebook

                force_disable_tqdm(tqdm_notebook.tqdm)
            except Exception:
                pass
            try:
                import tqdm.rich as tqdm_rich  # type: ignore[import-not-found]

                force_disable_tqdm(tqdm_rich.tqdm)
            except Exception:
                pass
        except Exception:
            pass

        yield
    finally:
        if hf_prev_disabled is False:
            try:
                import huggingface_hub.utils as hf_utils

                enable = getattr(hf_utils, "enable_progress_bars", None)
                if callable(enable):
                    enable()
            except Exception:
                pass
        for target, attr, value in reversed(tqdm_patches):
            try:
                setattr(target, attr, value)
            except Exception:
                pass
        for key, old_value in previous.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value


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

    with _external_progress_disabled():
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
        with _external_progress_disabled():
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


def _decode_text_bytes(payload: bytes) -> str | None:
    if not payload:
        return None
    for encoding in ("utf-8", "latin-1"):
        try:
            decoded = payload.decode(encoding)
        except Exception:
            continue
        stripped = decoded.strip()
        if stripped:
            return stripped
    return None


def _decompress_gzip_if_needed(payload: bytes) -> bytes:
    if len(payload) >= 2 and payload[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(payload)
        except Exception:
            return payload
    return payload


def _extract_latex_text_files_from_tar(payload: bytes) -> list[tuple[str, str]]:
    extracted_files: list[tuple[str, str]] = []
    try:
        with tarfile.open(fileobj=BytesIO(payload), mode="r:*") as archive:
            members = sorted(archive.getmembers(), key=lambda member: member.name)
            for member in members:
                if not member.isfile():
                    continue
                file_name = member.name.strip()
                if not file_name:
                    continue
                if not file_name.lower().endswith(_LATEX_TEXT_SUFFIXES):
                    continue
                file_obj = archive.extractfile(member)
                if file_obj is None:
                    continue
                decoded = _decode_text_bytes(file_obj.read())
                if decoded is None:
                    continue
                extracted_files.append((file_name, decoded))
    except (tarfile.TarError, OSError):
        return []
    return extracted_files


def _clean_latex_text(raw_text: str) -> str | None:
    cleaned_lines: list[str] = []
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("%"):
            continue
        normalized = " ".join(stripped.split())
        if normalized:
            cleaned_lines.append(normalized)
    if not cleaned_lines:
        return None
    return "\n".join(cleaned_lines).strip() or None


def extract_arxiv_latex_source(archive_bytes: bytes, *, max_chars: int = _ARXIV_LATEX_MAX_CHARS) -> str | None:
    if not archive_bytes:
        return None
    payload = _decompress_gzip_if_needed(archive_bytes)
    chunks: list[str] = []
    tar_chunks = _extract_latex_text_files_from_tar(payload)
    if tar_chunks:
        for file_name, raw_text in tar_chunks:
            cleaned = _clean_latex_text(raw_text)
            if cleaned is None:
                continue
            chunks.append(f"% FILE: {file_name}\n{cleaned}")
    else:
        decoded = _decode_text_bytes(payload)
        if decoded is not None:
            cleaned = _clean_latex_text(decoded)
            if cleaned is not None:
                chunks.append(cleaned)
    if not chunks:
        return None
    combined = "\n\n".join(chunks).strip()
    if max_chars > 0 and len(combined) > max_chars:
        combined = combined[:max_chars].rstrip()
    return combined or None


def extract_html_document_cleaned(html: str, *, max_chars: int = _HTML_DOCUMENT_MAX_CHARS) -> str | None:
    stripped = html.strip()
    if not stripped:
        return None
    soup = BeautifulSoup(stripped, "html.parser")
    for tag in soup(["script", "style", "noscript", "iframe"]):
        tag.decompose()
    for tag_name in ("nav", "header", "footer", "aside", "form"):
        for tag in soup.find_all(tag_name):
            tag.decompose()

    main_container = soup.find("main")
    if main_container is None:
        main_container = soup.find("article")
    if main_container is None:
        main_container = soup.body if soup.body is not None else soup

    if not main_container.get_text(" ", strip=True):
        return None
    normalized_lines = [line.strip() for line in str(main_container).splitlines() if line.strip()]
    cleaned_html = "\n".join(normalized_lines).strip()
    if max_chars > 0 and len(cleaned_html) > max_chars:
        cleaned_html = cleaned_html[:max_chars].rstrip()
    return cleaned_html or None

