from __future__ import annotations

from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Iterator

import recoleta.cli as cli
from recoleta.cli.site_support import (
    default_language_code_from_settings,
    normalize_item_export_scope,
    site_input_dir_from_settings,
    site_output_dir_from_settings,
)
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
    WorkflowExecutionContext,
    WorkflowInvocation,
)


@dataclass(frozen=True, slots=True)
class TranslationStepRequest:
    repository: Any
    settings: Any
    include: list[str]
    granularities: list[str] | None
    period_start: datetime | None
    period_end: datetime | None
    all_history: bool
    run_id: str
    fail_on_failed_outputs: bool = False


@dataclass(frozen=True, slots=True)
class SiteDeployStepRequest:
    settings: Any
    repo_dir: Path | None
    remote: str
    branch: str
    commit_message: str | None
    cname: str | None
    pages_config: str
    force: bool
    item_export_scope: str = "linked"


def localization_targets_configured(settings: Any) -> bool:
    target_codes = getattr(settings, "localization_target_codes", None)
    if callable(target_codes):
        try:
            return bool(target_codes())
        except Exception:
            return False
    localization = getattr(settings, "localization", None)
    return bool(
        getattr(localization, "targets", []) if localization is not None else []
    )


@contextmanager
def stdout_guard(*, enabled: bool) -> Iterator[None]:
    if not enabled:
        yield
        return
    with redirect_stdout(sys.stderr):
        yield


@contextmanager
def delivery_mode_override(*, settings: Any, delivery_mode: str) -> Iterator[None]:
    normalized_mode = str(delivery_mode or "").strip().lower() or "all"
    if normalized_mode in {"all", "none"}:
        yield
        return
    if normalized_mode != "local_only":
        raise ValueError("delivery_mode must be one of: all, local_only, none")
    original_publish_targets = list(getattr(settings, "publish_targets", []) or [])
    try:
        settings.publish_targets = [
            target for target in original_publish_targets if target != "telegram"
        ]
        yield
    finally:
        settings.publish_targets = original_publish_targets


def run_translation_step(*, request: TranslationStepRequest) -> dict[str, Any]:
    run_translation = cli._import_symbol(
        "recoleta.translation", attr_name="run_translation"
    )
    materialize_localized_projections = cli._import_symbol(
        "recoleta.translation", attr_name="materialize_localized_projections"
    )
    totals = {
        "scanned": 0,
        "translated": 0,
        "mirrored": 0,
        "skipped": 0,
        "failed": 0,
    }
    abort_reason: str | None = None
    normalized_include = ",".join(request.include)
    for granularity in (
        request.granularities if request.granularities is not None else [None]
    ):
        result = run_translation(
            repository=request.repository,
            settings=request.settings,
            granularity=granularity,
            include=normalized_include,
            period_start=request.period_start,
            period_end=request.period_end,
            all_history=request.all_history,
            run_id=request.run_id,
        )
        totals["scanned"] += int(result.scanned_total)
        totals["translated"] += int(result.translated_total)
        totals["mirrored"] += int(result.mirrored_total)
        totals["skipped"] += int(result.skipped_total)
        totals["failed"] += int(result.failed_total)
        if bool(result.aborted):
            abort_reason = str(result.abort_reason or "translation aborted")
            break
    if abort_reason is not None:
        raise RuntimeError(abort_reason)
    materialize_localized_projections(
        repository=request.repository,
        settings=request.settings,
    )
    if request.fail_on_failed_outputs and totals["failed"] > 0:
        raise RuntimeError(
            "translation completed with failures "
            f"failed={totals['failed']} translated={totals['translated']} "
            f"skipped={totals['skipped']}"
        )
    return totals


def run_site_build_step(
    *,
    settings: Any,
    item_export_scope: str = "linked",
) -> dict[str, Any]:
    export_trend_static_site = cli._import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )
    normalized_item_export_scope = normalize_item_export_scope(item_export_scope)
    export_kwargs: dict[str, Any] = {
        "input_dir": site_input_dir_from_settings(settings),
        "output_dir": site_output_dir_from_settings(settings),
        "default_language_code": default_language_code_from_settings(settings),
    }
    if normalized_item_export_scope != "linked":
        export_kwargs["item_export_scope"] = normalized_item_export_scope
    manifest_path = export_trend_static_site(**export_kwargs)
    return {
        "manifest_path": str(manifest_path),
        "input_dir": str(export_kwargs["input_dir"]),
        "output_dir": str(export_kwargs["output_dir"]),
    }


def run_site_deploy_step(*, request: SiteDeployStepRequest) -> dict[str, Any]:
    deploy_site = cli._import_symbol(
        "recoleta.site_deploy",
        attr_name="deploy_trend_static_site_to_github_pages",
    )
    normalized_item_export_scope = normalize_item_export_scope(
        request.item_export_scope
    )
    deploy_kwargs: dict[str, Any] = {
        "input_dir": site_input_dir_from_settings(request.settings),
        "repo_dir": (request.repo_dir or Path.cwd()).expanduser().resolve(),
        "remote": request.remote,
        "branch": request.branch,
        "commit_message": request.commit_message,
        "cname": request.cname,
        "pages_config_mode": request.pages_config,
        "force": request.force,
        "default_language_code": default_language_code_from_settings(request.settings),
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


def _execute_ingest_step(
    invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    result = cli._invoke_service_method(
        context.service,
        "prepare",
        run_id=context.run_id,
        period_start=invocation.period_start,
        period_end=invocation.period_end,
    )
    return {
        "inserted": int(getattr(result, "inserted", 0) or 0),
        "updated": int(getattr(result, "updated", 0) or 0),
    }


def _execute_analyze_step(
    invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    result = cli._invoke_service_method(
        context.service,
        "analyze",
        run_id=context.run_id,
        limit=context.analyze_limit,
        period_start=invocation.period_start,
        period_end=invocation.period_end,
    )
    return {
        "processed": int(getattr(result, "processed", 0) or 0),
        "failed": int(getattr(result, "failed", 0) or 0),
    }


def _execute_publish_step(
    invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    normalized_delivery_mode = str(context.delivery_mode or "").strip().lower() or "all"
    if normalized_delivery_mode == "none" and context.publish_requested_explicitly:
        normalized_delivery_mode = "all"
    if normalized_delivery_mode == "none":
        return {"status": "skipped", "reason": "delivery_mode=none"}
    with delivery_mode_override(
        settings=context.settings, delivery_mode=normalized_delivery_mode
    ):
        result = cli._invoke_service_method(
            context.service,
            "publish",
            run_id=context.run_id,
            limit=context.publish_limit,
            period_start=invocation.period_start,
            period_end=invocation.period_end,
        )
    return {
        "sent": int(getattr(result, "sent", 0) or 0),
        "skipped": int(getattr(result, "skipped", 0) or 0),
        "failed": int(getattr(result, "failed", 0) or 0),
    }


def _execute_trends_step(
    invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    granularity = invocation.step_id.split(":", 1)[1]
    result = cli._invoke_service_method(
        context.service,
        "trends",
        run_id=context.run_id,
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


def _execute_ideas_step(
    invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    granularity = invocation.step_id.split(":", 1)[1]
    result = cli._invoke_service_method(
        context.service,
        "ideas",
        run_id=context.run_id,
        granularity=granularity,
        anchor_date=invocation.anchor_date,
    )
    return {
        "granularity": granularity,
        "period_start": cli._isoformat_or_none(getattr(result, "period_start", None)),
        "period_end": cli._isoformat_or_none(getattr(result, "period_end", None)),
    }


def _execute_translate_step(
    _invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    return run_translation_step(
        request=TranslationStepRequest(
            repository=context.repository,
            settings=context.settings,
            include=context.translate_include,
            granularities=context.translate_granularities,
            period_start=context.target_period_start,
            period_end=context.target_period_end,
            all_history=not (
                context.target_period_start is not None
                or context.target_period_end is not None
            ),
            run_id=context.run_id,
            fail_on_failed_outputs=context.on_translate_failure == "fail",
        )
    )


def _execute_site_build_step(
    _invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    return run_site_build_step(
        settings=context.settings,
        item_export_scope=context.item_export_scope,
    )


def _execute_site_deploy_step(
    _invocation: WorkflowInvocation, context: WorkflowExecutionContext
) -> dict[str, Any]:
    return run_site_deploy_step(
        request=SiteDeployStepRequest(
            settings=context.settings,
            repo_dir=context.repo_dir,
            remote=context.remote,
            branch=context.branch,
            commit_message=context.commit_message,
            cname=context.cname,
            pages_config=context.pages_config,
            force=context.force,
            item_export_scope=context.item_export_scope,
        )
    )


_STEP_EXECUTORS = {
    STEP_INGEST: _execute_ingest_step,
    STEP_ANALYZE: _execute_analyze_step,
    STEP_PUBLISH: _execute_publish_step,
    STEP_TRANSLATE: _execute_translate_step,
    STEP_SITE_BUILD: _execute_site_build_step,
    STEP_SITE_DEPLOY: _execute_site_deploy_step,
}
_TRENDS_STEPS = {STEP_TRENDS_DAY, STEP_TRENDS_WEEK, STEP_TRENDS_MONTH}
_IDEAS_STEPS = {STEP_IDEAS_DAY, STEP_IDEAS_WEEK, STEP_IDEAS_MONTH}


def execute_step(
    invocation: WorkflowInvocation, *, context: WorkflowExecutionContext
) -> dict[str, Any]:
    handler = _STEP_EXECUTORS.get(invocation.step_id)
    if handler is not None:
        return handler(invocation, context)
    if invocation.step_id in _TRENDS_STEPS:
        return _execute_trends_step(invocation, context)
    if invocation.step_id in _IDEAS_STEPS:
        return _execute_ideas_step(invocation, context)
    raise ValueError(f"unsupported workflow step: {invocation.step_id}")
