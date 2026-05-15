from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import recoleta.cli as cli
from recoleta.arxiv_pool import (
    ArxivPoolStore,
    ArxivPoolSync,
    ArxivPoolWorker,
    ArxivPoolWindow,
    build_arxiv_pool_windows,
    build_arxiv_pool_windows_for_days,
    resolve_arxiv_pool_db_path,
    worker_state_payload,
)


def run_arxiv_pool_sync_command(
    *,
    anchor_date: str,
    lookback_days: int,
    force: bool,
    config_path: Path | None,
    json_output: bool,
    command_name: str = "arxiv-pool sync",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    target_date = cli._parse_anchor_date_option(anchor_date)
    windows = _configured_windows_for_lookback(
        settings=settings,
        anchor_date=target_date,
        lookback_days=lookback_days,
    )
    result = _sync_configured_windows(
        settings=settings,
        windows=windows,
        force=force,
    )
    payload = {
        "status": "ok",
        "command": command_name,
        "date": target_date.isoformat(),
        "lookback_days": max(1, int(lookback_days)),
        "pool_db_path": str(resolve_arxiv_pool_db_path(settings)),
        "sync": result.as_payload(),
    }
    return _emit_or_print_sync_payload(
        payload=payload,
        json_output=json_output,
        command_name=command_name,
    )


def run_arxiv_pool_backfill_command(
    *,
    start_date: str,
    end_date: str,
    force: bool,
    config_path: Path | None,
    json_output: bool,
    command_name: str = "arxiv-pool backfill",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    start = cli._parse_anchor_date_option(start_date)
    end = cli._parse_anchor_date_option(end_date)
    if end < start:
        raise ValueError("--end must be on or after --start")
    days: list[date] = []
    cursor = start
    while cursor <= end:
        days.append(cursor)
        cursor += timedelta(days=1)
    windows = _configured_windows_for_days(settings=settings, days=days)
    result = _sync_configured_windows(
        settings=settings,
        windows=windows,
        force=force,
    )
    payload = {
        "status": "ok",
        "command": command_name,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "pool_db_path": str(resolve_arxiv_pool_db_path(settings)),
        "sync": result.as_payload(),
    }
    return _emit_or_print_sync_payload(
        payload=payload,
        json_output=json_output,
        command_name=command_name,
    )


def run_arxiv_pool_worker_command(
    *,
    poll_interval_seconds: int,
    lookback_days: int,
    idle_jitter_seconds: int,
    backfill_start: str | None,
    backfill_end: str | None,
    config_path: Path | None,
    json_output: bool,
    command_name: str = "arxiv-pool worker",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        raise ValueError("SOURCES.arxiv.enabled=true is required for arxiv-pool worker")
    start = _optional_date(backfill_start)
    end = _optional_date(backfill_end)
    if (start is None) != (end is None):
        raise ValueError("--backfill-start and --backfill-end must be provided together")
    if start is not None and end is not None and end < start:
        raise ValueError("--backfill-end must be on or after --backfill-start")

    pool_path = resolve_arxiv_pool_db_path(settings)
    store = ArxivPoolStore(pool_path)
    console = None if json_output else cli._runtime_symbols()["Console"]()

    def emit_event(payload: dict[str, Any]) -> None:
        event_payload = {
            "status": "ok",
            "command": command_name,
            "pool_db_path": str(pool_path),
            **payload,
        }
        if json_output:
            cli._emit_json(event_payload)
            return
        if console is None:
            return
        event = str(event_payload.get("event") or "")
        if event in {"worker_start", "worker_stop", "sync_pass_result"}:
            console.print(
                f"[cyan]{command_name}[/cyan] {event} "
                f"pool={event_payload['pool_db_path']}"
            )
        elif event in {"cooldown_active", "transient_failure"}:
            console.print(
                f"[yellow]{command_name}[/yellow] {event} "
                f"next_wake={event_payload.get('next_wake_at', '-')}"
            )

    worker = ArxivPoolWorker(
        store=store,
        queries=list(arxiv_settings.queries),
        max_results=int(arxiv_settings.max_results_per_run),
        request_interval_seconds=float(settings.arxiv_pool.request_interval_seconds),
        cooldown_seconds=int(settings.arxiv_pool.cooldown_seconds),
        poll_interval_seconds=poll_interval_seconds,
        lookback_days=lookback_days,
        idle_jitter_seconds=idle_jitter_seconds,
        backfill_start=start,
        backfill_end=end,
        event_sink=emit_event,
    )
    log = cli._runtime_symbols()["logger"].bind(module="cli.arxiv_pool.worker")
    try:
        with cli._graceful_shutdown_signals():
            worker.run()
    except KeyboardInterrupt as exc:
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="arXiv pool worker interrupted",
            exc=exc,
        )
    return {
        "status": "ok",
        "command": command_name,
        "pool_db_path": str(pool_path),
        "worker_state": worker_state_payload(store.get_worker_state()),
    }


def run_inspect_arxiv_pool_freshness_command(
    *,
    config_path: Path | None,
    limit: int,
    json_output: bool,
    command_name: str = "inspect arxiv-pool freshness",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    store = ArxivPoolStore(resolve_arxiv_pool_db_path(settings))
    rate_state = store.get_rate_state()
    windows = store.list_window_records(limit=limit)
    worker_state = store.get_worker_state()
    active_cooldown = _active_cooldown(rate_state)
    payload = {
        "status": "ok",
        "command": command_name,
        "pool_db_path": str(resolve_arxiv_pool_db_path(settings)),
        "active_cooldown": active_cooldown,
        "rate_state": _rate_state_payload(rate_state),
        "worker_state": worker_state_payload(worker_state),
        "window_status_summary": _window_status_summary(windows),
        "windows": [_window_payload(window) for window in windows],
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{command_name} completed[/green] "
        f"windows={len(windows)} pool={payload['pool_db_path']}"
    )
    return payload


def run_admin_arxiv_pool_gc_command(
    *,
    config_path: Path | None,
    older_than_days: int,
    json_output: bool,
    command_name: str = "admin arxiv-pool gc",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    cutoff = datetime.now().astimezone() - timedelta(days=max(1, int(older_than_days)))
    deleted = ArxivPoolStore(resolve_arxiv_pool_db_path(settings)).prune_query_matches_older_than(
        cutoff
    )
    payload = {
        "status": "ok",
        "command": command_name,
        "pool_db_path": str(resolve_arxiv_pool_db_path(settings)),
        "cutoff": cutoff.isoformat(),
        "deleted_matches": deleted,
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{command_name} completed[/green] "
        f"deleted_matches={deleted} pool={payload['pool_db_path']}"
    )
    return payload


def _configured_windows_for_days(settings: Any, days: list[date]) -> list[ArxivPoolWindow]:
    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        return []
    return build_arxiv_pool_windows_for_days(
        queries=list(arxiv_settings.queries),
        days=days,
        max_results=int(arxiv_settings.max_results_per_run),
    )


def _configured_windows_for_lookback(
    *,
    settings: Any,
    anchor_date: date,
    lookback_days: int,
) -> list[ArxivPoolWindow]:
    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        return []
    return build_arxiv_pool_windows(
        queries=list(arxiv_settings.queries),
        anchor_date=anchor_date,
        lookback_days=lookback_days,
        max_results=int(arxiv_settings.max_results_per_run),
    )


def _pool_arxiv_settings(settings: Any) -> Any | None:
    arxiv_settings = settings.sources.arxiv
    if not bool(arxiv_settings.enabled):
        return None
    if str(arxiv_settings.mode) != "pool":
        raise ValueError("SOURCES.arxiv.mode must be pool for arxiv-pool commands")
    return arxiv_settings


def _sync_configured_windows(
    *,
    settings: Any,
    windows: list[ArxivPoolWindow],
    force: bool,
) -> Any:
    pool_settings = settings.arxiv_pool
    return ArxivPoolSync(
        store=ArxivPoolStore(resolve_arxiv_pool_db_path(settings)),
        request_interval_seconds=float(pool_settings.request_interval_seconds),
        cooldown_seconds=int(pool_settings.cooldown_seconds),
    ).sync_windows(windows, force=force)


def _emit_or_print_sync_payload(
    *,
    payload: dict[str, Any],
    json_output: bool,
    command_name: str,
) -> dict[str, Any]:
    if json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    sync = payload["sync"]
    console.print(
        f"[green]{command_name} completed[/green] "
        f"windows={sync['requested_windows_total']} "
        f"upstream_requests={sync['upstream_requests_total']} "
        f"cache_hits={sync['cache_hit_total']}"
    )
    return payload


def _window_payload(window: Any) -> dict[str, Any]:
    return {
        "query_text": window.query_text,
        "period_start": window.period_start.isoformat(),
        "period_end": window.period_end.isoformat(),
        "max_results": window.max_results,
        "status": window.status,
        "requested_at": _isoformat_or_none(window.requested_at),
        "completed_at": _isoformat_or_none(window.completed_at),
        "cooldown_until": _isoformat_or_none(window.cooldown_until),
        "upstream_requests_total": window.upstream_requests_total,
        "upstream_status": window.upstream_status,
        "error_category": window.error_category,
        "error_message": window.error_message,
        "result_count": window.result_count,
    }


def _optional_date(value: str | None) -> date | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    return cli._parse_anchor_date_option(raw)


def _rate_state_payload(rate_state: Any | None) -> dict[str, Any] | None:
    if rate_state is None:
        return None
    return {
        "last_request_at": _isoformat_or_none(
            getattr(rate_state, "last_request_at", None)
        ),
        "cooldown_until": _isoformat_or_none(
            getattr(rate_state, "cooldown_until", None)
        ),
        "consecutive_429_total": int(
            getattr(rate_state, "consecutive_429_total", 0) or 0
        ),
        "last_status": getattr(rate_state, "last_status", None),
        "last_error_message": getattr(rate_state, "last_error_message", None),
    }


def _active_cooldown(rate_state: Any | None) -> bool:
    cooldown_until = getattr(rate_state, "cooldown_until", None)
    if cooldown_until is None:
        return False
    return cooldown_until > datetime.now().astimezone()


def _window_status_summary(windows: list[Any]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for window in windows:
        status = str(getattr(window, "status", "") or "unknown")
        summary[status] = int(summary.get(status, 0)) + 1
    return dict(sorted(summary.items()))


def _isoformat_or_none(value: Any) -> str | None:
    return value.isoformat() if value is not None else None
