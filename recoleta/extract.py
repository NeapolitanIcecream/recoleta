from __future__ import annotations

import os
import tempfile
from contextlib import contextmanager
from typing import Any

import httpx
import trafilatura
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter


_MARKER_PDF_CONVERTER: Any | None = None


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
    try:
        try:
            from huggingface_hub.utils.tqdm import disable_progress_bars

            disable_progress_bars()
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

