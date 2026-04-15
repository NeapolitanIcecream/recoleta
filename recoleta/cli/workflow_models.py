from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

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

GRANULARITY_TO_STEP_IDS = {
    "day": (STEP_TRENDS_DAY, STEP_IDEAS_DAY),
    "week": (STEP_TRENDS_WEEK, STEP_IDEAS_WEEK),
    "month": (STEP_TRENDS_MONTH, STEP_IDEAS_MONTH),
}
ALL_STEP_IDS = {
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
GRANULARITY_ORDER = ("day", "week", "month")
DAY_OR_WEEK_SKIP_STEPS = {
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
MONTH_SKIP_STEPS = {
    STEP_INGEST,
    STEP_ANALYZE,
    STEP_PUBLISH,
    STEP_TRANSLATE,
    STEP_SITE_BUILD,
}
DEPLOY_SKIP_STEPS = {STEP_TRANSLATE, STEP_SITE_BUILD}


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


@dataclass(frozen=True, slots=True)
class WorkflowExecutionContext:
    repository: Any
    service: Any
    settings: Any
    run_id: str
    target_granularity: str | None
    target_period_start: datetime | None
    target_period_end: datetime | None
    on_translate_failure: str
    translate_include: list[str]
    translate_granularities: list[str] | None
    delivery_mode: str | None
    publish_requested_explicitly: bool
    analyze_limit: int | None
    publish_limit: int
    repo_dir: Path | None
    remote: str
    branch: str
    commit_message: str | None
    cname: str | None
    pages_config: str
    force: bool
    item_export_scope: str = "linked"


@dataclass(frozen=True, slots=True)
class WorkflowStepResult:
    step_id: str
    status: str
    duration_ms: int
    payload: dict[str, Any] | None = None
    error_type: str | None = None
    error: str | None = None

    def as_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "step_id": self.step_id,
            "status": self.status,
            "duration_ms": self.duration_ms,
        }
        if self.status == "ok":
            payload["label"] = self.step_id.replace(":", " ")
        if self.payload is not None:
            payload["payload"] = self.payload
        if self.error_type is not None:
            payload["error_type"] = self.error_type
        if self.error is not None:
            payload["error"] = self.error
        return payload
