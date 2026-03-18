from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, NoReturn

import recoleta.cli as cli


def _parse_json_object(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        loaded = json.loads(raw)
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _parse_json_list(raw: str | None) -> list[Any]:
    if not raw:
        return []
    try:
        loaded = json.loads(raw)
    except Exception:
        return []
    return loaded if isinstance(loaded, list) else []


def _run_duration_seconds(*, run: Any, reference_now: datetime) -> int | None:
    started_at = cli._normalize_utc_datetime(getattr(run, "started_at", None))
    if started_at is None:
        return None
    finished_at = cli._normalize_utc_datetime(getattr(run, "finished_at", None))
    heartbeat_at = cli._normalize_utc_datetime(getattr(run, "heartbeat_at", None))
    end_at = finished_at or heartbeat_at or reference_now
    return max(0, int((end_at - started_at).total_seconds()))


def _serialize_pass_output(row: Any) -> dict[str, Any]:
    return {
        "id": int(getattr(row, "id", 0) or 0),
        "scope": str(getattr(row, "scope", "") or ""),
        "pass_kind": str(getattr(row, "pass_kind", "") or ""),
        "status": str(getattr(row, "status", "") or ""),
        "granularity": str(getattr(row, "granularity", "") or "") or None,
        "period_start": cli._isoformat_or_none(getattr(row, "period_start", None)),
        "period_end": cli._isoformat_or_none(getattr(row, "period_end", None)),
        "created_at": cli._isoformat_or_none(getattr(row, "created_at", None)),
        "schema_version": int(getattr(row, "schema_version", 0) or 0),
        "content_hash": str(getattr(row, "content_hash", "") or ""),
        "diagnostics": _parse_json_object(getattr(row, "diagnostics_json", None)),
        "input_refs_total": len(
            _parse_json_list(getattr(row, "input_refs_json", None))
        ),
    }


def _serialize_artifact(row: Any) -> dict[str, Any]:
    return {
        "id": int(getattr(row, "id", 0) or 0),
        "item_id": int(getattr(row, "item_id", 0) or 0) or None,
        "kind": str(getattr(row, "kind", "") or ""),
        "path": str(getattr(row, "path", "") or ""),
        "details": _parse_json_object(getattr(row, "details_json", None)),
        "created_at": cli._isoformat_or_none(getattr(row, "created_at", None)),
    }


def _derive_run_context(*, run: Any, pass_outputs: list[Any]) -> dict[str, Any]:
    scope_candidates = sorted(
        {
            str(getattr(row, "scope", "") or "").strip()
            for row in pass_outputs
            if str(getattr(row, "scope", "") or "").strip()
        }
    )
    granularity_candidates = sorted(
        {
            str(getattr(row, "granularity", "") or "").strip()
            for row in pass_outputs
            if str(getattr(row, "granularity", "") or "").strip()
        }
    )
    period_starts = sorted(
        {
            value
            for value in (
                cli._isoformat_or_none(getattr(row, "period_start", None))
                for row in pass_outputs
            )
            if value is not None
        }
    )
    period_ends = sorted(
        {
            value
            for value in (
                cli._isoformat_or_none(getattr(row, "period_end", None))
                for row in pass_outputs
            )
            if value is not None
        }
    )
    command = str(getattr(run, "command", "") or "").strip() or None
    scope = str(getattr(run, "scope", "") or "").strip() or None
    granularity = str(getattr(run, "granularity", "") or "").strip() or None
    period_start = cli._isoformat_or_none(getattr(run, "period_start", None))
    period_end = cli._isoformat_or_none(getattr(run, "period_end", None))
    return {
        "command": command,
        "scope": scope or (scope_candidates[0] if len(scope_candidates) == 1 else None),
        "scope_candidates": scope_candidates,
        "granularity": (
            granularity
            or (
                granularity_candidates[0]
                if len(granularity_candidates) == 1
                else None
            )
        ),
        "granularity_candidates": granularity_candidates,
        "period_start": (
            period_start or (period_starts[0] if len(period_starts) == 1 else None)
        ),
        "period_end": period_end or (period_ends[0] if len(period_ends) == 1 else None),
    }


def _build_failure_summary(*, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    failure_artifacts = [
        artifact
        for artifact in artifacts
        if isinstance(artifact.get("details"), dict) and artifact["details"]
    ]
    by_category: dict[str, int] = {}
    by_type: dict[str, int] = {}
    http_status: dict[str, int] = {}
    retryable_total = 0
    for artifact in failure_artifacts:
        details = artifact["details"]
        category = str(details.get("error_category") or "").strip()
        if category:
            by_category[category] = by_category.get(category, 0) + 1
        error_type = str(details.get("error_type") or "").strip()
        if error_type:
            by_type[error_type] = by_type.get(error_type, 0) + 1
        status = details.get("http_status")
        if isinstance(status, int) and status > 0:
            key = str(status)
            http_status[key] = http_status.get(key, 0) + 1
        if details.get("retryable") is True:
            retryable_total += 1
    return {
        "artifacts_total": len(failure_artifacts),
        "retryable_total": retryable_total,
        "by_category": dict(sorted(by_category.items())),
        "by_type": dict(sorted(by_type.items())),
        "http_status": dict(sorted(http_status.items())),
    }


def _build_run_payload(
    *,
    repository: Any,
    run: Any,
    reference_now: datetime,
) -> dict[str, Any]:
    run_id = str(getattr(run, "id", "") or "")
    metrics = repository.list_metrics(run_id=run_id)
    pass_outputs = repository.list_pass_outputs_for_run(run_id=run_id)
    artifacts = repository.list_artifacts_for_run(run_id=run_id)
    context = _derive_run_context(run=run, pass_outputs=pass_outputs)
    artifacts_by_kind: dict[str, int] = {}
    for artifact in artifacts:
        kind = str(getattr(artifact, "kind", "") or "unknown")
        artifacts_by_kind[kind] = artifacts_by_kind.get(kind, 0) + 1
    serialized_artifacts = [_serialize_artifact(row) for row in artifacts]

    return {
        "id": run_id,
        "status": str(getattr(run, "status", "") or ""),
        "started_at": cli._isoformat_or_none(getattr(run, "started_at", None)),
        "heartbeat_at": cli._isoformat_or_none(getattr(run, "heartbeat_at", None)),
        "finished_at": cli._isoformat_or_none(getattr(run, "finished_at", None)),
        "duration_seconds": _run_duration_seconds(run=run, reference_now=reference_now),
        "config_fingerprint": str(getattr(run, "config_fingerprint", "") or ""),
        **context,
        "metrics_total": len(metrics),
        "metrics": cli._metrics_payload(metrics),
        "billing": cli._billing_summary_payload(metrics),
        "pass_outputs_total": len(pass_outputs),
        "pass_outputs": [_serialize_pass_output(row) for row in pass_outputs],
        "artifacts_total": len(artifacts),
        "artifacts_by_kind": dict(sorted(artifacts_by_kind.items())),
        "artifacts": serialized_artifacts,
        "failure_summary": _build_failure_summary(artifacts=serialized_artifacts),
    }


def _build_run_list_entry(
    *,
    repository: Any,
    run: Any,
    reference_now: datetime,
) -> dict[str, Any]:
    payload = _build_run_payload(
        repository=repository,
        run=run,
        reference_now=reference_now,
    )
    return {
        "id": payload["id"],
        "status": payload["status"],
        "started_at": payload["started_at"],
        "finished_at": payload["finished_at"],
        "duration_seconds": payload["duration_seconds"],
        "command": payload["command"],
        "scope": payload["scope"],
        "granularity": payload["granularity"],
        "period_start": payload["period_start"],
        "period_end": payload["period_end"],
        "metrics_total": payload["metrics_total"],
        "pass_outputs_total": payload["pass_outputs_total"],
        "artifacts_total": payload["artifacts_total"],
        "failure_artifacts_total": payload["failure_summary"]["artifacts_total"],
        "billing": payload["billing"],
    }


def _load_repository_or_exit(
    *,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
    log_module: str,
) -> tuple[Any, Path]:
    symbols = cli._runtime_symbols()
    logger = symbols["logger"]
    console = symbols["Console"]()
    log = logger.bind(module=log_module, json=json_output)

    def _exit_with_error(message: str, *, code: int = 1) -> NoReturn:
        log.warning("Run inspection failed db_path={} error={}", resolved_db_path, message)
        if json_output:
            cli._emit_json({"status": "error", "error": message})
        else:
            console.print(f"[red]runs failed[/red] {message}")
        raise cli.typer.Exit(code=code)

    resolved_db_path: Path | None = None
    try:
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path,
            config_path=config_path,
        )
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        log.warning(message)
        if json_output:
            cli._emit_json({"status": "error", "error": message})
        else:
            console.print(f"[red]runs failed[/red] {message}")
        raise cli.typer.Exit(code=1) from exc

    if not resolved_db_path.exists():
        _exit_with_error(f"db does not exist: {resolved_db_path}")

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        repository.ensure_schema_current()
    except Exception as exc:  # noqa: BLE001
        _exit_with_error(str(exc))

    return repository, resolved_db_path


def run_runs_show_command(
    *,
    run_id: str | None,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
) -> None:
    repository, resolved_db_path = _load_repository_or_exit(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
        log_module="cli.runs.show",
    )
    reference_now = datetime.now(UTC)
    target_run = (
        repository.get_run(run_id=run_id)
        if run_id is not None and str(run_id).strip()
        else next(iter(repository.list_recent_runs(limit=1)), None)
    )
    if target_run is None:
        if json_output:
            cli._emit_json({"status": "error", "error": "run not found"})
        else:
            cli._runtime_symbols()["Console"]().print("[red]run not found[/red]")
        raise cli.typer.Exit(code=1)

    payload = {
        "status": "ok",
        "db_path": str(resolved_db_path),
        "run": _build_run_payload(
            repository=repository,
            run=target_run,
            reference_now=reference_now,
        ),
    }
    if json_output:
        cli._emit_json(payload)
        return

    console = cli._runtime_symbols()["Console"]()
    run_payload = payload["run"]
    console.print(
        "[green]run ok[/green] "
        f"id={run_payload['id']} status={run_payload['status']} "
        f"duration_seconds={run_payload['duration_seconds'] if run_payload['duration_seconds'] is not None else 'unknown'}"
    )
    console.print(f"db={payload['db_path']}")
    if run_payload["command"] is not None:
        console.print(
            f"command={run_payload['command']} scope={run_payload['scope'] or 'unknown'} "
            f"granularity={run_payload['granularity'] or 'unknown'}"
        )
    console.print(
        f"metrics_total={run_payload['metrics_total']} "
        f"pass_outputs_total={run_payload['pass_outputs_total']} "
        f"artifacts_total={run_payload['artifacts_total']}"
    )
    if run_payload["failure_summary"]["artifacts_total"] > 0:
        console.print(
            f"failure_artifacts={run_payload['failure_summary']['artifacts_total']} "
            f"retryable={run_payload['failure_summary']['retryable_total']}"
        )
    if run_payload["artifacts_by_kind"]:
        parts = [
            f"{kind}={count}"
            for kind, count in run_payload["artifacts_by_kind"].items()
        ]
        console.print("artifacts_by_kind=" + " ".join(parts))
    for row in run_payload["pass_outputs"]:
        console.print(
            f"[cyan]{row['pass_kind']}[/cyan] "
            f"id={row['id']} scope={row['scope']} status={row['status']}"
        )


def run_runs_list_command(
    *,
    limit: int,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
) -> None:
    repository, resolved_db_path = _load_repository_or_exit(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
        log_module="cli.runs.list",
    )
    reference_now = datetime.now(UTC)
    runs = repository.list_recent_runs(limit=limit)
    payload = {
        "status": "ok",
        "db_path": str(resolved_db_path),
        "runs": [
            _build_run_list_entry(
                repository=repository,
                run=run,
                reference_now=reference_now,
            )
            for run in runs
        ],
    }
    if json_output:
        cli._emit_json(payload)
        return

    console = cli._runtime_symbols()["Console"]()
    console.print(f"[green]runs ok[/green] count={len(payload['runs'])}")
    for row in payload["runs"]:
        console.print(
            f"[cyan]{row['id']}[/cyan] "
            f"command={row['command'] or 'unknown'} "
            f"status={row['status']} "
            f"duration_seconds={row['duration_seconds'] if row['duration_seconds'] is not None else 'unknown'} "
            f"pass_outputs={row['pass_outputs_total']} artifacts={row['artifacts_total']}"
        )
