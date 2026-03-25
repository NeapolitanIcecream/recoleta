from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
import os
from pathlib import Path
import time
from typing import Any, NoReturn, cast

import recoleta.cli as cli


_SOURCE_DIAGNOSTIC_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")


def _default_source_diagnostic_entry(*, enabled: bool | None) -> dict[str, Any]:
    return {
        "enabled": enabled,
        "status": "disabled" if enabled is False else "not_run",
        "pipeline_completed": False,
        "ingest": {
            "drafts_total": 0,
            "pull_failed_total": 0,
            "pull_duration_ms": 0,
            "filtered_out_total": 0,
            "in_window_total": 0,
            "missing_published_at_total": 0,
            "deduped_total": 0,
            "deferred_total": 0,
            "not_modified_total": 0,
            "oldest_published_at": None,
            "newest_published_at": None,
            "inserted_total": 0,
            "updated_total": 0,
        },
        "enrich": {
            "processed_total": 0,
            "skipped_total": 0,
            "failed_total": 0,
            "item_duration_ms_total": 0,
            "fetch_ms_sum": 0,
            "extract_ms_sum": 0,
            "db_read_ms_sum": 0,
            "db_write_ms_sum": 0,
            "input_bytes_sum": 0,
            "content_chars_sum": 0,
            "short_content_total": 0,
            "content_types": {},
            "pdf_backends": {},
        },
    }


def _source_enabled_map(settings: Any | None) -> dict[str, bool | None]:
    if settings is None:
        return {source_name: None for source_name in _SOURCE_DIAGNOSTIC_NAMES}
    sources = getattr(settings, "sources", None)
    if sources is None:
        return {source_name: None for source_name in _SOURCE_DIAGNOSTIC_NAMES}
    enabled: dict[str, bool | None] = {}
    for source_name in _SOURCE_DIAGNOSTIC_NAMES:
        source_config = getattr(sources, source_name, None)
        enabled[source_name] = (
            bool(getattr(source_config, "enabled", False))
            if source_config is not None
            else None
        )
    return enabled


def _build_source_diagnostics_payload(
    *,
    repository: Any,
    settings: Any | None,
    reference_now: datetime,
) -> dict[str, Any] | None:
    enabled_by_source = _source_enabled_map(settings)
    recent_runs = repository.list_recent_runs(limit=20)
    for run in recent_runs:
        metrics = repository.list_metrics(run_id=run.id)
        if not any(
            str(getattr(metric, "name", "") or "").startswith("pipeline.ingest.source.")
            or str(getattr(metric, "name", "") or "").startswith(
                "pipeline.enrich.source."
            )
            for metric in metrics
        ):
            continue

        sources_payload: dict[str, dict[str, Any]] = {
            source_name: _default_source_diagnostic_entry(
                enabled=enabled_by_source.get(source_name)
            )
            for source_name in _SOURCE_DIAGNOSTIC_NAMES
        }

        def _source_entry(source_name: str) -> dict[str, Any]:
            normalized = str(source_name or "").strip().lower() or "unknown"
            if normalized not in sources_payload:
                sources_payload[normalized] = _default_source_diagnostic_entry(
                    enabled=enabled_by_source.get(normalized)
                )
            return sources_payload[normalized]

        for metric in metrics:
            metric_name = str(getattr(metric, "name", "") or "")
            metric_value = int(float(getattr(metric, "value", 0) or 0))
            if metric_name.startswith("pipeline.ingest.source."):
                remainder = metric_name.removeprefix("pipeline.ingest.source.")
                source_name, _, metric_key = remainder.partition(".")
                if not metric_key:
                    continue
                entry = _source_entry(source_name)
                ingest_payload = entry["ingest"]
                if metric_key in {
                    "oldest_published_at_unix",
                    "newest_published_at_unix",
                }:
                    if metric_value > 0:
                        payload_key = metric_key.removesuffix("_unix")
                        ingest_payload[payload_key] = datetime.fromtimestamp(
                            metric_value,
                            tz=UTC,
                        ).isoformat()
                    continue
                if metric_key in ingest_payload:
                    ingest_payload[metric_key] = metric_value
                continue
            if not metric_name.startswith("pipeline.enrich.source."):
                continue
            remainder = metric_name.removeprefix("pipeline.enrich.source.")
            source_name, _, metric_key = remainder.partition(".")
            if not metric_key:
                continue
            entry = _source_entry(source_name)
            enrich_payload = entry["enrich"]
            if metric_key.startswith("content_type.") and metric_key.endswith("_total"):
                content_type = metric_key[len("content_type.") : -len("_total")]
                if content_type:
                    enrich_payload["content_types"][content_type] = metric_value
                continue
            if metric_key.startswith("pdf_backend.") and metric_key.endswith("_total"):
                backend = metric_key[len("pdf_backend.") : -len("_total")]
                if backend:
                    enrich_payload["pdf_backends"][backend] = metric_value
                continue
            if metric_key in enrich_payload:
                enrich_payload[metric_key] = metric_value

        for entry in sources_payload.values():
            enabled = entry.get("enabled")
            ingest_payload = entry["ingest"]
            enrich_payload = entry["enrich"]
            enrich_success_total = int(enrich_payload["processed_total"]) + int(
                enrich_payload["skipped_total"]
            )
            observed = (
                int(ingest_payload["drafts_total"]) > 0
                or int(ingest_payload["pull_failed_total"]) > 0
                or int(ingest_payload["not_modified_total"]) > 0
                or enrich_success_total > 0
                or int(enrich_payload["failed_total"]) > 0
            )
            if enabled is False and not observed:
                status = "disabled"
            elif (
                int(ingest_payload["not_modified_total"]) > 0
                and int(ingest_payload["pull_failed_total"]) <= 0
                and int(enrich_payload["failed_total"]) <= 0
            ):
                status = "not_modified"
            elif (
                int(ingest_payload["pull_failed_total"]) > 0
                and int(ingest_payload["drafts_total"]) <= 0
                and int(enrich_payload["failed_total"]) <= 0
            ):
                status = "pull_failed"
            elif int(enrich_payload["failed_total"]) > 0:
                status = "enrich_failed"
            elif enrich_success_total > 0:
                status = "ok"
            elif int(ingest_payload["drafts_total"]) > 0:
                status = "ingested_only"
            else:
                status = "not_run"
            entry["status"] = status
            entry["pipeline_completed"] = bool(status in {"ok", "not_modified"})

        started_at = cli._normalize_utc_datetime(getattr(run, "started_at", None))
        age_seconds: int | None = None
        if started_at is not None:
            age_seconds = max(
                0,
                int((reference_now - started_at).total_seconds()),
            )
        return {
            "run_id": run.id,
            "run_status": str(getattr(run, "status", "") or ""),
            "started_at": started_at.isoformat() if started_at is not None else None,
            "age_seconds": age_seconds,
            "sources": sources_payload,
        }
    return None


def _period_bounds_for_granularity(
    *,
    anchor_date: str,
    granularity: str,
) -> tuple[datetime, datetime]:
    from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds

    parsed_anchor = cli._parse_anchor_date_option(str(anchor_date or "").strip())
    normalized = str(granularity or "").strip().lower()
    if normalized == "week":
        period_start, period_end = week_period_bounds(parsed_anchor)
    elif normalized == "month":
        period_start, period_end = month_period_bounds(parsed_anchor)
    elif normalized == "day":
        period_start, period_end = day_period_bounds(parsed_anchor)
    else:
        raise ValueError("granularity must be one of: day, week, month")
    return period_start.astimezone(UTC), period_end.astimezone(UTC)


def _parse_stream_names(value: str) -> list[str]:
    streams = sorted(
        {
            token
            for token in (
                str(part or "").strip() for part in str(value or "").split(",")
            )
            if token
        }
    )
    if not streams:
        raise ValueError("at least one stream name is required")
    return streams


def _min_relevance_score_for_scope(*, settings: Any | None, scope: str) -> float:
    fallback = float(getattr(settings, "min_relevance_score", 0.0) or 0.0)
    if settings is None or scope == "default":
        return fallback
    runtime_builder = getattr(settings, "topic_stream_runtimes", None)
    if not callable(runtime_builder):
        return fallback
    try:
        runtimes = runtime_builder()
    except Exception:
        return fallback
    if not isinstance(runtimes, list):
        return fallback
    for stream in runtimes:
        if str(getattr(stream, "name", "") or "").strip() != scope:
            continue
        return float(
            getattr(stream, "min_relevance_score", fallback)
            if getattr(stream, "min_relevance_score", None) is not None
            else fallback
        )
    return fallback


def _llm_provider_from_model(model: str) -> str:
    normalized = str(model or "").strip()
    if not normalized:
        return "unknown"
    if "/" not in normalized:
        return "unknown"
    provider, _ = normalized.split("/", 1)
    return provider or "unknown"


def _llm_connection_payload(*, settings: Any) -> dict[str, Any]:
    mask_value = cli._import_symbol("recoleta.observability", attr_name="mask_value")
    llm_connection_from_settings = cli._import_symbol(
        "recoleta.llm_connection",
        attr_name="llm_connection_from_settings",
    )
    connection = llm_connection_from_settings(settings)
    api_key = getattr(connection, "api_key", None)
    base_url = getattr(connection, "base_url", None)
    return {
        "api_key": {
            "configured": api_key is not None,
            "env_var": "RECOLETA_LLM_API_KEY",
            "env_present": bool(str(os.getenv("RECOLETA_LLM_API_KEY", "")).strip()),
            "fingerprint": mask_value(api_key) if api_key is not None else None,
        },
        "base_url": {
            "configured": base_url is not None,
            "value": base_url,
            "env_var": "RECOLETA_LLM_BASE_URL",
            "env_present": bool(str(os.getenv("RECOLETA_LLM_BASE_URL", "")).strip()),
        },
    }


def _build_llm_diagnostics_payload(
    *,
    settings: Any,
    ping_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    connection_payload = _llm_connection_payload(settings=settings)
    issues: list[str] = []
    if not connection_payload["api_key"]["configured"]:
        issues.append("missing_api_key")
    return {
        "ready": not issues,
        "issues": issues,
        "model": str(getattr(settings, "llm_model", "") or ""),
        "provider": _llm_provider_from_model(str(getattr(settings, "llm_model", "") or "")),
        "output_language": str(getattr(settings, "llm_output_language", "") or "") or None,
        "config_path": cli._path_or_none(getattr(settings, "config_path", None)),
        "connection": connection_payload,
        "ping": ping_payload or {"status": "skipped"},
    }


def _run_llm_ping(*, settings: Any, timeout_seconds: float) -> dict[str, Any]:
    analyzer_module = cli._import_symbol("recoleta.analyzer")
    llm_connection_from_settings = cli._import_symbol(
        "recoleta.llm_connection",
        attr_name="llm_connection_from_settings",
    )
    connection = llm_connection_from_settings(settings)
    api_key = getattr(connection, "api_key", None)
    if api_key is None:
        return {
            "status": "failed",
            "error_type": "MissingConfiguration",
            "error_message": "RECOLETA_LLM_API_KEY is not configured",
        }

    completion = analyzer_module._get_completion()
    messages = [
        {"role": "system", "content": "Reply with the single word pong."},
        {"role": "user", "content": "ping"},
    ]
    started = time.perf_counter()
    try:
        response = completion(
            model=str(getattr(settings, "llm_model", "") or ""),
            messages=messages,
            max_tokens=8,
            timeout=float(timeout_seconds),
            **connection.litellm_completion_kwargs(),
        )
    except Exception as exc:  # noqa: BLE001
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        sanitize = getattr(analyzer_module, "_sanitize_error_message")
        return {
            "status": "failed",
            "elapsed_ms": elapsed_ms,
            "error_type": type(exc).__name__,
            "error_message": sanitize(str(exc)),
        }

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    usage = analyzer_module._extract_usage_dict(response)
    prompt_tokens, completion_tokens, total_tokens = (
        analyzer_module._extract_token_counts(usage)
    )
    cost_usd = analyzer_module._resolve_response_cost_usd(
        response=response,
        model=str(getattr(settings, "llm_model", "") or ""),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    resolved_model = (
        str(response.get("model") or "").strip()
        if isinstance(response, dict)
        else str(getattr(response, "model", "") or "").strip()
    )
    return {
        "status": "ok",
        "elapsed_ms": elapsed_ms,
        "resolved_model": resolved_model or str(getattr(settings, "llm_model", "") or ""),
        "response_excerpt": analyzer_module._extract_content(response)[:200],
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost_usd,
        "usage": usage,
    }


def _doctor_ping_attempted_request(ping_payload: dict[str, Any]) -> bool:
    status = str(ping_payload.get("status", "") or "").strip().lower()
    if status == "ok":
        return True
    error_type = str(ping_payload.get("error_type", "") or "").strip()
    return status == "failed" and error_type not in {"", "MissingConfiguration"}


def _record_doctor_llm_metrics(
    *,
    repository: Any,
    run_id: str,
    ping_payload: dict[str, Any],
) -> None:
    attempted_request = _doctor_ping_attempted_request(ping_payload)
    if attempted_request:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.requests_total",
            value=1,
            unit="count",
        )
    prompt_tokens = ping_payload.get("prompt_tokens")
    if isinstance(prompt_tokens, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.input_tokens_total",
            value=float(prompt_tokens),
            unit="count",
        )
    completion_tokens = ping_payload.get("completion_tokens")
    if isinstance(completion_tokens, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.output_tokens_total",
            value=float(completion_tokens),
            unit="count",
        )
    cost_usd = ping_payload.get("cost_usd")
    if isinstance(cost_usd, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.estimated_cost_usd",
            value=float(cost_usd),
            unit="usd",
        )
    elif attempted_request:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.cost_missing_total",
            value=1,
            unit="count",
        )
    elapsed_ms = ping_payload.get("elapsed_ms")
    if isinstance(elapsed_ms, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.doctor.llm.duration_ms",
            value=float(elapsed_ms),
            unit="ms",
        )


def run_gc_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    prune_caches: bool,
    dry_run: bool,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()

    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(
            "[green]gc completed[/green] "
            f"deleted_artifacts=0 deleted_runs=0 path={resolved}"
        )
        return

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="gc",
        log_module="cli.gc",
    )
    try:
        settings: Any | None = None
        filesystem_cache_pruning = "available"
        try:
            settings = cli._maybe_load_settings(
                db_path_option=db_path,
                config_path_option=config_path,
                resolved_db_path=resolved,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "GC settings unavailable; filesystem cache pruning skipped error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            settings = None
            filesystem_cache_pruning = "skipped"
        else:
            if prune_caches and settings is None:
                filesystem_cache_pruning = "skipped"

        reference_now = datetime.now(UTC)
        debug_cutoff = reference_now - timedelta(days=cli._GC_DEBUG_RETENTION_DAYS)
        operational_cutoff = reference_now - timedelta(
            days=cli._GC_OPERATIONAL_RETENTION_DAYS
        )

        artifact_result = repository.prune_artifacts_older_than(
            older_than=debug_cutoff,
            dry_run=dry_run,
        )
        operational_result = repository.prune_operational_history_older_than(
            older_than=operational_cutoff,
            dry_run=dry_run,
        )
        pdf_debug_deleted = (
            cli._prune_expired_pdf_debug_dirs(
                settings=settings,
                older_than=(None if prune_caches else debug_cutoff),
                dry_run=dry_run,
            )
            if settings is not None
            else 0
        )

        chunk_cache_result = (
            repository.clear_document_chunk_cache(dry_run=dry_run)
            if prune_caches
            else None
        )
        lancedb_tables_deleted = (
            cli._prune_inactive_lancedb_tables(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )
        trend_pdfs_deleted = (
            cli._prune_trend_pdfs(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )
        site_outputs_deleted = (
            cli._prune_managed_site_outputs(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )

        counter_prefix = "would_delete" if dry_run else "deleted"
        heartbeat_monitor.raise_if_failed()
        log.info(
            "GC completed artifact_rows={} artifact_paths={} missing_artifact_paths={} run_rows={} metric_rows={} pdf_debug_dirs={} document_chunks={} chunk_embeddings={} chunk_fts_rows={} lancedb_tables={} trend_pdfs={} site_outputs={} dry_run={}",
            artifact_result.artifact_rows,
            artifact_result.deleted_paths,
            artifact_result.missing_paths,
            operational_result.run_rows,
            operational_result.metric_rows,
            pdf_debug_deleted,
            int((chunk_cache_result.document_chunks if chunk_cache_result else 0)),
            int((chunk_cache_result.chunk_embeddings if chunk_cache_result else 0)),
            int((chunk_cache_result.chunk_fts_rows if chunk_cache_result else 0)),
            lancedb_tables_deleted,
            trend_pdfs_deleted,
            site_outputs_deleted,
            dry_run,
        )
        filesystem_segment = (
            f" filesystem_cache_pruning={filesystem_cache_pruning}"
            if prune_caches
            else ""
        )
        console.print(
            f"[green]gc completed[/green] "
            f"{counter_prefix}_artifacts={artifact_result.artifact_rows} "
            f"{counter_prefix}_artifact_paths={artifact_result.deleted_paths} "
            f"{counter_prefix}_missing_artifact_paths={artifact_result.missing_paths} "
            f"{counter_prefix}_runs={operational_result.run_rows} "
            f"{counter_prefix}_metrics={operational_result.metric_rows} "
            f"{counter_prefix}_pdf_debug_dirs={pdf_debug_deleted} "
            f"{counter_prefix}_document_chunks={int((chunk_cache_result.document_chunks if chunk_cache_result else 0))} "
            f"{counter_prefix}_chunk_embeddings={int((chunk_cache_result.chunk_embeddings if chunk_cache_result else 0))} "
            f"{counter_prefix}_chunk_fts_rows={int((chunk_cache_result.chunk_fts_rows if chunk_cache_result else 0))} "
            f"{counter_prefix}_lancedb_tables={lancedb_tables_deleted} "
            f"{counter_prefix}_trend_pdfs={trend_pdfs_deleted} "
            f"{counter_prefix}_site_outputs={site_outputs_deleted} "
            f"{filesystem_segment}"
            f"path={resolved}"
        )
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_repair_streams_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    anchor_date: str,
    streams: str,
    json_output: bool,
    command_name: str = "repair streams",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.repair_streams", json=json_output)

    def _exit_with_error(message: str, *, code: int = 1) -> NoReturn:
        log.warning("{} failed error={}", command_name, message)
        if json_output:
            cli.typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
        raise cli.typer.Exit(code=code)

    try:
        normalized_streams = _parse_stream_names(streams)
        period_start, period_end = _period_bounds_for_granularity(
            anchor_date=anchor_date,
            granularity="day",
        )
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path,
            config_path=config_path,
        )
    except Exception as exc:  # noqa: BLE001
        _exit_with_error(str(exc))

    if not resolved_db_path.exists():
        _exit_with_error(f"db does not exist: {resolved_db_path}")

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        repository.init_schema()
    except Exception as exc:
        _exit_with_error(str(exc))

    owner_token, lease_log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command=command_name,
        log_module="cli.repair_streams",
    )
    try:
        payload = repository.repair_stream_states_for_period(
            period_start=period_start,
            period_end=period_end,
            streams=normalized_streams,
        )
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=lease_log,
        )

    payload["status"] = "ok"
    if json_output:
        cli.typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return

    console.print(
        f"[green]{command_name} completed[/green] "
        f"period_start={payload['period_start']} "
        f"period_end={payload['period_end']} "
        f"item_total={payload['item_total']} "
        f"candidate_total={payload['candidate_total']} "
        f"inserted={payload['inserted_total']} "
        f"updated={payload['updated_total']} "
        f"unchanged={payload['unchanged_total']}"
    )
    console.print("streams=" + ",".join(payload["streams"]))


def run_doctor_why_empty_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    anchor_date: str,
    granularity: str,
    stream: str,
    min_relevance_score: float | None,
    json_output: bool,
    command_name: str = "doctor why-empty",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.doctor.why_empty", json=json_output)

    def _exit_with_error(message: str, *, code: int = 1) -> NoReturn:
        log.warning("{} failed error={}", command_name, message)
        if json_output:
            cli.typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
        raise cli.typer.Exit(code=code)

    try:
        period_start, period_end = _period_bounds_for_granularity(
            anchor_date=anchor_date,
            granularity=granularity,
        )
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path,
            config_path=config_path,
        )
    except Exception as exc:  # noqa: BLE001
        _exit_with_error(str(exc))

    if not resolved_db_path.exists():
        _exit_with_error(f"db does not exist: {resolved_db_path}")

    settings: Any | None = None
    if cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "{} settings load skipped error_type={} error={}",
                command_name,
                type(exc).__name__,
                str(exc),
            )

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        repository.ensure_schema_current()
    except Exception as exc:
        _exit_with_error(str(exc))

    normalized_scope = str(stream or "").strip() or "default"
    effective_min_relevance = (
        float(min_relevance_score)
        if min_relevance_score is not None
        else _min_relevance_score_for_scope(
            settings=settings,
            scope=normalized_scope,
        )
    )
    payload = repository.diagnose_corpus_window(
        period_start=period_start,
        period_end=period_end,
        scope=normalized_scope,
        min_relevance_score=effective_min_relevance,
    )
    payload["status"] = "ok"
    payload["granularity"] = str(granularity or "").strip().lower()

    if json_output:
        cli.typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return

    console.print(f"[green]{command_name}[/green]")
    console.print(
        f"scope={payload['scope']} granularity={payload['granularity']} "
        f"period_start={payload['period_start']} period_end={payload['period_end']}"
    )
    console.print(
        f"candidate_total={payload['candidate_total']} "
        f"selected_total={payload['selected_total']} "
        f"filtered_out_total={payload['filtered_out_total']} "
        f"indexed_item_docs_total={payload['indexed_item_docs_total']}"
    )
    if payload["item_states"]:
        console.print(
            "item_states="
            + " ".join(
                f"{name}={count}" for name, count in payload["item_states"].items()
            )
        )
    if payload["stream_states"]:
        console.print(
            "stream_states="
            + " ".join(
                f"{name}={count}" for name, count in payload["stream_states"].items()
            )
        )
    if payload["exclusion_reasons"]:
        console.print(
            "exclusion_reasons="
            + " ".join(
                f"{name}={count}"
                for name, count in payload["exclusion_reasons"].items()
            )
        )
    for sample in payload["excluded_samples"]:
        console.print(
            "excluded_sample="
            + f"id={sample['item_id']} "
            + f"title={sample['title']} "
            + f"reasons={','.join(sample['reasons'])}"
        )


def run_vacuum_command(*, db_path: Path | None, config_path: Path | None) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise cli.typer.Exit(code=2)

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="vacuum",
        log_module="cli.vacuum",
    )
    try:
        repository.vacuum()
        heartbeat_monitor.raise_if_failed()
        log.info("VACUUM completed path={}", str(resolved))
        console.print(f"[green]vacuum completed[/green] path={resolved}")
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_backup_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    output_dir: Path | None,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise cli.typer.Exit(code=2)

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="backup",
        log_module="cli.backup",
    )
    try:
        bundle_root = (
            output_dir.expanduser().resolve()
            if output_dir is not None
            else (resolved.parent / "backups").resolve()
        )
        result = repository.backup_database(output_dir=bundle_root)
        heartbeat_monitor.raise_if_failed()
        log.info(
            "Backup completed bundle_dir={} manifest_path={} schema_version={}",
            str(result.bundle_dir),
            str(result.manifest_path),
            result.schema_version,
        )
        console.print(
            "[green]backup completed[/green] "
            f"bundle={result.bundle_dir} schema_version={result.schema_version}"
        )
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_restore_command(
    *,
    bundle: Path,
    db_path: Path | None,
    config_path: Path | None,
    yes: bool,
) -> None:
    if not yes:
        cli.typer.echo("refusing to restore db without --yes")
        raise cli.typer.Exit(code=2)

    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.restore")

    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    lease_repository: Any | None = None
    lease_owner_token: str | None = None
    lease_heartbeat_monitor: Any | None = None
    try:
        if resolved.exists():
            lease_repository = cli._build_repository_for_db_path(db_path=resolved)
            assert lease_repository is not None
            lease_repository.init_schema()
            lease_owner_token, _, lease_heartbeat_monitor = (
                cli._acquire_workspace_lease_for_command(
                    repository=lease_repository,
                    console=console,
                    command="restore",
                    log_module="cli.restore",
                )
            )
        result = cli._build_repository_for_db_path(db_path=resolved).restore_database(
            bundle_dir=bundle,
            db_path=resolved,
        )
        if lease_heartbeat_monitor is not None:
            lease_heartbeat_monitor.raise_if_failed()
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Restore failed bundle={} path={} error_type={} error={}",
            str(bundle),
            str(resolved),
            type(exc).__name__,
            str(exc),
        )
        console.print(f"[red]restore failed[/red] {exc}")
        raise cli.typer.Exit(code=1) from exc
    finally:
        if (
            lease_repository is not None
            and lease_owner_token is not None
            and lease_heartbeat_monitor is not None
        ):
            cli._cleanup_workspace_lease(
                repository=lease_repository,
                owner_token=lease_owner_token,
                heartbeat_monitor=lease_heartbeat_monitor,
                log=log,
            )

    log.info(
        "Restore completed bundle_dir={} path={} schema_version={}",
        str(result.bundle_dir),
        str(result.database_path),
        result.schema_version,
    )
    console.print(
        "[green]restore completed[/green] "
        f"bundle={result.bundle_dir} path={result.database_path} schema_version={result.schema_version}"
    )


def run_stats_command(
    *,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
    command_name: str = "stats",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.stats", json=json_output)

    def _exit_with_error(message: str, *, code: int = 1) -> NoReturn:
        log.warning("Stats failed db_path={} error={}", resolved_db_path, message)
        if json_output:
            cli.typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
        raise cli.typer.Exit(code=code)

    resolved_db_path: Path | None = None
    try:
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path, config_path=config_path
        )
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        log.warning(message)
        if json_output:
            cli.typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
        raise cli.typer.Exit(code=1) from exc

    if not resolved_db_path.exists():
        _exit_with_error(f"db does not exist: {resolved_db_path}")

    settings: Any | None = None
    settings_status = "skipped"
    workspace_bytes: dict[str, int | None] = {}
    if cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
            settings_status = "ok"
            workspace_bytes = cli._workspace_bytes_from_settings(settings)
        except Exception as exc:  # noqa: BLE001
            settings_status = "failed"
            log.warning(
                "Stats settings load failed db_path={} error_type={} error={}",
                resolved_db_path,
                type(exc).__name__,
                str(exc),
            )

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        schema_version = repository.ensure_schema_current()
    except Exception as exc:
        _exit_with_error(str(exc))

    reference_now = datetime.now(UTC)
    snapshot = repository.collect_workspace_stats(
        stale_after_seconds=cli._WORKSPACE_LEASE_TIMEOUT_SECONDS,
        now=reference_now,
    )
    lease_state = "unavailable"
    lease_payload: dict[str, Any] = {
        "state": "unavailable",
        "holder_command": None,
        "holder_run_id": None,
        "holder_pid": None,
        "holder_hostname": None,
        "expires_at": None,
    }
    if repository.has_table("workspace_leases"):
        lease = repository.get_workspace_lease()
        if lease is None:
            lease_state = "free"
            lease_payload["state"] = lease_state
        else:
            lease_state = "held"
            lease_payload = {
                "state": lease_state,
                "holder_command": lease.command,
                "holder_run_id": lease.run_id,
                "holder_pid": lease.pid,
                "holder_hostname": lease.hostname,
                "expires_at": (
                    lease.expires_at.isoformat()
                    if lease.expires_at is not None
                    else None
                ),
            }

    oldest_unfinished_at = cli._normalize_utc_datetime(snapshot.oldest_unfinished_at)
    oldest_unfinished_age_seconds: int | None = None
    if oldest_unfinished_at is not None:
        oldest_unfinished_age_seconds = max(
            0,
            int((reference_now - oldest_unfinished_at).total_seconds()),
        )
    latest_successful_run_at = cli._normalize_utc_datetime(
        snapshot.latest_successful_run_at
    )
    latest_successful_run_age_seconds: int | None = None
    if latest_successful_run_at is not None:
        latest_successful_run_age_seconds = max(
            0,
            int((reference_now - latest_successful_run_at).total_seconds()),
        )
    source_diagnostics = _build_source_diagnostics_payload(
        repository=repository,
        settings=settings,
        reference_now=reference_now,
    )

    payload = {
        "status": "ok",
        "db_path": str(resolved_db_path),
        "schema_version": int(schema_version),
        "db_bytes": int(resolved_db_path.stat().st_size),
        "settings": settings_status,
        "items_total": int(sum(snapshot.item_state_counts.values())),
        "items_by_state": snapshot.item_state_counts,
        "unfinished_total": int(snapshot.unfinished_total),
        "oldest_unfinished_age_seconds": oldest_unfinished_age_seconds,
        "runs_by_status": snapshot.run_status_counts,
        "stale_running_runs": int(snapshot.stale_running_runs),
        "latest_successful_run_id": snapshot.latest_successful_run_id,
        "latest_successful_run_at": (
            latest_successful_run_at.isoformat()
            if latest_successful_run_at is not None
            else None
        ),
        "latest_successful_run_age_seconds": latest_successful_run_age_seconds,
        "source_diagnostics": source_diagnostics,
        "lease": lease_payload,
        "workspace_bytes": workspace_bytes,
    }

    if json_output:
        cli.typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return

    item_parts = [
        f"{state}={count}"
        for state, count in payload["items_by_state"].items()
        if int(count) > 0
    ]
    run_parts = [
        f"{state}={count}"
        for state, count in payload["runs_by_status"].items()
        if int(count) > 0
    ]
    console.print(f"[green]{command_name} ok[/green]")
    console.print(f"db={payload['db_path']}")
    console.print(
        f"schema_version={payload['schema_version']} db_bytes={payload['db_bytes']}"
    )
    console.print(f"settings={payload['settings']}")
    console.print(
        f"items_total={payload['items_total']} unfinished_total={payload['unfinished_total']}"
    )
    console.print("items_by_state=" + (" ".join(item_parts) if item_parts else "none"))
    console.print(
        "oldest_unfinished_age_seconds="
        + (
            str(payload["oldest_unfinished_age_seconds"])
            if payload["oldest_unfinished_age_seconds"] is not None
            else "none"
        )
    )
    console.print("runs_by_status=" + (" ".join(run_parts) if run_parts else "none"))
    console.print(f"stale_running_runs={payload['stale_running_runs']}")
    console.print(
        "latest_successful_run="
        + (
            " ".join(
                [
                    str(payload["latest_successful_run_id"]),
                    str(payload["latest_successful_run_at"]),
                    f"age_seconds={payload['latest_successful_run_age_seconds']}",
                ]
            )
            if payload["latest_successful_run_id"] is not None
            else "none"
        )
    )
    console.print(
        f"lease={lease_state}"
        + (
            " "
            + " ".join(
                part
                for part in (
                    f"holder_command={lease_payload['holder_command']}"
                    if lease_payload["holder_command"]
                    else "",
                    f"holder_run_id={lease_payload['holder_run_id']}"
                    if lease_payload["holder_run_id"]
                    else "",
                    f"holder_pid={lease_payload['holder_pid']}"
                    if lease_payload["holder_pid"] is not None
                    else "",
                )
                if part
            )
            if lease_state == "held"
            else ""
        )
    )
    if payload["workspace_bytes"]:
        workspace_parts = [
            f"{name}={size if size is not None else 'unavailable'}"
            for name, size in payload["workspace_bytes"].items()
        ]
        console.print("workspace_bytes=" + " ".join(workspace_parts))
    if payload["source_diagnostics"] is not None:
        source_payload = payload["source_diagnostics"]
        console.print(
            "source_diagnostics_run="
            + f"{source_payload['run_id']} status={source_payload['run_status']}"
        )
        source_parts = [
            f"{source_name}={entry['status']}"
            for source_name, entry in source_payload["sources"].items()
            if entry["status"] not in {"disabled", "not_run"}
        ]
        if source_parts:
            console.print("sources=" + " ".join(source_parts))


def run_doctor_command(
    *,
    healthcheck: bool,
    db_path: Path | None,
    config_path: Path | None,
    max_success_age_minutes: int | None,
    command_name: str = "doctor",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.doctor", healthcheck=healthcheck)

    resolved_db_path: Path
    try:
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path, config_path=config_path
        )
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        log.warning(message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
        )
        raise cli.typer.Exit(code=1) from exc

    settings: Any | None = None
    settings_status = "skipped"
    if cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
            settings_status = "ok"
        except Exception as exc:  # noqa: BLE001
            message = f"settings load failed: {exc}"
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
            )
            raise cli.typer.Exit(code=1) from exc

    if not resolved_db_path.exists():
        message = f"db does not exist: {resolved_db_path}"
        log.warning(message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
        )
        raise cli.typer.Exit(code=1)

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        schema_version = repository.ensure_schema_current()
    except Exception as exc:
        message = str(exc)
        log.warning("Schema compatibility check failed error={}", message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
        )
        raise cli.typer.Exit(code=1) from exc

    path_status = "ok"
    if settings is not None:
        paths_to_check = [
            Path(settings.markdown_output_dir),
            Path(settings.rag_lancedb_dir),
        ]
        artifacts_dir = getattr(settings, "artifacts_dir", None)
        if artifacts_dir is not None:
            paths_to_check.append(Path(artifacts_dir))
        failed_paths = [
            path for path in paths_to_check if not cli._is_accessible_path(path)
        ]
        if failed_paths:
            message = "path access failed: " + ", ".join(
                str(path) for path in failed_paths
            )
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
            )
            raise cli.typer.Exit(code=1)
    else:
        path_status = "skipped"

    lease_state = "unavailable"
    lease_details = ""
    if repository.has_table("workspace_leases"):
        lease = repository.get_workspace_lease()
        if lease is None:
            lease_state = "free"
        else:
            lease_state = "held"
            details = [
                f"holder_command={lease.command}" if lease.command else "",
                f"holder_run_id={lease.run_id}" if lease.run_id else "",
                f"holder_pid={lease.pid}" if lease.pid is not None else "",
            ]
            lease_details = " ".join(part for part in details if part)

    latest_run_state = "none"
    latest_successful_run_at: datetime | None = None
    if repository.has_table("runs"):
        snapshot = repository.collect_workspace_stats(
            stale_after_seconds=cli._WORKSPACE_LEASE_TIMEOUT_SECONDS,
            now=datetime.now(UTC),
        )
        latest_successful_run_at = cli._normalize_utc_datetime(
            snapshot.latest_successful_run_at
        )
        runs = repository.list_recent_runs(limit=1)
        if runs:
            latest_run = runs[0]
            latest_run_state = f"{latest_run.status}:{latest_run.id}"

    if max_success_age_minutes is not None:
        threshold_seconds = int(max_success_age_minutes) * 60
        if latest_successful_run_at is None:
            message = "latest successful run is too old: no successful runs recorded"
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
            )
            raise cli.typer.Exit(code=1)
        age_seconds = max(
            0,
            int((datetime.now(UTC) - latest_successful_run_at).total_seconds()),
        )
        if age_seconds > threshold_seconds:
            message = (
                "latest successful run is too old: "
                f"age_seconds={age_seconds} threshold_seconds={threshold_seconds}"
            )
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else command_name + ' failed'}[/red] {message}"
            )
            raise cli.typer.Exit(code=1)

    if healthcheck:
        console.print(
            "[green]healthcheck ok[/green] "
            f"schema_version={schema_version} "
            f"settings={settings_status} "
            f"paths={path_status} "
            f"lease={lease_state} "
            f"latest_run={latest_run_state}"
            + (f" {lease_details}" if lease_details else "")
        )
        return

    console.print(f"[green]{command_name} ok[/green]")
    console.print(f"db={resolved_db_path}")
    console.print(f"schema_version={schema_version}")
    console.print(f"settings={settings_status}")
    console.print(f"paths={path_status}")
    console.print(
        f"lease={lease_state}" + (f" {lease_details}" if lease_details else "")
    )
    console.print(f"latest_run={latest_run_state}")


def run_doctor_llm_command(
    *,
    ping: bool,
    timeout_seconds: float,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
    command_name: str = "doctor llm",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.doctor.llm", ping=ping, json=json_output)

    try:
        settings = cli._build_settings(
            config_path=config_path,
            db_path=db_path,
        )
    except Exception as exc:  # noqa: BLE001
        message = f"settings load failed: {exc}"
        log.warning(message)
        if json_output:
            cli._emit_json({"status": "error", "error": message})
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
        raise cli.typer.Exit(code=1) from exc

    repository: Any | None = None
    run_id: str | None = None
    billing: dict[str, Any] | None = None
    if ping:
        raw_db_path = getattr(settings, "recoleta_db_path", None)
        if raw_db_path is None:
            message = "settings do not expose recoleta_db_path"
            log.warning(message)
            if json_output:
                cli._emit_json({"status": "error", "error": message})
            else:
                console.print(f"[red]{command_name} failed[/red] {message}")
            raise cli.typer.Exit(code=1)
        try:
            repository = cast(
                Any,
                cli._build_repository_for_db_path(db_path=Path(raw_db_path)),
            )
            assert repository is not None
            repository.init_schema()
            run_id, log = cli._begin_observed_run_for_settings(
                settings=settings,
                repository=repository,
                command=command_name,
                log_module="cli.doctor.llm",
            )
        except Exception as exc:  # noqa: BLE001
            message = f"{command_name} run setup failed: {exc}"
            log.warning(message)
            if json_output:
                cli._emit_json({"status": "error", "error": message})
            else:
                console.print(f"[red]{command_name} failed[/red] {message}")
            raise cli.typer.Exit(code=1) from exc

    try:
        ping_payload = _run_llm_ping(
            settings=settings,
            timeout_seconds=timeout_seconds,
        ) if ping else {"status": "skipped"}
        if repository is not None and run_id is not None:
            _record_doctor_llm_metrics(
                repository=repository,
                run_id=run_id,
                ping_payload=ping_payload,
            )
            repository.finish_run(
                run_id,
                success=str(ping_payload.get("status", "") or "") == "ok",
            )
            try:
                billing = cli._billing_summary_payload(
                    repository.list_metrics(run_id=run_id)
                )
            except Exception as exc:  # noqa: BLE001
                log.warning(
                    "Doctor llm billing metrics load failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
    except Exception as exc:  # noqa: BLE001
        if repository is not None and run_id is not None:
            try:
                repository.finish_run(run_id, success=False)
            except Exception:
                log.exception("Doctor llm run finish failed during error handling")
        message = f"llm ping failed: {exc}"
        log.warning(message)
        if json_output:
            cli._emit_json(
                {
                    "status": "error",
                    "error": message,
                    "run_id": run_id,
                    "billing": billing,
                }
            )
        else:
            console.print(f"[red]{command_name} failed[/red] {message}")
            if repository is not None and run_id is not None:
                cli._print_billing_report(
                    console=console,
                    repository=repository,
                    run_id=run_id,
                )
        raise cli.typer.Exit(code=1) from exc
    payload = _build_llm_diagnostics_payload(
        settings=settings,
        ping_payload=ping_payload,
    )

    if ping and str(ping_payload.get("status", "") or "") != "ok":
        message = "llm ping failed"
        log.warning(
            "LLM ping failed model={} provider={} error_type={} error={}",
            payload["model"],
            payload["provider"],
            ping_payload.get("error_type"),
            ping_payload.get("error_message"),
        )
        if json_output:
            cli._emit_json(
                {
                    "status": "error",
                    "error": message,
                    "run_id": run_id,
                    "billing": billing,
                    "diagnostics": payload,
                }
            )
        else:
            console.print(
                f"[red]{command_name} failed[/red] "
                f"{message} error_type={ping_payload.get('error_type')} "
                f"error={ping_payload.get('error_message')}"
            )
            if repository is not None and run_id is not None:
                cli._print_billing_report(
                    console=console,
                    repository=repository,
                    run_id=run_id,
                )
        raise cli.typer.Exit(code=1)

    if json_output:
        output_payload: dict[str, Any] = {"status": "ok", **payload}
        if ping:
            output_payload["run_id"] = run_id
            output_payload["billing"] = billing
        cli._emit_json(output_payload)
        return

    console.print(
        f"[green]{command_name} ok[/green] "
        f"ready={str(payload['ready']).lower()} "
        f"provider={payload['provider']} model={payload['model']}"
    )
    console.print(
        "api_key="
        + (
            f"configured fingerprint={payload['connection']['api_key']['fingerprint']}"
            if payload["connection"]["api_key"]["configured"]
            else "missing"
        )
        + (
            " env_present=true"
            if payload["connection"]["api_key"]["env_present"]
            else " env_present=false"
        )
    )
    console.print(
        "base_url="
        + (
            str(payload["connection"]["base_url"]["value"])
            if payload["connection"]["base_url"]["configured"]
            else "default"
        )
        + (
            " env_present=true"
            if payload["connection"]["base_url"]["env_present"]
            else " env_present=false"
        )
    )
    if payload["output_language"] is not None:
        console.print(f"output_language={payload['output_language']}")
    if payload["config_path"] is not None:
        console.print(f"config_path={payload['config_path']}")
    if payload["issues"]:
        console.print("issues=" + " ".join(payload["issues"]))
    if ping:
        console.print(
            "ping="
            + " ".join(
                part
                for part in (
                    payload["ping"]["status"],
                    f"elapsed_ms={payload['ping'].get('elapsed_ms')}"
                    if payload["ping"].get("elapsed_ms") is not None
                    else "",
                    f"resolved_model={payload['ping'].get('resolved_model')}"
                    if payload["ping"].get("resolved_model")
                    else "",
                    f"prompt_tokens={payload['ping'].get('prompt_tokens')}"
                    if payload["ping"].get("prompt_tokens") is not None
                    else "",
                    f"completion_tokens={payload['ping'].get('completion_tokens')}"
                    if payload["ping"].get("completion_tokens") is not None
                    else "",
                )
                if part
            )
        )
    if repository is not None and run_id is not None:
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
