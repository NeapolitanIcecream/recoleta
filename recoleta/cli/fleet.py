from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import recoleta.cli as cli
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
    STEP_TRANSLATE,
    _parse_step_list,
    _validate_step_overrides,
    execute_granularity_workflow,
)
from recoleta.fleet import (
    child_default_language_code,
    child_site_input_dir,
    load_child_settings,
    load_fleet_manifest,
)


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
    manifest = load_fleet_manifest(manifest_path)
    children = [
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
    payload = {
        "status": "ok",
        "command": command,
        "manifest_path": str(manifest.manifest_path),
        "workflow_name": workflow_name,
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
