from __future__ import annotations

from dataclasses import dataclass
import time
from types import SimpleNamespace
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class MarkdownConversionRequest:
    html: str
    max_chars: int
    diag: dict[str, Any] | None
    ensure_pandoc_ready: Callable[[], tuple[bool, str | None, Any | None]]
    prepare_html: Callable[[str], tuple[str, dict[str, int]]]
    run_pandoc: Callable[..., tuple[str | None, str, str | None]]
    split_messages: Callable[[str], list[tuple[str, str]]]
    categorize_warning: Callable[[str], str]


def _warning_counts(
    *,
    stderr: str,
    split_messages: Callable[[str], list[tuple[str, str]]],
    categorize_warning: Callable[[str], str],
) -> tuple[int, dict[str, int]]:
    warning_counts: dict[str, int] = {}
    warning_count = 0
    for level, message in split_messages(stderr):
        if level != "WARNING":
            continue
        warning_count += 1
        category = categorize_warning(message)
        warning_counts[category] = warning_counts.get(category, 0) + 1
    return warning_count, warning_counts


def _pandoc_unavailable_result(
    *,
    diag: dict[str, Any] | None,
    error: str,
) -> tuple[str | None, int, str | None]:
    if diag is not None:
        diag["pandoc_failed"] = 1
    return None, 0, error


def _pandoc_runtime(started: float) -> SimpleNamespace:
    return SimpleNamespace(elapsed_ms=int((time.perf_counter() - started) * 1000))


def _record_warning_diag(
    *,
    diag: dict[str, Any] | None,
    stderr: str,
    split_messages: Callable[[str], list[tuple[str, str]]],
    categorize_warning: Callable[[str], str],
) -> None:
    warning_count, warning_counts = _warning_counts(
        stderr=stderr,
        split_messages=split_messages,
        categorize_warning=categorize_warning,
    )
    if diag is None:
        return
    diag["pandoc_warning_count"] = warning_count
    for category, count in warning_counts.items():
        diag[f"pandoc_warning_{category}"] = count


def _normalized_markdown_result(
    *,
    markdown: str | None,
    max_chars: int,
) -> str | None:
    normalized = str(markdown or "").strip()
    if not normalized:
        return None
    if max_chars > 0 and len(normalized) > max_chars:
        normalized = normalized[:max_chars].rstrip()
    return normalized or None


def _prepare_pandoc_conversion(
    *,
    html: str,
    diag: dict[str, Any] | None,
    ensure_pandoc_ready: Callable[[], tuple[bool, str | None, Any | None]],
    prepare_html: Callable[[str], tuple[str, dict[str, int]]],
) -> tuple[str, str] | tuple[None, str]:
    ready, ready_error, pypandoc = ensure_pandoc_ready()
    if (not ready) or pypandoc is None:
        return None, ready_error or "pandoc_unavailable"
    prepared_html, prepare_stats = prepare_html(html)
    if diag is not None:
        diag.update(prepare_stats)
    return str(pypandoc.get_pandoc_path()), prepared_html


def _finalize_pandoc_result(
    *,
    started: float,
    diag: dict[str, Any] | None,
    markdown: str | None,
    error: str | None,
    max_chars: int,
) -> tuple[str | None, int, str | None]:
    runtime = _pandoc_runtime(started)
    if error is not None:
        if diag is not None:
            diag["pandoc_failed"] = 1
        return None, runtime.elapsed_ms, error
    normalized = _normalized_markdown_result(markdown=markdown, max_chars=max_chars)
    if normalized:
        return normalized, runtime.elapsed_ms, None
    if diag is not None:
        diag["pandoc_failed"] = 1
    return None, runtime.elapsed_ms, "empty_markdown"


def convert_html_document_to_markdown_impl(
    *,
    request: MarkdownConversionRequest,
) -> tuple[str | None, int, str | None]:
    started = time.perf_counter()
    pandoc_path, prepared_html = _prepare_pandoc_conversion(
        html=request.html,
        diag=request.diag,
        ensure_pandoc_ready=request.ensure_pandoc_ready,
        prepare_html=request.prepare_html,
    )
    if pandoc_path is None:
        return _pandoc_unavailable_result(
            diag=request.diag,
            error=prepared_html,
        )
    markdown, stderr, error = request.run_pandoc(
        pandoc_path=pandoc_path,
        html=prepared_html,
    )
    _record_warning_diag(
        diag=request.diag,
        stderr=stderr,
        split_messages=request.split_messages,
        categorize_warning=request.categorize_warning,
    )
    return _finalize_pandoc_result(
        started=started,
        diag=request.diag,
        markdown=markdown,
        error=error,
        max_chars=request.max_chars,
    )
