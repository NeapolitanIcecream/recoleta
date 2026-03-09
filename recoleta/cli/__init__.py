from __future__ import annotations

from datetime import UTC, datetime
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
from recoleta.cli.analyze import run_analyze_command
from recoleta.cli.db import run_db_clear_command, run_db_reset_command
from recoleta.cli.ingest import run_ingest_command
from recoleta.cli.maintenance import (
    run_backup_command,
    run_doctor_command,
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
from recoleta.cli.run import run_pipeline_once as _run_pipeline_once_impl
from recoleta.cli.run import run_scheduler_command
from recoleta.cli.site import run_site_build_command, run_site_stage_command
from recoleta.cli.trends import run_trends_command, run_trends_week_command

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

app = typer.Typer(
    help="Recoleta research intelligence funnel CLI.", no_args_is_help=True
)
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True)
app.add_typer(db_app, name="db")
rag_app = typer.Typer(help="RAG utilities.", no_args_is_help=True)
app.add_typer(rag_app, name="rag")
site_app = typer.Typer(help="Static site utilities.", no_args_is_help=True)
app.add_typer(site_app, name="site")


@app.command()
def ingest() -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""
    run_ingest_command()


@app.command()
def analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    ),
) -> None:
    """Run LLM analysis for prepared items."""
    run_analyze_command(limit=limit)


@app.command()
def publish(
    limit: int = typer.Option(
        50, min=1, help="Max number of analyzed items published."
    ),
) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""
    run_publish_command(limit=limit)


@app.command()
def trends(
    granularity: str = typer.Option(
        "day",
        "--granularity",
        help="Trend granularity. Allowed: day, week, month.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for trend generation. Defaults to LLM_MODEL.",
    ),
    backfill: bool = typer.Option(
        False,
        "--backfill/--no-backfill",
        help="Backfill missing lower-granularity trends before generating week/month trends.",
    ),
    backfill_mode: str = typer.Option(
        "missing",
        "--backfill-mode",
        help="Backfill policy. Allowed: missing, all.",
    ),
    debug_pdf: bool = typer.Option(
        False,
        "--debug-pdf/--no-debug-pdf",
        help="Export PDF render intermediates and page previews beside the trend PDF.",
    ),
) -> None:
    """Generate trends for a period (day/week/month)."""
    run_trends_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        backfill=backfill,
        backfill_mode=backfill_mode,
        debug_pdf=debug_pdf,
    )


@app.command("trends-week")
def trends_week(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for trend generation. Defaults to LLM_MODEL.",
    ),
    backfill_mode: str = typer.Option(
        "missing",
        "--backfill-mode",
        help="Backfill policy. Allowed: missing, all.",
    ),
    debug_pdf: bool = typer.Option(
        False,
        "--debug-pdf/--no-debug-pdf",
        help="Export PDF render intermediates and page previews beside the trend PDF.",
    ),
) -> None:
    """Generate weekly trends and backfill missing daily trends."""
    run_trends_week_command(
        anchor_date=anchor_date,
        model=model,
        backfill_mode=backfill_mode,
        debug_pdf=debug_pdf,
    )


@site_app.command("build")
def site_build(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Destination directory for the exported static site. Defaults to MARKDOWN_OUTPUT_DIR/site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally export only the latest N trend notes.",
    ),
) -> None:
    """Build a static website from trend markdown notes."""
    run_site_build_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
    )


@site_app.command("stage")
def site_stage(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Repo-local directory to mirror trend markdown notes for deployment. Defaults to ./site-content/Trends, or ./site-content in topic-stream mode.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally stage only the latest N trend notes.",
    ),
) -> None:
    """Stage trend markdown notes into a repo-local directory for deployment."""
    run_site_stage_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
    )


@rag_app.command("sync-vectors")
def rag_sync_vectors(
    doc_type: str = typer.Option(
        "item",
        "--doc-type",
        help="Corpus doc_type for summary vector sync. Allowed: item, trend.",
    ),
    period_start: str = typer.Option(
        ...,
        "--period-start",
        help="Inclusive start time (ISO 8601, UTC recommended).",
    ),
    period_end: str = typer.Option(
        ...,
        "--period-end",
        help="Exclusive end time (ISO 8601, UTC recommended).",
    ),
    page_size: int = typer.Option(
        500, "--page-size", min=1, max=5000, help="SQLite paging size per batch."
    ),
) -> None:
    """Sync/rebuild summary vectors from SQLite corpus into LanceDB."""
    run_rag_sync_vectors_command(
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        page_size=page_size,
    )


@rag_app.command("build-index")
def rag_build_index(
    vector: bool = typer.Option(
        True, "--vector/--no-vector", help="Build a vector index (ANN)."
    ),
    scalar: bool = typer.Option(
        True,
        "--scalar/--no-scalar",
        help="Build scalar indices for filter columns.",
    ),
    vector_index_type: str = typer.Option(
        "IVF_HNSW_SQ",
        "--vector-index-type",
        help="Vector index type. Examples: IVF_FLAT, IVF_SQ, IVF_HNSW_SQ, IVF_PQ (requires enough rows).",
    ),
    vector_metric: str = typer.Option(
        "cosine",
        "--vector-metric",
        help="Vector distance metric. Examples: cosine, l2, dot.",
    ),
    vector_num_partitions: int | None = typer.Option(
        None,
        "--vector-num-partitions",
        min=1,
        help="Optional IVF partition count. If omitted, LanceDB chooses defaults.",
    ),
    vector_num_sub_vectors: int | None = typer.Option(
        None,
        "--vector-num-sub-vectors",
        min=1,
        help="Optional PQ sub-vector count (PQ variants only).",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Exit non-zero if any index build fails.",
    ),
) -> None:
    """Build/rebuild indices for the current embedding table in LanceDB."""
    run_rag_build_index_command(
        vector=vector,
        scalar=scalar,
        vector_index_type=vector_index_type,
        vector_metric=vector_metric,
        vector_num_partitions=vector_num_partitions,
        vector_num_sub_vectors=vector_num_sub_vectors,
        strict=strict,
    )


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


@db_app.command("clear")
def db_clear(
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
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm deletion without prompting.",
    ),
) -> None:
    """Delete the configured SQLite DB file (and sidecar files) for a clean slate."""
    run_db_clear_command(
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@app.command("gc")
def gc(
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
    prune_caches: bool = typer.Option(
        False,
        "--prune-caches",
        help="Also prune rebuildable caches such as chunk indices, inactive LanceDB tables, trend PDFs, and managed site output.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Report what would be deleted without mutating the workspace.",
    ),
) -> None:
    """Prune expired debug material and operational history."""
    run_gc_command(
        db_path=db_path,
        config_path=config_path,
        prune_caches=prune_caches,
        dry_run=dry_run,
    )


@app.command("vacuum")
def vacuum(
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
    """Run SQLite VACUUM on the configured database."""
    run_vacuum_command(db_path=db_path, config_path=config_path)


@app.command("backup")
def backup(
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
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Directory where timestamped backup bundles should be created. Defaults to <db-dir>/backups.",
    ),
) -> None:
    """Create a DB-scoped backup bundle with manifest metadata."""
    run_backup_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
    )


@app.command("restore")
def restore(
    bundle: Path = typer.Option(
        ...,
        "--bundle",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to a backup bundle directory created by `recoleta backup`.",
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
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm replacing the target DB.",
    ),
) -> None:
    """Restore the SQLite DB from a backup bundle."""
    run_restore_command(
        bundle=bundle,
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@app.command("stats")
def stats(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
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
    """Summarize read-only workspace operational state."""
    run_stats_command(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@app.command("doctor")
def doctor(
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
    """Run read-only diagnostics for the current workspace."""
    run_doctor_command(
        healthcheck=healthcheck,
        db_path=db_path,
        config_path=config_path,
        max_success_age_minutes=max_success_age_minutes,
    )


@db_app.command("reset")
def db_reset(
    db_path: Path | None = typer.Option(
        None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."
    ),
    config_path: Path | None = typer.Option(
        None, "--config", help="Path to config file used to resolve recoleta_db_path."
    ),
    trends_only: bool = typer.Option(
        False,
        "--trends-only",
        help="Only reset trend-related documents/chunks (keeps items, analyses, contents).",
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Confirm deletion without prompting."
    ),
) -> None:
    """Reset the SQLite DB (full reset) or only trend-related content."""
    run_db_reset_command(
        db_path=db_path,
        config_path=config_path,
        trends_only=trends_only,
        yes=yes,
    )


@app.command("run")
def run_scheduler(
    once: bool = typer.Option(
        False,
        "--once",
        help="Run ingest/analyze/publish once and exit (no scheduler).",
    ),
    analyze_limit: int | None = typer.Option(
        None,
        "--analyze-limit",
        min=1,
        help="Max number of items analyzed in the one-off run. Defaults to ANALYZE_LIMIT.",
    ),
    publish_limit: int = typer.Option(
        50,
        "--publish-limit",
        min=1,
        help="Max number of analyzed items published in the one-off run.",
    ),
) -> None:
    """Run periodic ingest/analyze/publish jobs with APScheduler (or run once)."""
    run_scheduler_command(
        once=once,
        analyze_limit=analyze_limit,
        publish_limit=publish_limit,
    )


def _run_pipeline_once(*, analyze_limit: int | None, publish_limit: int) -> None:
    """Run prepare -> analyze -> publish once under one run_id."""
    _run_pipeline_once_impl(
        analyze_limit=analyze_limit,
        publish_limit=publish_limit,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
