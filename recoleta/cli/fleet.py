from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import recoleta.cli as cli
from recoleta.cli.arxiv_pool_readiness import (
    TERMINAL_ARXIV_POOL_BACKEND_REASONS,
    arxiv_pool_workflow_readiness_should_block,
    build_arxiv_pool_workflow_readiness_plan,
    evaluate_arxiv_pool_workflow_readiness,
)
from recoleta.cli.command_support import emit_command_error
from recoleta.cli.email import (
    _parse_anchor_or_exit,
    _preview_payload,
    _send_payload,
)
from recoleta.cli.materialize import run_materialize_outputs_command
from recoleta.cli.site_support import (
    FleetSitePayloadContext,
    fleet_default_language,
    fleet_input_dirs,
    load_manifest,
    fleet_site_output_dir,
    fleet_site_payload,
    fleet_site_segments,
    normalize_item_export_scope,
)
from recoleta.cli.translate import run_translate_run_command
from recoleta.cli.workflows import (
    STEP_INGEST,
    STEP_TRANSLATE,
    _parse_step_list,
    _validate_step_overrides,
    execute_granularity_workflow,
)
from recoleta.fleet import (
    _fleet_instance_slug,
    child_default_language_code,
    child_site_input_dir,
    load_child_settings,
    load_fleet_manifest,
)
from recoleta.arxiv_pool import (
    ArxivPoolBackendDescriptor,
    ArxivPoolReadinessPolicy,
    ArxivPoolStore,
    ArxivPoolSync,
    ArxivPoolSyncResult,
    ArxivPoolWindow,
    arxiv_pool_backend_descriptor_from_settings,
    arxiv_pool_readiness_policy_from_settings,
    arxiv_pool_sync_result_from_huldra,
    build_huldra_arxiv_request_for_window,
    build_arxiv_pool_windows_for_period,
    huldra_wait_timeout_seconds,
    resolve_arxiv_pool_db_path,
)
from recoleta.storage import Repository
from recoleta.cli.workflow_runner import (
    GranularityPlanRequest,
    build_granularity_plan,
    normalize_anchor_date,
    period_bounds_for_granularity,
)
from recoleta.trend_email import (
    TrendEmailSendRequest,
    build_trend_email_preview,
    send_trend_email,
)

_READINESS_GATE_RANK = {"off": 0, "warn": 1, "strict": 2}


@dataclass(frozen=True, slots=True)
class FleetDeployRequest:
    manifest_path: Path
    command: str
    include_steps: list[str]
    skip_steps: list[str]
    repo_dir: Path | None
    remote: str
    branch: str
    commit_message: str | None
    cname: str | None
    pages_config: str
    force: bool
    item_export_scope: str
    json_output: bool


@dataclass(frozen=True, slots=True)
class FleetGranularityChildRequest:
    instance: Any
    workflow_name: str
    command: str
    anchor_date: str | None
    include: str | None
    skip: str | None


@dataclass(frozen=True, slots=True)
class FleetSiteServeRequest:
    manifest_path: Path
    output_dir: Path | None
    limit: int | None
    host: str
    port: int
    build: bool
    default_language_code: str | None
    item_export_scope: str
    command_name: str
    build_command_name: str


@dataclass(frozen=True, slots=True)
class FleetSiteDeployContext:
    manifest: Any
    child_results: list[dict[str, Any]]
    repo_dir: Path | None
    remote: str
    branch: str
    commit_message: str | None
    cname: str | None
    pages_config: str
    force: bool
    item_export_scope: str


@dataclass(frozen=True, slots=True)
class FleetArxivPoolPreSyncPlan:
    status: str
    reason: str | None
    pool_db_path: Path | None
    windows: list[ArxivPoolWindow]
    backend_descriptor: ArxivPoolBackendDescriptor | None = None
    request_interval_seconds: float = 5.0
    cooldown_seconds: int = 3600
    huldra_request_timeout_seconds: float = 30.0
    huldra_wait_timeout_seconds: float | None = None
    maturity_lag_days: int = 1
    readiness_gate: str = "strict"
    allow_immature_windows: bool = False

    def as_payload(self) -> dict[str, Any]:
        backend = self.backend_descriptor.kind if self.backend_descriptor else None
        return {
            "status": self.status,
            "reason": self.reason,
            "backend": backend,
            "huldra_base_url": (
                self.backend_descriptor.identity
                if self.backend_descriptor is not None
                and self.backend_descriptor.kind == "huldra"
                else None
            ),
            "pool_db_path": str(self.pool_db_path) if self.pool_db_path else None,
            "windows_total": len(self.windows),
            "request_interval_seconds": self.request_interval_seconds,
            "cooldown_seconds": self.cooldown_seconds,
            "huldra_request_timeout_seconds": self.huldra_request_timeout_seconds,
            "huldra_wait_timeout_seconds": self.huldra_wait_timeout_seconds,
            "maturity_lag_days": self.maturity_lag_days,
            "readiness_gate": self.readiness_gate,
            "allow_immature_windows": self.allow_immature_windows,
        }


@dataclass(frozen=True, slots=True)
class FleetGranularityReadinessContext:
    manifest: Any
    requested_steps: list[str]
    readiness_plan: Any
    arxiv_pool_pre_sync: dict[str, Any]
    arxiv_pool_readiness: dict[str, Any] | None


def _fleet_input_dirs(manifest_path: Path) -> tuple[Any, list[Any]]:
    trend_site_input_spec_cls = cli._import_symbol(
        "recoleta.site",
        attr_name="TrendSiteInputSpec",
    )
    return fleet_input_dirs(
        manifest_path=manifest_path,
        trend_site_input_spec_cls=trend_site_input_spec_cls,
        load_fleet_manifest=load_fleet_manifest,
        child_site_input_dir=child_site_input_dir,
    )


def _fleet_default_language(manifest: Any, explicit: str | None) -> str | None:
    return fleet_default_language(
        manifest=manifest,
        explicit=explicit,
        child_default_language_code=child_default_language_code,
    )


def _fleet_site_output_dir(manifest_path: Path, output_dir: Path | None) -> Path:
    return fleet_site_output_dir(
        manifest_path=manifest_path,
        output_dir=output_dir,
        load_fleet_manifest=load_fleet_manifest,
    )


def _resolve_fleet_instance(*, manifest: Any, value: str) -> Any:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError("--instance is required")
    normalized_slug = _fleet_instance_slug(normalized)
    for instance in manifest.instances:
        if instance.name == normalized or _fleet_instance_slug(instance.name) == normalized_slug:
            return instance
    raise ValueError(f"unknown fleet instance: {normalized}")


def run_fleet_site_build_command(**kwargs: Any) -> dict[str, Any]:
    command_name = str(kwargs.get("command_name", "fleet site build"))
    manifest_path = Path(kwargs["manifest_path"])
    manifest, input_dirs = _fleet_input_dirs(manifest_path)
    resolved_output_dir = _fleet_site_output_dir(
        manifest.manifest_path, kwargs.get("output_dir")
    )
    resolved_default_language_code = _fleet_default_language(
        manifest,
        kwargs.get("default_language_code"),
    )
    normalized_item_export_scope = normalize_item_export_scope(
        str(kwargs.get("item_export_scope", "linked"))
    )
    export_trend_static_site = cli._import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )
    export_kwargs: dict[str, Any] = {
        "input_dir": input_dirs,
        "output_dir": resolved_output_dir,
        "limit": kwargs.get("limit"),
        "default_language_code": resolved_default_language_code,
    }
    if normalized_item_export_scope != "linked":
        export_kwargs["item_export_scope"] = normalized_item_export_scope
    manifest_result_path = export_trend_static_site(**export_kwargs)
    payload = fleet_site_payload(
        context=FleetSitePayloadContext(
            command_name=command_name,
            manifest=manifest,
            input_dirs=input_dirs,
            output_dir=resolved_output_dir,
            manifest_result_path=manifest_result_path,
            default_language_code=resolved_default_language_code,
            item_export_scope=normalized_item_export_scope,
            site_manifest=load_manifest(manifest_result_path),
        )
    )
    if bool(kwargs.get("json_output", False)):
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{command_name} completed[/green] "
        + " ".join(
            fleet_site_segments(
                manifest=manifest,
                site_manifest=payload["manifest"],
                output_dir=resolved_output_dir,
            )
        )
    )
    return payload


def run_fleet_site_serve_command(**kwargs: Any) -> None:
    request = FleetSiteServeRequest(
        manifest_path=Path(kwargs["manifest_path"]),
        output_dir=kwargs.get("output_dir"),
        limit=kwargs.get("limit"),
        host=str(kwargs["host"]),
        port=int(kwargs["port"]),
        build=bool(kwargs["build"]),
        default_language_code=kwargs.get("default_language_code"),
        item_export_scope=str(kwargs.get("item_export_scope", "linked")),
        command_name=str(kwargs.get("command_name", "fleet site serve")),
        build_command_name=str(kwargs.get("build_command_name", "fleet site build")),
    )
    resolved_output_dir = _fleet_site_output_dir(
        request.manifest_path, request.output_dir
    )
    if request.build:
        run_fleet_site_build_command(
            manifest_path=request.manifest_path,
            output_dir=resolved_output_dir,
            limit=request.limit,
            default_language_code=request.default_language_code,
            item_export_scope=request.item_export_scope,
            json_output=False,
            command_name=request.build_command_name,
        )
    run_site_serve_command = cli._import_symbol(
        "recoleta.cli.site",
        attr_name="run_site_serve_command",
    )
    run_site_serve_command(
        input_dir=None,
        output_dir=resolved_output_dir,
        limit=request.limit,
        host=request.host,
        port=request.port,
        build=False,
        default_language_code=request.default_language_code,
        item_export_scope=request.item_export_scope,
        command_name=request.command_name,
        build_command_name=request.build_command_name,
    )


def run_fleet_email_preview_command(**kwargs: Any) -> dict[str, Any]:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "fleet run email preview"))
    console = cli._runtime_symbols()["Console"]()
    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=kwargs.get("anchor_date"),
        command_name=command_name,
        console=console,
        json_output=json_output,
    )
    try:
        manifest = load_fleet_manifest(Path(kwargs["manifest_path"]))
        resolved_instance = _resolve_fleet_instance(
            manifest=manifest,
            value=str(kwargs.get("instance") or ""),
        )
        settings = load_child_settings(resolved_instance.config_path)
        result = build_trend_email_preview(
            settings=settings,
            site_output_dir=_fleet_site_output_dir(
                manifest.manifest_path,
                kwargs.get("site_output_dir"),
            ),
            anchor_date=parsed_anchor,
            output_dir=kwargs.get("output_dir"),
            granularities=kwargs.get("granularities"),
        )
    except Exception as exc:  # noqa: BLE001
        emit_command_error(
            command_name=command_name,
            message=str(exc),
            console=console,
            json_output=json_output,
            exit_code=1,
        )
    payload = _preview_payload(
        command_name=command_name,
        result=result,
        instance_name=resolved_instance.name,
    )
    if json_output:
        cli._emit_json(payload)
        return payload
    console.print(
        f"[green]{command_name} completed[/green] "
        f"instance={resolved_instance.name} bundles={len(result.results)} "
        f"output={result.preview_root_dir}"
    )
    return payload


def run_fleet_email_send_command(**kwargs: Any) -> dict[str, Any]:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "fleet run email send"))
    console = cli._runtime_symbols()["Console"]()
    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=kwargs.get("anchor_date"),
        command_name=command_name,
        console=console,
        json_output=json_output,
    )
    try:
        manifest = load_fleet_manifest(Path(kwargs["manifest_path"]))
        resolved_instance = _resolve_fleet_instance(
            manifest=manifest,
            value=str(kwargs.get("instance") or ""),
        )
        settings = load_child_settings(resolved_instance.config_path)
        repository = Repository(db_path=Path(settings.recoleta_db_path))
        repository.init_schema()
        result = send_trend_email(
            settings=settings,
            repository=repository,
            request=TrendEmailSendRequest(
                site_output_dir=_fleet_site_output_dir(
                    manifest.manifest_path,
                    kwargs.get("site_output_dir"),
                ),
                anchor_date=parsed_anchor,
                force_batch=bool(kwargs.get("force_batch", False)),
                granularities=kwargs.get("granularities"),
            ),
        )
    except Exception as exc:  # noqa: BLE001
        emit_command_error(
            command_name=command_name,
            message=str(exc),
            console=console,
            json_output=json_output,
            exit_code=1,
        )
    payload = _send_payload(
        command_name=command_name,
        result=result,
        instance_name=resolved_instance.name,
    )
    if json_output:
        cli._emit_json(payload)
        if result.status in {"preflight_failed", "send_failed"}:
            raise cli.typer.Exit(code=1)
        return payload
    all_skipped = bool(result.results) and all(
        entry.status == "skipped" for entry in result.results
    )
    color = (
        "red"
        if result.status in {"preflight_failed", "send_failed"}
        else ("yellow" if all_skipped else "green")
    )
    console.print(
        f"[{color}]{command_name} {result.status}[/{color}] "
        f"instance={resolved_instance.name} bundles={len(result.results)} "
        f"output={result.send_root_dir}"
    )
    if result.status in {"preflight_failed", "send_failed"}:
        raise cli.typer.Exit(code=1)
    return payload


def execute_fleet_granularity_workflow(
    *,
    manifest_path: Path,
    workflow_name: str,
    command: str,
    anchor_date: str | None = None,
    include: str | None = None,
    skip: str | None = None,
    json_output: bool = False,
) -> dict[str, Any]:
    include_steps = _parse_step_list(include)
    skip_steps = _parse_step_list(skip)
    _validate_step_overrides(
        workflow_name=workflow_name,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    context = _fleet_granularity_readiness_context(
        manifest_path=manifest_path,
        workflow_name=workflow_name,
        command=command,
        anchor_date=anchor_date,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    if _fleet_granularity_readiness_should_block(context):
        payload = _fleet_granularity_blocked_payload(
            context=context,
            command=command,
            workflow_name=workflow_name,
        )
        _emit_fleet_granularity_blocked(
            payload=payload,
            command=command,
            json_output=json_output,
        )
        raise cli.typer.Exit(code=1)

    children = _fleet_granularity_child_payloads(
        manifest=context.manifest,
        workflow_name=workflow_name,
        command=command,
        anchor_date=anchor_date,
        include=include,
        skip=skip,
    )
    payload = {
        "status": "ok",
        "command": command,
        "manifest_path": str(context.manifest.manifest_path),
        "workflow_name": workflow_name,
        "arxiv_pool_pre_sync": context.arxiv_pool_pre_sync,
        "arxiv_pool_readiness": context.arxiv_pool_readiness,
        "children": children,
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{command} completed[/green] "
        f"instances={len(children)} workflow={workflow_name}"
    )
    return payload


def _fleet_granularity_readiness_context(
    *,
    manifest_path: Path,
    workflow_name: str,
    command: str,
    anchor_date: str | None,
    include_steps: list[str],
    skip_steps: list[str],
) -> FleetGranularityReadinessContext:
    manifest = load_fleet_manifest(manifest_path)
    child_settings = [
        load_child_settings(instance.config_path) for instance in manifest.instances
    ]
    target_period_start, target_period_end = _fleet_granularity_target_period(
        workflow_name=workflow_name,
        anchor_date=anchor_date,
    )
    requested_steps = _fleet_granularity_requested_steps(
        settings_list=child_settings,
        workflow_name=workflow_name,
        command=command,
        anchor_date=anchor_date,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    readiness_plan = build_arxiv_pool_workflow_readiness_plan(
        settings_list=child_settings,
        target_period_start=target_period_start,
        target_period_end=target_period_end,
        requested_steps=requested_steps,
    )
    pre_sync_plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest.manifest_path,
        workflow_name=workflow_name,
        anchor_date=anchor_date,
        manifest=manifest,
        skip_steps=skip_steps,
    )
    pre_sync_payload, readiness_payload = _fleet_arxiv_pool_pre_sync_payload(
        pre_sync_plan=pre_sync_plan,
        readiness_plan=readiness_plan,
    )
    return FleetGranularityReadinessContext(
        manifest=manifest,
        requested_steps=requested_steps,
        readiness_plan=readiness_plan,
        arxiv_pool_pre_sync=pre_sync_payload,
        arxiv_pool_readiness=readiness_payload,
    )


def _fleet_arxiv_pool_pre_sync_payload(
    *,
    pre_sync_plan: FleetArxivPoolPreSyncPlan,
    readiness_plan: Any,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    pre_sync_payload: dict[str, Any] = pre_sync_plan.as_payload()
    if pre_sync_plan.status == "planned":
        sync_result = run_fleet_arxiv_pool_pre_sync(pre_sync_plan)
        pre_sync_payload = {
            **pre_sync_payload,
            "status": "completed",
            "sync": sync_result.as_payload(),
        }
        if readiness_plan.status == "planned":
            readiness_payload = evaluate_arxiv_pool_workflow_readiness(readiness_plan)
            pre_sync_payload["readiness"] = readiness_payload
            return pre_sync_payload, readiness_payload
    if readiness_plan.status == "planned":
        return pre_sync_payload, evaluate_arxiv_pool_workflow_readiness(readiness_plan)
    if readiness_plan.status == "blocked":
        return pre_sync_payload, evaluate_arxiv_pool_workflow_readiness(readiness_plan)
    return pre_sync_payload, None


def _fleet_granularity_readiness_should_block(
    context: FleetGranularityReadinessContext,
) -> bool:
    if context.arxiv_pool_pre_sync.get("status") == "blocked":
        return True
    if context.arxiv_pool_readiness is None:
        return False
    return arxiv_pool_workflow_readiness_should_block(
        context.readiness_plan,
        context.arxiv_pool_readiness,
    )


def _fleet_granularity_blocked_payload(
    *,
    context: FleetGranularityReadinessContext,
    command: str,
    workflow_name: str,
) -> dict[str, Any]:
    return {
        "status": "blocked",
        "command": command,
        "manifest_path": str(context.manifest.manifest_path),
        "workflow_name": workflow_name,
        "requested_steps": context.requested_steps,
        "arxiv_pool_pre_sync": context.arxiv_pool_pre_sync,
        "arxiv_pool_readiness": context.arxiv_pool_readiness,
        "children": [],
    }


def _emit_fleet_granularity_blocked(
    *,
    payload: dict[str, Any],
    command: str,
    json_output: bool,
) -> None:
    if json_output:
        cli._emit_json(payload)
        return
    readiness = payload["arxiv_pool_readiness"]
    console = cli._runtime_symbols()["Console"]()
    if readiness is None:
        pre_sync = payload["arxiv_pool_pre_sync"]
        console.print(
            f"[yellow]{command} blocked[/yellow] "
            f"reason={pre_sync.get('reason')}"
        )
        return
    console.print(
        f"[yellow]{command} blocked[/yellow] "
        f"arxiv_pool_windows={readiness['blocked_windows_total']}"
    )


def _fleet_granularity_child_payloads(
    *,
    manifest: Any,
    workflow_name: str,
    command: str,
    anchor_date: str | None,
    include: str | None,
    skip: str | None,
) -> list[dict[str, Any]]:
    return [
        _fleet_granularity_child_payload(
            request=FleetGranularityChildRequest(
                instance=instance,
                workflow_name=workflow_name,
                command=command,
                anchor_date=anchor_date,
                include=include,
                skip=skip,
            )
        )
        for instance in manifest.instances
    ]


def _fleet_granularity_target_period(
    *, workflow_name: str, anchor_date: str | None
) -> tuple[Any, Any]:
    normalized_workflow = _fleet_arxiv_pool_workflow_name(workflow_name) or workflow_name
    anchor = normalize_anchor_date(anchor_date, workflow_name=normalized_workflow)
    return period_bounds_for_granularity(
        granularity=normalized_workflow,
        anchor=anchor,
    )


def _fleet_granularity_requested_steps(
    *,
    settings_list: list[Any],
    workflow_name: str,
    command: str,
    anchor_date: str | None,
    include_steps: list[str],
    skip_steps: list[str],
) -> list[str]:
    requested_steps: list[str] = []
    for settings in settings_list:
        plan = build_granularity_plan(
            request=GranularityPlanRequest(
                workflow_name=workflow_name,
                command=command,
                anchor_date=anchor_date,
                settings=settings,
                include_steps=include_steps,
                skip_steps=skip_steps,
            )
        )
        for step_id in plan.requested_steps:
            if step_id not in requested_steps:
                requested_steps.append(step_id)
    return requested_steps


def build_fleet_arxiv_pool_pre_sync_plan(
    *,
    manifest_path: Path,
    workflow_name: str,
    anchor_date: str | None,
    manifest: Any | None = None,
    skip_steps: list[str] | None = None,
) -> FleetArxivPoolPreSyncPlan:
    normalized_workflow = _fleet_arxiv_pool_workflow_name(workflow_name)
    if normalized_workflow is None:
        return _skipped_fleet_arxiv_pool_pre_sync_plan("unsupported_workflow")
    if STEP_INGEST in set(skip_steps or []):
        return _skipped_fleet_arxiv_pool_pre_sync_plan("ingest_not_requested")
    resolved_manifest = manifest or load_fleet_manifest(manifest_path)
    arxiv_settings = _fleet_arxiv_pool_source_settings(resolved_manifest)
    skip_reason = _fleet_arxiv_pool_settings_skip_reason(arxiv_settings)
    if skip_reason is not None:
        return _skipped_fleet_arxiv_pool_pre_sync_plan(skip_reason)
    backend_descriptor, backend_skip_reason = _shared_fleet_arxiv_pool_backend_descriptor(
        arxiv_settings
    )
    if backend_descriptor is None:
        reason = backend_skip_reason or "multiple_pool_db_paths"
        if reason in TERMINAL_ARXIV_POOL_BACKEND_REASONS:
            return _blocked_fleet_arxiv_pool_pre_sync_plan(reason)
        return _skipped_fleet_arxiv_pool_pre_sync_plan(reason)
    windows = _fleet_arxiv_pool_windows(
        arxiv_settings=arxiv_settings,
        workflow_name=normalized_workflow,
        anchor_date=anchor_date,
    )
    (
        request_interval_seconds,
        cooldown_seconds,
        readiness_policy,
    ) = _merged_fleet_arxiv_pool_plan_settings(arxiv_settings)
    return FleetArxivPoolPreSyncPlan(
        status="planned",
        reason=None,
        pool_db_path=(
            Path(backend_descriptor.identity)
            if backend_descriptor.kind == "local_sqlite"
            else None
        ),
        windows=windows,
        backend_descriptor=backend_descriptor,
        request_interval_seconds=request_interval_seconds,
        cooldown_seconds=cooldown_seconds,
        huldra_request_timeout_seconds=max(
            float(settings.arxiv_pool.huldra_request_timeout_seconds)
            for settings in arxiv_settings
        ),
        huldra_wait_timeout_seconds=_merged_huldra_wait_timeout(arxiv_settings),
        maturity_lag_days=readiness_policy.maturity_lag_days,
        readiness_gate=readiness_policy.readiness_gate,
        allow_immature_windows=readiness_policy.allow_immature_windows,
    )


def _fleet_arxiv_pool_workflow_name(workflow_name: str) -> str | None:
    normalized_workflow = str(workflow_name or "").strip().lower()
    if normalized_workflow == "now":
        normalized_workflow = "day"
    if normalized_workflow in {"day", "week", "month"}:
        return normalized_workflow
    return None


def _skipped_fleet_arxiv_pool_pre_sync_plan(
    reason: str,
) -> FleetArxivPoolPreSyncPlan:
    return FleetArxivPoolPreSyncPlan(
        status="skipped",
        reason=reason,
        pool_db_path=None,
        windows=[],
    )


def _blocked_fleet_arxiv_pool_pre_sync_plan(
    reason: str,
) -> FleetArxivPoolPreSyncPlan:
    return FleetArxivPoolPreSyncPlan(
        status="blocked",
        reason=reason,
        pool_db_path=None,
        windows=[],
    )


def _fleet_arxiv_pool_source_settings(manifest: Any) -> list[Any]:
    child_settings = [
        load_child_settings(instance.config_path) for instance in manifest.instances
    ]
    return [
        settings
        for settings in child_settings
        if bool(getattr(settings.sources.arxiv, "enabled", False))
    ]


def _fleet_arxiv_pool_settings_skip_reason(arxiv_settings: list[Any]) -> str | None:
    if not arxiv_settings:
        return "no_arxiv_sources"
    if any(str(settings.sources.arxiv.mode) != "pool" for settings in arxiv_settings):
        return "direct_arxiv_source_present"
    return None


def _shared_fleet_arxiv_pool_db_path(arxiv_settings: list[Any]) -> Path | None:
    pool_paths = {resolve_arxiv_pool_db_path(settings) for settings in arxiv_settings}
    if len(pool_paths) != 1:
        return None
    return next(iter(pool_paths))


def _shared_fleet_arxiv_pool_backend_descriptor(
    arxiv_settings: list[Any],
) -> tuple[ArxivPoolBackendDescriptor | None, str | None]:
    descriptors = [
        arxiv_pool_backend_descriptor_from_settings(settings)
        for settings in arxiv_settings
    ]
    kinds = {descriptor.kind for descriptor in descriptors}
    if len(kinds) > 1:
        return None, "mixed_arxiv_pool_backends"
    identities = {descriptor.identity for descriptor in descriptors}
    if len(identities) != 1:
        kind = next(iter(kinds))
        if kind == "huldra":
            return None, "multiple_huldra_endpoints"
        return None, "multiple_pool_db_paths"
    return descriptors[0], None


def _merged_huldra_wait_timeout(arxiv_settings: list[Any]) -> float | None:
    values = [
        getattr(settings.arxiv_pool, "huldra_wait_timeout_seconds", None)
        for settings in arxiv_settings
    ]
    numeric_values = [float(value) for value in values if value is not None]
    return max(numeric_values) if numeric_values else None


def _merged_fleet_arxiv_pool_plan_settings(
    arxiv_settings: list[Any],
) -> tuple[float, int, ArxivPoolReadinessPolicy]:
    pool_settings = [settings.arxiv_pool for settings in arxiv_settings]
    readiness_policies = [
        arxiv_pool_readiness_policy_from_settings(settings)
        for settings in arxiv_settings
    ]
    readiness_gate = max(
        (policy.readiness_gate for policy in readiness_policies),
        key=lambda gate: _READINESS_GATE_RANK[gate],
    )
    return (
        max(float(pool.request_interval_seconds) for pool in pool_settings),
        max(int(pool.cooldown_seconds) for pool in pool_settings),
        ArxivPoolReadinessPolicy(
            maturity_lag_days=max(
                policy.maturity_lag_days for policy in readiness_policies
            ),
            readiness_gate=readiness_gate,
            allow_immature_windows=all(
                policy.allow_immature_windows for policy in readiness_policies
            ),
        ),
    )


def _fleet_arxiv_pool_windows(
    *,
    arxiv_settings: list[Any],
    workflow_name: str,
    anchor_date: str | None,
) -> list[ArxivPoolWindow]:
    anchor = normalize_anchor_date(anchor_date, workflow_name=workflow_name)
    period_start, period_end = period_bounds_for_granularity(
        granularity=workflow_name,
        anchor=anchor,
    )
    windows_by_key: dict[tuple[str, str, str, int], ArxivPoolWindow] = {}
    for settings in arxiv_settings:
        for window in build_arxiv_pool_windows_for_period(
            queries=list(settings.sources.arxiv.queries),
            period_start=period_start,
            period_end=period_end,
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


def run_fleet_arxiv_pool_pre_sync(
    plan: FleetArxivPoolPreSyncPlan,
) -> ArxivPoolSyncResult:
    if (
        plan.backend_descriptor is not None
        and plan.backend_descriptor.kind == "huldra"
    ):
        from huldra.client import HuldraClient

        readiness_policy = ArxivPoolReadinessPolicy(
            maturity_lag_days=plan.maturity_lag_days,
            readiness_gate=plan.readiness_gate,
            allow_immature_windows=plan.allow_immature_windows,
        )
        requests = [
            build_huldra_arxiv_request_for_window(
                window=window,
                readiness_policy=readiness_policy,
                client_id="recoleta:fleet",
                timeout_seconds=plan.huldra_request_timeout_seconds,
            )
            for window in plan.windows
        ]
        wait_timeout = huldra_wait_timeout_seconds(
            configured_timeout_seconds=plan.huldra_wait_timeout_seconds,
            requested_windows_total=len(requests),
        )
        with HuldraClient(
            base_url=plan.backend_descriptor.identity,
            timeout=plan.huldra_request_timeout_seconds,
        ) as client:
            result = client.sync_windows(
                requests,
                wait=True,
                wait_timeout_seconds=wait_timeout,
            )
        return arxiv_pool_sync_result_from_huldra(result)
    if plan.pool_db_path is None:
        return ArxivPoolSyncResult(requested_windows_total=0)
    return ArxivPoolSync(
        store=ArxivPoolStore(plan.pool_db_path),
        request_interval_seconds=plan.request_interval_seconds,
        cooldown_seconds=plan.cooldown_seconds,
    ).sync_windows(plan.windows)


def execute_fleet_deploy_workflow(**kwargs: Any) -> dict[str, Any]:
    include_steps = _parse_step_list(kwargs.get("include"))
    skip_steps = _parse_step_list(kwargs.get("skip"))
    _validate_step_overrides(
        workflow_name="deploy",
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    request = FleetDeployRequest(
        manifest_path=Path(kwargs["manifest_path"]),
        command=str(kwargs["command"]),
        include_steps=include_steps,
        skip_steps=skip_steps,
        repo_dir=kwargs.get("repo_dir"),
        remote=str(kwargs.get("remote", "origin")),
        branch=str(kwargs.get("branch", "gh-pages")),
        commit_message=kwargs.get("commit_message"),
        cname=kwargs.get("cname"),
        pages_config=str(kwargs.get("pages_config", "auto")),
        force=bool(kwargs.get("force", True)),
        item_export_scope=str(kwargs.get("item_export_scope", "linked")),
        json_output=bool(kwargs.get("json_output", False)),
    )
    manifest = load_fleet_manifest(request.manifest_path)
    child_results = _run_fleet_deploy_children(
        manifest=manifest,
        command=request.command,
        include_steps=request.include_steps,
        skip_steps=request.skip_steps,
    )
    payload = {
        "status": "ok",
        "command": request.command,
        "manifest_path": str(manifest.manifest_path),
        "children": child_results,
        "deployment": _deploy_fleet_site(
            context=FleetSiteDeployContext(
                manifest=manifest,
                child_results=child_results,
                repo_dir=request.repo_dir,
                remote=request.remote,
                branch=request.branch,
                commit_message=request.commit_message,
                cname=request.cname,
                pages_config=request.pages_config,
                force=request.force,
                item_export_scope=request.item_export_scope,
            )
        ),
    }
    if request.json_output:
        cli._emit_json(payload)
        return payload
    console = cli._runtime_symbols()["Console"]()
    console.print(
        f"[green]{request.command} completed[/green] "
        f"instances={len(child_results)} "
        f"branch={payload['deployment']['branch']} "
        f"remote={payload['deployment']['remote']}"
    )
    return payload


def _fleet_granularity_child_payload(
    *, request: FleetGranularityChildRequest
) -> dict[str, Any]:
    child_payload = execute_granularity_workflow(
        workflow_name=request.workflow_name,
        command=f"{request.command} --instance {request.instance.name}",
        anchor_date=request.anchor_date,
        include=request.include,
        skip=request.skip,
        json_output=False,
        config_path=request.instance.config_path,
        emit_output=False,
    )
    child_payload["instance"] = request.instance.name
    child_payload["config_path"] = str(request.instance.config_path)
    return child_payload


def _run_fleet_deploy_children(
    *,
    manifest: Any,
    command: str,
    include_steps: list[str],
    skip_steps: list[str],
) -> list[dict[str, Any]]:
    child_results: list[dict[str, Any]] = []
    normalized_include = set(include_steps)
    normalized_skip = set(skip_steps)
    for instance in manifest.instances:
        settings = load_child_settings(instance.config_path)
        translation_requested = _translation_requested(
            settings=settings,
            normalized_include=normalized_include,
            normalized_skip=normalized_skip,
        )
        if translation_requested:
            run_translate_run_command(
                db_path=None,
                config_path=instance.config_path,
                granularity=None,
                include=",".join(list(settings.workflows.deploy.translate_include)),
                limit=None,
                force=False,
                context_assist="direct",
                json_output=False,
                command_name=f"{command} translate --instance {instance.name}",
                raise_on_abort=True,
            )
        run_materialize_outputs_command(
            db_path=None,
            config_path=instance.config_path,
            output_dir=None,
            granularity=None,
            pdf=False,
            site=False,
            debug_pdf=False,
            json_output=False,
            command_name=f"{command} materialize --instance {instance.name}",
        )
        child_results.append(
            {
                "instance": instance.name,
                "config_path": str(instance.config_path),
                "translation_requested": translation_requested,
                "site_input_dir": str(child_site_input_dir(instance.config_path)),
            }
        )
    return child_results


def _translation_requested(
    *,
    settings: Any,
    normalized_include: set[str],
    normalized_skip: set[str],
) -> bool:
    if STEP_TRANSLATE in normalized_skip:
        return False
    if STEP_TRANSLATE in normalized_include:
        return True
    return str(
        settings.workflows.deploy.translation or ""
    ).strip().lower() == "auto" and bool(settings.localization_target_codes())


def _deploy_fleet_site(*, context: FleetSiteDeployContext) -> dict[str, Any]:
    trend_site_input_spec_cls = cli._import_symbol(
        "recoleta.site",
        attr_name="TrendSiteInputSpec",
    )
    input_dirs = [
        trend_site_input_spec_cls(
            path=Path(str(child["site_input_dir"])),
            instance=str(child["instance"]),
        )
        for child in context.child_results
    ]
    deploy_site = cli._import_symbol(
        "recoleta.site_deploy",
        attr_name="deploy_trend_static_site_to_github_pages",
    )
    deploy_kwargs: dict[str, Any] = {
        "input_dir": input_dirs,
        "repo_dir": (context.repo_dir or Path.cwd()).expanduser().resolve(),
        "remote": context.remote,
        "branch": context.branch,
        "commit_message": context.commit_message,
        "cname": context.cname,
        "pages_config_mode": context.pages_config,
        "force": context.force,
        "default_language_code": _fleet_default_language(context.manifest, None),
    }
    normalized_item_export_scope = normalize_item_export_scope(
        context.item_export_scope
    )
    if normalized_item_export_scope != "linked":
        deploy_kwargs["item_export_scope"] = normalized_item_export_scope
    deploy_result = deploy_site(**deploy_kwargs)
    return {
        "remote": str(deploy_result.remote),
        "branch": str(deploy_result.branch),
        "remote_url": str(deploy_result.remote_url),
        "repo_root": str(deploy_result.repo_root),
        "commit_sha": deploy_result.commit_sha,
        "skipped": bool(deploy_result.skipped),
        "site_url": deploy_result.pages_source.site_url,
        "pages_source_status": str(deploy_result.pages_source.status),
    }
