from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, NoReturn, cast

import recoleta.cli as cli
from recoleta.cli.command_support import (
    finish_run_safely,
    load_billing_metrics,
    load_runtime,
    managed_run_for_settings,
    RuntimeLoadRequest,
)


@dataclass(frozen=True, slots=True)
class TranslateCommandRequest:
    db_path: Path | None
    config_path: Path | None
    granularity: str | None
    include: str
    json_output: bool
    command_name: str
    raise_on_abort: bool
    log_module: str
    runner_attr: str
    runner_kwargs: dict[str, Any]


@dataclass(frozen=True, slots=True)
class TranslateRunnerRequest:
    repository: Any
    settings: Any
    granularity: str | None
    include: str
    run_id: str
    runner_attr: str
    runner_kwargs: dict[str, Any]


@dataclass(frozen=True, slots=True)
class TranslateResultContext:
    resolved_db_path: Path
    repository: Any
    console: Any
    run_id: str
    result: Any
    metrics: list[Any]
    command_name: str
    granularity: str | None
    include: str
    json_output: bool
    raise_on_abort: bool


@dataclass(frozen=True, slots=True)
class TranslateSessionContext:
    request: TranslateCommandRequest
    resolved_db_path: Path
    repository: Any
    settings: Any
    console: Any
    workspace_lease_lost_error: type[BaseException]


def _load_settings_for_translate(
    *,
    db_path: Path | None,
    config_path: Path | None,
) -> tuple[Path, Any, Any, Any]:
    runtime = load_runtime(
        request=RuntimeLoadRequest(
            db_path=db_path,
            config_path=config_path,
            command_name="translate",
            require_settings=True,
            init_schema=True,
        ),
    )
    return (
        runtime.resolved_db_path,
        runtime.settings,
        runtime.repository,
        runtime.console,
    )


def run_translate_run_command(**kwargs: Any) -> None:
    _run_translate_command(
        request=TranslateCommandRequest(
            db_path=kwargs.get("db_path"),
            config_path=kwargs.get("config_path"),
            granularity=kwargs.get("granularity"),
            include=str(kwargs["include"]),
            json_output=bool(kwargs.get("json_output", False)),
            command_name=str(kwargs.get("command_name", "translate run")),
            raise_on_abort=bool(kwargs.get("raise_on_abort", False)),
            log_module="cli.translate.run",
            runner_attr="run_translation",
            runner_kwargs={
                "limit": kwargs.get("limit"),
                "force": bool(kwargs.get("force", False)),
                "context_assist": kwargs["context_assist"],
            },
        )
    )


def run_translate_backfill_command(**kwargs: Any) -> None:
    _run_translate_command(
        request=TranslateCommandRequest(
            db_path=kwargs.get("db_path"),
            config_path=kwargs.get("config_path"),
            granularity=kwargs.get("granularity"),
            include=str(kwargs["include"]),
            json_output=bool(kwargs.get("json_output", False)),
            command_name=str(kwargs.get("command_name", "translate backfill")),
            raise_on_abort=False,
            log_module="cli.translate.backfill",
            runner_attr="run_translation_backfill",
            runner_kwargs={
                "limit": kwargs.get("limit"),
                "force": bool(kwargs.get("force", False)),
                "context_assist": kwargs["context_assist"],
                "legacy_source_language": kwargs.get("legacy_source_language"),
                "emit_mirror_targets": bool(kwargs.get("emit_mirror_targets", False)),
                "all_history": bool(kwargs.get("all_history", False)),
            },
        )
    )


def _run_translate_command(*, request: TranslateCommandRequest) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = cast(type[BaseException], symbols["WorkspaceLeaseLostError"])
    resolved_db_path, settings, repository, console = _load_settings_for_translate(
        db_path=request.db_path,
        config_path=request.config_path,
    )
    context = TranslateSessionContext(
        request=request,
        resolved_db_path=resolved_db_path,
        repository=cast(Any, repository),
        settings=cast(Any, settings),
        console=cast(Any, console),
        workspace_lease_lost_error=workspace_lease_lost_error,
    )
    with managed_run_for_settings(
        settings=context.settings,
        repository=context.repository,
        console=context.console,
        command=request.command_name,
        log_module=request.log_module,
    ) as session:
        result = _execute_translate_session(context=context, session=session)
        metrics = load_billing_metrics(
            repository=context.repository,
            run_id=session.run_id,
            log=session.log,
            warning_message=f"{request.command_name.capitalize()} billing metrics load failed",
        )
        _emit_translate_result(
            context=TranslateResultContext(
                resolved_db_path=context.resolved_db_path,
                repository=context.repository,
                console=context.console,
                run_id=session.run_id,
                result=result,
                metrics=metrics,
                command_name=request.command_name,
                granularity=request.granularity,
                include=request.include,
                json_output=request.json_output,
                raise_on_abort=request.raise_on_abort,
            )
        )


def _execute_translate_session(*, context: TranslateSessionContext, session: Any) -> Any:
    try:
        cli._update_run_context(
            context.repository,
            run_id=session.run_id,
            scope="default",
            granularity=context.request.granularity,
        )
        result = _execute_translate_runner(
            request=TranslateRunnerRequest(
                repository=context.repository,
                settings=context.settings,
                granularity=context.request.granularity,
                include=context.request.include,
                run_id=session.run_id,
                runner_attr=context.request.runner_attr,
                runner_kwargs=context.request.runner_kwargs,
            )
        )
        session.heartbeat_monitor.raise_if_failed()
        context.repository.finish_run(session.run_id, success=not bool(result.aborted))
        return result
    except KeyboardInterrupt as exc:
        _handle_translate_interrupt(context=context, session=session, exc=exc)
    except context.workspace_lease_lost_error as exc:
        _handle_translate_lease_loss(context=context, session=session, exc=exc)
    except Exception:
        _handle_translate_exception(context=context, session=session)


def _handle_translate_interrupt(
    *,
    context: TranslateSessionContext,
    session: Any,
    exc: KeyboardInterrupt,
) -> NoReturn:
    finish_run_safely(
        repository=context.repository,
        run_id=session.run_id,
        success=False,
        log=session.log,
        message="Run finish failed during interrupt",
    )
    cli._raise_typer_exit_for_interrupt(
        log=session.log,
        message=f"{context.request.command_name} interrupted".capitalize(),
        exc=exc,
    )


def _handle_translate_lease_loss(
    *,
    context: TranslateSessionContext,
    session: Any,
    exc: BaseException,
) -> NoReturn:
    finish_run_safely(
        repository=context.repository,
        run_id=session.run_id,
        success=False,
        log=session.log,
        message="Run finish failed after lease loss",
    )
    session.log.warning(
        "{} stopped because workspace lease was lost error_type={} error={}",
        context.request.command_name.capitalize(),
        type(exc).__name__,
        str(exc),
    )
    raise cli.typer.Exit(code=1) from None


def _handle_translate_exception(*, context: TranslateSessionContext, session: Any) -> NoReturn:
    context.repository.finish_run(session.run_id, success=False)
    session.log.exception("{} failed", context.request.command_name.capitalize())
    raise


def _execute_translate_runner(*, request: TranslateRunnerRequest) -> Any:
    runner = cli._import_symbol("recoleta.translation", attr_name=request.runner_attr)
    with cli._graceful_shutdown_signals():
        return runner(
            repository=request.repository,
            settings=request.settings,
            granularity=request.granularity,
            include=request.include,
            run_id=request.run_id,
            **request.runner_kwargs,
        )


def _emit_translate_result(*, context: TranslateResultContext) -> None:
    if context.json_output:
        cli._emit_json(
            {
                "status": "aborted" if context.result.aborted else "ok",
                "command": context.command_name,
                "run_id": context.run_id,
                "db_path": str(context.resolved_db_path),
                "granularity": context.granularity,
                "include": context.include,
                "aborted": context.result.aborted,
                "abort_reason": context.result.abort_reason,
                "totals": {
                    "scanned": context.result.scanned_total,
                    "translated": context.result.translated_total,
                    "mirrored": context.result.mirrored_total,
                    "skipped": context.result.skipped_total,
                    "failed": context.result.failed_total,
                },
                "billing": cli._billing_summary_payload(context.metrics),
            }
        )
        return
    if context.result.aborted:
        context.console.print(
            f"[yellow]{context.command_name} aborted[/yellow] "
            f"translated={context.result.translated_total} "
            f"skipped={context.result.skipped_total} "
            f"failed={context.result.failed_total} "
            f"reason={context.result.abort_reason}"
        )
        cli._print_billing_report(
            console=context.console,
            repository=context.repository,
            run_id=context.run_id,
        )
        if context.raise_on_abort:
            raise RuntimeError(str(context.result.abort_reason or "translation aborted"))
        return
    context.console.print(
        f"[green]{context.command_name} completed[/green] "
        f"translated={context.result.translated_total} "
        f"skipped={context.result.skipped_total} "
        f"failed={context.result.failed_total}"
    )
    cli._print_billing_report(
        console=context.console,
        repository=context.repository,
        run_id=context.run_id,
    )
