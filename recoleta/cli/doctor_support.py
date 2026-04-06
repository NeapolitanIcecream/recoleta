from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
import time
from typing import Any

import recoleta.cli as cli

_SOURCE_DIAGNOSTIC_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")


@dataclass(frozen=True, slots=True)
class GcPayloadRequest:
    repository: Any
    settings: Any | None
    prune_caches: bool
    dry_run: bool
    reference_now: datetime
    filesystem_cache_pruning: str


@dataclass(frozen=True, slots=True)
class StatsPayloadRequest:
    repository: Any
    resolved_db_path: Path
    settings: Any | None
    settings_status: str
    workspace_bytes: dict[str, int | None]
    reference_now: datetime


def _age_seconds(reference_now: datetime, value: datetime | None) -> int | None:
    if value is None:
        return None
    return max(0, int((reference_now - value).total_seconds()))


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
    if settings is None or getattr(settings, "sources", None) is None:
        return {source_name: None for source_name in _SOURCE_DIAGNOSTIC_NAMES}
    enabled: dict[str, bool | None] = {}
    for source_name in _SOURCE_DIAGNOSTIC_NAMES:
        source_config = getattr(settings.sources, source_name, None)
        enabled[source_name] = (
            bool(getattr(source_config, "enabled", False))
            if source_config is not None
            else None
        )
    return enabled


def _has_source_metrics(metrics: list[Any]) -> bool:
    for metric in metrics:
        metric_name = str(getattr(metric, "name", "") or "")
        if metric_name.startswith("pipeline.ingest.source."):
            return True
        if metric_name.startswith("pipeline.enrich.source."):
            return True
    return False


def _latest_source_metrics_run(*, repository: Any) -> tuple[Any, list[Any]] | None:
    for run in repository.list_recent_runs(limit=20):
        metrics = repository.list_metrics(run_id=run.id)
        if _has_source_metrics(metrics):
            return run, metrics
    return None


def _source_payloads(*, settings: Any | None) -> dict[str, dict[str, Any]]:
    enabled_by_source = _source_enabled_map(settings)
    return {
        source_name: _default_source_diagnostic_entry(
            enabled=enabled_by_source.get(source_name)
        )
        for source_name in _SOURCE_DIAGNOSTIC_NAMES
    }


def _source_entry(
    *,
    sources_payload: dict[str, dict[str, Any]],
    settings: Any | None,
    source_name: str,
) -> dict[str, Any]:
    normalized = str(source_name or "").strip().lower() or "unknown"
    if normalized not in sources_payload:
        sources_payload[normalized] = _default_source_diagnostic_entry(
            enabled=_source_enabled_map(settings).get(normalized)
        )
    return sources_payload[normalized]


def _apply_ingest_metric(
    *, ingest_payload: dict[str, Any], metric_key: str, metric_value: int
) -> None:
    if metric_key in {"oldest_published_at_unix", "newest_published_at_unix"}:
        if metric_value > 0:
            payload_key = metric_key.removesuffix("_unix")
            ingest_payload[payload_key] = datetime.fromtimestamp(
                metric_value, tz=UTC
            ).isoformat()
        return
    if metric_key in ingest_payload:
        ingest_payload[metric_key] = metric_value


def _apply_enrich_metric(
    *, enrich_payload: dict[str, Any], metric_key: str, metric_value: int
) -> None:
    if metric_key.startswith("content_type.") and metric_key.endswith("_total"):
        content_type = metric_key[len("content_type.") : -len("_total")]
        if content_type:
            enrich_payload["content_types"][content_type] = metric_value
        return
    if metric_key.startswith("pdf_backend.") and metric_key.endswith("_total"):
        backend = metric_key[len("pdf_backend.") : -len("_total")]
        if backend:
            enrich_payload["pdf_backends"][backend] = metric_value
        return
    if metric_key in enrich_payload:
        enrich_payload[metric_key] = metric_value


def _apply_source_metric(
    *,
    sources_payload: dict[str, dict[str, Any]],
    settings: Any | None,
    metric: Any,
) -> None:
    metric_name = str(getattr(metric, "name", "") or "")
    metric_value = int(float(getattr(metric, "value", 0) or 0))
    if metric_name.startswith("pipeline.ingest.source."):
        remainder = metric_name.removeprefix("pipeline.ingest.source.")
        source_name, _, metric_key = remainder.partition(".")
        if metric_key:
            entry = _source_entry(
                sources_payload=sources_payload,
                settings=settings,
                source_name=source_name,
            )
            _apply_ingest_metric(
                ingest_payload=entry["ingest"],
                metric_key=metric_key,
                metric_value=metric_value,
            )
        return
    if not metric_name.startswith("pipeline.enrich.source."):
        return
    remainder = metric_name.removeprefix("pipeline.enrich.source.")
    source_name, _, metric_key = remainder.partition(".")
    if not metric_key:
        return
    entry = _source_entry(
        sources_payload=sources_payload,
        settings=settings,
        source_name=source_name,
    )
    _apply_enrich_metric(
        enrich_payload=entry["enrich"],
        metric_key=metric_key,
        metric_value=metric_value,
    )


def _source_status(entry: dict[str, Any]) -> str:
    enabled = entry.get("enabled")
    ingest_payload = entry["ingest"]
    enrich_payload = entry["enrich"]
    enrich_success_total = int(enrich_payload["processed_total"]) + int(
        enrich_payload["skipped_total"]
    )
    if enabled is False and not _source_observed(
        ingest_payload=ingest_payload,
        enrich_payload=enrich_payload,
        enrich_success_total=enrich_success_total,
    ):
        return "disabled"
    if _source_not_modified(
        ingest_payload=ingest_payload,
        enrich_payload=enrich_payload,
    ):
        return "not_modified"
    if _source_pull_failed(
        ingest_payload=ingest_payload,
        enrich_payload=enrich_payload,
    ):
        return "pull_failed"
    if int(enrich_payload["failed_total"]) > 0:
        return "enrich_failed"
    if enrich_success_total > 0:
        return "ok"
    if int(ingest_payload["drafts_total"]) > 0:
        return "ingested_only"
    return "not_run"


def _source_observed(
    *,
    ingest_payload: dict[str, Any],
    enrich_payload: dict[str, Any],
    enrich_success_total: int,
) -> bool:
    return (
        int(ingest_payload["drafts_total"]) > 0
        or int(ingest_payload["pull_failed_total"]) > 0
        or int(ingest_payload["not_modified_total"]) > 0
        or enrich_success_total > 0
        or int(enrich_payload["failed_total"]) > 0
    )


def _source_not_modified(
    *,
    ingest_payload: dict[str, Any],
    enrich_payload: dict[str, Any],
) -> bool:
    return (
        int(ingest_payload["not_modified_total"]) > 0
        and int(ingest_payload["pull_failed_total"]) <= 0
        and int(enrich_payload["failed_total"]) <= 0
    )


def _source_pull_failed(
    *,
    ingest_payload: dict[str, Any],
    enrich_payload: dict[str, Any],
) -> bool:
    return (
        int(ingest_payload["pull_failed_total"]) > 0
        and int(ingest_payload["drafts_total"]) <= 0
        and int(enrich_payload["failed_total"]) <= 0
    )


def _finalize_source_payloads(*, sources_payload: dict[str, dict[str, Any]]) -> None:
    for entry in sources_payload.values():
        status = _source_status(entry)
        entry["status"] = status
        entry["pipeline_completed"] = bool(status in {"ok", "not_modified"})


def build_source_diagnostics_payload(
    *,
    repository: Any,
    settings: Any | None,
    reference_now: datetime,
) -> dict[str, Any] | None:
    run_with_metrics = _latest_source_metrics_run(repository=repository)
    if run_with_metrics is None:
        return None
    run, metrics = run_with_metrics
    sources_payload = _source_payloads(settings=settings)
    for metric in metrics:
        _apply_source_metric(
            sources_payload=sources_payload,
            settings=settings,
            metric=metric,
        )
    _finalize_source_payloads(sources_payload=sources_payload)
    started_at = cli._normalize_utc_datetime(getattr(run, "started_at", None))
    return {
        "run_id": run.id,
        "run_status": str(getattr(run, "status", "") or ""),
        "started_at": started_at.isoformat() if started_at is not None else None,
        "age_seconds": _age_seconds(reference_now, started_at),
        "sources": sources_payload,
    }


def period_bounds_for_granularity(
    *,
    anchor_date: str,
    granularity: str,
) -> tuple[datetime, datetime]:
    from recoleta.trends import (
        day_period_bounds,
        month_period_bounds,
        week_period_bounds,
    )

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


def default_min_relevance_score(*, settings: Any | None) -> float:
    return float(getattr(settings, "min_relevance_score", 0.0) or 0.0)


def _llm_provider_from_model(model: str) -> str:
    normalized = str(model or "").strip()
    if not normalized or "/" not in normalized:
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


def build_llm_diagnostics_payload(
    *,
    settings: Any,
    ping_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    connection_payload = _llm_connection_payload(settings=settings)
    issues = [] if connection_payload["api_key"]["configured"] else ["missing_api_key"]
    model = str(getattr(settings, "llm_model", "") or "")
    return {
        "ready": not issues,
        "issues": issues,
        "model": model,
        "provider": _llm_provider_from_model(model),
        "output_language": str(getattr(settings, "llm_output_language", "") or "")
        or None,
        "config_path": cli._path_or_none(getattr(settings, "config_path", None)),
        "connection": connection_payload,
        "ping": ping_payload or {"status": "skipped"},
    }


def run_llm_ping(*, settings: Any, timeout_seconds: float) -> dict[str, Any]:
    analyzer_module = cli._import_symbol("recoleta.analyzer")
    llm_connection_from_settings = cli._import_symbol(
        "recoleta.llm_connection",
        attr_name="llm_connection_from_settings",
    )
    connection = llm_connection_from_settings(settings)
    if getattr(connection, "api_key", None) is None:
        return {
            "status": "failed",
            "error_type": "MissingConfiguration",
            "error_message": "RECOLETA_LLM_API_KEY is not configured",
        }

    completion = analyzer_module._get_completion()
    started = time.perf_counter()
    try:
        response = completion(
            model=str(getattr(settings, "llm_model", "") or ""),
            messages=[
                {"role": "system", "content": "Reply with the single word pong."},
                {"role": "user", "content": "ping"},
            ],
            max_tokens=8,
            timeout=float(timeout_seconds),
            **connection.litellm_completion_kwargs(),
        )
    except Exception as exc:  # noqa: BLE001
        sanitize = getattr(analyzer_module, "_sanitize_error_message")
        return {
            "status": "failed",
            "elapsed_ms": int((time.perf_counter() - started) * 1000),
            "error_type": type(exc).__name__,
            "error_message": sanitize(str(exc)),
        }

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
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
        "resolved_model": resolved_model
        or str(getattr(settings, "llm_model", "") or ""),
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


def record_doctor_llm_metrics(
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
    for payload_key, metric_name in (
        ("prompt_tokens", "pipeline.doctor.llm.input_tokens_total"),
        ("completion_tokens", "pipeline.doctor.llm.output_tokens_total"),
        ("elapsed_ms", "pipeline.doctor.llm.duration_ms"),
    ):
        metric_value = ping_payload.get(payload_key)
        if isinstance(metric_value, (int, float)):
            repository.record_metric(
                run_id=run_id,
                name=metric_name,
                value=float(metric_value),
                unit="count" if "tokens" in payload_key else "ms",
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


def load_gc_settings(
    *,
    db_path: Path | None,
    config_path: Path | None,
    resolved_db_path: Path,
    prune_caches: bool,
    log: Any,
) -> tuple[Any | None, str]:
    try:
        settings = cli._maybe_load_settings(
            db_path_option=db_path,
            config_path_option=config_path,
            resolved_db_path=resolved_db_path,
        )
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "GC settings unavailable; filesystem cache pruning skipped error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return None, "skipped"
    if prune_caches and settings is None:
        return None, "skipped"
    return settings, "available"


def _gc_chunk_cache_result(
    *, repository: Any, prune_caches: bool, dry_run: bool
) -> Any | None:
    if not prune_caches:
        return None
    return repository.clear_document_chunk_cache(dry_run=dry_run)


def _gc_filesystem_count(*, enabled: bool, handler: Any) -> int:
    if not enabled:
        return 0
    return int(handler())


def build_gc_payload(*, request: GcPayloadRequest) -> dict[str, Any]:
    debug_cutoff = request.reference_now - timedelta(days=cli._GC_DEBUG_RETENTION_DAYS)
    operational_cutoff = request.reference_now - timedelta(
        days=cli._GC_OPERATIONAL_RETENTION_DAYS
    )
    artifact_result = request.repository.prune_artifacts_older_than(
        older_than=debug_cutoff,
        dry_run=request.dry_run,
    )
    operational_result = request.repository.prune_operational_history_older_than(
        older_than=operational_cutoff,
        dry_run=request.dry_run,
    )
    chunk_cache_result = _gc_chunk_cache_result(
        repository=request.repository,
        prune_caches=request.prune_caches,
        dry_run=request.dry_run,
    )
    return {
        "artifact_rows": artifact_result.artifact_rows,
        "deleted_paths": artifact_result.deleted_paths,
        "missing_paths": artifact_result.missing_paths,
        "run_rows": operational_result.run_rows,
        "metric_rows": operational_result.metric_rows,
        "pdf_debug_deleted": _gc_filesystem_count(
            enabled=request.settings is not None,
            handler=lambda: cli._prune_expired_pdf_debug_dirs(
                settings=request.settings,
                older_than=(None if request.prune_caches else debug_cutoff),
                dry_run=request.dry_run,
            ),
        ),
        "document_chunks": int(
            (chunk_cache_result.document_chunks if chunk_cache_result else 0)
        ),
        "chunk_embeddings": int(
            (chunk_cache_result.chunk_embeddings if chunk_cache_result else 0)
        ),
        "chunk_fts_rows": int(
            (chunk_cache_result.chunk_fts_rows if chunk_cache_result else 0)
        ),
        "lancedb_tables_deleted": _gc_filesystem_count(
            enabled=request.prune_caches and request.settings is not None,
            handler=lambda: cli._prune_inactive_lancedb_tables(
                settings=request.settings,
                dry_run=request.dry_run,
            ),
        ),
        "trend_pdfs_deleted": _gc_filesystem_count(
            enabled=request.prune_caches and request.settings is not None,
            handler=lambda: cli._prune_trend_pdfs(
                settings=request.settings,
                dry_run=request.dry_run,
            ),
        ),
        "site_outputs_deleted": _gc_filesystem_count(
            enabled=request.prune_caches and request.settings is not None,
            handler=lambda: cli._prune_managed_site_outputs(
                settings=request.settings,
                dry_run=request.dry_run,
            ),
        ),
        "filesystem_cache_pruning": request.filesystem_cache_pruning,
    }


def log_gc_completion(*, log: Any, payload: dict[str, Any], dry_run: bool) -> None:
    log.info(
        "GC completed artifact_rows={} artifact_paths={} missing_artifact_paths={} run_rows={} metric_rows={} pdf_debug_dirs={} document_chunks={} chunk_embeddings={} chunk_fts_rows={} lancedb_tables={} trend_pdfs={} site_outputs={} dry_run={}",
        payload["artifact_rows"],
        payload["deleted_paths"],
        payload["missing_paths"],
        payload["run_rows"],
        payload["metric_rows"],
        payload["pdf_debug_deleted"],
        payload["document_chunks"],
        payload["chunk_embeddings"],
        payload["chunk_fts_rows"],
        payload["lancedb_tables_deleted"],
        payload["trend_pdfs_deleted"],
        payload["site_outputs_deleted"],
        dry_run,
    )


def render_gc_summary(
    *,
    console: Any,
    payload: dict[str, Any],
    resolved_db_path: Path,
    dry_run: bool,
    prune_caches: bool,
) -> None:
    counter_prefix = "would_delete" if dry_run else "deleted"
    filesystem_segment = (
        f" filesystem_cache_pruning={payload['filesystem_cache_pruning']}"
        if prune_caches
        else ""
    )
    console.print(
        f"[green]gc completed[/green] "
        f"{counter_prefix}_artifacts={payload['artifact_rows']} "
        f"{counter_prefix}_artifact_paths={payload['deleted_paths']} "
        f"{counter_prefix}_missing_artifact_paths={payload['missing_paths']} "
        f"{counter_prefix}_runs={payload['run_rows']} "
        f"{counter_prefix}_metrics={payload['metric_rows']} "
        f"{counter_prefix}_pdf_debug_dirs={payload['pdf_debug_deleted']} "
        f"{counter_prefix}_document_chunks={payload['document_chunks']} "
        f"{counter_prefix}_chunk_embeddings={payload['chunk_embeddings']} "
        f"{counter_prefix}_chunk_fts_rows={payload['chunk_fts_rows']} "
        f"{counter_prefix}_lancedb_tables={payload['lancedb_tables_deleted']} "
        f"{counter_prefix}_trend_pdfs={payload['trend_pdfs_deleted']} "
        f"{counter_prefix}_site_outputs={payload['site_outputs_deleted']} "
        f"{filesystem_segment}"
        f"path={resolved_db_path}"
    )


def render_why_empty_output(
    *, console: Any, payload: dict[str, Any], command_name: str
) -> None:
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
    for key in ("item_states", "eligible_item_states", "exclusion_reasons"):
        if payload[key]:
            console.print(
                key
                + "="
                + " ".join(f"{name}={count}" for name, count in payload[key].items())
            )
    for sample in payload["excluded_samples"]:
        console.print(
            "excluded_sample="
            + f"id={sample['item_id']} title={sample['title']} "
            + f"reasons={','.join(sample['reasons'])}"
        )


def _lease_payload(*, repository: Any) -> tuple[str, dict[str, Any]]:
    payload: dict[str, Any] = {
        "state": "unavailable",
        "holder_command": None,
        "holder_run_id": None,
        "holder_pid": None,
        "holder_hostname": None,
        "expires_at": None,
    }
    if not repository.has_table("workspace_leases"):
        return "unavailable", payload
    lease = repository.get_workspace_lease()
    if lease is None:
        payload["state"] = "free"
        return "free", payload
    payload.update(
        {
            "state": "held",
            "holder_command": lease.command,
            "holder_run_id": lease.run_id,
            "holder_pid": lease.pid,
            "holder_hostname": lease.hostname,
            "expires_at": lease.expires_at.isoformat()
            if lease.expires_at is not None
            else None,
        }
    )
    return "held", payload


def build_stats_payload(*, request: StatsPayloadRequest) -> dict[str, Any]:
    schema_version = request.repository.ensure_schema_current()
    snapshot = request.repository.collect_workspace_stats(
        stale_after_seconds=cli._WORKSPACE_LEASE_TIMEOUT_SECONDS,
        now=request.reference_now,
    )
    lease_state, lease_payload = _lease_payload(repository=request.repository)
    oldest_unfinished_at = cli._normalize_utc_datetime(snapshot.oldest_unfinished_at)
    latest_successful_run_at = cli._normalize_utc_datetime(
        snapshot.latest_successful_run_at
    )
    return {
        "status": "ok",
        "db_path": str(request.resolved_db_path),
        "schema_version": int(schema_version),
        "db_bytes": int(request.resolved_db_path.stat().st_size),
        "settings": request.settings_status,
        "items_total": int(sum(snapshot.item_state_counts.values())),
        "items_by_state": snapshot.item_state_counts,
        "unfinished_total": int(snapshot.unfinished_total),
        "oldest_unfinished_age_seconds": _age_seconds(
            request.reference_now,
            oldest_unfinished_at,
        ),
        "runs_by_status": snapshot.run_status_counts,
        "stale_running_runs": int(snapshot.stale_running_runs),
        "latest_successful_run_id": snapshot.latest_successful_run_id,
        "latest_successful_run_at": (
            latest_successful_run_at.isoformat()
            if latest_successful_run_at is not None
            else None
        ),
        "latest_successful_run_age_seconds": _age_seconds(
            request.reference_now,
            latest_successful_run_at,
        ),
        "source_diagnostics": build_source_diagnostics_payload(
            repository=request.repository,
            settings=request.settings,
            reference_now=request.reference_now,
        ),
        "lease": lease_payload,
        "lease_state": lease_state,
        "workspace_bytes": request.workspace_bytes,
    }


def render_stats_output(
    *, console: Any, payload: dict[str, Any], command_name: str
) -> None:
    console.print(f"[green]{command_name} ok[/green]")
    console.print(f"db={payload['db_path']}")
    console.print(
        f"schema_version={payload['schema_version']} db_bytes={payload['db_bytes']}"
    )
    console.print(f"settings={payload['settings']}")
    console.print(
        f"items_total={payload['items_total']} unfinished_total={payload['unfinished_total']}"
    )
    console.print("items_by_state=" + _stats_count_parts(payload["items_by_state"]))
    console.print(
        "oldest_unfinished_age_seconds="
        + (
            str(payload["oldest_unfinished_age_seconds"])
            if payload["oldest_unfinished_age_seconds"] is not None
            else "none"
        )
    )
    console.print("runs_by_status=" + _stats_count_parts(payload["runs_by_status"]))
    console.print(f"stale_running_runs={payload['stale_running_runs']}")
    console.print("latest_successful_run=" + _latest_successful_run_segment(payload))
    console.print(_lease_line(payload))
    if payload["workspace_bytes"]:
        console.print(
            "workspace_bytes=" + _workspace_bytes_line(payload["workspace_bytes"])
        )
    _render_source_diagnostics(console=console, payload=payload["source_diagnostics"])


def _stats_count_parts(counts: dict[str, Any]) -> str:
    parts = [f"{state}={count}" for state, count in counts.items() if int(count) > 0]
    return " ".join(parts) if parts else "none"


def _latest_successful_run_segment(payload: dict[str, Any]) -> str:
    if payload["latest_successful_run_id"] is None:
        return "none"
    return " ".join(
        [
            str(payload["latest_successful_run_id"]),
            str(payload["latest_successful_run_at"]),
            f"age_seconds={payload['latest_successful_run_age_seconds']}",
        ]
    )


def _lease_line(payload: dict[str, Any]) -> str:
    return f"lease={payload['lease_state']}" + _lease_details_suffix(payload)


def _lease_details_suffix(payload: dict[str, Any]) -> str:
    if payload["lease_state"] != "held":
        return ""
    details = [
        f"holder_command={payload['lease']['holder_command']}"
        if payload["lease"]["holder_command"]
        else "",
        f"holder_run_id={payload['lease']['holder_run_id']}"
        if payload["lease"]["holder_run_id"]
        else "",
        f"holder_pid={payload['lease']['holder_pid']}"
        if payload["lease"]["holder_pid"] is not None
        else "",
    ]
    rendered = " ".join(part for part in details if part)
    return f" {rendered}" if rendered else ""


def _workspace_bytes_line(workspace_bytes: dict[str, int | None]) -> str:
    return " ".join(
        f"{name}={size if size is not None else 'unavailable'}"
        for name, size in workspace_bytes.items()
    )


def _render_source_diagnostics(*, console: Any, payload: dict[str, Any] | None) -> None:
    if payload is None:
        return
    console.print(
        "source_diagnostics_run="
        + f"{payload['run_id']} status={payload['run_status']}"
    )
    source_parts = [
        f"{source_name}={entry['status']}"
        for source_name, entry in payload["sources"].items()
        if entry["status"] not in {"disabled", "not_run"}
    ]
    if source_parts:
        console.print("sources=" + " ".join(source_parts))


def _path_status(*, settings: Any | None) -> str:
    if settings is None:
        return "skipped"
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
        raise ValueError(
            "path access failed: " + ", ".join(str(path) for path in failed_paths)
        )
    return "ok"


def _doctor_lease_state(*, repository: Any) -> tuple[str, str]:
    if not repository.has_table("workspace_leases"):
        return "unavailable", ""
    lease = repository.get_workspace_lease()
    if lease is None:
        return "free", ""
    details = [
        f"holder_command={lease.command}" if lease.command else "",
        f"holder_run_id={lease.run_id}" if lease.run_id else "",
        f"holder_pid={lease.pid}" if lease.pid is not None else "",
    ]
    return "held", " ".join(part for part in details if part)


def build_doctor_payload(
    *,
    repository: Any,
    resolved_db_path: Path,
    settings: Any | None,
    settings_status: str,
    reference_now: datetime,
) -> dict[str, Any]:
    schema_version = repository.ensure_schema_current()
    lease_state, lease_details = _doctor_lease_state(repository=repository)
    latest_run_state = "none"
    latest_successful_run_at: datetime | None = None
    if repository.has_table("runs"):
        snapshot = repository.collect_workspace_stats(
            stale_after_seconds=cli._WORKSPACE_LEASE_TIMEOUT_SECONDS,
            now=reference_now,
        )
        latest_successful_run_at = cli._normalize_utc_datetime(
            snapshot.latest_successful_run_at
        )
        runs = repository.list_recent_runs(limit=1)
        if runs:
            latest_run = runs[0]
            latest_run_state = f"{latest_run.status}:{latest_run.id}"
    return {
        "db_path": str(resolved_db_path),
        "schema_version": int(schema_version),
        "settings": settings_status,
        "paths": _path_status(settings=settings),
        "lease_state": lease_state,
        "lease_details": lease_details,
        "latest_run_state": latest_run_state,
        "latest_successful_run_at": latest_successful_run_at,
    }


def validate_latest_success_age(
    *,
    payload: dict[str, Any],
    max_success_age_minutes: int | None,
    reference_now: datetime,
) -> None:
    if max_success_age_minutes is None:
        return
    latest_successful_run_at = payload["latest_successful_run_at"]
    if latest_successful_run_at is None:
        raise ValueError(
            "latest successful run is too old: no successful runs recorded"
        )
    age_seconds = _age_seconds(reference_now, latest_successful_run_at)
    threshold_seconds = int(max_success_age_minutes) * 60
    assert age_seconds is not None
    if age_seconds > threshold_seconds:
        raise ValueError(
            "latest successful run is too old: "
            f"age_seconds={age_seconds} threshold_seconds={threshold_seconds}"
        )


def render_doctor_output(
    *,
    console: Any,
    payload: dict[str, Any],
    command_name: str,
    healthcheck: bool,
) -> None:
    if healthcheck:
        console.print(
            "[green]healthcheck ok[/green] "
            f"schema_version={payload['schema_version']} "
            f"settings={payload['settings']} "
            f"paths={payload['paths']} "
            f"lease={payload['lease_state']} "
            f"latest_run={payload['latest_run_state']}"
            + (f" {payload['lease_details']}" if payload["lease_details"] else "")
        )
        return
    console.print(f"[green]{command_name} ok[/green]")
    console.print(f"db={payload['db_path']}")
    console.print(f"schema_version={payload['schema_version']}")
    console.print(f"settings={payload['settings']}")
    console.print(f"paths={payload['paths']}")
    console.print(
        f"lease={payload['lease_state']}"
        + (f" {payload['lease_details']}" if payload["lease_details"] else "")
    )
    console.print(f"latest_run={payload['latest_run_state']}")
