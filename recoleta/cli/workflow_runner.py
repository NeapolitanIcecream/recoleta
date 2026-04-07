from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
import importlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import recoleta.cli as cli
from recoleta.cli.workflow_models import (
    ALL_STEP_IDS,
    DAY_OR_WEEK_SKIP_STEPS,
    DEPLOY_SKIP_STEPS,
    GRANULARITY_ORDER,
    GRANULARITY_TO_STEP_IDS,
    MONTH_SKIP_STEPS,
    STEP_PUBLISH,
    STEP_SITE_BUILD,
    STEP_SITE_DEPLOY,
    STEP_TRANSLATE,
    WorkflowExecutionContext,
    WorkflowInvocation,
    WorkflowPlan,
    WorkflowStepResult,
)
from recoleta.cli.workflow_steps import (
    execute_step,
    localization_targets_configured,
    stdout_guard,
)
from recoleta.models import (
    RUN_TERMINAL_STATE_FAILED,
    RUN_TERMINAL_STATE_SUCCEEDED_CLEAN,
    RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL,
)
from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds


@dataclass(frozen=True, slots=True)
class GranularityPlanRequest:
    workflow_name: str
    command: str
    anchor_date: str | None
    settings: Any
    include_steps: list[str]
    skip_steps: list[str]


@dataclass(frozen=True, slots=True)
class WorkflowLoopRequest:
    repository: Any
    heartbeat_monitor: Any
    plan: WorkflowPlan
    execution_context: WorkflowExecutionContext
    json_output: bool
    on_translate_failure: str


@dataclass(frozen=True, slots=True)
class WorkflowPayloadContext:
    command: str
    run_id: str
    plan: WorkflowPlan
    metrics: list[Any]
    executed_steps: list[str]
    billing_metrics_by_step: dict[str, list[Any]]
    terminal_state: str
    step_results: list[WorkflowStepResult]


def today_utc() -> date:
    override = _workflow_override("_today_utc", current=today_utc)
    if override is not None:
        return override()
    return datetime.now(tz=UTC).date()


def latest_complete_utc_day() -> date:
    return today_utc() - timedelta(days=1)


def normalize_anchor_date(anchor_date: str | None, *, workflow_name: str) -> date:
    if anchor_date is None or not str(anchor_date).strip():
        return latest_complete_utc_day() if workflow_name == "day" else today_utc()
    return cli._parse_anchor_date_option(str(anchor_date).strip())


def granularity_stack(
    *, target_granularity: str, recursive_lower_levels: bool
) -> list[str]:
    normalized = str(target_granularity or "").strip().lower()
    if normalized not in GRANULARITY_ORDER:
        raise ValueError("target granularity must be one of: day, week, month")
    if not recursive_lower_levels:
        return [normalized]
    stop_index = GRANULARITY_ORDER.index(normalized)
    return list(GRANULARITY_ORDER[: stop_index + 1])


def period_bounds_for_granularity(
    *, granularity: str, anchor: date
) -> tuple[datetime, datetime]:
    if granularity == "day":
        return day_period_bounds(anchor)
    if granularity == "week":
        return week_period_bounds(anchor)
    if granularity == "month":
        return month_period_bounds(anchor)
    raise ValueError("granularity must be one of: day, week, month")


def enumerate_days(period_start: datetime, period_end: datetime) -> list[date]:
    cursor = period_start.date()
    dates: list[date] = []
    while cursor < period_end.date():
        dates.append(cursor)
        cursor += timedelta(days=1)
    return dates


def enumerate_weeks_for_period(
    period_start: datetime, period_end: datetime
) -> list[date]:
    cursor = period_start.date()
    anchors: list[date] = []
    while True:
        week_start, _week_end = week_period_bounds(cursor)
        if week_start >= period_end:
            return anchors
        anchors.append(week_start.date())
        cursor = (week_start + timedelta(days=7)).date()


def dedupe_preserve_order(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def parse_step_list(value: str | None) -> list[str]:
    normalized = [
        str(part or "").strip().lower()
        for part in str(value or "").split(",")
        if str(part or "").strip()
    ]
    unknown = sorted({token for token in normalized if token not in ALL_STEP_IDS})
    if unknown:
        raise ValueError("unknown step id(s): " + ", ".join(unknown))
    return dedupe_preserve_order(normalized)


def allowed_skip_steps(*, workflow_name: str) -> set[str]:
    if workflow_name in {"day", "week", "now"}:
        return set(DAY_OR_WEEK_SKIP_STEPS)
    if workflow_name == "month":
        return set(MONTH_SKIP_STEPS)
    if workflow_name == "deploy":
        return set(DEPLOY_SKIP_STEPS)
    return set()


def validate_step_overrides(
    *,
    workflow_name: str,
    include_steps: list[str],
    skip_steps: list[str],
) -> None:
    allowed = allowed_skip_steps(workflow_name=workflow_name)
    unsupported = sorted(
        {step for step in include_steps + skip_steps if step not in allowed}
    )
    if unsupported:
        raise ValueError(
            f"{workflow_name} only supports --include/--skip for: "
            + ", ".join(sorted(allowed))
        )


def metric_snapshot(metrics: list[Any]) -> dict[tuple[str, str | None], float]:
    totals: dict[tuple[str, str | None], float] = {}
    for metric in metrics:
        name = str(getattr(metric, "name", "") or "").strip()
        raw_value = getattr(metric, "value", None)
        if not name or not isinstance(raw_value, (int, float)):
            continue
        raw_unit = getattr(metric, "unit", None)
        unit = str(raw_unit).strip() or None if raw_unit is not None else None
        key = (name, unit)
        totals[key] = float(totals.get(key, 0.0)) + float(raw_value)
    return totals


def metric_diff(
    before: dict[tuple[str, str | None], float],
    after: dict[tuple[str, str | None], float],
) -> list[Any]:
    diff_metrics: list[Any] = []
    for key, after_total in sorted(after.items()):
        delta = float(after_total) - float(before.get(key, 0.0))
        if abs(delta) <= 1e-12:
            continue
        name, unit = key
        diff_metrics.append(SimpleNamespace(name=name, value=delta, unit=unit))
    return diff_metrics


def billing_by_step_payload(
    billing_metrics_by_step: dict[str, list[Any]],
) -> dict[str, Any]:
    return {
        step_id: cli._billing_summary_payload(billing_metrics_by_step[step_id])
        for step_id in sorted(billing_metrics_by_step)
    }


def build_granularity_plan(*, request: GranularityPlanRequest) -> WorkflowPlan:
    target_granularity = (
        "day" if request.workflow_name == "now" else request.workflow_name
    )
    policy = request.settings.workflow_policy_for_granularity(target_granularity)
    anchor = normalize_anchor_date(
        request.anchor_date,
        workflow_name=request.workflow_name,
    )
    target_period_start, target_period_end = period_bounds_for_granularity(
        granularity=target_granularity,
        anchor=anchor,
    )
    requested_steps = ["ingest", "analyze"]
    if str(policy.delivery_mode or "").strip().lower() != "none":
        requested_steps.append(STEP_PUBLISH)
    for granularity in granularity_stack(
        target_granularity=target_granularity,
        recursive_lower_levels=bool(policy.recursive_lower_levels),
    ):
        requested_steps.extend(GRANULARITY_TO_STEP_IDS[granularity])
    skipped = _optional_workflow_steps(
        requested_steps=requested_steps,
        settings=request.settings,
        policy=policy,
    )
    requested_steps = dedupe_preserve_order(requested_steps + request.include_steps)
    requested_steps, skipped = _apply_skip_overrides(
        requested_steps=requested_steps,
        skipped_steps=skipped,
        skip_overrides=request.skip_steps,
    )
    invocations = _build_granularity_invocations(
        target_granularity=target_granularity,
        anchor=anchor,
        target_period_start=target_period_start,
        target_period_end=target_period_end,
        requested_steps=requested_steps,
    )
    return WorkflowPlan(
        operation_kind=f"workflow.run.{target_granularity}",
        command=request.command,
        target_granularity=target_granularity,
        target_period_start=target_period_start,
        target_period_end=target_period_end,
        requested_steps=requested_steps,
        skipped_steps=skipped,
        invocations=invocations,
    )


def build_deploy_plan(
    *,
    command: str,
    settings: Any,
    include_steps: list[str],
    skip_steps: list[str],
) -> WorkflowPlan:
    policy = settings.workflows.deploy
    requested_steps: list[str] = []
    skipped: list[str] = []
    if str(
        policy.translation or ""
    ).strip().lower() == "auto" and localization_targets_configured(settings):
        requested_steps.append(STEP_TRANSLATE)
    else:
        skipped.append(STEP_TRANSLATE)
    if bool(policy.site_build):
        requested_steps.append(STEP_SITE_BUILD)
    else:
        skipped.append(STEP_SITE_BUILD)
    requested_steps.append(STEP_SITE_DEPLOY)
    requested_steps = dedupe_preserve_order(requested_steps + include_steps)
    requested_steps, skipped = _apply_deploy_skip_overrides(
        requested_steps=requested_steps,
        skipped_steps=skipped,
        skip_overrides=skip_steps,
    )
    return WorkflowPlan(
        operation_kind="workflow.run.deploy",
        command=command,
        target_granularity=None,
        target_period_start=None,
        target_period_end=None,
        requested_steps=requested_steps,
        skipped_steps=skipped,
        invocations=[
            WorkflowInvocation(step_id=step_id) for step_id in requested_steps
        ],
    )


def begin_workflow_runtime(
    *,
    command: str,
    log_module: str,
    config_path: Path | None = None,
) -> tuple[Any, Any, Any, Any, str, str, Any, Any]:
    begin_kwargs: dict[str, Any] = {"command": command, "log_module": log_module}
    if config_path is not None:
        begin_kwargs["config_path"] = config_path
    return cli._begin_managed_run(**begin_kwargs)


def execute_workflow_loop(
    *,
    request: WorkflowLoopRequest,
) -> tuple[list[str], dict[str, list[Any]], str, list[WorkflowStepResult]]:
    previous_snapshot = metric_snapshot(
        request.repository.list_metrics(run_id=request.execution_context.run_id)
    )
    billing_metrics_by_step: dict[str, list[Any]] = defaultdict(list)
    executed_steps: list[str] = []
    terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_CLEAN
    step_results: list[WorkflowStepResult] = []
    with cli._graceful_shutdown_signals(), stdout_guard(enabled=request.json_output):
        for invocation in request.plan.invocations:
            try:
                step_payload = execute_step(
                    invocation, context=request.execution_context
                )
            except Exception as exc:
                if (
                    invocation.step_id != STEP_TRANSLATE
                    or request.on_translate_failure == "fail"
                ):
                    raise
                if request.on_translate_failure == "partial_success":
                    terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL
                step_results.append(
                    WorkflowStepResult(
                        step_id=invocation.step_id,
                        status=(
                            "partial_failure"
                            if request.on_translate_failure == "partial_success"
                            else "skipped"
                        ),
                        error_type=type(exc).__name__,
                        error=str(exc),
                    )
                )
                continue
            request.heartbeat_monitor.raise_if_failed()
            current_snapshot = metric_snapshot(
                request.repository.list_metrics(run_id=request.execution_context.run_id)
            )
            billing_metrics_by_step[invocation.step_id].extend(
                metric_diff(previous_snapshot, current_snapshot)
            )
            previous_snapshot = current_snapshot
            if invocation.step_id not in executed_steps:
                executed_steps.append(invocation.step_id)
            if (
                invocation.step_id == STEP_TRANSLATE
                and isinstance(step_payload, dict)
                and int(step_payload.get("failed") or 0) > 0
            ):
                step_status = "skipped"
                if request.on_translate_failure == "partial_success":
                    terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL
                    step_status = "partial_failure"
                step_results.append(
                    WorkflowStepResult(
                        step_id=invocation.step_id,
                        status=step_status,
                        payload=step_payload,
                        error=(
                            "translation completed with failures "
                            f"failed={int(step_payload.get('failed') or 0)} "
                            f"translated={int(step_payload.get('translated') or 0)} "
                            f"skipped={int(step_payload.get('skipped') or 0)}"
                        ),
                    )
                )
                continue
            step_results.append(
                WorkflowStepResult(
                    step_id=invocation.step_id,
                    status="ok",
                    payload=step_payload,
                )
            )
    return executed_steps, billing_metrics_by_step, terminal_state, step_results


def finalize_workflow_success(
    *,
    repository: Any,
    run_id: str,
    executed_steps: list[str],
    billing_metrics_by_step: dict[str, list[Any]],
    terminal_state: str,
) -> None:
    cli._update_run_context(
        repository,
        run_id=run_id,
        executed_steps=executed_steps,
        billing_by_step=billing_by_step_payload(billing_metrics_by_step),
    )
    cli._finish_run(
        repository,
        run_id=run_id,
        success=True,
        terminal_state=terminal_state,
    )


def finish_workflow_failure(
    *, repository: Any, run_id: str, log: Any, message: str
) -> None:
    try:
        cli._finish_run(
            repository,
            run_id=run_id,
            success=False,
            terminal_state=RUN_TERMINAL_STATE_FAILED,
        )
    except Exception:
        log.exception(message)


def granularity_workflow_payload(*, context: WorkflowPayloadContext) -> dict[str, Any]:
    return {
        "status": (
            "ok" if context.terminal_state != RUN_TERMINAL_STATE_FAILED else "error"
        ),
        "command": context.command,
        "run_id": context.run_id,
        "operation_kind": context.plan.operation_kind,
        "target_granularity": context.plan.target_granularity,
        "target_period_start": cli._isoformat_or_none(context.plan.target_period_start),
        "target_period_end": cli._isoformat_or_none(context.plan.target_period_end),
        "requested_steps": context.plan.requested_steps,
        "executed_steps": context.executed_steps,
        "skipped_steps": context.plan.skipped_steps,
        "billing": cli._billing_summary_payload(context.metrics),
        "billing_by_step": billing_by_step_payload(context.billing_metrics_by_step),
        "terminal_state": context.terminal_state,
        "steps": [step_result.as_payload() for step_result in context.step_results],
    }


def deploy_workflow_payload(*, context: WorkflowPayloadContext) -> dict[str, Any]:
    deploy_payload = next(
        (
            step_result.payload
            for step_result in context.step_results
            if step_result.step_id == STEP_SITE_DEPLOY
            and isinstance(step_result.payload, dict)
        ),
        {},
    )
    deploy_payload = deploy_payload if isinstance(deploy_payload, dict) else {}
    return {
        "status": "ok",
        "command": context.command,
        "run_id": context.run_id,
        "operation_kind": context.plan.operation_kind,
        "requested_steps": context.plan.requested_steps,
        "executed_steps": context.executed_steps,
        "skipped_steps": context.plan.skipped_steps,
        "billing": cli._billing_summary_payload(context.metrics),
        "billing_by_step": billing_by_step_payload(context.billing_metrics_by_step),
        "terminal_state": context.terminal_state,
        "branch": deploy_payload.get("branch"),
        "remote": deploy_payload.get("remote"),
        "remote_url": deploy_payload.get("remote_url"),
        "repo_root": deploy_payload.get("repo_root"),
        "commit_sha": deploy_payload.get("commit_sha"),
        "pages_source": {
            "status": deploy_payload.get("pages_source_status"),
            "site_url": deploy_payload.get("site_url"),
        }
        if deploy_payload
        else None,
        "steps": [step_result.as_payload() for step_result in context.step_results],
    }


def _optional_workflow_steps(
    *,
    requested_steps: list[str],
    settings: Any,
    policy: Any,
) -> list[str]:
    skipped: list[str] = []
    if str(
        policy.translation or ""
    ).strip().lower() == "auto" and localization_targets_configured(settings):
        requested_steps.append(STEP_TRANSLATE)
    else:
        skipped.append(STEP_TRANSLATE)
    if bool(policy.site_build):
        requested_steps.append(STEP_SITE_BUILD)
    else:
        skipped.append(STEP_SITE_BUILD)
    return skipped


def _apply_skip_overrides(
    *,
    requested_steps: list[str],
    skipped_steps: list[str],
    skip_overrides: list[str],
) -> tuple[list[str], list[str]]:
    skipped = [step_id for step_id in skipped_steps if step_id not in requested_steps]
    for step_id in skip_overrides:
        if step_id in requested_steps:
            requested_steps.remove(step_id)
        if step_id not in skipped:
            skipped.append(step_id)
    return requested_steps, [
        step_id for step_id in skipped if step_id not in requested_steps
    ]


def _apply_deploy_skip_overrides(
    *,
    requested_steps: list[str],
    skipped_steps: list[str],
    skip_overrides: list[str],
) -> tuple[list[str], list[str]]:
    for step_id in skip_overrides:
        if step_id == STEP_SITE_DEPLOY:
            raise ValueError("deploy does not allow skipping site-deploy")
    return _apply_skip_overrides(
        requested_steps=requested_steps,
        skipped_steps=skipped_steps,
        skip_overrides=skip_overrides,
    )


def _build_granularity_invocations(
    *,
    target_granularity: str,
    anchor: date,
    target_period_start: datetime,
    target_period_end: datetime,
    requested_steps: list[str],
) -> list[WorkflowInvocation]:
    invocations: list[WorkflowInvocation] = []
    if target_granularity == "day":
        day_dates = [anchor]
        week_dates: list[date] = []
        month_dates: list[date] = []
    elif target_granularity == "week":
        day_dates = enumerate_days(target_period_start, target_period_end)
        week_dates = [target_period_start.date()]
        month_dates = []
    else:
        day_dates = enumerate_days(target_period_start, target_period_end)
        week_dates = enumerate_weeks_for_period(target_period_start, target_period_end)
        month_dates = [target_period_start.date()]
    _extend_day_invocations(
        invocations=invocations, day_dates=day_dates, requested_steps=requested_steps
    )
    _extend_window_invocations(
        invocations=invocations,
        anchors=week_dates,
        requested_steps=requested_steps,
        trends_step="trends:week",
        ideas_step="ideas:week",
    )
    _extend_window_invocations(
        invocations=invocations,
        anchors=month_dates,
        requested_steps=requested_steps,
        trends_step="trends:month",
        ideas_step="ideas:month",
    )
    if STEP_TRANSLATE in requested_steps:
        invocations.append(WorkflowInvocation(step_id=STEP_TRANSLATE))
    if STEP_SITE_BUILD in requested_steps:
        invocations.append(WorkflowInvocation(step_id=STEP_SITE_BUILD))
    return invocations


def _extend_day_invocations(
    *,
    invocations: list[WorkflowInvocation],
    day_dates: list[date],
    requested_steps: list[str],
) -> None:
    for day_anchor in day_dates:
        period_start, period_end = day_period_bounds(day_anchor)
        for step_id in ("ingest", "analyze", STEP_PUBLISH):
            if step_id in requested_steps:
                invocations.append(
                    WorkflowInvocation(
                        step_id=step_id,
                        anchor_date=day_anchor,
                        period_start=period_start,
                        period_end=period_end,
                    )
                )
        for step_id in ("trends:day", "ideas:day"):
            if step_id in requested_steps:
                invocations.append(
                    WorkflowInvocation(step_id=step_id, anchor_date=day_anchor)
                )


def _extend_window_invocations(
    *,
    invocations: list[WorkflowInvocation],
    anchors: list[date],
    requested_steps: list[str],
    trends_step: str,
    ideas_step: str,
) -> None:
    for anchor_date in anchors:
        if trends_step in requested_steps:
            invocations.append(
                WorkflowInvocation(step_id=trends_step, anchor_date=anchor_date)
            )
        if ideas_step in requested_steps:
            invocations.append(
                WorkflowInvocation(step_id=ideas_step, anchor_date=anchor_date)
            )


def _workflow_override(name: str, *, current: Any) -> Any | None:
    try:
        workflows_module = importlib.import_module("recoleta.cli.workflows")
    except Exception:
        return None
    override = getattr(workflows_module, name, None)
    if not callable(override) or override is current:
        return None
    default_hooks = getattr(workflows_module, "_MONKEYPATCHABLE_CLOCK_HOOKS", ())
    for hook in default_hooks:
        if (
            callable(hook)
            and getattr(hook, "__name__", None) == name
            and override is hook
        ):
            return None
    return override
