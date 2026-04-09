from __future__ import annotations

from dataclasses import dataclass
import json
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, cast

from loguru import logger

from recoleta import trends
from recoleta.idea_projection import (
    IdeaProjectionRequest,
    persist_idea_document_projection,
)
from recoleta.pipeline.metrics import metric_token
from recoleta.pipeline.pass_runner import (
    PassDefinition,
    PassPersistSpec,
    ProjectionSpec,
    run_pass_definition,
)
from recoleta.passes import (
    PassInputRef,
    PassStatus,
    TREND_SYNTHESIS_PASS_KIND,
    TrendIdeasPayload,
    build_empty_trend_ideas_payload,
    build_suppressed_trend_ideas_payload,
    build_trend_ideas_pass_output,
    build_trend_snapshot_pack_md,
    normalize_trend_ideas_payload,
)
from recoleta.rag import ideas_agent
from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name
from recoleta.trends import TrendPayload
from recoleta.types import IdeasResult, utc_now


@dataclass(frozen=True, slots=True)
class IdeasStageContext:
    service: Any
    run_id: str
    log: Any
    started: float
    normalized_granularity: str
    period_start: datetime
    period_end: datetime
    record_metric: Any
    include_debug: bool
    llm_model: str | None


@dataclass(frozen=True, slots=True)
class IdeasUpstreamResult:
    upstream_pass_output_id: int
    upstream_empty_corpus: bool
    trend_payload: TrendPayload
    trend_snapshot_pack_md: str


@dataclass(frozen=True, slots=True)
class IdeasGenerationRequest:
    context: IdeasStageContext
    trend_payload: TrendPayload
    trend_snapshot_pack_md: str
    upstream_empty_corpus: bool


@dataclass(frozen=True, slots=True)
class IdeasProjectionContext:
    context: IdeasStageContext
    targets: set[str]
    status: PassStatus
    payload: TrendIdeasPayload
    trend_payload: TrendPayload
    upstream_pass_output_id: int


@dataclass(frozen=True, slots=True)
class IdeasDebugArtifactRequest:
    service: Any
    run_id: str
    upstream_pass_output_id: int
    status: PassStatus
    trend_snapshot_pack_md: str
    ideas_payload: TrendIdeasPayload
    debug: dict[str, Any]


@dataclass(frozen=True, slots=True)
class IdeasPassDefinitionRequest:
    context: IdeasStageContext
    payload: TrendIdeasPayload
    status: PassStatus
    trend_payload: TrendPayload
    upstream_pass_output_id: int
    debug: dict[str, Any]
    targets: set[str]


def _trend_metric_name(name: str) -> str:
    return str(name or "").strip()


def _period_bounds_for_granularity(
    *, granularity: str, anchor: date
) -> tuple[datetime, datetime]:
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity == "week":
        return trends.week_period_bounds(anchor)
    if normalized_granularity == "month":
        return trends.month_period_bounds(anchor)
    return trends.day_period_bounds(anchor)


def _load_trend_payload_from_pass_output(row: Any) -> TrendPayload:
    payload_json = str(getattr(row, "payload_json", "") or "{}")
    return TrendPayload.model_validate(json.loads(payload_json))


def _truthy_flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value or "").strip().lower()
    return normalized in {"1", "true", "yes", "on"}


def _trend_pass_output_has_empty_corpus(row: Any) -> bool:
    try:
        diagnostics = json.loads(str(getattr(row, "diagnostics_json", "") or "{}"))
    except Exception:
        diagnostics = {}
    if isinstance(diagnostics, dict):
        if _truthy_flag(diagnostics.get("empty_corpus")):
            return True
        debug = diagnostics.get("debug")
        if isinstance(debug, dict) and _truthy_flag(debug.get("empty_corpus")):
            return True
    try:
        payload = _load_trend_payload_from_pass_output(row)
    except Exception:
        return False
    return trends.is_empty_trend_payload(payload)


def _build_metric_recorder(*, service: Any, run_id: str):
    def record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        service.repository.record_metric(
            run_id=run_id,
            name=_trend_metric_name(name),
            value=value,
            unit=unit,
        )

    return record_metric


def _load_upstream_context(context: IdeasStageContext) -> IdeasUpstreamResult:
    upstream = context.service.repository.get_latest_pass_output(
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        status=PassStatus.SUCCEEDED.value,
        granularity=context.normalized_granularity,
        period_start=context.period_start,
        period_end=context.period_end,
    )
    if upstream is None or getattr(upstream, "id", None) is None:
        context.record_metric(
            name="pipeline.trends.pass.ideas.upstream_missing_total",
            value=1,
            unit="count",
        )
        context.record_metric(
            name="pipeline.trends.pass.ideas.duration_ms",
            value=int((time.perf_counter() - context.started) * 1000),
            unit="ms",
        )
        raise RuntimeError(
            "Missing trend_synthesis pass output for "
            f"granularity={context.normalized_granularity} "
            f"period_start={context.period_start.isoformat()} "
            f"period_end={context.period_end.isoformat()}"
        )

    upstream_pass_output_id = int(getattr(upstream, "id"))
    upstream_empty_corpus = _trend_pass_output_has_empty_corpus(upstream)
    trend_payload = _load_trend_payload_from_pass_output(upstream)
    trend_snapshot_pack_md = build_trend_snapshot_pack_md(
        trend_payload=trend_payload,
        upstream_pass_output_id=upstream_pass_output_id,
    )
    context.log.bind(upstream_pass_output_id=upstream_pass_output_id)
    return IdeasUpstreamResult(
        upstream_pass_output_id,
        upstream_empty_corpus,
        trend_payload,
        trend_snapshot_pack_md,
    )


def _validate_ideas_targets(*, service: Any, log: Any, record_metric: Any) -> set[str]:
    targets = set(service.settings.publish_targets or [])
    if "obsidian" in targets and service.settings.obsidian_vault_path is None:
        raise ValueError(
            "OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'"
        )
    if "telegram" in targets:
        record_metric(
            name="pipeline.trends.projection.ideas_telegram.skipped_total",
            value=1,
            unit="count",
        )
        log.info("Ideas telegram projection is not implemented; target ignored")
    return targets


def _generate_ideas_payload(
    request: IdeasGenerationRequest,
) -> tuple[TrendIdeasPayload, dict[str, Any]]:
    if request.upstream_empty_corpus:
        request.context.record_metric(
            name="pipeline.trends.pass.ideas.upstream_empty_corpus_total",
            value=1,
            unit="count",
        )
        return (
            build_empty_trend_ideas_payload(
                granularity=request.context.normalized_granularity,
                period_start=request.context.period_start,
                period_end=request.context.period_end,
                output_language=request.context.service.settings.llm_output_language,
            ),
            {
                "empty_corpus": True,
                "usage": {"requests": 0, "input_tokens": 0, "output_tokens": 0},
                "tool_calls_total": 0,
                "tool_call_breakdown": {},
                "estimated_cost_usd": 0.0,
            },
        )

    model = str(
        request.context.llm_model or request.context.service.settings.llm_model or ""
    ).strip()
    if not model:
        raise ValueError("llm_model must not be empty")
    store = LanceVectorStore(
        db_dir=Path(request.context.service.settings.rag_lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=request.context.service.settings.trends_embedding_model,
            embedding_dimensions=request.context.service.settings.trends_embedding_dimensions,
        ),
    )
    payload, debug = ideas_agent.generate_trend_ideas_payload(
        repository=cast(Any, request.context.service.repository),
        vector_store=store,
        run_id=request.context.run_id,
        llm_model=model,
        output_language=request.context.service.settings.llm_output_language,
        embedding_model=request.context.service.settings.trends_embedding_model,
        embedding_dimensions=request.context.service.settings.trends_embedding_dimensions,
        embedding_batch_max_inputs=request.context.service.settings.trends_embedding_batch_max_inputs,
        embedding_batch_max_chars=request.context.service.settings.trends_embedding_batch_max_chars,
        embedding_failure_mode=getattr(
            request.context.service.settings,
            "trends_embedding_failure_mode",
            "continue",
        ),
        embedding_max_errors=int(
            getattr(request.context.service.settings, "trends_embedding_max_errors", 0)
            or 0
        ),
        granularity=request.context.normalized_granularity,
        period_start=request.context.period_start,
        period_end=request.context.period_end,
        trend_payload=request.trend_payload,
        trend_snapshot_pack_md=request.trend_snapshot_pack_md,
        rag_sources=trends.rag_sources_for_granularity(
            request.context.normalized_granularity
        ),
        include_debug=request.context.include_debug,
        metric_namespace=_trend_metric_name("pipeline.trends.pass.ideas"),
        llm_connection=request.context.service._llm_connection,
    )
    normalized_payload = normalize_trend_ideas_payload(payload)
    normalized_debug = debug if isinstance(debug, dict) else {}
    output_language = request.context.service.settings.llm_output_language
    if not list(normalized_payload.ideas or []):
        return (
            build_suppressed_trend_ideas_payload(
                granularity=request.context.normalized_granularity,
                period_start=request.context.period_start,
                period_end=request.context.period_end,
                output_language=output_language,
            ),
            normalized_debug,
        )
    title = str(normalized_payload.title or "").strip()
    title_debug: dict[str, Any] = {}
    try:
        title, title_debug = ideas_agent.generate_trend_ideas_bundle_title(
            llm_model=model,
            summary_md=normalized_payload.summary_md,
            ideas=[
                {
                    "title": str(idea.title or "").strip(),
                    "content_md": str(idea.content_md or "").strip(),
                }
                for idea in list(normalized_payload.ideas or [])
            ],
            output_language=output_language,
            llm_connection=request.context.service._llm_connection,
        )
    except Exception as exc:
        sanitized_error = request.context.service._sanitize_error_message(str(exc))
        request.context.record_metric(
            name="pipeline.trends.pass.ideas.bundle_title_failed_total",
            value=1,
            unit="count",
        )
        request.context.log.warning(
            "Ideas bundle title generation failed; using primary payload title "
            "run_id={} granularity={} period_start={} error_type={} error={}",
            request.context.run_id,
            request.context.normalized_granularity,
            request.context.period_start.isoformat(),
            type(exc).__name__,
            sanitized_error,
        )
        title_debug = {
            "fallback_used": True,
            "fallback_title": title,
            "error_type": type(exc).__name__,
            "error": sanitized_error,
        }
    return (
        normalized_payload.model_copy(update={"title": title}),
        _merge_ideas_debug(base=normalized_debug, extra=title_debug),
    )


def _merge_usage_dicts(
    *,
    base: dict[str, Any] | None,
    extra: dict[str, Any] | None,
) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key in ("requests", "input_tokens", "output_tokens"):
        total = 0.0
        found = False
        for source in (base or {}, extra or {}):
            value = source.get(key)
            if isinstance(value, (int, float)):
                total += float(value)
                found = True
        if found:
            merged[key] = int(total) if total.is_integer() else total
    return merged


def _merge_ideas_debug(
    *,
    base: dict[str, Any],
    extra: dict[str, Any],
) -> dict[str, Any]:
    merged = dict(base)
    merged["usage"] = _merge_usage_dicts(
        base=base.get("usage") if isinstance(base.get("usage"), dict) else None,
        extra=extra.get("usage") if isinstance(extra.get("usage"), dict) else None,
    )
    base_cost = base.get("estimated_cost_usd")
    extra_cost = extra.get("estimated_cost_usd")
    if isinstance(base_cost, (int, float)) or isinstance(extra_cost, (int, float)):
        merged["estimated_cost_usd"] = float(base_cost or 0.0) + float(
            extra_cost or 0.0
        )
    base_prompt_chars = base.get("prompt_chars")
    extra_prompt_chars = extra.get("prompt_chars")
    if isinstance(base_prompt_chars, (int, float)) or isinstance(
        extra_prompt_chars, (int, float)
    ):
        merged["prompt_chars"] = int(base_prompt_chars or 0) + int(
            extra_prompt_chars or 0
        )
    merged["bundle_title"] = extra
    return merged


def _build_projection_specs(context: IdeasProjectionContext):
    return lambda pass_output_id, _state: _ideas_projection_specs(
        context=context,
        pass_output_id=int(pass_output_id or 0),
    )


def _ideas_projection_specs(
    *,
    context: IdeasProjectionContext,
    pass_output_id: int,
) -> list[ProjectionSpec]:
    return [
        _ideas_document_projection_spec(context=context, pass_output_id=pass_output_id),
        _ideas_markdown_projection_spec(context=context, pass_output_id=pass_output_id),
        _ideas_obsidian_projection_spec(context=context, pass_output_id=pass_output_id),
    ]


def _ideas_document_projection_spec(
    *,
    context: IdeasProjectionContext,
    pass_output_id: int,
) -> ProjectionSpec:
    return ProjectionSpec(
        name="documents",
        enabled=True,
        metric_base="pipeline.trends.projection.ideas_documents",
        log=context.context.log.bind(
            module="pipeline.trends.projection.ideas_documents"
        ),
        failure_message=(
            "Ideas document projection failed pass_output_id={pass_output_id} "
            "error_type={error_type} error={error}"
        ),
        execute=lambda: persist_idea_document_projection(
            IdeaProjectionRequest(
                repository=context.context.service.repository,
                pass_output_id=pass_output_id,
                upstream_pass_output_id=context.upstream_pass_output_id,
                granularity=context.context.normalized_granularity,
                period_start=context.context.period_start,
                period_end=context.context.period_end,
                payload=context.payload,
            )
        ),
        warning_context={"pass_output_id": pass_output_id},
        sanitize_error=context.context.service._sanitize_error_message,
    )


def _ideas_markdown_projection_spec(
    *,
    context: IdeasProjectionContext,
    pass_output_id: int,
) -> ProjectionSpec:
    return ProjectionSpec(
        name="markdown",
        enabled="markdown" in context.targets,
        metric_base="pipeline.trends.projection.ideas_markdown",
        log=context.context.log.bind(
            module="pipeline.trends.projection.ideas_markdown"
        ),
        failure_message=(
            "Ideas markdown projection failed pass_output_id={pass_output_id} "
            "error_type={error_type} error={error}"
        ),
        execute=lambda: __import__(
            "recoleta.publish",
            fromlist=["write_markdown_ideas_note"],
        ).write_markdown_ideas_note(
            repository=cast(Any, context.context.service.repository),
            output_dir=Path(context.context.service.settings.markdown_output_dir),
            pass_output_id=pass_output_id,
            upstream_pass_output_id=context.upstream_pass_output_id,
            granularity=context.context.normalized_granularity,
            period_start=context.context.period_start,
            period_end=context.context.period_end,
            run_id=context.context.run_id,
            status=context.status.value,
            payload=context.payload,
            topics=list(context.trend_payload.topics or []),
            output_language=context.context.service.settings.llm_output_language,
        ),
        warning_context={"pass_output_id": pass_output_id},
        sanitize_error=context.context.service._sanitize_error_message,
    )


def _ideas_obsidian_projection_spec(
    *,
    context: IdeasProjectionContext,
    pass_output_id: int,
) -> ProjectionSpec:
    return ProjectionSpec(
        name="obsidian",
        enabled="obsidian" in context.targets
        and context.context.service.settings.obsidian_vault_path is not None,
        metric_base="pipeline.trends.projection.ideas_obsidian",
        log=context.context.log.bind(
            module="pipeline.trends.projection.ideas_obsidian"
        ),
        failure_message=(
            "Ideas obsidian projection failed pass_output_id={pass_output_id} "
            "error_type={error_type} error={error}"
        ),
        execute=lambda: __import__(
            "recoleta.publish",
            fromlist=["write_obsidian_ideas_note"],
        ).write_obsidian_ideas_note(
            repository=cast(Any, context.context.service.repository),
            vault_path=context.context.service.settings.obsidian_vault_path,
            base_folder=context.context.service.settings.obsidian_base_folder,
            pass_output_id=pass_output_id,
            upstream_pass_output_id=context.upstream_pass_output_id,
            granularity=context.context.normalized_granularity,
            period_start=context.context.period_start,
            period_end=context.context.period_end,
            run_id=context.context.run_id,
            status=context.status.value,
            payload=context.payload,
            topics=list(context.trend_payload.topics or []),
            output_language=context.context.service.settings.llm_output_language,
        ),
        warning_context={"pass_output_id": pass_output_id},
        sanitize_error=context.context.service._sanitize_error_message,
    )


def _record_ideas_usage_metrics(*, record_metric: Any, debug: dict[str, Any]) -> None:
    usage = debug.get("usage")
    if isinstance(usage, dict):
        requests = usage.get("requests")
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if isinstance(requests, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.llm_requests_total",
                value=float(requests),
                unit="count",
            )
        if isinstance(input_tokens, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.llm_input_tokens_total",
                value=float(input_tokens),
                unit="count",
            )
        if isinstance(output_tokens, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.llm_output_tokens_total",
                value=float(output_tokens),
                unit="count",
            )

    for metric_name, debug_key, unit in (
        ("pipeline.trends.pass.ideas.prompt_chars", "prompt_chars", "chars"),
        (
            "pipeline.trends.pass.ideas.snapshot_pack.chars",
            "trend_snapshot_pack_chars",
            "chars",
        ),
    ):
        value = debug.get(debug_key)
        if isinstance(value, (int, float)):
            record_metric(name=metric_name, value=float(value), unit=unit)

    cost_usd = debug.get("estimated_cost_usd")
    if isinstance(cost_usd, (int, float)):
        record_metric(
            name="pipeline.trends.pass.ideas.estimated_cost_usd",
            value=float(cost_usd),
            unit="usd",
        )
    else:
        record_metric(
            name="pipeline.trends.pass.ideas.cost_missing_total",
            value=1,
            unit="count",
        )


def _record_ideas_tool_metrics(*, record_metric: Any, debug: dict[str, Any]) -> None:
    tool_calls_total = int(debug.get("tool_calls_total") or 0)
    record_metric(
        name="pipeline.trends.pass.ideas.tool_calls_total",
        value=tool_calls_total,
        unit="count",
    )
    tool_call_breakdown = debug.get("tool_call_breakdown")
    if not isinstance(tool_call_breakdown, dict):
        return
    for raw_tool_name, raw_count in sorted(tool_call_breakdown.items()):
        if not isinstance(raw_count, (int, float)):
            continue
        metric_tool_name = metric_token(str(raw_tool_name), max_len=32)
        if not metric_tool_name:
            continue
        record_metric(
            name=f"pipeline.trends.pass.ideas.tool.{metric_tool_name}.calls_total",
            value=float(raw_count),
            unit="count",
        )


def _record_ideas_debug_artifact(
    request: IdeasDebugArtifactRequest | None = None,
    /,
    **kwargs: Any,
) -> None:
    normalized_request = request or IdeasDebugArtifactRequest(**kwargs)
    if not (
        bool(normalized_request.service.settings.write_debug_artifacts)
        and normalized_request.service.settings.artifacts_dir is not None
    ):
        return
    payload = {
        "upstream_pass_output_id": normalized_request.upstream_pass_output_id,
        "status": normalized_request.status.value,
        "trend_snapshot_pack_md": normalized_request.trend_snapshot_pack_md,
        "payload": normalized_request.ideas_payload.model_dump(mode="json"),
        "debug": normalized_request.debug,
    }
    record_debug_artifact = getattr(
        normalized_request.service, "_record_debug_artifact", None
    )
    if callable(record_debug_artifact):
        try:
            record_debug_artifact(
                run_id=normalized_request.run_id,
                item_id=None,
                kind="ideas_llm_response",
                payload=payload,
                log=logger.bind(
                    module="pipeline.trends.pass.ideas",
                    run_id=normalized_request.run_id,
                ),
                failure_message="Ideas debug artifact record failed: {}",
            )
        except Exception:
            return
        return
    try:
        artifact_path = normalized_request.service._write_debug_artifact(
            run_id=normalized_request.run_id,
            item_id=None,
            kind="ideas_llm_response",
            payload=payload,
        )
    except Exception:
        return
    if artifact_path is None:
        return
    try:
        normalized_request.service.repository.add_artifact(
            run_id=normalized_request.run_id,
            item_id=None,
            kind="ideas_llm_response",
            path=str(artifact_path),
        )
    except Exception:
        return


def execute_ideas_stage(
    service: Any,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
) -> IdeasResult:
    context = _build_ideas_stage_context(
        service=service,
        run_id=run_id,
        granularity=granularity,
        anchor_date=anchor_date,
        llm_model=llm_model,
    )
    upstream = _load_upstream_context(context)
    targets = _validate_ideas_targets(
        service=service,
        log=context.log,
        record_metric=context.record_metric,
    )
    payload, debug = _generate_ideas_payload(
        IdeasGenerationRequest(
            context=context,
            trend_payload=upstream.trend_payload,
            trend_snapshot_pack_md=upstream.trend_snapshot_pack_md,
            upstream_empty_corpus=upstream.upstream_empty_corpus,
        )
    )
    status = _ideas_status(payload)
    pass_execution = _run_ideas_pass_definition(
        IdeasPassDefinitionRequest(
            context=context,
            payload=payload,
            status=status,
            trend_payload=upstream.trend_payload,
            upstream_pass_output_id=upstream.upstream_pass_output_id,
            debug=debug,
            targets=targets,
        )
    )
    pass_output_id = pass_execution.pass_output_id
    if pass_output_id is None:
        raise RuntimeError("ideas pass output persistence returned an empty id")
    note_path = _ideas_note_path(
        context=context,
        status=status,
        pass_execution=pass_execution,
    )
    _record_ideas_usage_metrics(record_metric=context.record_metric, debug=debug)
    _record_ideas_tool_metrics(record_metric=context.record_metric, debug=debug)
    _record_ideas_debug_artifact(
        IdeasDebugArtifactRequest(
            service=service,
            run_id=run_id,
            upstream_pass_output_id=upstream.upstream_pass_output_id,
            status=status,
            trend_snapshot_pack_md=upstream.trend_snapshot_pack_md,
            ideas_payload=payload,
            debug=debug,
        )
    )
    context.record_metric(
        name="pipeline.trends.pass.ideas.duration_ms",
        value=int((time.perf_counter() - context.started) * 1000),
        unit="ms",
    )
    return IdeasResult(
        pass_output_id=pass_output_id,
        granularity=context.normalized_granularity,
        period_start=context.period_start,
        period_end=context.period_end,
        title=payload.title,
        status=status.value,
        note_path=note_path,
        upstream_pass_output_id=upstream.upstream_pass_output_id,
    )


def _build_ideas_stage_context(
    *,
    service: Any,
    run_id: str,
    granularity: str,
    anchor_date: date | None,
    llm_model: str | None,
) -> IdeasStageContext:
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity not in {"day", "week", "month"}:
        raise ValueError("granularity must be one of: day, week, month")
    anchor = anchor_date or utc_now().date()
    period_start, period_end = _period_bounds_for_granularity(
        granularity=normalized_granularity,
        anchor=anchor,
    )
    return IdeasStageContext(
        service=service,
        run_id=run_id,
        log=logger.bind(module="pipeline.trends.pass.ideas", run_id=run_id),
        started=time.perf_counter(),
        normalized_granularity=normalized_granularity,
        period_start=period_start,
        period_end=period_end,
        record_metric=_build_metric_recorder(service=service, run_id=run_id),
        include_debug=bool(
            service.settings.write_debug_artifacts
            and service.settings.artifacts_dir is not None
        ),
        llm_model=llm_model,
    )


def _ideas_status(payload: TrendIdeasPayload) -> PassStatus:
    return (
        PassStatus.SUPPRESSED if not list(payload.ideas or []) else PassStatus.SUCCEEDED
    )


def _run_ideas_pass_definition(request: IdeasPassDefinitionRequest) -> Any:
    envelope = build_trend_ideas_pass_output(
        run_id=request.context.run_id,
        status=request.status,
        granularity=request.context.normalized_granularity,
        period_start=request.context.period_start,
        period_end=request.context.period_end,
        payload=request.payload,
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind=TREND_SYNTHESIS_PASS_KIND,
                granularity=request.context.normalized_granularity,
                period_start=request.context.period_start.isoformat(),
                period_end=request.context.period_end.isoformat(),
                pass_output_id=request.upstream_pass_output_id,
            )
        ],
        diagnostics=request.debug,
    )
    projection_context = IdeasProjectionContext(
        context=request.context,
        targets=request.targets,
        status=request.status,
        payload=request.payload,
        trend_payload=request.trend_payload,
        upstream_pass_output_id=request.upstream_pass_output_id,
    )
    return run_pass_definition(
        repository=request.context.service.repository,
        record_metric=request.context.record_metric,
        definition=PassDefinition[None](
            persist=PassPersistSpec(
                envelope=envelope,
                period_start=request.context.period_start,
                period_end=request.context.period_end,
                log=request.context.log.bind(module="pipeline.trends.pass.ideas"),
                failure_message=(
                    "Ideas pass output persist failed granularity={granularity} "
                    "period_start={period_start} period_end={period_end} "
                    "pass_kind={pass_kind} error_type={error_type} error={error}"
                ),
                warning_context={
                    "granularity": request.context.normalized_granularity,
                    "period_start": request.context.period_start.isoformat(),
                    "period_end": request.context.period_end.isoformat(),
                },
                sanitize_error=request.context.service._sanitize_error_message,
                persisted_metric_name="pipeline.trends.pass.ideas.persisted_total",
            ),
            should_project=request.status != PassStatus.SUPPRESSED,
            build_projection_specs=_build_projection_specs(projection_context),
        ),
    )


def _ideas_note_path(
    *,
    context: IdeasStageContext,
    status: PassStatus,
    pass_execution: Any,
) -> Path | None:
    if status == PassStatus.SUPPRESSED:
        context.record_metric(
            name="pipeline.trends.pass.ideas.suppressed_total",
            value=1,
            unit="count",
        )
        return None
    raw_note_path = pass_execution.projection_results.get("markdown")
    return raw_note_path if isinstance(raw_note_path, Path) else None
