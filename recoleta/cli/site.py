from __future__ import annotations

import json
from pathlib import Path

import recoleta.cli as cli


def run_site_build_command(
    *,
    input_dir: Path | None,
    output_dir: Path | None,
    limit: int | None,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    export_trend_static_site = cli._import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )

    resolved_input_dir = (
        input_dir.expanduser().resolve() if input_dir is not None else None
    )
    resolved_output_dir = (
        output_dir.expanduser().resolve() if output_dir is not None else None
    )
    settings = (
        cli._build_settings()
        if resolved_input_dir is None or resolved_output_dir is None
        else None
    )
    if resolved_input_dir is None:
        assert settings is not None
        resolved_input_dir = (
            settings.markdown_output_dir
            if cli._has_explicit_topic_streams(settings)
            else settings.markdown_output_dir / "Trends"
        )
    if resolved_output_dir is None:
        assert settings is not None
        resolved_output_dir = settings.markdown_output_dir / "site"
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        cli._maybe_acquire_workspace_lease_for_settings(
            settings=settings,
            console=console,
            command="site build",
            log_module="cli.site.build",
        )
    )
    try:
        manifest_path = export_trend_static_site(
            input_dir=resolved_input_dir,
            output_dir=resolved_output_dir,
            limit=limit,
        )
        if lease_heartbeat_monitor is not None:
            lease_heartbeat_monitor.raise_if_failed()
    finally:
        if (
            lease_repository is not None
            and lease_owner_token is not None
            and lease_log is not None
            and lease_heartbeat_monitor is not None
        ):
            cli._cleanup_workspace_lease(
                repository=lease_repository,
                owner_token=lease_owner_token,
                heartbeat_monitor=lease_heartbeat_monitor,
                log=lease_log,
            )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stream_segment = (
        f" streams={manifest['streams_total']}"
        if int(manifest.get("streams_total") or 0) > 1
        else ""
    )
    console.print(
        "[green]site build completed[/green] "
        f"trends={manifest['trends_total']} "
        f"topics={manifest['topics_total']} "
        f"{stream_segment}"
        f"output={resolved_output_dir}"
    )


def run_site_stage_command(
    *,
    input_dir: Path | None,
    output_dir: Path | None,
    limit: int | None,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    stage_trend_site_source = cli._import_symbol(
        "recoleta.site",
        attr_name="stage_trend_site_source",
    )

    resolved_input_dir = (
        input_dir.expanduser().resolve() if input_dir is not None else None
    )
    resolved_output_dir = (
        output_dir.expanduser().resolve() if output_dir is not None else None
    )
    settings = (
        cli._build_settings()
        if resolved_input_dir is None or resolved_output_dir is None
        else None
    )
    if resolved_input_dir is None:
        assert settings is not None
        resolved_input_dir = (
            settings.markdown_output_dir
            if cli._has_explicit_topic_streams(settings)
            else settings.markdown_output_dir / "Trends"
        )
    if resolved_output_dir is None:
        resolved_output_dir = (
            (Path.cwd() / "site-content").resolve()
            if settings is not None and cli._has_explicit_topic_streams(settings)
            else (Path.cwd() / "site-content" / "Trends").resolve()
        )
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        cli._maybe_acquire_workspace_lease_for_settings(
            settings=settings,
            console=console,
            command="site stage",
            log_module="cli.site.stage",
        )
    )
    try:
        manifest_path = stage_trend_site_source(
            input_dir=resolved_input_dir,
            output_dir=resolved_output_dir,
            limit=limit,
        )
        if lease_heartbeat_monitor is not None:
            lease_heartbeat_monitor.raise_if_failed()
    finally:
        if (
            lease_repository is not None
            and lease_owner_token is not None
            and lease_log is not None
            and lease_heartbeat_monitor is not None
        ):
            cli._cleanup_workspace_lease(
                repository=lease_repository,
                owner_token=lease_owner_token,
                heartbeat_monitor=lease_heartbeat_monitor,
                log=lease_log,
            )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    stream_segment = (
        f" streams={manifest['streams_total']}"
        if int(manifest.get("streams_total") or 0) > 1
        else ""
    )
    console.print(
        "[green]site stage completed[/green] "
        f"trends={manifest['trends_total']} "
        f"pdfs={manifest['pdf_total']} "
        f"{stream_segment}"
        f"output={resolved_output_dir}"
    )
