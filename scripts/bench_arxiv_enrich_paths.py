from __future__ import annotations

import argparse
import json
import os
import resource
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import httpx
from litellm.utils import token_counter
from rich.console import Console
from rich.table import Table

from recoleta.analyzer import LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.extract import (
    convert_html_document_to_markdown,
    extract_html_document_cleaned,
)
from recoleta.models import Item
from recoleta.pipeline import PipelineService
from recoleta.sources import fetch_arxiv_drafts
from recoleta.storage import Repository
from recoleta.types import ItemDraft

_ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS = (
    "http_404",
    "http_429",
    "http_5xx",
    "http_other",
    "timeout",
    "request_error",
    "missing_url",
    "empty_document",
    "other",
)


@dataclass(frozen=True)
class FrozenDraft:
    source: str
    source_item_id: str
    canonical_url: str
    title: str
    authors: list[str]
    published_at: str | None
    raw_metadata: dict[str, Any]

    @staticmethod
    def from_item_draft(draft: ItemDraft) -> "FrozenDraft":
        published_at: str | None = None
        if isinstance(draft.published_at, datetime):
            published_at = draft.published_at.isoformat()
        return FrozenDraft(
            source=str(draft.source),
            source_item_id=str(draft.source_item_id or ""),
            canonical_url=str(draft.canonical_url),
            title=str(draft.title),
            authors=list(draft.authors or []),
            published_at=published_at,
            raw_metadata=dict(draft.raw_metadata or {}),
        )

    def to_item_draft(self) -> ItemDraft:
        published_at: datetime | None = None
        if self.published_at:
            published_at = datetime.fromisoformat(self.published_at)
        return ItemDraft.from_values(
            source=self.source,
            source_item_id=self.source_item_id,
            canonical_url=self.canonical_url,
            title=self.title,
            authors=self.authors,
            published_at=published_at,
            raw_metadata=self.raw_metadata,
        )


@dataclass(slots=True)
class _BenchCliConfig:
    config_path: Path
    out_dir: Path
    n: int
    candidates: int
    repeat: int
    warmup: int
    concurrency: int
    drafts_path: Path | None


@dataclass(slots=True)
class _MethodRunSnapshot:
    service: PipelineService
    repository: Repository
    items: list[Item]
    run_id: str
    ingest_result: Any
    enrich_summary: dict[str, Any]
    enrich_per_item: list[dict[str, Any]]


@dataclass(slots=True)
class _RunRecordRequest:
    run_id: str
    ingest_ms: int
    enrich_summary: dict[str, Any]
    triage_ms: int
    before: dict[str, Any]
    after: dict[str, Any]


@dataclass(slots=True)
class _MethodIterationRequest:
    base_settings: Settings
    frozen: list[FrozenDraft]
    method: str
    idx: int
    config: _BenchCliConfig


_ENRICH_SUMMARY_KEYS = (
    ("enrich_ms", "pipeline.enrich.duration_ms"),
    ("processed", "pipeline.enrich.processed_total"),
    ("skipped", "pipeline.enrich.skipped_total"),
    ("failed", "pipeline.enrich.failed_total"),
    ("item_duration_ms_total", "pipeline.enrich.item_duration_ms_total"),
    ("sql_queries_total", "pipeline.enrich.db.sql_queries_total"),
    ("sql_commits_total", "pipeline.enrich.db.sql_commits_total"),
    ("html_document_items_total", "pipeline.enrich.arxiv.html_document.items_total"),
    ("fetch_ms_sum", "pipeline.enrich.arxiv.html_document.fetch_ms_sum"),
    ("cleanup_ms_sum", "pipeline.enrich.arxiv.html_document.cleanup_ms_sum"),
    ("pandoc_ms_sum", "pipeline.enrich.arxiv.html_document.pandoc_ms_sum"),
    (
        "pandoc_failed_total",
        "pipeline.enrich.arxiv.html_document.pandoc_failed_total",
    ),
    (
        "pandoc_warning_items_total",
        "pipeline.enrich.arxiv.html_document.pandoc_warning_items_total",
    ),
    (
        "pandoc_warning_count_sum",
        "pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum",
    ),
    (
        "pandoc_warning_tex_math_convert_failed_sum",
        "pipeline.enrich.arxiv.html_document.pandoc_warning_tex_math_convert_failed_sum",
    ),
    (
        "pandoc_math_replaced_sum",
        "pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum",
    ),
    (
        "fallback_to_pdf_total",
        "pipeline.enrich.arxiv.html_document.fallback_to_pdf_total",
    ),
    ("db_read_ms_sum", "pipeline.enrich.arxiv.html_document.db_read_ms_sum"),
    ("db_write_ms_sum", "pipeline.enrich.arxiv.html_document.db_write_ms_sum"),
)

_CONTENT_TYPE_PRIORITY = (
    "html_document",
    "html_document_md",
)


def _json_dump(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _json_load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_token_counter(
    *, model: str, messages: list[dict[str, str]]
) -> tuple[int, str | None]:
    try:
        value = int(token_counter(model=model, messages=messages))
        return value, None
    except Exception as exc:
        fallback_model = "gpt-3.5-turbo"
        try:
            value = int(token_counter(model=fallback_model, messages=messages))
            return (
                value,
                f"token_counter failed for model={model!r}, fell back to {fallback_model!r}: {type(exc).__name__}: {exc}",
            )
        except Exception as fallback_exc:
            raise RuntimeError(
                f"token_counter failed for model={model!r} and fallback model={fallback_model!r}: {fallback_exc}"
            ) from fallback_exc


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    sorted_values = sorted(values)
    idx = max(0, int(round(0.95 * (len(sorted_values) - 1))))
    return float(sorted_values[idx])


def _resource_snapshot() -> dict[str, Any]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    ru_maxrss = int(getattr(usage, "ru_maxrss", 0) or 0)
    # On macOS ru_maxrss is bytes; on Linux it's kilobytes.
    maxrss_unit = "bytes" if sys.platform == "darwin" else "kb"
    maxrss_mb = (
        (ru_maxrss / (1024 * 1024)) if maxrss_unit == "bytes" else (ru_maxrss / 1024)
    )
    return {
        "platform": sys.platform,
        "ru_maxrss": ru_maxrss,
        "ru_maxrss_unit": maxrss_unit,
        "max_rss_mb": float(maxrss_mb),
        "user_cpu_s": float(getattr(usage, "ru_utime", 0.0) or 0.0),
        "sys_cpu_s": float(getattr(usage, "ru_stime", 0.0) or 0.0),
    }


def _probe_candidate_html_md(
    *,
    client: httpx.Client,
    draft: ItemDraft,
    html_url: str,
) -> tuple[bool, dict[str, Any]]:
    debug: dict[str, Any] = {
        "arxiv_id": draft.source_item_id,
        "urls": {"html": html_url},
    }
    try:
        html_resp = client.get(html_url)
        html_resp.raise_for_status()
        html_text = html_resp.text
    except Exception as exc:
        debug["html_error"] = f"{type(exc).__name__}: {exc}"
        return False, debug
    try:
        cleaned_html = extract_html_document_cleaned(html_text)
    except Exception as exc:
        debug["html_extract_error"] = f"{type(exc).__name__}: {exc}"
        return False, debug
    if not (isinstance(cleaned_html, str) and cleaned_html.strip()):
        debug["html_extract_empty"] = True
        return False, debug

    markdown, convert_ms, convert_error = convert_html_document_to_markdown(
        cleaned_html
    )
    debug["pandoc_ms"] = convert_ms
    if convert_error is not None:
        debug["pandoc_error"] = convert_error
        return False, debug
    if not (isinstance(markdown, str) and markdown.strip()):
        debug["pandoc_empty"] = True
        return False, debug

    debug["probe_ok"] = True
    debug["probe_chars"] = {
        "html": len(cleaned_html),
        "html_document_md": len(markdown),
    }
    return True, debug


def _missing_html_url_probe_debug(*, draft: ItemDraft) -> dict[str, Any]:
    return {
        "arxiv_id": draft.source_item_id,
        "probe_ok": False,
        "reason": "missing_url",
    }


def _probe_frozen_draft_candidate(
    *,
    client: httpx.Client,
    draft: ItemDraft,
) -> tuple[FrozenDraft | None, dict[str, Any]]:
    html_url = PipelineService._build_arxiv_html_url(
        canonical_url=draft.canonical_url,
        source_item_id=draft.source_item_id,
    )
    if not html_url:
        return None, _missing_html_url_probe_debug(draft=draft)
    ok, debug = _probe_candidate_html_md(
        client=client,
        draft=draft,
        html_url=html_url,
    )
    if not ok:
        return None, debug
    return FrozenDraft.from_item_draft(draft), debug


def _freeze_drafts(
    *,
    settings: Settings,
    out_dir: Path,
    n: int,
    candidates: int,
) -> tuple[list[FrozenDraft], dict[str, Any]]:
    pull_started = time.perf_counter()
    drafts = fetch_arxiv_drafts(
        queries=list(settings.sources.arxiv.queries),
        max_results_per_run=max(1, int(candidates)),
    )
    pull_ms = int((time.perf_counter() - pull_started) * 1000)

    if not drafts:
        raise RuntimeError(
            "No arXiv drafts fetched. Check SOURCES.arxiv.queries and network."
        )

    timeout = httpx.Timeout(20.0, connect=8.0)
    headers = {"User-Agent": "recoleta/bench/0.1"}
    probe_debug: list[dict[str, Any]] = []
    selected: list[FrozenDraft] = []
    console = Console()
    with httpx.Client(
        timeout=timeout, headers=headers, follow_redirects=True
    ) as client:
        for idx, draft in enumerate(drafts, start=1):
            if len(selected) >= n:
                break
            if str(draft.source).strip().lower() != "arxiv":
                continue

            console.print(
                f"[cyan]probe[/cyan] {idx}/{len(drafts)} arxiv_id={draft.source_item_id}"
            )
            selected_draft, debug = _probe_frozen_draft_candidate(
                client=client,
                draft=draft,
            )
            probe_debug.append(debug)
            if selected_draft is not None:
                selected.append(selected_draft)
                console.print(
                    f"[green]selected[/green] {draft.source_item_id} ({len(selected)}/{n})"
                )

    if len(selected) < n:
        _json_dump(out_dir / "drafts-probe-debug.json", probe_debug)
        raise RuntimeError(
            f"Unable to select {n} drafts that support html_document -> html_document_md conversion. "
            f"Selected={len(selected)}. See drafts-probe-debug.json for details."
        )

    _json_dump(out_dir / "drafts.json", [d.__dict__ for d in selected])
    meta = {
        "pull_drafts_ms": pull_ms,
        "candidates_requested": candidates,
        "candidates_received": len(drafts),
        "selected": len(selected),
        "probe_debug_path": str(out_dir / "drafts-probe-debug.json")
        if (out_dir / "drafts-probe-debug.json").exists()
        else None,
    }
    return selected, meta


def _build_settings_for_method(
    *,
    base: Settings,
    method: str,
    db_path: Path,
    html_document_max_concurrency: int,
) -> Settings:
    payload = base.model_dump(mode="python")
    payload["recoleta_db_path"] = str(db_path)
    payload["triage_enabled"] = False
    sources = dict(payload.get("sources") or {})
    normalized_sources: dict[str, Any] = {}
    for source_name, source_cfg in sources.items():
        if not isinstance(source_cfg, dict):
            continue
        if bool(source_cfg.get("enabled")) is not True:
            continue
        normalized_sources[str(source_name)] = dict(source_cfg)
    sources = normalized_sources
    arxiv_cfg = dict((sources.get("arxiv") or {}))
    arxiv_cfg["enrich_method"] = method
    arxiv_cfg["enrich_failure_mode"] = "strict"
    arxiv_cfg["html_document_max_concurrency"] = int(html_document_max_concurrency)
    sources["arxiv"] = arxiv_cfg
    payload["sources"] = sources
    return Settings.model_validate(payload)  # pyright: ignore[reportCallIssue]


def _query_items_for_frozen_drafts(
    *, repo: Repository, frozen: list[FrozenDraft]
) -> list[Item]:
    from sqlmodel import Session, select  # local import to keep script fast

    ids = {d.source_item_id for d in frozen if d.source_item_id}
    with Session(repo.engine) as session:
        statement = select(Item).where(Item.source == "arxiv")
        items = list(session.exec(statement))
    filtered: list[Item] = []
    for item in items:
        if (item.source_item_id or "") in ids:
            filtered.append(item)
    return filtered


def _metric_int(by_name: dict[str, float], key: str) -> int:
    return int(by_name.get(key) or 0)


def _fallback_reason_totals(by_name: dict[str, float]) -> dict[str, int]:
    return {
        bucket: _metric_int(
            by_name,
            f"pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.{bucket}_total",
        )
        for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS
    }


def _summarize_enrich_metrics(by_name: dict[str, float]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        output_key: _metric_int(by_name, metric_name)
        for output_key, metric_name in _ENRICH_SUMMARY_KEYS
    }
    summary["fallback_to_pdf_by_reason"] = _fallback_reason_totals(by_name)
    return summary


def _enrich_with_timing(
    *,
    service: PipelineService,
    run_id: str,
    items: list[Item],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    from sqlmodel import Session, select  # local import to keep script fast

    from recoleta.models import Metric

    started = time.perf_counter()
    service.enrich(run_id=run_id, limit=max(1, len(items)))
    enrich_wall_ms = int((time.perf_counter() - started) * 1000)

    with Session(service.repository.engine) as session:
        statement = (
            select(Metric).where(Metric.run_id == run_id).order_by(cast(Any, Metric.id))
        )
        metrics = list(session.exec(statement))

    by_name: dict[str, float] = {m.name: float(m.value) for m in metrics}
    summary = _summarize_enrich_metrics(by_name)
    summary["enrich_wall_ms"] = enrich_wall_ms
    if not int(summary.get("enrich_ms") or 0):
        summary["enrich_ms"] = enrich_wall_ms

    per_item: list[dict[str, Any]] = []
    for item in items:
        if item.id is None:
            continue
        per_item.append(
            {
                "item_id": int(item.id),
                "arxiv_id": PipelineService._extract_arxiv_identifier(  # noqa: SLF001
                    canonical_url=item.canonical_url,
                    source_item_id=item.source_item_id,
                ),
                "enrich_item_ms": None,
            }
        )
    return summary, per_item


def _content_text_for_item(
    *,
    service: PipelineService,
    item_id: int,
    content_type: str,
) -> str:
    content = service.repository.get_latest_content(
        item_id=item_id,
        content_type=content_type,
    )
    return (getattr(content, "text", None) or "").strip() if content is not None else ""


def _prompt_token_inputs(
    *,
    analyzer: LiteLLMAnalyzer,
    item: Item,
    text: str,
    topics: list[str],
) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": analyzer._build_system_message()},  # noqa: SLF001
        {
            "role": "user",
            "content": analyzer._build_prompt(  # noqa: SLF001
                title=item.title,
                canonical_url=item.canonical_url,
                user_topics=topics,
                content=text,
            ),
        },
    ]


def _missing_content_token_row(
    *,
    item_id: int,
    arxiv_id: str | None,
    content_type: str,
) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "arxiv_id": arxiv_id,
        "status": "missing_content",
        "content_type": content_type,
    }


def _token_summary_payload(
    *,
    content_type: str,
    full_tokens_values: list[int],
    prompt_tokens_values: list[int],
    warnings: list[str],
) -> dict[str, Any]:
    full_token_floats = [float(value) for value in full_tokens_values]
    prompt_token_floats = [float(value) for value in prompt_tokens_values]
    return {
        "content_type": content_type,
        "full_tokens_sum": int(sum(full_tokens_values)),
        "full_tokens_median": int(_median(full_token_floats) or 0),
        "full_tokens_p95": int(_p95(full_token_floats) or 0),
        "prompt_tokens_sum": int(sum(prompt_tokens_values)),
        "prompt_tokens_median": int(_median(prompt_token_floats) or 0),
        "prompt_tokens_p95": int(_p95(prompt_token_floats) or 0),
        "token_counter_warnings": list(dict.fromkeys(warnings))[:10],
    }


def _compute_tokens(
    *,
    service: PipelineService,
    items: list[Item],
    content_type: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    analyzer = LiteLLMAnalyzer(
        model=service.settings.llm_model,
        output_language=service.settings.llm_output_language,
    )
    warnings: list[str] = []

    per_item: list[dict[str, Any]] = []
    full_tokens_values: list[int] = []
    prompt_tokens_values: list[int] = []

    for item in items:
        if item.id is None:
            continue
        item_id = int(item.id)
        arxiv_id = PipelineService._extract_arxiv_identifier(
            canonical_url=item.canonical_url,
            source_item_id=item.source_item_id,
        )
        text = _content_text_for_item(
            service=service,
            item_id=item_id,
            content_type=content_type,
        )
        if not text:
            per_item.append(
                _missing_content_token_row(
                    item_id=item_id,
                    arxiv_id=arxiv_id,
                    content_type=content_type,
                )
            )
            continue

        full_tok, warn1 = _safe_token_counter(
            model=service.settings.llm_model,
            messages=[{"role": "user", "content": text}],
        )
        if warn1:
            warnings.append(warn1)
        prompt_tok, warn2 = _safe_token_counter(
            model=service.settings.llm_model,
            messages=_prompt_token_inputs(
                analyzer=analyzer,
                item=item,
                text=text,
                topics=list(service.settings.topics),
            ),
        )
        if warn2:
            warnings.append(warn2)

        full_tokens_values.append(full_tok)
        prompt_tokens_values.append(prompt_tok)
        per_item.append(
            {
                "item_id": item_id,
                "arxiv_id": arxiv_id,
                "status": "ok",
                "content_type": content_type,
                "content_chars": len(text),
                "full_tokens": full_tok,
                "prompt_tokens": prompt_tok,
            }
        )

    summary = _token_summary_payload(
        content_type=content_type,
        full_tokens_values=full_tokens_values,
        prompt_tokens_values=prompt_tokens_values,
        warnings=warnings,
    )
    return summary, per_item


def _append_report_pairs(
    lines: list[str],
    *,
    values: list[tuple[str, Any]],
) -> None:
    for label, value in values:
        lines.append(f"- {label}: {value}")


def _append_duration_section(
    lines: list[str], *, method_results: dict[str, Any]
) -> None:
    lines.append("### durations\n")
    durations = method_results.get("durations") or {}
    _append_report_pairs(
        lines,
        values=[
            ("ingest_ms_median", durations.get("ingest_ms_median")),
            ("ingest_ms_p95", durations.get("ingest_ms_p95")),
            ("enrich_ms_median", durations.get("enrich_ms_median")),
            ("enrich_ms_p95", durations.get("enrich_ms_p95")),
            ("triage_ms_median", durations.get("triage_ms_median")),
            ("triage_ms_p95", durations.get("triage_ms_p95")),
            ("pipeline_ms_median", durations.get("pipeline_ms_median")),
            ("pipeline_ms_p95", durations.get("pipeline_ms_p95")),
        ],
    )
    lines.append("")


def _append_diagnostics_section(
    lines: list[str],
    *,
    method_results: dict[str, Any],
) -> None:
    lines.append("### diagnostics\n")
    enrich_result = method_results.get("enrich_result") or {}
    _append_report_pairs(
        lines,
        values=[
            (
                "html_document_items_total",
                enrich_result.get("html_document_items_total"),
            ),
            ("pandoc_failed_total", enrich_result.get("pandoc_failed_total")),
            (
                "pandoc_warning_items_total",
                enrich_result.get("pandoc_warning_items_total"),
            ),
            (
                "pandoc_warning_count_sum",
                enrich_result.get("pandoc_warning_count_sum"),
            ),
            (
                "pandoc_warning_tex_math_convert_failed_sum",
                enrich_result.get("pandoc_warning_tex_math_convert_failed_sum"),
            ),
            ("pandoc_math_replaced_sum", enrich_result.get("pandoc_math_replaced_sum")),
            ("fallback_to_pdf_total", enrich_result.get("fallback_to_pdf_total")),
        ],
    )
    fallback_by_reason = enrich_result.get("fallback_to_pdf_by_reason") or {}
    for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS:
        if int(fallback_by_reason.get(bucket) or 0) <= 0:
            continue
        lines.append(
            f"- fallback_to_pdf_reason.{bucket}_total: {fallback_by_reason.get(bucket)}"
        )
    lines.append("")


def _append_token_summary_section(
    lines: list[str],
    *,
    title: str,
    token_summary: dict[str, Any],
) -> None:
    lines.append(f"#### {title}\n")
    _append_report_pairs(
        lines,
        values=[
            ("full_tokens_sum", token_summary.get("full_tokens_sum")),
            ("full_tokens_median", token_summary.get("full_tokens_median")),
            ("full_tokens_p95", token_summary.get("full_tokens_p95")),
            ("prompt_tokens_sum", token_summary.get("prompt_tokens_sum")),
            ("prompt_tokens_median", token_summary.get("prompt_tokens_median")),
            ("prompt_tokens_p95", token_summary.get("prompt_tokens_p95")),
        ],
    )
    lines.append("")


def _append_tokens_section(lines: list[str], *, method_results: dict[str, Any]) -> None:
    lines.append("### tokens\n")
    tokens = method_results.get("tokens") or {}
    html_tokens = tokens.get("html_document") or {}
    md_tokens = tokens.get("html_document_md") or {}
    _append_token_summary_section(
        lines,
        title="html_document (cleaned HTML)",
        token_summary=html_tokens,
    )
    _append_token_summary_section(
        lines,
        title="html_document_md (pandoc Markdown)",
        token_summary=md_tokens,
    )
    delta = tokens.get("delta") or {}
    if delta:
        lines.append("#### delta (md - html)\n")
        _append_report_pairs(
            lines,
            values=[
                ("full_tokens_sum_delta", delta.get("full_tokens_sum_delta")),
                ("prompt_tokens_sum_delta", delta.get("prompt_tokens_sum_delta")),
            ],
        )
    warnings = (md_tokens.get("token_counter_warnings") or []) + (
        html_tokens.get("token_counter_warnings") or []
    )
    if warnings:
        lines.append("")
        lines.append("#### token_counter warnings\n")
        for warning in warnings:
            lines.append(f"- {warning}")
    lines.append("")


def _append_per_item_section(
    lines: list[str], *, method_results: dict[str, Any]
) -> None:
    lines.append("### per-item\n")
    per_items = method_results.get("per_item") or []
    for item in per_items:
        if item.get("status") != "ok":
            lines.append(
                f"- {item.get('arxiv_id') or item.get('item_id')}: status={item.get('status')}"
            )
            continue
        lines.append(
            f"- {item.get('arxiv_id')}: "
            f"html_full={item.get('html_full_tokens')} html_prompt={item.get('html_prompt_tokens')} | "
            f"md_full={item.get('md_full_tokens')} md_prompt={item.get('md_prompt_tokens')} | "
            f"enrich_item_ms={item.get('enrich_item_ms')}"
        )
    lines.append("")


def _render_report_md(*, results: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# arXiv enrich path benchmark\n")
    generated_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    _append_report_pairs(
        lines,
        values=[
            ("generated_at", generated_at),
            ("config_path", results.get("config_path")),
            ("selected_n", results.get("selected_n")),
            ("candidates_requested", results.get("candidates_requested")),
            ("pull_drafts_ms", results.get("pull_drafts_ms")),
            ("repeat", results.get("repeat")),
            ("warmup", results.get("warmup")),
            ("concurrency", results.get("concurrency")),
        ],
    )
    lines.append("")

    for method in ("html_document",):
        r = (results.get("methods") or {}).get(method) or {}
        lines.append(f"## {method}\n")
        _append_duration_section(lines, method_results=r)
        _append_diagnostics_section(lines, method_results=r)
        _append_tokens_section(lines, method_results=r)
        _append_per_item_section(lines, method_results=r)

    return "\n".join(lines).strip() + "\n"


def _validated_int(
    *,
    label: str,
    value: Any,
    minimum: int,
    maximum: int,
) -> int:
    normalized = int(value)
    if normalized < minimum or normalized > maximum:
        raise ValueError(f"{label} must be in [{minimum},{maximum}]")
    return normalized


def _build_cli_config(args: argparse.Namespace) -> _BenchCliConfig:
    config_path = Path(str(args.config)).expanduser().resolve()
    out_dir = Path(str(args.out)).expanduser().resolve()
    return _BenchCliConfig(
        config_path=config_path,
        out_dir=out_dir,
        n=_validated_int(label="--n", value=args.n, minimum=1, maximum=50),
        candidates=max(5, int(args.candidates)),
        repeat=_validated_int(
            label="--repeat", value=args.repeat, minimum=1, maximum=50
        ),
        warmup=_validated_int(
            label="--warmup", value=args.warmup, minimum=0, maximum=20
        ),
        concurrency=_validated_int(
            label="--concurrency",
            value=args.concurrency,
            minimum=1,
            maximum=32,
        ),
        drafts_path=(
            Path(str(args.drafts)).expanduser().resolve() if args.drafts else None
        ),
    )


def _load_base_settings(*, config: _BenchCliConfig) -> Settings:
    os.environ["RECOLETA_CONFIG_PATH"] = str(config.config_path)
    return Settings()  # pyright: ignore[reportCallIssue]


def _load_existing_frozen_drafts(
    *,
    drafts_path: Path,
    out_dir: Path,
    n: int,
) -> tuple[list[FrozenDraft], dict[str, Any]]:
    loaded = _json_load(drafts_path)
    if not isinstance(loaded, list) or not loaded:
        raise ValueError(f"--drafts must point to a non-empty JSON list: {drafts_path}")
    frozen = [FrozenDraft(**cast(dict[str, Any], item)) for item in loaded]  # type: ignore[arg-type]
    if len(frozen) < n:
        raise ValueError(
            f"--drafts has only {len(frozen)} items, but --n={n} was requested."
        )
    selected = frozen[:n]
    _json_dump(out_dir / "drafts.json", [draft.__dict__ for draft in selected])
    return selected, {
        "pull_drafts_ms": None,
        "candidates_requested": None,
        "candidates_received": None,
        "selected": len(selected),
    }


def _resolve_frozen_drafts(
    *,
    config: _BenchCliConfig,
    settings: Settings,
) -> tuple[list[FrozenDraft], dict[str, Any]]:
    if config.drafts_path is not None:
        return _load_existing_frozen_drafts(
            drafts_path=config.drafts_path,
            out_dir=config.out_dir,
            n=config.n,
        )
    return _freeze_drafts(
        settings=settings,
        out_dir=config.out_dir,
        n=config.n,
        candidates=config.candidates,
    )


def _resource_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "before": before,
        "after": after,
        "cpu_user_s_delta": float(after.get("user_cpu_s") or 0.0)
        - float(before.get("user_cpu_s") or 0.0),
        "cpu_sys_s_delta": float(after.get("sys_cpu_s") or 0.0)
        - float(before.get("sys_cpu_s") or 0.0),
        "max_rss_mb": float(after.get("max_rss_mb") or 0.0),
    }


def _run_record(*, request: _RunRecordRequest) -> dict[str, Any]:
    enrich_ms = int(request.enrich_summary.get("enrich_ms") or 0)
    return {
        "run_id": request.run_id,
        "ingest_ms": request.ingest_ms,
        "enrich_ms": enrich_ms,
        "triage_ms": request.triage_ms,
        "pipeline_ms": int(request.ingest_ms + enrich_ms + request.triage_ms),
        "enrich": request.enrich_summary,
        "resources": _resource_delta(request.before, request.after),
    }


def _run_method_iteration(
    *,
    request: _MethodIterationRequest,
) -> tuple[dict[str, Any], _MethodRunSnapshot]:
    db_path = request.config.out_dir / f"recoleta-bench-{request.method}.db"
    if db_path.exists():
        db_path.unlink()
    settings = _build_settings_for_method(
        base=request.base_settings,
        method=request.method,
        db_path=db_path,
        html_document_max_concurrency=request.config.concurrency,
    )
    repository = Repository(
        db_path=settings.recoleta_db_path,
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = PipelineService(settings=settings, repository=repository)

    run_id = f"bench-{request.method}-{int(time.time())}-{request.idx}"
    before = _resource_snapshot()
    ingest_started = time.perf_counter()
    ingest_result = service.ingest(
        run_id=run_id,
        drafts=[draft.to_item_draft() for draft in request.frozen],
    )
    ingest_ms = int((time.perf_counter() - ingest_started) * 1000)

    items = _query_items_for_frozen_drafts(repo=repository, frozen=request.frozen)
    enrich_summary, enrich_per_item = _enrich_with_timing(
        service=service,
        run_id=run_id,
        items=items,
    )

    triage_started = time.perf_counter()
    service.triage(run_id=run_id, limit=max(1, len(items)))
    triage_ms = int((time.perf_counter() - triage_started) * 1000)
    after = _resource_snapshot()

    return _run_record(
        request=_RunRecordRequest(
            run_id=run_id,
            ingest_ms=ingest_ms,
            enrich_summary=enrich_summary,
            triage_ms=triage_ms,
            before=before,
            after=after,
        )
    ), _MethodRunSnapshot(
        service=service,
        repository=repository,
        items=items,
        run_id=run_id,
        ingest_result=ingest_result,
        enrich_summary=enrich_summary,
        enrich_per_item=enrich_per_item,
    )


def _duration_summary(runs: list[dict[str, Any]]) -> dict[str, float | None]:
    ingest_values = [float(run.get("ingest_ms") or 0) for run in runs]
    enrich_values = [float(run.get("enrich_ms") or 0) for run in runs]
    triage_values = [float(run.get("triage_ms") or 0) for run in runs]
    pipeline_values = [float(run.get("pipeline_ms") or 0) for run in runs]
    return {
        "ingest_ms_median": _median(ingest_values),
        "ingest_ms_p95": _p95(ingest_values),
        "enrich_ms_median": _median(enrich_values),
        "enrich_ms_p95": _p95(enrich_values),
        "triage_ms_median": _median(triage_values),
        "triage_ms_p95": _p95(triage_values),
        "pipeline_ms_median": _median(pipeline_values),
        "pipeline_ms_p95": _p95(pipeline_values),
    }


def _merge_per_item_tokens(
    *,
    items: list[Item],
    enrich_per_item: list[dict[str, Any]],
    html_tokens_per_item: list[dict[str, Any]],
    md_tokens_per_item: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    per_item_by_id = {int(row["item_id"]): dict(row) for row in enrich_per_item}
    html_by_id = {int(row["item_id"]): dict(row) for row in html_tokens_per_item}
    md_by_id = {int(row["item_id"]): dict(row) for row in md_tokens_per_item}
    merged_per_item: list[dict[str, Any]] = []
    for item in items:
        if item.id is None:
            continue
        item_id = int(item.id)
        html_part = html_by_id.get(item_id) or {}
        md_part = md_by_id.get(item_id) or {}
        merged_per_item.append(
            {
                "item_id": item_id,
                "arxiv_id": PipelineService._extract_arxiv_identifier(  # noqa: SLF001
                    canonical_url=item.canonical_url,
                    source_item_id=item.source_item_id,
                ),
                "status": (
                    "ok"
                    if (
                        html_part.get("status") == "ok"
                        and md_part.get("status") == "ok"
                    )
                    else "partial"
                ),
                "html_full_tokens": html_part.get("full_tokens"),
                "html_prompt_tokens": html_part.get("prompt_tokens"),
                "md_full_tokens": md_part.get("full_tokens"),
                "md_prompt_tokens": md_part.get("prompt_tokens"),
                "enrich_item_ms": (per_item_by_id.get(item_id) or {}).get(
                    "enrich_item_ms"
                ),
            }
        )
    return merged_per_item


def _token_results(
    snapshot: _MethodRunSnapshot,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    html_tokens_summary, html_tokens_per_item = _compute_tokens(
        service=snapshot.service,
        items=snapshot.items,
        content_type=_CONTENT_TYPE_PRIORITY[0],
    )
    md_tokens_summary, md_tokens_per_item = _compute_tokens(
        service=snapshot.service,
        items=snapshot.items,
        content_type=_CONTENT_TYPE_PRIORITY[1],
    )
    return {
        "html_document": html_tokens_summary,
        "html_document_md": md_tokens_summary,
        "delta": {
            "full_tokens_sum_delta": int(
                (md_tokens_summary.get("full_tokens_sum") or 0)
                - (html_tokens_summary.get("full_tokens_sum") or 0)
            ),
            "prompt_tokens_sum_delta": int(
                (md_tokens_summary.get("prompt_tokens_sum") or 0)
                - (html_tokens_summary.get("prompt_tokens_sum") or 0)
            ),
        },
    }, _merge_per_item_tokens(
        items=snapshot.items,
        enrich_per_item=snapshot.enrich_per_item,
        html_tokens_per_item=html_tokens_per_item,
        md_tokens_per_item=md_tokens_per_item,
    )


def _run_method_benchmark(
    *,
    base_settings: Settings,
    frozen: list[FrozenDraft],
    method: str,
    config: _BenchCliConfig,
) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    last_snapshot: _MethodRunSnapshot | None = None
    for idx in range(config.warmup + config.repeat):
        run_record, snapshot = _run_method_iteration(
            request=_MethodIterationRequest(
                base_settings=base_settings,
                frozen=frozen,
                method=method,
                idx=idx,
                config=config,
            )
        )
        if idx >= config.warmup:
            runs.append(run_record)
        last_snapshot = snapshot
    if last_snapshot is None:
        raise RuntimeError("benchmark did not produce a final run")

    tokens, per_item = _token_results(last_snapshot)
    return {
        "runs": runs,
        "durations": _duration_summary(runs),
        "run_id": last_snapshot.run_id,
        "db_path": str(config.out_dir / f"recoleta-bench-{method}.db"),
        "ingest_result": {
            "inserted": getattr(last_snapshot.ingest_result, "inserted", None),
            "updated": getattr(last_snapshot.ingest_result, "updated", None),
            "failed": getattr(last_snapshot.ingest_result, "failed", None),
        },
        "enrich_result": last_snapshot.enrich_summary,
        "tokens": tokens,
        "per_item": per_item,
    }


def _initial_results(
    *,
    config: _BenchCliConfig,
    freeze_meta: dict[str, Any],
) -> dict[str, Any]:
    return {
        "config_path": str(config.config_path),
        "selected_n": config.n,
        "candidates_requested": freeze_meta.get("candidates_requested"),
        "pull_drafts_ms": freeze_meta.get("pull_drafts_ms"),
        "repeat": config.repeat,
        "warmup": config.warmup,
        "concurrency": config.concurrency,
        "methods": {},
    }


def _print_summary_table(*, console: Console, results: dict[str, Any]) -> None:
    table = Table(title="arXiv enrich benchmark summary")
    table.add_column("method", style="bold")
    table.add_column("ingest_ms", justify="right")
    table.add_column("enrich_ms", justify="right")
    table.add_column("pandoc_warns", justify="right")
    table.add_column("pdf_fallbacks", justify="right")
    table.add_column("html_full_sum", justify="right")
    table.add_column("md_full_sum", justify="right")
    table.add_column("md_minus_html_full", justify="right")
    for method in ("html_document",):
        method_results = results["methods"][method]
        html_sum = (
            (method_results.get("tokens") or {}).get("html_document") or {}
        ).get("full_tokens_sum")
        md_sum = (
            (method_results.get("tokens") or {}).get("html_document_md") or {}
        ).get("full_tokens_sum")
        delta = ((method_results.get("tokens") or {}).get("delta") or {}).get(
            "full_tokens_sum_delta"
        )
        enrich_result = method_results.get("enrich_result") or {}
        table.add_row(
            method,
            str((method_results.get("durations") or {}).get("ingest_ms_median")),
            str((method_results.get("durations") or {}).get("enrich_ms_median")),
            str(enrich_result.get("pandoc_warning_count_sum")),
            str(enrich_result.get("fallback_to_pdf_total")),
            str(html_sum),
            str(md_sum),
            str(delta),
        )
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark arXiv html_document_md route (html_document -> html_document_md)."
    )
    parser.add_argument("--config", required=True, help="Path to recoleta.yaml")
    parser.add_argument(
        "--n",
        type=int,
        default=20,
        help="Number of arXiv sources to benchmark (<= 50 recommended).",
    )
    parser.add_argument(
        "--candidates",
        type=int,
        default=20,
        help="Max arXiv results per query used for selecting candidates.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=5,
        help="Number of benchmark repetitions (recorded).",
    )
    parser.add_argument(
        "--warmup", type=int, default=1, help="Number of warm-up runs (not recorded)."
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="html_document_max_concurrency used by PipelineService.enrich.",
    )
    parser.add_argument(
        "--drafts",
        default=None,
        help="Optional path to an existing drafts.json produced by a previous run. When set, skips arXiv API draft fetching.",
    )
    parser.add_argument(
        "--out", default=".", help="Output directory for drafts.json and bench results."
    )
    config = _build_cli_config(parser.parse_args())
    console = Console()
    config.out_dir.mkdir(parents=True, exist_ok=True)

    base_settings = _load_base_settings(config=config)
    frozen, freeze_meta = _resolve_frozen_drafts(config=config, settings=base_settings)
    results = _initial_results(config=config, freeze_meta=freeze_meta)
    for method in ("html_document",):
        results["methods"][method] = _run_method_benchmark(
            base_settings=base_settings,
            frozen=frozen,
            method=method,
            config=config,
        )

    _json_dump(config.out_dir / "bench-results.json", results)
    (config.out_dir / "bench-results.md").write_text(
        _render_report_md(results=results),
        encoding="utf-8",
    )
    _print_summary_table(console=console, results=results)
    console.print(f"[green]wrote[/green] {config.out_dir / 'drafts.json'}")
    console.print(f"[green]wrote[/green] {config.out_dir / 'bench-results.json'}")
    console.print(f"[green]wrote[/green] {config.out_dir / 'bench-results.md'}")


if __name__ == "__main__":
    main()
