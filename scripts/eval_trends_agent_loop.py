from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_ALLOWED_GRANULARITIES = {"day", "week", "month"}


@dataclass(slots=True)
class EvalWindow:
    window_id: str
    granularity: str
    anchor_date: str
    stream: str
    topics: list[str]
    notes: str


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
                    "report_markdown": str(artifact_dir / "report.md"),
                    "rubric": str(artifact_dir / "rubric.json"),
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a fixed-window eval manifest for trends agent loop research."
    )
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
    print(
        json.dumps(
            {
                "manifest_json": str(manifest_json_path),
                "manifest_md": str(manifest_md_path),
                "runbook": str(runbook_path),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
