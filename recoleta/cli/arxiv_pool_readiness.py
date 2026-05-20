from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from recoleta.arxiv_pool import (
    ArxivPoolReadinessPolicy,
    ArxivPoolStore,
    ArxivPoolWindow,
    arxiv_pool_readiness_policy_from_settings,
    build_arxiv_pool_windows_for_period,
    evaluate_arxiv_pool_readiness,
    resolve_arxiv_pool_db_path,
)
from recoleta.cli.workflow_models import (
    STEP_ANALYZE,
    STEP_IDEAS_DAY,
    STEP_IDEAS_MONTH,
    STEP_IDEAS_WEEK,
    STEP_PUBLISH,
    STEP_SITE_BUILD,
    STEP_TRANSLATE,
    STEP_TRENDS_DAY,
    STEP_TRENDS_MONTH,
    STEP_TRENDS_WEEK,
)

ARXIV_POOL_ANALYSIS_DEPENDENT_STEPS = {
    STEP_ANALYZE,
    STEP_PUBLISH,
    STEP_TRENDS_DAY,
    STEP_TRENDS_WEEK,
    STEP_TRENDS_MONTH,
    STEP_IDEAS_DAY,
    STEP_IDEAS_WEEK,
    STEP_IDEAS_MONTH,
    STEP_TRANSLATE,
    STEP_SITE_BUILD,
}
_READINESS_GATE_RANK = {"off": 0, "warn": 1, "strict": 2}


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkflowReadinessPlan:
    status: str
    reason: str | None
    pool_db_path: Path | None
    windows: list[ArxivPoolWindow]
    maturity_lag_days: int = 1
    readiness_gate: str = "strict"
    allow_immature_windows: bool = False

    def as_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason": self.reason,
            "pool_db_path": str(self.pool_db_path) if self.pool_db_path else None,
            "windows_total": len(self.windows),
            "maturity_lag_days": self.maturity_lag_days,
            "readiness_gate": self.readiness_gate,
            "allow_immature_windows": self.allow_immature_windows,
        }


def arxiv_pool_analysis_requested(requested_steps: list[str]) -> bool:
    return bool(set(requested_steps) & ARXIV_POOL_ANALYSIS_DEPENDENT_STEPS)


def skipped_arxiv_pool_workflow_readiness_plan(
    reason: str,
) -> ArxivPoolWorkflowReadinessPlan:
    return ArxivPoolWorkflowReadinessPlan(
        status="skipped",
        reason=reason,
        pool_db_path=None,
        windows=[],
    )


def build_arxiv_pool_workflow_readiness_plan(
    *,
    settings_list: list[Any],
    target_period_start: datetime | None,
    target_period_end: datetime | None,
    requested_steps: list[str],
) -> ArxivPoolWorkflowReadinessPlan:
    if not arxiv_pool_analysis_requested(requested_steps):
        return skipped_arxiv_pool_workflow_readiness_plan("no_analysis_dependent_steps")
    if target_period_start is None or target_period_end is None:
        return skipped_arxiv_pool_workflow_readiness_plan("no_target_period")
    arxiv_settings = _pool_mode_arxiv_source_settings(settings_list)
    if not arxiv_settings:
        return skipped_arxiv_pool_workflow_readiness_plan("no_arxiv_sources")
    if any(str(settings.sources.arxiv.mode) != "pool" for settings in arxiv_settings):
        return skipped_arxiv_pool_workflow_readiness_plan("direct_arxiv_source_present")
    pool_db_path = _shared_arxiv_pool_db_path(arxiv_settings)
    if pool_db_path is None:
        return skipped_arxiv_pool_workflow_readiness_plan("multiple_pool_db_paths")
    readiness_policy = _merged_arxiv_pool_readiness_policy(arxiv_settings)
    return ArxivPoolWorkflowReadinessPlan(
        status="planned",
        reason=None,
        pool_db_path=pool_db_path,
        windows=_arxiv_pool_windows_for_settings(
            arxiv_settings=arxiv_settings,
            target_period_start=target_period_start,
            target_period_end=target_period_end,
        ),
        maturity_lag_days=readiness_policy.maturity_lag_days,
        readiness_gate=readiness_policy.readiness_gate,
        allow_immature_windows=readiness_policy.allow_immature_windows,
    )


def evaluate_arxiv_pool_workflow_readiness(
    plan: ArxivPoolWorkflowReadinessPlan,
) -> dict[str, Any]:
    if plan.pool_db_path is None:
        return {
            "status": "skipped",
            "reason": plan.reason,
            "windows_total": 0,
            "analysis_ready_windows_total": 0,
            "blocked_windows_total": 0,
            "immature_windows_total": 0,
            "unavailable_windows_total": 0,
            "unsafe_override_windows_total": 0,
            "maturity_policy": {
                "timezone": "UTC",
                "maturity_lag_days": plan.maturity_lag_days,
                "maturity_cutoff": None,
                "readiness_gate": plan.readiness_gate,
                "allow_immature_windows": plan.allow_immature_windows,
            },
            "windows": [],
        }
    policy = ArxivPoolReadinessPolicy(
        maturity_lag_days=plan.maturity_lag_days,
        readiness_gate=plan.readiness_gate,
        allow_immature_windows=plan.allow_immature_windows,
    )
    return evaluate_arxiv_pool_readiness(
        store=ArxivPoolStore(plan.pool_db_path),
        windows=plan.windows,
        policy=policy,
    )


def arxiv_pool_workflow_readiness_should_block(
    plan: ArxivPoolWorkflowReadinessPlan,
    readiness: dict[str, Any],
) -> bool:
    if plan.readiness_gate != "strict":
        return False
    return int(readiness.get("blocked_windows_total") or 0) > 0


def _pool_mode_arxiv_source_settings(settings_list: list[Any]) -> list[Any]:
    return [
        settings
        for settings in settings_list
        if bool(getattr(settings.sources.arxiv, "enabled", False))
    ]


def _shared_arxiv_pool_db_path(arxiv_settings: list[Any]) -> Path | None:
    pool_paths = {resolve_arxiv_pool_db_path(settings) for settings in arxiv_settings}
    if len(pool_paths) != 1:
        return None
    return next(iter(pool_paths))


def _merged_arxiv_pool_readiness_policy(
    arxiv_settings: list[Any],
) -> ArxivPoolReadinessPolicy:
    readiness_policies = [
        arxiv_pool_readiness_policy_from_settings(settings)
        for settings in arxiv_settings
    ]
    readiness_gate = max(
        (policy.readiness_gate for policy in readiness_policies),
        key=lambda gate: _READINESS_GATE_RANK[gate],
    )
    return ArxivPoolReadinessPolicy(
        maturity_lag_days=max(policy.maturity_lag_days for policy in readiness_policies),
        readiness_gate=readiness_gate,
        allow_immature_windows=all(
            policy.allow_immature_windows for policy in readiness_policies
        ),
    )


def _arxiv_pool_windows_for_settings(
    *,
    arxiv_settings: list[Any],
    target_period_start: datetime,
    target_period_end: datetime,
) -> list[ArxivPoolWindow]:
    windows_by_key: dict[tuple[str, str, str, int], ArxivPoolWindow] = {}
    for settings in arxiv_settings:
        for window in build_arxiv_pool_windows_for_period(
            queries=list(settings.sources.arxiv.queries),
            period_start=target_period_start,
            period_end=target_period_end,
            max_results=int(settings.sources.arxiv.max_results_per_run),
        ):
            key = (
                window.query_text,
                window.period_start.isoformat(),
                window.period_end.isoformat(),
                window.max_results,
            )
            windows_by_key[key] = window
    return list(windows_by_key.values())
