from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from loguru import logger

import recoleta.cli as cli


class _SilentSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        _ = (format, args)
        return None


def _create_site_server(
    *,
    directory: Path,
    host: str,
    port: int,
) -> ThreadingHTTPServer:
    handler = partial(_SilentSimpleHTTPRequestHandler, directory=str(directory))
    return ThreadingHTTPServer((host, port), handler)


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
    segments = [f"trends={manifest['trends_total']}"]
    if int(manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={manifest['ideas_total']}")
    segments.append(f"topics={manifest['topics_total']}")
    if int(manifest.get("streams_total") or 0) > 1:
        segments.append(f"streams={manifest['streams_total']}")
    segments.append(f"output={resolved_output_dir}")
    console.print(
        "[green]site build completed[/green] " + " ".join(segments)
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
    segments = [f"trends={manifest['trends_total']}"]
    if int(manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={manifest['ideas_total']}")
    segments.append(f"pdfs={manifest['pdf_total']}")
    if int(manifest.get("streams_total") or 0) > 1:
        segments.append(f"streams={manifest['streams_total']}")
    segments.append(f"output={resolved_output_dir}")
    console.print(
        "[green]site stage completed[/green] " + " ".join(segments)
    )


def run_site_serve_command(
    *,
    input_dir: Path | None,
    output_dir: Path | None,
    limit: int | None,
    host: str,
    port: int,
    build: bool,
) -> None:
    resolved_output_dir = (
        output_dir.expanduser().resolve() if output_dir is not None else None
    )
    settings = (
        cli._build_settings()
        if resolved_output_dir is None or (build and input_dir is None)
        else None
    )
    if resolved_output_dir is None:
        assert settings is not None
        resolved_output_dir = settings.markdown_output_dir / "site"

    if build:
        run_site_build_command(
            input_dir=input_dir,
            output_dir=resolved_output_dir,
            limit=limit,
        )

    if not resolved_output_dir.exists() or not resolved_output_dir.is_dir():
        raise ValueError(
            f"Static site output directory must exist before serving: {resolved_output_dir}"
        )

    console_cls = cli._runtime_symbols()["Console"]
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    log = logger.bind(
        module="cli.site.serve",
        host=host,
        port=port,
    )
    try:
        with _create_site_server(
            directory=resolved_output_dir,
            host=host,
            port=port,
        ) as server:
            served_host = str(server.server_address[0])
            served_port = int(server.server_address[1])
            log.info("Site preview server started")
            console.print(
                "[green]site serve ready[/green] "
                f"url=http://{served_host}:{served_port} "
                f"output={resolved_output_dir}"
            )
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                log.info("Site preview server stopped")
    except OSError as exc:
        log.warning("site preview server failed error={}", str(exc))
        raise


def run_site_gh_deploy_command(
    *,
    input_dir: Path | None,
    repo_dir: Path | None,
    remote: str,
    branch: str,
    limit: int | None,
    commit_message: str | None,
    cname: str | None,
    pages_config: str,
    force: bool,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    deploy_trend_static_site_to_github_pages = cli._import_symbol(
        "recoleta.site_deploy",
        attr_name="deploy_trend_static_site_to_github_pages",
    )

    resolved_input_dir = (
        input_dir.expanduser().resolve() if input_dir is not None else None
    )
    resolved_repo_dir = (
        repo_dir.expanduser().resolve() if repo_dir is not None else Path.cwd().resolve()
    )
    settings = cli._build_settings() if resolved_input_dir is None else None
    if resolved_input_dir is None:
        assert settings is not None
        resolved_input_dir = (
            settings.markdown_output_dir
            if cli._has_explicit_topic_streams(settings)
            else settings.markdown_output_dir / "Trends"
        )
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        cli._maybe_acquire_workspace_lease_for_settings(
            settings=settings,
            console=console,
            command="site gh-deploy",
            log_module="cli.site.gh_deploy",
        )
    )
    try:
        result = deploy_trend_static_site_to_github_pages(
            input_dir=resolved_input_dir,
            repo_dir=resolved_repo_dir,
            remote=remote,
            branch=branch,
            limit=limit,
            commit_message=commit_message,
            cname=cname,
            pages_config_mode=pages_config,
            force=force,
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

    stream_segment = (
        f"streams={result.streams_total}" if int(result.streams_total or 0) > 1 else None
    )
    status_segment = "no changes" if result.skipped else "pushed"
    commit_segment = (
        f"commit={result.commit_sha[:12]}" if result.commit_sha is not None else None
    )
    summary_parts = [
        f"status={status_segment}",
        f"trends={result.trends_total}",
        f"topics={result.topics_total}",
    ]
    if stream_segment is not None:
        summary_parts.append(stream_segment)
    summary_parts.append(f"branch={result.branch}")
    summary_parts.append(f"remote={result.remote}")
    if commit_segment is not None:
        summary_parts.append(commit_segment)
    console.print(
        "[green]site gh-deploy completed[/green] " + " ".join(summary_parts)
    )
    if result.pages_source.site_url:
        console.print(f"[cyan]pages url[/cyan] {result.pages_source.site_url}")
    if result.pages_source.status == "configured":
        console.print(f"[cyan]pages source[/cyan] {result.pages_source.detail}")
    elif result.pages_source.status == "failed":
        console.print(f"[yellow]pages source unchanged[/yellow] {result.pages_source.detail}")
    else:
        console.print(f"[yellow]pages source skipped[/yellow] {result.pages_source.detail}")
