from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, date, datetime, timedelta
import importlib
import json
import os
from pathlib import Path
import signal
import shutil
import socket
from threading import Event, Thread
from typing import Any, NoReturn
from uuid import uuid4

_ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS = (
    "http_404",
    "http_429",
    "http_5xx",
    "http_other",
    "timeout",
    "request_error",
    "missing_url",
    "empty_document",
    "other",
)

_WORKSPACE_LEASE_TIMEOUT_SECONDS = 90
_RUN_HEARTBEAT_INTERVAL_SECONDS = 15
_GC_DEBUG_RETENTION_DAYS = 14
_GC_OPERATIONAL_RETENTION_DAYS = 60


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
        "WorkspaceLeaseHeldError": _import_symbol(
            "recoleta.storage", attr_name="WorkspaceLeaseHeldError"
        ),
        "WorkspaceLeaseLostError": _import_symbol(
            "recoleta.storage", attr_name="WorkspaceLeaseLostError"
        ),
    }
    return _RUNTIME_SYMBOLS


def _build_runtime(
    *,
    config_path: Path | None = None,
    db_path: Path | None = None,
) -> tuple[Any, Any, Any]:
    symbols = _runtime_symbols()
    repository_cls = symbols["Repository"]
    pipeline_service_cls = _import_symbol(
        "recoleta.pipeline", attr_name="PipelineService"
    )

    settings = _build_settings(config_path=config_path, db_path=db_path)
    repository = repository_cls(
        db_path=settings.recoleta_db_path,
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = pipeline_service_cls(settings=settings, repository=repository)
    return settings, repository, service


def _build_settings(
    *,
    config_path: Path | None = None,
    db_path: Path | None = None,
) -> Any:
    symbols = _runtime_symbols()
    settings_cls = symbols["Settings"]
    configure_process_logging = symbols["configure_process_logging"]

    init_kwargs: dict[str, Any] = {}
    if config_path is not None:
        init_kwargs["config_path"] = config_path.expanduser().resolve()
    if db_path is not None:
        init_kwargs["recoleta_db_path"] = db_path.expanduser().resolve()
    settings = settings_cls(**init_kwargs)  # pyright: ignore[reportCallIssue]
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


def _print_ingest_html_document_summary(
    *, console: Any, repository: Any, run_id: str
) -> None:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    log = logger.bind(module="cli.ingest_summary", run_id=run_id)
    try:
        metrics = repository.list_metrics(run_id=run_id)
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Ingest diagnostics load failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return

    by_name = {
        str(getattr(metric, "name", "") or ""): float(getattr(metric, "value", 0) or 0)
        for metric in metrics
    }
    items_total = int(
        by_name.get("pipeline.enrich.arxiv.html_document.items_total") or 0
    )
    if items_total <= 0:
        return

    pandoc_failed_total = int(
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_failed_total") or 0
    )
    pandoc_warning_items_total = int(
        by_name.get(
            "pipeline.enrich.arxiv.html_document.pandoc_warning_items_total"
        )
        or 0
    )
    pandoc_warning_count_sum = int(
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum")
        or 0
    )
    fallback_to_pdf_total = int(
        by_name.get("pipeline.enrich.arxiv.html_document.fallback_to_pdf_total") or 0
    )
    pandoc_math_replaced_sum = int(
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum")
        or 0
    )
    console.print(
        "[cyan]arxiv html_document[/cyan] "
        f"items={items_total} "
        f"pandoc_failed={pandoc_failed_total} "
        f"pandoc_warning_items={pandoc_warning_items_total} "
        f"pandoc_warning_count={pandoc_warning_count_sum} "
        f"pdf_fallbacks={fallback_to_pdf_total} "
        f"math_replaced={pandoc_math_replaced_sum}"
    )

    fallback_reason_parts: list[str] = []
    for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS:
        count = int(
            by_name.get(
                f"pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.{bucket}_total"
            )
            or 0
        )
        if count <= 0:
            continue
        fallback_reason_parts.append(f"{bucket}={count}")
    if fallback_reason_parts:
        console.print(
            "[cyan]arxiv html_document fallback reasons[/cyan] "
            + " ".join(fallback_reason_parts)
        )


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


def _raise_typer_exit_for_workspace_lock(
    *,
    console: Any,
    log: Any,
    exc: Any,
) -> NoReturn:
    expires_at = getattr(exc, "expires_at", None)
    log.warning(
        "Workspace lease blocked command requested_run_id={} holder_run_id={} holder_command={} holder_hostname={} holder_pid={} expires_at={}",
        getattr(exc, "requested_run_id", None),
        getattr(exc, "holder_run_id", None),
        getattr(exc, "holder_command", None),
        getattr(exc, "holder_hostname", None),
        getattr(exc, "holder_pid", None),
        expires_at.isoformat() if expires_at is not None else None,
    )
    details = [
        f"holder_command={getattr(exc, 'holder_command', None)}"
        if getattr(exc, "holder_command", None)
        else "",
        f"holder_hostname={getattr(exc, 'holder_hostname', None)}"
        if getattr(exc, "holder_hostname", None)
        else "",
        f"holder_pid={getattr(exc, 'holder_pid', None)}"
        if getattr(exc, "holder_pid", None) is not None
        else "",
    ]
    detail_text = " ".join(part for part in details if part)
    console.print(
        "[red]workspace is locked[/red]"
        + (f" {detail_text}" if detail_text else "")
    )
    raise typer.Exit(code=1) from None


class _LeaseHeartbeatMonitor:
    def __init__(
        self,
        *,
        repository: Any,
        run_id: str | None,
        owner_token: str,
        lease_timeout_seconds: int,
        interval_seconds: int,
        log: Any,
        lease_lost_error_cls: type[BaseException],
        thread_name: str,
    ) -> None:
        self._repository = repository
        self._run_id = run_id
        self._owner_token = owner_token
        self._lease_timeout_seconds = lease_timeout_seconds
        self._interval_seconds = max(1, int(interval_seconds))
        self._log = log
        self._lease_lost_error_cls = lease_lost_error_cls
        self._thread_name = thread_name
        self._stop_event = Event()
        self._thread: Thread | None = None
        self._fatal_error: BaseException | None = None

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = Thread(
            target=self._run,
            name=self._thread_name,
            daemon=True,
        )
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread is None:
            return
        self._thread.join(timeout=self._interval_seconds + 1)

    def raise_if_failed(self) -> None:
        if self._fatal_error is not None:
            raise self._fatal_error

    def _run(self) -> None:
        while not self._stop_event.wait(self._interval_seconds):
            try:
                self._repository.renew_workspace_lease(
                    owner_token=self._owner_token,
                    lease_timeout_seconds=self._lease_timeout_seconds,
                )
                if self._run_id is not None:
                    self._repository.heartbeat_run(self._run_id)
            except self._lease_lost_error_cls as exc:
                self._fatal_error = exc
                self._log.warning(
                    "Run heartbeat stopped because workspace lease was lost error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
                self._stop_event.set()
                return
            except Exception as exc:  # noqa: BLE001
                self._log.warning(
                    "Run heartbeat update failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )


def _begin_managed_run(
    *,
    command: str,
    log_module: str,
) -> tuple[Any, Any, Any, Any, str, str, Any, _LeaseHeartbeatMonitor]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]
    workspace_lease_held_error = symbols["WorkspaceLeaseHeldError"]
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    settings, repository, service = _build_runtime()
    console = console_cls(stderr=bool(getattr(settings, "log_json", False)))
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
            config_fingerprint=settings.safe_fingerprint(),
            run_id=run_id,
        )
        command_log = logger.bind(module=log_module, run_id=run.id)
        heartbeat_monitor = _LeaseHeartbeatMonitor(
            repository=repository,
            run_id=run.id,
            owner_token=owner_token,
            lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            interval_seconds=_RUN_HEARTBEAT_INTERVAL_SECONDS,
            log=logger.bind(module="cli.runtime.heartbeat", command=command, run_id=run.id),
            lease_lost_error_cls=workspace_lease_lost_error,
            thread_name=f"recoleta-heartbeat-{run.id}",
        )
        heartbeat_monitor.start()
        return (
            settings,
            repository,
            service,
            console,
            run.id,
            owner_token,
            command_log,
            heartbeat_monitor,
        )
    except Exception:
        try:
            repository.release_workspace_lease(owner_token=owner_token)
        except Exception:
            lock_log.exception("Workspace lease release failed during startup")
        raise


def _cleanup_managed_run(
    *,
    repository: Any,
    owner_token: str,
    heartbeat_monitor: _LeaseHeartbeatMonitor,
    log: Any,
) -> None:
    heartbeat_monitor.stop()
    try:
        repository.release_workspace_lease(owner_token=owner_token)
    except Exception:
        log.exception("Workspace lease release failed")


def _cleanup_workspace_lease(
    *,
    repository: Any,
    owner_token: str,
    heartbeat_monitor: _LeaseHeartbeatMonitor,
    log: Any,
) -> None:
    heartbeat_monitor.stop()
    try:
        repository.release_workspace_lease(owner_token=owner_token)
    except Exception:
        log.exception("Workspace lease release failed")


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Callable[[Any, str], Any],
) -> tuple[Any, Any, str, Any]:
    symbols = _runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        service,
        _console,
        run_id,
        owner_token,
        stage_log,
        heartbeat_monitor,
    ) = _begin_managed_run(
        command=stage_name,
        log_module=f"cli.{stage_name}",
    )
    try:
        with _graceful_shutdown_signals():
            result = stage_runner(service, run_id)
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=True)
        return settings, repository, run_id, result
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            stage_log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=stage_log,
            message="Stage interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            stage_log.exception("Run finish failed after lease loss")
        stage_log.warning(
            "Stage stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        stage_log.exception("Stage execution failed")
        raise
    finally:
        _cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=stage_log,
        )


@app.command()
def ingest() -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, repository, run_id, result = _execute_stage(
        stage_name="ingest",
        stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )
    _print_ingest_html_document_summary(
        console=console,
        repository=repository,
        run_id=run_id,
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
    console = (
        console_cls(stderr=settings.log_json)
        if settings is not None
        else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        _maybe_acquire_workspace_lease_for_settings(
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
            _cleanup_workspace_lease(
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
    console = (
        console_cls(stderr=settings.log_json)
        if settings is not None
        else console_cls()
    )
    lease_repository, lease_owner_token, lease_log, lease_heartbeat_monitor = (
        _maybe_acquire_workspace_lease_for_settings(
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
            _cleanup_workspace_lease(
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
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        _service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = _begin_managed_run(
        command="rag sync-vectors",
        log_module="cli.rag.sync_vectors",
    )

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
                run_id=run_id,
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
                llm_connection=settings.llm_connection_config(),
            )
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=True)
        console.print(f"[green]rag sync completed[/green] stats={stats}")
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="RAG sync interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "RAG sync stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        log.exception("RAG sync failed")
        raise
    finally:
        _cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
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

    symbols = _runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        _service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = _begin_managed_run(
        command="rag build-index",
        log_module="cli.rag.build_index",
    )
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
        heartbeat_monitor.raise_if_failed()
        errors = stats.get("errors") or []
        table_exists = bool(stats.get("table_exists"))

        if not table_exists:
            repository.finish_run(run_id, success=True)
            console.print(
                "[yellow]rag build-index skipped[/yellow] table not found (run `recoleta rag sync-vectors` first)"
            )
            return

        if strict and errors:
            repository.finish_run(run_id, success=False)
            console.print(f"[red]rag build-index failed[/red] stats={stats}")
            raise typer.Exit(code=1)

        repository.finish_run(run_id, success=True)
        if errors:
            console.print(
                f"[yellow]rag build-index completed with errors[/yellow] stats={stats}"
            )
        else:
            console.print(f"[green]rag build-index completed[/green] stats={stats}")
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="RAG build-index interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "RAG build-index stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise typer.Exit(code=1) from None
    except typer.Exit:
        raise
    except Exception:
        repository.finish_run(run_id, success=False)
        log.exception("RAG build-index failed")
        raise
    finally:
        _cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()

    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(
            "[green]gc completed[/green] "
            f"deleted_artifacts=0 deleted_runs=0 path={resolved}"
        )
        return

    repository = _build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = _acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="gc",
        log_module="cli.gc",
    )
    try:
        settings: Any | None = None
        filesystem_cache_pruning = "available"
        try:
            settings = _maybe_load_settings(
                db_path_option=db_path,
                config_path_option=config_path,
                resolved_db_path=resolved,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "GC settings unavailable; filesystem cache pruning skipped error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            settings = None
            filesystem_cache_pruning = "skipped"
        else:
            if prune_caches and settings is None:
                filesystem_cache_pruning = "skipped"

        reference_now = datetime.now(UTC)
        debug_cutoff = reference_now - timedelta(days=_GC_DEBUG_RETENTION_DAYS)
        operational_cutoff = reference_now - timedelta(
            days=_GC_OPERATIONAL_RETENTION_DAYS
        )

        artifact_result = repository.prune_artifacts_older_than(
            older_than=debug_cutoff,
            dry_run=dry_run,
        )
        operational_result = repository.prune_operational_history_older_than(
            older_than=operational_cutoff,
            dry_run=dry_run,
        )
        pdf_debug_deleted = (
            _prune_expired_pdf_debug_dirs(
                settings=settings,
                older_than=(None if prune_caches else debug_cutoff),
                dry_run=dry_run,
            )
            if settings is not None
            else 0
        )

        chunk_cache_result = (
            repository.clear_document_chunk_cache(dry_run=dry_run)
            if prune_caches
            else None
        )
        lancedb_tables_deleted = (
            _prune_inactive_lancedb_tables(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )
        trend_pdfs_deleted = (
            _prune_trend_pdfs(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )
        site_outputs_deleted = (
            _prune_managed_site_outputs(settings=settings, dry_run=dry_run)
            if prune_caches and settings is not None
            else 0
        )

        counter_prefix = "would_delete" if dry_run else "deleted"
        heartbeat_monitor.raise_if_failed()
        log.info(
            "GC completed artifact_rows={} artifact_paths={} missing_artifact_paths={} run_rows={} metric_rows={} pdf_debug_dirs={} document_chunks={} chunk_embeddings={} chunk_fts_rows={} lancedb_tables={} trend_pdfs={} site_outputs={} dry_run={}",
            artifact_result.artifact_rows,
            artifact_result.deleted_paths,
            artifact_result.missing_paths,
            operational_result.run_rows,
            operational_result.metric_rows,
            pdf_debug_deleted,
            int((chunk_cache_result.document_chunks if chunk_cache_result else 0)),
            int((chunk_cache_result.chunk_embeddings if chunk_cache_result else 0)),
            int((chunk_cache_result.chunk_fts_rows if chunk_cache_result else 0)),
            lancedb_tables_deleted,
            trend_pdfs_deleted,
            site_outputs_deleted,
            dry_run,
        )
        filesystem_segment = (
            f" filesystem_cache_pruning={filesystem_cache_pruning}"
            if prune_caches
            else ""
        )
        console.print(
            f"[green]gc completed[/green] "
            f"{counter_prefix}_artifacts={artifact_result.artifact_rows} "
            f"{counter_prefix}_artifact_paths={artifact_result.deleted_paths} "
            f"{counter_prefix}_missing_artifact_paths={artifact_result.missing_paths} "
            f"{counter_prefix}_runs={operational_result.run_rows} "
            f"{counter_prefix}_metrics={operational_result.metric_rows} "
            f"{counter_prefix}_pdf_debug_dirs={pdf_debug_deleted} "
            f"{counter_prefix}_document_chunks={int((chunk_cache_result.document_chunks if chunk_cache_result else 0))} "
            f"{counter_prefix}_chunk_embeddings={int((chunk_cache_result.chunk_embeddings if chunk_cache_result else 0))} "
            f"{counter_prefix}_chunk_fts_rows={int((chunk_cache_result.chunk_fts_rows if chunk_cache_result else 0))} "
            f"{counter_prefix}_lancedb_tables={lancedb_tables_deleted} "
            f"{counter_prefix}_trend_pdfs={trend_pdfs_deleted} "
            f"{counter_prefix}_site_outputs={site_outputs_deleted} "
            f"{filesystem_segment}"
            f"path={resolved}"
        )
    finally:
        _cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise typer.Exit(code=2)

    repository = _build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = _acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="vacuum",
        log_module="cli.vacuum",
    )
    try:
        repository.vacuum()
        heartbeat_monitor.raise_if_failed()
        log.info("VACUUM completed path={}", str(resolved))
        console.print(f"[green]vacuum completed[/green] path={resolved}")
    finally:
        _cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise typer.Exit(code=2)

    repository = _build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = _acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="backup",
        log_module="cli.backup",
    )
    try:
        bundle_root = (
            output_dir.expanduser().resolve()
            if output_dir is not None
            else (resolved.parent / "backups").resolve()
        )
        result = repository.backup_database(output_dir=bundle_root)
        heartbeat_monitor.raise_if_failed()
        log.info(
            "Backup completed bundle_dir={} manifest_path={} schema_version={}",
            str(result.bundle_dir),
            str(result.manifest_path),
            result.schema_version,
        )
        console.print(
            "[green]backup completed[/green] "
            f"bundle={result.bundle_dir} schema_version={result.schema_version}"
        )
    finally:
        _cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
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

    if not yes:
        typer.echo("refusing to restore db without --yes")
        raise typer.Exit(code=2)

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.restore")

    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    lease_repository: Any | None = None
    lease_owner_token: str | None = None
    lease_heartbeat_monitor: _LeaseHeartbeatMonitor | None = None
    try:
        if resolved.exists():
            lease_repository = _build_repository_for_db_path(db_path=resolved)
            assert lease_repository is not None
            lease_repository.init_schema()
            lease_owner_token, _, lease_heartbeat_monitor = _acquire_workspace_lease_for_command(
                repository=lease_repository,
                console=console,
                command="restore",
                log_module="cli.restore",
            )
        result = _build_repository_for_db_path(db_path=resolved).restore_database(
            bundle_dir=bundle,
            db_path=resolved,
        )
        if lease_heartbeat_monitor is not None:
            lease_heartbeat_monitor.raise_if_failed()
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Restore failed bundle={} path={} error_type={} error={}",
            str(bundle),
            str(resolved),
            type(exc).__name__,
            str(exc),
        )
        console.print(f"[red]restore failed[/red] {exc}")
        raise typer.Exit(code=1) from exc
    finally:
        if (
            lease_repository is not None
            and lease_owner_token is not None
            and lease_heartbeat_monitor is not None
        ):
            _cleanup_workspace_lease(
                repository=lease_repository,
                owner_token=lease_owner_token,
                heartbeat_monitor=lease_heartbeat_monitor,
                log=log,
            )

    log.info(
        "Restore completed bundle_dir={} path={} schema_version={}",
        str(result.bundle_dir),
        str(result.database_path),
        result.schema_version,
    )
    console.print(
        "[green]restore completed[/green] "
        f"bundle={result.bundle_dir} path={result.database_path} schema_version={result.schema_version}"
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.stats", json=json_output)

    def _exit_with_error(message: str, *, code: int = 1) -> NoReturn:
        log.warning("Stats failed db_path={} error={}", resolved_db_path, message)
        if json_output:
            typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]stats failed[/red] {message}")
        raise typer.Exit(code=code)

    resolved_db_path: Path | None = None
    try:
        resolved_db_path = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        log.warning(message)
        if json_output:
            typer.echo(
                json.dumps(
                    {"status": "error", "error": message},
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            console.print(f"[red]stats failed[/red] {message}")
        raise typer.Exit(code=1) from exc

    if not resolved_db_path.exists():
        _exit_with_error(f"db does not exist: {resolved_db_path}")

    settings: Any | None = None
    settings_status = "skipped"
    workspace_bytes: dict[str, int | None] = {}
    if _should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = _build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
            settings_status = "ok"
            workspace_bytes = _workspace_bytes_from_settings(settings)
        except Exception as exc:  # noqa: BLE001
            settings_status = "failed"
            log.warning(
                "Stats settings load failed db_path={} error_type={} error={}",
                resolved_db_path,
                type(exc).__name__,
                str(exc),
            )

    repository = _build_repository_for_db_path(db_path=resolved_db_path)
    try:
        schema_version = repository.ensure_schema_current()
    except Exception as exc:
        _exit_with_error(str(exc))

    reference_now = datetime.now(UTC)
    snapshot = repository.collect_workspace_stats(
        stale_after_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
        now=reference_now,
    )
    lease_state = "unavailable"
    lease_payload: dict[str, Any] = {
        "state": "unavailable",
        "holder_command": None,
        "holder_run_id": None,
        "holder_pid": None,
        "holder_hostname": None,
        "expires_at": None,
    }
    if repository.has_table("workspace_leases"):
        lease = repository.get_workspace_lease()
        if lease is None:
            lease_state = "free"
            lease_payload["state"] = lease_state
        else:
            lease_state = "held"
            lease_payload = {
                "state": lease_state,
                "holder_command": lease.command,
                "holder_run_id": lease.run_id,
                "holder_pid": lease.pid,
                "holder_hostname": lease.hostname,
                "expires_at": (
                    lease.expires_at.isoformat()
                    if lease.expires_at is not None
                    else None
                ),
            }

    oldest_unfinished_at = _normalize_utc_datetime(snapshot.oldest_unfinished_at)
    oldest_unfinished_age_seconds: int | None = None
    if oldest_unfinished_at is not None:
        oldest_unfinished_age_seconds = max(
            0,
            int((reference_now - oldest_unfinished_at).total_seconds()),
        )
    latest_successful_run_at = _normalize_utc_datetime(
        snapshot.latest_successful_run_at
    )
    latest_successful_run_age_seconds: int | None = None
    if latest_successful_run_at is not None:
        latest_successful_run_age_seconds = max(
            0,
            int((reference_now - latest_successful_run_at).total_seconds()),
        )

    payload = {
        "status": "ok",
        "db_path": str(resolved_db_path),
        "schema_version": int(schema_version),
        "db_bytes": int(resolved_db_path.stat().st_size),
        "settings": settings_status,
        "items_total": int(sum(snapshot.item_state_counts.values())),
        "items_by_state": snapshot.item_state_counts,
        "unfinished_total": int(snapshot.unfinished_total),
        "oldest_unfinished_age_seconds": oldest_unfinished_age_seconds,
        "runs_by_status": snapshot.run_status_counts,
        "stale_running_runs": int(snapshot.stale_running_runs),
        "latest_successful_run_id": snapshot.latest_successful_run_id,
        "latest_successful_run_at": (
            latest_successful_run_at.isoformat()
            if latest_successful_run_at is not None
            else None
        ),
        "latest_successful_run_age_seconds": latest_successful_run_age_seconds,
        "lease": lease_payload,
        "workspace_bytes": workspace_bytes,
    }

    if json_output:
        typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return

    item_parts = [
        f"{state}={count}"
        for state, count in payload["items_by_state"].items()
        if int(count) > 0
    ]
    run_parts = [
        f"{state}={count}"
        for state, count in payload["runs_by_status"].items()
        if int(count) > 0
    ]
    console.print("[green]stats ok[/green]")
    console.print(f"db={payload['db_path']}")
    console.print(
        f"schema_version={payload['schema_version']} db_bytes={payload['db_bytes']}"
    )
    console.print(f"settings={payload['settings']}")
    console.print(
        f"items_total={payload['items_total']} unfinished_total={payload['unfinished_total']}"
    )
    console.print("items_by_state=" + (" ".join(item_parts) if item_parts else "none"))
    console.print(
        "oldest_unfinished_age_seconds="
        + (
            str(payload["oldest_unfinished_age_seconds"])
            if payload["oldest_unfinished_age_seconds"] is not None
            else "none"
        )
    )
    console.print("runs_by_status=" + (" ".join(run_parts) if run_parts else "none"))
    console.print(f"stale_running_runs={payload['stale_running_runs']}")
    console.print(
        "latest_successful_run="
        + (
            " ".join(
                [
                    str(payload["latest_successful_run_id"]),
                    str(payload["latest_successful_run_at"]),
                    f"age_seconds={payload['latest_successful_run_age_seconds']}",
                ]
            )
            if payload["latest_successful_run_id"] is not None
            else "none"
        )
    )
    console.print(
        f"lease={lease_state}"
        + (
            " "
            + " ".join(
                part
                for part in (
                    f"holder_command={lease_payload['holder_command']}"
                    if lease_payload["holder_command"]
                    else "",
                    f"holder_run_id={lease_payload['holder_run_id']}"
                    if lease_payload["holder_run_id"]
                    else "",
                    f"holder_pid={lease_payload['holder_pid']}"
                    if lease_payload["holder_pid"] is not None
                    else "",
                )
                if part
            )
            if lease_state == "held"
            else ""
        )
    )
    if payload["workspace_bytes"]:
        workspace_parts = [
            f"{name}={size if size is not None else 'unavailable'}"
            for name, size in payload["workspace_bytes"].items()
        ]
        console.print("workspace_bytes=" + " ".join(workspace_parts))


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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.doctor", healthcheck=healthcheck)

    resolved_db_path: Path
    try:
        resolved_db_path = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        message = f"db path resolution failed: {exc}"
        log.warning(message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
        )
        raise typer.Exit(code=1) from exc

    settings: Any | None = None
    settings_status = "skipped"
    if _should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = _build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
            settings_status = "ok"
        except Exception as exc:  # noqa: BLE001
            message = f"settings load failed: {exc}"
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
            )
            raise typer.Exit(code=1) from exc

    if not resolved_db_path.exists():
        message = f"db does not exist: {resolved_db_path}"
        log.warning(message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
        )
        raise typer.Exit(code=1)

    repository = _build_repository_for_db_path(db_path=resolved_db_path)
    try:
        schema_version = repository.ensure_schema_current()
    except Exception as exc:
        message = str(exc)
        log.warning("Schema compatibility check failed error={}", message)
        console.print(
            f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
        )
        raise typer.Exit(code=1) from exc

    path_status = "ok"
    if settings is not None:
        paths_to_check = [
            Path(settings.markdown_output_dir),
            Path(settings.rag_lancedb_dir),
        ]
        artifacts_dir = getattr(settings, "artifacts_dir", None)
        if artifacts_dir is not None:
            paths_to_check.append(Path(artifacts_dir))
        failed_paths = [path for path in paths_to_check if not _is_accessible_path(path)]
        if failed_paths:
            message = "path access failed: " + ", ".join(str(path) for path in failed_paths)
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
            )
            raise typer.Exit(code=1)
    else:
        path_status = "skipped"

    lease_state = "unavailable"
    lease_details = ""
    if repository.has_table("workspace_leases"):
        lease = repository.get_workspace_lease()
        if lease is None:
            lease_state = "free"
        else:
            lease_state = "held"
            details = [
                f"holder_command={lease.command}" if lease.command else "",
                f"holder_run_id={lease.run_id}" if lease.run_id else "",
                f"holder_pid={lease.pid}" if lease.pid is not None else "",
            ]
            lease_details = " ".join(part for part in details if part)

    latest_run_state = "none"
    latest_successful_run_at: datetime | None = None
    if repository.has_table("runs"):
        snapshot = repository.collect_workspace_stats(
            stale_after_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            now=datetime.now(UTC),
        )
        latest_successful_run_at = _normalize_utc_datetime(
            snapshot.latest_successful_run_at
        )
        runs = repository.list_recent_runs(limit=1)
        if runs:
            latest_run = runs[0]
            latest_run_state = (
                f"{latest_run.status}:{latest_run.id}"
            )

    if max_success_age_minutes is not None:
        threshold_seconds = int(max_success_age_minutes) * 60
        if latest_successful_run_at is None:
            message = (
                "latest successful run is too old: "
                "no successful runs recorded"
            )
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
            )
            raise typer.Exit(code=1)
        age_seconds = max(
            0,
            int((datetime.now(UTC) - latest_successful_run_at).total_seconds()),
        )
        if age_seconds > threshold_seconds:
            message = (
                "latest successful run is too old: "
                f"age_seconds={age_seconds} threshold_seconds={threshold_seconds}"
            )
            log.warning(message)
            console.print(
                f"[red]{'healthcheck failed' if healthcheck else 'doctor failed'}[/red] {message}"
            )
            raise typer.Exit(code=1)

    if healthcheck:
        console.print(
            "[green]healthcheck ok[/green] "
            f"schema_version={schema_version} "
            f"settings={settings_status} "
            f"paths={path_status} "
            f"lease={lease_state} "
            f"latest_run={latest_run_state}"
            + (f" {lease_details}" if lease_details else "")
        )
        return

    console.print("[green]doctor ok[/green]")
    console.print(f"db={resolved_db_path}")
    console.print(f"schema_version={schema_version}")
    console.print(f"settings={settings_status}")
    console.print(f"paths={path_status}")
    console.print(f"lease={lease_state}" + (f" {lease_details}" if lease_details else ""))
    console.print(f"latest_run={latest_run_state}")


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
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = _begin_managed_run(
        command="run --once",
        log_module="cli.run.once",
    )

    try:
        with _graceful_shutdown_signals():
            ingest_result = service.prepare(run_id=run_id)
            heartbeat_monitor.raise_if_failed()
            analyze_result = service.analyze(run_id=run_id, limit=analyze_limit)
            heartbeat_monitor.raise_if_failed()
            publish_result = service.publish(run_id=run_id, limit=publish_limit)
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=True)
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        _raise_typer_exit_for_interrupt(
            log=log,
            message="Run interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "Run stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
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
        _print_billing_report(console=console, repository=repository, run_id=run_id)
        _cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
