from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, date, datetime
import importlib
import json
from pathlib import Path
import signal
from typing import Any, NoReturn


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
site_app = typer.Typer(help="Static site utilities.", no_args_is_help=True)
app.add_typer(site_app, name="site")


def _runtime_symbols() -> dict[str, Any]:
    global _RUNTIME_SYMBOLS
    if _RUNTIME_SYMBOLS is not None:
        return _RUNTIME_SYMBOLS

    _RUNTIME_SYMBOLS = {
        "logger": _import_symbol("loguru", attr_name="logger"),
        "Console": _import_symbol("rich.console", attr_name="Console"),
        "build_billing_table": _import_symbol(
            "recoleta.billing", attr_name="build_billing_table"
        ),
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


def _build_settings() -> Any:
    symbols = _runtime_symbols()
    settings_cls = symbols["Settings"]
    configure_process_logging = symbols["configure_process_logging"]

    settings = settings_cls()  # pyright: ignore[reportCallIssue]
    configure_process_logging(level=settings.log_level, log_json=settings.log_json)
    return settings


def _has_explicit_topic_streams(settings: Any) -> bool:
    runtime_builder = getattr(settings, "topic_stream_runtimes", None)
    if not callable(runtime_builder):
        return False
    try:
        runtimes = runtime_builder()
    except Exception:
        return False
    if not isinstance(runtimes, list):
        return False
    return any(bool(getattr(stream, "explicit", False)) for stream in runtimes)


def _parse_anchor_date_option(value: str) -> date:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("date is required")
    if len(raw) == 8 and raw.isdigit():
        raw = f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return date.fromisoformat(raw)


def _print_billing_report(*, console: Any, repository: Any, run_id: str) -> None:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    build_billing_table = symbols["build_billing_table"]
    log = logger.bind(module="cli.billing", run_id=run_id)
    try:
        metrics = repository.list_metrics(run_id=run_id)
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Billing metrics load failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return
    try:
        table = build_billing_table(metrics=metrics, title="Billing report")
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Billing table render failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return
    if table is None:
        return
    console.print(table)


class _SignalKeyboardInterrupt(KeyboardInterrupt):
    def __init__(self, signum: int) -> None:
        super().__init__()
        self.signum = int(signum)


def _interrupt_signal_name(exc: KeyboardInterrupt) -> str:
    signum = getattr(exc, "signum", None)
    if isinstance(signum, int) and signum > 0:
        try:
            return signal.Signals(signum).name
        except ValueError:
            return f"SIG{signum}"
    return "SIGINT"


def _interrupt_exit_code(exc: KeyboardInterrupt) -> int:
    signum = getattr(exc, "signum", None)
    if isinstance(signum, int) and signum > 0:
        return 128 + signum
    return 130


@contextmanager
def _graceful_shutdown_signals() -> Iterator[None]:
    try:
        previous_sigterm = signal.getsignal(signal.SIGTERM)
    except (AttributeError, ValueError):
        yield
        return

    def _handle_sigterm(signum: int, _: Any) -> None:
        raise _SignalKeyboardInterrupt(signum)

    try:
        signal.signal(signal.SIGTERM, _handle_sigterm)
    except ValueError:
        yield
        return

    try:
        yield
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm)


def _raise_typer_exit_for_interrupt(
    *, log: Any, message: str, exc: KeyboardInterrupt
) -> NoReturn:
    exit_code = _interrupt_exit_code(exc)
    log.warning(
        "{} signal={} exit_code={}",
        message,
        _interrupt_signal_name(exc),
        exit_code,
    )
    raise typer.Exit(code=exit_code) from None


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Callable[[Any, str], Any],
) -> tuple[Any, Any, str, Any]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]

    settings, repository, service = _build_runtime()
    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    stage_log = logger.bind(module=f"cli.{stage_name}", run_id=run.id)
    try:
        with _graceful_shutdown_signals():
            result = stage_runner(service, run.id)
        repository.finish_run(run.id, success=True)
        return settings, repository, run.id, result
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            stage_log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=stage_log,
            message="Stage interrupted",
            exc=exc,
        )
    except Exception:
        repository.finish_run(run.id, success=False)
        stage_log.exception("Stage execution failed")
        raise


@app.command()
def ingest() -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, _, _, result = _execute_stage(
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

    settings, _, _, result = _execute_stage(
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

    settings, _, _, result = _execute_stage(
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    parsed_anchor: date | None = None
    if anchor_date is not None and str(anchor_date).strip():
        raw_anchor = str(anchor_date).strip()
        try:
            parsed_anchor = _parse_anchor_date_option(raw_anchor)
        except Exception as exc:  # noqa: BLE001
            console = console_cls()
            console.print(
                f"[red]invalid date[/red] value={raw_anchor} expected=YYYY-MM-DD|YYYYMMDD"
            )
            raise typer.Exit(code=2) from exc

    settings, repository, run_id, result = _execute_stage(
        stage_name="trends",
        stage_runner=lambda service, run_id: service.trends(
            run_id=run_id,
            granularity=granularity,
            anchor_date=parsed_anchor,
            llm_model=model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
        ),
    )
    console = console_cls(stderr=settings.log_json)
    if len(getattr(result, "stream_results", []) or []) > 1:
        console.print(
            "[green]trends completed[/green] "
            f"streams={len(result.stream_results)} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
        for stream_result in result.stream_results:
            console.print(
                f"[cyan]{stream_result.stream}[/cyan] "
                f"doc_id={stream_result.doc_id}"
            )
    else:
        console.print(
            "[green]trends completed[/green] "
            f"doc_id={result.doc_id} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
    _print_billing_report(console=console, repository=repository, run_id=run_id)


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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    parsed_anchor: date | None = None
    if anchor_date is not None and str(anchor_date).strip():
        raw_anchor = str(anchor_date).strip()
        try:
            parsed_anchor = _parse_anchor_date_option(raw_anchor)
        except Exception as exc:  # noqa: BLE001
            console = console_cls()
            console.print(
                f"[red]invalid date[/red] value={raw_anchor} expected=YYYY-MM-DD|YYYYMMDD"
            )
            raise typer.Exit(code=2) from exc

    settings, repository, run_id, result = _execute_stage(
        stage_name="trends",
        stage_runner=lambda service, run_id: service.trends(
            run_id=run_id,
            granularity="week",
            anchor_date=parsed_anchor,
            llm_model=model,
            backfill=True,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
        ),
    )
    console = console_cls(stderr=settings.log_json)
    if len(getattr(result, "stream_results", []) or []) > 1:
        console.print(
            "[green]trends completed[/green] "
            f"streams={len(result.stream_results)} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
        for stream_result in result.stream_results:
            console.print(
                f"[cyan]{stream_result.stream}[/cyan] "
                f"doc_id={stream_result.doc_id}"
            )
    else:
        console.print(
            "[green]trends completed[/green] "
            f"doc_id={result.doc_id} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
    _print_billing_report(console=console, repository=repository, run_id=run_id)


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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    export_trend_static_site = _import_symbol(
        "recoleta.site",
        attr_name="export_trend_static_site",
    )

    resolved_input_dir = (
        input_dir.expanduser().resolve()
        if input_dir is not None
        else None
    )
    resolved_output_dir = (
        output_dir.expanduser().resolve()
        if output_dir is not None
        else None
    )
    settings = _build_settings() if resolved_input_dir is None or resolved_output_dir is None else None
    if resolved_input_dir is None:
        assert settings is not None
        resolved_input_dir = (
            settings.markdown_output_dir
            if _has_explicit_topic_streams(settings)
            else settings.markdown_output_dir / "Trends"
        )
    if resolved_output_dir is None:
        assert settings is not None
        resolved_output_dir = settings.markdown_output_dir / "site"
    manifest_path = export_trend_static_site(
        input_dir=resolved_input_dir,
        output_dir=resolved_output_dir,
        limit=limit,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    console = (
        console_cls(stderr=settings.log_json)
        if settings is not None
        else console_cls()
    )
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    stage_trend_site_source = _import_symbol(
        "recoleta.site",
        attr_name="stage_trend_site_source",
    )

    resolved_input_dir = (
        input_dir.expanduser().resolve()
        if input_dir is not None
        else None
    )
    resolved_output_dir = (
        output_dir.expanduser().resolve()
        if output_dir is not None
        else None
    )
    settings = _build_settings() if resolved_input_dir is None or resolved_output_dir is None else None
    if resolved_input_dir is None:
        assert settings is not None
        resolved_input_dir = (
            settings.markdown_output_dir
            if _has_explicit_topic_streams(settings)
            else settings.markdown_output_dir / "Trends"
        )
    if resolved_output_dir is None:
        resolved_output_dir = (
            (Path.cwd() / "site-content").resolve()
            if settings is not None and _has_explicit_topic_streams(settings)
            else (Path.cwd() / "site-content" / "Trends").resolve()
        )
    manifest_path = stage_trend_site_source(
        input_dir=resolved_input_dir,
        output_dir=resolved_output_dir,
        limit=limit,
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    console = (
        console_cls(stderr=settings.log_json)
        if settings is not None
        else console_cls()
    )
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
        with _graceful_shutdown_signals():
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
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="RAG sync interrupted",
            exc=exc,
        )
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
        with _graceful_shutdown_signals():
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
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="RAG build-index interrupted",
            exc=exc,
        )
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

    if not trends_only:
        db_clear(db_path=db_path, config_path=config_path, yes=yes)
        return

    if not yes:
        typer.echo("refusing to reset trends without --yes")
        raise typer.Exit(code=2)

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    repository_cls = symbols["Repository"]
    console = console_cls()
    log = logger.bind(module="cli.db.reset")

    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[green]db already empty[/green] path={resolved}")
        return

    repository = repository_cls(db_path=resolved)
    repository.init_schema()

    sqlmodel_session = _import_symbol("sqlmodel", attr_name="Session")
    sqlmodel_select = _import_symbol("sqlmodel", attr_name="select")
    document_model = _import_symbol("recoleta.models", attr_name="Document")

    with sqlmodel_session(repository.engine) as session:  # type: ignore[operator]
        statement = sqlmodel_select(document_model).where(
            document_model.doc_type.in_(["item", "trend"])
        )
        docs = list(session.exec(statement))
        doc_ids = [int(getattr(d, "id") or 0) for d in docs if getattr(d, "id", None)]

    chunks_deleted_total = 0
    for doc_id in doc_ids:
        chunks_deleted_total += int(repository.delete_document_chunks(doc_id=doc_id))

    docs_deleted_total = 0
    with sqlmodel_session(repository.engine) as session:  # type: ignore[operator]
        statement = sqlmodel_select(document_model).where(
            document_model.id.in_(doc_ids)
        )
        for doc in session.exec(statement):
            session.delete(doc)
            docs_deleted_total += 1
        session.commit()

    log.info(
        "Trends reset done deleted_docs={} deleted_chunks={} path={}",
        docs_deleted_total,
        chunks_deleted_total,
        str(resolved),
    )
    console.print(
        "[green]db trends reset[/green] "
        f"deleted_docs={docs_deleted_total} deleted_chunks={chunks_deleted_total} path={resolved}"
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

    symbols = _runtime_symbols()
    logger = symbols["logger"]

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
    scheduler_log = logger.bind(module="cli.run.scheduler")
    try:
        with _graceful_shutdown_signals():
            scheduler.start()
    except KeyboardInterrupt as exc:
        scheduler_log.warning(
            "Scheduler stopping signal={} exit_code={} waiting_for_jobs=true",
            _interrupt_signal_name(exc),
            _interrupt_exit_code(exc),
        )
        try:
            scheduler.shutdown(wait=True)
        except KeyboardInterrupt:
            scheduler_log.warning(
                "Scheduler shutdown interrupted again; forcing stop without waiting."
            )
            try:
                scheduler.shutdown(wait=False)
            except Exception:
                scheduler_log.exception("Forced scheduler shutdown failed")
        except Exception:
            scheduler_log.exception("Scheduler shutdown failed during interrupt")
        raise typer.Exit(code=_interrupt_exit_code(exc)) from None


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
        with _graceful_shutdown_signals():
            ingest_result = service.prepare(run_id=run.id)
            analyze_result = service.analyze(run_id=run.id, limit=analyze_limit)
            publish_result = service.publish(run_id=run.id, limit=publish_limit)
        repository.finish_run(run.id, success=True)
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run.id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="Run interrupted",
            exc=exc,
        )
    except Exception:
        repository.finish_run(run.id, success=False)
        log.exception("Run failed")
        raise
    else:
        console.print(
            "[green]run --once completed[/green] "
            f"ingest(inserted={ingest_result.inserted} updated={ingest_result.updated} failed={ingest_result.failed}) "
            f"analyze(processed={analyze_result.processed} failed={analyze_result.failed}) "
            f"publish(sent={publish_result.sent} skipped={publish_result.skipped} failed={publish_result.failed})"
        )
        if "markdown" in settings.publish_targets:
            console.print(
                f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}"
            )
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
    finally:
        _print_billing_report(console=console, repository=repository, run_id=run.id)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
