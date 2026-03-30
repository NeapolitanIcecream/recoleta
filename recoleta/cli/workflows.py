from __future__ import annotations

from collections import defaultdict
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Any, Iterator

import recoleta.cli as cli
from recoleta.models import (
    RUN_TERMINAL_STATE_FAILED,
    RUN_TERMINAL_STATE_SUCCEEDED_CLEAN,
    RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL,
)
from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds
from recoleta.types import DEFAULT_TOPIC_STREAM

STEP_INGEST = "ingest"
STEP_ANALYZE = "analyze"
STEP_PUBLISH = "publish"
STEP_TRENDS_DAY = "trends:day"
STEP_IDEAS_DAY = "ideas:day"
STEP_TRENDS_WEEK = "trends:week"
STEP_IDEAS_WEEK = "ideas:week"
STEP_TRENDS_MONTH = "trends:month"
STEP_IDEAS_MONTH = "ideas:month"
STEP_TRANSLATE = "translate"
STEP_SITE_BUILD = "site-build"
STEP_SITE_DEPLOY = "site-deploy"

_GRANULARITY_TO_STEP_IDS = {
    "day": (STEP_TRENDS_DAY, STEP_IDEAS_DAY),
    "week": (STEP_TRENDS_WEEK, STEP_IDEAS_WEEK),
    "month": (STEP_TRENDS_MONTH, STEP_IDEAS_MONTH),
}
_ALL_STEP_IDS = {
    STEP_INGEST,
    STEP_ANALYZE,
    STEP_PUBLISH,
    STEP_TRENDS_DAY,
    STEP_IDEAS_DAY,
    STEP_TRENDS_WEEK,
    STEP_IDEAS_WEEK,
    STEP_TRENDS_MONTH,
    STEP_IDEAS_MONTH,
    STEP_TRANSLATE,
    STEP_SITE_BUILD,
    STEP_SITE_DEPLOY,
}
_GRANULARITY_ORDER = ("day", "week", "month")
_DAY_OR_WEEK_SKIP_STEPS = {
    STEP_INGEST,
    STEP_ANALYZE,
    STEP_PUBLISH,
    STEP_TRENDS_DAY,
    STEP_IDEAS_DAY,
    STEP_TRENDS_WEEK,
    STEP_IDEAS_WEEK,
    STEP_TRANSLATE,
    STEP_SITE_BUILD,
}
_MONTH_SKIP_STEPS = {
    STEP_INGEST,
    STEP_ANALYZE,
    STEP_PUBLISH,
    STEP_TRANSLATE,
    STEP_SITE_BUILD,
}
_DEPLOY_SKIP_STEPS = {STEP_TRANSLATE, STEP_SITE_BUILD}


@dataclass(frozen=True, slots=True)
class WorkflowInvocation:
    step_id: str
    anchor_date: date | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(frozen=True, slots=True)
class WorkflowPlan:
    operation_kind: str
    command: str
    target_granularity: str | None
    target_period_start: datetime | None
    target_period_end: datetime | None
    requested_steps: list[str]
    skipped_steps: list[str]
    invocations: list[WorkflowInvocation]


def _today_utc() -> date:
    return datetime.now(tz=UTC).date()


def _latest_complete_utc_day() -> date:
    return _today_utc() - timedelta(days=1)


def _normalize_anchor_date(
    anchor_date: str | None,
    *,
    workflow_name: str,
) -> date:
    if anchor_date is None or not str(anchor_date).strip():
        if workflow_name == "day":
            return _latest_complete_utc_day()
        return _today_utc()
    return cli._parse_anchor_date_option(str(anchor_date).strip())


def _granularity_stack(
    *,
    target_granularity: str,
    recursive_lower_levels: bool,
) -> list[str]:
    normalized = str(target_granularity or "").strip().lower()
    if normalized not in _GRANULARITY_ORDER:
        raise ValueError("target granularity must be one of: day, week, month")
    if not recursive_lower_levels:
        return [normalized]
    stop_index = _GRANULARITY_ORDER.index(normalized)
    return list(_GRANULARITY_ORDER[: stop_index + 1])


def _period_bounds_for_granularity(
    *,
    granularity: str,
    anchor: date,
) -> tuple[datetime, datetime]:
    if granularity == "day":
        return day_period_bounds(anchor)
    if granularity == "week":
        return week_period_bounds(anchor)
    if granularity == "month":
        return month_period_bounds(anchor)
    raise ValueError("granularity must be one of: day, week, month")


def _enumerate_days(period_start: datetime, period_end: datetime) -> list[date]:
    cursor = period_start.date()
    dates: list[date] = []
    while cursor < period_end.date():
        dates.append(cursor)
        cursor += timedelta(days=1)
    return dates


def _enumerate_weeks_for_period(period_start: datetime, period_end: datetime) -> list[date]:
    cursor = period_start.date()
    anchors: list[date] = []
    while True:
        week_start, _week_end = week_period_bounds(cursor)
        if week_start >= period_end:
            break
        anchors.append(week_start.date())
        cursor = (week_start + timedelta(days=7)).date()
    return anchors


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _parse_step_list(value: str | None) -> list[str]:
    tokens = [
        str(part or "").strip().lower()
        for part in str(value or "").split(",")
    ]
    normalized = [token for token in tokens if token]
    unknown = sorted({token for token in normalized if token not in _ALL_STEP_IDS})
    if unknown:
        raise ValueError("unknown step id(s): " + ", ".join(unknown))
    return _dedupe_preserve_order(normalized)


def _allowed_skip_steps(*, workflow_name: str) -> set[str]:
    if workflow_name in {"day", "week", "now"}:
        return set(_DAY_OR_WEEK_SKIP_STEPS)
    if workflow_name == "month":
        return set(_MONTH_SKIP_STEPS)
    if workflow_name == "deploy":
        return set(_DEPLOY_SKIP_STEPS)
    return set()


def _validate_step_overrides(
    *,
    workflow_name: str,
    include_steps: list[str],
    skip_steps: list[str],
) -> None:
    allowed = _allowed_skip_steps(workflow_name=workflow_name)
    unsupported = sorted({step for step in include_steps + skip_steps if step not in allowed})
    if unsupported:
        raise ValueError(
            f"{workflow_name} only supports --include/--skip for: " + ", ".join(sorted(allowed))
        )


def _localization_targets_configured(settings: Any) -> bool:
    target_codes = getattr(settings, "localization_target_codes", None)
    if callable(target_codes):
        try:
            return bool(target_codes())
        except Exception:
            return False
    localization = getattr(settings, "localization", None)
    return bool(getattr(localization, "targets", []) if localization is not None else [])


def _workflow_scopes(settings: Any) -> list[str]:
    _ = settings
    return [DEFAULT_TOPIC_STREAM]


@contextmanager
def _stdout_guard(*, enabled: bool) -> Iterator[None]:
    if not enabled:
        yield
        return
    with redirect_stdout(sys.stderr):
        yield


@contextmanager
def _delivery_mode_override(*, settings: Any, delivery_mode: str) -> Iterator[None]:
    normalized_mode = str(delivery_mode or "").strip().lower() or "all"
    if normalized_mode == "all":
        yield
        return
    if normalized_mode == "none":
        yield
        return
    if normalized_mode != "local_only":
        raise ValueError("delivery_mode must be one of: all, local_only, none")

    original_publish_targets = list(getattr(settings, "publish_targets", []) or [])
    filtered_publish_targets = [
        target for target in original_publish_targets if target != "telegram"
    ]
    try:
        settings.publish_targets = filtered_publish_targets
        yield
    finally:
        settings.publish_targets = original_publish_targets


def _site_input_dir_from_settings(settings: Any) -> Path:
    markdown_output_dir = Path(settings.markdown_output_dir).expanduser().resolve()
    return markdown_output_dir / "Trends"


def _site_output_dir_from_settings(settings: Any) -> Path:
    return Path(settings.markdown_output_dir).expanduser().resolve() / "site"


def _default_language_code_from_settings(settings: Any) -> str | None:
    localization = getattr(settings, "localization", None)
    if localization is None:
        return None
    return str(getattr(localization, "site_default_language_code", "") or "").strip() or None


def _metric_snapshot(metrics: list[Any]) -> dict[tuple[str, str | None], float]:
    totals: dict[tuple[str, str | None], float] = {}
    for metric in metrics:
        name = str(getattr(metric, "name", "") or "").strip()
        if not name:
            continue
        raw_value = getattr(metric, "value", None)
        if not isinstance(raw_value, (int, float)):
            continue
        unit_value = getattr(metric, "unit", None)
        unit = str(unit_value).strip() or None if unit_value is not None else None
        key = (name, unit)
        totals[key] = float(totals.get(key, 0.0)) + float(raw_value)
    return totals


def _metric_diff(
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


def _append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def _billing_by_step_payload(billing_metrics_by_step: dict[str, list[Any]]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for step_id in sorted(billing_metrics_by_step):
        summary = cli._billing_summary_payload(billing_metrics_by_step[step_id])
        payload[step_id] = summary
    return payload


def _build_granularity_plan(
    *,
    workflow_name: str,
    command: str,
    anchor_date: str | None,
    settings: Any,
    include_steps: list[str],
    skip_steps: list[str],
) -> WorkflowPlan:
    target_granularity = "day" if workflow_name == "now" else workflow_name
    policy = settings.workflow_policy_for_granularity(target_granularity)
    anchor = _normalize_anchor_date(anchor_date, workflow_name=workflow_name)
    target_period_start, target_period_end = _period_bounds_for_granularity(
        granularity=target_granularity,
        anchor=anchor,
    )
    granularities = _granularity_stack(
        target_granularity=target_granularity,
        recursive_lower_levels=bool(policy.recursive_lower_levels),
    )
    requested_steps: list[str] = [STEP_INGEST, STEP_ANALYZE]
    if str(policy.delivery_mode or "").strip().lower() != "none":
        requested_steps.append(STEP_PUBLISH)
    for granularity in granularities:
        trends_step, ideas_step = _GRANULARITY_TO_STEP_IDS[granularity]
        requested_steps.extend([trends_step, ideas_step])
    skipped: list[str] = []
    if (
        str(policy.translation or "").strip().lower() == "auto"
        and _localization_targets_configured(settings)
    ):
        requested_steps.append(STEP_TRANSLATE)
    else:
        skipped.append(STEP_TRANSLATE)
    if bool(policy.site_build):
        requested_steps.append(STEP_SITE_BUILD)
    else:
        skipped.append(STEP_SITE_BUILD)

    requested_steps = _dedupe_preserve_order(requested_steps + include_steps)
    skipped = [step_id for step_id in skipped if step_id not in requested_steps]
    for step_id in skip_steps:
        if step_id in requested_steps:
            requested_steps.remove(step_id)
        _append_unique(skipped, step_id)
    skipped = [step_id for step_id in skipped if step_id not in requested_steps]

    invocations: list[WorkflowInvocation] = []
    if target_granularity == "day":
        day_dates = [anchor]
        week_dates: list[date] = []
        month_dates: list[date] = []
    elif target_granularity == "week":
        day_dates = _enumerate_days(target_period_start, target_period_end)
        week_dates = [target_period_start.date()]
        month_dates = []
    else:
        day_dates = _enumerate_days(target_period_start, target_period_end)
        week_dates = _enumerate_weeks_for_period(target_period_start, target_period_end)
        month_dates = [target_period_start.date()]

    for day_anchor in day_dates:
        period_start, period_end = day_period_bounds(day_anchor)
        if STEP_INGEST in requested_steps:
            invocations.append(
                WorkflowInvocation(
                    step_id=STEP_INGEST,
                    anchor_date=day_anchor,
                    period_start=period_start,
                    period_end=period_end,
                )
            )
        if STEP_ANALYZE in requested_steps:
            invocations.append(
                WorkflowInvocation(
                    step_id=STEP_ANALYZE,
                    anchor_date=day_anchor,
                    period_start=period_start,
                    period_end=period_end,
                )
            )
        if STEP_PUBLISH in requested_steps:
            invocations.append(
                WorkflowInvocation(
                    step_id=STEP_PUBLISH,
                    anchor_date=day_anchor,
                    period_start=period_start,
                    period_end=period_end,
                )
            )
        if STEP_TRENDS_DAY in requested_steps:
            invocations.append(WorkflowInvocation(step_id=STEP_TRENDS_DAY, anchor_date=day_anchor))
        if STEP_IDEAS_DAY in requested_steps:
            invocations.append(WorkflowInvocation(step_id=STEP_IDEAS_DAY, anchor_date=day_anchor))

    for week_anchor in week_dates:
        if STEP_TRENDS_WEEK in requested_steps:
            invocations.append(WorkflowInvocation(step_id=STEP_TRENDS_WEEK, anchor_date=week_anchor))
        if STEP_IDEAS_WEEK in requested_steps:
            invocations.append(WorkflowInvocation(step_id=STEP_IDEAS_WEEK, anchor_date=week_anchor))

    for month_anchor in month_dates:
        if STEP_TRENDS_MONTH in requested_steps:
            invocations.append(
                WorkflowInvocation(step_id=STEP_TRENDS_MONTH, anchor_date=month_anchor)
            )
        if STEP_IDEAS_MONTH in requested_steps:
            invocations.append(
                WorkflowInvocation(step_id=STEP_IDEAS_MONTH, anchor_date=month_anchor)
            )

    if STEP_TRANSLATE in requested_steps:
        invocations.append(WorkflowInvocation(step_id=STEP_TRANSLATE))
    if STEP_SITE_BUILD in requested_steps:
        invocations.append(WorkflowInvocation(step_id=STEP_SITE_BUILD))

    return WorkflowPlan(
        operation_kind=f"workflow.run.{target_granularity}",
        command=command,
        target_granularity=target_granularity,
        target_period_start=target_period_start,
        target_period_end=target_period_end,
        requested_steps=requested_steps,
        skipped_steps=skipped,
        invocations=invocations,
    )


def _build_deploy_plan(
    *,
    command: str,
    settings: Any,
    include_steps: list[str],
    skip_steps: list[str],
) -> WorkflowPlan:
    policy = settings.workflows.deploy
    requested_steps: list[str] = []
    skipped: list[str] = []
    if (
        str(policy.translation or "").strip().lower() == "auto"
        and _localization_targets_configured(settings)
    ):
        requested_steps.append(STEP_TRANSLATE)
    else:
        skipped.append(STEP_TRANSLATE)
    if bool(policy.site_build):
        requested_steps.append(STEP_SITE_BUILD)
    else:
        skipped.append(STEP_SITE_BUILD)
    requested_steps.append(STEP_SITE_DEPLOY)
    requested_steps = _dedupe_preserve_order(requested_steps + include_steps)
    skipped = [step_id for step_id in skipped if step_id not in requested_steps]
    for step_id in skip_steps:
        if step_id == STEP_SITE_DEPLOY:
            raise ValueError("deploy does not allow skipping site-deploy")
        if step_id in requested_steps:
            requested_steps.remove(step_id)
        _append_unique(skipped, step_id)
    skipped = [step_id for step_id in skipped if step_id not in requested_steps]
    invocations = [WorkflowInvocation(step_id=step_id) for step_id in requested_steps]
    return WorkflowPlan(
        operation_kind="workflow.run.deploy",
        command=command,
        target_granularity=None,
        target_period_start=None,
        target_period_end=None,
        requested_steps=requested_steps,
        skipped_steps=skipped,
        invocations=invocations,
    )


def _run_translation_step(
    *,
    repository: Any,
    settings: Any,
    include: list[str],
    granularities: list[str] | None,
    period_start: datetime | None,
    period_end: datetime | None,
    all_history: bool,
    run_id: str,
) -> dict[str, Any]:
    run_translation = cli._import_symbol("recoleta.translation", attr_name="run_translation")
    totals = {
        "scanned": 0,
        "translated": 0,
        "mirrored": 0,
        "skipped": 0,
        "failed": 0,
    }
    scopes = _workflow_scopes(settings)
    normalized_include = ",".join(include)
    per_granularity = granularities if granularities is not None else [None]
    for scope in scopes:
        for granularity in per_granularity:
            result = run_translation(
                repository=repository,
                settings=settings,
                scope=scope,
                granularity=granularity,
                include=normalized_include,
                period_start=period_start,
                period_end=period_end,
                all_history=all_history,
                run_id=run_id,
            )
            totals["scanned"] += int(result.scanned_total)
            totals["translated"] += int(result.translated_total)
            totals["mirrored"] += int(result.mirrored_total)
            totals["skipped"] += int(result.skipped_total)
            totals["failed"] += int(result.failed_total)
            if bool(result.aborted):
                raise RuntimeError(str(result.abort_reason or "translation aborted"))
    return totals


def _run_site_build_step(
    *,
    settings: Any,
    item_export_scope: str = "linked",
) -> dict[str, Any]:
    export_trend_static_site = cli._import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )
    input_dir = _site_input_dir_from_settings(settings)
    output_dir = _site_output_dir_from_settings(settings)
    normalized_item_export_scope = (
        str(item_export_scope or "").strip().lower() or "linked"
    )
    export_kwargs: dict[str, Any] = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "default_language_code": _default_language_code_from_settings(settings),
    }
    if normalized_item_export_scope != "linked":
        export_kwargs["item_export_scope"] = normalized_item_export_scope
    manifest_path = export_trend_static_site(**export_kwargs)
    return {
        "manifest_path": str(manifest_path),
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
    }


def _run_site_deploy_step(
    *,
    settings: Any,
    repo_dir: Path | None,
    remote: str,
    branch: str,
    commit_message: str | None,
    cname: str | None,
    pages_config: str,
    force: bool,
    item_export_scope: str = "linked",
) -> dict[str, Any]:
    deploy_site = cli._import_symbol(
        "recoleta.site_deploy",
        attr_name="deploy_trend_static_site_to_github_pages",
    )
    normalized_item_export_scope = (
        str(item_export_scope or "").strip().lower() or "linked"
    )
    deploy_kwargs: dict[str, Any] = {
        "input_dir": _site_input_dir_from_settings(settings),
        "repo_dir": (repo_dir or Path.cwd()).expanduser().resolve(),
        "remote": remote,
        "branch": branch,
        "commit_message": commit_message,
        "cname": cname,
        "pages_config_mode": pages_config,
        "force": force,
        "default_language_code": _default_language_code_from_settings(settings),
    }
    if normalized_item_export_scope != "linked":
        deploy_kwargs["item_export_scope"] = normalized_item_export_scope
    result = deploy_site(**deploy_kwargs)
    return {
        "remote": str(result.remote),
        "branch": str(result.branch),
        "remote_url": str(result.remote_url),
        "repo_root": str(result.repo_root),
        "commit_sha": result.commit_sha,
        "skipped": bool(result.skipped),
        "site_url": result.pages_source.site_url,
        "pages_source_status": str(result.pages_source.status),
    }


def _human_step_name(step_id: str) -> str:
    return step_id.replace(":", " ")


def _execute_invocation(
    *,
    invocation: WorkflowInvocation,
    repository: Any,
    service: Any,
    settings: Any,
    run_id: str,
    target_granularity: str | None,
    target_period_start: datetime | None,
    target_period_end: datetime | None,
    translate_include: list[str],
    translate_granularities: list[str] | None,
    delivery_mode: str | None,
    publish_requested_explicitly: bool,
    analyze_limit: int | None,
    publish_limit: int,
    repo_dir: Path | None,
    remote: str,
    branch: str,
    commit_message: str | None,
    cname: str | None,
    pages_config: str,
    force: bool,
) -> dict[str, Any]:
    step_id = invocation.step_id
    if step_id == STEP_INGEST:
        result = cli._invoke_service_method(
            service,
            "prepare",
            run_id=run_id,
            period_start=invocation.period_start,
            period_end=invocation.period_end,
        )
        return {"inserted": int(getattr(result, "inserted", 0) or 0), "updated": int(getattr(result, "updated", 0) or 0)}
    if step_id == STEP_ANALYZE:
        result = cli._invoke_service_method(
            service,
            "analyze",
            run_id=run_id,
            limit=analyze_limit,
            period_start=invocation.period_start,
            period_end=invocation.period_end,
        )
        return {"processed": int(getattr(result, "processed", 0) or 0), "failed": int(getattr(result, "failed", 0) or 0)}
    if step_id == STEP_PUBLISH:
        normalized_delivery_mode = str(delivery_mode or "").strip().lower() or "all"
        if normalized_delivery_mode == "none" and publish_requested_explicitly:
            normalized_delivery_mode = "all"
        if normalized_delivery_mode == "none":
            return {"status": "skipped", "reason": "delivery_mode=none"}
        with _delivery_mode_override(settings=settings, delivery_mode=normalized_delivery_mode):
            result = cli._invoke_service_method(
                service,
                "publish",
                run_id=run_id,
                limit=publish_limit,
                period_start=invocation.period_start,
                period_end=invocation.period_end,
            )
        return {
            "sent": int(getattr(result, "sent", 0) or 0),
            "skipped": int(getattr(result, "skipped", 0) or 0),
            "failed": int(getattr(result, "failed", 0) or 0),
        }
    if step_id in {STEP_TRENDS_DAY, STEP_TRENDS_WEEK, STEP_TRENDS_MONTH}:
        granularity = step_id.split(":", 1)[1]
        result = cli._invoke_service_method(
            service,
            "trends",
            run_id=run_id,
            granularity=granularity,
            anchor_date=invocation.anchor_date,
            backfill=False,
            backfill_mode="missing",
            reuse_existing_corpus=True,
        )
        return {
            "granularity": granularity,
            "period_start": cli._isoformat_or_none(getattr(result, "period_start", None)),
            "period_end": cli._isoformat_or_none(getattr(result, "period_end", None)),
        }
    if step_id in {STEP_IDEAS_DAY, STEP_IDEAS_WEEK, STEP_IDEAS_MONTH}:
        granularity = step_id.split(":", 1)[1]
        result = cli._invoke_service_method(
            service,
            "ideas",
            run_id=run_id,
            granularity=granularity,
            anchor_date=invocation.anchor_date,
        )
        return {
            "granularity": granularity,
            "period_start": cli._isoformat_or_none(getattr(result, "period_start", None)),
            "period_end": cli._isoformat_or_none(getattr(result, "period_end", None)),
        }
    if step_id == STEP_TRANSLATE:
        return _run_translation_step(
            repository=repository,
            settings=settings,
            include=translate_include,
            granularities=translate_granularities,
            period_start=target_period_start,
            period_end=target_period_end,
            all_history=not (
                target_period_start is not None or target_period_end is not None
            ),
            run_id=run_id,
        )
    if step_id == STEP_SITE_BUILD:
        return _run_site_build_step(settings=settings)
    if step_id == STEP_SITE_DEPLOY:
        return _run_site_deploy_step(
            settings=settings,
            repo_dir=repo_dir,
            remote=remote,
            branch=branch,
            commit_message=commit_message,
            cname=cname,
            pages_config=pages_config,
            force=force,
        )
    raise ValueError(f"unsupported workflow step: {step_id}")


def execute_granularity_workflow(
    *,
    workflow_name: str,
    command: str,
    anchor_date: str | None = None,
    include: str | None = None,
    skip: str | None = None,
    json_output: bool = False,
    config_path: Path | None = None,
    emit_output: bool = True,
) -> dict[str, Any]:
    include_steps = _parse_step_list(include)
    skip_steps = _parse_step_list(skip)
    _validate_step_overrides(
        workflow_name=workflow_name,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )

    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]
    begin_kwargs: dict[str, Any] = {
        "command": command,
        "log_module": f"cli.workflow.{workflow_name}",
    }
    if config_path is not None:
        begin_kwargs["config_path"] = config_path
    (
        settings,
        repository,
        service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = cli._begin_managed_run(**begin_kwargs)

    plan: WorkflowPlan | None = None
    billing_metrics_by_step: dict[str, list[Any]] = defaultdict(list)
    executed_steps: list[str] = []
    terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_CLEAN
    step_results: list[dict[str, Any]] = []
    analyze_limit = int(getattr(settings, "analyze_limit", 100) or 100)
    publish_limit = max(50, analyze_limit)

    try:
        plan = _build_granularity_plan(
            workflow_name=workflow_name,
            command=command,
            anchor_date=anchor_date,
            settings=settings,
            include_steps=include_steps,
            skip_steps=skip_steps,
        )
        policy = settings.workflow_policy_for_granularity(plan.target_granularity or "day")
        translate_granularities = _granularity_stack(
            target_granularity=plan.target_granularity or "day",
            recursive_lower_levels=bool(policy.recursive_lower_levels),
        )
        cli._update_run_context(
            repository,
            run_id=run_id,
            command=command,
            operation_kind=plan.operation_kind,
            scope=DEFAULT_TOPIC_STREAM,
            granularity=plan.target_granularity,
            period_start=plan.target_period_start,
            period_end=plan.target_period_end,
            target_granularity=plan.target_granularity,
            target_period_start=plan.target_period_start,
            target_period_end=plan.target_period_end,
            requested_steps=plan.requested_steps,
            skipped_steps=plan.skipped_steps,
        )
        previous_snapshot = _metric_snapshot(repository.list_metrics(run_id=run_id))
        with cli._graceful_shutdown_signals(), _stdout_guard(enabled=json_output):
            for invocation in plan.invocations:
                step_id = invocation.step_id
                try:
                    step_payload = _execute_invocation(
                        invocation=invocation,
                        repository=repository,
                        service=service,
                        settings=settings,
                        run_id=run_id,
                        target_granularity=plan.target_granularity,
                        target_period_start=plan.target_period_start,
                        target_period_end=plan.target_period_end,
                        translate_include=list(policy.translate_include),
                        translate_granularities=translate_granularities,
                        delivery_mode=policy.delivery_mode,
                        publish_requested_explicitly=STEP_PUBLISH in include_steps,
                        analyze_limit=analyze_limit,
                        publish_limit=publish_limit,
                        repo_dir=None,
                        remote="origin",
                        branch="gh-pages",
                        commit_message=None,
                        cname=None,
                        pages_config="auto",
                        force=True,
                    )
                except Exception as exc:
                    if step_id == STEP_TRANSLATE and policy.on_translate_failure != "fail":
                        if policy.on_translate_failure == "partial_success":
                            terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL
                        step_results.append(
                            {
                                "step_id": step_id,
                                "status": (
                                    "partial_failure"
                                    if policy.on_translate_failure == "partial_success"
                                    else "skipped"
                                ),
                                "error_type": type(exc).__name__,
                                "error": str(exc),
                            }
                        )
                        continue
                    raise
                heartbeat_monitor.raise_if_failed()
                metrics_after = repository.list_metrics(run_id=run_id)
                current_snapshot = _metric_snapshot(metrics_after)
                billing_metrics_by_step[step_id].extend(
                    _metric_diff(previous_snapshot, current_snapshot)
                )
                previous_snapshot = current_snapshot
                _append_unique(executed_steps, step_id)
                step_results.append(
                    {
                        "step_id": step_id,
                        "status": "ok",
                        "label": _human_step_name(step_id),
                        "payload": step_payload,
                    }
                )
        heartbeat_monitor.raise_if_failed()
        cli._update_run_context(
            repository,
            run_id=run_id,
            executed_steps=executed_steps,
            billing_by_step=_billing_by_step_payload(billing_metrics_by_step),
        )
        cli._finish_run(
            repository,
            run_id=run_id,
            success=True,
            terminal_state=terminal_state,
        )
    except KeyboardInterrupt as exc:
        try:
            cli._finish_run(
                repository,
                run_id=run_id,
                success=False,
                terminal_state=RUN_TERMINAL_STATE_FAILED,
            )
        except Exception:
            log.exception("Workflow finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="Workflow interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            cli._finish_run(
                repository,
                run_id=run_id,
                success=False,
                terminal_state=RUN_TERMINAL_STATE_FAILED,
            )
        except Exception:
            log.exception("Workflow finish failed after lease loss")
        log.warning(
            "Workflow stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        cli._finish_run(
            repository,
            run_id=run_id,
            success=False,
            terminal_state=RUN_TERMINAL_STATE_FAILED,
        )
        log.exception("Workflow execution failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )

    assert plan is not None
    metrics = repository.list_metrics(run_id=run_id)
    billing = cli._billing_summary_payload(metrics)
    payload = {
        "status": "ok" if terminal_state != RUN_TERMINAL_STATE_FAILED else "error",
        "command": command,
        "run_id": run_id,
        "operation_kind": plan.operation_kind,
        "target_granularity": plan.target_granularity,
        "target_period_start": cli._isoformat_or_none(plan.target_period_start),
        "target_period_end": cli._isoformat_or_none(plan.target_period_end),
        "requested_steps": plan.requested_steps,
        "executed_steps": executed_steps,
        "skipped_steps": plan.skipped_steps,
        "billing": billing,
        "billing_by_step": _billing_by_step_payload(billing_metrics_by_step),
        "terminal_state": terminal_state,
        "steps": step_results,
    }
    if json_output:
        if emit_output:
            cli._emit_json(payload)
        return payload

    if emit_output:
        console.print(
            f"[green]{command} completed[/green] "
            f"run_id={run_id} terminal_state={terminal_state} "
            f"steps={len(executed_steps)}/{len(plan.requested_steps)}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
    return payload


def execute_deploy_workflow(
    *,
    command: str,
    include: str | None = None,
    skip: str | None = None,
    repo_dir: Path | None = None,
    remote: str = "origin",
    branch: str = "gh-pages",
    commit_message: str | None = None,
    cname: str | None = None,
    pages_config: str = "auto",
    force: bool = True,
    item_export_scope: str = "linked",
    json_output: bool = False,
    config_path: Path | None = None,
    emit_output: bool = True,
) -> dict[str, Any]:
    include_steps = _parse_step_list(include)
    skip_steps = _parse_step_list(skip)
    _validate_step_overrides(
        workflow_name="deploy",
        include_steps=include_steps,
        skip_steps=skip_steps,
    )

    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]
    begin_kwargs: dict[str, Any] = {
        "command": command,
        "log_module": "cli.workflow.deploy",
    }
    if config_path is not None:
        begin_kwargs["config_path"] = config_path
    (
        settings,
        repository,
        service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = cli._begin_managed_run(**begin_kwargs)
    _ = service
    plan: WorkflowPlan | None = None
    billing_metrics_by_step: dict[str, list[Any]] = defaultdict(list)
    executed_steps: list[str] = []
    terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_CLEAN
    step_results: list[dict[str, Any]] = []

    try:
        plan = _build_deploy_plan(
            command=command,
            settings=settings,
            include_steps=include_steps,
            skip_steps=skip_steps,
        )
        cli._update_run_context(
            repository,
            run_id=run_id,
            command=command,
            operation_kind=plan.operation_kind,
            requested_steps=plan.requested_steps,
            skipped_steps=plan.skipped_steps,
        )
        previous_snapshot = _metric_snapshot(repository.list_metrics(run_id=run_id))
        with cli._graceful_shutdown_signals(), _stdout_guard(enabled=json_output):
            for invocation in plan.invocations:
                step_id = invocation.step_id
                try:
                    if step_id == STEP_TRANSLATE:
                        step_payload = _run_translation_step(
                            repository=repository,
                            settings=settings,
                            include=list(settings.workflows.deploy.translate_include),
                            granularities=None,
                            period_start=None,
                            period_end=None,
                            all_history=True,
                            run_id=run_id,
                        )
                    elif step_id == STEP_SITE_BUILD:
                        step_payload = _run_site_build_step(
                            settings=settings,
                            item_export_scope=item_export_scope,
                        )
                    elif step_id == STEP_SITE_DEPLOY:
                        step_payload = _run_site_deploy_step(
                            settings=settings,
                            repo_dir=repo_dir,
                            remote=remote,
                            branch=branch,
                            commit_message=commit_message,
                            cname=cname,
                            pages_config=pages_config,
                            force=force,
                            item_export_scope=item_export_scope,
                        )
                    else:
                        raise ValueError(f"unsupported deploy step: {step_id}")
                except Exception as exc:
                    if (
                        step_id == STEP_TRANSLATE
                        and settings.workflows.deploy.on_translate_failure != "fail"
                    ):
                        if settings.workflows.deploy.on_translate_failure == "partial_success":
                            terminal_state = RUN_TERMINAL_STATE_SUCCEEDED_PARTIAL
                        step_results.append(
                            {
                                "step_id": step_id,
                                "status": (
                                    "partial_failure"
                                    if settings.workflows.deploy.on_translate_failure
                                    == "partial_success"
                                    else "skipped"
                                ),
                                "error_type": type(exc).__name__,
                                "error": str(exc),
                            }
                        )
                        continue
                    raise
                heartbeat_monitor.raise_if_failed()
                metrics_after = repository.list_metrics(run_id=run_id)
                current_snapshot = _metric_snapshot(metrics_after)
                billing_metrics_by_step[step_id].extend(
                    _metric_diff(previous_snapshot, current_snapshot)
                )
                previous_snapshot = current_snapshot
                _append_unique(executed_steps, step_id)
                step_results.append(
                    {
                        "step_id": step_id,
                        "status": "ok",
                        "label": _human_step_name(step_id),
                        "payload": step_payload,
                    }
                )
        heartbeat_monitor.raise_if_failed()
        cli._update_run_context(
            repository,
            run_id=run_id,
            executed_steps=executed_steps,
            billing_by_step=_billing_by_step_payload(billing_metrics_by_step),
        )
        cli._finish_run(
            repository,
            run_id=run_id,
            success=True,
            terminal_state=terminal_state,
        )
    except KeyboardInterrupt as exc:
        try:
            cli._finish_run(
                repository,
                run_id=run_id,
                success=False,
                terminal_state=RUN_TERMINAL_STATE_FAILED,
            )
        except Exception:
            log.exception("Deploy finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="Workflow interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            cli._finish_run(
                repository,
                run_id=run_id,
                success=False,
                terminal_state=RUN_TERMINAL_STATE_FAILED,
            )
        except Exception:
            log.exception("Deploy finish failed after lease loss")
        log.warning(
            "Deploy stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        cli._finish_run(
            repository,
            run_id=run_id,
            success=False,
            terminal_state=RUN_TERMINAL_STATE_FAILED,
        )
        log.exception("Deploy execution failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )

    assert plan is not None
    metrics = repository.list_metrics(run_id=run_id)
    deploy_payload_candidate = next(
        (
            step_result.get("payload")
            for step_result in step_results
            if step_result.get("step_id") == STEP_SITE_DEPLOY
            and isinstance(step_result.get("payload"), dict)
        ),
        {},
    )
    deploy_payload = (
        deploy_payload_candidate
        if isinstance(deploy_payload_candidate, dict)
        else {}
    )
    payload = {
        "status": "ok",
        "command": command,
        "run_id": run_id,
        "operation_kind": plan.operation_kind,
        "requested_steps": plan.requested_steps,
        "executed_steps": executed_steps,
        "skipped_steps": plan.skipped_steps,
        "billing": cli._billing_summary_payload(metrics),
        "billing_by_step": _billing_by_step_payload(billing_metrics_by_step),
        "terminal_state": terminal_state,
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
        "steps": step_results,
    }
    if json_output:
        if emit_output:
            cli._emit_json(payload)
        return payload
    if emit_output:
        console.print(
            f"[green]{command} completed[/green] "
            f"run_id={run_id} terminal_state={terminal_state} "
            f"steps={len(executed_steps)}/{len(plan.requested_steps)}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
    return payload


def run_daemon_start_command() -> None:
    symbols = cli._runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]
    settings = cli._build_settings()
    console = console_cls(stderr=bool(getattr(settings, "log_json", False)))

    blocking_scheduler_cls = cli._import_symbol(
        "apscheduler.schedulers.blocking",
        attr_name="BlockingScheduler",
    )
    scheduler = blocking_scheduler_cls(
        timezone="UTC",
        executors={"default": {"type": "threadpool", "max_workers": 1}},
        job_defaults={"coalesce": True, "max_instances": 1},
    )

    for schedule_index, schedule in enumerate(list(getattr(settings.daemon, "schedules", []) or [])):
        workflow_name = str(getattr(schedule, "workflow", "") or "").strip().lower()
        if getattr(schedule, "interval_minutes", None) is not None:
            job_id = (
                f"workflow:{workflow_name}:interval:{int(schedule.interval_minutes)}:{schedule_index}"
            )
        else:
            job_id = (
                "workflow:"
                f"{workflow_name}:cron:{str(schedule.weekday)}:"
                f"{int(schedule.hour_utc)}:{int(schedule.minute_utc)}:{schedule_index}"
            )

        def _run_scheduled_workflow(name: str = workflow_name) -> None:
            if name in {"now", "day", "week", "month"}:
                execute_granularity_workflow(
                    workflow_name=name,
                    command=f"daemon {name}",
                )
                return
            if name == "deploy":
                execute_deploy_workflow(command="daemon deploy")
                return
            raise ValueError(f"unsupported daemon workflow: {name}")

        if getattr(schedule, "interval_minutes", None) is not None:
            scheduler.add_job(
                _run_scheduled_workflow,
                "interval",
                minutes=int(schedule.interval_minutes),
                id=job_id,
                replace_existing=True,
            )
            continue
        scheduler.add_job(
            _run_scheduled_workflow,
            "cron",
            day_of_week=str(schedule.weekday),
            hour=int(schedule.hour_utc),
            minute=int(schedule.minute_utc),
            id=job_id,
            replace_existing=True,
        )

    console.print("[cyan]daemon started[/cyan]")
    scheduler_log = logger.bind(module="cli.daemon.start")
    try:
        with cli._graceful_shutdown_signals():
            scheduler.start()
    except KeyboardInterrupt as exc:
        scheduler_log.warning(
            "Daemon stopping signal={} exit_code={} waiting_for_jobs=true",
            cli._interrupt_signal_name(exc),
            cli._interrupt_exit_code(exc),
        )
        try:
            scheduler.shutdown(wait=True)
        except KeyboardInterrupt:
            scheduler_log.warning(
                "Daemon shutdown interrupted again; forcing stop without waiting."
            )
            try:
                scheduler.shutdown(wait=False)
            except Exception:
                scheduler_log.exception("Forced daemon shutdown failed")
        except Exception:
            scheduler_log.exception("Daemon shutdown failed during interrupt")
        raise cli.typer.Exit(code=cli._interrupt_exit_code(exc)) from None
