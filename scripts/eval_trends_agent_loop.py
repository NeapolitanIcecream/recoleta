from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
import os
from pathlib import Path
import shutil
from typing import Any, cast


_ALLOWED_GRANULARITIES = {"day", "week", "month"}
_ALLOWED_CAPTURE_MODES = {"existing-trends", "existing-corpus", "pipeline"}
# Keep eval reruns on a stable, cheaper budget than production defaults so
# repeated baseline captures stay comparable and affordable.
_DEFAULT_CAPTURE_BUDGET = {
    "overview_pack_max_chars": 6000,
    "item_overview_top_k": 12,
    "item_overview_item_max_chars": 320,
}


@dataclass(slots=True)
class EvalWindow:
    window_id: str
    granularity: str
    anchor_date: str
    stream: str
    topics: list[str]
    notes: str


@dataclass(slots=True)
class EvalCaptureResult:
    window_id: str
    status: str
    run_id: str | None
    doc_id: int | None
    artifact_dir: str
    error_type: str | None = None
    error_message: str | None = None


@dataclass(slots=True)
class EvalRuntimeSnapshot:
    mode: str
    source_db_path: str
    active_db_path: str
    source_lancedb_dir: str | None
    active_lancedb_dir: str
    backup_bundle_dir: str | None = None


def _normalize_string(value: Any, *, field_name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"missing required field: {field_name}")
    return normalized


def _normalize_topics(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    topics: list[str] = []
    seen: set[str] = set()
    for raw_topic in value:
        topic = str(raw_topic or "").strip().lower()
        if not topic or topic in seen:
            continue
        seen.add(topic)
        topics.append(topic)
    return topics


def _parse_window(raw_window: Any) -> EvalWindow:
    if not isinstance(raw_window, dict):
        raise ValueError("window entry must be an object")
    window_id = _normalize_string(raw_window.get("id"), field_name="id")
    granularity = _normalize_string(
        raw_window.get("granularity"), field_name="granularity"
    ).lower()
    if granularity not in _ALLOWED_GRANULARITIES:
        raise ValueError(
            f"unsupported granularity for window {window_id}: {granularity}"
        )
    anchor_date = _normalize_string(
        raw_window.get("anchor_date"), field_name="anchor_date"
    )
    try:
        datetime.strptime(anchor_date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            f"invalid anchor_date for window {window_id}: {anchor_date}"
        ) from exc
    stream = str(raw_window.get("stream") or "default").strip() or "default"
    notes = str(raw_window.get("notes") or "").strip()
    return EvalWindow(
        window_id=window_id,
        granularity=granularity,
        anchor_date=anchor_date,
        stream=stream,
        topics=_normalize_topics(raw_window.get("topics")),
        notes=notes,
    )


def load_eval_windows(fixtures_path: Path) -> list[EvalWindow]:
    payload = json.loads(fixtures_path.read_text(encoding="utf-8"))
    raw_windows = payload.get("windows") if isinstance(payload, dict) else payload
    if not isinstance(raw_windows, list):
        raise ValueError("fixtures file must contain a top-level windows list")
    windows = [_parse_window(raw_window) for raw_window in raw_windows]
    if not windows:
        raise ValueError("fixtures file must define at least one eval window")
    seen_ids: set[str] = set()
    for window in windows:
        if window.window_id in seen_ids:
            raise ValueError(f"duplicate window id: {window.window_id}")
        seen_ids.add(window.window_id)
    return windows


def _build_trends_command(window: EvalWindow) -> str:
    parts = [
        "uv",
        "run",
        "recoleta",
        "trends",
        "--granularity",
        window.granularity,
        "--date",
        window.anchor_date,
    ]
    if window.granularity in {"week", "month"}:
        parts.append("--backfill")
    return " ".join(parts)


def build_eval_manifest(
    *,
    fixtures_path: Path,
    out_dir: Path,
    windows: list[EvalWindow],
) -> dict[str, Any]:
    resolved_fixtures = fixtures_path.expanduser().resolve()
    resolved_out_dir = out_dir.expanduser().resolve()
    manifest_windows: list[dict[str, Any]] = []
    for window in windows:
        artifact_dir = resolved_out_dir / window.window_id
        manifest_windows.append(
            {
                "id": window.window_id,
                "granularity": window.granularity,
                "anchor_date": window.anchor_date,
                "stream": window.stream,
                "topics": list(window.topics),
                "notes": window.notes,
                "artifact_dir": str(artifact_dir),
                "artifacts": {
                    "prompt": str(artifact_dir / "prompt.json"),
                    "tool_trace": str(artifact_dir / "tool-trace.json"),
                    "payload_json": str(artifact_dir / "payload.json"),
                    "report_markdown": str(artifact_dir / "report.md"),
                    "rubric": str(artifact_dir / "rubric.json"),
                    "capture_summary": str(artifact_dir / "capture-summary.json"),
                },
                "commands": {
                    "trends": _build_trends_command(window),
                },
            }
        )
    return {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "fixtures_path": str(resolved_fixtures),
        "out_dir": str(resolved_out_dir),
        "window_count": len(manifest_windows),
        "windows": manifest_windows,
    }


def render_eval_manifest_md(*, manifest: dict[str, Any]) -> str:
    lines = [
        "# trends agent eval manifest",
        "",
        f"- fixtures_path: {manifest['fixtures_path']}",
        f"- out_dir: {manifest['out_dir']}",
        f"- window_count: {manifest['window_count']}",
        "",
        "| id | granularity | anchor_date | stream | topics | artifact_dir |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for window in manifest.get("windows", []):
        topics = ", ".join(str(topic) for topic in window.get("topics", []))
        lines.append(
            "| {id} | {granularity} | {anchor_date} | {stream} | {topics} | {artifact_dir} |".format(
                id=window.get("id", ""),
                granularity=window.get("granularity", ""),
                anchor_date=window.get("anchor_date", ""),
                stream=window.get("stream", ""),
                topics=topics,
                artifact_dir=window.get("artifact_dir", ""),
            )
        )
    lines.append("")
    lines.append("## commands")
    lines.append("")
    for window in manifest.get("windows", []):
        lines.append(f"### {window.get('id', '')}")
        lines.append("")
        lines.append(f"- trends: `{window['commands']['trends']}`")
        notes = str(window.get("notes", "") or "").strip()
        if notes:
            lines.append(f"- notes: {notes}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_eval_runbook_sh(*, manifest: dict[str, Any]) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# Generated by scripts/eval_trends_agent_loop.py",
        "",
    ]
    for window in manifest.get("windows", []):
        window_id = str(window.get("id", "") or "").strip()
        artifact_dir = str(window.get("artifact_dir", "") or "").strip()
        trends_command = str(window.get("commands", {}).get("trends", "") or "").strip()
        if not window_id or not artifact_dir or not trends_command:
            continue
        stdout_log_path = str(Path(artifact_dir) / "trends.stdout.log")
        lines.extend(
            [
                f'echo "[eval] {window_id}"',
                f'mkdir -p "{artifact_dir}"',
                f'{trends_command} | tee "{stdout_log_path}"',
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def summarize_run_metrics(metrics: list[Any]) -> dict[str, Any]:
    by_name: dict[str, float] = {}
    tool_call_breakdown: dict[str, int] = {}
    tool_calls_total = 0
    prompt_chars: int | None = None
    overview_pack_chars: int | None = None
    duration_ms: int | None = None

    for metric in metrics:
        name = str(getattr(metric, "name", "") or "").strip()
        if not name:
            continue
        value = float(getattr(metric, "value", 0.0) or 0.0)
        by_name[name] = value
        if name.endswith(".tool_calls_total"):
            tool_calls_total = int(value)
            continue
        if ".tool." in name and name.endswith(".calls_total"):
            tool_name = name.split(".tool.", 1)[1].removesuffix(".calls_total")
            normalized_tool_name = str(tool_name or "").strip()
            if normalized_tool_name:
                tool_call_breakdown[normalized_tool_name] = int(value)
            continue
        if name.endswith(".prompt_chars"):
            prompt_chars = int(value)
            continue
        if name.endswith(".overview_pack.chars"):
            overview_pack_chars = int(value)
            continue
        if name.endswith(".duration_ms"):
            duration_ms = int(value)

    return {
        "tool_calls_total": tool_calls_total,
        "tool_call_breakdown": {
            tool_name: tool_call_breakdown[tool_name]
            for tool_name in sorted(tool_call_breakdown)
        },
        "prompt_chars": prompt_chars,
        "overview_pack_chars": overview_pack_chars,
        "duration_ms": duration_ms,
        "metrics_by_name": {name: by_name[name] for name in sorted(by_name)},
    }


def _json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def _capture_budget_env_overrides() -> dict[str, str]:
    return {
        "TRENDS_OVERVIEW_PACK_MAX_CHARS": str(
            _DEFAULT_CAPTURE_BUDGET["overview_pack_max_chars"]
        ),
        "TRENDS_ITEM_OVERVIEW_TOP_K": str(
            _DEFAULT_CAPTURE_BUDGET["item_overview_top_k"]
        ),
        "TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS": str(
            _DEFAULT_CAPTURE_BUDGET["item_overview_item_max_chars"]
        ),
    }


def _capture_budget_summary() -> dict[str, int]:
    return dict(_DEFAULT_CAPTURE_BUDGET)


def _build_prompt_capture_stub(*, run_id: str | None, doc_id: int | None) -> dict[str, Any]:
    return {
        "status": "not_captured_yet",
        "run_id": run_id,
        "doc_id": doc_id,
        "notes": (
            "Prompt capture is not wired yet for trends runs. "
            "The current baseline harness stores the rendered note, payload JSON, "
            "metrics-derived tool trace, and debug response artifact when available."
        ),
    }


def _build_rubric_stub(
    *,
    window_manifest: dict[str, Any],
    run_id: str | None,
    doc_id: int | None,
) -> dict[str, Any]:
    return {
        "status": "pending_manual_review",
        "run_id": run_id,
        "doc_id": doc_id,
        "window_id": str(window_manifest.get("id", "") or ""),
        "scores": {
            "grounding": None,
            "distinctness": None,
            "representative_quality": None,
            "readability": None,
            "tool_efficiency": None,
        },
        "notes": [],
    }


def write_window_capture_artifacts(
    *,
    window_manifest: dict[str, Any],
    run_id: str,
    doc_id: int,
    report_markdown: str,
    payload_json: dict[str, Any],
    tool_trace: dict[str, Any],
    capture_metadata: dict[str, Any] | None = None,
) -> None:
    artifacts = cast(dict[str, str], window_manifest["artifacts"])
    artifact_dir = Path(str(window_manifest["artifact_dir"]))
    artifact_dir.mkdir(parents=True, exist_ok=True)
    Path(artifacts["report_markdown"]).write_text(report_markdown, encoding="utf-8")
    _json_dump(Path(artifacts["payload_json"]), payload_json)
    _json_dump(
        Path(artifacts["tool_trace"]),
        {
            "status": "captured",
            "run_id": run_id,
            "doc_id": doc_id,
            **tool_trace,
        },
    )
    _json_dump(Path(artifacts["prompt"]), _build_prompt_capture_stub(run_id=run_id, doc_id=doc_id))
    _json_dump(
        Path(artifacts["rubric"]),
        _build_rubric_stub(window_manifest=window_manifest, run_id=run_id, doc_id=doc_id),
    )
    _json_dump(
        Path(artifacts["capture_summary"]),
        {
            "status": "captured",
            "run_id": run_id,
            "doc_id": doc_id,
            "window_id": str(window_manifest.get("id", "") or ""),
            "granularity": str(window_manifest.get("granularity", "") or ""),
            **(capture_metadata or {}),
        },
    )


def write_window_capture_failure_artifacts(
    *,
    window_manifest: dict[str, Any],
    error_type: str,
    error_message: str,
) -> None:
    artifacts = cast(dict[str, str], window_manifest["artifacts"])
    artifact_dir = Path(str(window_manifest["artifact_dir"]))
    artifact_dir.mkdir(parents=True, exist_ok=True)
    Path(artifacts["report_markdown"]).write_text("", encoding="utf-8")
    _json_dump(
        Path(artifacts["payload_json"]),
        {
            "status": "failed",
            "error": {"type": error_type, "message": error_message},
        },
    )
    _json_dump(
        Path(artifacts["tool_trace"]),
        {
            "status": "failed",
            "error": {"type": error_type, "message": error_message},
            "tool_calls_total": 0,
            "tool_call_breakdown": {},
        },
    )
    _json_dump(Path(artifacts["prompt"]), _build_prompt_capture_stub(run_id=None, doc_id=None))
    _json_dump(
        Path(artifacts["rubric"]),
        _build_rubric_stub(window_manifest=window_manifest, run_id=None, doc_id=None),
    )
    _json_dump(
        Path(artifacts["capture_summary"]),
        {
            "status": "failed",
            "window_id": str(window_manifest.get("id", "") or ""),
            "error": {"type": error_type, "message": error_message},
        },
    )


def _period_bounds(*, granularity: str, anchor_date: str) -> tuple[datetime, datetime]:
    from recoleta import trends

    anchor = date.fromisoformat(anchor_date)
    if granularity == "day":
        return trends.day_period_bounds(anchor)
    if granularity == "week":
        return trends.week_period_bounds(anchor)
    if granularity == "month":
        return trends.month_period_bounds(anchor)
    raise ValueError(f"unsupported granularity: {granularity}")


def _load_payload_json(*, repository: Any, doc_id: int) -> dict[str, Any]:
    payload_chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=1)
    payload_text = str(getattr(payload_chunk, "text", "") or "").strip()
    if not payload_text:
        return {}
    loaded = json.loads(payload_text)
    return loaded if isinstance(loaded, dict) else {}


def _render_report_markdown(
    *,
    repository: Any,
    payload_json: dict[str, Any],
    doc_id: int,
    run_id: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    output_dir: Path,
    output_language: str | None,
) -> str:
    from recoleta.publish.trend_notes import write_markdown_trend_note
    from recoleta.trend_materialize import materialize_trend_note_payload
    from recoleta.trends import TrendPayload

    payload = TrendPayload.model_validate(payload_json)
    materialized = materialize_trend_note_payload(
        repository=repository,
        payload=payload,
        markdown_output_dir=output_dir,
        output_language=output_language,
    )
    note_path = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=doc_id,
        title=materialized.title,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=materialized.overview_md,
        topics=materialized.topics,
        clusters=materialized.clusters,
        highlights=materialized.highlights,
    )
    return note_path.read_text(encoding="utf-8")


def _load_debug_payload(*, artifact_dir: Path, run_id: str) -> dict[str, Any] | None:
    candidate = artifact_dir / "debug-artifacts" / run_id / "no-item" / "llm-response.json"
    return _read_json(candidate)


@contextmanager
def _temporary_env(overrides: dict[str, str]) -> Any:
    previous = {key: os.environ.get(key) for key in overrides}
    try:
        for key, value in overrides.items():
            os.environ[key] = value
        yield
    finally:
        for key, previous_value in previous.items():
            if previous_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous_value


def _describe_workspace_runtime(*, mode: str) -> dict[str, Any]:
    import recoleta.cli as cli

    settings = cli._build_settings()
    source_lancedb_dir = Path(settings.rag_lancedb_dir).expanduser().resolve()
    return asdict(
        EvalRuntimeSnapshot(
            mode=mode,
            source_db_path=str(Path(settings.recoleta_db_path).expanduser().resolve()),
            active_db_path=str(Path(settings.recoleta_db_path).expanduser().resolve()),
            source_lancedb_dir=str(source_lancedb_dir),
            active_lancedb_dir=str(source_lancedb_dir),
        )
    )


def describe_live_eval_runtime() -> dict[str, Any]:
    return _describe_workspace_runtime(mode="live_workspace")


def prepare_isolated_eval_runtime(*, out_dir: Path) -> dict[str, Any]:
    import recoleta.cli as cli

    settings = cli._build_settings()
    source_db_path = Path(settings.recoleta_db_path).expanduser().resolve()
    source_lancedb_dir = Path(settings.rag_lancedb_dir).expanduser().resolve()
    runtime_root = out_dir.expanduser().resolve() / "_runtime"
    runtime_root.mkdir(parents=True, exist_ok=True)

    source_repository = cli._build_repository_for_db_path(db_path=source_db_path)
    backup_result = source_repository.backup_database(output_dir=runtime_root / "db-backups")

    isolated_db_path = runtime_root / "recoleta-eval.db"
    type(source_repository).restore_database(
        bundle_dir=backup_result.bundle_dir,
        db_path=isolated_db_path,
    )

    isolated_lancedb_dir = runtime_root / "lancedb"
    if isolated_lancedb_dir.exists():
        shutil.rmtree(isolated_lancedb_dir)
    if source_lancedb_dir.exists():
        shutil.copytree(source_lancedb_dir, isolated_lancedb_dir)
    else:
        isolated_lancedb_dir.mkdir(parents=True, exist_ok=True)

    return asdict(
        EvalRuntimeSnapshot(
            mode="isolated_copy",
            source_db_path=str(source_db_path),
            active_db_path=str(isolated_db_path),
            source_lancedb_dir=str(source_lancedb_dir),
            active_lancedb_dir=str(isolated_lancedb_dir),
            backup_bundle_dir=str(backup_result.bundle_dir),
        )
    )


def _serialize_capture_source_document(document: Any) -> dict[str, Any]:
    period_start = getattr(document, "period_start", None)
    period_end = getattr(document, "period_end", None)
    return {
        "doc_id": int(getattr(document, "id") or 0),
        "scope": str(getattr(document, "scope", "") or ""),
        "granularity": str(getattr(document, "granularity", "") or ""),
        "title": str(getattr(document, "title", "") or ""),
        "period_start": period_start.isoformat()
        if isinstance(period_start, datetime)
        else None,
        "period_end": period_end.isoformat() if isinstance(period_end, datetime) else None,
    }


def _normalize_period_bound(value: Any) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _find_existing_trend_document(
    *,
    repository: Any,
    granularity: str,
    anchor_date: str,
    scope: str,
) -> tuple[Any, datetime, datetime]:
    period_start, period_end = _period_bounds(
        granularity=granularity,
        anchor_date=anchor_date,
    )
    documents = repository.list_documents(
        doc_type="trend",
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        scope=scope,
        limit=10,
    )
    exact_matches = [
        document
        for document in documents
        if _normalize_period_bound(getattr(document, "period_start", None)) == period_start
        and _normalize_period_bound(getattr(document, "period_end", None)) == period_end
    ]
    if not exact_matches:
        raise ValueError(
            "No existing trend document found for "
            f"scope={scope} granularity={granularity} period_start={period_start.isoformat()}"
        )
    selected = sorted(
        exact_matches,
        key=lambda document: int(getattr(document, "id") or 0),
        reverse=True,
    )[0]
    return selected, period_start, period_end


def capture_existing_trends_baseline(
    *,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    import recoleta.cli as cli

    runtime = _describe_workspace_runtime(mode="existing_docs")
    repository = cli._build_repository_for_db_path(
        db_path=Path(str(runtime["active_db_path"]))
    )
    results: list[dict[str, Any]] = []
    out_dir = Path(str(manifest["out_dir"]))
    windows = cast(list[dict[str, Any]], manifest.get("windows", []))
    for window_manifest in windows:
        granularity = str(window_manifest.get("granularity", "") or "").strip().lower()
        anchor_date = str(window_manifest.get("anchor_date", "") or "").strip()
        artifact_dir = Path(str(window_manifest.get("artifact_dir", "") or ""))
        scope = str(window_manifest.get("stream", "") or "").strip() or "default"
        try:
            document, period_start, period_end = _find_existing_trend_document(
                repository=repository,
                granularity=granularity,
                anchor_date=anchor_date,
                scope=scope,
            )
            doc_id = int(getattr(document, "id") or 0)
            payload_json = _load_payload_json(repository=repository, doc_id=doc_id)
            report_markdown = _render_report_markdown(
                repository=repository,
                payload_json=payload_json,
                doc_id=doc_id,
                run_id=f"eval-existing-trends-{window_manifest['id']}",
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                output_dir=artifact_dir / "rendered-note",
                output_language=cli._build_settings().llm_output_language,
            )
            tool_trace = {
                "trace_status": "unavailable_from_existing_doc",
                "notes": (
                    "Existing trend documents do not retain the originating run_id, "
                    "so metrics-derived tool traces are unavailable without rerunning the pipeline."
                ),
                "source_document": _serialize_capture_source_document(document),
            }
            write_window_capture_artifacts(
                window_manifest=window_manifest,
                run_id=f"existing-trend-doc-{doc_id}",
                doc_id=doc_id,
                report_markdown=report_markdown,
                payload_json=payload_json,
                tool_trace=tool_trace,
                capture_metadata={
                    "capture_mode": "existing-trends",
                    "source_document": _serialize_capture_source_document(document),
                },
            )
            results.append(
                asdict(
                    EvalCaptureResult(
                        window_id=str(window_manifest.get("id", "") or ""),
                        status="captured",
                        run_id=None,
                        doc_id=doc_id,
                        artifact_dir=str(artifact_dir),
                    )
                )
            )
        except Exception as exc:  # noqa: BLE001
            write_window_capture_failure_artifacts(
                window_manifest=window_manifest,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )
            results.append(
                asdict(
                    EvalCaptureResult(
                        window_id=str(window_manifest.get("id", "") or ""),
                        status="failed",
                        run_id=None,
                        doc_id=None,
                        artifact_dir=str(artifact_dir),
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )
            )
    baseline_summary = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "capture_mode": "existing-trends",
        "runtime": runtime,
        "captured_total": sum(1 for row in results if row["status"] == "captured"),
        "failed_total": sum(1 for row in results if row["status"] == "failed"),
        "windows": results,
    }
    _json_dump(out_dir / "baseline-summary.json", baseline_summary)
    return baseline_summary


def _run_window_trends_capture(
    service: Any,
    *,
    stage_run_id: str,
    window_manifest: dict[str, Any],
    llm_model: str | None,
    reuse_existing_corpus: bool,
    backfill: bool,
) -> Any:
    granularity = str(window_manifest.get("granularity", "") or "").strip().lower()
    anchor_date = date.fromisoformat(str(window_manifest.get("anchor_date", "") or "").strip())
    stream = str(window_manifest.get("stream", "") or "").strip() or "default"
    if bool(getattr(service, "_explicit_topic_streams", False)):
        selected_stream = next(
            (
                stream_runtime
                for stream_runtime in list(getattr(service, "_topic_streams", []) or [])
                if str(getattr(stream_runtime, "name", "") or "").strip() == stream
            ),
            None,
        )
        if selected_stream is None:
            raise ValueError(f"unknown topic stream for eval window: {stream}")
        stream_settings = service._settings_for_topic_stream(selected_stream)
        stream_targets = set(getattr(selected_stream, "publish_targets", []) or [])
        stream_sender = (
            service._telegram_sender_for_stream(selected_stream)
            if "telegram" in stream_targets
            else None
        )
        service_factory = cast(Any, service.__class__)
        child_service = service_factory(
            settings=stream_settings,
            repository=service.repository,
            analyzer=service.analyzer,
            triage=service.semantic_triage,
            telegram_sender=stream_sender,
        )
        from recoleta.pipeline.trends_stage import run_trends_stage

        return run_trends_stage(
            child_service,
            run_id=stage_run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode="missing",
            debug_pdf=False,
            scope=stream,
            reuse_existing_corpus=reuse_existing_corpus,
        )
    if stream != "default":
        raise ValueError(
            "stream-specific eval window requires explicit topic streams in settings: "
            f"{stream}"
        )
    return service.trends(
        run_id=stage_run_id,
        granularity=granularity,
        anchor_date=anchor_date,
        llm_model=llm_model,
        backfill=backfill,
        backfill_mode="missing",
        debug_pdf=False,
        reuse_existing_corpus=reuse_existing_corpus,
    )


def capture_trends_rerun_baseline(
    *,
    manifest: dict[str, Any],
    llm_model: str | None,
    isolate_runtime: bool,
    capture_mode: str,
    reuse_existing_corpus: bool,
    backfill: bool,
) -> dict[str, Any]:
    import recoleta.cli as cli

    results: list[dict[str, Any]] = []
    runtime: dict[str, Any]
    capture_budget = _capture_budget_summary()
    out_dir = Path(str(manifest["out_dir"]))
    windows = cast(list[dict[str, Any]], manifest.get("windows", []))
    try:
        runtime = (
            prepare_isolated_eval_runtime(out_dir=out_dir)
            if isolate_runtime
            else describe_live_eval_runtime()
        )
    except Exception as exc:  # noqa: BLE001
        for window_manifest in windows:
            write_window_capture_failure_artifacts(
                window_manifest=window_manifest,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )
            results.append(
                asdict(
                    EvalCaptureResult(
                        window_id=str(window_manifest.get("id", "") or ""),
                        status="failed",
                        run_id=None,
                        doc_id=None,
                        artifact_dir=str(window_manifest.get("artifact_dir", "") or ""),
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )
            )
        baseline_summary = {
            "generated_at": datetime.now(tz=UTC).isoformat(),
            "capture_mode": capture_mode,
            "runtime": {
                "mode": "isolated_copy" if isolate_runtime else "live_workspace",
                "status": "failed",
                "error": {"type": type(exc).__name__, "message": str(exc)},
            },
            "captured_total": 0,
            "failed_total": len(results),
            "windows": results,
        }
        _json_dump(out_dir / "baseline-summary.json", baseline_summary)
        return baseline_summary

    runtime_env_overrides = {
        "RECOLETA_DB_PATH": str(runtime["active_db_path"]),
        "RAG_LANCEDB_DIR": str(runtime["active_lancedb_dir"]),
        **_capture_budget_env_overrides(),
    }
    for window_manifest in windows:
        granularity = str(window_manifest.get("granularity", "") or "").strip().lower()
        anchor_date = str(window_manifest.get("anchor_date", "") or "").strip()
        artifact_dir = Path(str(window_manifest.get("artifact_dir", "") or ""))
        artifact_dir.mkdir(parents=True, exist_ok=True)
        env_overrides = {
            **runtime_env_overrides,
            "PUBLISH_TARGETS": "markdown",
            "MARKDOWN_OUTPUT_DIR": str(artifact_dir / "published"),
            "ARTIFACTS_DIR": str(artifact_dir / "debug-artifacts"),
            "WRITE_DEBUG_ARTIFACTS": "true",
        }
        try:
            with _temporary_env(env_overrides):
                settings, repository, run_id, result = cli._execute_stage(
                    stage_name="trends",
                    stage_runner=lambda service, stage_run_id: _run_window_trends_capture(
                        service,
                        stage_run_id=stage_run_id,
                        window_manifest=window_manifest,
                        llm_model=llm_model,
                        reuse_existing_corpus=reuse_existing_corpus,
                        backfill=backfill,
                    ),
                )
            period_start, period_end = _period_bounds(
                granularity=granularity,
                anchor_date=anchor_date,
            )
            doc_id = int(getattr(result, "doc_id"))
            payload_json = _load_payload_json(repository=repository, doc_id=doc_id)
            report_markdown = _render_report_markdown(
                repository=repository,
                payload_json=payload_json,
                doc_id=doc_id,
                run_id=run_id,
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                output_dir=artifact_dir / "rendered-note",
                output_language=getattr(settings, "llm_output_language", None),
            )
            tool_trace = summarize_run_metrics(repository.list_metrics(run_id=run_id))
            debug_payload = _load_debug_payload(artifact_dir=artifact_dir, run_id=run_id)
            if debug_payload is not None:
                tool_trace["llm_debug"] = debug_payload.get("debug")
            write_window_capture_artifacts(
                window_manifest=window_manifest,
                run_id=run_id,
                doc_id=doc_id,
                report_markdown=report_markdown,
                payload_json=payload_json,
                tool_trace=tool_trace,
                capture_metadata={
                    "capture_mode": capture_mode,
                    "reuse_existing_corpus": reuse_existing_corpus,
                    "capture_budget": capture_budget,
                },
            )
            results.append(
                asdict(
                    EvalCaptureResult(
                        window_id=str(window_manifest.get("id", "") or ""),
                        status="captured",
                        run_id=run_id,
                        doc_id=doc_id,
                        artifact_dir=str(artifact_dir),
                    )
                )
            )
        except Exception as exc:  # noqa: BLE001
            write_window_capture_failure_artifacts(
                window_manifest=window_manifest,
                error_type=type(exc).__name__,
                error_message=str(exc),
            )
            results.append(
                asdict(
                    EvalCaptureResult(
                        window_id=str(window_manifest.get("id", "") or ""),
                        status="failed",
                        run_id=None,
                        doc_id=None,
                        artifact_dir=str(artifact_dir),
                        error_type=type(exc).__name__,
                        error_message=str(exc),
                    )
                )
            )
    baseline_summary = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "capture_mode": capture_mode,
        "capture_budget": capture_budget,
        "runtime": runtime,
        "captured_total": sum(1 for row in results if row["status"] == "captured"),
        "failed_total": sum(1 for row in results if row["status"] == "failed"),
        "windows": results,
    }
    _json_dump(out_dir / "baseline-summary.json", baseline_summary)
    return baseline_summary


def capture_eval_baseline(
    *,
    manifest: dict[str, Any],
    llm_model: str | None,
    isolate_runtime: bool,
    capture_mode: str,
) -> dict[str, Any]:
    normalized_mode = str(capture_mode or "").strip().lower()
    if normalized_mode not in _ALLOWED_CAPTURE_MODES:
        raise ValueError(f"unsupported capture mode: {capture_mode}")
    if normalized_mode == "existing-trends":
        return capture_existing_trends_baseline(manifest=manifest)
    if normalized_mode == "existing-corpus":
        return capture_trends_rerun_baseline(
            manifest=manifest,
            llm_model=llm_model,
            isolate_runtime=isolate_runtime,
            capture_mode="existing-corpus",
            reuse_existing_corpus=True,
            backfill=False,
        )
    return capture_trends_rerun_baseline(
        manifest=manifest,
        llm_model=llm_model,
        isolate_runtime=isolate_runtime,
        capture_mode="pipeline",
        reuse_existing_corpus=False,
        backfill=True,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a fixed-window eval manifest for trends agent loop research."
    )
    # The default fixture intentionally excludes live month windows for now.
    # As of 2026-03-12 the real corpus only has week 2026-W10 coverage, which
    # is not enough to treat month-level report scoring as meaningful.
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("benchmarks/trends_agent_eval_windows.json"),
        help="JSON file that defines eval windows.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("bench-out-trends-agent-eval"),
        help="Output directory for eval-manifest artifacts.",
    )
    parser.add_argument(
        "--capture-baseline",
        action="store_true",
        help="Run the current trends loop on each eval window and capture baseline artifacts.",
    )
    parser.add_argument(
        "--capture-mode",
        type=str,
        default="existing-corpus",
        choices=sorted(_ALLOWED_CAPTURE_MODES),
        help=(
            "Baseline capture strategy. `existing-corpus` reruns trend generation on the "
            "existing indexed corpus, `existing-trends` snapshots already-generated trend "
            "documents, and `pipeline` reruns the full trends stage."
        ),
    )
    parser.add_argument(
        "--live-workspace",
        action="store_true",
        help=(
            "For rerun capture modes (`existing-corpus`, `pipeline`), reuse the configured "
            "SQLite/LanceDB workspace directly instead of cloning it under the eval output "
            "root. Unsafe: rerun capture writes runs, metrics, and trend docs into the "
            "live workspace."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Optional LLM model override for baseline capture runs.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    fixtures_path = Path(args.fixtures)
    out_dir = Path(args.out)
    windows = load_eval_windows(fixtures_path)
    manifest = build_eval_manifest(
        fixtures_path=fixtures_path,
        out_dir=out_dir,
        windows=windows,
    )

    resolved_out_dir = out_dir.expanduser().resolve()
    resolved_out_dir.mkdir(parents=True, exist_ok=True)
    manifest_json_path = resolved_out_dir / "eval-manifest.json"
    manifest_md_path = resolved_out_dir / "eval-manifest.md"
    runbook_path = resolved_out_dir / "run-eval.sh"
    manifest_json_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest_md_path.write_text(
        render_eval_manifest_md(manifest=manifest),
        encoding="utf-8",
    )
    runbook_path.write_text(
        render_eval_runbook_sh(manifest=manifest),
        encoding="utf-8",
    )
    runbook_path.chmod(0o755)
    baseline_summary_path: str | None = None
    if bool(args.capture_baseline):
        _ = capture_eval_baseline(
            manifest=manifest,
            llm_model=str(args.model).strip() if args.model else None,
            isolate_runtime=not bool(args.live_workspace),
            capture_mode=str(args.capture_mode),
        )
        baseline_summary_path = str(
            resolved_out_dir.expanduser().resolve() / "baseline-summary.json"
        )
    print(
        json.dumps(
            {
                "manifest_json": str(manifest_json_path),
                "manifest_md": str(manifest_md_path),
                "runbook": str(runbook_path),
                "baseline_summary": baseline_summary_path,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
