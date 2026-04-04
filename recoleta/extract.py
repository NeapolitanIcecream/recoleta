from __future__ import annotations

import gzip
from io import BytesIO
import re
import subprocess
import tarfile
import time
from typing import Any

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import httpx
import trafilatura
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)


_PYMUPDF: Any | None = None
_PYMUPDF4LLM: Any | None = None
_PYMUPDF_READY: bool | None = None
_PYMUPDF4LLM_READY: bool | None = None
_ARXIV_LATEX_MAX_CHARS = 200_000
_HTML_DOCUMENT_MAX_CHARS = 200_000
_HTML_REFERENCES_MAX_CHARS = 120_000
_LATEX_TEXT_SUFFIXES = (".tex", ".bib", ".bbl", ".txt", ".cls", ".sty")
_PDF_TEXT_LAYER_CHECK_MAX_PAGES = 3
_PDF_TEXT_LAYER_MIN_CHARS = 200

# Pandoc availability is environment-dependent. Cache the check so we don't
# repeatedly raise and log the same error on hot paths.
_PYPANDOC: Any | None = None
_PANDOC_READY: bool | None = None
_PANDOC_READY_ERROR: str | None = None
_PANDOC_LOG_PATTERN = re.compile(r"^\[(ERROR|WARNING|INFO|DEBUG)\]\s*(.*)$")


def _ensure_pandoc_ready() -> tuple[bool, str | None, Any | None]:
    global _PYPANDOC, _PANDOC_READY, _PANDOC_READY_ERROR  # noqa: PLW0603
    if _PANDOC_READY is not None:
        return _PANDOC_READY, _PANDOC_READY_ERROR, _PYPANDOC

    started = time.perf_counter()
    try:
        import pypandoc  # type: ignore[import-not-found]

        _PYPANDOC = pypandoc
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        _PANDOC_READY = False
        _PANDOC_READY_ERROR = f"pypandoc_import_failed elapsed_ms={elapsed_ms} error={type(exc).__name__}: {exc}"
        return _PANDOC_READY, _PANDOC_READY_ERROR, _PYPANDOC

    try:
        # This will raise when the pandoc binary isn't installed.
        _ = _PYPANDOC.get_pandoc_version()  # type: ignore[union-attr]
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        _PANDOC_READY = False
        _PANDOC_READY_ERROR = f"pandoc_unavailable elapsed_ms={elapsed_ms} error={type(exc).__name__}: {exc}"
        return _PANDOC_READY, _PANDOC_READY_ERROR, _PYPANDOC

    _PANDOC_READY = True
    _PANDOC_READY_ERROR = None
    return _PANDOC_READY, _PANDOC_READY_ERROR, _PYPANDOC


def _extract_tex_annotation_from_math(tag: Tag) -> str | None:
    annotation = tag.find("annotation", attrs={"encoding": "application/x-tex"})
    if annotation is None:
        for candidate in tag.find_all("annotation"):
            encoding = str(candidate.get("encoding") or "").strip().lower()
            if "tex" in encoding:
                annotation = candidate
                break
    if annotation is not None:
        tex = annotation.get_text("", strip=True)
        if tex:
            return tex
    alttext = str(tag.get("alttext") or "").strip()
    return alttext or None


def _prepare_html_for_pandoc_markdown(html: str) -> tuple[str, dict[str, int]]:
    soup = BeautifulSoup(html, "html.parser")
    math_tags = list(soup.find_all("math"))
    inline_total = 0
    block_total = 0
    replaced_total = 0
    missing_tex_total = 0

    for math_tag in math_tags:
        tex = _extract_tex_annotation_from_math(math_tag)
        if tex is None:
            missing_tex_total += 1
            continue
        is_block = str(math_tag.get("display") or "").strip().lower() == "block"
        replacement = f"$$\n{tex}\n$$" if is_block else f"${tex}$"
        math_tag.replace_with(NavigableString(replacement))
        replaced_total += 1
        if is_block:
            block_total += 1
        else:
            inline_total += 1

    return str(soup), {
        "pandoc_input_math_tags": len(math_tags),
        "pandoc_math_replaced_total": replaced_total,
        "pandoc_math_inline_total": inline_total,
        "pandoc_math_block_total": block_total,
        "pandoc_math_missing_tex_total": missing_tex_total,
    }


def _split_pandoc_stderr_messages(raw: str) -> list[tuple[str, str]]:
    stripped = str(raw or "").strip()
    if not stripped:
        return []

    messages: list[tuple[str, str]] = []
    current_level = "WARNING"
    current_lines: list[str] = []
    for line in stripped.splitlines():
        match = _PANDOC_LOG_PATTERN.match(line)
        if match is not None:
            if current_lines:
                messages.append((current_level, "\n".join(current_lines).strip()))
            current_level = str(match.group(1) or "WARNING").upper()
            current_lines = [str(match.group(2) or "")]
            continue
        current_lines.append(line)
    if current_lines:
        messages.append((current_level, "\n".join(current_lines).strip()))
    return messages


def _categorize_pandoc_warning(message: str) -> str:
    normalized = " ".join(str(message or "").strip().lower().split())
    if normalized.startswith("could not convert tex math"):
        return "tex_math_convert_failed"
    return "other"


def _run_pandoc_html_to_markdown(
    *, pandoc_path: str, html: str
) -> tuple[str | None, str, str | None]:
    try:
        completed = subprocess.run(
            [pandoc_path, "--from=html", "--to=gfm", "--wrap=none"],
            input=html,
            capture_output=True,
            check=False,
            text=True,
            encoding="utf-8",
        )
    except Exception as exc:  # noqa: BLE001
        return None, "", f"pandoc_convert_failed error={type(exc).__name__}: {exc}"

    stderr = str(completed.stderr or "")
    if completed.returncode != 0:
        excerpt = " ".join(stderr.strip().split())
        if len(excerpt) > 280:
            excerpt = excerpt[:280].rstrip()
        error_text = excerpt or "unknown"
        return (
            None,
            stderr,
            f"pandoc_convert_failed exit_code={completed.returncode} error={error_text}",
        )
    return str(completed.stdout or ""), stderr, None


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


def _get_pymupdf_module() -> Any | None:
    global _PYMUPDF, _PYMUPDF_READY
    if _PYMUPDF_READY is False:
        return None
    if _PYMUPDF is not None:
        return _PYMUPDF
    try:
        import pymupdf  # type: ignore[import-not-found]

        _PYMUPDF = pymupdf
        _PYMUPDF_READY = True
        return _PYMUPDF
    except Exception:
        try:
            import fitz  # type: ignore[import-not-found]

            _PYMUPDF = fitz
            _PYMUPDF_READY = True
            return _PYMUPDF
        except Exception:
            _PYMUPDF_READY = False
            return None


def _get_pymupdf4llm_module() -> Any | None:
    global _PYMUPDF4LLM, _PYMUPDF4LLM_READY
    if _PYMUPDF4LLM_READY is False:
        return None
    if _PYMUPDF4LLM is not None:
        return _PYMUPDF4LLM
    try:
        import pymupdf4llm  # type: ignore[import-not-found]

        _PYMUPDF4LLM = pymupdf4llm
        _PYMUPDF4LLM_READY = True
        return _PYMUPDF4LLM
    except Exception:
        _PYMUPDF4LLM_READY = False
        return None


def _pdf_has_text_layer(doc: Any) -> bool:
    try:
        page_count = int(getattr(doc, "page_count", 0) or 0)
        if page_count <= 0:
            return False
        text_chars = 0
        for page_index in range(min(page_count, _PDF_TEXT_LAYER_CHECK_MAX_PAGES)):
            page = doc.load_page(page_index)
            extracted = str(page.get_text("text") or "")
            if not extracted:
                continue
            # Ignore layout whitespace to avoid false positives.
            text_chars += len("".join(extracted.split()))
            if text_chars >= _PDF_TEXT_LAYER_MIN_CHARS:
                return True
    except Exception:
        return False
    return False


def _extract_pdf_text_with_pymupdf4llm(
    doc: Any, *, pymupdf4llm: Any | None = None
) -> str | None:
    module = pymupdf4llm or _get_pymupdf4llm_module()
    if module is None:
        return None

    markdown: Any = None
    try:
        markdown = module.to_markdown(doc)
    except Exception:
        return None

    normalized = str(markdown or "").strip()
    return normalized or None


def _pdf_markdown_looks_useful(markdown: str | None, *, min_chars: int) -> bool:
    normalized = str(markdown or "").strip()
    if not normalized:
        return False
    # Ignore whitespace to avoid accepting empty layout artifacts.
    dense_chars = len("".join(normalized.split()))
    return dense_chars >= min_chars


def extract_pdf_text(
    pdf_bytes: bytes,
    *,
    diag: dict[str, Any] | None = None,
) -> str | None:
    from recoleta.extract_pdf import PdfTextExtractionRequest, extract_pdf_text_impl

    return extract_pdf_text_impl(
        request=PdfTextExtractionRequest(
            pdf_bytes=pdf_bytes,
            diag=diag,
            get_pymupdf_module=_get_pymupdf_module,
            get_pymupdf4llm_module=_get_pymupdf4llm_module,
            pdf_has_text_layer=_pdf_has_text_layer,
            extract_with_pymupdf4llm=_extract_pdf_text_with_pymupdf4llm,
            markdown_looks_useful=lambda value: _pdf_markdown_looks_useful(
                value,
                min_chars=24,
            ),
        )
    )


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


def extract_arxiv_latex_source(
    archive_bytes: bytes, *, max_chars: int = _ARXIV_LATEX_MAX_CHARS
) -> str | None:
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


def extract_html_document_cleaned(
    html: str, *, max_chars: int = _HTML_DOCUMENT_MAX_CHARS
) -> str | None:
    cleaned, _, _ = extract_html_document_cleaned_with_references(
        html, max_chars=max_chars
    )
    return cleaned


def extract_html_document_cleaned_with_references(
    html: str,
    *,
    max_chars: int = _HTML_DOCUMENT_MAX_CHARS,
    references_max_chars: int = _HTML_REFERENCES_MAX_CHARS,
) -> tuple[str | None, str | None, dict[str, Any]]:
    from recoleta.extract_html import extract_html_document_cleaned_with_references_impl

    return extract_html_document_cleaned_with_references_impl(
        html,
        max_chars=max_chars,
        references_max_chars=references_max_chars,
    )


def convert_html_document_to_markdown(
    html: str,
    *,
    max_chars: int = _HTML_DOCUMENT_MAX_CHARS,
    diag: dict[str, Any] | None = None,
) -> tuple[str | None, int, str | None]:
    from recoleta.extract_markdown import (
        MarkdownConversionRequest,
        convert_html_document_to_markdown_impl,
    )

    return convert_html_document_to_markdown_impl(
        request=MarkdownConversionRequest(
            html=html,
            max_chars=max_chars,
            diag=diag,
            ensure_pandoc_ready=_ensure_pandoc_ready,
            prepare_html=_prepare_html_for_pandoc_markdown,
            run_pandoc=_run_pandoc_html_to_markdown,
            split_messages=_split_pandoc_stderr_messages,
            categorize_warning=_categorize_pandoc_warning,
        )
    )
