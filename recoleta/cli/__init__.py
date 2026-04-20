from __future__ import annotations

from datetime import UTC, datetime
import inspect
import json
import os
from pathlib import Path
import shutil
import socket
from typing import Any, NoReturn
import importlib
from uuid import uuid4

from recoleta.app import runtime as _app_runtime
from recoleta.app.runtime import (
    _LeaseHeartbeatMonitor,
    _RUN_HEARTBEAT_INTERVAL_SECONDS,
    _WORKSPACE_LEASE_TIMEOUT_SECONDS,
    _cleanup_managed_run as _cleanup_managed_run,
    _cleanup_workspace_lease as _cleanup_workspace_lease,
    _graceful_shutdown_signals as _graceful_shutdown_signals,
    _import_symbol,
    _interrupt_exit_code as _interrupt_exit_code,
    _interrupt_signal_name as _interrupt_signal_name,
    _parse_anchor_date_option as _parse_anchor_date_option,
    _print_billing_report as _print_billing_report,
    _print_ingest_html_document_summary as _print_ingest_html_document_summary,
    _raise_typer_exit_for_interrupt as _raise_typer_exit_for_interrupt,
    _raise_typer_exit_for_workspace_lock,
    typer,
)

_GC_DEBUG_RETENTION_DAYS = 14
_GC_OPERATIONAL_RETENTION_DAYS = 60

_runtime_symbols_impl = _app_runtime._runtime_symbols
_build_settings_impl = _app_runtime._build_settings
_build_runtime_impl = _app_runtime._build_runtime
_begin_managed_run_impl = _app_runtime._begin_managed_run
_execute_stage_impl = _app_runtime._execute_stage


def _sync_cli_runtime_state(*, clear_runtime_symbols: bool = False) -> None:
    _app_runtime._build_settings = globals()["_build_settings"]
    _app_runtime._build_runtime = globals()["_build_runtime"]
    _app_runtime._begin_managed_run = globals()["_begin_managed_run"]
    _app_runtime._cleanup_managed_run = globals()["_cleanup_managed_run"]
    _app_runtime._cleanup_workspace_lease = globals()["_cleanup_workspace_lease"]
    _app_runtime._raise_typer_exit_for_interrupt = globals()[
        "_raise_typer_exit_for_interrupt"
    ]
    _app_runtime._raise_typer_exit_for_workspace_lock = globals()[
        "_raise_typer_exit_for_workspace_lock"
    ]
    _app_runtime._WORKSPACE_LEASE_TIMEOUT_SECONDS = globals()[
        "_WORKSPACE_LEASE_TIMEOUT_SECONDS"
    ]
    _app_runtime._RUN_HEARTBEAT_INTERVAL_SECONDS = globals()[
        "_RUN_HEARTBEAT_INTERVAL_SECONDS"
    ]
    if clear_runtime_symbols:
        _clear_runtime_symbol_cache()


def _clear_runtime_symbol_cache() -> None:
    setattr(_app_runtime, "_RUNTIME_SYMBOLS", None)


def _runtime_symbols() -> dict[str, Any]:
    return _runtime_symbols_impl()


def _raise_typer_exit_for_invalid_settings(exc: ValueError) -> NoReturn:
    typer.echo(str(exc))
    raise typer.Exit(code=2) from None


def _build_settings(
    *,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> Any:
    _sync_cli_runtime_state(clear_runtime_symbols=True)
    try:
        return _build_settings_impl(config_path=config_path, db_path=db_path)
    except ValueError as exc:
        _raise_typer_exit_for_invalid_settings(exc)


def _build_runtime(
    *,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> tuple[Any, Any, Any]:
    _sync_cli_runtime_state(clear_runtime_symbols=True)
    try:
        return _build_runtime_impl(config_path=config_path, db_path=db_path)
    except ValueError as exc:
        _raise_typer_exit_for_invalid_settings(exc)


def _begin_managed_run(
    *,
    command: str,
    log_module: str,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> tuple[Any, Any, Any, Any, str, str, Any, _LeaseHeartbeatMonitor]:
    _sync_cli_runtime_state()
    begin_kwargs: dict[str, Any] = {
        "command": command,
        "log_module": log_module,
    }
    if config_path is not None:
        begin_kwargs["config_path"] = config_path
    if db_path is not None:
        begin_kwargs["db_path"] = db_path
    return _begin_managed_run_impl(**begin_kwargs)


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Any,
) -> tuple[Any, Any, str, Any]:
    _sync_cli_runtime_state()
    return _execute_stage_impl(stage_name=stage_name, stage_runner=stage_runner)


def _invoke_service_method(service: Any, method_name: str, /, **kwargs: Any) -> Any:
    method = getattr(service, method_name)
    try:
        signature = inspect.signature(method)
    except TypeError, ValueError:
        return method(**kwargs)

    accepts_var_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    if accepts_var_kwargs:
        return method(**kwargs)

    supported_kwargs = {
        name: value for name, value in kwargs.items() if name in signature.parameters
    }
    return method(**supported_kwargs)


def _update_run_context(repository: Any, *, run_id: str, **context: Any) -> None:
    method = getattr(repository, "update_run_context", None)
    if not callable(method):
        return
    kwargs = {
        "run_id": run_id,
        **{key: value for key, value in context.items() if value is not None},
    }
    if len(kwargs) <= 1:
        return
    try:
        signature = inspect.signature(method)
    except Exception:
        method(**kwargs)
        return
    accepts_var_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    supported_kwargs = (
        kwargs
        if accepts_var_kwargs
        else {
            key: value for key, value in kwargs.items() if key in signature.parameters
        }
    )
    if len(supported_kwargs) <= 1:
        return
    method(**supported_kwargs)


def _finish_run(
    repository: Any,
    *,
    run_id: str,
    success: bool,
    terminal_state: str | None = None,
) -> None:
    method = getattr(repository, "finish_run", None)
    if not callable(method):
        return
    kwargs: dict[str, Any] = {
        "run_id": run_id,
        "success": success,
    }
    if terminal_state is not None:
        kwargs["terminal_state"] = terminal_state
    try:
        signature = inspect.signature(method)
    except Exception:
        method(**kwargs)
        return
    accepts_var_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    supported_kwargs = (
        kwargs
        if accepts_var_kwargs
        else {
            key: value for key, value in kwargs.items() if key in signature.parameters
        }
    )
    method(**supported_kwargs)


def _resolve_db_path(*, db_path: Path | None, config_path: Path | None) -> Path:
    if isinstance(db_path, Path):
        normalized = db_path.expanduser().resolve()
        if str(normalized).strip():
            return normalized

    env_path = _env_path("RECOLETA_DB_PATH")
    if env_path:
        return Path(env_path).expanduser().resolve()

    resolved_config_path = _resolved_config_path(config_path=config_path)
    if resolved_config_path is None:
        raise ValueError(
            "Missing db path (pass --db-path or set RECOLETA_DB_PATH / RECOLETA_CONFIG_PATH)."
        )
    loaded = _load_config_mapping(resolved_config_path)
    candidate_str = str(
        loaded.get("recoleta_db_path") or loaded.get("RECOLETA_DB_PATH") or ""
    ).strip()
    if not candidate_str:
        raise ValueError(
            "Config does not define recoleta_db_path (or RECOLETA_DB_PATH)."
        )
    return Path(candidate_str).expanduser().resolve()


def _env_path(name: str) -> str:
    return str(importlib.import_module("os").getenv(name, "")).strip()


def _resolved_config_path(*, config_path: Path | None) -> Path | None:
    if isinstance(config_path, Path):
        return config_path.expanduser().resolve()
    raw = _env_path("RECOLETA_CONFIG_PATH")
    if raw:
        return Path(raw).expanduser().resolve()
    return None


def _load_config_mapping(resolved_config_path: Path) -> dict[str, Any]:
    if not resolved_config_path.exists():
        raise ValueError(f"Config path does not exist: {resolved_config_path}")
    if not resolved_config_path.is_file():
        raise ValueError(f"Config path must be a file: {resolved_config_path}")

    suffix = resolved_config_path.suffix.lower()
    raw_text = resolved_config_path.read_text(encoding="utf-8")
    if suffix == ".json":
        loaded = json.loads(raw_text)
    elif suffix in {".yaml", ".yml"}:
        yaml = _import_symbol("yaml")
        loaded = yaml.safe_load(raw_text)
    else:
        raise ValueError(
            f"Unsupported config file type: {resolved_config_path.suffix} (expected .yaml/.yml/.json)"
        )

    if not isinstance(loaded, dict):
        raise ValueError("Config file must contain a mapping/object at the top level")
    return loaded


def _build_repository_for_db_path(*, db_path: Path) -> Any:
    symbols = _runtime_symbols()
    repository_cls = symbols["Repository"]
    return repository_cls(db_path=db_path.expanduser().resolve())


def _acquire_workspace_lease_for_command(
    *,
    repository: Any,
    console: Any,
    command: str,
    log_module: str,
) -> tuple[str, Any, _LeaseHeartbeatMonitor]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    workspace_lease_held_error = symbols["WorkspaceLeaseHeldError"]
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    owner_token = str(uuid4())
    lock_log = logger.bind(module=log_module, command=command)
    try:
        repository.acquire_workspace_lease(
            owner_token=owner_token,
            command=command,
            lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            hostname=socket.gethostname(),
            pid=os.getpid(),
        )
    except workspace_lease_held_error as exc:
        _raise_typer_exit_for_workspace_lock(
            console=console,
            log=lock_log,
            exc=exc,
        )
    heartbeat_monitor = _LeaseHeartbeatMonitor(
        repository=repository,
        run_id=None,
        owner_token=owner_token,
        lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
        interval_seconds=_RUN_HEARTBEAT_INTERVAL_SECONDS,
        log=logger.bind(module="cli.runtime.heartbeat", command=command),
        lease_lost_error_cls=workspace_lease_lost_error,
        thread_name=f"recoleta-lease-{command.replace(' ', '-')}",
    )
    heartbeat_monitor.start()
    return owner_token, lock_log, heartbeat_monitor


def _safe_fingerprint_for_settings(settings: Any) -> str:
    builder = getattr(settings, "safe_fingerprint", None)
    if callable(builder):
        try:
            return str(builder())
        except Exception:
            return ""
    return ""


def _begin_managed_run_for_settings(
    *,
    settings: Any,
    repository: Any,
    console: Any,
    command: str,
    log_module: str,
) -> tuple[str, str, Any, _LeaseHeartbeatMonitor]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    workspace_lease_held_error = symbols["WorkspaceLeaseHeldError"]
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    run_id = str(uuid4())
    owner_token = str(uuid4())
    lock_log = logger.bind(
        module="cli.runtime.lock",
        command=command,
        requested_run_id=run_id,
    )
    try:
        repository.acquire_workspace_lease(
            run_id=run_id,
            command=command,
            owner_token=owner_token,
            lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            hostname=socket.gethostname(),
            pid=os.getpid(),
        )
    except workspace_lease_held_error as exc:
        _raise_typer_exit_for_workspace_lock(
            console=console,
            log=lock_log,
            exc=exc,
        )

    try:
        recovered_total = repository.mark_stale_runs_failed(
            stale_after_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS
        )
        if int(recovered_total or 0) > 0:
            lock_log.warning(
                "Recovered stale runs recovered_total={}",
                int(recovered_total),
            )
        run = repository.create_run(
            config_fingerprint=_safe_fingerprint_for_settings(settings),
            run_id=run_id,
        )
        _update_run_context(repository, run_id=run.id, command=command)
        command_log = logger.bind(module=log_module, run_id=run.id)
        heartbeat_monitor = _LeaseHeartbeatMonitor(
            repository=repository,
            run_id=run.id,
            owner_token=owner_token,
            lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            interval_seconds=_RUN_HEARTBEAT_INTERVAL_SECONDS,
            log=logger.bind(
                module="cli.runtime.heartbeat", command=command, run_id=run.id
            ),
            lease_lost_error_cls=workspace_lease_lost_error,
            thread_name=f"recoleta-heartbeat-{run.id}",
        )
        heartbeat_monitor.start()
        return run.id, owner_token, command_log, heartbeat_monitor
    except Exception:
        try:
            repository.release_workspace_lease(owner_token=owner_token)
        except Exception:
            lock_log.exception("Workspace lease release failed during startup")
        raise


def _begin_observed_run_for_settings(
    *,
    settings: Any,
    repository: Any,
    command: str,
    log_module: str,
) -> tuple[str, Any]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    run = repository.create_run(
        config_fingerprint=_safe_fingerprint_for_settings(settings),
    )
    _update_run_context(repository, run_id=run.id, command=command)
    return run.id, logger.bind(module=log_module, run_id=run.id)


def _maybe_acquire_workspace_lease_for_settings(
    *,
    settings: Any | None,
    console: Any,
    command: str,
    log_module: str,
) -> tuple[Any | None, str | None, Any | None, _LeaseHeartbeatMonitor | None]:
    if settings is None:
        return None, None, None, None
    db_path = getattr(settings, "recoleta_db_path", None)
    if not isinstance(db_path, Path):
        return None, None, None, None
    repository = _build_repository_for_db_path(db_path=db_path)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = _acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command=command,
        log_module=log_module,
    )
    return repository, owner_token, log, heartbeat_monitor


def _should_attempt_settings_load(
    *,
    db_path_option: Path | None,
    config_path_option: Path | None,
) -> bool:
    if config_path_option is not None:
        return True
    if str(os.getenv("RECOLETA_CONFIG_PATH", "")).strip():
        return True
    return db_path_option is None


def _maybe_load_settings(
    *,
    db_path_option: Path | None,
    config_path_option: Path | None,
    resolved_db_path: Path,
) -> Any | None:
    if not _should_attempt_settings_load(
        db_path_option=db_path_option,
        config_path_option=config_path_option,
    ):
        return None
    return _build_settings(config_path=config_path_option, db_path=resolved_db_path)


def _is_accessible_path(path: Path) -> bool:
    candidate = path.expanduser().resolve()
    if candidate.exists():
        if candidate.is_dir():
            return os.access(candidate, os.R_OK | os.W_OK | os.X_OK)
        return os.access(candidate, os.R_OK | os.W_OK)
    parent = candidate.parent
    return parent.exists() and os.access(parent, os.R_OK | os.W_OK | os.X_OK)


def _normalize_utc_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _isoformat_or_none(value: Any) -> str | None:
    if not isinstance(value, datetime):
        return None
    normalized = _normalize_utc_datetime(value)
    return normalized.isoformat() if normalized is not None else None


def _path_or_none(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, Path):
        return str(value)
    normalized = str(value).strip()
    return normalized or None


def _json_number(value: float | None) -> int | float | None:
    if value is None:
        return None
    normalized = float(value)
    if normalized.is_integer():
        return int(normalized)
    return normalized


def _emit_json(payload: dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _metrics_payload(
    metrics: list[Any],
) -> dict[str, dict[str, int | float | str | None]]:
    totals: dict[str, float] = {}
    units: dict[str, str | None] = {}
    for metric in metrics:
        name = str(getattr(metric, "name", "") or "").strip()
        if not name:
            continue
        raw_value = getattr(metric, "value", None)
        if not isinstance(raw_value, (int, float)):
            continue
        totals[name] = float(totals.get(name, 0.0)) + float(raw_value)
        raw_unit = getattr(metric, "unit", None)
        normalized_unit = str(raw_unit).strip() if raw_unit is not None else ""
        units[name] = normalized_unit or None
    return {
        name: {
            "value": _json_number(total),
            "unit": units.get(name),
        }
        for name, total in sorted(totals.items())
    }


def _billing_summary_payload(metrics: list[Any]) -> dict[str, Any] | None:
    summarize_billing_metrics = _import_symbol(
        "recoleta.billing",
        attr_name="summarize_billing_metrics",
    )
    return summarize_billing_metrics(metrics)


def _path_size_bytes(path: Path) -> int | None:
    candidate = path.expanduser().resolve()
    if not candidate.exists():
        return 0
    try:
        if candidate.is_file():
            return int(candidate.stat().st_size)
    except OSError:
        return None

    total = 0
    try:
        for child in candidate.rglob("*"):
            try:
                if child.is_file():
                    total += int(child.stat().st_size)
            except OSError:
                return None
    except OSError:
        return None
    return total


def _workspace_bytes_from_settings(settings: Any) -> dict[str, int | None]:
    workspace_bytes: dict[str, int | None] = {
        "markdown_output_dir": _path_size_bytes(Path(settings.markdown_output_dir)),
        "artifacts_dir": None,
        "rag_lancedb_dir": _path_size_bytes(Path(settings.rag_lancedb_dir)),
    }
    artifacts_dir = getattr(settings, "artifacts_dir", None)
    if artifacts_dir is not None:
        workspace_bytes["artifacts_dir"] = _path_size_bytes(Path(artifacts_dir))
    return workspace_bytes


def _backup_output_dir_from_settings(settings: Any | None) -> Path | None:
    if settings is None:
        return None
    raw_path = getattr(settings, "backup_output_dir", None)
    if raw_path is None:
        return None
    return Path(raw_path).expanduser().resolve()


def _backup_output_dir_from_env() -> Path | None:
    raw_path = str(os.getenv("BACKUP_OUTPUT_DIR", "")).strip()
    if not raw_path:
        return None
    return Path(raw_path).expanduser().resolve()


def _resolve_backup_output_dir(
    *,
    resolved_db_path: Path,
    settings: Any | None = None,
    output_dir: Path | None = None,
) -> Path:
    if output_dir is not None:
        return output_dir.expanduser().resolve()
    configured = _backup_output_dir_from_settings(settings)
    if configured is not None:
        return configured
    configured_from_env = _backup_output_dir_from_env()
    if configured_from_env is not None:
        return configured_from_env
    return (resolved_db_path.parent / "backups").resolve()


def _delete_path_if_present(*, path: Path, dry_run: bool = False) -> bool:
    if not path.exists():
        return False
    if dry_run:
        return True
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def _collect_markdown_output_dirs(settings: Any) -> set[Path]:
    return {Path(settings.markdown_output_dir).expanduser().resolve()}


def _pdf_debug_root(markdown_root: Path) -> Path | None:
    debug_root = markdown_root / "Trends" / ".pdf-debug"
    if not debug_root.exists() or not debug_root.is_dir():
        return None
    return debug_root


def _is_expired_debug_child(*, child: Path, older_than: datetime | None) -> bool:
    if older_than is None:
        return True
    try:
        modified_at = datetime.fromtimestamp(child.stat().st_mtime, tz=UTC)
    except Exception:
        return False
    return modified_at < older_than


def _prune_expired_pdf_debug_dirs(
    *,
    settings: Any,
    older_than: datetime | None = None,
    dry_run: bool = False,
) -> int:
    deleted = 0
    for markdown_root in _collect_markdown_output_dirs(settings):
        debug_root = _pdf_debug_root(markdown_root)
        if debug_root is None:
            continue
        for child in list(debug_root.iterdir()):
            if not _is_expired_debug_child(child=child, older_than=older_than):
                continue
            if _delete_path_if_present(path=child, dry_run=dry_run):
                deleted += 1
    return deleted


def _prune_trend_pdfs(
    *,
    settings: Any,
    dry_run: bool = False,
) -> int:
    deleted = 0
    for markdown_root in _collect_markdown_output_dirs(settings):
        trends_dir = markdown_root / "Trends"
        if not trends_dir.exists() or not trends_dir.is_dir():
            continue
        for pdf_path in trends_dir.glob("*.pdf"):
            if _delete_path_if_present(path=pdf_path, dry_run=dry_run):
                deleted += 1
    return deleted


def _prune_managed_site_outputs(
    *,
    settings: Any,
    dry_run: bool = False,
) -> int:
    deleted = 0
    candidate_paths: set[Path] = {Path(settings.markdown_output_dir).resolve() / "site"}
    for markdown_root in _collect_markdown_output_dirs(settings):
        candidate_paths.add(markdown_root / "site")
    for path in candidate_paths:
        if _delete_path_if_present(path=path, dry_run=dry_run):
            deleted += 1
    return deleted


def _prune_inactive_lancedb_tables(
    *,
    settings: Any,
    dry_run: bool = False,
) -> int:
    lancedb_dir = Path(settings.rag_lancedb_dir).expanduser().resolve()
    if not lancedb_dir.exists():
        return 0

    from recoleta.rag.vector_store import embedding_table_name

    active_table = embedding_table_name(
        embedding_model=settings.trends_embedding_model,
        embedding_dimensions=settings.trends_embedding_dimensions,
    )

    import lancedb

    db = lancedb.connect(str(lancedb_dir))
    deleted = 0
    for table_name in list(db.list_tables(limit=10_000).tables or []):
        normalized = str(table_name or "").strip()
        if not normalized.startswith("chunk_vectors_"):
            continue
        if normalized == active_table:
            continue
        if not dry_run:
            try:
                db.drop_table(normalized)
            except Exception:
                continue
        deleted += 1
    return deleted


_app_module = importlib.import_module("recoleta.cli.app")
app = _app_module.app
run_app = _app_module.run_app
daemon_app = _app_module.daemon_app
inspect_app = _app_module.inspect_app
repair_app = _app_module.repair_app
stage_app = _app_module.stage_app
admin_app = _app_module.admin_app
db_app = _app_module.db_app
rag_app = _app_module.rag_app
site_app = _app_module.site_app
materialize_app = _app_module.materialize_app
runs_app = _app_module.runs_app
doctor_app = _app_module.doctor_app
main = _app_module.main

__all__ = [
    "app",
    "run_app",
    "daemon_app",
    "inspect_app",
    "repair_app",
    "stage_app",
    "admin_app",
    "db_app",
    "rag_app",
    "site_app",
    "materialize_app",
    "runs_app",
    "doctor_app",
    "main",
    "typer",
]


if __name__ == "__main__":
    main()
