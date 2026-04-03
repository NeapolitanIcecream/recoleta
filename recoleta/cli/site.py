from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from loguru import logger

import recoleta.cli as cli
from recoleta.cli.site_support import (
    SitePathRequest,
    load_manifest,
    resolve_site_command_paths,
    site_manifest_payload,
    site_manifest_segments,
    site_output_dir_from_settings,
)


@dataclass(frozen=True, slots=True)
class SiteExportRequest:
    input_dir: Path | None
    output_dir: Path | None
    limit: int | None
    default_language_code: str | None
    item_export_scope: str
    command_name: str
    log_module: str
    exporter_attr: str
    default_output_dir: Path | None


@dataclass(frozen=True, slots=True)
class SiteServeRequest:
    input_dir: Path | None
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
class SiteExportResultContext:
    command_name: str
    paths: Any
    manifest_path: Path
    limit: int | None
    json_output: bool
    include_pdfs: bool


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


def run_site_build_command(**kwargs: Any) -> None:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "site build"))
    paths, manifest_path = _site_export_result(
        request=SiteExportRequest(
            input_dir=kwargs.get("input_dir"),
            output_dir=kwargs.get("output_dir"),
            limit=kwargs.get("limit"),
            default_language_code=kwargs.get("default_language_code"),
            item_export_scope=str(kwargs.get("item_export_scope", "linked")),
            command_name=command_name,
            log_module="cli.site.build",
            exporter_attr="export_trend_static_site",
            default_output_dir=(
                kwargs["output_dir"].expanduser().resolve()
                if kwargs.get("output_dir") is not None
                else None
            ),
        )
    )
    _emit_site_export_result(
        context=SiteExportResultContext(
            command_name=command_name,
            paths=paths,
            manifest_path=manifest_path,
            limit=kwargs.get("limit"),
            json_output=json_output,
            include_pdfs=False,
        )
    )


def run_site_stage_command(**kwargs: Any) -> None:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "site stage"))
    paths, manifest_path = _site_export_result(
        request=SiteExportRequest(
            input_dir=kwargs.get("input_dir"),
            output_dir=kwargs.get("output_dir"),
            limit=kwargs.get("limit"),
            default_language_code=kwargs.get("default_language_code"),
            item_export_scope=str(kwargs.get("item_export_scope", "linked")),
            command_name=command_name,
            log_module="cli.site.stage",
            exporter_attr="stage_trend_site_source",
            default_output_dir=(
                kwargs["output_dir"].expanduser().resolve()
                if kwargs.get("output_dir") is not None
                else (Path.cwd() / "site-content" / "Trends").resolve()
            ),
        )
    )
    _emit_site_export_result(
        context=SiteExportResultContext(
            command_name=command_name,
            paths=paths,
            manifest_path=manifest_path,
            limit=kwargs.get("limit"),
            json_output=json_output,
            include_pdfs=True,
        )
    )


def run_site_serve_command(**kwargs: Any) -> None:
    request = SiteServeRequest(
        input_dir=kwargs.get("input_dir"),
        output_dir=kwargs.get("output_dir"),
        limit=kwargs.get("limit"),
        host=str(kwargs.get("host", "127.0.0.1")),
        port=int(kwargs.get("port", 8000)),
        build=bool(kwargs.get("build", False)),
        default_language_code=kwargs.get("default_language_code"),
        item_export_scope=str(kwargs.get("item_export_scope", "linked")),
        command_name=str(kwargs.get("command_name", "site serve")),
        build_command_name=str(kwargs.get("build_command_name", "site build")),
    )
    resolved_output_dir, settings = _resolve_site_serve_output(request)
    if request.build:
        run_site_build_command(
            input_dir=request.input_dir,
            output_dir=resolved_output_dir,
            limit=request.limit,
            default_language_code=request.default_language_code,
            item_export_scope=request.item_export_scope,
            command_name=request.build_command_name,
        )
    _serve_site_directory(
        output_dir=resolved_output_dir,
        settings=settings,
        request=request,
    )


def _site_export_result(*, request: SiteExportRequest) -> tuple[Any, Path]:
    settings = (
        cli._build_settings()
        if request.input_dir is None or request.output_dir is None
        else None
    )
    assert request.default_output_dir is not None or settings is not None
    paths = resolve_site_command_paths(
        request=SitePathRequest(
            input_dir=request.input_dir,
            output_dir=request.output_dir,
            default_language_code=request.default_language_code,
            item_export_scope=request.item_export_scope,
            settings=settings,
            default_output_dir=(
                request.default_output_dir or site_output_dir_from_settings(settings)
            ),
        )
    )
    console = _site_console(settings=settings)
    lease = cli._maybe_acquire_workspace_lease_for_settings(
        settings=settings,
        console=console,
        command=request.command_name,
        log_module=request.log_module,
    )
    try:
        manifest_path = _run_site_exporter(
            exporter_attr=request.exporter_attr,
            paths=paths,
            limit=request.limit,
        )
        heartbeat_monitor = lease[3]
        if heartbeat_monitor is not None:
            heartbeat_monitor.raise_if_failed()
        return paths, manifest_path
    finally:
        _cleanup_site_lease(lease)


def _run_site_exporter(*, exporter_attr: str, paths: Any, limit: int | None) -> Path:
    exporter = cli._import_symbol("recoleta.site", attr_name=exporter_attr)
    export_kwargs: dict[str, object] = {
        "input_dir": paths.input_dir,
        "output_dir": paths.output_dir,
        "limit": limit,
    }
    if paths.default_language_code is not None:
        export_kwargs["default_language_code"] = paths.default_language_code
    if paths.item_export_scope != "linked":
        export_kwargs["item_export_scope"] = paths.item_export_scope
    return exporter(**export_kwargs)


def _emit_site_export_result(*, context: SiteExportResultContext) -> None:
    manifest = load_manifest(context.manifest_path)
    if context.json_output:
        cli._emit_json(
            site_manifest_payload(
                command_name=context.command_name,
                paths=context.paths,
                limit=context.limit,
                manifest_path=context.manifest_path,
                manifest=manifest,
            )
        )
        return
    console = _site_console(settings=context.paths.settings)
    console.print(
        f"[green]{context.command_name} completed[/green] "
        + _site_manifest_summary(
            manifest=manifest,
            output_dir=context.paths.output_dir,
            include_pdfs=context.include_pdfs,
        )
    )


def _site_manifest_summary(
    *,
    manifest: dict[str, Any],
    output_dir: Path,
    include_pdfs: bool,
) -> str:
    return " ".join(
        site_manifest_segments(
            manifest=manifest,
            output_dir=output_dir,
            include_pdfs=include_pdfs,
        )
    )


def _resolve_site_serve_output(request: SiteServeRequest) -> tuple[Path, Any | None]:
    resolved_output_dir = (
        request.output_dir.expanduser().resolve() if request.output_dir is not None else None
    )
    settings = (
        cli._build_settings()
        if resolved_output_dir is None or (request.build and request.input_dir is None)
        else None
    )
    return (
        resolved_output_dir if resolved_output_dir is not None else site_output_dir_from_settings(settings),
        settings,
    )


def _serve_site_directory(
    *,
    output_dir: Path,
    settings: Any | None,
    request: SiteServeRequest,
) -> None:
    if not output_dir.exists() or not output_dir.is_dir():
        raise ValueError(f"Static site output directory must exist before serving: {output_dir}")
    console = _site_console(settings=settings)
    log = logger.bind(module="cli.site.serve", host=request.host, port=request.port)
    try:
        with _create_site_server(
            directory=output_dir,
            host=request.host,
            port=request.port,
        ) as server:
            served_host = str(server.server_address[0])
            served_port = int(server.server_address[1])
            log.info("Site preview server started")
            console.print(
                f"[green]{request.command_name} ready[/green] "
                f"url=http://{served_host}:{served_port} "
                f"output={output_dir}"
            )
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                log.info("Site preview server stopped")
    except OSError as exc:
        log.warning("site preview server failed error={}", str(exc))
        raise


def _site_console(*, settings: Any | None) -> Any:
    return cli._runtime_symbols()["Console"](
        stderr=bool(getattr(settings, "log_json", False)) if settings is not None else False
    )


def _cleanup_site_lease(lease: tuple[Any | None, str | None, Any | None, Any | None]) -> None:
    repository, owner_token, log, heartbeat_monitor = lease
    if (
        repository is not None
        and owner_token is not None
        and log is not None
        and heartbeat_monitor is not None
    ):
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )
