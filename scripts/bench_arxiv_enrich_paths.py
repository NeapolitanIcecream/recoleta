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

            html_url = PipelineService._build_arxiv_html_url(
                canonical_url=draft.canonical_url,
                source_item_id=draft.source_item_id,
            )
            if not html_url:
                probe_debug.append(
                    {
                        "arxiv_id": draft.source_item_id,
                        "probe_ok": False,
                        "reason": "missing_url",
                    }
                )
                continue

            console.print(
                f"[cyan]probe[/cyan] {idx}/{len(drafts)} arxiv_id={draft.source_item_id}"
            )
            ok, dbg = _probe_candidate_html_md(
                client=client,
                draft=draft,
                html_url=html_url,
            )
            probe_debug.append(dbg)
            if ok:
                selected.append(FrozenDraft.from_item_draft(draft))
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

    summary = {
        "enrich_wall_ms": enrich_wall_ms,
        "enrich_ms": int(by_name.get("pipeline.enrich.duration_ms") or enrich_wall_ms),
        "processed": int(by_name.get("pipeline.enrich.processed_total") or 0),
        "skipped": int(by_name.get("pipeline.enrich.skipped_total") or 0),
        "failed": int(by_name.get("pipeline.enrich.failed_total") or 0),
        "item_duration_ms_total": int(
            by_name.get("pipeline.enrich.item_duration_ms_total") or 0
        ),
        "sql_queries_total": int(
            by_name.get("pipeline.enrich.db.sql_queries_total") or 0
        ),
        "sql_commits_total": int(
            by_name.get("pipeline.enrich.db.sql_commits_total") or 0
        ),
        "fetch_ms_sum": int(
            by_name.get("pipeline.enrich.arxiv.html_document.fetch_ms_sum") or 0
        ),
        "cleanup_ms_sum": int(
            by_name.get("pipeline.enrich.arxiv.html_document.cleanup_ms_sum") or 0
        ),
        "pandoc_ms_sum": int(
            by_name.get("pipeline.enrich.arxiv.html_document.pandoc_ms_sum") or 0
        ),
        "db_read_ms_sum": int(
            by_name.get("pipeline.enrich.arxiv.html_document.db_read_ms_sum") or 0
        ),
        "db_write_ms_sum": int(
            by_name.get("pipeline.enrich.arxiv.html_document.db_write_ms_sum") or 0
        ),
    }

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
        content = service.repository.get_latest_content(
            item_id=item_id, content_type=content_type
        )
        text = (
            (getattr(content, "text", None) or "").strip()
            if content is not None
            else ""
        )
        if not text:
            per_item.append(
                {
                    "item_id": item_id,
                    "arxiv_id": arxiv_id,
                    "status": "missing_content",
                    "content_type": content_type,
                }
            )
            continue

        full_tok, warn1 = _safe_token_counter(
            model=service.settings.llm_model,
            messages=[{"role": "user", "content": text}],
        )
        if warn1:
            warnings.append(warn1)
        system_msg = analyzer._build_system_message()  # noqa: SLF001
        prompt = analyzer._build_prompt(  # noqa: SLF001
            title=item.title,
            canonical_url=item.canonical_url,
            user_topics=list(service.settings.topics),
            content=text,
        )
        prompt_tok, warn2 = _safe_token_counter(
            model=service.settings.llm_model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
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

    summary = {
        "content_type": content_type,
        "full_tokens_sum": int(sum(full_tokens_values)),
        "full_tokens_median": int(_median([float(v) for v in full_tokens_values]) or 0),
        "full_tokens_p95": int(_p95([float(v) for v in full_tokens_values]) or 0),
        "prompt_tokens_sum": int(sum(prompt_tokens_values)),
        "prompt_tokens_median": int(
            _median([float(v) for v in prompt_tokens_values]) or 0
        ),
        "prompt_tokens_p95": int(_p95([float(v) for v in prompt_tokens_values]) or 0),
        "token_counter_warnings": list(dict.fromkeys(warnings))[:10],
    }
    return summary, per_item


def _render_report_md(*, results: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# arXiv enrich path benchmark\n")
    generated_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    lines.append(f"- generated_at: {generated_at}")
    lines.append(f"- config_path: {results.get('config_path')}")
    lines.append(f"- selected_n: {results.get('selected_n')}")
    lines.append(f"- candidates_requested: {results.get('candidates_requested')}")
    lines.append(f"- pull_drafts_ms: {results.get('pull_drafts_ms')}")
    lines.append(f"- repeat: {results.get('repeat')}")
    lines.append(f"- warmup: {results.get('warmup')}")
    lines.append(f"- concurrency: {results.get('concurrency')}")
    lines.append("")

    for method in ("html_document",):
        r = (results.get("methods") or {}).get(method) or {}
        lines.append(f"## {method}\n")
        lines.append("### durations\n")
        durations = r.get("durations") or {}
        lines.append(f"- ingest_ms_median: {durations.get('ingest_ms_median')}")
        lines.append(f"- ingest_ms_p95: {durations.get('ingest_ms_p95')}")
        lines.append(f"- enrich_ms_median: {durations.get('enrich_ms_median')}")
        lines.append(f"- enrich_ms_p95: {durations.get('enrich_ms_p95')}")
        lines.append(f"- triage_ms_median: {durations.get('triage_ms_median')}")
        lines.append(f"- triage_ms_p95: {durations.get('triage_ms_p95')}")
        lines.append(f"- pipeline_ms_median: {durations.get('pipeline_ms_median')}")
        lines.append(f"- pipeline_ms_p95: {durations.get('pipeline_ms_p95')}")
        lines.append("")

        lines.append("### tokens\n")
        tokens = r.get("tokens") or {}
        html_tokens = tokens.get("html_document") or {}
        md_tokens = tokens.get("html_document_md") or {}
        lines.append("#### html_document (cleaned HTML)\n")
        lines.append(f"- full_tokens_sum: {html_tokens.get('full_tokens_sum')}")
        lines.append(f"- full_tokens_median: {html_tokens.get('full_tokens_median')}")
        lines.append(f"- full_tokens_p95: {html_tokens.get('full_tokens_p95')}")
        lines.append(f"- prompt_tokens_sum: {html_tokens.get('prompt_tokens_sum')}")
        lines.append(
            f"- prompt_tokens_median: {html_tokens.get('prompt_tokens_median')}"
        )
        lines.append(f"- prompt_tokens_p95: {html_tokens.get('prompt_tokens_p95')}")
        lines.append("")
        lines.append("#### html_document_md (pandoc Markdown)\n")
        lines.append(f"- full_tokens_sum: {md_tokens.get('full_tokens_sum')}")
        lines.append(f"- full_tokens_median: {md_tokens.get('full_tokens_median')}")
        lines.append(f"- full_tokens_p95: {md_tokens.get('full_tokens_p95')}")
        lines.append(f"- prompt_tokens_sum: {md_tokens.get('prompt_tokens_sum')}")
        lines.append(f"- prompt_tokens_median: {md_tokens.get('prompt_tokens_median')}")
        lines.append(f"- prompt_tokens_p95: {md_tokens.get('prompt_tokens_p95')}")
        lines.append("")
        delta = tokens.get("delta") or {}
        if delta:
            lines.append("#### delta (md - html)\n")
            lines.append(
                f"- full_tokens_sum_delta: {delta.get('full_tokens_sum_delta')}"
            )
            lines.append(
                f"- prompt_tokens_sum_delta: {delta.get('prompt_tokens_sum_delta')}"
            )
        warnings = (md_tokens.get("token_counter_warnings") or []) + (
            html_tokens.get("token_counter_warnings") or []
        )
        if warnings:
            lines.append("")
            lines.append("#### token_counter warnings\n")
            for w in warnings:
                lines.append(f"- {w}")
        lines.append("")

        lines.append("### per-item\n")
        per_items = r.get("per_item") or []
        for it in per_items:
            if it.get("status") != "ok":
                lines.append(
                    f"- {it.get('arxiv_id') or it.get('item_id')}: status={it.get('status')}"
                )
                continue
            lines.append(
                f"- {it.get('arxiv_id')}: "
                f"html_full={it.get('html_full_tokens')} html_prompt={it.get('html_prompt_tokens')} | "
                f"md_full={it.get('md_full_tokens')} md_prompt={it.get('md_prompt_tokens')} | "
                f"enrich_item_ms={it.get('enrich_item_ms')}"
            )
        lines.append("")

    return "\n".join(lines).strip() + "\n"


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
    args = parser.parse_args()

    console = Console()
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    os.environ["RECOLETA_CONFIG_PATH"] = str(Path(args.config).expanduser().resolve())
    base_settings = Settings()  # pyright: ignore[reportCallIssue]

    n = int(args.n)
    if n <= 0 or n > 50:
        raise ValueError("--n must be in [1,50]")
    repeat = int(args.repeat)
    warmup = int(args.warmup)
    if repeat <= 0 or repeat > 50:
        raise ValueError("--repeat must be in [1,50]")
    if warmup < 0 or warmup > 20:
        raise ValueError("--warmup must be in [0,20]")
    concurrency = int(args.concurrency)
    if concurrency <= 0 or concurrency > 32:
        raise ValueError("--concurrency must be in [1,32]")

    drafts_path: Path | None = None
    frozen: list[FrozenDraft] = []
    freeze_meta: dict[str, Any] = {}
    if args.drafts:
        drafts_path = Path(str(args.drafts)).expanduser().resolve()
        loaded = _json_load(drafts_path)
        if not isinstance(loaded, list) or not loaded:
            raise ValueError(
                f"--drafts must point to a non-empty JSON list: {drafts_path}"
            )
        frozen = [FrozenDraft(**cast(dict[str, Any], item)) for item in loaded]  # type: ignore[arg-type]
        if len(frozen) < n:
            raise ValueError(
                f"--drafts has only {len(frozen)} items, but --n={n} was requested."
            )
        frozen = frozen[:n]
        _json_dump(out_dir / "drafts.json", [d.__dict__ for d in frozen])
        freeze_meta = {
            "pull_drafts_ms": None,
            "candidates_requested": None,
            "candidates_received": None,
            "selected": len(frozen),
        }
    else:
        candidates = max(5, int(args.candidates))
        frozen, freeze_meta = _freeze_drafts(
            settings=base_settings, out_dir=out_dir, n=n, candidates=candidates
        )

    results: dict[str, Any] = {
        "config_path": str(os.environ["RECOLETA_CONFIG_PATH"]),
        "selected_n": n,
        "candidates_requested": freeze_meta.get("candidates_requested"),
        "pull_drafts_ms": freeze_meta.get("pull_drafts_ms"),
        "repeat": repeat,
        "warmup": warmup,
        "concurrency": concurrency,
        "methods": {},
    }

    for method in ("html_document",):
        method_out: dict[str, Any] = {}
        db_path = out_dir / f"recoleta-bench-{method}.db"
        drafts = [d.to_item_draft() for d in frozen]

        runs: list[dict[str, Any]] = []
        last_service: PipelineService | None = None
        last_repo: Repository | None = None
        last_items: list[Item] = []
        last_run_id: str | None = None
        last_ingest_result: Any | None = None
        last_enrich_summary: dict[str, Any] = {}
        last_enrich_per_item: list[dict[str, Any]] = []

        for idx in range(warmup + repeat):
            if db_path.exists():
                db_path.unlink()

            settings = _build_settings_for_method(
                base=base_settings,
                method=method,
                db_path=db_path,
                html_document_max_concurrency=concurrency,
            )
            repo = Repository(
                db_path=settings.recoleta_db_path,
                title_dedup_threshold=settings.title_dedup_threshold,
                title_dedup_max_candidates=settings.title_dedup_max_candidates,
            )
            repo.init_schema()
            service = PipelineService(settings=settings, repository=repo)

            run_id = f"bench-{method}-{int(time.time())}-{idx}"
            before = _resource_snapshot()

            ingest_started = time.perf_counter()
            ingest_result = service.ingest(run_id=run_id, drafts=drafts)
            ingest_ms = int((time.perf_counter() - ingest_started) * 1000)

            items = _query_items_for_frozen_drafts(repo=repo, frozen=frozen)
            enrich_summary, enrich_per_item = _enrich_with_timing(
                service=service, run_id=run_id, items=items
            )

            triage_started = time.perf_counter()
            service.triage(run_id=run_id, limit=max(1, len(items)))
            triage_ms = int((time.perf_counter() - triage_started) * 1000)

            after = _resource_snapshot()
            run_record = {
                "run_id": run_id,
                "ingest_ms": ingest_ms,
                "enrich_ms": int(enrich_summary.get("enrich_ms") or 0),
                "triage_ms": triage_ms,
                "pipeline_ms": int(
                    ingest_ms + int(enrich_summary.get("enrich_ms") or 0) + triage_ms
                ),
                "enrich": enrich_summary,
                "resources": {
                    "before": before,
                    "after": after,
                    "cpu_user_s_delta": float(after.get("user_cpu_s") or 0.0)
                    - float(before.get("user_cpu_s") or 0.0),
                    "cpu_sys_s_delta": float(after.get("sys_cpu_s") or 0.0)
                    - float(before.get("sys_cpu_s") or 0.0),
                    "max_rss_mb": float(after.get("max_rss_mb") or 0.0),
                },
            }
            if idx >= warmup:
                runs.append(run_record)

            last_service = service
            last_repo = repo
            last_items = items
            last_run_id = run_id
            last_ingest_result = ingest_result
            last_enrich_summary = enrich_summary
            last_enrich_per_item = enrich_per_item

        ingest_values = [float(r.get("ingest_ms") or 0) for r in runs]
        enrich_values = [float(r.get("enrich_ms") or 0) for r in runs]
        triage_values = [float(r.get("triage_ms") or 0) for r in runs]
        pipeline_values = [float(r.get("pipeline_ms") or 0) for r in runs]
        method_out["runs"] = runs
        method_out["durations"] = {
            "ingest_ms_median": _median(ingest_values),
            "ingest_ms_p95": _p95(ingest_values),
            "enrich_ms_median": _median(enrich_values),
            "enrich_ms_p95": _p95(enrich_values),
            "triage_ms_median": _median(triage_values),
            "triage_ms_p95": _p95(triage_values),
            "pipeline_ms_median": _median(pipeline_values),
            "pipeline_ms_p95": _p95(pipeline_values),
        }

        method_out["run_id"] = last_run_id
        method_out["db_path"] = str(db_path)
        method_out["ingest_result"] = {
            "inserted": getattr(last_ingest_result, "inserted", None),
            "updated": getattr(last_ingest_result, "updated", None),
            "failed": getattr(last_ingest_result, "failed", None),
        }
        method_out["enrich_result"] = last_enrich_summary

        if last_service is None or last_repo is None:
            raise RuntimeError("benchmark did not produce a final run")

        html_tokens_summary, html_tokens_per_item = _compute_tokens(
            service=last_service,
            items=last_items,
            content_type="html_document",
        )
        md_tokens_summary, md_tokens_per_item = _compute_tokens(
            service=last_service,
            items=last_items,
            content_type="html_document_md",
        )

        per_item_by_id: dict[int, dict[str, Any]] = {
            int(r["item_id"]): dict(r) for r in last_enrich_per_item
        }
        html_by_id: dict[int, dict[str, Any]] = {
            int(r["item_id"]): dict(r) for r in html_tokens_per_item
        }
        md_by_id: dict[int, dict[str, Any]] = {
            int(r["item_id"]): dict(r) for r in md_tokens_per_item
        }
        merged_per_item: list[dict[str, Any]] = []
        for item in last_items:
            if item.id is None:
                continue
            item_id = int(item.id)
            enrich_part = per_item_by_id.get(item_id) or {}
            html_part = html_by_id.get(item_id) or {}
            md_part = md_by_id.get(item_id) or {}
            status = (
                "ok"
                if (html_part.get("status") == "ok" and md_part.get("status") == "ok")
                else "partial"
            )
            merged_per_item.append(
                {
                    "item_id": item_id,
                    "arxiv_id": PipelineService._extract_arxiv_identifier(  # noqa: SLF001
                        canonical_url=item.canonical_url,
                        source_item_id=item.source_item_id,
                    ),
                    "status": status,
                    "html_full_tokens": html_part.get("full_tokens"),
                    "html_prompt_tokens": html_part.get("prompt_tokens"),
                    "md_full_tokens": md_part.get("full_tokens"),
                    "md_prompt_tokens": md_part.get("prompt_tokens"),
                    "enrich_item_ms": enrich_part.get("enrich_item_ms"),
                }
            )

        method_out["tokens"] = {
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
        }
        method_out["per_item"] = merged_per_item
        results["methods"][method] = method_out

    _json_dump(out_dir / "bench-results.json", results)
    (out_dir / "bench-results.md").write_text(
        _render_report_md(results=results), encoding="utf-8"
    )

    table = Table(title="arXiv enrich benchmark summary")
    table.add_column("method", style="bold")
    table.add_column("ingest_ms", justify="right")
    table.add_column("enrich_ms", justify="right")
    table.add_column("html_full_sum", justify="right")
    table.add_column("md_full_sum", justify="right")
    table.add_column("md_minus_html_full", justify="right")
    for method in ("html_document",):
        r = results["methods"][method]
        html_sum = ((r.get("tokens") or {}).get("html_document") or {}).get(
            "full_tokens_sum"
        )
        md_sum = ((r.get("tokens") or {}).get("html_document_md") or {}).get(
            "full_tokens_sum"
        )
        delta = ((r.get("tokens") or {}).get("delta") or {}).get(
            "full_tokens_sum_delta"
        )
        table.add_row(
            method,
            str((r.get("durations") or {}).get("ingest_ms_median")),
            str((r.get("durations") or {}).get("enrich_ms_median")),
            str(html_sum),
            str(md_sum),
            str(delta),
        )
    console.print(table)
    console.print(f"[green]wrote[/green] {out_dir / 'drafts.json'}")
    console.print(f"[green]wrote[/green] {out_dir / 'bench-results.json'}")
    console.print(f"[green]wrote[/green] {out_dir / 'bench-results.md'}")


if __name__ == "__main__":
    main()
