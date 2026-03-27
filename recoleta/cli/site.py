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
    default_language_code: str | None = None,
    json_output: bool = False,
    command_name: str = "site build",
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
        resolved_input_dir = settings.markdown_output_dir / "Trends"
    if resolved_output_dir is None:
        assert settings is not None
        resolved_output_dir = settings.markdown_output_dir / "site"
    resolved_default_language_code = str(default_language_code or "").strip() or None
    if (
        resolved_default_language_code is None
        and settings is not None
        and getattr(settings, "localization", None) is not None
    ):
        configured_default = getattr(
            getattr(settings, "localization", None),
            "site_default_language_code",
            None,
        )
        resolved_default_language_code = str(configured_default or "").strip() or None
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        cli._maybe_acquire_workspace_lease_for_settings(
            settings=settings,
            console=console,
            command=command_name,
            log_module="cli.site.build",
        )
    )
    try:
        export_kwargs: dict[str, object] = {
            "input_dir": resolved_input_dir,
            "output_dir": resolved_output_dir,
            "limit": limit,
        }
        if resolved_default_language_code is not None:
            export_kwargs["default_language_code"] = resolved_default_language_code
        manifest_path = export_trend_static_site(
            **export_kwargs,
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
    if json_output:
        cli._emit_json(
            {
                "status": "ok",
                "command": command_name,
                "input_dir": str(resolved_input_dir),
                "output_dir": str(resolved_output_dir),
                "manifest_path": str(manifest_path),
                "default_language_code": resolved_default_language_code,
                "manifest": manifest,
            }
        )
        return
    segments = [f"trends={manifest['trends_total']}"]
    if int(manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={manifest['ideas_total']}")
    segments.append(f"topics={manifest['topics_total']}")
    if int(manifest.get("streams_total") or 0) > 1:
        segments.append(f"streams={manifest['streams_total']}")
    segments.append(f"output={resolved_output_dir}")
    console.print(
        f"[green]{command_name} completed[/green] " + " ".join(segments)
    )


def run_site_stage_command(
    *,
    input_dir: Path | None,
    output_dir: Path | None,
    limit: int | None,
    default_language_code: str | None = None,
    json_output: bool = False,
    command_name: str = "site stage",
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
        resolved_input_dir = settings.markdown_output_dir / "Trends"
    if resolved_output_dir is None:
        resolved_output_dir = (Path.cwd() / "site-content" / "Trends").resolve()
    resolved_default_language_code = str(default_language_code or "").strip() or None
    if (
        resolved_default_language_code is None
        and settings is not None
        and getattr(settings, "localization", None) is not None
    ):
        configured_default = getattr(
            getattr(settings, "localization", None),
            "site_default_language_code",
            None,
        )
        resolved_default_language_code = str(configured_default or "").strip() or None
    console = (
        console_cls(stderr=settings.log_json) if settings is not None else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        cli._maybe_acquire_workspace_lease_for_settings(
            settings=settings,
            console=console,
            command=command_name,
            log_module="cli.site.stage",
        )
    )
    try:
        stage_kwargs: dict[str, object] = {
            "input_dir": resolved_input_dir,
            "output_dir": resolved_output_dir,
            "limit": limit,
        }
        if resolved_default_language_code is not None:
            stage_kwargs["default_language_code"] = resolved_default_language_code
        manifest_path = stage_trend_site_source(**stage_kwargs)
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
    if json_output:
        cli._emit_json(
            {
                "status": "ok",
                "command": command_name,
                "input_dir": str(resolved_input_dir),
                "output_dir": str(resolved_output_dir),
                "manifest_path": str(manifest_path),
                "default_language_code": resolved_default_language_code,
                "manifest": manifest,
            }
        )
        return
    segments = [f"trends={manifest['trends_total']}"]
    if int(manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={manifest['ideas_total']}")
    segments.append(f"pdfs={manifest['pdf_total']}")
    if int(manifest.get("streams_total") or 0) > 1:
        segments.append(f"streams={manifest['streams_total']}")
    segments.append(f"output={resolved_output_dir}")
    console.print(
        f"[green]{command_name} completed[/green] " + " ".join(segments)
    )


def run_site_serve_command(
    *,
    input_dir: Path | None,
    output_dir: Path | None,
    limit: int | None,
    host: str,
    port: int,
    build: bool,
    default_language_code: str | None = None,
    command_name: str = "site serve",
    build_command_name: str = "site build",
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
            default_language_code=default_language_code,
            command_name=build_command_name,
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
                f"[green]{command_name} ready[/green] "
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
