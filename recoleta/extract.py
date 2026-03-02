from __future__ import annotations

import gzip
from io import BytesIO
import os
import tarfile
import tempfile
import time
from contextlib import contextmanager
from typing import Any

from bs4 import BeautifulSoup
from bs4.element import Tag
import httpx
import trafilatura
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)


_MARKER_PDF_CONVERTER: Any | None = None
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


_EXTERNAL_PROGRESS_ENV: dict[str, str] = {
    # HuggingFace Hub tqdm progress bars (used by many model download paths).
    "HF_HUB_DISABLE_PROGRESS_BARS": "1",
    # tqdm supports env overrides via the TQDM_ prefix (envwrap). Use a boolean-ish value.
    "TQDM_DISABLE": "True",
}


@contextmanager
def _external_progress_disabled() -> Any:
    """Disable third-party progress bars for clean Rich TUI output."""

    previous: dict[str, str | None] = {
        key: os.environ.get(key) for key in _EXTERNAL_PROGRESS_ENV
    }
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


def _pdf_has_text_layer(pdf_bytes: bytes) -> bool:
    if not pdf_bytes:
        return False
    pymupdf = _get_pymupdf_module()
    if pymupdf is None:
        return False

    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return False

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
    finally:
        try:
            doc.close()
        except Exception:
            pass
    return False


def _extract_pdf_text_with_pymupdf4llm(pdf_bytes: bytes) -> str | None:
    if not pdf_bytes:
        return None
    pymupdf = _get_pymupdf_module()
    pymupdf4llm = _get_pymupdf4llm_module()
    if pymupdf is None or pymupdf4llm is None:
        return None

    markdown: Any = None
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return None

    try:
        markdown = pymupdf4llm.to_markdown(doc)
    except Exception:
        return None
    finally:
        try:
            doc.close()
        except Exception:
            pass

    normalized = str(markdown or "").strip()
    return normalized or None


def _extract_pdf_text_with_marker(pdf_bytes: bytes) -> str | None:
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


def extract_pdf_text(pdf_bytes: bytes) -> str | None:
    if not pdf_bytes:
        return None
    if _pdf_has_text_layer(pdf_bytes):
        pymupdf_markdown = _extract_pdf_text_with_pymupdf4llm(pdf_bytes)
        if pymupdf_markdown is not None:
            return pymupdf_markdown
    return _extract_pdf_text_with_marker(pdf_bytes)


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
    except tarfile.TarError, OSError:
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
    """Extract a cleaned HTML document and split off References/Bibliography blocks.

    Returns (cleaned_html, references_html, stats).
    """

    stripped = html.strip()
    if not stripped:
        return None, None, {"error": "empty_input"}

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
        return None, None, {"error": "empty_main_container"}

    def _has_semantic_payload(tag: Tag) -> bool:
        # Keep wrappers that contain valuable structured content.
        if tag.find(["math", "table", "pre", "code", "svg", "img"]):
            return True
        class_attr = tag.get("class")
        classes = (
            [str(c) for c in class_attr]
            if isinstance(class_attr, list)
            else [str(class_attr)]
            if class_attr
            else []
        )
        class_blob = " ".join(classes).lower()
        # arXiv/LaTeXML math/table/code wrappers often include these markers.
        keep_markers = (
            "math",
            "equation",
            "eqn",
            "align",
            "matrix",
            "tabular",
            "table",
            "listing",
            "verbatim",
            "code",
            "algorithm",
            "figure",
            "caption",
        )
        return any(marker in class_blob for marker in keep_markers)

    def _simplify_arxiv_html(container: Tag) -> dict[str, int]:
        removed_metadata = 0
        unwrapped = 0
        removed_attrs = 0

        # Remove common author/contact/metadata blocks (keeps abstract and body).
        metadata_selectors = [
            ".ltx_authors",
            ".ltx_author_notes",
            ".ltx_affiliation",
            ".ltx_contact",
            ".ltx_role_orcid",
            ".ltx_role_email",
            ".ltx_role_author",
            ".ltx_creator",
            ".ltx_date",
        ]
        for selector in metadata_selectors:
            for tag in list(container.select(selector)):
                tag.decompose()
                removed_metadata += 1

        # Drop mailto/orcid links while keeping visible text (avoid raw href noise).
        for a in list(container.find_all("a")):
            href = a.get("href")
            href_str = str(href or "")
            if "mailto:" in href_str or "orcid.org" in href_str:
                a.unwrap()

        # Strip most attributes to reduce pandoc emitting raw HTML. Preserve a small allowlist.
        allowed_attrs = {"colspan", "rowspan", "href", "src", "alt"}
        for tag in container.find_all(True):
            attrs = dict(getattr(tag, "attrs", {}) or {})
            if not attrs:
                continue
            new_attrs: dict[str, Any] = {}
            for key, value in attrs.items():
                if key in allowed_attrs:
                    new_attrs[key] = value
            if new_attrs != attrs:
                removed_attrs += len(attrs) - len(new_attrs)
                tag.attrs = new_attrs

        # Unwrap stylistic span/div wrappers that don't carry semantic payload.
        for tag_name in ("span", "div"):
            for tag in list(container.find_all(tag_name)):
                if _has_semantic_payload(tag):
                    continue
                # Avoid unwrapping section/article containers (structural boundaries).
                if tag.name in {"section", "article"}:
                    continue
                try:
                    tag.unwrap()
                    unwrapped += 1
                except Exception:
                    continue

        return {
            "removed_metadata_blocks": removed_metadata,
            "unwrapped_wrappers": unwrapped,
            "removed_attrs_total": removed_attrs,
        }

    # Remove obvious non-body blocks that often duplicate navigation/TOC/metadata.
    removed_non_body = 0
    non_body_selectors = [
        '[role="navigation"]',
        '[aria-label="navigation"]',
        ".toc",
        ".ltx_toc",
        ".ltx_role_toc",
        ".ltx_page_header",
        ".ltx_page_footer",
        ".ltx_sidebar",
        ".sidebar",
    ]
    for selector in non_body_selectors:
        for tag in list(main_container.select(selector)):
            tag.decompose()
            removed_non_body += 1

    # Split References/Bibliography blocks out of the main container.
    references_blocks: list[str] = []
    removed_references = 0

    def is_reference_heading(text: str) -> bool:
        normalized = " ".join(text.strip().lower().split())
        return normalized in {"references", "bibliography"}

    # 1) Prefer explicit bibliography containers/classes (arXiv HTML often uses these).
    for tag in list(
        main_container.select(
            ".ltx_bibliography, .ltx_biblist, .ltx_references, #references, #bibliography, .references, .bibliography"
        )
    ):
        references_blocks.append(str(tag))
        tag.decompose()
        removed_references += 1

    # 2) Fallback: heading-based split (remove heading + following siblings until next heading of same/higher level).
    for heading in list(main_container.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])):
        heading_text = heading.get_text(" ", strip=True)
        if not heading_text or not is_reference_heading(heading_text):
            continue
        level = int(heading.name[1])
        parent = heading.parent
        if parent is None:
            continue
        # If the heading is inside a section-like container, extract that container.
        if parent.name in {"section", "div"} and parent.get_text(" ", strip=True):
            references_blocks.append(str(parent))
            parent.decompose()
            removed_references += 1
            continue
        # Otherwise remove the heading and a best-effort contiguous block after it.
        collected: list[str] = [str(heading)]
        current = heading.next_sibling
        while current is not None:
            next_node = getattr(current, "next_sibling", None)
            if getattr(current, "name", None) in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                try:
                    next_level = int(str(getattr(current, "name"))[1])
                except Exception:
                    next_level = 6
                if next_level <= level:
                    break
            try:
                collected.append(str(current))
                current.extract()
            except Exception:
                pass
            current = next_node
        try:
            heading.decompose()
        except Exception:
            pass
        references_blocks.append("\n".join(collected))
        removed_references += 1

    simplify_stats = _simplify_arxiv_html(main_container)

    def normalize_html_fragment(fragment: str, *, limit: int) -> str | None:
        normalized_lines = [
            line.strip() for line in fragment.splitlines() if line.strip()
        ]
        combined = "\n".join(normalized_lines).strip()
        if not combined:
            return None
        if limit > 0 and len(combined) > limit:
            combined = combined[:limit].rstrip()
        return combined or None

    cleaned_html = normalize_html_fragment(str(main_container), limit=max_chars)
    references_html: str | None = None
    if references_blocks:
        references_html = normalize_html_fragment(
            "\n\n".join(references_blocks), limit=references_max_chars
        )

    stats: dict[str, Any] = {
        "removed_non_body_blocks": removed_non_body,
        "removed_references_blocks": removed_references,
        "references_blocks_collected": len(references_blocks),
        "cleaned_chars": len(cleaned_html or ""),
        "references_chars": len(references_html or ""),
        **simplify_stats,
    }
    return cleaned_html, references_html, stats


def convert_html_document_to_markdown(
    html: str,
    *,
    max_chars: int = _HTML_DOCUMENT_MAX_CHARS,
) -> tuple[str | None, int, str | None]:
    """Convert HTML to GitHub-flavored Markdown via Pandoc (pypandoc)."""

    started = time.perf_counter()
    ready, ready_error, pypandoc = _ensure_pandoc_ready()
    if (not ready) or pypandoc is None:
        return None, 0, ready_error or "pandoc_unavailable"
    try:
        markdown = pypandoc.convert_text(
            html,
            to="gfm",
            format="html",
            extra_args=["--wrap=none"],
        )
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return (
            None,
            elapsed_ms,
            f"pandoc_convert_failed error={type(exc).__name__}: {exc}",
        )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    normalized = str(markdown or "").strip()
    if not normalized:
        return None, elapsed_ms, "empty_markdown"
    if max_chars > 0 and len(normalized) > max_chars:
        normalized = normalized[:max_chars].rstrip()
    return normalized or None, elapsed_ms, None
