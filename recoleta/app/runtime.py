from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
import importlib
import os
import signal
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


def _import_symbol(module_name: str, *, attr_name: str | None = None) -> Any:
    module = importlib.import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


typer = _import_symbol("typer")
_RUNTIME_SYMBOLS: dict[str, Any] | None = None


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
    config_path: Any | None = None,
    db_path: Any | None = None,
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
    config_path: Any | None = None,
    db_path: Any | None = None,
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
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_warning_items_total")
        or 0
    )
    pandoc_warning_count_sum = int(
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum") or 0
    )
    fallback_to_pdf_total = int(
        by_name.get("pipeline.enrich.arxiv.html_document.fallback_to_pdf_total") or 0
    )
    pandoc_math_replaced_sum = int(
        by_name.get("pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum") or 0
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
    except AttributeError, ValueError:
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
        "[red]workspace is locked[/red]" + (f" {detail_text}" if detail_text else "")
    )
    raise typer.Exit(code=1) from None


@dataclass(frozen=True, slots=True)
class _LeaseHeartbeatMonitorConfig:
    repository: Any
    run_id: str | None
    owner_token: str
    lease_timeout_seconds: int
    interval_seconds: int
    log: Any
    lease_lost_error_cls: type[BaseException]
    thread_name: str


@dataclass(frozen=True, slots=True)
class _ManagedRunStartupContext:
    settings: Any
    repository: Any
    logger: Any
    lock_log: Any
    log_module: str
    command: str
    run_id: str
    owner_token: str
    workspace_lease_lost_error: type[BaseException]


def _coerce_lease_heartbeat_monitor_config(
    *,
    config: _LeaseHeartbeatMonitorConfig | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _LeaseHeartbeatMonitorConfig:
    if config is not None:
        return config
    values = dict(legacy_kwargs or {})
    return _LeaseHeartbeatMonitorConfig(
        repository=values["repository"],
        run_id=values.get("run_id"),
        owner_token=str(values["owner_token"]),
        lease_timeout_seconds=int(values["lease_timeout_seconds"]),
        interval_seconds=int(values["interval_seconds"]),
        log=values["log"],
        lease_lost_error_cls=values["lease_lost_error_cls"],
        thread_name=str(values["thread_name"]),
    )


class _LeaseHeartbeatMonitor:
    def __init__(
        self,
        config: _LeaseHeartbeatMonitorConfig | None = None,
        **legacy_kwargs: Any,
    ) -> None:
        resolved = _coerce_lease_heartbeat_monitor_config(
            config=config,
            legacy_kwargs=legacy_kwargs,
        )
        self._repository = resolved.repository
        self._run_id = resolved.run_id
        self._owner_token = resolved.owner_token
        self._lease_timeout_seconds = resolved.lease_timeout_seconds
        self._interval_seconds = max(1, int(resolved.interval_seconds))
        self._log = resolved.log
        self._lease_lost_error_cls = resolved.lease_lost_error_cls
        self._thread_name = resolved.thread_name
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


def _build_heartbeat_monitor(
    *,
    config: _LeaseHeartbeatMonitorConfig,
) -> _LeaseHeartbeatMonitor:
    return _LeaseHeartbeatMonitor(config=config)


def _maybe_update_run_context(
    *,
    repository: Any,
    run_id: str,
    command: str,
    log: Any,
) -> None:
    update_run_context = getattr(repository, "update_run_context", None)
    if not callable(update_run_context):
        return
    try:
        update_run_context(run_id=run_id, command=command)
    except Exception:
        log.exception("Run context update failed during startup")


def _start_managed_run_resources(
    context: _ManagedRunStartupContext,
) -> tuple[Any, Any, _LeaseHeartbeatMonitor]:
    recovered_total = context.repository.mark_stale_runs_failed(
        stale_after_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS
    )
    if int(recovered_total or 0) > 0:
        context.lock_log.warning(
            "Recovered stale runs recovered_total={}",
            int(recovered_total),
        )
    run = context.repository.create_run(
        config_fingerprint=context.settings.safe_fingerprint(),
        run_id=context.run_id,
    )
    _maybe_update_run_context(
        repository=context.repository,
        run_id=run.id,
        command=context.command,
        log=context.lock_log,
    )
    heartbeat_monitor = _build_heartbeat_monitor(
        config=_LeaseHeartbeatMonitorConfig(
            repository=context.repository,
            run_id=run.id,
            owner_token=context.owner_token,
            lease_timeout_seconds=_WORKSPACE_LEASE_TIMEOUT_SECONDS,
            interval_seconds=_RUN_HEARTBEAT_INTERVAL_SECONDS,
            log=context.logger.bind(
                module="cli.runtime.heartbeat",
                command=context.command,
                run_id=run.id,
            ),
            lease_lost_error_cls=context.workspace_lease_lost_error,
            thread_name=f"recoleta-heartbeat-{run.id}",
        ),
    )
    heartbeat_monitor.start()
    return (
        run,
        context.logger.bind(module=context.log_module, run_id=run.id),
        heartbeat_monitor,
    )


def _begin_managed_run(
    *,
    command: str,
    log_module: str,
    config_path: Any | None = None,
    db_path: Any | None = None,
) -> tuple[Any, Any, Any, Any, str, str, Any, _LeaseHeartbeatMonitor]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]
    console_cls = symbols["Console"]
    workspace_lease_held_error = symbols["WorkspaceLeaseHeldError"]
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    build_runtime_kwargs: dict[str, Any] = {}
    if config_path is not None:
        build_runtime_kwargs["config_path"] = config_path
    if db_path is not None:
        build_runtime_kwargs["db_path"] = db_path
    settings, repository, service = _build_runtime(**build_runtime_kwargs)
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
        run, command_log, heartbeat_monitor = _start_managed_run_resources(
            _ManagedRunStartupContext(
                settings=settings,
                repository=repository,
                logger=logger,
                lock_log=lock_log,
                log_module=log_module,
                command=command,
                run_id=run_id,
                owner_token=owner_token,
                workspace_lease_lost_error=workspace_lease_lost_error,
            )
        )
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
