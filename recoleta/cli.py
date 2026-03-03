from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, date, datetime
import importlib
import json
from pathlib import Path
from typing import Any


def _import_symbol(module_name: str, *, attr_name: str | None = None) -> Any:
    module = importlib.import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


typer = _import_symbol("typer")
_RUNTIME_SYMBOLS: dict[str, Any] | None = None

app = typer.Typer(
    help="Recoleta research intelligence funnel CLI.", no_args_is_help=True
)
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True)
app.add_typer(db_app, name="db")
rag_app = typer.Typer(help="RAG utilities.", no_args_is_help=True)
app.add_typer(rag_app, name="rag")


def _runtime_symbols() -> dict[str, Any]:
    global _RUNTIME_SYMBOLS
    if _RUNTIME_SYMBOLS is not None:
        return _RUNTIME_SYMBOLS

    _RUNTIME_SYMBOLS = {
        "logger": _import_symbol("loguru", attr_name="logger"),
        "Console": _import_symbol("rich.console", attr_name="Console"),
        "Settings": _import_symbol("recoleta.config", attr_name="Settings"),
        "configure_process_logging": _import_symbol(
            "recoleta.observability",
            attr_name="configure_process_logging",
        ),
        "Repository": _import_symbol("recoleta.storage", attr_name="Repository"),
    }
    return _RUNTIME_SYMBOLS


def _build_runtime() -> tuple[Any, Any, Any]:
    symbols = _runtime_symbols()
    settings_cls = symbols["Settings"]
    configure_process_logging = symbols["configure_process_logging"]
    repository_cls = symbols["Repository"]
    pipeline_service_cls = _import_symbol(
        "recoleta.pipeline", attr_name="PipelineService"
    )

    settings = settings_cls()  # pyright: ignore[reportCallIssue]
    configure_process_logging(level=settings.log_level, log_json=settings.log_json)
    repository = repository_cls(
        db_path=settings.recoleta_db_path,
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = pipeline_service_cls(settings=settings, repository=repository)
    return settings, repository, service


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Callable[[Any, str], Any],
) -> tuple[Any, Any]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]

    settings, repository, service = _build_runtime()
    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    stage_log = logger.bind(module=f"cli.{stage_name}", run_id=run.id)
    try:
        result = stage_runner(service, run.id)
        repository.finish_run(run.id, success=True)
        return settings, result
    except KeyboardInterrupt:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            stage_log.exception("Run finish failed during interrupt")
        stage_log.warning("Stage interrupted")
        raise typer.Exit(code=130) from None
    except Exception:
        repository.finish_run(run.id, success=False)
        stage_log.exception("Stage execution failed")
        raise


@app.command()
def ingest() -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="ingest",
        stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )


@app.command()
def analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    ),
) -> None:
    """Run LLM analysis for prepared items."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="analyze",
        stage_runner=lambda service, run_id: service.analyze(
            run_id=run_id, limit=limit
        ),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]analyze completed[/green] processed={result.processed} failed={result.failed}"
    )


@app.command()
def publish(
    limit: int = typer.Option(
        50, min=1, help="Max number of analyzed items published."
    ),
) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="publish",
        stage_runner=lambda service, run_id: service.publish(
            run_id=run_id, limit=limit
        ),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]publish completed[/green] sent={result.sent} skipped={result.skipped} failed={result.failed}"
    )
    if "markdown" in settings.publish_targets:
        console.print(f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}")
        console.print(
            f"[cyan]latest index[/cyan] {settings.markdown_output_dir / 'latest.md'}"
        )
    if (
        "obsidian" in settings.publish_targets
        and settings.obsidian_vault_path is not None
    ):
        console.print(
            f"[cyan]obsidian notes[/cyan] {settings.obsidian_vault_path / settings.obsidian_base_folder / 'Inbox'}"
        )


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
        help="Anchor date in UTC (YYYY-MM-DD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for trend generation. Defaults to LLM_MODEL.",
    ),
) -> None:
    """Generate trends for a period (day/week/month)."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    parsed_anchor: date | None = None
    if anchor_date is not None and str(anchor_date).strip():
        parsed_anchor = date.fromisoformat(str(anchor_date).strip())

    settings, result = _execute_stage(
        stage_name="trends",
        stage_runner=lambda service, run_id: service.trends(
            run_id=run_id,
            granularity=granularity,
            anchor_date=parsed_anchor,
            llm_model=model,
        ),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        "[green]trends completed[/green] "
        f"doc_id={result.doc_id} granularity={result.granularity} "
        f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
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

    symbols = _runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]

    settings, repository, _ = _build_runtime()
    console = console_cls(stderr=settings.log_json)

    try:
        start_dt = datetime.fromisoformat(str(period_start).strip())
        end_dt = datetime.fromisoformat(str(period_end).strip())
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]invalid datetime[/red] {exc}")
        raise typer.Exit(code=2) from exc
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=UTC)
    else:
        start_dt = start_dt.astimezone(UTC)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=UTC)
    else:
        end_dt = end_dt.astimezone(UTC)
    if end_dt <= start_dt:
        console.print(
            "[red]invalid datetime range[/red] period_end must be > period_start"
        )
        raise typer.Exit(code=2)

    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    log = logger.bind(module="cli.rag.sync_vectors", run_id=run.id)
    try:
        from recoleta.rag.sync import sync_summary_vectors_in_period
        from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

        store = LanceVectorStore(
            db_dir=settings.rag_lancedb_dir,
            table_name=embedding_table_name(
                embedding_model=settings.trends_embedding_model,
                embedding_dimensions=settings.trends_embedding_dimensions,
            ),
        )
        stats = sync_summary_vectors_in_period(
            repository=repository,
            vector_store=store,
            run_id=run.id,
            doc_type=str(doc_type).strip().lower(),
            period_start=start_dt,
            period_end=end_dt,
            embedding_model=settings.trends_embedding_model,
            embedding_dimensions=settings.trends_embedding_dimensions,
            max_batch_inputs=settings.trends_embedding_batch_max_inputs,
            max_batch_chars=settings.trends_embedding_batch_max_chars,
            embedding_failure_mode=getattr(
                settings, "trends_embedding_failure_mode", "continue"
            ),
            embedding_max_errors=int(
                getattr(settings, "trends_embedding_max_errors", 0) or 0
            ),
            page_size=page_size,
        )
        repository.finish_run(run.id, success=True)
        console.print(f"[green]rag sync completed[/green] stats={stats}")
    except KeyboardInterrupt:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        log.warning("RAG sync interrupted")
        raise typer.Exit(code=130) from None
    except Exception:
        repository.finish_run(run.id, success=False)
        log.exception("RAG sync failed")
        raise


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

    symbols = _runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]

    settings, repository, _ = _build_runtime()
    console = console_cls(stderr=settings.log_json)

    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    log = logger.bind(module="cli.rag.build_index", run_id=run.id)
    try:
        from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

        store = LanceVectorStore(
            db_dir=settings.rag_lancedb_dir,
            table_name=embedding_table_name(
                embedding_model=settings.trends_embedding_model,
                embedding_dimensions=settings.trends_embedding_dimensions,
            ),
        )
        stats = store.build_indices(
            build_vector_index=bool(vector),
            vector_index_type=str(vector_index_type),
            vector_metric=str(vector_metric),
            vector_num_partitions=vector_num_partitions,
            vector_num_sub_vectors=vector_num_sub_vectors,
            build_scalar_indices=bool(scalar),
            replace=True,
            strict=bool(strict),
        )
        errors = stats.get("errors") or []
        table_exists = bool(stats.get("table_exists"))

        if not table_exists:
            repository.finish_run(run.id, success=True)
            console.print(
                "[yellow]rag build-index skipped[/yellow] table not found (run `recoleta rag sync-vectors` first)"
            )
            return

        if strict and errors:
            repository.finish_run(run.id, success=False)
            console.print(f"[red]rag build-index failed[/red] stats={stats}")
            raise typer.Exit(code=1)

        repository.finish_run(run.id, success=True)
        if errors:
            console.print(
                f"[yellow]rag build-index completed with errors[/yellow] stats={stats}"
            )
        else:
            console.print(f"[green]rag build-index completed[/green] stats={stats}")
    except KeyboardInterrupt:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        log.warning("RAG build-index interrupted")
        raise typer.Exit(code=130) from None
    except typer.Exit:
        raise
    except Exception:
        repository.finish_run(run.id, success=False)
        log.exception("RAG build-index failed")
        raise


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

    if not yes:
        typer.echo("refusing to delete db without --yes")
        raise typer.Exit(code=2)

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()

    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    to_delete = [
        resolved,
        Path(f"{resolved}-wal"),
        Path(f"{resolved}-shm"),
        Path(f"{resolved}-journal"),
    ]
    deleted: list[str] = []
    for path in to_delete:
        try:
            if path.exists():
                path.unlink()
                deleted.append(str(path))
        except Exception as exc:  # noqa: BLE001
            logger.bind(module="cli.db.clear").warning(
                "db delete failed path={} error={}", str(path), str(exc)
            )
            console.print(f"[red]failed to delete[/red] {path}")
            raise typer.Exit(code=1) from exc

    if deleted:
        console.print(
            f"[green]db cleared[/green] deleted={len(deleted)} path={resolved}"
        )
    else:
        console.print(f"[green]db already empty[/green] path={resolved}")


@db_app.command("reset")
def db_reset(
    db_path: Path | None = typer.Option(
        None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."
    ),
    config_path: Path | None = typer.Option(
        None, "--config", help="Path to config file used to resolve recoleta_db_path."
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Confirm deletion without prompting."
    ),
) -> None:
    """Alias for `recoleta db clear`."""

    db_clear(db_path=db_path, config_path=config_path, yes=yes)


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

    symbols = _runtime_symbols()

    if once:
        _run_pipeline_once(
            analyze_limit=analyze_limit,
            publish_limit=publish_limit,
        )
        return

    console_cls = symbols["Console"]
    settings, _, _ = _build_runtime()
    console = console_cls(stderr=settings.log_json)

    blocking_scheduler_cls = _import_symbol(
        "apscheduler.schedulers.blocking",
        attr_name="BlockingScheduler",
    )
    scheduler = blocking_scheduler_cls(
        timezone="UTC",
        executors={"default": {"type": "threadpool", "max_workers": 1}},
        job_defaults={"coalesce": True, "max_instances": 1},
    )

    def run_ingest_job() -> None:
        _execute_stage(
            stage_name="ingest",
            stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
        )

    def run_analyze_job() -> None:
        _execute_stage(
            stage_name="analyze",
            stage_runner=lambda service, run_id: service.analyze(run_id=run_id),
        )

    def run_publish_job() -> None:
        _execute_stage(
            stage_name="publish",
            stage_runner=lambda service, run_id: service.publish(run_id=run_id),
        )

    scheduler.add_job(
        run_ingest_job,
        "interval",
        minutes=settings.ingest_interval_minutes,
        id="ingest",
        replace_existing=True,
    )
    scheduler.add_job(
        run_analyze_job,
        "interval",
        minutes=settings.analyze_interval_minutes,
        id="analyze",
        replace_existing=True,
    )
    scheduler.add_job(
        run_publish_job,
        "interval",
        minutes=settings.publish_interval_minutes,
        id="publish",
        replace_existing=True,
    )
    console.print("[cyan]scheduler started[/cyan]")
    scheduler.start()


def _run_pipeline_once(*, analyze_limit: int | None, publish_limit: int) -> None:
    """Run prepare -> analyze -> publish once under one run_id."""

    symbols = _runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]

    settings, repository, service = _build_runtime()
    console = console_cls(stderr=settings.log_json)
    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    log = logger.bind(module="cli.run.once", run_id=run.id)

    try:
        ingest_result = service.prepare(run_id=run.id)
        analyze_result = service.analyze(run_id=run.id, limit=analyze_limit)
        publish_result = service.publish(run_id=run.id, limit=publish_limit)
        repository.finish_run(run.id, success=True)
    except KeyboardInterrupt:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        log.warning("Run interrupted")
        raise typer.Exit(code=130) from None
    except Exception:
        repository.finish_run(run.id, success=False)
        log.exception("Run failed")
        raise

    console.print(
        "[green]run --once completed[/green] "
        f"ingest(inserted={ingest_result.inserted} updated={ingest_result.updated} failed={ingest_result.failed}) "
        f"analyze(processed={analyze_result.processed} failed={analyze_result.failed}) "
        f"publish(sent={publish_result.sent} skipped={publish_result.skipped} failed={publish_result.failed})"
    )
    if "markdown" in settings.publish_targets:
        console.print(f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}")
        console.print(
            f"[cyan]latest index[/cyan] {settings.markdown_output_dir / 'latest.md'}"
        )
    if (
        "obsidian" in settings.publish_targets
        and settings.obsidian_vault_path is not None
    ):
        console.print(
            f"[cyan]obsidian notes[/cyan] {settings.obsidian_vault_path / settings.obsidian_base_folder / 'Inbox'}"
        )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
