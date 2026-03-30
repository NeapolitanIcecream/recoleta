from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import recoleta.cli as cli
from recoleta.cli.materialize import run_materialize_outputs_command
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


def _fleet_input_dirs(manifest_path: Path) -> tuple[Any, list[Path]]:
    manifest = load_fleet_manifest(manifest_path)
    return manifest, [child_site_input_dir(instance.config_path) for instance in manifest.instances]


def _fleet_default_language(manifest: Any, explicit: str | None) -> str | None:
    if explicit is not None and str(explicit).strip():
        return str(explicit).strip()
    for instance in manifest.instances:
        candidate = child_default_language_code(instance.config_path)
        if candidate:
            return candidate
    return None


def _fleet_site_output_dir(manifest_path: Path, output_dir: Path | None) -> Path:
    if output_dir is not None:
        return output_dir.expanduser().resolve()
    manifest = load_fleet_manifest(manifest_path)
    return manifest.manifest_path.parent / "site"


def run_fleet_site_build_command(
    *,
    manifest_path: Path,
    output_dir: Path | None,
    limit: int | None,
    default_language_code: str | None = None,
    json_output: bool = False,
    command_name: str = "fleet site build",
) -> dict[str, Any]:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    export_trend_static_site = cli._import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )

    manifest, input_dirs = _fleet_input_dirs(manifest_path)
    resolved_output_dir = _fleet_site_output_dir(manifest.manifest_path, output_dir)
    resolved_default_language_code = _fleet_default_language(
        manifest,
        default_language_code,
    )
    manifest_result_path = export_trend_static_site(
        input_dir=input_dirs,
        output_dir=resolved_output_dir,
        limit=limit,
        default_language_code=resolved_default_language_code,
    )
    site_manifest = json.loads(manifest_result_path.read_text(encoding="utf-8"))
    payload = {
        "status": "ok",
        "command": command_name,
        "manifest_path": str(manifest.manifest_path),
        "input_dir": [str(path) for path in input_dirs],
        "output_dir": str(resolved_output_dir),
        "site_manifest_path": str(manifest_result_path),
        "default_language_code": resolved_default_language_code,
        "manifest": site_manifest,
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console.print(
        f"[green]{command_name} completed[/green] "
        f"instances={len(manifest.instances)} "
        f"trends={site_manifest.get('trends_total', 0)} "
        f"output={resolved_output_dir}"
    )
    return payload


def run_fleet_site_serve_command(
    *,
    manifest_path: Path,
    output_dir: Path | None,
    limit: int | None,
    host: str,
    port: int,
    build: bool,
    default_language_code: str | None = None,
    command_name: str = "fleet site serve",
    build_command_name: str = "fleet site build",
) -> None:
    resolved_output_dir = _fleet_site_output_dir(manifest_path, output_dir)
    if build:
        run_fleet_site_build_command(
            manifest_path=manifest_path,
            output_dir=resolved_output_dir,
            limit=limit,
            default_language_code=default_language_code,
            json_output=False,
            command_name=build_command_name,
        )

    run_site_serve_command = cli._import_symbol(
        "recoleta.cli.site",
        attr_name="run_site_serve_command",
    )
    run_site_serve_command(
        input_dir=None,
        output_dir=resolved_output_dir,
        limit=limit,
        host=host,
        port=port,
        build=False,
        default_language_code=default_language_code,
        command_name=command_name,
        build_command_name=build_command_name,
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
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    manifest = load_fleet_manifest(manifest_path)
    children: list[dict[str, Any]] = []
    for instance in manifest.instances:
        child_payload = execute_granularity_workflow(
            workflow_name=workflow_name,
            command=f"{command} --instance {instance.name}",
            anchor_date=anchor_date,
            include=include,
            skip=skip,
            json_output=False,
            config_path=instance.config_path,
            emit_output=False,
        )
        child_payload["instance"] = instance.name
        child_payload["config_path"] = str(instance.config_path)
        children.append(child_payload)

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
    console.print(
        f"[green]{command} completed[/green] "
        f"instances={len(children)} workflow={workflow_name}"
    )
    return payload


def execute_fleet_deploy_workflow(
    *,
    manifest_path: Path,
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
    json_output: bool = False,
) -> dict[str, Any]:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    deploy_site = cli._import_symbol(
        "recoleta.site_deploy",
        attr_name="deploy_trend_static_site_to_github_pages",
    )
    include_steps = _parse_step_list(include)
    skip_steps = _parse_step_list(skip)
    _validate_step_overrides(
        workflow_name="deploy",
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    manifest = load_fleet_manifest(manifest_path)

    normalized_include = set(include_steps)
    normalized_skip = set(skip_steps)

    child_results: list[dict[str, Any]] = []
    for instance in manifest.instances:
        settings = load_child_settings(instance.config_path)
        translation_requested = (
            (
                STEP_TRANSLATE not in normalized_skip
                and (
                    STEP_TRANSLATE in normalized_include
                    or (
                        str(settings.workflows.deploy.translation or "").strip().lower() == "auto"
                        and bool(settings.localization_target_codes())
                    )
                )
            )
        )
        if translation_requested:
            run_translate_run_command(
                db_path=None,
                config_path=instance.config_path,
                scope="default",
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
            scope="default",
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

    input_dirs = [Path(child["site_input_dir"]) for child in child_results]
    deploy_result = deploy_site(
        input_dir=input_dirs,
        repo_dir=(repo_dir or Path.cwd()).expanduser().resolve(),
        remote=remote,
        branch=branch,
        commit_message=commit_message,
        cname=cname,
        pages_config_mode=pages_config,
        force=force,
        default_language_code=_fleet_default_language(manifest, None),
    )
    payload = {
        "status": "ok",
        "command": command,
        "manifest_path": str(manifest.manifest_path),
        "children": child_results,
        "deployment": {
            "remote": str(deploy_result.remote),
            "branch": str(deploy_result.branch),
            "remote_url": str(deploy_result.remote_url),
            "repo_root": str(deploy_result.repo_root),
            "commit_sha": deploy_result.commit_sha,
            "skipped": bool(deploy_result.skipped),
            "site_url": deploy_result.pages_source.site_url,
            "pages_source_status": str(deploy_result.pages_source.status),
        },
    }
    if json_output:
        cli._emit_json(payload)
        return payload
    console.print(
        f"[green]{command} completed[/green] "
        f"instances={len(child_results)} "
        f"branch={deploy_result.branch} "
        f"remote={deploy_result.remote}"
    )
    return payload
