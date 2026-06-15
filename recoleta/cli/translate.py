from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, NoReturn, cast

import recoleta.cli as cli
from recoleta.cli.command_support import (
    build_console,
    emit_command_error,
    finish_run_safely,
    load_billing_metrics,
    load_runtime,
    managed_run_for_settings,
    RuntimeLoadRequest,
)
from recoleta.trends import day_period_bounds, month_period_bounds, week_period_bounds


@dataclass(frozen=True, slots=True)
class TranslateCommandRequest:
    db_path: Path | None
    config_path: Path | None
    granularity: str | None
    include: str
    period_start: datetime | None
    period_end: datetime | None
    all_history: bool
    json_output: bool
    command_name: str
    raise_on_abort: bool
    log_module: str
    runner_attr: str
    runner_kwargs: dict[str, Any]
    json_fields: dict[str, Any]
    show_mirrored_total: bool = False


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
    json_fields: dict[str, Any]
    show_mirrored_total: bool


@dataclass(frozen=True, slots=True)
class TranslateSessionContext:
    request: TranslateCommandRequest
    resolved_db_path: Path
    repository: Any
    settings: Any
    console: Any
    workspace_lease_lost_error: type[BaseException]


@dataclass(frozen=True, slots=True)
class TranslateRunScope:
    period_start: datetime | None
    period_end: datetime | None
    all_history: bool


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
    scope = _resolve_translate_run_scope(
        date=kwargs.get("date"),
        period_start=kwargs.get("period_start"),
        period_end=kwargs.get("period_end"),
        granularity=kwargs.get("granularity"),
        force=bool(kwargs.get("force", False)),
        all_history=bool(kwargs.get("all_history", False)),
        json_output=bool(kwargs.get("json_output", False)),
        command_name=str(kwargs.get("command_name", "translate run")),
    )
    _run_translate_command(
        request=TranslateCommandRequest(
            db_path=kwargs.get("db_path"),
            config_path=kwargs.get("config_path"),
            granularity=kwargs.get("granularity"),
            include=str(kwargs["include"]),
            period_start=scope.period_start,
            period_end=scope.period_end,
            all_history=scope.all_history,
            json_output=bool(kwargs.get("json_output", False)),
            command_name=str(kwargs.get("command_name", "translate run")),
            raise_on_abort=bool(kwargs.get("raise_on_abort", False)),
            log_module="cli.translate.run",
            runner_attr="run_translation",
            runner_kwargs={
                "limit": kwargs.get("limit"),
                "force": bool(kwargs.get("force", False)),
                "context_assist": kwargs["context_assist"],
                "period_start": scope.period_start,
                "period_end": scope.period_end,
                "all_history": scope.all_history,
            },
            json_fields={
                "period_start": _datetime_isoformat(scope.period_start),
                "period_end": _datetime_isoformat(scope.period_end),
                "all_history": scope.all_history,
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
            period_start=None,
            period_end=None,
            all_history=bool(kwargs.get("all_history", False)),
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
            json_fields={
                "legacy_source_language": kwargs.get("legacy_source_language"),
                "emit_mirror_targets": bool(kwargs.get("emit_mirror_targets", False)),
                "all_history": bool(kwargs.get("all_history", False)),
            },
            show_mirrored_total=True,
        )
    )


def _run_translate_command(*, request: TranslateCommandRequest) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = cast(
        type[BaseException], symbols["WorkspaceLeaseLostError"]
    )
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
                json_fields=_resolved_translate_json_fields(
                    request=request,
                    settings=context.settings,
                ),
                show_mirrored_total=request.show_mirrored_total,
            )
        )


def _execute_translate_session(
    *, context: TranslateSessionContext, session: Any
) -> Any:
    try:
        cli._update_run_context(
            context.repository,
            run_id=session.run_id,
            scope="default",
            granularity=context.request.granularity,
            period_start=context.request.period_start,
            period_end=context.request.period_end,
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
        if not bool(result.aborted):
            cli._import_symbol(
                "recoleta.translation",
                attr_name="materialize_localized_projections",
            )(
                repository=context.repository,
                settings=context.settings,
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


def _handle_translate_exception(
    *, context: TranslateSessionContext, session: Any
) -> NoReturn:
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


def _resolve_translate_run_scope(
    *,
    date: Any,
    period_start: Any,
    period_end: Any,
    granularity: Any,
    force: bool,
    all_history: bool,
    json_output: bool,
    command_name: str,
) -> TranslateRunScope:
    raw_date = str(date or "").strip()
    raw_period_start = str(period_start or "").strip()
    raw_period_end = str(period_end or "").strip()
    has_date = bool(raw_date)
    has_period_bound = bool(raw_period_start or raw_period_end)
    if all_history and (has_date or has_period_bound):
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message="--all-history cannot be combined with --date or --period-start/--period-end",
        )
    if has_date and has_period_bound:
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message="--date cannot be combined with --period-start/--period-end",
        )
    if bool(raw_period_start) != bool(raw_period_end):
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message="--period-start and --period-end must be provided together",
        )
    resolved_period_start: datetime | None = None
    resolved_period_end: datetime | None = None
    if has_date:
        resolved_period_start, resolved_period_end = _date_translate_window(
            raw_date=raw_date,
            granularity=granularity,
            command_name=command_name,
            json_output=json_output,
        )
    elif has_period_bound:
        resolved_period_start = _parse_translate_period_bound(
            value=raw_period_start,
            option_name="--period-start",
            command_name=command_name,
            json_output=json_output,
        )
        resolved_period_end = _parse_translate_period_bound(
            value=raw_period_end,
            option_name="--period-end",
            command_name=command_name,
            json_output=json_output,
        )
        if resolved_period_start >= resolved_period_end:
            _fail_translate_scope(
                command_name=command_name,
                json_output=json_output,
                message="--period-start must be before --period-end",
            )
    has_window = resolved_period_start is not None or resolved_period_end is not None
    if force and not has_window and not all_history:
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message=(
                "--force requires --date or --period-start/--period-end; "
                "use --all-history to force a full historical rerun. "
                "--granularity is not a date filter."
            ),
        )
    return TranslateRunScope(
        period_start=resolved_period_start,
        period_end=resolved_period_end,
        all_history=all_history or not has_window,
    )


def _date_translate_window(
    *,
    raw_date: str,
    granularity: Any,
    command_name: str,
    json_output: bool,
) -> tuple[datetime, datetime]:
    try:
        anchor = cli._parse_anchor_date_option(raw_date)
    except Exception:
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message="invalid --date: expected YYYY-MM-DD or YYYYMMDD",
        )
    normalized_granularity = str(granularity or "").strip().lower() or "day"
    if normalized_granularity == "day":
        return day_period_bounds(anchor)
    if normalized_granularity == "week":
        return week_period_bounds(anchor)
    if normalized_granularity == "month":
        return month_period_bounds(anchor)
    _fail_translate_scope(
        command_name=command_name,
        json_output=json_output,
        message="--date requires --granularity to be day, week, or month",
    )


def _parse_translate_period_bound(
    *,
    value: str,
    option_name: str,
    command_name: str,
    json_output: bool,
) -> datetime:
    raw = str(value or "").strip()
    try:
        if "T" not in raw and " " not in raw:
            parsed = datetime.fromisoformat(raw)
        else:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        _fail_translate_scope(
            command_name=command_name,
            json_output=json_output,
            message=f"invalid {option_name}: expected ISO date or datetime",
        )
    if parsed.tzinfo is None or parsed.tzinfo.utcoffset(parsed) is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _fail_translate_scope(
    *,
    command_name: str,
    json_output: bool,
    message: str,
) -> NoReturn:
    emit_command_error(
        command_name=command_name,
        message=message,
        console=build_console(),
        json_output=json_output,
        exit_code=2,
    )


def _datetime_isoformat(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _resolved_translate_json_fields(
    *,
    request: TranslateCommandRequest,
    settings: Any,
) -> dict[str, Any]:
    if "legacy_source_language" not in request.json_fields:
        return dict(request.json_fields)
    configured_language = str(
        getattr(
            getattr(settings, "localization", None),
            "legacy_backfill_source_language_code",
            "",
        )
        or ""
    ).strip()
    if not configured_language:
        return dict(request.json_fields)
    requested_language = str(
        request.json_fields.get("legacy_source_language") or ""
    ).strip()
    if requested_language:
        return dict(request.json_fields)
    return {
        **request.json_fields,
        "legacy_source_language": configured_language,
    }


def _translate_json_status(result: Any) -> str:
    if bool(result.aborted):
        return "aborted"
    if int(result.failed_total or 0) > 0:
        return "partial_failure"
    return "ok"


def _emit_translate_result(*, context: TranslateResultContext) -> None:
    if context.json_output:
        cli._emit_json(
            {
                "status": _translate_json_status(context.result),
                "command": context.command_name,
                "run_id": context.run_id,
                "db_path": str(context.resolved_db_path),
                "granularity": context.granularity,
                "include": context.include,
                **context.json_fields,
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
            f"{_translate_result_totals_text(context=context)} "
            f"reason={context.result.abort_reason}"
        )
        cli._print_billing_report(
            console=context.console,
            repository=context.repository,
            run_id=context.run_id,
        )
        if context.raise_on_abort:
            raise RuntimeError(
                str(context.result.abort_reason or "translation aborted")
            )
        return
    context.console.print(
        f"[green]{context.command_name} completed[/green] "
        f"{_translate_result_totals_text(context=context)}"
    )
    cli._print_billing_report(
        console=context.console,
        repository=context.repository,
        run_id=context.run_id,
    )


def _translate_result_totals_text(*, context: TranslateResultContext) -> str:
    parts = [f"translated={context.result.translated_total}"]
    if context.show_mirrored_total:
        parts.append(f"mirrored={context.result.mirrored_total}")
    parts.extend(
        [
            f"skipped={context.result.skipped_total}",
            f"failed={context.result.failed_total}",
        ]
    )
    return " ".join(parts)
