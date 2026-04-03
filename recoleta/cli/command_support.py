from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, NoReturn

import recoleta.cli as cli


@dataclass(slots=True)
class CommandRuntime:
    resolved_db_path: Path
    repository: Any
    settings: Any | None
    console: Any


@dataclass(slots=True)
class ManagedRunSession:
    run_id: str
    owner_token: str
    log: Any
    heartbeat_monitor: Any


@dataclass(frozen=True, slots=True)
class RuntimeLoadRequest:
    db_path: Path | None
    config_path: Path | None
    command_name: str
    require_settings: bool
    init_schema: bool
    exit_code: int = 2


def build_console(*, settings: Any | None = None) -> Any:
    console_cls = cli._runtime_symbols()["Console"]
    if settings is None:
        return console_cls()
    return console_cls(stderr=bool(getattr(settings, "log_json", False)))


def resolve_db_path_or_exit(
    *,
    request: RuntimeLoadRequest,
    console: Any,
    json_output: bool = False,
) -> Path:
    try:
        return cli._resolve_db_path(
            db_path=request.db_path,
            config_path=request.config_path,
        )
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        emit_command_error(
            command_name=request.command_name,
            message=message,
            console=console,
            json_output=json_output,
            exit_code=request.exit_code,
        )


def load_settings_or_exit(
    *,
    db_path: Path | None,
    request: RuntimeLoadRequest,
    console: Any,
    json_output: bool = False,
) -> Any:
    try:
        return cli._build_settings(
            config_path=request.config_path,
            db_path=db_path,
        )
    except Exception as exc:  # noqa: BLE001
        message = f"settings load failed: {exc}"
        emit_command_error(
            command_name=request.command_name,
            message=message,
            console=console,
            json_output=json_output,
            exit_code=request.exit_code,
        )


def maybe_load_settings(
    *,
    db_path_option: Path | None,
    config_path_option: Path | None,
    resolved_db_path: Path,
) -> Any | None:
    return cli._maybe_load_settings(
        db_path_option=db_path_option,
        config_path_option=config_path_option,
        resolved_db_path=resolved_db_path,
    )


def build_repository(*, db_path: Path, init_schema: bool = False) -> Any:
    repository = cli._build_repository_for_db_path(db_path=db_path)
    if init_schema:
        repository.init_schema()
    return repository


def load_runtime(
    *,
    request: RuntimeLoadRequest,
) -> CommandRuntime:
    console = build_console()
    resolved_db_path = resolve_db_path_or_exit(
        request=request,
        console=console,
    )
    settings = (
        load_settings_or_exit(
            db_path=resolved_db_path,
            request=request,
            console=console,
        )
        if request.require_settings
        else maybe_load_settings(
            db_path_option=request.db_path,
            config_path_option=request.config_path,
            resolved_db_path=resolved_db_path,
        )
    )
    console = build_console(settings=settings)
    repository = build_repository(
        db_path=resolved_db_path,
        init_schema=request.init_schema,
    )
    return CommandRuntime(
        resolved_db_path=resolved_db_path,
        repository=repository,
        settings=settings,
        console=console,
    )

@contextmanager
def managed_run_for_settings(
    *,
    settings: Any,
    repository: Any,
    console: Any,
    command: str,
    log_module: str,
) -> Iterator[ManagedRunSession]:
    run_id, owner_token, log, heartbeat_monitor = cli._begin_managed_run_for_settings(
        settings=settings,
        repository=repository,
        console=console,
        command=command,
        log_module=log_module,
    )
    try:
        yield ManagedRunSession(
            run_id=run_id,
            owner_token=owner_token,
            log=log,
            heartbeat_monitor=heartbeat_monitor,
        )
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def finish_run_safely(
    *,
    repository: Any,
    run_id: str,
    success: bool,
    log: Any,
    message: str,
) -> None:
    try:
        repository.finish_run(run_id, success=success)
    except Exception:
        log.exception(message)


def load_billing_metrics(
    *,
    repository: Any,
    run_id: str,
    log: Any,
    warning_message: str,
) -> list[Any]:
    try:
        return repository.list_metrics(run_id=run_id)
    except Exception as exc:  # noqa: BLE001
        log.warning(
            warning_message + " error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return []

def emit_command_error(
    *,
    command_name: str,
    message: str,
    console: Any,
    json_output: bool,
    exit_code: int,
) -> NoReturn:
    if json_output:
        cli._emit_json({"status": "error", "error": message})
    else:
        console.print(f"[red]{command_name} failed[/red] {message}")
    raise cli.typer.Exit(code=exit_code)
