from __future__ import annotations

from dataclasses import dataclass, field
import time
from types import SimpleNamespace
from typing import Any

from loguru import logger

from recoleta.models import ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED
from recoleta.pipeline.metrics import metric_token
from recoleta.types import AnalysisWrite, AnalyzeResult, ItemStateUpdate


@dataclass(frozen=True, slots=True)
class AnalyzeLoadRequest:
    service: Any
    run_id: str
    effective_limit: int
    triage_required: bool
    period_start: Any
    period_end: Any


@dataclass(frozen=True, slots=True)
class AnalyzePrepareRequest:
    service: Any
    items: list[Any]
    include_debug: bool
    analyze_result: AnalyzeResult
    write_and_record_artifact: Any
    log: Any


@dataclass(slots=True)
class AnalyzeCounters:
    llm_calls_total: int
    llm_errors_total: int = 0
    llm_prompt_tokens_total: int = 0
    llm_completion_tokens_total: int = 0
    llm_tokens_seen: bool = False
    llm_cost_usd_total: float = 0.0
    llm_cost_seen: bool = False
    llm_cost_missing_total: int = 0
    llm_calls_by_provider_token: dict[str, int] = field(default_factory=dict)
    llm_errors_by_provider_token: dict[str, int] = field(default_factory=dict)
    llm_calls_by_model_token: dict[str, int] = field(default_factory=dict)
    llm_errors_by_model_token: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalyzeFailureContext:
    service: Any
    analyze_result: AnalyzeResult
    state_updates: list[ItemStateUpdate]
    write_and_record_artifact: Any
    log: Any
    configured_provider_token: str
    configured_model_token: str
    counters: AnalyzeCounters


@dataclass(frozen=True, slots=True)
class AnalyzeOutcomeRequest:
    include_debug: bool
    failure_context: AnalyzeFailureContext
    outcomes: list[Any]


@dataclass(frozen=True, slots=True)
class AnalyzeSuccessRequest:
    outcome: Any
    include_debug: bool
    counters: AnalyzeCounters
    configured_provider_token: str
    configured_model_token: str
    write_and_record_artifact: Any
    analysis_writes: list[AnalysisWrite]


@dataclass(frozen=True, slots=True)
class AnalyzeOutcomeProcessing:
    analysis_writes: list[AnalysisWrite]
    state_updates: list[ItemStateUpdate]
    counters: AnalyzeCounters


@dataclass(frozen=True, slots=True)
class AnalyzePersistFailureRequest:
    failure_context: AnalyzeFailureContext
    persisted_analyses: Any


@dataclass(frozen=True, slots=True)
class AnalyzeExecutionContext:
    service: Any
    run_id: str
    log: Any
    started: float
    triage_required: bool
    effective_limit: int
    analyze_result: AnalyzeResult
    configured_provider_token: str
    configured_model_token: str
    include_debug: bool
    write_and_record_artifact: Any


@dataclass(frozen=True, slots=True)
class AnalyzeBatchResult:
    missing_content_total: int
    counters: AnalyzeCounters
    persisted_analyses: Any
    state_batches_total: int
    state_rows_total: int
    parallelism: int
    work_items_total: int


def _configured_llm_tokens(*, service: Any) -> tuple[str, str]:
    configured_provider = (
        service.settings.llm_model.split("/", 1)[0]
        if "/" in service.settings.llm_model
        else "unknown"
    )
    return metric_token(configured_provider, max_len=24), metric_token(
        service.settings.llm_model
    )


def _build_analyze_artifact_writer(*, service: Any, run_id: str, log: Any):
    def write_and_record_artifact(
        *,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> None:
        service._record_debug_artifact(
            run_id=run_id,
            item_id=item_id,
            kind=kind,
            payload=payload,
            log=log.bind(item_id=item_id),
            failure_message=f"Analyze {kind} artifact record failed: {{}}",
        )

    return write_and_record_artifact


def _load_analyze_items(request: AnalyzeLoadRequest) -> list[Any]:
    candidate_limit = request.service._stage_candidate_limit(limit=request.effective_limit)
    items = request.service._invoke_repository_method(
        "list_items_for_llm_analysis",
        limit=candidate_limit,
        triage_required=request.triage_required,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    items, candidate_counts, deferred_counts = request.service._rebalance_items_by_source(
        items=list(items),
        limit=request.effective_limit,
    )
    request.service._record_stage_source_selection_metrics(
        run_id=request.run_id,
        stage="analyze",
        candidate_counts=candidate_counts,
        deferred_counts=deferred_counts,
    )
    return list(items)


def _prepare_analyze_work(
    request: AnalyzePrepareRequest,
) -> tuple[list[Any], list[ItemStateUpdate], int]:
    work_items: list[Any] = []
    state_updates: list[ItemStateUpdate] = []
    missing_content_total = 0
    for item in request.items:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            request.analyze_result.failed += 1
            request.log.warning("Analyze skipped: item has no id")
            continue
        item_id = int(raw_item_id)
        content_text = request.service._load_stored_content_for_analysis(item=item)
        if content_text:
            work_items.append(
                SimpleNamespace(
                    item_id=item_id,
                    title=item.title,
                    canonical_url=item.canonical_url,
                    user_topics=list(request.service.settings.topics),
                    content_text=content_text,
                    mirror_item_state=True,
                )
            )
            continue
        missing_content_total += 1
        request.analyze_result.failed += 1
        state_updates.append(
            ItemStateUpdate(
                item_id=item_id,
                state=ITEM_STATE_RETRYABLE_FAILED,
            )
        )
        if request.include_debug:
            request.write_and_record_artifact(
                item_id=item_id,
                kind="error_context",
                payload={
                    "stage": "analyze",
                    "error_type": "MissingContent",
                    "error_message": "missing stored content before LLM analysis",
                    "item_id": item_id,
                    "error_category": "ordering",
                    "retryable": True,
                },
            )
        request.log.bind(item_id=item_id).warning("Analyze failed: missing stored content")
    return work_items, state_updates, missing_content_total


def _bucket_token(
    *,
    observed: str,
    configured: str,
    max_len: int = 48,
) -> str:
    token = metric_token(observed, max_len=max_len)
    if token == configured:
        return token
    return "other"


def _record_analyze_failure(
    context: AnalyzeFailureContext,
    *,
    item_id: int,
    exc: Exception,
) -> None:
    context.analyze_result.failed += 1
    context.counters.llm_errors_total += 1
    _increment_counter(
        context.counters.llm_errors_by_provider_token,
        context.configured_provider_token,
    )
    _increment_counter(
        context.counters.llm_errors_by_model_token,
        context.configured_model_token,
    )
    sanitized_error = context.service._sanitize_error_message(str(exc))
    classification = context.service._classify_exception(exc)
    context.state_updates.append(
        ItemStateUpdate(
            item_id=item_id,
            state=(
                ITEM_STATE_RETRYABLE_FAILED
                if classification.get("retryable") is True
                else ITEM_STATE_FAILED
            ),
        )
    )
    context.write_and_record_artifact(
        item_id=item_id,
        kind="error_context",
        payload={
            "stage": "analyze",
            "error_type": type(exc).__name__,
            "error_message": sanitized_error,
            "item_id": item_id,
            **classification,
        },
    )
    context.log.bind(item_id=item_id).warning("Analyze failed: {}", sanitized_error)


def _process_analyze_outcomes(
    request: AnalyzeOutcomeRequest,
) -> AnalyzeOutcomeProcessing:
    analysis_writes: list[AnalysisWrite] = []
    state_updates: list[ItemStateUpdate] = []
    counters = AnalyzeCounters(llm_calls_total=len(request.outcomes))
    failure_context = AnalyzeFailureContext(
        service=request.failure_context.service,
        analyze_result=request.failure_context.analyze_result,
        state_updates=state_updates,
        write_and_record_artifact=request.failure_context.write_and_record_artifact,
        log=request.failure_context.log,
        configured_provider_token=request.failure_context.configured_provider_token,
        configured_model_token=request.failure_context.configured_model_token,
        counters=counters,
    )
    for outcome in request.outcomes:
        item_id = outcome.work_item.item_id
        try:
            _record_analyze_success(
                AnalyzeSuccessRequest(
                    outcome=outcome,
                    include_debug=request.include_debug,
                    counters=counters,
                    configured_provider_token=failure_context.configured_provider_token,
                    configured_model_token=failure_context.configured_model_token,
                    write_and_record_artifact=failure_context.write_and_record_artifact,
                    analysis_writes=analysis_writes,
                )
            )
        except Exception as exc:  # noqa: BLE001
            _record_analyze_failure(failure_context, item_id=item_id, exc=exc)
    return AnalyzeOutcomeProcessing(
        analysis_writes=analysis_writes,
        state_updates=state_updates,
        counters=counters,
    )


def _record_analyze_success(request: AnalyzeSuccessRequest) -> None:
    analysis_result_payload, debug = _outcome_payload(
        outcome=request.outcome,
        include_debug=request.include_debug,
    )
    _record_analyze_usage(
        counters=request.counters,
        analysis_result_payload=analysis_result_payload,
        configured_provider_token=request.configured_provider_token,
        configured_model_token=request.configured_model_token,
    )
    if request.include_debug and debug is not None:
        _record_analyze_debug_artifacts(
            write_and_record_artifact=request.write_and_record_artifact,
            item_id=request.outcome.work_item.item_id,
            debug=debug,
        )
    request.analysis_writes.append(
        AnalysisWrite(
            item_id=request.outcome.work_item.item_id,
            result=analysis_result_payload,
            mirror_item_state=request.outcome.work_item.mirror_item_state,
        )
    )


def _outcome_payload(*, outcome: Any, include_debug: bool) -> tuple[Any, Any]:
    if hasattr(outcome, "error") and not hasattr(outcome, "result"):
        raise outcome.error
    analysis_result_payload = outcome.result
    debug = outcome.debug
    if include_debug and debug is None:
        raise RuntimeError(
            "Analyzer did not return debug payload while include_debug is enabled"
        )
    return analysis_result_payload, debug


def _record_analyze_usage(
    *,
    counters: AnalyzeCounters,
    analysis_result_payload: Any,
    configured_provider_token: str,
    configured_model_token: str,
) -> None:
    _increment_counter(
        counters.llm_calls_by_provider_token,
        _bucket_token(
            observed=analysis_result_payload.provider,
            configured=configured_provider_token,
            max_len=24,
        ),
    )
    _increment_counter(
        counters.llm_calls_by_model_token,
        _bucket_token(
            observed=analysis_result_payload.model,
            configured=configured_model_token,
        ),
    )
    if analysis_result_payload.prompt_tokens is not None:
        counters.llm_prompt_tokens_total += int(analysis_result_payload.prompt_tokens)
        counters.llm_tokens_seen = True
    if analysis_result_payload.completion_tokens is not None:
        counters.llm_completion_tokens_total += int(
            analysis_result_payload.completion_tokens
        )
        counters.llm_tokens_seen = True
    if analysis_result_payload.cost_usd is not None:
        counters.llm_cost_usd_total += float(analysis_result_payload.cost_usd)
        counters.llm_cost_seen = True
    else:
        counters.llm_cost_missing_total += 1


def _record_analyze_debug_artifacts(
    *,
    write_and_record_artifact: Any,
    item_id: int,
    debug: Any,
) -> None:
    write_and_record_artifact(
        item_id=item_id,
        kind="llm_request",
        payload=debug.request,
    )
    write_and_record_artifact(
        item_id=item_id,
        kind="llm_response",
        payload=debug.response,
    )


def _handle_persist_failures(request: AnalyzePersistFailureRequest) -> None:
    request.failure_context.analyze_result.processed += len(
        request.persisted_analyses.persisted
    )
    for failed_persist in request.persisted_analyses.failed:
        _record_analyze_failure(
            request.failure_context,
            item_id=failed_persist.analysis.item_id,
            exc=failed_persist.error,
        )


def execute_analyze(
    service: Any,
    *,
    run_id: str,
    limit: int | None = None,
    period_start: Any = None,
    period_end: Any = None,
) -> AnalyzeResult:
    context = _build_analyze_context(service=service, run_id=run_id, limit=limit)
    with service.repository.sql_diagnostics() as sql_diag:
        batch_result = _run_analyze_batch(
            context=context,
            period_start=period_start,
            period_end=period_end,
        )
        _record_analyze_metrics(
            context=context,
            batch_result=batch_result,
            sql_diag=sql_diag,
        )
    context.log.info(
        "Analyze completed with processed={} failed={} missing_content={}",
        context.analyze_result.processed,
        context.analyze_result.failed,
        batch_result.missing_content_total,
    )
    return context.analyze_result


def _build_analyze_context(
    *,
    service: Any,
    run_id: str,
    limit: int | None,
) -> AnalyzeExecutionContext:
    configured_provider_token, configured_model_token = _configured_llm_tokens(
        service=service
    )
    log = logger.bind(module="pipeline.analyze", run_id=run_id)
    include_debug = (
        service.settings.write_debug_artifacts
        and service.settings.artifacts_dir is not None
    )
    return AnalyzeExecutionContext(
        service=service,
        run_id=run_id,
        log=log,
        started=time.perf_counter(),
        triage_required=bool(service.settings.triage_enabled)
        and bool(service.settings.topics),
        effective_limit=service._resolve_analysis_limit(limit=limit),
        analyze_result=AnalyzeResult(),
        configured_provider_token=configured_provider_token,
        configured_model_token=configured_model_token,
        include_debug=include_debug,
        write_and_record_artifact=_build_analyze_artifact_writer(
            service=service,
            run_id=run_id,
            log=log,
        ),
    )


def _run_analyze_batch(
    *,
    context: AnalyzeExecutionContext,
    period_start: Any,
    period_end: Any,
) -> AnalyzeBatchResult:
    items = _load_analyze_items(
        AnalyzeLoadRequest(
            service=context.service,
            run_id=context.run_id,
            effective_limit=context.effective_limit,
            triage_required=context.triage_required,
            period_start=period_start,
            period_end=period_end,
        )
    )
    work_items, state_updates, missing_content_total = _prepare_analyze_work(
        AnalyzePrepareRequest(
            service=context.service,
            items=items,
            include_debug=context.include_debug,
            analyze_result=context.analyze_result,
            write_and_record_artifact=context.write_and_record_artifact,
            log=context.log,
        )
    )
    outcomes, parallelism = context.service._run_analyze_calls(
        work_items=work_items,
        include_debug=context.include_debug,
        description="Analyzing items",
    )
    processed_outcomes = _process_analyze_outcomes(
        AnalyzeOutcomeRequest(
            include_debug=context.include_debug,
            outcomes=outcomes,
            failure_context=AnalyzeFailureContext(
                service=context.service,
                analyze_result=context.analyze_result,
                state_updates=state_updates,
                write_and_record_artifact=context.write_and_record_artifact,
                log=context.log,
                configured_provider_token=context.configured_provider_token,
                configured_model_token=context.configured_model_token,
                counters=AnalyzeCounters(llm_calls_total=len(outcomes)),
            ),
        )
    )
    state_updates.extend(processed_outcomes.state_updates)
    persisted_analyses = context.service._persist_analysis_writes(
        analyses=processed_outcomes.analysis_writes
    )
    _handle_persist_failures(
        AnalyzePersistFailureRequest(
            failure_context=AnalyzeFailureContext(
                service=context.service,
                analyze_result=context.analyze_result,
                state_updates=state_updates,
                write_and_record_artifact=context.write_and_record_artifact,
                log=context.log,
                configured_provider_token=context.configured_provider_token,
                configured_model_token=context.configured_model_token,
                counters=processed_outcomes.counters,
            ),
            persisted_analyses=persisted_analyses,
        )
    )
    state_batches_total, state_rows_total = context.service._persist_state_updates(
        state_updates=state_updates,
    )
    return AnalyzeBatchResult(
        missing_content_total=missing_content_total,
        counters=processed_outcomes.counters,
        persisted_analyses=persisted_analyses,
        state_batches_total=state_batches_total,
        state_rows_total=state_rows_total,
        parallelism=parallelism,
        work_items_total=len(work_items),
    )


def _record_analyze_metrics(
    *,
    context: AnalyzeExecutionContext,
    batch_result: AnalyzeBatchResult,
    sql_diag: Any,
) -> None:
    metric_points = context.service._build_analyze_metric_points(
        analyze_result=context.analyze_result,
        llm_calls_total=batch_result.work_items_total,
        llm_errors_total=batch_result.counters.llm_errors_total,
        missing_content_total=batch_result.missing_content_total,
        llm_prompt_tokens_total=batch_result.counters.llm_prompt_tokens_total,
        llm_completion_tokens_total=batch_result.counters.llm_completion_tokens_total,
        llm_tokens_seen=batch_result.counters.llm_tokens_seen,
        llm_cost_usd_total=batch_result.counters.llm_cost_usd_total,
        llm_cost_seen=batch_result.counters.llm_cost_seen,
        llm_cost_missing_total=batch_result.counters.llm_cost_missing_total,
        llm_calls_by_provider_token=batch_result.counters.llm_calls_by_provider_token,
        llm_errors_by_provider_token=batch_result.counters.llm_errors_by_provider_token,
        llm_calls_by_model_token=batch_result.counters.llm_calls_by_model_token,
        llm_errors_by_model_token=batch_result.counters.llm_errors_by_model_token,
        duration_ms=int((time.perf_counter() - context.started) * 1000),
        parallelism=batch_result.parallelism,
        sql_queries_total=sql_diag.queries_total,
        sql_commits_total=sql_diag.commits_total,
        analysis_batches_total=batch_result.persisted_analyses.analysis_batches_total,
        analysis_rows_total=batch_result.persisted_analyses.analysis_rows_total,
        state_batches_total=batch_result.state_batches_total,
        state_rows_total=batch_result.state_rows_total,
    )
    context.service._record_metrics_batch(run_id=context.run_id, metrics=metric_points)


def _increment_counter(counter: dict[str, int], token: str) -> None:
    counter[token] = counter.get(token, 0) + 1
