from __future__ import annotations

from dataclasses import dataclass
import time
from typing import Any, cast

from loguru import logger

from recoleta.models import ITEM_STATE_ENRICHED
from recoleta.triage import TriageCandidate


@dataclass(frozen=True, slots=True)
class TriageContentMaps:
    pdf_by_id: dict[int, Any]
    html_by_id: dict[int, Any]
    html_document_md_by_id: dict[int, Any]
    html_document_by_id: dict[int, Any]
    latex_by_id: dict[int, Any]


@dataclass(frozen=True, slots=True)
class TriageContentFetchResult:
    content_maps: TriageContentMaps
    failed: bool
    error: dict[str, Any] | None


@dataclass(frozen=True, slots=True)
class TriageExcerptRequest:
    item: Any
    content_maps: TriageContentMaps


@dataclass(frozen=True, slots=True)
class TriageExecutionContext:
    service: Any
    run_id: str
    log: Any
    normalized_limit: int
    normalized_candidate_limit: int
    include_debug: bool


@dataclass(frozen=True, slots=True)
class TriageStageRequest:
    service: Any
    run_id: str
    limit: int
    candidate_limit: int | None = None
    period_start: Any = None
    period_end: Any = None


@dataclass(frozen=True, slots=True)
class TriageFailureRequest:
    context: TriageExecutionContext
    triage_items: list[Any]
    triage_candidates: list[TriageCandidate]
    triage_started: float
    write_and_record_artifact: Any
    exc: Exception


def _collect_triage_item_ids(
    *, items: list[Any]
) -> tuple[list[Any], list[int], list[int], list[int]]:
    candidates_items: list[Any] = []
    item_ids: list[int] = []
    pdf_item_ids: list[int] = []
    arxiv_item_ids: list[int] = []
    for item in items:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            continue
        try:
            item_id = int(raw_item_id)
        except Exception:
            continue
        if item_id <= 0:
            continue
        candidates_items.append(item)
        item_ids.append(item_id)
        source = str(getattr(item, "source", "") or "").strip().lower()
        if source in {"arxiv", "openreview"}:
            pdf_item_ids.append(item_id)
        if source == "arxiv":
            arxiv_item_ids.append(item_id)
    return candidates_items, item_ids, pdf_item_ids, arxiv_item_ids


def _fetch_triage_content_maps(
    *,
    service: Any,
    item_ids: list[int],
    pdf_item_ids: list[int],
    arxiv_item_ids: list[int],
) -> TriageContentFetchResult:
    html_by_id: dict[int, Any] = {}
    pdf_by_id: dict[int, Any] = {}
    html_document_by_id: dict[int, Any] = {}
    html_document_md_by_id: dict[int, Any] = {}
    latex_by_id: dict[int, Any] = {}
    content_fetch_failed = False
    content_fetch_error: dict[str, Any] | None = None
    try:
        html_by_id = service.repository.get_latest_contents(
            item_ids=item_ids, content_type="html_maintext"
        )
        if pdf_item_ids:
            pdf_by_id = service.repository.get_latest_contents(
                item_ids=pdf_item_ids, content_type="pdf_text"
            )
        if arxiv_item_ids:
            html_document_md_by_id = service.repository.get_latest_contents(
                item_ids=arxiv_item_ids,
                content_type="html_document_md",
            )
            html_document_by_id = service.repository.get_latest_contents(
                item_ids=arxiv_item_ids,
                content_type="html_document",
            )
            latex_by_id = service.repository.get_latest_contents(
                item_ids=arxiv_item_ids,
                content_type="latex_source",
            )
    except Exception as exc:  # noqa: BLE001
        content_fetch_failed = True
        sanitized_error = service._sanitize_error_message(str(exc))
        content_fetch_error = {
            "stage": "triage_content_fetch",
            "error_type": type(exc).__name__,
            "error_message": sanitized_error,
            **service._classify_exception(exc),
            "content_types": [
                "html_maintext",
                "pdf_text",
                "html_document_md",
                "html_document",
                "latex_source",
            ],
            "item_ids_total": len(item_ids),
            "pdf_item_ids_total": len(pdf_item_ids),
            "arxiv_item_ids_total": len(arxiv_item_ids),
        }
    return TriageContentFetchResult(
        content_maps=TriageContentMaps(
            pdf_by_id=pdf_by_id,
            html_by_id=html_by_id,
            html_document_md_by_id=html_document_md_by_id,
            html_document_by_id=html_document_by_id,
            latex_by_id=latex_by_id,
        ),
        failed=content_fetch_failed,
        error=content_fetch_error,
    )


def _content_text_value(content: Any) -> str | None:
    if content is None or getattr(content, "text", None) is None:
        return None
    value = str(getattr(content, "text") or "")
    return value if value else None


def _select_triage_excerpt(request: TriageExcerptRequest) -> str | None:
    item_id = int(getattr(request.item, "id"))
    source = str(getattr(request.item, "source", "") or "").strip().lower()
    if source in {"arxiv", "openreview"}:
        if excerpt := _content_text_value(request.content_maps.pdf_by_id.get(item_id)):
            return excerpt
    if excerpt := _content_text_value(request.content_maps.html_by_id.get(item_id)):
        return excerpt
    if source == "arxiv":
        for content_map in (
            request.content_maps.html_document_md_by_id,
            request.content_maps.html_document_by_id,
            request.content_maps.latex_by_id,
        ):
            if excerpt := _content_text_value(content_map.get(item_id)):
                return excerpt
    return None


def build_triage_candidates(
    service: Any,
    *,
    items: list[Any],
) -> tuple[list[TriageCandidate], bool, dict[str, Any] | None]:
    (
        candidates_items,
        item_ids,
        pdf_item_ids,
        arxiv_item_ids,
    ) = _collect_triage_item_ids(items=items)
    if not candidates_items:
        return [], False, None

    max_chars = int(
        getattr(service.settings, "triage_item_text_max_chars", 1200) or 1200
    )
    fetch_result = _fetch_triage_content_maps(
        service=service,
        item_ids=item_ids,
        pdf_item_ids=pdf_item_ids,
        arxiv_item_ids=arxiv_item_ids,
    )

    candidates: list[TriageCandidate] = []
    for item in candidates_items:
        title = str(getattr(item, "title", "") or "").strip()
        excerpt = _select_triage_excerpt(
            TriageExcerptRequest(
                item=item,
                content_maps=fetch_result.content_maps,
            )
        )
        combined = title
        if excerpt:
            trimmed_excerpt = excerpt.strip()
            if trimmed_excerpt:
                combined = f"{title}\n\n{trimmed_excerpt}" if title else trimmed_excerpt
        if max_chars > 0 and len(combined) > max_chars:
            combined = combined[:max_chars]
        candidates.append(TriageCandidate(item=item, text=combined))
    return candidates, fetch_result.failed, fetch_result.error


def _record_empty_triage_metrics(*, service: Any, run_id: str) -> None:
    for name in (
        "pipeline.triage.candidates_total",
        "pipeline.triage.scored_total",
        "pipeline.triage.selected_total",
        "pipeline.triage.skipped_total",
        "pipeline.triage.embedding_calls_total",
        "pipeline.triage.embedding_errors_total",
        "pipeline.triage.content_fetch_failed_total",
        "pipeline.triage.failed_total",
        "pipeline.triage.duration_ms",
    ):
        service.repository.record_metric(
            run_id=run_id,
            name=name,
            value=0,
            unit="ms" if name.endswith("duration_ms") else "count",
        )


def _record_triage_success_metrics(*, service: Any, run_id: str, stats: Any) -> None:
    metric_rows = [
        ("pipeline.triage.candidates_total", stats.candidates_total, "count"),
        ("pipeline.triage.scored_total", stats.scored_total, "count"),
        ("pipeline.triage.selected_total", stats.selected_total, "count"),
        ("pipeline.triage.skipped_total", stats.skipped_total, "count"),
        (
            "pipeline.triage.embedding_calls_total",
            stats.embedding_calls_total,
            "count",
        ),
        (
            "pipeline.triage.embedding_errors_total",
            stats.embedding_errors_total,
            "count",
        ),
        ("pipeline.triage.failed_total", 0, "count"),
        ("pipeline.triage.duration_ms", stats.duration_ms, "ms"),
    ]
    for name, value, unit in metric_rows:
        service.repository.record_metric(
            run_id=run_id, name=name, value=value, unit=unit
        )
    if stats.embedding_prompt_tokens_total is not None:
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.triage.embedding_prompt_tokens_total",
            value=stats.embedding_prompt_tokens_total,
            unit="count",
        )
    if stats.embedding_cost_usd_total is not None:
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.triage.estimated_cost_usd",
            value=stats.embedding_cost_usd_total,
            unit="usd",
        )
    if (
        stats.embedding_cost_missing_total is not None
        and stats.embedding_cost_missing_total > 0
    ):
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.triage.cost_missing_total",
            value=stats.embedding_cost_missing_total,
            unit="count",
        )


def _mark_selected_triage_items(*, service: Any, selected: list[Any], log: Any) -> int:
    selected_total = 0
    for entry in selected:
        selected_item_id = getattr(entry.candidate.item, "id", None)
        if selected_item_id is None:
            continue
        try:
            service.repository.mark_item_triaged(item_id=int(selected_item_id))
            selected_total += 1
        except Exception as mark_exc:
            log.bind(item_id=selected_item_id).warning(
                "Triage mark_item_triaged failed: {}",
                service._sanitize_error_message(str(mark_exc)),
            )
    return selected_total


def _mark_fallback_triage_items(
    *,
    service: Any,
    items: list[Any],
    limit: int,
    log: Any,
) -> int:
    fallback_marked_total = 0
    for item in items[:limit]:
        fallback_item_id = getattr(item, "id", None)
        if fallback_item_id is None:
            continue
        try:
            service.repository.mark_item_triaged(item_id=int(fallback_item_id))
            fallback_marked_total += 1
        except Exception as mark_exc:
            log.bind(item_id=fallback_item_id).warning(
                "Triage fallback mark_item_triaged failed: {}",
                service._sanitize_error_message(str(mark_exc)),
            )
    return fallback_marked_total


def execute_triage(request: TriageStageRequest) -> None:
    context = _triage_execution_context(
        service=request.service,
        run_id=request.run_id,
        limit=request.limit,
        candidate_limit=request.candidate_limit,
    )
    if context is None:
        return
    triage_items = _load_triage_items(
        context=context,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    write_and_record_artifact = _build_triage_artifact_writer(context)
    triage_candidates, content_fetch_failed, content_fetch_error = (
        _resolve_triage_candidates(
            context=context,
            triage_items=triage_items,
        )
    )
    if not triage_candidates:
        _record_empty_triage_metrics(service=context.service, run_id=context.run_id)
        context.log.info("Triage skipped: no candidates")
        return

    context.service.repository.record_metric(
        run_id=context.run_id,
        name="pipeline.triage.content_fetch_failed_total",
        value=1 if content_fetch_failed else 0,
        unit="count",
    )
    if (
        content_fetch_failed
        and context.include_debug
        and content_fetch_error is not None
    ):
        write_and_record_artifact(
            item_id=None,
            kind="error_context",
            payload=content_fetch_error,
        )
    _run_triage_selection(
        context=context,
        triage_items=triage_items,
        triage_candidates=triage_candidates,
        write_and_record_artifact=write_and_record_artifact,
    )


def _triage_execution_context(
    *,
    service: Any,
    run_id: str,
    limit: int,
    candidate_limit: int | None,
) -> TriageExecutionContext | None:
    triage_enabled = bool(service.settings.triage_enabled) and bool(
        service.settings.topics
    )
    if not triage_enabled:
        return None
    normalized_limit = service._resolve_analysis_limit(limit=limit)
    normalized_candidate_limit = (
        candidate_limit
        or service._resolve_triage_candidate_limit(limit=normalized_limit)
    )
    return TriageExecutionContext(
        service=service,
        run_id=run_id,
        log=logger.bind(module="pipeline.triage", run_id=run_id),
        normalized_limit=normalized_limit,
        normalized_candidate_limit=normalized_candidate_limit,
        include_debug=bool(
            service.settings.write_debug_artifacts
            and service.settings.artifacts_dir is not None
        ),
    )


def _load_triage_items(
    *,
    context: TriageExecutionContext,
    period_start: Any,
    period_end: Any,
) -> list[Any]:
    selection_limit = context.service._stage_candidate_limit(
        limit=context.normalized_candidate_limit
    )
    items = context.service._invoke_repository_method(
        "list_items_for_llm_analysis",
        limit=selection_limit,
        triage_required=False,
        period_start=period_start,
        period_end=period_end,
    )
    items, candidate_counts, deferred_counts = (
        context.service._rebalance_items_by_source(
            items=list(items),
            limit=context.normalized_candidate_limit,
        )
    )
    context.service._record_stage_source_selection_metrics(
        run_id=context.run_id,
        stage="triage",
        candidate_counts=candidate_counts,
        deferred_counts=deferred_counts,
    )
    return [
        item for item in items if getattr(item, "state", None) == ITEM_STATE_ENRICHED
    ]


def _build_triage_artifact_writer(context: TriageExecutionContext):
    def write_and_record_artifact(
        *,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> None:
        context.service._record_debug_artifact(
            run_id=context.run_id,
            item_id=item_id,
            kind=kind,
            payload=payload,
            log=context.log.bind(item_id=item_id),
            failure_message=f"Triage {kind} artifact record failed: {{}}",
        )

    return write_and_record_artifact


def _resolve_triage_candidates(
    *,
    context: TriageExecutionContext,
    triage_items: list[Any],
) -> tuple[list[TriageCandidate], bool, dict[str, Any] | None]:
    triage_candidate_builder = getattr(
        context.service, "_build_triage_candidates", None
    )
    if callable(triage_candidate_builder):
        return cast(
            tuple[list[TriageCandidate], bool, dict[str, Any] | None],
            triage_candidate_builder(items=triage_items),
        )
    return build_triage_candidates(context.service, items=triage_items)


def _run_triage_selection(
    *,
    context: TriageExecutionContext,
    triage_items: list[Any],
    triage_candidates: list[TriageCandidate],
    write_and_record_artifact: Any,
) -> None:
    triage_started = time.perf_counter()
    try:
        triage_output = context.service.semantic_triage.select(
            run_id=context.run_id,
            candidates=triage_candidates,
            topics=context.service.settings.topics,
            limit=context.normalized_limit,
            mode=context.service.settings.triage_mode,
            query_mode=context.service.settings.triage_query_mode,
            embedding_model=context.service.settings.triage_embedding_model,
            embedding_dimensions=context.service.settings.triage_embedding_dimensions,
            min_similarity=context.service.settings.triage_min_similarity,
            exploration_rate=context.service.settings.triage_exploration_rate,
            recency_floor=context.service.settings.triage_recency_floor,
            include_debug=context.include_debug,
        )
    except Exception as triage_exc:  # noqa: BLE001
        _handle_triage_failure(
            TriageFailureRequest(
                context=context,
                triage_items=triage_items,
                triage_candidates=triage_candidates,
                triage_started=triage_started,
                write_and_record_artifact=write_and_record_artifact,
                exc=triage_exc,
            )
        )
        return
    _handle_triage_success(
        context=context,
        triage_output=triage_output,
        write_and_record_artifact=write_and_record_artifact,
    )


def _handle_triage_success(
    *,
    context: TriageExecutionContext,
    triage_output: Any,
    write_and_record_artifact: Any,
) -> None:
    stats = triage_output.stats
    _record_triage_success_metrics(
        service=context.service,
        run_id=context.run_id,
        stats=stats,
    )
    for kind, payload in triage_output.artifacts.items():
        write_and_record_artifact(item_id=None, kind=kind, payload=payload)
    selected_total = _mark_selected_triage_items(
        service=context.service,
        selected=list(triage_output.selected),
        log=context.log,
    )
    context.log.info(
        "Triage selected {} of {} candidates mode={} method={}",
        selected_total,
        stats.candidates_total,
        context.service.settings.triage_mode,
        stats.method,
    )


def _handle_triage_failure(request: TriageFailureRequest) -> None:
    triage_duration_ms = int((time.perf_counter() - request.triage_started) * 1000)
    sanitized_error = request.context.service._sanitize_error_message(str(request.exc))
    request.write_and_record_artifact(
        item_id=None,
        kind="error_context",
        payload={
            "stage": "triage",
            "error_type": type(request.exc).__name__,
            "error_message": sanitized_error,
            **request.context.service._classify_exception(request.exc),
        },
    )
    request.context.service.repository.record_metric(
        run_id=request.context.run_id,
        name="pipeline.triage.failed_total",
        value=1,
        unit="count",
    )
    request.context.service.repository.record_metric(
        run_id=request.context.run_id,
        name="pipeline.triage.duration_ms",
        value=triage_duration_ms,
        unit="ms",
    )
    request.context.service.repository.record_metric(
        run_id=request.context.run_id,
        name="pipeline.triage.candidates_total",
        value=len(request.triage_candidates),
        unit="count",
    )
    fallback_marked_total = _mark_fallback_triage_items(
        service=request.context.service,
        items=request.triage_items,
        limit=request.context.normalized_limit,
        log=request.context.log,
    )
    request.context.log.warning(
        "Triage failed, falling back to recency marked={} error={}",
        fallback_marked_total,
        sanitized_error,
    )
