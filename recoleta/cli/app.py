from __future__ import annotations

from click import Context
import json
from pathlib import Path
from typing import Any

from recoleta.app.runtime import typer
from recoleta.cli.analyze import run_analyze_command
from recoleta.cli.db import (
    run_db_cleanup_instance_first_schema_command,
    run_db_clear_command,
    run_db_reset_command,
)
from recoleta.cli.ideas import run_ideas_command
from recoleta.cli.ingest import run_ingest_command
from recoleta.cli.materialize import run_materialize_outputs_command
from recoleta.cli.maintenance import (
    run_backup_command,
    run_doctor_command,
    run_doctor_llm_command,
    run_doctor_why_empty_command,
    run_gc_command,
    run_restore_command,
    run_stats_command,
    run_vacuum_command,
)
from recoleta.cli.publish import run_publish_command
from recoleta.cli.rag import (
    run_rag_build_index_command,
    run_rag_sync_vectors_command,
)
from recoleta.cli.runs import run_runs_list_command, run_runs_show_command
from recoleta.cli.site import (
    run_site_build_command,
    run_site_serve_command,
    run_site_stage_command,
)
from recoleta.cli.translate import (
    run_translate_backfill_command,
    run_translate_run_command,
)
from recoleta.cli.trends import run_trends_command
from recoleta.cli.workflows import (
    execute_deploy_workflow,
    execute_granularity_workflow,
    run_daemon_start_command,
)


def execute_fleet_granularity_workflow(**kwargs: Any) -> Any:
    from recoleta.cli.fleet import execute_fleet_granularity_workflow as impl

    return impl(**kwargs)


def execute_fleet_deploy_workflow(**kwargs: Any) -> Any:
    from recoleta.cli.fleet import execute_fleet_deploy_workflow as impl

    return impl(**kwargs)


def run_fleet_site_build_command(**kwargs: Any) -> Any:
    from recoleta.cli.fleet import run_fleet_site_build_command as impl

    return impl(**kwargs)


def run_fleet_site_serve_command(**kwargs: Any) -> Any:
    from recoleta.cli.fleet import run_fleet_site_serve_command as impl

    return impl(**kwargs)

app = typer.Typer(
    help="Recoleta workflow-first CLI.", no_args_is_help=True
)

run_app = typer.Typer(help="Workflow entrypoints.", no_args_is_help=True)
run_site_app = typer.Typer(help="Common site workflows.", no_args_is_help=True)
run_app.add_typer(run_site_app, name="site")
app.add_typer(run_app, name="run")

fleet_app = typer.Typer(help="Fleet orchestration workflows.", no_args_is_help=True)
fleet_run_app = typer.Typer(help="Fleet workflow entrypoints.", no_args_is_help=True)
fleet_site_app = typer.Typer(help="Fleet site workflows.", no_args_is_help=True)
fleet_app.add_typer(fleet_run_app, name="run")
fleet_app.add_typer(fleet_site_app, name="site")
app.add_typer(fleet_app, name="fleet")

daemon_app = typer.Typer(help="Background workflow scheduling.", no_args_is_help=True)
app.add_typer(daemon_app, name="daemon")

inspect_app = typer.Typer(help="Read-only inspection workflows.", no_args_is_help=True)
inspect_runs_app = typer.Typer(help="Run history inspection.", no_args_is_help=True)
inspect_app.add_typer(inspect_runs_app, name="runs")
app.add_typer(inspect_app, name="inspect")

repair_app = typer.Typer(help="Repair workflows.", no_args_is_help=True)
app.add_typer(repair_app, name="repair")

stage_app = typer.Typer(help="Low-level stage primitives.", no_args_is_help=True)
stage_site_app = typer.Typer(help="Site stage primitives.", no_args_is_help=True)
stage_translate_app = typer.Typer(
    help="Translation stage primitives.", no_args_is_help=True
)
stage_app.add_typer(stage_site_app, name="site")
stage_app.add_typer(stage_translate_app, name="translate")
app.add_typer(stage_app, name="stage")

admin_app = typer.Typer(help="Administrative maintenance commands.", no_args_is_help=True)
admin_db_app = typer.Typer(help="Administrative DB commands.", no_args_is_help=True)
admin_app.add_typer(admin_db_app, name="db")
app.add_typer(admin_app, name="admin")

# Hidden legacy groups retained only where they still map cleanly.
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True, hidden=True)
rag_app = typer.Typer(help="RAG utilities.", no_args_is_help=True, hidden=True)
site_app = typer.Typer(help="Static site utilities.", no_args_is_help=True, hidden=True)
materialize_app = typer.Typer(
    help="Offline output materialization utilities.",
    no_args_is_help=True,
    hidden=True,
)
runs_app = typer.Typer(help="Run history utilities.", no_args_is_help=True, hidden=True)
doctor_app = typer.Typer(help="Workspace diagnostics.", hidden=True)
translate_app = typer.Typer(
    help="Derived translation utilities.", no_args_is_help=True, hidden=True
)
app.add_typer(db_app, name="db", hidden=True)
app.add_typer(rag_app, name="rag", hidden=True)
app.add_typer(site_app, name="site", hidden=True)
app.add_typer(materialize_app, name="materialize", hidden=True)
app.add_typer(runs_app, name="runs", hidden=True)
app.add_typer(doctor_app, name="doctor", hidden=True)
app.add_typer(translate_app, name="translate", hidden=True)


def _legacy_error(
    *,
    command: str,
    replacement: str | None = None,
    json_output: bool = False,
) -> None:
    if replacement is None:
        message = f"`{command}` was removed in CLI v2 and is no longer supported."
    else:
        message = f"`{command}` was removed in CLI v2. Use `{replacement}`."
    if json_output:
        typer.echo(
            json.dumps(
                {"status": "error", "command": command, "error": message},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        typer.echo(message)
    raise typer.Exit(code=2)


@run_app.callback(invoke_without_command=True)
def run_callback(
    ctx: Context,
    once: bool = typer.Option(
        False,
        "--once",
        hidden=True,
        help="Removed in CLI v2.",
    ),
    analyze_limit: int | None = typer.Option(
        None,
        "--analyze-limit",
        hidden=True,
        help="Removed in CLI v2.",
    ),
    publish_limit: int | None = typer.Option(
        None,
        "--publish-limit",
        hidden=True,
        help="Removed in CLI v2.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        hidden=True,
        help="Removed in CLI v2.",
    ),
) -> None:
    if once or analyze_limit is not None or publish_limit is not None or anchor_date is not None:
        _legacy_error(
            command="run --once",
            replacement="run now | run day --date <YYYY-MM-DD> | daemon start",
        )
    if getattr(ctx, "invoked_subcommand", None) is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=2)


@run_app.command("now")
def run_now(
    include: str | None = typer.Option(
        None,
        "--include",
        help="Optionally re-enable preset-optional steps: publish, translate, site-build.",
    ),
    skip: str | None = typer.Option(
        None,
        "--skip",
        help="Optionally skip preset-optional steps: publish, translate, site-build.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run the full current UTC-day workflow."""
    execute_granularity_workflow(
        workflow_name="now",
        command="run now",
        include=include,
        skip=skip,
        json_output=json_output,
    )


@run_app.command("day")
def run_day(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day (YYYY-MM-DD or YYYYMMDD). Defaults to the latest complete UTC day.",
    ),
    include: str | None = typer.Option(
        None,
        "--include",
        help="Optionally re-enable preset-optional steps: publish, translate, site-build.",
    ),
    skip: str | None = typer.Option(
        None,
        "--skip",
        help="Optionally skip preset-optional steps: publish, translate, site-build.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run the full UTC-day workflow."""
    execute_granularity_workflow(
        workflow_name="day",
        command="run day" + (f" --date {anchor_date}" if anchor_date else ""),
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@run_app.command("week")
def run_week(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor UTC date for the target ISO week (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    include: str | None = typer.Option(
        None,
        "--include",
        help="Optionally re-enable preset-optional steps: publish, translate, site-build.",
    ),
    skip: str | None = typer.Option(
        None,
        "--skip",
        help="Optionally skip preset-optional steps: publish, translate, site-build.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run the full ISO-week workflow."""
    execute_granularity_workflow(
        workflow_name="week",
        command="run week" + (f" --date {anchor_date}" if anchor_date else ""),
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@run_app.command("month")
def run_month(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor UTC date for the target month (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    include: str | None = typer.Option(
        None,
        "--include",
        help="Optionally re-enable preset-optional steps: publish, translate, site-build.",
    ),
    skip: str | None = typer.Option(
        None,
        "--skip",
        help="Optionally skip preset-optional steps: publish, translate, site-build.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run the full month workflow."""
    execute_granularity_workflow(
        workflow_name="month",
        command="run month" + (f" --date {anchor_date}" if anchor_date else ""),
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@run_app.command("deploy")
def run_deploy(
    include: str | None = typer.Option(
        None,
        "--include",
        help="Optionally re-enable preset-optional steps: translate, site-build.",
    ),
    skip: str | None = typer.Option(
        None,
        "--skip",
        help="Optionally skip preset-optional steps: translate, site-build.",
    ),
    repo_dir: Path | None = typer.Option(
        None,
        "--repo-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Git repository used to resolve the deployment remote. Defaults to the current working directory.",
    ),
    remote: str = typer.Option(
        "origin",
        "--remote",
        help="Git remote that will receive the deployment branch.",
    ),
    branch: str = typer.Option(
        "gh-pages",
        "--branch",
        help="Deployment branch used by GitHub Pages.",
    ),
    commit_message: str | None = typer.Option(
        None,
        "--message",
        help="Optional git commit message for the deployment branch update.",
    ),
    cname: str | None = typer.Option(
        None,
        "--cname",
        help="Optional custom domain written to the deployment branch CNAME file.",
    ),
    pages_config: str = typer.Option(
        "auto",
        "--pages-config",
        help="How to configure the GitHub Pages source after pushing. Allowed: auto, always, never.",
    ),
    force: bool = typer.Option(
        True,
        "--force/--no-force",
        help="Force-push the deployment branch. Defaults to force for derived site output.",
    ),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Translate, build, and deploy the public site from existing state."""
    execute_deploy_workflow(
        command="run deploy",
        include=include,
        skip=skip,
        repo_dir=repo_dir,
        remote=remote,
        branch=branch,
        commit_message=commit_message,
        cname=cname,
        pages_config=pages_config,
        force=force,
        item_export_scope=item_export_scope,
        json_output=json_output,
    )


@fleet_run_app.command("day")
def fleet_run_day(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day (YYYY-MM-DD or YYYYMMDD). Defaults to the latest complete UTC day.",
    ),
    include: str | None = typer.Option(None, "--include"),
    skip: str | None = typer.Option(None, "--skip"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Run the full UTC-day workflow for every child instance."""
    execute_fleet_granularity_workflow(
        manifest_path=manifest_path,
        workflow_name="day",
        command="fleet run day",
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@fleet_run_app.command("week")
def fleet_run_week(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor UTC date for the target ISO week (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    include: str | None = typer.Option(None, "--include"),
    skip: str | None = typer.Option(None, "--skip"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Run the full ISO-week workflow for every child instance."""
    execute_fleet_granularity_workflow(
        manifest_path=manifest_path,
        workflow_name="week",
        command="fleet run week",
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@fleet_run_app.command("month")
def fleet_run_month(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor UTC date for the target month (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    include: str | None = typer.Option(None, "--include"),
    skip: str | None = typer.Option(None, "--skip"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Run the full month workflow for every child instance."""
    execute_fleet_granularity_workflow(
        manifest_path=manifest_path,
        workflow_name="month",
        command="fleet run month",
        anchor_date=anchor_date,
        include=include,
        skip=skip,
        json_output=json_output,
    )


@fleet_run_app.command("deploy")
def fleet_run_deploy(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    include: str | None = typer.Option(None, "--include"),
    skip: str | None = typer.Option(None, "--skip"),
    repo_dir: Path | None = typer.Option(
        None,
        "--repo-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    remote: str = typer.Option("origin", "--remote"),
    branch: str = typer.Option("gh-pages", "--branch"),
    commit_message: str | None = typer.Option(None, "--message"),
    cname: str | None = typer.Option(None, "--cname"),
    pages_config: str = typer.Option("auto", "--pages-config"),
    force: bool = typer.Option(True, "--force/--no-force"),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Deploy the aggregate fleet static site."""
    execute_fleet_deploy_workflow(
        manifest_path=manifest_path,
        command="fleet run deploy",
        include=include,
        skip=skip,
        repo_dir=repo_dir,
        remote=remote,
        branch=branch,
        commit_message=commit_message,
        cname=cname,
        pages_config=pages_config,
        force=force,
        item_export_scope=item_export_scope,
        json_output=json_output,
    )


@run_app.command("translate")
def run_translate(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="SQLite database path. Defaults to RECOLETA_DB_PATH or the configured settings file.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="YAML/JSON config path used to resolve localization settings and the database path.",
    ),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(
        None,
        "--granularity",
        help="Optionally constrain trend and idea translations to day, week, or month windows.",
    ),
    include: str = typer.Option(
        "items,trends,ideas",
        "--include",
        help="Comma-separated surfaces to translate: items, trends, ideas.",
    ),
    limit: int | None = typer.Option(
        None,
        "--limit",
        min=1,
        help="Optional cap on source records per included surface.",
    ),
    force: bool = typer.Option(
        False,
        "--force/--no-force",
        help="Rewrite localized outputs even when the source hash is unchanged.",
    ),
    context_assist: str = typer.Option(
        "direct",
        "--context-assist",
        help="Translation context mode: none, direct, or hybrid.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run the translation workflow only."""
    run_translate_run_command(
        db_path=db_path,
        config_path=config_path,
        scope=scope,
        granularity=granularity,
        include=include,
        limit=limit,
        force=force,
        context_assist=context_assist,
        json_output=json_output,
        command_name="run translate",
    )


@fleet_site_app.command("build")
def fleet_site_build(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    limit: int | None = typer.Option(None, min=1),
    default_language_code: str | None = typer.Option(None, "--default-language-code"),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Build the aggregate fleet static site from child outputs only."""
    run_fleet_site_build_command(
        manifest_path=manifest_path,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
        command_name="fleet site build",
    )


@fleet_site_app.command("serve")
def fleet_site_serve(
    manifest_path: Path = typer.Option(
        ...,
        "--manifest",
        envvar="RECOLETA_FLEET_MANIFEST",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Fleet manifest that references child instance configs.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Directory containing the built aggregate fleet static site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally build only the latest N trend notes and sibling idea briefs before serving.",
    ),
    host: str = typer.Option("127.0.0.1", "--host", help="Host interface to bind the preview server to."),
    port: int = typer.Option(
        8000,
        "--port",
        min=0,
        max=65535,
        help="TCP port for the local preview server. Use 0 to auto-select.",
    ),
    build: bool = typer.Option(
        True,
        "--build/--no-build",
        help="Build the aggregate fleet static site before serving it.",
    ),
    default_language_code: str | None = typer.Option(
        None,
        "--default-language-code",
        help="Default language code for multilingual aggregate site builds performed before serving.",
    ),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
) -> None:
    """Build and serve the aggregate fleet static site locally."""
    run_fleet_site_serve_command(
        manifest_path=manifest_path,
        output_dir=output_dir,
        limit=limit,
        host=host,
        port=port,
        build=build,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        command_name="fleet site serve",
        build_command_name="fleet site build",
    )


@run_site_app.command("build")
def run_site_build(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes and sibling idea briefs.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Destination directory for the exported static site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally export only the latest N trend notes and sibling idea briefs.",
    ),
    default_language_code: str | None = typer.Option(
        None,
        "--default-language-code",
        help="Default language code for multilingual static site builds.",
    ),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Build the static site."""
    run_site_build_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
        command_name="run site build",
    )


@run_site_app.command("serve")
def run_site_serve(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes and sibling idea briefs when building before serving.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Directory containing the built static site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally build only the latest N trend notes and sibling idea briefs before serving.",
    ),
    host: str = typer.Option("127.0.0.1", "--host", help="Host interface to bind the preview server to."),
    port: int = typer.Option(
        8000,
        "--port",
        min=0,
        max=65535,
        help="TCP port for the local preview server. Use 0 to auto-select.",
    ),
    build: bool = typer.Option(
        True,
        "--build/--no-build",
        help="Build the static site before serving it.",
    ),
    default_language_code: str | None = typer.Option(
        None,
        "--default-language-code",
        help="Default language code for multilingual builds performed before serving.",
    ),
    item_export_scope: str = typer.Option(
        "linked",
        "--item-export-scope",
        help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export.",
    ),
) -> None:
    """Build and serve the static site locally."""
    run_site_serve_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        host=host,
        port=port,
        build=build,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        command_name="run site serve",
        build_command_name="run site build",
    )


@daemon_app.command("start")
def daemon_start() -> None:
    """Start the configured workflow scheduler."""
    run_daemon_start_command()


@inspect_app.command("health")
def inspect_health(
    healthcheck: bool = typer.Option(
        False,
        "--healthcheck",
        help="Run a read-only healthcheck suitable for supervisors and containers.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    max_success_age_minutes: int | None = typer.Option(
        None,
        "--max-success-age-minutes",
        min=1,
        help="Fail if the latest successful run is older than this many minutes.",
    ),
) -> None:
    """Run read-only workspace health diagnostics."""
    run_doctor_command(
        healthcheck=healthcheck,
        db_path=db_path,
        config_path=config_path,
        max_success_age_minutes=max_success_age_minutes,
        command_name="inspect health",
    )


@inspect_app.command("why-empty")
def inspect_why_empty(
    anchor_date: str = typer.Option(..., "--date", help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD)."),
    granularity: str = typer.Option(
        "day",
        "--granularity",
        help="Corpus window granularity. Allowed: day, week, month.",
    ),
    stream: str = typer.Option(
        "default",
        "--stream",
        help="Topic stream / scope to inspect. Use default for the default corpus.",
    ),
    min_relevance_score: float | None = typer.Option(
        None,
        "--min-relevance-score",
        help="Override the relevance threshold used when explaining corpus selection.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of human-readable text.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
) -> None:
    """Explain why a trend corpus window is empty or smaller than expected."""
    run_doctor_why_empty_command(
        db_path=db_path,
        config_path=config_path,
        anchor_date=anchor_date,
        granularity=granularity,
        stream=stream,
        min_relevance_score=min_relevance_score,
        json_output=json_output,
        command_name="inspect why-empty",
    )


@inspect_app.command("llm")
def inspect_llm(
    ping: bool = typer.Option(
        False,
        "--ping/--no-ping",
        help="Run a lightweight connectivity probe against the configured LLM model.",
    ),
    timeout_seconds: float = typer.Option(
        20.0,
        "--timeout-seconds",
        min=1.0,
        help="Per-request timeout for the optional LLM ping probe.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of human-readable text.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Used only to help load settings when needed.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve settings.",
    ),
) -> None:
    """Inspect effective LLM configuration and optionally probe the provider."""
    run_doctor_llm_command(
        ping=ping,
        timeout_seconds=timeout_seconds,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
        command_name="inspect llm",
    )


@inspect_app.command("stats")
def inspect_stats(
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
) -> None:
    """Summarize read-only workspace operational state."""
    run_stats_command(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
        command_name="inspect stats",
    )


@inspect_runs_app.command("show")
def inspect_runs_show(
    run_id: str | None = typer.Option(None, "--run-id", help="Run id to inspect. Defaults to the most recent run."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
) -> None:
    """Inspect a single recorded run."""
    run_runs_show_command(
        run_id=run_id,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@inspect_runs_app.command("list")
def inspect_runs_list(
    limit: int = typer.Option(10, "--limit", min=1, help="Max number of recent runs to return."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
) -> None:
    """List recent runs."""
    run_runs_list_command(
        limit=limit,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@repair_app.command("streams", hidden=True)
def repair_streams(
    _anchor_date: str = typer.Option(..., "--date", help="Target UTC day to repair (YYYY-MM-DD or YYYYMMDD)."),
    _streams: str = typer.Option(..., "--streams", help="Comma-separated topic stream names to requeue for analysis."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON instead of human-readable text."),
    _db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    _config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
) -> None:
    """Legacy compatibility entrypoint retained only to fail closed."""
    _legacy_error(command="repair streams", json_output=json_output)


@repair_app.command("outputs")
def repair_outputs(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="SQLite database path. Defaults to RECOLETA_DB_PATH or the configured settings file.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Optional YAML/JSON config path used to resolve the database and default output directories.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Markdown output root to rewrite for one standalone instance or one child instance.",
    ),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(
        None,
        "--granularity",
        help="Optionally rerender only day, week, or month trend notes.",
    ),
    pdf: bool = typer.Option(False, "--pdf/--no-pdf", help="Regenerate trend PDFs from the rerendered markdown notes."),
    site: bool = typer.Option(False, "--site/--no-site", help="Rebuild the static site after markdown outputs are materialized."),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    debug_pdf: bool = typer.Option(False, "--debug-pdf/--no-debug-pdf", help="Export PDF render debug bundles beside regenerated PDFs."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Repair filesystem outputs from stored DB state."""
    run_materialize_outputs_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
        scope=scope,
        granularity=granularity,
        pdf=pdf,
        site=site,
        item_export_scope=item_export_scope,
        debug_pdf=debug_pdf,
        json_output=json_output,
        command_name="repair outputs",
    )


@stage_app.command("ingest")
def stage_ingest(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to prepare (YYYY-MM-DD or YYYYMMDD). Defaults to latest backlog behavior.",
    ),
) -> None:
    """Run the ingest stage primitive."""
    run_ingest_command(anchor_date=anchor_date)


@stage_app.command("analyze")
def stage_analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to analyze (YYYY-MM-DD or YYYYMMDD). Defaults to latest prepared backlog behavior.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the analyze stage primitive."""
    run_analyze_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


@stage_app.command("publish")
def stage_publish(
    limit: int = typer.Option(50, min=1, help="Max number of analyzed items published."),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to publish (YYYY-MM-DD or YYYYMMDD). Defaults to latest analyzed backlog behavior.",
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the publish stage primitive."""
    run_publish_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


@stage_app.command("trends")
def stage_trends(
    granularity: str = typer.Option("day", "--granularity", help="Trend granularity. Allowed: day, week, month."),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(None, "--model", help="Override LLM model for trend generation. Defaults to LLM_MODEL."),
    debug_pdf: bool = typer.Option(False, "--debug-pdf/--no-debug-pdf", help="Export PDF render intermediates and page previews beside the trend PDF."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the trends stage primitive."""
    run_trends_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        backfill=False,
        backfill_mode="missing",
        debug_pdf=debug_pdf,
        json_output=json_output,
    )


@stage_app.command("ideas")
def stage_ideas(
    granularity: str = typer.Option("day", "--granularity", help="Ideas granularity. Allowed: day, week, month."),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(None, "--model", help="Override LLM model for ideas generation. Defaults to LLM_MODEL."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the ideas stage primitive."""
    run_ideas_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        json_output=json_output,
    )


@stage_translate_app.command("run")
def stage_translate_run(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="SQLite database path. Defaults to RECOLETA_DB_PATH or the configured settings file.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="YAML/JSON config path used to resolve localization settings and the database path.",
    ),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(None, "--granularity", help="Optionally constrain trend and idea translations to day, week, or month windows."),
    include: str = typer.Option("items,trends,ideas", "--include", help="Comma-separated surfaces to translate: items, trends, ideas."),
    limit: int | None = typer.Option(None, "--limit", min=1, help="Optional cap on source records per included surface."),
    force: bool = typer.Option(False, "--force/--no-force", help="Rewrite localized outputs even when the source hash is unchanged."),
    context_assist: str = typer.Option("direct", "--context-assist", help="Translation context mode: none, direct, or hybrid."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the translation stage primitive."""
    run_translate_run_command(
        db_path=db_path,
        config_path=config_path,
        scope=scope,
        granularity=granularity,
        include=include,
        limit=limit,
        force=force,
        context_assist=context_assist,
        json_output=json_output,
        command_name="stage translate run",
    )


@stage_translate_app.command("backfill")
def stage_translate_backfill(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="SQLite database path. Defaults to RECOLETA_DB_PATH or the configured settings file.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="YAML/JSON config path used to resolve localization settings and the database path.",
    ),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(None, "--granularity", help="Optionally constrain trend and idea backfill to day, week, or month windows."),
    include: str = typer.Option("items,trends,ideas", "--include", help="Comma-separated surfaces to backfill: items, trends, ideas."),
    limit: int | None = typer.Option(None, "--limit", min=1, help="Optional cap on source records per included surface."),
    force: bool = typer.Option(False, "--force/--no-force", help="Rewrite localized outputs even when the source hash is unchanged."),
    context_assist: str = typer.Option("direct", "--context-assist", help="Translation context mode: none, direct, or hybrid."),
    legacy_source_language: str | None = typer.Option(None, "--legacy-source-language", help="Language code for historical canonical content."),
    emit_mirror_targets: bool = typer.Option(False, "--emit-mirror-targets/--no-emit-mirror-targets", help="Also persist mirror variants for configured target languages."),
    all_history: bool = typer.Option(False, "--all-history/--latest-only", help="Backfill the full historical corpus instead of only current windows."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the translation backfill primitive."""
    run_translate_backfill_command(
        db_path=db_path,
        config_path=config_path,
        scope=scope,
        granularity=granularity,
        include=include,
        limit=limit,
        force=force,
        context_assist=context_assist,
        legacy_source_language=legacy_source_language,
        emit_mirror_targets=emit_mirror_targets,
        all_history=all_history,
        json_output=json_output,
        command_name="stage translate backfill",
    )


@stage_site_app.command("build")
def stage_site_build(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True, help="Directory containing trend markdown notes and sibling idea briefs."),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Destination directory for the exported static site."),
    limit: int | None = typer.Option(None, min=1, help="Optionally export only the latest N trend notes and sibling idea briefs."),
    default_language_code: str | None = typer.Option(None, "--default-language-code", help="Default language code for multilingual static site builds."),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the site build stage primitive."""
    run_site_build_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
        command_name="stage site build",
    )


@stage_site_app.command("stage")
def stage_site_stage(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True, help="Directory containing trend markdown notes and sibling idea briefs."),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Repo-local directory to mirror trend markdown notes and sibling idea briefs for deployment."),
    limit: int | None = typer.Option(None, min=1, help="Optionally stage only the latest N trend notes and sibling idea briefs."),
    default_language_code: str | None = typer.Option(None, "--default-language-code", help="Default language code metadata for multilingual staged content."),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the site stage primitive."""
    run_site_stage_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
        command_name="stage site stage",
    )


@stage_site_app.command("serve")
def stage_site_serve(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True, help="Directory containing trend markdown notes and sibling idea briefs when building before serving."),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Directory containing the built static site."),
    limit: int | None = typer.Option(None, min=1, help="Optionally build only the latest N trend notes and sibling idea briefs before serving."),
    host: str = typer.Option("127.0.0.1", "--host", help="Host interface to bind the local preview server to."),
    port: int = typer.Option(8000, "--port", min=0, max=65535, help="TCP port for the local preview server. Use 0 to auto-select."),
    build: bool = typer.Option(True, "--build/--no-build", help="Build the static site before serving it."),
    default_language_code: str | None = typer.Option(None, "--default-language-code", help="Default language code for multilingual builds performed before serving."),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
) -> None:
    """Run the site serve primitive."""
    run_site_serve_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        host=host,
        port=port,
        build=build,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        command_name="stage site serve",
        build_command_name="stage site build",
    )


@stage_app.command("materialize")
def stage_materialize(
    db_path: Path | None = typer.Option(None, "--db-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="SQLite database path."),
    config_path: Path | None = typer.Option(None, "--config-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True, help="Optional YAML/JSON config path used to resolve the database and default output directories."),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Markdown output root to rewrite for one standalone instance or one child instance."),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(None, "--granularity", help="Optionally rerender only day, week, or month trend notes."),
    pdf: bool = typer.Option(False, "--pdf/--no-pdf", help="Regenerate trend PDFs from the rerendered markdown notes."),
    site: bool = typer.Option(False, "--site/--no-site", help="Rebuild the static site after markdown outputs are materialized."),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    debug_pdf: bool = typer.Option(False, "--debug-pdf/--no-debug-pdf", help="Export PDF render debug bundles beside regenerated PDFs."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    """Run the materialize primitive."""
    run_materialize_outputs_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
        scope=scope,
        granularity=granularity,
        pdf=pdf,
        site=site,
        item_export_scope=item_export_scope,
        debug_pdf=debug_pdf,
        json_output=json_output,
        command_name="stage materialize",
    )


@admin_app.command("gc")
def admin_gc(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    prune_caches: bool = typer.Option(False, "--prune-caches", help="Also prune rebuildable caches."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Report what would be deleted without mutating the workspace."),
) -> None:
    """Prune expired debug material and operational history."""
    run_gc_command(
        db_path=db_path,
        config_path=config_path,
        prune_caches=prune_caches,
        dry_run=dry_run,
    )


@admin_app.command("vacuum")
def admin_vacuum(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
) -> None:
    """Run SQLite VACUUM on the configured database."""
    run_vacuum_command(db_path=db_path, config_path=config_path)


@admin_app.command("backup")
def admin_backup(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True, help="Directory where timestamped backup bundles should be created."),
) -> None:
    """Create a DB-scoped backup bundle."""
    run_backup_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
    )


@admin_app.command("restore")
def admin_restore(
    bundle: Path = typer.Option(..., "--bundle", exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True, help="Path to a backup bundle directory created by `recoleta admin backup`."),
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm replacing the target DB."),
) -> None:
    """Restore the SQLite DB from a backup bundle."""
    run_restore_command(
        bundle=bundle,
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@admin_db_app.command("clear")
def admin_db_clear(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm deletion without prompting."),
) -> None:
    """Delete the configured SQLite DB file for a clean slate."""
    run_db_clear_command(db_path=db_path, config_path=config_path, yes=yes)


@admin_db_app.command("reset")
def admin_db_reset(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    trends_only: bool = typer.Option(False, "--trends-only", help="Only reset trend-related documents/chunks."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm deletion without prompting."),
) -> None:
    """Reset the SQLite DB (full reset) or only trend-related content."""
    run_db_reset_command(
        db_path=db_path,
        config_path=config_path,
        trends_only=trends_only,
        yes=yes,
    )


@admin_db_app.command("cleanup-instance-first-schema")
def admin_db_cleanup_instance_first_schema(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm dropping legacy stream-state tables."),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    """Drop legacy stream-state tables after instance-first cutover."""
    run_db_cleanup_instance_first_schema_command(
        db_path=db_path,
        config_path=config_path,
        yes=yes,
        json_output=json_output,
    )


# Hidden legacy commands and groups that should fail cleanly.
@app.command("trends-week", hidden=True, context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def legacy_trends_week(ctx: Context) -> None:  # noqa: ARG001
    _legacy_error(command="trends-week", replacement="run week --date <YYYY-MM-DD>")


@app.command("repair-streams", hidden=True, context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def legacy_repair_streams(
    ctx: Context,  # noqa: ARG001
    json_output: bool = typer.Option(False, "--json", hidden=True),
) -> None:
    _legacy_error(command="repair-streams", json_output=json_output)


@materialize_app.command("outputs", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def legacy_materialize_outputs(
    ctx: Context,  # noqa: ARG001
    json_output: bool = typer.Option(False, "--json", hidden=True),
) -> None:
    _legacy_error(command="materialize outputs", replacement="repair outputs", json_output=json_output)


@site_app.command("gh-deploy", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def legacy_site_gh_deploy(
    ctx: Context,  # noqa: ARG001
    json_output: bool = typer.Option(False, "--json", hidden=True),
) -> None:
    _legacy_error(command="site gh-deploy", replacement="run deploy", json_output=json_output)


# Hidden legacy aliases that still map cleanly.
@app.command(hidden=True)
def ingest(
    anchor_date: str | None = typer.Option(None, "--date", help="Target UTC day to prepare (YYYY-MM-DD or YYYYMMDD)."),
) -> None:
    run_ingest_command(anchor_date=anchor_date)


@app.command(hidden=True)
def analyze(
    limit: int | None = typer.Option(None, min=1, help="Max number of items analyzed in one run."),
    anchor_date: str | None = typer.Option(None, "--date", help="Target UTC day to analyze (YYYY-MM-DD or YYYYMMDD)."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    run_analyze_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


@app.command(hidden=True)
def publish(
    limit: int = typer.Option(50, min=1, help="Max number of analyzed items published."),
    anchor_date: str | None = typer.Option(None, "--date", help="Target UTC day to publish (YYYY-MM-DD or YYYYMMDD)."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    run_publish_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


@app.command(hidden=True)
def trends(
    granularity: str = typer.Option("day", "--granularity", help="Trend granularity. Allowed: day, week, month."),
    anchor_date: str | None = typer.Option(None, "--date", help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD)."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model for trend generation."),
    debug_pdf: bool = typer.Option(False, "--debug-pdf/--no-debug-pdf", help="Export PDF render intermediates and previews."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    run_trends_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        backfill=False,
        backfill_mode="missing",
        debug_pdf=debug_pdf,
        json_output=json_output,
    )


@app.command(hidden=True)
def ideas(
    granularity: str = typer.Option("day", "--granularity", help="Ideas granularity. Allowed: day, week, month."),
    anchor_date: str | None = typer.Option(None, "--date", help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD)."),
    model: str | None = typer.Option(None, "--model", help="Override LLM model for ideas generation."),
    json_output: bool = typer.Option(False, "--json", help="Emit machine-readable JSON output."),
) -> None:
    run_ideas_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        json_output=json_output,
    )


@app.command("gc", hidden=True)
def legacy_gc(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    prune_caches: bool = typer.Option(False, "--prune-caches", help="Also prune rebuildable caches."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Report what would be deleted without mutating the workspace."),
) -> None:
    run_gc_command(
        db_path=db_path,
        config_path=config_path,
        prune_caches=prune_caches,
        dry_run=dry_run,
    )


@app.command("vacuum", hidden=True)
def legacy_vacuum(
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_vacuum_command(db_path=db_path, config_path=config_path)


@app.command("backup", hidden=True)
def legacy_backup(
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True),
) -> None:
    run_backup_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
    )


@app.command("restore", hidden=True)
def legacy_restore(
    bundle: Path = typer.Option(..., "--bundle", exists=True, file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    run_restore_command(
        bundle=bundle,
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@app.command("stats", hidden=True)
def legacy_stats(
    json_output: bool = typer.Option(False, "--json"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_stats_command(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@site_app.command("build")
def legacy_site_build(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    limit: int | None = typer.Option(None, min=1),
    default_language_code: str | None = typer.Option(None, "--default-language-code"),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    run_site_build_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
    )


@site_app.command("stage")
def legacy_site_stage(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, resolve_path=True, writable=True),
    limit: int | None = typer.Option(None, min=1),
    default_language_code: str | None = typer.Option(None, "--default-language-code"),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    run_site_stage_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        json_output=json_output,
    )


@site_app.command("serve")
def legacy_site_serve(
    input_dir: Path | None = typer.Option(None, "--input-dir", file_okay=False, dir_okay=True, readable=True, resolve_path=True),
    output_dir: Path | None = typer.Option(None, "--output-dir", file_okay=False, dir_okay=True, writable=True, resolve_path=True),
    limit: int | None = typer.Option(None, min=1),
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8000, "--port", min=0, max=65535),
    build: bool = typer.Option(True, "--build/--no-build"),
    default_language_code: str | None = typer.Option(None, "--default-language-code"),
    item_export_scope: str = typer.Option("linked", "--item-export-scope", help="Export only items linked from selected trend/idea pages by default. Use 'all' to restore the legacy full item export."),
) -> None:
    run_site_serve_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        host=host,
        port=port,
        build=build,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
    )


@translate_app.command("run")
def legacy_translate_run(
    db_path: Path | None = typer.Option(None, "--db-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    config_path: Path | None = typer.Option(None, "--config-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(None, "--granularity"),
    include: str = typer.Option("items,trends,ideas", "--include"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    force: bool = typer.Option(False, "--force/--no-force"),
    context_assist: str = typer.Option("direct", "--context-assist"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    run_translate_run_command(
        db_path=db_path,
        config_path=config_path,
        scope=scope,
        granularity=granularity,
        include=include,
        limit=limit,
        force=force,
        context_assist=context_assist,
        json_output=json_output,
    )


@translate_app.command("backfill")
def legacy_translate_backfill(
    db_path: Path | None = typer.Option(None, "--db-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    config_path: Path | None = typer.Option(None, "--config-path", file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Instance-local scope. Must stay 'default' in instance-first runtime.",
    ),
    granularity: str | None = typer.Option(None, "--granularity"),
    include: str = typer.Option("items,trends,ideas", "--include"),
    limit: int | None = typer.Option(None, "--limit", min=1),
    force: bool = typer.Option(False, "--force/--no-force"),
    context_assist: str = typer.Option("direct", "--context-assist"),
    legacy_source_language: str | None = typer.Option(None, "--legacy-source-language"),
    emit_mirror_targets: bool = typer.Option(False, "--emit-mirror-targets/--no-emit-mirror-targets"),
    all_history: bool = typer.Option(False, "--all-history/--latest-only"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    run_translate_backfill_command(
        db_path=db_path,
        config_path=config_path,
        scope=scope,
        granularity=granularity,
        include=include,
        limit=limit,
        force=force,
        context_assist=context_assist,
        legacy_source_language=legacy_source_language,
        emit_mirror_targets=emit_mirror_targets,
        all_history=all_history,
        json_output=json_output,
    )


@runs_app.command("show")
def legacy_runs_show(
    run_id: str | None = typer.Option(None, "--run-id"),
    json_output: bool = typer.Option(False, "--json"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_runs_show_command(
        run_id=run_id,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@runs_app.command("list")
def legacy_runs_list(
    limit: int = typer.Option(10, "--limit", min=1),
    json_output: bool = typer.Option(False, "--json"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_runs_list_command(
        limit=limit,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@doctor_app.callback(invoke_without_command=True)
def legacy_doctor(
    ctx: Context,
    healthcheck: bool = typer.Option(False, "--healthcheck"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
    max_success_age_minutes: int | None = typer.Option(None, "--max-success-age-minutes", min=1),
) -> None:
    if getattr(ctx, "invoked_subcommand", None) is not None:
        return
    run_doctor_command(
        healthcheck=healthcheck,
        db_path=db_path,
        config_path=config_path,
        max_success_age_minutes=max_success_age_minutes,
    )


@doctor_app.command("why-empty")
def legacy_doctor_why_empty(
    anchor_date: str = typer.Option(..., "--date"),
    granularity: str = typer.Option("day", "--granularity"),
    stream: str = typer.Option("default", "--stream"),
    min_relevance_score: float | None = typer.Option(None, "--min-relevance-score"),
    json_output: bool = typer.Option(False, "--json"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_doctor_why_empty_command(
        db_path=db_path,
        config_path=config_path,
        anchor_date=anchor_date,
        granularity=granularity,
        stream=stream,
        min_relevance_score=min_relevance_score,
        json_output=json_output,
    )


@doctor_app.command("llm")
def legacy_doctor_llm(
    ping: bool = typer.Option(False, "--ping/--no-ping"),
    timeout_seconds: float = typer.Option(20.0, "--timeout-seconds", min=1.0),
    json_output: bool = typer.Option(False, "--json"),
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
) -> None:
    run_doctor_llm_command(
        ping=ping,
        timeout_seconds=timeout_seconds,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@db_app.command("clear")
def legacy_db_clear(
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    run_db_clear_command(db_path=db_path, config_path=config_path, yes=yes)


@db_app.command("reset")
def legacy_db_reset(
    db_path: Path | None = typer.Option(None, "--db-path"),
    config_path: Path | None = typer.Option(None, "--config"),
    trends_only: bool = typer.Option(False, "--trends-only"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    run_db_reset_command(
        db_path=db_path,
        config_path=config_path,
        trends_only=trends_only,
        yes=yes,
    )


@rag_app.command("sync-vectors")
def legacy_rag_sync_vectors(
    doc_type: str = typer.Option("item", "--doc-type"),
    period_start: str = typer.Option(..., "--period-start"),
    period_end: str = typer.Option(..., "--period-end"),
    page_size: int = typer.Option(500, "--page-size", min=1, max=5000),
) -> None:
    run_rag_sync_vectors_command(
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        page_size=page_size,
    )


@rag_app.command("build-index")
def legacy_rag_build_index(
    vector: bool = typer.Option(True, "--vector/--no-vector"),
    scalar: bool = typer.Option(True, "--scalar/--no-scalar"),
    vector_index_type: str = typer.Option("IVF_HNSW_SQ", "--vector-index-type"),
    vector_metric: str = typer.Option("cosine", "--vector-metric"),
    vector_num_partitions: int | None = typer.Option(None, "--vector-num-partitions", min=1),
    vector_num_sub_vectors: int | None = typer.Option(None, "--vector-num-sub-vectors", min=1),
    strict: bool = typer.Option(False, "--strict"),
) -> None:
    run_rag_build_index_command(
        vector=vector,
        scalar=scalar,
        vector_index_type=vector_index_type,
        vector_metric=vector_metric,
        vector_num_partitions=vector_num_partitions,
        vector_num_sub_vectors=vector_num_sub_vectors,
        strict=strict,
    )


def main() -> None:
    app()
