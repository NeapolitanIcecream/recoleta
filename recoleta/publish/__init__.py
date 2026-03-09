from __future__ import annotations

import os
from pathlib import Path
import shutil
import sys
from typing import Any, Callable

from loguru import logger

from recoleta.publish.item_notes import (
    write_markdown_note,
    write_obsidian_note,
)
from recoleta.publish.telegram_format import (
    build_telegram_message,
    build_telegram_trend_document_caption,
)
from recoleta.publish.trend_notes import (
    write_markdown_run_index,
    write_markdown_stream_index,
    write_markdown_trend_note,
    write_obsidian_trend_note,
)
from recoleta.publish.trend_pdf import (
    TrendPdfRenderInputs,
    TrendPdfRenderResult,
    _prepare_trend_pdf_render_inputs,
    _render_trend_note_pdf_browser_with_dependencies,
    _render_trend_note_pdf_story,
    export_trend_note_pdf_debug_bundle,
)

__all__ = [
    "TrendPdfRenderInputs",
    "TrendPdfRenderResult",
    "build_telegram_message",
    "build_telegram_trend_document_caption",
    "export_trend_note_pdf_debug_bundle",
    "render_trend_note_pdf",
    "render_trend_note_pdf_result",
    "write_markdown_note",
    "write_markdown_run_index",
    "write_markdown_stream_index",
    "write_markdown_trend_note",
    "write_obsidian_note",
    "write_obsidian_trend_note",
]


def _get_playwright_sync_api() -> Callable[[], Any]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Playwright is unavailable for browser-based trend PDF rendering."
        ) from exc
    return sync_playwright


def _trend_pdf_browser_launch_options() -> list[dict[str, Any]]:
    raw_candidates = [
        os.environ.get("RECOLETA_PLAYWRIGHT_EXECUTABLE_PATH"),
        os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH"),
        os.environ.get("GOOGLE_CHROME_BIN"),
        os.environ.get("CHROME_BIN"),
    ]
    if sys.platform == "darwin":
        raw_candidates.extend(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ]
        )
    else:
        raw_candidates.extend(
            [
                shutil.which("google-chrome"),
                shutil.which("chromium"),
                shutil.which("chromium-browser"),
                shutil.which("microsoft-edge"),
                shutil.which("msedge"),
            ]
        )

    launch_options: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in raw_candidates:
        if not candidate:
            continue
        candidate_path = Path(candidate).expanduser()
        if not candidate_path.exists():
            continue
        resolved = str(candidate_path.resolve())
        if resolved in seen:
            continue
        launch_options.append({"headless": True, "executable_path": resolved})
        seen.add(resolved)
    launch_options.append({"headless": True})
    return launch_options


def _render_trend_note_pdf_browser(inputs: TrendPdfRenderInputs) -> None:
    _render_trend_note_pdf_browser_with_dependencies(
        inputs=inputs,
        sync_playwright=_get_playwright_sync_api(),
        launch_options_list=_trend_pdf_browser_launch_options(),
    )


def render_trend_note_pdf_result(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
    debug_dir: Path | None = None,
) -> TrendPdfRenderResult:
    normalized_backend = str(backend or "").strip().lower() or "story"
    if normalized_backend not in {"story", "browser", "auto"}:
        raise ValueError("Trend PDF backend must be one of: story, browser, auto")

    prepared: TrendPdfRenderInputs | None = None
    if normalized_backend in {"browser", "auto"}:
        try:
            prepared = _prepare_trend_pdf_render_inputs(
                markdown_path=markdown_path,
                output_path=output_path,
                backend="browser",
                page_mode=page_mode,
            )
            _render_trend_note_pdf_browser(prepared)
        except Exception as exc:  # noqa: BLE001
            if normalized_backend == "browser":
                raise
            logger.bind(
                module="publish.trends.pdf",
                requested_backend=normalized_backend,
            ).warning(
                "Trend PDF browser render failed, falling back to story error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            prepared = None

    if prepared is None:
        prepared = _prepare_trend_pdf_render_inputs(
            markdown_path=markdown_path,
            output_path=output_path,
            backend="story",
            page_mode="a4",
        )
        _render_trend_note_pdf_story(prepared)

    if debug_dir is not None:
        export_trend_note_pdf_debug_bundle(
            markdown_path=prepared.markdown_path,
            pdf_path=prepared.output_path,
            debug_dir=debug_dir,
            prepared=prepared,
        )
    return TrendPdfRenderResult(path=prepared.output_path, prepared=prepared)


def render_trend_note_pdf(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
    debug_dir: Path | None = None,
) -> Path:
    return render_trend_note_pdf_result(
        markdown_path=markdown_path,
        output_path=output_path,
        backend=backend,
        page_mode=page_mode,
        debug_dir=debug_dir,
    ).path
