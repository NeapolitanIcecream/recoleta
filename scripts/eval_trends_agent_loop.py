from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
import os
from pathlib import Path
from typing import Any, cast


_ALLOWED_GRANULARITIES = {"day", "week", "month"}


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


def capture_eval_baseline(
    *,
    manifest: dict[str, Any],
    llm_model: str | None,
) -> dict[str, Any]:
    import recoleta.cli as cli

    results: list[dict[str, Any]] = []
    for window_manifest in cast(list[dict[str, Any]], manifest.get("windows", [])):
        granularity = str(window_manifest.get("granularity", "") or "").strip().lower()
        anchor_date = str(window_manifest.get("anchor_date", "") or "").strip()
        artifact_dir = Path(str(window_manifest.get("artifact_dir", "") or ""))
        artifact_dir.mkdir(parents=True, exist_ok=True)
        env_overrides = {
            "PUBLISH_TARGETS": "markdown",
            "MARKDOWN_OUTPUT_DIR": str(artifact_dir / "published"),
            "ARTIFACTS_DIR": str(artifact_dir / "debug-artifacts"),
            "WRITE_DEBUG_ARTIFACTS": "true",
        }
        try:
            with _temporary_env(env_overrides):
                settings, repository, run_id, result = cli._execute_stage(
                    stage_name="trends",
                    stage_runner=lambda service, stage_run_id: service.trends(
                        run_id=stage_run_id,
                        granularity=granularity,
                        anchor_date=date.fromisoformat(anchor_date),
                        llm_model=llm_model,
                        backfill=granularity in {"week", "month"},
                        backfill_mode="missing",
                        debug_pdf=False,
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
        "captured_total": sum(1 for row in results if row["status"] == "captured"),
        "failed_total": sum(1 for row in results if row["status"] == "failed"),
        "windows": results,
    }
    out_dir = Path(str(manifest["out_dir"]))
    _json_dump(out_dir / "baseline-summary.json", baseline_summary)
    return baseline_summary


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
