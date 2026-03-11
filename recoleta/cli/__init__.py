from __future__ import annotations

from datetime import UTC, datetime
import inspect
import json
import os
from pathlib import Path
import shutil
import socket
from typing import Any
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
    _has_explicit_topic_streams as _has_explicit_topic_streams,
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
        _app_runtime._RUNTIME_SYMBOLS = None


def _runtime_symbols() -> dict[str, Any]:
    return _runtime_symbols_impl()


def _build_settings(
    *,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> Any:
    _sync_cli_runtime_state(clear_runtime_symbols=True)
    return _build_settings_impl(config_path=config_path, db_path=db_path)


def _build_runtime(
    *,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> tuple[Any, Any, Any]:
    _sync_cli_runtime_state(clear_runtime_symbols=True)
    return _build_runtime_impl(config_path=config_path, db_path=db_path)


def _begin_managed_run(
    *,
    command: str,
    log_module: str,
) -> tuple[Any, Any, Any, Any, str, str, Any, _LeaseHeartbeatMonitor]:
    _sync_cli_runtime_state()
    return _begin_managed_run_impl(command=command, log_module=log_module)


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


def _resolve_db_path(*, db_path: Path | None, config_path: Path | None) -> Path:
    if isinstance(db_path, Path):
        normalized = db_path.expanduser().resolve()
        if str(normalized).strip():
            return normalized

    env_path = str(importlib.import_module("os").getenv("RECOLETA_DB_PATH", "")).strip()
    if env_path:
        return Path(env_path).expanduser().resolve()

    resolved_config_path: Path | None = None
    if isinstance(config_path, Path):
        resolved_config_path = config_path.expanduser().resolve()
    else:
        raw = str(
            importlib.import_module("os").getenv("RECOLETA_CONFIG_PATH", "")
        ).strip()
        if raw:
            resolved_config_path = Path(raw).expanduser().resolve()

    if resolved_config_path is None:
        raise ValueError(
            "Missing db path (pass --db-path or set RECOLETA_DB_PATH / RECOLETA_CONFIG_PATH)."
        )
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

    candidate = loaded.get("recoleta_db_path") or loaded.get("RECOLETA_DB_PATH")
    candidate_str = str(candidate or "").strip()
    if not candidate_str:
        raise ValueError(
            "Config does not define recoleta_db_path (or RECOLETA_DB_PATH)."
        )
    return Path(candidate_str).expanduser().resolve()


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
    dirs: set[Path] = {Path(settings.markdown_output_dir).expanduser().resolve()}
    runtime_builder = getattr(settings, "topic_stream_runtimes", None)
    if callable(runtime_builder):
        try:
            runtimes = runtime_builder()
        except Exception:
            runtimes = []
        if isinstance(runtimes, list):
            for runtime in runtimes:
                raw_dir = getattr(runtime, "markdown_output_dir", None)
                if raw_dir is None:
                    continue
                dirs.add(Path(raw_dir).expanduser().resolve())
    return dirs


def _prune_expired_pdf_debug_dirs(
    *,
    settings: Any,
    older_than: datetime | None = None,
    dry_run: bool = False,
) -> int:
    deleted = 0
    for markdown_root in _collect_markdown_output_dirs(settings):
        debug_root = markdown_root / "Trends" / ".pdf-debug"
        if not debug_root.exists() or not debug_root.is_dir():
            continue
        for child in list(debug_root.iterdir()):
            if older_than is not None:
                try:
                    modified_at = datetime.fromtimestamp(child.stat().st_mtime, tz=UTC)
                except Exception:
                    continue
                if modified_at >= older_than:
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
db_app = _app_module.db_app
rag_app = _app_module.rag_app
site_app = _app_module.site_app
main = _app_module.main

__all__ = [
    "app",
    "db_app",
    "rag_app",
    "site_app",
    "main",
    "typer",
]


if __name__ == "__main__":
    main()
