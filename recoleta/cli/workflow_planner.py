from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import date, datetime
from typing import Any, Sequence, cast

from recoleta.cli.workflow_models import (
    GRANULARITY_ORDER,
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
from recoleta.config import resolve_stage_llm_model
from recoleta.models import ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED
from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds
from recoleta.workflow_freshness import (
    analyze_budget_config_fingerprint_candidates,
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
AGGREGATE_TREND_SOURCE_STEP = {
    STEP_TRENDS_WEEK: STEP_TRENDS_DAY,
    STEP_TRENDS_MONTH: STEP_TRENDS_WEEK,
}
PLANNED_RUN_ACTIONS = {"run", "repair", "force"}
ANALYZE_MODEL_REFRESH_REASON = "stale_analysis_model"
UPSTREAM_ANALYZE_MODEL_REFRESH_REASON = "upstream_analyze_model_refresh"
UPSTREAM_TREND_MODEL_REFRESH_REASON = "upstream_trend_model_refresh"
TREND_MODEL_REFRESH_REASONS = {
    UPSTREAM_ANALYZE_MODEL_REFRESH_REASON,
    UPSTREAM_TREND_MODEL_REFRESH_REASON,
}

TREND_SYNTHESIS_PASS_KIND = "trend_synthesis"
TREND_IDEAS_PASS_KIND = "trend_ideas"
PASS_STATUS_SUCCEEDED = "succeeded"
PASS_STATUS_SUPPRESSED = "suppressed"
GRANULARITY_RANK = {
    granularity: index for index, granularity in enumerate(GRANULARITY_ORDER)
}


@dataclass(frozen=True, slots=True)
class _InspectionRequest:
    invocation: WorkflowInvocation
    plan: WorkflowPlan
    repository: Any
    settings: Any
    generation_force: bool
    llm_model: str | None
    translate_include: list[str] | None
    translate_granularities: list[str] | None
    lower_level_task_sets: dict[str, "_LowerLevelTaskSetState"]


@dataclass(frozen=True, slots=True)
class WorkflowPlanningOptions:
    generation_force: bool = False
    llm_model: str | None = None
    translate_include: list[str] | None = None
    translate_granularities: list[str] | None = None


@dataclass(frozen=True, slots=True)
class _DecisionContext:
    invocation: WorkflowInvocation
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None


@dataclass(frozen=True, slots=True)
class _LowerLevelTaskSetState:
    granularity: str
    untouched: bool
    reason: str
    evidence: str | None = None


@dataclass(frozen=True, slots=True)
class _PassOutputCompletionRequest:
    context: _DecisionContext
    repository: Any
    row: Any
    doc_type: str
    expected_freshness_key: str | None
    refresh_legacy_output: bool = False
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
    llm_model: str
    global_llm_model: str
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
    options: WorkflowPlanningOptions | None = None,
) -> list[WorkflowPlanDecision]:
    resolved_options = options or WorkflowPlanningOptions()
    lower_level_task_sets = _inspect_lower_level_task_sets(
        plan=plan,
        repository=repository,
    )
    inspected = [
        _inspect_invocation(
            _InspectionRequest(
                invocation=invocation,
                plan=plan,
                repository=repository,
                settings=settings,
                generation_force=resolved_options.generation_force,
                llm_model=resolved_options.llm_model,
                translate_include=resolved_options.translate_include,
                translate_granularities=resolved_options.translate_granularities,
                lower_level_task_sets=lower_level_task_sets,
            )
        )
        for invocation in plan.invocations
    ]
    decisions = _skip_complete_ingest_windows(inspected, plan=plan)
    return _run_downstream_when_upstream_is_planned(decisions, plan=plan)


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
            llm_model=request.llm_model,
        )
    if invocation.step_id == STEP_PUBLISH:
        return _inspect_publish(
            context=context,
            repository=request.repository,
            settings=request.settings,
        )
    if invocation.step_id in TREND_STEPS:
        if _is_lower_level_generation_context(context=context, plan=request.plan):
            return _inspect_lower_level_trend_output(
                context=context,
                repository=request.repository,
                settings=request.settings,
                llm_model=request.llm_model,
                task_set_state=request.lower_level_task_sets.get(
                    str(context.granularity or "")
                ),
            )
        return _inspect_trend_output(
            context=context,
            repository=request.repository,
            settings=request.settings,
            llm_model=request.llm_model,
        )
    if invocation.step_id in IDEA_STEPS:
        if _is_lower_level_generation_context(context=context, plan=request.plan):
            return _inspect_lower_level_ideas_output(
                context=context,
                repository=request.repository,
                settings=request.settings,
                llm_model=request.llm_model,
                task_set_state=request.lower_level_task_sets.get(
                    str(context.granularity or "")
                ),
            )
        return _inspect_ideas_output(
            context=context,
            repository=request.repository,
            settings=request.settings,
            llm_model=request.llm_model,
        )
    if invocation.step_id == STEP_TRANSLATE:
        return _inspect_translation(
            context=context,
            repository=request.repository,
            settings=request.settings,
            translate_include=request.translate_include,
            translate_granularities=request.translate_granularities,
            llm_model=request.llm_model,
        )
    return _decision(
        context=context,
        action="run",
        reason="not_inspected",
        authority=_authority_for_step(invocation.step_id),
    )


def _is_lower_level_generation_context(
    *,
    context: _DecisionContext,
    plan: WorkflowPlan,
) -> bool:
    return _is_lower_level_granularity(
        granularity=context.granularity,
        target_granularity=plan.target_granularity,
    )


def _is_lower_level_generation_decision(
    *,
    decision: WorkflowPlanDecision,
    plan: WorkflowPlan,
) -> bool:
    if decision.step_id not in TREND_STEPS and decision.step_id not in IDEA_STEPS:
        return False
    return _is_lower_level_granularity(
        granularity=decision.granularity,
        target_granularity=plan.target_granularity,
    )


def _is_lower_level_granularity(
    *,
    granularity: str | None,
    target_granularity: str | None,
) -> bool:
    if granularity is None or target_granularity is None:
        return False
    granularity_rank = GRANULARITY_RANK.get(str(granularity or "").strip().lower())
    target_rank = GRANULARITY_RANK.get(
        str(target_granularity or "").strip().lower()
    )
    if granularity_rank is None or target_rank is None:
        return False
    return granularity_rank < target_rank


def _inspect_lower_level_task_sets(
    *,
    plan: WorkflowPlan,
    repository: Any,
) -> dict[str, _LowerLevelTaskSetState]:
    states: dict[str, _LowerLevelTaskSetState] = {}
    for granularity in _lower_level_granularities_for_plan(plan):
        evidence = _lower_level_task_set_evidence(
            plan=plan,
            repository=repository,
            granularity=granularity,
        )
        if evidence is None:
            states[granularity] = _LowerLevelTaskSetState(
                granularity=granularity,
                untouched=True,
                reason="missing_lower_level_task_set",
            )
            continue
        states[granularity] = _LowerLevelTaskSetState(
            granularity=granularity,
            untouched=False,
            reason=(
                "lower_level_task_set_inspection_unavailable"
                if evidence == "inspection_unavailable"
                else "existing_lower_level_task_set"
            ),
            evidence=evidence,
        )
    return states


def _lower_level_granularities_for_plan(plan: WorkflowPlan) -> list[str]:
    granularities: set[str] = set()
    for invocation in plan.invocations:
        if invocation.step_id not in TREND_STEPS and invocation.step_id not in IDEA_STEPS:
            continue
        context = _invocation_context(invocation=invocation, plan=plan)
        if _is_lower_level_generation_context(context=context, plan=plan):
            granularities.add(str(context.granularity or ""))
    return sorted(
        (granularity for granularity in granularities if granularity),
        key=lambda value: GRANULARITY_RANK.get(value, 999),
    )


def _lower_level_task_set_evidence(
    *,
    plan: WorkflowPlan,
    repository: Any,
    granularity: str,
) -> str | None:
    windows = _lower_level_windows_for_plan(plan=plan, granularity=granularity)
    inspection_unavailable = False
    for period_start, period_end in windows:
        evidence = _lower_level_window_evidence(
            repository=repository,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
        )
        if evidence is None:
            continue
        if evidence == "inspection_unavailable":
            inspection_unavailable = True
            continue
        return evidence
    return "inspection_unavailable" if inspection_unavailable else None


def _lower_level_windows_for_plan(
    *,
    plan: WorkflowPlan,
    granularity: str,
) -> list[tuple[datetime, datetime]]:
    windows: list[tuple[datetime, datetime]] = []
    seen: set[tuple[datetime, datetime]] = set()
    for invocation in plan.invocations:
        if invocation.step_id not in TREND_STEPS and invocation.step_id not in IDEA_STEPS:
            continue
        context = _invocation_context(invocation=invocation, plan=plan)
        if (
            context.granularity != granularity
            or context.period_start is None
            or context.period_end is None
        ):
            continue
        key = (context.period_start, context.period_end)
        if key in seen:
            continue
        seen.add(key)
        windows.append(key)
    return windows


def _lower_level_window_evidence(
    *,
    repository: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> str | None:
    evidence = _lower_level_pass_output_evidence(
        repository=repository,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    if evidence is not None:
        return evidence
    return _lower_level_document_evidence(
        repository=repository,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )


def _lower_level_pass_output_evidence(
    *,
    repository: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> str | None:
    getter = getattr(repository, "get_latest_pass_output", None)
    if not callable(getter):
        return "inspection_unavailable"
    for pass_kind in (TREND_SYNTHESIS_PASS_KIND, TREND_IDEAS_PASS_KIND):
        try:
            row = getter(
                pass_kind=pass_kind,
                status=None,
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
            )
        except Exception:
            return "inspection_unavailable"
        if row is not None:
            return f"pass_output:{pass_kind}"
    return None


def _lower_level_document_evidence(
    *,
    repository: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> str | None:
    list_documents = getattr(repository, "list_documents", None)
    if not callable(list_documents):
        return "inspection_unavailable"
    for doc_type in ("trend", "idea"):
        try:
            rows = list_documents(
                doc_type=doc_type,
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                limit=1,
            )
        except Exception:
            return "inspection_unavailable"
        if _has_any(rows):
            return f"document:{doc_type}"
    return None


def _lower_level_task_set_metadata(
    state: _LowerLevelTaskSetState,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "lower_level_task_set": {
            "granularity": state.granularity,
            "untouched": state.untouched,
        }
    }
    if state.evidence is not None:
        metadata["lower_level_task_set"]["evidence"] = state.evidence
    return metadata


def _inspect_analyze(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    llm_model: str | None,
) -> WorkflowPlanDecision:
    list_items = getattr(repository, "list_items_for_llm_analysis", None)
    period_start = context.period_start
    period_end = context.period_end
    triage_required = _triage_required(settings)
    effective_llm_model = resolve_stage_llm_model(
        settings,
        stage="analyze",
        override=llm_model,
    )
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
            triage_required=triage_required,
            period_start=period_start,
            period_end=period_end,
            llm_model=effective_llm_model,
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
    backlog = _candidate_backlog_metadata(
        repository=repository,
        triage_required=triage_required,
        period_start=period_start,
        period_end=period_end,
        llm_model=effective_llm_model,
    )
    model_refresh_pending = _analysis_model_refresh_pending(
        items=items,
        backlog=backlog,
    )
    configured_limit = _configured_analyze_limit(settings)
    receipt = _latest_analyze_budget_receipt(
        context=context,
        repository=repository,
        settings=settings,
        configured_limit=configured_limit,
        llm_model=llm_model,
    )
    if receipt is not None:
        return _decision(
            context=context,
            action="skip",
            reason="analyze_budget_satisfied",
            authority="workflow_step_receipts",
            estimated_llm_calls=0,
            metadata=_analyze_budget_metadata(
                receipt=receipt,
                configured_limit=configured_limit,
                backlog=backlog,
            ),
        )
    return _decision(
        context=context,
        action="run",
        reason=(
            ANALYZE_MODEL_REFRESH_REASON
            if model_refresh_pending
            else "candidate_items"
        ),
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
    llm_model: str | None,
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
        llm_model=llm_model,
        repository=repository,
    )
    return _classify_pass_output_completion(
        _PassOutputCompletionRequest(
            context=context,
            repository=repository,
            row=row,
            doc_type="trend",
            expected_freshness_key=workflow_freshness_key(expected),
            refresh_legacy_output=_model_change_requires_legacy_refresh(
                settings=settings,
                stage="trends",
                llm_model=llm_model,
            ),
        )
    )


def _inspect_lower_level_trend_output(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    llm_model: str | None,
    task_set_state: _LowerLevelTaskSetState | None,
) -> WorkflowPlanDecision:
    granularity = context.granularity
    period_start = context.period_start
    period_end = context.period_end
    if granularity is None or period_start is None or period_end is None:
        return _pass_output_unavailable_decision(context)
    if task_set_state is None:
        return _pass_output_unavailable_decision(context)
    if task_set_state.untouched:
        return _decision(
            context=context,
            action="run",
            reason=task_set_state.reason,
            authority="pass_outputs",
            metadata=_lower_level_task_set_metadata(task_set_state),
        )
    if _lower_level_model_is_stale(
        context=context,
        repository=repository,
        settings=settings,
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        llm_model=llm_model,
    ):
        return _decision(
            context=context,
            action="run",
            reason="stale_freshness",
            authority="pass_outputs",
            metadata=_lower_level_task_set_metadata(task_set_state),
        )
    return _decision(
        context=context,
        action="skip",
        reason=task_set_state.reason,
        authority="pass_outputs",
        estimated_llm_calls=0,
        metadata=_lower_level_task_set_metadata(task_set_state),
    )


def _inspect_ideas_output(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    llm_model: str | None,
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
        llm_model=llm_model,
    )
    projection_required = str(getattr(row, "status", "") or "") != PASS_STATUS_SUPPRESSED
    return _classify_pass_output_completion(
        _PassOutputCompletionRequest(
            context=context,
            repository=repository,
            row=row,
            doc_type="idea",
            expected_freshness_key=workflow_freshness_key(expected),
            refresh_legacy_output=_model_change_requires_legacy_refresh(
                settings=settings,
                stage="ideas",
                llm_model=llm_model,
            ),
            projection_required=projection_required,
            fallback_skip_reason=(
                "suppressed_ideas"
                if str(getattr(row, "status", "") or "") == PASS_STATUS_SUPPRESSED
                else "fresh_pass_output"
            ),
        )
    )


def _inspect_lower_level_ideas_output(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    llm_model: str | None,
    task_set_state: _LowerLevelTaskSetState | None,
) -> WorkflowPlanDecision:
    granularity = context.granularity
    period_start = context.period_start
    period_end = context.period_end
    if granularity is None or period_start is None or period_end is None:
        return _pass_output_unavailable_decision(context)
    if task_set_state is None:
        return _pass_output_unavailable_decision(context)
    if task_set_state.untouched:
        return _decision(
            context=context,
            action="run",
            reason=task_set_state.reason,
            authority="pass_outputs",
            metadata=_lower_level_task_set_metadata(task_set_state),
        )
    if _lower_level_model_is_stale(
        context=context,
        repository=repository,
        settings=settings,
        pass_kind=TREND_IDEAS_PASS_KIND,
        llm_model=llm_model,
    ):
        return _decision(
            context=context,
            action="run",
            reason="stale_freshness",
            authority="pass_outputs",
            metadata=_lower_level_task_set_metadata(task_set_state),
        )
    return _decision(
        context=context,
        action="skip",
        reason=task_set_state.reason,
        authority="pass_outputs",
        estimated_llm_calls=0,
        metadata=_lower_level_task_set_metadata(task_set_state),
    )


def _lower_level_model_is_stale(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    pass_kind: str,
    llm_model: str | None,
) -> bool:
    if not _decision_context_has_period(context):
        return False
    effective_model = resolve_stage_llm_model(
        settings,
        stage=_stage_for_pass_kind(pass_kind),
        override=llm_model,
    )
    row = _latest_pass_output(
        repository=repository,
        pass_kind=pass_kind,
        statuses=_statuses_for_pass_kind(pass_kind),
        granularity=cast(str, context.granularity),
        period_start=cast(datetime, context.period_start),
        period_end=cast(datetime, context.period_end),
    )
    if row is None:
        return _document_only_model_is_stale(
            settings=settings,
            effective_model=effective_model,
            llm_model=llm_model,
        )
    stored_model = _pass_output_llm_model(row)
    if stored_model:
        return stored_model != effective_model
    global_model = str(getattr(settings, "llm_model", "") or "").strip()
    return bool(global_model) and effective_model != global_model


def _decision_context_has_period(context: _DecisionContext) -> bool:
    return (
        context.granularity is not None
        and context.period_start is not None
        and context.period_end is not None
    )


def _stage_for_pass_kind(pass_kind: str) -> str:
    return "trends" if pass_kind == TREND_SYNTHESIS_PASS_KIND else "ideas"


def _statuses_for_pass_kind(pass_kind: str) -> list[str]:
    if pass_kind == TREND_SYNTHESIS_PASS_KIND:
        return [PASS_STATUS_SUCCEEDED]
    return [PASS_STATUS_SUCCEEDED, PASS_STATUS_SUPPRESSED]


def _document_only_model_is_stale(
    *,
    settings: Any,
    effective_model: str,
    llm_model: str | None,
) -> bool:
    if llm_model is not None:
        return True
    global_model = str(getattr(settings, "llm_model", "") or "").strip()
    return bool(global_model) and effective_model != global_model


def _pass_output_llm_model(row: Any) -> str:
    freshness = _row_workflow_freshness(row) or {}
    components = freshness.get("components")
    if not isinstance(components, dict):
        return ""
    return str(components.get("llm_model") or "").strip()


def _inspect_translation(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    translate_include: list[str] | None,
    translate_granularities: list[str] | None,
    llm_model: str | None,
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
    effective_llm_model = resolve_stage_llm_model(
        settings,
        stage="translation",
        override=llm_model,
    )
    try:
        scan = _scan_translation_plan(
            _TranslationScanRequest(
                repository=repository,
                targets=targets,
                include=include,
                granularities=candidate_granularities,
                source_language_code=source_language_code,
                llm_model=effective_llm_model,
                global_llm_model=str(getattr(settings, "llm_model", "") or ""),
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
        if _localized_output_matches_freshness(
            repository=request.repository,
            candidate=candidate,
            language_code=target_code,
            source_hash=source_hash,
            llm_model=request.llm_model,
            global_llm_model=request.global_llm_model,
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
        if request.refresh_legacy_output:
            return _decision(
                context=request.context,
                action="run",
                reason="stale_freshness",
                authority="pass_outputs",
            )
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


def _model_change_requires_legacy_refresh(
    *,
    settings: Any,
    stage: str,
    llm_model: str | None,
) -> bool:
    if llm_model is not None:
        return True
    effective_model = resolve_stage_llm_model(settings, stage=stage)
    global_model = str(getattr(settings, "llm_model", "") or "").strip()
    return bool(global_model) and effective_model != global_model


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


def _localized_output_matches_freshness(
    *,
    repository: Any,
    candidate: Any,
    language_code: str,
    source_hash: str,
    llm_model: str,
    global_llm_model: str,
) -> bool:
    from recoleta.translation_runtime import localized_output_matches_freshness

    existing = repository.get_localized_output(
        source_kind=getattr(candidate, "source_kind", ""),
        source_record_id=int(getattr(candidate, "source_record_id") or 0),
        language_code=language_code,
    )
    return localized_output_matches_freshness(
        existing=existing,
        source_hash=source_hash,
        llm_model=llm_model,
        global_llm_model=global_llm_model,
        force=False,
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


def _configured_analyze_limit(settings: Any) -> int:
    try:
        value = int(getattr(settings, "analyze_limit", 100) or 100)
    except Exception:
        return 100
    return max(1, value)


def _latest_analyze_budget_receipt(
    *,
    context: _DecisionContext,
    repository: Any,
    settings: Any,
    configured_limit: int,
    llm_model: str | None,
) -> Any | None:
    getter = getattr(repository, "get_latest_workflow_step_receipt", None)
    fingerprints = analyze_budget_config_fingerprint_candidates(
        settings,
        llm_model=llm_model,
    )
    if (
        not callable(getter)
        or not fingerprints
        or context.period_start is None
        or context.period_end is None
    ):
        return None
    for fingerprint in fingerprints:
        try:
            receipt = getter(
                step_id=STEP_ANALYZE,
                granularity=context.granularity,
                period_start=context.period_start,
                period_end=context.period_end,
                config_fingerprint=fingerprint,
                min_selected_total=configured_limit,
                status="succeeded",
            )
        except Exception:
            return None
        if receipt is not None:
            return receipt
    return None


def _candidate_backlog_metadata(
    *,
    repository: Any,
    triage_required: bool,
    period_start: datetime,
    period_end: datetime,
    llm_model: str,
) -> dict[str, Any]:
    counter = getattr(repository, "count_items_for_llm_analysis_by_state", None)
    if not callable(counter):
        return {"present": True}
    try:
        raw_counts = counter(
            triage_required=triage_required,
            period_start=period_start,
            period_end=period_end,
            llm_model=llm_model,
        )
    except Exception:
        return {"present": True}
    if not isinstance(raw_counts, dict):
        return {"present": True}
    counts: dict[str, int] = {}
    for state, total in sorted(raw_counts.items(), key=lambda item: str(item[0])):
        try:
            normalized_total = int(total or 0)
        except Exception:
            continue
        if normalized_total > 0:
            counts[str(state)] = normalized_total
    total = sum(counts.values())
    return {
        "present": total > 0,
        "total": total,
        "by_state": counts,
    }


def _analysis_model_refresh_pending(
    *,
    items: Any,
    backlog: dict[str, Any],
) -> bool:
    by_state = backlog.get("by_state")
    if isinstance(by_state, dict) and any(
        int(by_state.get(state) or 0) > 0
        for state in (ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED)
    ):
        return True
    return any(
        getattr(item, "state", None)
        in {ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED}
        for item in items
    )


def _analyze_budget_metadata(
    *,
    receipt: Any,
    configured_limit: int,
    backlog: dict[str, Any],
) -> dict[str, Any]:
    return {
        "analyze_budget": {
            "configured_limit": configured_limit,
            "receipt_run_id": str(getattr(receipt, "run_id", "") or ""),
            "receipt_selected_total": int(getattr(receipt, "selected_total", 0) or 0),
            "receipt_requested_limit": _optional_int_attr(
                receipt, "requested_limit"
            ),
            "receipt_processed_total": int(getattr(receipt, "processed_total", 0) or 0),
            "receipt_failed_total": int(getattr(receipt, "failed_total", 0) or 0),
        },
        "candidate_backlog": backlog,
    }


def _optional_int_attr(row: Any, attr_name: str) -> int | None:
    value = getattr(row, attr_name, None)
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _skip_complete_ingest_windows(
    decisions: list[WorkflowPlanDecision],
    *,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    content_runs_by_window: set[tuple[datetime | None, datetime | None]] = set()
    content_decisions_by_window: set[tuple[datetime | None, datetime | None]] = set()
    for decision in decisions:
        if decision.step_id not in CONTENT_COMPLETION_STEPS:
            continue
        key = (decision.period_start, decision.period_end)
        content_decisions_by_window.add(key)
        if (
            decision.action in {*PLANNED_RUN_ACTIONS, "blocked"}
            and not _is_lower_level_generation_decision(decision=decision, plan=plan)
        ):
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
    *,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    upstream_updated = _run_generation_when_upstream_is_planned(
        decisions,
        plan=plan,
    )
    return _run_translation_when_generation_is_planned(upstream_updated)


def _run_generation_when_upstream_is_planned(
    decisions: list[WorkflowPlanDecision],
    *,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    analyze_updated = _run_analyze_when_ingest_is_planned(decisions)
    publish_updated = _run_publish_when_analyze_is_planned(analyze_updated)
    trend_updated = _run_trends_when_analyze_is_planned(
        publish_updated,
        plan=plan,
    )
    aggregate_updated = _run_aggregate_trends_when_sources_are_planned(
        trend_updated,
        plan=plan,
    )
    return _run_ideas_when_trends_are_planned(aggregate_updated, plan=plan)


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
                _reactivate_planned_decision(decision, "upstream_ingest_planned")
            )
            continue
        updated.append(decision)
    return updated


def _run_publish_when_analyze_is_planned(
    decisions: list[WorkflowPlanDecision],
) -> list[WorkflowPlanDecision]:
    analyze_run_windows = _planned_analyze_windows(decisions)
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _publish_has_planned_analyze(
            decision=decision,
            analyze_run_windows=analyze_run_windows,
        ):
            updated.append(
                _reactivate_planned_decision(decision, "upstream_analyze_planned")
            )
            continue
        updated.append(decision)
    return updated


def _run_trends_when_analyze_is_planned(
    decisions: list[WorkflowPlanDecision],
    *,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    analyze_run_windows = _planned_analyze_windows(decisions)
    analyze_model_refresh_windows = _planned_analyze_model_refresh_windows(decisions)
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _trend_has_planned_analyze(
            decision=decision,
            analyze_run_windows=analyze_run_windows,
            analyze_model_refresh_windows=analyze_model_refresh_windows,
            plan=plan,
        ):
            reason = (
                UPSTREAM_ANALYZE_MODEL_REFRESH_REASON
                if _is_lower_level_generation_decision(decision=decision, plan=plan)
                else "upstream_analyze_planned"
            )
            updated.append(
                _reactivate_planned_decision(decision, reason)
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


def _planned_analyze_model_refresh_windows(
    decisions: list[WorkflowPlanDecision],
) -> set[tuple[str | None, datetime | None, datetime | None]]:
    return {
        (decision.granularity, decision.period_start, decision.period_end)
        for decision in decisions
        if decision.step_id == STEP_ANALYZE
        and decision.action in PLANNED_RUN_ACTIONS
        and decision.reason == ANALYZE_MODEL_REFRESH_REASON
    }


def _run_aggregate_trends_when_sources_are_planned(
    decisions: list[WorkflowPlanDecision],
    *,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    updated = decisions
    for aggregate_step in (STEP_TRENDS_WEEK, STEP_TRENDS_MONTH):
        updated = _run_aggregate_trend_when_source_is_planned(
            decisions=updated,
            aggregate_step=aggregate_step,
            plan=plan,
        )
    return updated


def _run_aggregate_trend_when_source_is_planned(
    *,
    decisions: list[WorkflowPlanDecision],
    aggregate_step: str,
    plan: WorkflowPlan,
) -> list[WorkflowPlanDecision]:
    source_windows = _planned_trend_source_windows(
        decisions=decisions,
        source_step=AGGREGATE_TREND_SOURCE_STEP[aggregate_step],
    )
    model_refresh_source_windows = _planned_trend_source_windows(
        decisions=decisions,
        source_step=AGGREGATE_TREND_SOURCE_STEP[aggregate_step],
        reasons=TREND_MODEL_REFRESH_REASONS,
    )
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _aggregate_trend_has_planned_source(
            decision=decision,
            aggregate_step=aggregate_step,
            source_windows=source_windows,
            model_refresh_source_windows=model_refresh_source_windows,
            plan=plan,
        ):
            reason = (
                UPSTREAM_TREND_MODEL_REFRESH_REASON
                if _is_lower_level_generation_decision(decision=decision, plan=plan)
                else "upstream_trend_planned"
            )
            updated.append(
                _reactivate_planned_decision(decision, reason)
            )
            continue
        updated.append(decision)
    return updated


def _planned_trend_source_windows(
    *,
    decisions: list[WorkflowPlanDecision],
    source_step: str,
    reasons: set[str] | None = None,
) -> list[tuple[datetime, datetime]]:
    return [
        (decision.period_start, decision.period_end)
        for decision in decisions
        if decision.step_id == source_step
        and decision.action in PLANNED_RUN_ACTIONS
        and (reasons is None or decision.reason in reasons)
        and decision.period_start is not None
        and decision.period_end is not None
    ]


def _publish_has_planned_analyze(
    *,
    decision: WorkflowPlanDecision,
    analyze_run_windows: set[tuple[str | None, datetime | None, datetime | None]],
) -> bool:
    if (
        decision.step_id != STEP_PUBLISH
        or decision.action != "skip"
        or decision.reason != "no_publish_candidates"
    ):
        return False
    return (
        decision.granularity,
        decision.period_start,
        decision.period_end,
    ) in analyze_run_windows


def _aggregate_trend_has_planned_source(
    *,
    decision: WorkflowPlanDecision,
    aggregate_step: str,
    source_windows: list[tuple[datetime, datetime]],
    model_refresh_source_windows: list[tuple[datetime, datetime]],
    plan: WorkflowPlan,
) -> bool:
    if decision.step_id != aggregate_step or decision.action != "skip":
        return False
    candidate_windows = (
        model_refresh_source_windows
        if _is_lower_level_generation_decision(decision=decision, plan=plan)
        else source_windows
    )
    return any(
        _decision_periods_overlap(
            left_start=decision.period_start,
            left_end=decision.period_end,
            right_start=source_start,
            right_end=source_end,
        )
        for source_start, source_end in candidate_windows
    )


def _run_ideas_when_trends_are_planned(
    decisions: list[WorkflowPlanDecision],
    *,
    plan: WorkflowPlan,
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
    model_refresh_trend_run_windows = {
        (
            decision.step_id,
            decision.granularity,
            decision.period_start,
            decision.period_end,
        )
        for decision in decisions
        if decision.step_id in TREND_STEPS
        and decision.action in PLANNED_RUN_ACTIONS
        and (
            decision.reason in TREND_MODEL_REFRESH_REASONS
            or (
                decision.reason == "stale_freshness"
                and _is_lower_level_generation_decision(
                    decision=decision,
                    plan=plan,
                )
            )
        )
    }
    updated: list[WorkflowPlanDecision] = []
    for decision in decisions:
        if _idea_has_planned_trend(
            decision=decision,
            trend_run_windows=trend_run_windows,
            model_refresh_trend_run_windows=model_refresh_trend_run_windows,
            plan=plan,
        ):
            reason = (
                UPSTREAM_TREND_MODEL_REFRESH_REASON
                if _is_lower_level_generation_decision(decision=decision, plan=plan)
                else "upstream_trend_planned"
            )
            updated.append(
                _reactivate_planned_decision(decision, reason)
            )
            continue
        updated.append(decision)
    return updated


def _reactivate_planned_decision(
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
    analyze_model_refresh_windows: set[
        tuple[str | None, datetime | None, datetime | None]
    ],
    plan: WorkflowPlan,
) -> bool:
    if decision.step_id not in TREND_STEPS or decision.action != "skip":
        return False
    window = (
        decision.granularity,
        decision.period_start,
        decision.period_end,
    )
    if _is_lower_level_generation_decision(decision=decision, plan=plan):
        return window in analyze_model_refresh_windows
    return window in analyze_run_windows


def _idea_has_planned_trend(
    *,
    decision: WorkflowPlanDecision,
    trend_run_windows: set[tuple[str, str | None, datetime | None, datetime | None]],
    model_refresh_trend_run_windows: set[
        tuple[str, str | None, datetime | None, datetime | None]
    ],
    plan: WorkflowPlan,
) -> bool:
    matching_trend_step = IDEA_TO_TREND_STEP.get(decision.step_id)
    if matching_trend_step is None or decision.action != "skip":
        return False
    window = (
        matching_trend_step,
        decision.granularity,
        decision.period_start,
        decision.period_end,
    )
    if _is_lower_level_generation_decision(decision=decision, plan=plan):
        return window in model_refresh_trend_run_windows
    return window in trend_run_windows


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
