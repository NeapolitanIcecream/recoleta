from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, NoReturn

import recoleta.cli as cli
from recoleta.arxiv_pool import (
    ArxivPoolStore,
    ArxivPoolSync,
    ArxivPoolSyncResult,
    ArxivPoolWorker,
    ArxivPoolWindow,
    arxiv_pool_backend_descriptor_from_settings,
    arxiv_pool_readiness_policy_from_settings,
    arxiv_pool_sync_result_from_huldra,
    arxiv_pool_fetcher_name,
    build_arxiv_pool_backend_from_settings,
    build_huldra_arxiv_request_for_window,
    build_arxiv_pool_windows,
    build_arxiv_pool_windows_for_days,
    evaluate_arxiv_pool_window_readiness,
    huldra_wait_timeout_seconds,
    resolve_arxiv_pool_db_path,
    worker_state_payload,
)

HULDRA_FORCE_REFRESH_UNSUPPORTED_REASON = "huldra_force_refresh_unsupported"


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkerCommandOptions:
    poll_interval_seconds: int
    lookback_days: int
    idle_jitter_seconds: int
    backfill_start: str | None
    backfill_end: str | None
    config_path: Path | None
    json_output: bool
    command_name: str = "arxiv-pool worker"


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
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra" and force:
        _reject_huldra_force_refresh(
            command_name=command_name,
            json_output=json_output,
        )
    result = _sync_configured_windows(
        settings=settings,
        windows=windows,
        force=force,
    )
    payload = {
        "status": "ok",
        "command": command_name,
        "backend": descriptor.kind,
        "huldra_base_url": descriptor.identity if descriptor.kind == "huldra" else None,
        "date": target_date.isoformat(),
        "lookback_days": max(1, int(lookback_days)),
        "pool_db_path": (
            str(resolve_arxiv_pool_db_path(settings))
            if descriptor.kind == "local_sqlite"
            else None
        ),
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
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra" and force:
        _reject_huldra_force_refresh(
            command_name=command_name,
            json_output=json_output,
        )
    days: list[date] = []
    cursor = start
    while cursor <= end:
        days.append(cursor)
        cursor += timedelta(days=1)
    result = (
        _huldra_backfill_configured_days(
            settings=settings,
            start=start,
            end=end,
            requested_days_total=len(days),
            force=force,
        )
        if descriptor.kind == "huldra"
        else _sync_configured_windows(
            settings=settings,
            windows=_configured_windows_for_days(settings=settings, days=days),
            force=force,
        )
    )
    payload = {
        "status": "ok",
        "command": command_name,
        "backend": descriptor.kind,
        "huldra_base_url": descriptor.identity if descriptor.kind == "huldra" else None,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "pool_db_path": (
            str(resolve_arxiv_pool_db_path(settings))
            if descriptor.kind == "local_sqlite"
            else None
        ),
        "sync": result.as_payload(),
    }
    return _emit_or_print_sync_payload(
        payload=payload,
        json_output=json_output,
        command_name=command_name,
    )


def run_arxiv_pool_worker_command(
    options: ArxivPoolWorkerCommandOptions | None = None,
    **raw_options: Any,
) -> dict[str, Any]:
    worker_options = _coerce_worker_command_options(options, raw_options)
    return _run_arxiv_pool_worker_command(worker_options)


def _run_arxiv_pool_worker_command(
    options: ArxivPoolWorkerCommandOptions,
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=options.config_path)
    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        raise ValueError("SOURCES.arxiv.enabled=true is required for arxiv-pool worker")
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra":
        payload = {
            "status": "skipped",
            "command": options.command_name,
            "backend": "huldra",
            "huldra_base_url": descriptor.identity,
            "pool_db_path": None,
            "reason": "huldra_backend_uses_huldra_worker",
        }
        if options.json_output:
            cli._emit_json(payload)
        return payload

    start, end = _worker_backfill_range(options)
    pool_path = resolve_arxiv_pool_db_path(settings)
    store = ArxivPoolStore(pool_path)
    worker = ArxivPoolWorker(
        store=store,
        queries=list(arxiv_settings.queries),
        max_results=int(arxiv_settings.max_results_per_run),
        request_interval_seconds=float(settings.arxiv_pool.request_interval_seconds),
        cooldown_seconds=int(settings.arxiv_pool.cooldown_seconds),
        poll_interval_seconds=options.poll_interval_seconds,
        lookback_days=options.lookback_days,
        idle_jitter_seconds=options.idle_jitter_seconds,
        backfill_start=start,
        backfill_end=end,
        event_sink=_worker_event_sink(
            command_name=options.command_name,
            pool_path=pool_path,
            json_output=options.json_output,
        ),
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
        "command": options.command_name,
        "pool_db_path": str(pool_path),
        "worker_state": worker_state_payload(store.get_worker_state()),
    }


def _coerce_worker_command_options(
    options: ArxivPoolWorkerCommandOptions | None,
    raw_options: dict[str, Any],
) -> ArxivPoolWorkerCommandOptions:
    if options is not None:
        if raw_options:
            raise TypeError("options cannot be combined with worker command fields")
        return options
    return ArxivPoolWorkerCommandOptions(
        poll_interval_seconds=int(raw_options["poll_interval_seconds"]),
        lookback_days=int(raw_options["lookback_days"]),
        idle_jitter_seconds=int(raw_options["idle_jitter_seconds"]),
        backfill_start=raw_options.get("backfill_start"),
        backfill_end=raw_options.get("backfill_end"),
        config_path=raw_options.get("config_path"),
        json_output=bool(raw_options["json_output"]),
        command_name=str(raw_options.get("command_name", "arxiv-pool worker")),
    )


def _worker_backfill_range(
    options: ArxivPoolWorkerCommandOptions,
) -> tuple[date | None, date | None]:
    start = _optional_date(options.backfill_start)
    end = _optional_date(options.backfill_end)
    if (start is None) != (end is None):
        raise ValueError("--backfill-start and --backfill-end must be provided together")
    if start is not None and end is not None and end < start:
        raise ValueError("--backfill-end must be on or after --backfill-start")
    return start, end


def _worker_event_sink(
    *,
    command_name: str,
    pool_path: Path,
    json_output: bool,
) -> Any:
    console = None if json_output else cli._runtime_symbols()["Console"]()

    def emit_event(payload: dict[str, Any]) -> None:
        event_payload = _worker_event_payload(
            command_name=command_name,
            pool_path=pool_path,
            payload=payload,
        )
        if json_output:
            cli._emit_json(event_payload)
        elif console is not None:
            _print_worker_event(
                console=console,
                command_name=command_name,
                event_payload=event_payload,
            )

    return emit_event


def _worker_event_payload(
    *,
    command_name: str,
    pool_path: Path,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": "ok",
        "command": command_name,
        "pool_db_path": str(pool_path),
        **payload,
    }


def _print_worker_event(
    *,
    console: Any,
    command_name: str,
    event_payload: dict[str, Any],
) -> None:
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


def run_inspect_arxiv_pool_freshness_command(
    *,
    config_path: Path | None,
    limit: int,
    json_output: bool,
    command_name: str = "inspect arxiv-pool freshness",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra":
        return _run_huldra_inspect_arxiv_pool_freshness_command(
            settings=settings,
            descriptor_identity=descriptor.identity,
            limit=limit,
            json_output=json_output,
            command_name=command_name,
        )
    store = ArxivPoolStore(resolve_arxiv_pool_db_path(settings))
    rate_state = store.get_rate_state()
    windows = store.list_window_records(limit=limit)
    readiness_policy = arxiv_pool_readiness_policy_from_settings(settings)
    window_readiness = [
        evaluate_arxiv_pool_window_readiness(
            store=store,
            window=ArxivPoolWindow(
                query_text=window.query_text,
                period_start=window.period_start,
                period_end=window.period_end,
                max_results=window.max_results,
            ),
            policy=readiness_policy,
        )
        for window in windows
    ]
    worker_state = store.get_worker_state()
    active_cooldown = _active_cooldown(rate_state)
    payload = {
        "status": "ok",
        "command": command_name,
        "pool_db_path": str(resolve_arxiv_pool_db_path(settings)),
        "fetcher": arxiv_pool_fetcher_name(),
        "active_cooldown": active_cooldown,
        "rate_state": _rate_state_payload(rate_state),
        "worker_state": worker_state_payload(worker_state),
        "maturity_policy": readiness_policy.as_payload(),
        "window_status_summary": _window_status_summary(
            windows,
            window_readiness=window_readiness,
        ),
        "windows": [
            _window_payload(window, readiness=readiness)
            for window, readiness in zip(windows, window_readiness, strict=True)
        ],
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


def _run_huldra_inspect_arxiv_pool_freshness_command(
    *,
    settings: Any,
    descriptor_identity: str,
    limit: int,
    json_output: bool,
    command_name: str,
) -> dict[str, Any]:
    readiness_policy = arxiv_pool_readiness_policy_from_settings(settings)
    backend = build_arxiv_pool_backend_from_settings(settings)
    windows = _configured_recent_windows_for_limit(settings=settings, limit=limit)
    window_readiness = [
        backend.evaluate_window_readiness(
            window,
            readiness_policy=readiness_policy,
        )
        for window in windows
    ]
    payload = {
        "status": "ok",
        "command": command_name,
        "backend": "huldra",
        "huldra_base_url": descriptor_identity,
        "inspect_scope": "configured_windows",
        "cache_listing_supported": False,
        "pool_db_path": None,
        "fetcher": "huldra",
        "active_cooldown": False,
        "rate_state": None,
        "worker_state": None,
        "maturity_policy": readiness_policy.as_payload(),
        "window_status_summary": _window_status_summary(
            window_readiness,
            window_readiness=window_readiness,
        ),
        "windows": [
            _backend_window_payload(readiness)
            for readiness in window_readiness
        ],
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{command_name} completed[/green] "
        f"windows={len(windows)} huldra={descriptor_identity}"
    )
    return payload


def _configured_recent_windows_for_limit(
    *,
    settings: Any,
    limit: int,
) -> list[ArxivPoolWindow]:
    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        return []
    needed = max(0, int(limit))
    if needed <= 0:
        return []
    windows: list[ArxivPoolWindow] = []
    cursor = datetime.now(UTC).date()
    while len(windows) < needed:
        day_windows = build_arxiv_pool_windows_for_days(
            queries=list(arxiv_settings.queries),
            days=[cursor],
            max_results=int(arxiv_settings.max_results_per_run),
        )
        windows.extend(day_windows)
        cursor -= timedelta(days=1)
    return windows[:needed]


def _backend_window_payload(readiness: Any) -> dict[str, Any]:
    payload = readiness.as_payload()
    diagnostic = payload.get("diagnostic")
    rendered = {
        "query_text": payload["query_text"],
        "period_start": payload["period_start"],
        "period_end": payload["period_end"],
        "max_results": payload["max_results"],
        "backend": payload.get("backend"),
        "status": payload["status"],
        "record_status": payload["status"],
        "cache_status": payload.get("cache_status"),
        "serving_status": payload.get("serving_status"),
        "cache_readable": payload["cache_readable"],
        "mature": payload["mature"],
        "analysis_ready": payload["analysis_ready"],
        "blocked_reason": payload["blocked_reason"],
        "huldra_cache_key": payload.get("cache_key"),
    }
    if isinstance(diagnostic, dict):
        rendered.update(diagnostic)
    return rendered


def run_admin_arxiv_pool_gc_command(
    *,
    config_path: Path | None,
    older_than_days: int,
    json_output: bool,
    command_name: str = "admin arxiv-pool gc",
) -> dict[str, Any]:
    settings = cli._build_settings(config_path=config_path)
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra":
        payload = {
            "status": "skipped",
            "command": command_name,
            "backend": "huldra",
            "huldra_base_url": descriptor.identity,
            "pool_db_path": None,
            "reason": "huldra_backend_gc_not_supported",
            "deleted_matches": 0,
        }
        if json_output:
            cli._emit_json(payload)
        return payload
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


def _reject_huldra_force_refresh(
    *,
    command_name: str,
    json_output: bool,
) -> NoReturn:
    reason = HULDRA_FORCE_REFRESH_UNSUPPORTED_REASON
    message = "Huldra arXiv pool backend does not support --force refresh."
    if json_output:
        cli._emit_json(
            {
                "status": "error",
                "command": command_name,
                "reason": reason,
                "error": message,
            }
        )
    else:
        console = cli._runtime_symbols()["Console"]()
        console.print(f"[red]{command_name} failed[/red] reason={reason} {message}")
    raise cli.typer.Exit(code=1)


def _sync_configured_windows(
    *,
    settings: Any,
    windows: list[ArxivPoolWindow],
    force: bool,
) -> Any:
    pool_settings = settings.arxiv_pool
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra":
        if force:
            raise ValueError(HULDRA_FORCE_REFRESH_UNSUPPORTED_REASON)
        from huldra.client import HuldraClient

        readiness_policy = arxiv_pool_readiness_policy_from_settings(settings)
        requests = [
            build_huldra_arxiv_request_for_window(
                window=window,
                readiness_policy=readiness_policy,
                client_id="recoleta:arxiv-pool-sync",
                timeout_seconds=float(pool_settings.huldra_request_timeout_seconds),
            )
            for window in windows
        ]
        wait_timeout = huldra_wait_timeout_seconds(
            configured_timeout_seconds=pool_settings.huldra_wait_timeout_seconds,
            requested_windows_total=len(requests),
        )
        with HuldraClient(
            base_url=descriptor.identity,
            timeout=float(pool_settings.huldra_request_timeout_seconds),
        ) as client:
            result = client.sync_windows(
                requests,
                wait=True,
                wait_timeout_seconds=wait_timeout,
            )
        return arxiv_pool_sync_result_from_huldra(result)
    return ArxivPoolSync(
        store=ArxivPoolStore(resolve_arxiv_pool_db_path(settings)),
        request_interval_seconds=float(pool_settings.request_interval_seconds),
        cooldown_seconds=int(pool_settings.cooldown_seconds),
    ).sync_windows(windows, force=force)


def _huldra_backfill_configured_days(
    *,
    settings: Any,
    start: date,
    end: date,
    requested_days_total: int,
    force: bool,
) -> Any:
    if force:
        raise ValueError(HULDRA_FORCE_REFRESH_UNSUPPORTED_REASON)
    from huldra.client import HuldraClient

    arxiv_settings = _pool_arxiv_settings(settings)
    if arxiv_settings is None:
        return ArxivPoolSyncResult(requested_windows_total=0)
    pool_settings = settings.arxiv_pool
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    queries = list(arxiv_settings.queries)
    requested_windows_total = len(queries) * int(requested_days_total)
    wait_timeout = huldra_wait_timeout_seconds(
        configured_timeout_seconds=pool_settings.huldra_wait_timeout_seconds,
        requested_windows_total=requested_windows_total,
    )
    with HuldraClient(
        base_url=descriptor.identity,
        timeout=float(pool_settings.huldra_request_timeout_seconds),
    ) as client:
        result = client.backfill_windows(
            search_queries=queries,
            start_date=start,
            end_date=end,
            max_results=int(arxiv_settings.max_results_per_run),
            wait=True,
            wait_timeout_seconds=wait_timeout,
            client_id="recoleta:arxiv-pool-backfill",
        )
    return arxiv_pool_sync_result_from_huldra(result)


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


def _window_payload(window: Any, *, readiness: Any | None = None) -> dict[str, Any]:
    payload = {
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
    if readiness is not None:
        payload.update(
            {
                "cache_readable": bool(readiness.cache_readable),
                "mature": bool(readiness.mature),
                "analysis_ready": bool(readiness.analysis_ready),
                "blocked_reason": readiness.blocked_reason,
            }
        )
    return payload


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


def _window_status_summary(
    windows: list[Any],
    *,
    window_readiness: list[Any] | None = None,
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for window in windows:
        status = str(getattr(window, "status", "") or "unknown")
        summary[status] = int(summary.get(status, 0)) + 1
    if window_readiness is not None:
        summary["analysis_ready"] = sum(
            1 for readiness in window_readiness if bool(readiness.analysis_ready)
        )
        summary["immature"] = sum(
            1
            for readiness in window_readiness
            if readiness.blocked_reason == "immature_window"
        )
        summary.setdefault("rate_limited", 0)
    return dict(sorted(summary.items()))


def _isoformat_or_none(value: Any) -> str | None:
    return value.isoformat() if value is not None else None
