from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import date, datetime
from typing import Any, Sequence

from recoleta.cli.workflow_models import (
    STEP_ANALYZE,
    STEP_IDEAS_DAY,
    STEP_IDEAS_MONTH,
    STEP_IDEAS_WEEK,
    STEP_INGEST,
    STEP_PUBLISH,
    STEP_SITE_BUILD,
    STEP_SITE_DEPLOY,
    STEP_TRANSLATE,
    STEP_TRENDS_DAY,
    STEP_TRENDS_MONTH,
    STEP_TRENDS_WEEK,
    WorkflowInvocation,
    WorkflowPlan,
    WorkflowPlanDecision,
)
from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds
from recoleta.workflow_freshness import (
    build_trend_ideas_freshness,
    build_trend_synthesis_freshness,
    workflow_freshness_key,
)

EXPENSIVE_WORKFLOW_STEPS = {
    STEP_ANALYZE,
    STEP_TRENDS_DAY,
    STEP_TRENDS_WEEK,
    STEP_TRENDS_MONTH,
    STEP_IDEAS_DAY,
    STEP_IDEAS_WEEK,
    STEP_IDEAS_MONTH,
    STEP_TRANSLATE,
}
GENERATION_FORCE_STEPS = {
    STEP_ANALYZE,
    STEP_TRENDS_DAY,
    STEP_TRENDS_WEEK,
    STEP_TRENDS_MONTH,
    STEP_IDEAS_DAY,
    STEP_IDEAS_WEEK,
    STEP_IDEAS_MONTH,
}
CONTENT_COMPLETION_STEPS = {
    STEP_ANALYZE,
    STEP_TRENDS_DAY,
    STEP_TRENDS_WEEK,
    STEP_TRENDS_MONTH,
    STEP_IDEAS_DAY,
    STEP_IDEAS_WEEK,
    STEP_IDEAS_MONTH,
}
TREND_STEPS = {STEP_TRENDS_DAY, STEP_TRENDS_WEEK, STEP_TRENDS_MONTH}
IDEA_STEPS = {STEP_IDEAS_DAY, STEP_IDEAS_WEEK, STEP_IDEAS_MONTH}
TRANSLATABLE_GENERATION_STEPS = {STEP_ANALYZE} | TREND_STEPS | IDEA_STEPS
IDEA_TO_TREND_STEP = {
    STEP_IDEAS_DAY: STEP_TRENDS_DAY,
    STEP_IDEAS_WEEK: STEP_TRENDS_WEEK,
    STEP_IDEAS_MONTH: STEP_TRENDS_MONTH,
}
PLANNED_RUN_ACTIONS = {"run", "repair", "force"}

TREND_SYNTHESIS_PASS_KIND = "trend_synthesis"
TREND_IDEAS_PASS_KIND = "trend_ideas"
PASS_STATUS_SUCCEEDED = "succeeded"
PASS_STATUS_SUPPRESSED = "suppressed"


@dataclass(frozen=True, slots=True)
class _InspectionRequest:
    invocation: WorkflowInvocation
    plan: WorkflowPlan
    repository: Any
    settings: Any
    generation_force: bool
    translate_include: list[str] | None
    translate_granularities: list[str] | None


@dataclass(frozen=True, slots=True)
class _DecisionContext:
    invocation: WorkflowInvocation
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None


@dataclass(frozen=True, slots=True)
class _PassOutputCompletionRequest:
    context: _DecisionContext
    repository: Any
    row: Any
    doc_type: str
    expected_freshness_key: str | None
    projection_required: bool = True
    fallback_skip_reason: str = "fresh_pass_output"


@dataclass(frozen=True, slots=True)
class _TranslationCandidateQuery:
    repository: Any
    granularity: str | None
    include: list[str]
    source_language_code: str
    period_start: datetime | None
    period_end: datetime | None
    all_history: bool


@dataclass(frozen=True, slots=True)
class _TranslationScanRequest:
    repository: Any
    targets: list[str]
    include: list[str]
    granularities: list[str | None]
    source_language_code: str
    period_start: datetime | None
    period_end: datetime | None
    all_history: bool


@dataclass(slots=True)
class _TranslationScanState:
    summaries: dict[tuple[str, str, str | None], dict[str, Any]]
    source_hashes: set[str]
    source_candidate_count: int = 0
    pending_llm_calls: int = 0
    skipped_outputs: int = 0

    @property
    def source_hash(self) -> str | None:
        return next(iter(self.source_hashes)) if len(self.source_hashes) == 1 else None


def plan_workflow_execution(
    *,
    plan: WorkflowPlan,
    repository: Any,
    settings: Any,
    generation_force: bool = False,
    translate_include: list[str] | None = None,
    translate_granularities: list[str] | None = None,
) -> list[WorkflowPlanDecision]:
    inspected = [
        _inspect_invocation(
            _InspectionRequest(
                invocation=invocation,
                plan=plan,
                repository=repository,
                settings=settings,
                generation_force=generation_force,
                translate_include=translate_include,
                translate_granularities=translate_granularities,
            )
        )
        for invocation in plan.invocations
    ]
    decisions = _skip_complete_ingest_windows(inspected)
    return _run_downstream_when_upstream_is_planned(decisions)


def planned_expensive_steps(decisions: list[WorkflowPlanDecision]) -> int:
    return sum(
        1
        for decision in decisions
        if decision.expensive and decision.action in {"run", "repair", "force"}
    )


def decision_payloads(
    decisions: list[WorkflowPlanDecision],
) -> list[dict[str, Any]]:
    return [decision.as_payload() for decision in decisions]


def _inspect_invocation(request: _InspectionRequest) -> WorkflowPlanDecision:
    context = _invocation_context(
        invocation=request.invocation,
        plan=request.plan,
    )
    invocation = request.invocation
    if request.generation_force and invocation.step_id in GENERATION_FORCE_STEPS:
        return _decision(
            context=context,
            action="force",
            reason="generation_force",
            authority=_authority_for_step(invocation.step_id),
        )
    if invocation.step_id == STEP_ANALYZE:
        return _inspect_analyze(
            context=context,
            repository=request.repository,
            settings=request.settings,
        )
    if invocation.step_id == STEP_PUBLISH:
        return _inspect_publish(
            context=context,
            repository=request.repository,
            settings=request.settings,
        )
    if invocation.step_id in TREND_STEPS:
        return _inspect_trend_output(
            context=context,
            repository=request.repository,
            settings=request.settings,
        )
    if invocation.step_id in IDEA_STEPS:
        return _inspect_ideas_output(
            context=context,
            repository=request.repository,
            settings=request.settings,
        )
    if invocation.step_id == STEP_TRANSLATE:
        return _inspect_translation(
            context=context,
            repository=request.repository,
            settings=request.settings,
            translate_include=request.translate_include,
            translate_granularities=request.translate_granularities,
        )
    return _decision(
        context=context,
        action="run",
        reason="not_inspected",
        authority=_authority_for_step(invocation.step_id),
    )


def _inspect_analyze(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
) -> WorkflowPlanDecision:
    list_items = getattr(repository, "list_items_for_llm_analysis", None)
    period_start = context.period_start
    period_end = context.period_end
    if not callable(list_items) or period_start is None or period_end is None:
        return _decision(
            context=context,
            action="run",
            reason="inspection_unavailable",
            authority="item_state",
        )
    try:
        items = list_items(
            limit=1,
            triage_required=_triage_required(settings),
            period_start=period_start,
            period_end=period_end,
        )
    except Exception:
        return _decision(
            context=context,
            action="run",
            reason="inspection_failed",
            authority="item_state",
        )
    if not _has_any(items):
        return _decision(
            context=context,
            action="skip",
            reason="no_candidate_items",
            authority="item_state",
            estimated_llm_calls=0,
        )
    return _decision(
        context=context,
        action="run",
        reason="candidate_items",
        authority="item_state",
    )


def _inspect_publish(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
) -> WorkflowPlanDecision:
    list_items = getattr(repository, "list_items_for_publish", None)
    period_start = context.period_start
    period_end = context.period_end
    if not callable(list_items) or period_start is None or period_end is None:
        return _decision(
            context=context,
            action="run",
            reason="inspection_unavailable",
            authority="deliveries",
        )
    try:
        items = list_items(
            limit=1,
            min_relevance_score=float(
                getattr(settings, "min_relevance_score", 0.0) or 0.0
            ),
            period_start=period_start,
            period_end=period_end,
        )
    except Exception:
        return _decision(
            context=context,
            action="run",
            reason="inspection_failed",
            authority="deliveries",
        )
    if not _has_any(items):
        return _decision(
            context=context,
            action="skip",
            reason="no_publish_candidates",
            authority="deliveries",
        )
    return _decision(
        context=context,
        action="run",
        reason="publish_candidates",
        authority="deliveries",
    )


def _inspect_trend_output(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
) -> WorkflowPlanDecision:
    granularity = context.granularity
    period_start = context.period_start
    period_end = context.period_end
    if granularity is None or period_start is None or period_end is None:
        return _pass_output_unavailable_decision(context)
    row = _latest_pass_output(
        repository=repository,
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        statuses=[PASS_STATUS_SUCCEEDED],
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    if row is None:
        return _decision(
            context=context,
            action="run",
            reason="missing_pass_output",
            authority="pass_outputs",
        )
    expected = build_trend_synthesis_freshness(
        settings=settings,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        repository=repository,
    )
    return _classify_pass_output_completion(
        _PassOutputCompletionRequest(
            context=context,
            repository=repository,
            row=row,
            doc_type="trend",
            expected_freshness_key=workflow_freshness_key(expected),
        )
    )


def _inspect_ideas_output(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
) -> WorkflowPlanDecision:
    granularity = context.granularity
    period_start = context.period_start
    period_end = context.period_end
    if granularity is None or period_start is None or period_end is None:
        return _pass_output_unavailable_decision(context)
    upstream = _latest_pass_output(
        repository=repository,
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        statuses=[PASS_STATUS_SUCCEEDED],
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    upstream_id = _row_id(upstream)
    if upstream_id is None:
        return _decision(
            context=context,
            action="run",
            reason="missing_upstream_trend_pass_output",
            authority="pass_outputs",
        )
    row = _latest_pass_output(
        repository=repository,
        pass_kind=TREND_IDEAS_PASS_KIND,
        statuses=[PASS_STATUS_SUCCEEDED, PASS_STATUS_SUPPRESSED],
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    if row is None:
        return _decision(
            context=context,
            action="run",
            reason="missing_pass_output",
            authority="pass_outputs",
        )
    upstream_ref_id = _upstream_pass_output_id(row)
    if upstream_ref_id is not None and upstream_ref_id != upstream_id:
        return _decision(
            context=context,
            action="run",
            reason="stale_upstream_pass_output",
            authority="pass_outputs",
        )
    expected = build_trend_ideas_freshness(
        settings=settings,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        upstream_pass_output_id=upstream_id,
    )
    projection_required = str(getattr(row, "status", "") or "") != PASS_STATUS_SUPPRESSED
    return _classify_pass_output_completion(
        _PassOutputCompletionRequest(
            context=context,
            repository=repository,
            row=row,
            doc_type="idea",
            expected_freshness_key=workflow_freshness_key(expected),
            projection_required=projection_required,
            fallback_skip_reason=(
                "suppressed_ideas"
                if str(getattr(row, "status", "") or "") == PASS_STATUS_SUPPRESSED
                else "fresh_pass_output"
            ),
        )
    )


def _inspect_translation(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    translate_include: list[str] | None,
    translate_granularities: list[str] | None,
) -> WorkflowPlanDecision:
    targets = _translation_target_codes(settings)
    if not targets:
        return _decision(
            context=context,
            action="skip",
            reason="translation_targets_not_configured",
            authority="localized_outputs",
            estimated_llm_calls=0,
            metadata=_translation_metadata(
                include=_normalized_translation_include(translate_include),
                granularities=_normalized_translation_granularities(
                    translate_granularities
                ),
                target_language_codes=[],
                source_candidate_count=0,
                summaries={},
            ),
        )
    source_language_code = _translation_source_language_code(settings)
    if not source_language_code:
        return _translation_inspection_unavailable_decision(context)
    get_localized_output = getattr(repository, "get_localized_output", None)
    if not callable(get_localized_output):
        return _translation_inspection_unavailable_decision(context)

    include = _normalized_translation_include(translate_include)
    candidate_granularities = _normalized_translation_granularities(
        translate_granularities
    )
    try:
        scan = _scan_translation_plan(
            _TranslationScanRequest(
                repository=repository,
                targets=targets,
                include=include,
                granularities=candidate_granularities,
                source_language_code=source_language_code,
                period_start=context.period_start,
                period_end=context.period_end,
                all_history=context.period_start is None and context.period_end is None,
            )
        )
    except Exception:
        return _decision(
            context=context,
            action="run",
            reason="inspection_failed",
            authority="localized_outputs",
        )

    metadata = _translation_metadata(
        include=include,
        granularities=candidate_granularities,
        target_language_codes=targets,
        source_candidate_count=scan.source_candidate_count,
        summaries=scan.summaries,
    )
    if scan.pending_llm_calls > 0:
        return _decision(
            context=context,
            action="run",
            reason="translation_candidates",
            authority="localized_outputs",
            source_hash=scan.source_hash,
            estimated_llm_calls=scan.pending_llm_calls,
            metadata=metadata,
        )
    if scan.skipped_outputs > 0 or scan.source_candidate_count > 0:
        return _decision(
            context=context,
            action="skip",
            reason="localized_outputs_fresh",
            authority="localized_outputs",
            source_hash=scan.source_hash,
            estimated_llm_calls=0,
            metadata=metadata,
        )
    return _decision(
        context=context,
        action="skip",
        reason="no_translation_candidates",
        authority="localized_outputs",
        estimated_llm_calls=0,
        metadata=metadata,
    )


def _scan_translation_plan(
    request: _TranslationScanRequest,
) -> _TranslationScanState:
    state = _TranslationScanState(summaries={}, source_hashes=set())
    for candidate_granularity in request.granularities:
        candidates = _translation_candidates_for_plan(
            repository=request.repository,
            granularity=candidate_granularity,
            include=request.include,
            source_language_code=request.source_language_code,
            period_start=request.period_start,
            period_end=request.period_end,
            all_history=request.all_history,
        )
        state.source_candidate_count += len(candidates)
        for candidate in candidates:
            _scan_translation_candidate(
                request=request,
                state=state,
                candidate=candidate,
            )
    return state


def _scan_translation_candidate(
    *,
    request: _TranslationScanRequest,
    state: _TranslationScanState,
    candidate: Any,
) -> None:
    source_hash = _translation_payload_hash(candidate)
    state.source_hashes.add(source_hash)
    summary = _translation_summary_for_candidate(
        summaries=state.summaries,
        candidate=candidate,
    )
    summary["source_candidates"] += 1
    for target_code in request.targets:
        summary["scanned"] += 1
        if _localized_output_matches_source_hash(
            repository=request.repository,
            candidate=candidate,
            language_code=target_code,
            source_hash=source_hash,
        ):
            state.skipped_outputs += 1
            summary["skip"] += 1
        else:
            state.pending_llm_calls += 1
            summary["run"] += 1


def _classify_pass_output_completion(
    request: _PassOutputCompletionRequest,
) -> WorkflowPlanDecision:
    row_freshness_key = workflow_freshness_key(_row_workflow_freshness(request.row))
    projection_present = _pass_output_projection_present(request)
    if projection_present is False:
        return _decision(
            context=request.context,
            action="run",
            reason="missing_projection",
            authority="documents",
            freshness_key=row_freshness_key,
        )
    if row_freshness_key is not None:
        return _fresh_pass_output_decision(
            request=request,
            freshness_key=row_freshness_key,
        )
    if projection_present is True:
        return _decision(
            context=request.context,
            action="skip",
            reason="legacy_complete",
            authority="documents",
            estimated_llm_calls=0,
        )
    return _decision(
        context=request.context,
        action="run",
        reason="legacy_unverified",
        authority="pass_outputs",
    )


def _pass_output_projection_present(
    request: _PassOutputCompletionRequest,
) -> bool | None:
    context = request.context
    if not request.projection_required:
        return True
    if (
        context.granularity is None
        or context.period_start is None
        or context.period_end is None
    ):
        return None
    return _projection_contract_present(
        repository=request.repository,
        doc_type=request.doc_type,
        granularity=context.granularity,
        period_start=context.period_start,
        period_end=context.period_end,
    )


def _fresh_pass_output_decision(
    *,
    request: _PassOutputCompletionRequest,
    freshness_key: str,
) -> WorkflowPlanDecision:
    if (
        request.expected_freshness_key is not None
        and freshness_key != request.expected_freshness_key
    ):
        return _decision(
            context=request.context,
            action="run",
            reason="stale_freshness",
            authority="pass_outputs",
            freshness_key=freshness_key,
        )
    return _decision(
        context=request.context,
        action="skip",
        reason=request.fallback_skip_reason,
        authority="pass_outputs",
        freshness_key=freshness_key,
        estimated_llm_calls=0,
    )


def _pass_output_unavailable_decision(
    context: _DecisionContext,
) -> WorkflowPlanDecision:
    return _decision(
        context=context,
        action="run",
        reason="inspection_unavailable",
        authority="pass_outputs",
    )


def _latest_pass_output(
    *,
    repository: Any,
    pass_kind: str,
    statuses: list[str],
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> Any | None:
    getter = getattr(repository, "get_latest_pass_output", None)
    if not callable(getter):
        return None
    rows: list[Any] = []
    for status in statuses:
        try:
            row = getter(
                pass_kind=pass_kind,
                status=status,
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
            )
        except Exception:
            return None
        if row is not None:
            rows.append(row)
    if not rows:
        return None
    return max(rows, key=_pass_output_recency_key)


def _pass_output_recency_key(row: Any) -> tuple[float, int]:
    created_at = getattr(row, "created_at", None)
    timestamp = created_at.timestamp() if isinstance(created_at, datetime) else 0.0
    return (timestamp, _row_id(row) or 0)


def _projection_contract_present(
    *,
    repository: Any,
    doc_type: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> bool | None:
    list_documents = getattr(repository, "list_documents", None)
    list_chunks = getattr(repository, "list_document_chunks_in_period", None)
    if not callable(list_documents) or not callable(list_chunks):
        return None
    try:
        documents = list_documents(
            doc_type=doc_type,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            limit=1,
        )
        summary_chunks = list_chunks(
            doc_type=doc_type,
            kind="summary",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            limit=1,
        )
        meta_chunks = list_chunks(
            doc_type=doc_type,
            kind="meta",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            limit=1,
        )
    except Exception:
        return None
    return _has_any(documents) and _has_any(summary_chunks) and _has_any(meta_chunks)


def _has_any(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    try:
        iterator = iter(value)
    except TypeError:
        return bool(value)
    return any(True for _ in iterator)


def _translation_inspection_unavailable_decision(
    context: _DecisionContext,
) -> WorkflowPlanDecision:
    return _decision(
        context=context,
        action="run",
        reason="inspection_unavailable",
        authority="localized_outputs",
    )


def _translation_target_codes(settings: Any) -> list[str]:
    localization = getattr(settings, "localization", None)
    targets = getattr(localization, "targets", []) if localization is not None else []
    codes: list[str] = []
    for target in targets:
        code = str(getattr(target, "code", "") or "").strip()
        if code and code not in codes:
            codes.append(code)
    return codes


def _translation_source_language_code(settings: Any) -> str:
    localization = getattr(settings, "localization", None)
    return str(getattr(localization, "source_language_code", "") or "").strip()


def _normalized_translation_include(include: list[str] | None) -> list[str]:
    normalized: list[str] = []
    for value in include or ["items", "trends", "ideas"]:
        candidate = str(value or "").strip().lower()
        if candidate and candidate not in normalized:
            normalized.append(candidate)
    return normalized or ["items", "trends", "ideas"]


def _normalized_translation_granularities(
    granularities: Sequence[str | None] | None,
) -> list[str | None]:
    if granularities is None:
        return [None]
    normalized: list[str | None] = []
    for value in granularities:
        candidate = str(value or "").strip().lower() or None
        if candidate not in normalized:
            normalized.append(candidate)
    return normalized or [None]


def _translation_candidates_for_plan(**kwargs: Any) -> list[Any]:
    from recoleta.translation import _incremental_candidates

    query = _TranslationCandidateQuery(
        repository=kwargs["repository"],
        granularity=kwargs.get("granularity"),
        include=list(kwargs["include"]),
        source_language_code=str(kwargs["source_language_code"]),
        period_start=kwargs.get("period_start"),
        period_end=kwargs.get("period_end"),
        all_history=bool(kwargs.get("all_history", False)),
    )
    return _incremental_candidates(
        repository=query.repository,
        granularity=query.granularity,
        include=set(query.include),
        limit=None,
        source_language_code=query.source_language_code,
        period_start=query.period_start,
        period_end=query.period_end,
        all_history=query.all_history,
        materialize_missing_idea_projections=False,
    )


def _translation_payload_hash(candidate: Any) -> str:
    from recoleta.translation import _payload_hash

    payload = getattr(candidate, "payload", {})
    return _payload_hash(payload if isinstance(payload, dict) else {})


def _translation_summary_for_candidate(
    *,
    summaries: dict[tuple[str, str, str | None], dict[str, Any]],
    candidate: Any,
) -> dict[str, Any]:
    source_kind = str(getattr(candidate, "source_kind", "") or "").strip().lower()
    source_granularity = (
        str(getattr(candidate, "granularity", "") or "").strip().lower() or None
    )
    source_bucket = _translation_source_bucket(
        source_kind=source_kind,
        granularity=source_granularity,
    )
    key = (source_bucket, source_kind, source_granularity)
    if key not in summaries:
        summaries[key] = {
            "source_bucket": source_bucket,
            "source_kind": source_kind,
            "source_granularity": source_granularity,
            "source_candidates": 0,
            "scanned": 0,
            "run": 0,
            "skip": 0,
        }
    return summaries[key]


def _localized_output_matches_source_hash(
    *,
    repository: Any,
    candidate: Any,
    language_code: str,
    source_hash: str,
) -> bool:
    existing = repository.get_localized_output(
        source_kind=getattr(candidate, "source_kind", ""),
        source_record_id=int(getattr(candidate, "source_record_id") or 0),
        language_code=language_code,
    )
    return (
        existing is not None
        and str(getattr(existing, "source_hash", "") or "") == source_hash
    )


def _translation_metadata(
    *,
    include: list[str],
    granularities: list[str | None],
    target_language_codes: list[str],
    source_candidate_count: int,
    summaries: dict[tuple[str, str, str | None], dict[str, Any]],
) -> dict[str, Any]:
    return {
        "translation": {
            "include": include,
            "granularities": granularities,
            "target_language_codes": target_language_codes,
            "source_candidate_count": source_candidate_count,
            "by_source": [
                summaries[key]
                for key in sorted(
                    summaries,
                    key=lambda item: (
                        item[0],
                        item[1],
                        "" if item[2] is None else item[2],
                    ),
                )
            ],
        }
    }


def _translation_source_bucket(
    *,
    source_kind: str,
    granularity: str | None,
) -> str:
    normalized_kind = _metric_suffix_token(source_kind)
    if normalized_kind in {"trend_synthesis", "trend_ideas"} and granularity:
        return f"{normalized_kind}.{_metric_suffix_token(granularity)}"
    return normalized_kind


def _metric_suffix_token(value: str) -> str:
    cleaned = [
        char.lower() if char.isalnum() else "_"
        for char in str(value or "").strip()
    ]
    normalized = "".join(cleaned).strip("_")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    return normalized or "unknown"


def _row_workflow_freshness(row: Any) -> dict[str, Any] | None:
    diagnostics = _json_attr(row, "diagnostics_json", default={})
    if not isinstance(diagnostics, dict):
        return None
    freshness = diagnostics.get("workflow_freshness")
    return freshness if isinstance(freshness, dict) else None


def _upstream_pass_output_id(row: Any) -> int | None:
    refs = _json_attr(row, "input_refs_json", default=[])
    if not isinstance(refs, list):
        return None
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        if str(ref.get("pass_kind") or "") != TREND_SYNTHESIS_PASS_KIND:
            continue
        try:
            value = int(ref.get("pass_output_id") or 0)
        except Exception:
            return None
        return value if value > 0 else None
    return None


def _json_attr(row: Any, attr_name: str, *, default: Any) -> Any:
    raw = getattr(row, attr_name, None)
    if raw in (None, ""):
        return default
    try:
        return json.loads(str(raw))
    except Exception:
        return default


def _row_id(row: Any | None) -> int | None:
    if row is None:
        return None
    try:
        value = int(getattr(row, "id") or 0)
    except Exception:
        return None
    return value if value > 0 else None


def _triage_required(settings: Any) -> bool:
    return bool(getattr(settings, "triage_enabled", False)) and bool(
        getattr(settings, "topics", [])
    )


def _skip_complete_ingest_windows(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    content_runs_by_window: set[tuple[datetime | None, datetime | None]] = set()
    content_decisions_by_window: set[tuple[datetime | None, datetime | None]] = set()
    for decision in decisions:
        if decision.step_id not in CONTENT_COMPLETION_STEPS:
            continue
        key = (decision.period_start, decision.period_end)
        content_decisions_by_window.add(key)
        if decision.action in {*PLANNED_RUN_ACTIONS, "blocked"}:
            content_runs_by_window.add(key)

    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        key = (decision.period_start, decision.period_end)
        if (
            decision.step_id == STEP_INGEST
            and key in content_decisions_by_window
            and key not in content_runs_by_window
        ):
            updated.append(
                replace(
                    decision,
                    action="skip",
                    reason="downstream_complete",
                    authority="item_state",
                    estimated_llm_calls=0,
                )
            )
        else:
            updated.append(decision)
    return updated


def _run_downstream_when_upstream_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    upstream_updated = _run_generation_when_upstream_is_planned(decisions)
    return _run_translation_when_generation_is_planned(upstream_updated)


def _run_generation_when_upstream_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    analyze_updated = _run_analyze_when_ingest_is_planned(decisions)
    trend_updated = _run_trends_when_analyze_is_planned(analyze_updated)
    return _run_ideas_when_trends_are_planned(trend_updated)


def _run_analyze_when_ingest_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    ingest_run_windows = {
        (decision.period_start, decision.period_end)
        for decision in decisions
        if decision.step_id == STEP_INGEST and decision.action in PLANNED_RUN_ACTIONS
    }
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if (
            decision.step_id == STEP_ANALYZE
            and decision.action == "skip"
            and decision.reason == "no_candidate_items"
            and (decision.period_start, decision.period_end) in ingest_run_windows
        ):
            updated.append(
                _reactivate_generation_decision(decision, "upstream_ingest_planned")
            )
            continue
        updated.append(decision)
    return updated


def _run_trends_when_analyze_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    analyze_run_windows = _planned_analyze_windows(decisions)
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _trend_has_planned_analyze(
            decision=decision,
            analyze_run_windows=analyze_run_windows,
        ):
            updated.append(
                _reactivate_generation_decision(decision, "upstream_analyze_planned")
            )
            continue
        updated.append(decision)
    return updated


def _planned_analyze_windows(
    decisions: list[WorkflowPlanDecision],
) -> set[tuple[str | None, datetime | None, datetime | None]]:
    return {
        (decision.granularity, decision.period_start, decision.period_end)
        for decision in decisions
        if decision.step_id == STEP_ANALYZE and decision.action in PLANNED_RUN_ACTIONS
    }


def _run_ideas_when_trends_are_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    trend_run_windows = {
        (
            decision.step_id,
            decision.granularity,
            decision.period_start,
            decision.period_end,
        )
        for decision in decisions
        if decision.step_id in TREND_STEPS
        and decision.action in PLANNED_RUN_ACTIONS
    }
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _idea_has_planned_trend(
            decision=decision,
            trend_run_windows=trend_run_windows,
        ):
            updated.append(
                _reactivate_generation_decision(decision, "upstream_trend_planned")
            )
            continue
        updated.append(decision)
    return updated


def _reactivate_generation_decision(
    decision: WorkflowPlanDecision,
    reason: str,
) -> WorkflowPlanDecision:
    return replace(
        decision,
        action="run",
        reason=reason,
        estimated_llm_calls=None,
    )


def _trend_has_planned_analyze(
    *,
    decision: WorkflowPlanDecision,
    analyze_run_windows: set[tuple[str | None, datetime | None, datetime | None]],
) -> bool:
    if decision.step_id not in TREND_STEPS or decision.action != "skip":
        return False
    return (
        decision.granularity,
        decision.period_start,
        decision.period_end,
    ) in analyze_run_windows


def _idea_has_planned_trend(
    *,
    decision: WorkflowPlanDecision,
    trend_run_windows: set[tuple[str, str | None, datetime | None, datetime | None]],
) -> bool:
    matching_trend_step = IDEA_TO_TREND_STEP.get(decision.step_id)
    if matching_trend_step is None or decision.action != "skip":
        return False
    return (
        matching_trend_step,
        decision.granularity,
        decision.period_start,
        decision.period_end,
    ) in trend_run_windows


def _run_translation_when_generation_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    generation_runs = [
        decision
        for decision in decisions
        if decision.step_id in TRANSLATABLE_GENERATION_STEPS
        and decision.action in PLANNED_RUN_ACTIONS
    ]
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if (
            decision.step_id == STEP_TRANSLATE
            and decision.action == "skip"
            and decision.reason in {"localized_outputs_fresh", "no_translation_candidates"}
            and _translation_has_planned_generation(
                translation_decision=decision,
                generation_decisions=generation_runs,
            )
        ):
            updated.append(
                replace(
                    decision,
                    action="run",
                    reason="upstream_generation_planned",
                    estimated_llm_calls=None,
                )
            )
            continue
        updated.append(decision)
    return updated


def _translation_has_planned_generation(
    *,
    translation_decision: WorkflowPlanDecision,
    generation_decisions: list[WorkflowPlanDecision],
) -> bool:
    for generation_decision in generation_decisions:
        if _generation_requires_translation(
            translation_decision=translation_decision,
            generation_decision=generation_decision,
        ):
            return True
    return False


def _generation_requires_translation(
    *,
    translation_decision: WorkflowPlanDecision,
    generation_decision: WorkflowPlanDecision,
) -> bool:
    include = _translation_include_from_decision(translation_decision)
    if generation_decision.step_id == STEP_ANALYZE:
        if "items" not in include:
            return False
        return _decision_periods_overlap(
            left_start=translation_decision.period_start,
            left_end=translation_decision.period_end,
            right_start=generation_decision.period_start,
            right_end=generation_decision.period_end,
        )
    if generation_decision.step_id in TREND_STEPS:
        if "trends" not in include:
            return False
    elif generation_decision.step_id in IDEA_STEPS:
        if "ideas" not in include:
            return False
    else:
        return False
    granularities = _translation_granularities_from_decision(translation_decision)
    if None not in granularities and generation_decision.granularity not in granularities:
        return False
    return _decision_periods_overlap(
        left_start=translation_decision.period_start,
        left_end=translation_decision.period_end,
        right_start=generation_decision.period_start,
        right_end=generation_decision.period_end,
    )


def _translation_include_from_decision(
    decision: WorkflowPlanDecision,
) -> list[str]:
    metadata = decision.metadata if isinstance(decision.metadata, dict) else {}
    translation = metadata.get("translation") if isinstance(metadata, dict) else None
    include = (
        translation.get("include")
        if isinstance(translation, dict)
        else ["items", "trends", "ideas"]
    )
    if not isinstance(include, list):
        return ["items", "trends", "ideas"]
    return _normalized_translation_include([str(value) for value in include])


def _translation_granularities_from_decision(
    decision: WorkflowPlanDecision,
) -> list[str | None]:
    metadata = decision.metadata if isinstance(decision.metadata, dict) else {}
    translation = metadata.get("translation") if isinstance(metadata, dict) else None
    granularities = (
        translation.get("granularities")
        if isinstance(translation, dict)
        else [None]
    )
    if not isinstance(granularities, list):
        return [None]
    return _normalized_translation_granularities(
        [None if value is None else str(value) for value in granularities]
    )


def _decision_periods_overlap(
    *,
    left_start: datetime | None,
    left_end: datetime | None,
    right_start: datetime | None,
    right_end: datetime | None,
) -> bool:
    if left_start is None or left_end is None or right_start is None or right_end is None:
        return True
    return left_start < right_end and right_start < left_end


def _invocation_context(
    *,
    invocation: WorkflowInvocation,
    plan: WorkflowPlan,
) -> _DecisionContext:
    if invocation.step_id in {STEP_INGEST, STEP_ANALYZE, STEP_PUBLISH}:
        return _DecisionContext(
            invocation=invocation,
            granularity="day",
            period_start=invocation.period_start,
            period_end=invocation.period_end,
        )
    if invocation.step_id in {STEP_TRANSLATE, STEP_SITE_BUILD, STEP_SITE_DEPLOY}:
        return _DecisionContext(
            invocation=invocation,
            granularity=plan.target_granularity,
            period_start=plan.target_period_start,
            period_end=plan.target_period_end,
        )
    granularity = _granularity_from_step_id(invocation.step_id)
    if granularity is None or invocation.anchor_date is None:
        return _DecisionContext(
            invocation=invocation,
            granularity=granularity,
            period_start=None,
            period_end=None,
        )
    period_start, period_end = _period_bounds_for_granularity(
        granularity=granularity,
        anchor=invocation.anchor_date,
    )
    return _DecisionContext(
        invocation=invocation,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )


def _granularity_from_step_id(step_id: str) -> str | None:
    if ":" not in step_id:
        return None
    prefix, granularity = step_id.split(":", 1)
    if prefix not in {"trends", "ideas"}:
        return None
    normalized = granularity.strip().lower()
    return normalized if normalized in {"day", "week", "month"} else None


def _period_bounds_for_granularity(
    *, granularity: str, anchor: date
) -> tuple[datetime, datetime]:
    if granularity == "week":
        return week_period_bounds(anchor)
    if granularity == "month":
        return month_period_bounds(anchor)
    return day_period_bounds(anchor)


def _authority_for_step(step_id: str) -> str:
    if step_id == STEP_INGEST:
        return "source_pull_states"
    if step_id == STEP_ANALYZE:
        return "item_state"
    if step_id == STEP_PUBLISH:
        return "deliveries"
    if step_id in TREND_STEPS or step_id in IDEA_STEPS:
        return "pass_outputs"
    if step_id == STEP_TRANSLATE:
        return "localized_outputs"
    if step_id == STEP_SITE_BUILD:
        return "site_files"
    if step_id == STEP_SITE_DEPLOY:
        return "git_remote"
    return "workflow"


def _decision(
    *,
    context: _DecisionContext,
    action: str,
    reason: str,
    authority: str,
    **details: Any,
) -> WorkflowPlanDecision:
    invocation = context.invocation
    return WorkflowPlanDecision(
        step_id=invocation.step_id,
        granularity=context.granularity,
        period_start=context.period_start,
        period_end=context.period_end,
        action=action,
        reason=reason,
        expensive=invocation.step_id in EXPENSIVE_WORKFLOW_STEPS,
        authority=authority,
        anchor_date=invocation.anchor_date,
        freshness_key=details.get("freshness_key"),
        source_hash=details.get("source_hash"),
        estimated_llm_calls=details.get("estimated_llm_calls"),
        metadata=details.get("metadata"),
    )


__all__ = [
    "EXPENSIVE_WORKFLOW_STEPS",
    "decision_payloads",
    "plan_workflow_execution",
    "planned_expensive_steps",
]
