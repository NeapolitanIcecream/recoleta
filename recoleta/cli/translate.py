from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import recoleta.cli as cli


def _load_settings_for_translate(
    *,
    db_path: Path | None,
    config_path: Path | None,
) -> tuple[Path, Any, Any, Any]:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved_db_path = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    try:
        settings = cli._build_settings(
            config_path=config_path,
            db_path=resolved_db_path,
        )
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]settings load failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    console = console_cls(stderr=getattr(settings, "log_json", False))
    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    repository.init_schema()
    return resolved_db_path, settings, repository, console


def run_translate_run_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    granularity: str | None,
    include: str,
    limit: int | None,
    force: bool,
    context_assist: str,
    json_output: bool = False,
    command_name: str = "translate run",
    raise_on_abort: bool = False,
) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]
    (
        resolved_db_path,
        settings,
        repository,
        console,
    ) = _load_settings_for_translate(db_path=db_path, config_path=config_path)
    repository = cast(Any, repository)
    settings = cast(Any, settings)
    console = cast(Any, console)

    run_id, owner_token, run_log, heartbeat_monitor = cli._begin_managed_run_for_settings(
        settings=settings,
        repository=repository,
        console=console,
        command=command_name,
        log_module="cli.translate.run",
    )
    metrics: list[Any] = []
    try:
        cli._update_run_context(
            repository,
            run_id=run_id,
            scope="default",
            granularity=granularity,
        )
        run_translation = cli._import_symbol(
            "recoleta.translation",
            attr_name="run_translation",
        )
        with cli._graceful_shutdown_signals():
            result = run_translation(
                repository=repository,
                settings=settings,
                granularity=granularity,
                include=include,
                limit=limit,
                force=force,
                context_assist=context_assist,
                run_id=run_id,
            )
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=not bool(result.aborted))
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            run_log.exception("Run finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=run_log,
            message="Translate run interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            run_log.exception("Run finish failed after lease loss")
        run_log.warning(
            "Translate run stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        run_log.exception("Translate run failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=run_log,
        )
    try:
        metrics = repository.list_metrics(run_id=run_id)
    except Exception as exc:  # noqa: BLE001
        run_log.warning(
            "Translate run billing metrics load failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )

    if json_output:
        cli._emit_json(
            {
                "status": "aborted" if result.aborted else "ok",
                "command": command_name,
                "run_id": run_id,
                "db_path": str(resolved_db_path),
                "granularity": granularity,
                "include": include,
                "aborted": result.aborted,
                "abort_reason": result.abort_reason,
                "totals": {
                    "scanned": result.scanned_total,
                    "translated": result.translated_total,
                    "mirrored": result.mirrored_total,
                    "skipped": result.skipped_total,
                    "failed": result.failed_total,
                },
                "billing": cli._billing_summary_payload(metrics),
            }
        )
        return

    if result.aborted:
        console.print(
            f"[yellow]{command_name} aborted[/yellow] "
            f"translated={result.translated_total} "
            f"skipped={result.skipped_total} "
            f"failed={result.failed_total} "
            f"reason={result.abort_reason}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
        if raise_on_abort:
            raise RuntimeError(str(result.abort_reason or "translation aborted"))
        return

    console.print(
        f"[green]{command_name} completed[/green] "
        f"translated={result.translated_total} "
        f"skipped={result.skipped_total} "
        f"failed={result.failed_total}"
    )
    cli._print_billing_report(console=console, repository=repository, run_id=run_id)


def run_translate_backfill_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    granularity: str | None,
    include: str,
    limit: int | None,
    force: bool,
    context_assist: str,
    legacy_source_language: str | None,
    emit_mirror_targets: bool,
    all_history: bool,
    json_output: bool = False,
    command_name: str = "translate backfill",
) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]
    (
        resolved_db_path,
        settings,
        repository,
        console,
    ) = _load_settings_for_translate(db_path=db_path, config_path=config_path)
    repository = cast(Any, repository)
    settings = cast(Any, settings)
    console = cast(Any, console)

    run_id, owner_token, run_log, heartbeat_monitor = cli._begin_managed_run_for_settings(
        settings=settings,
        repository=repository,
        console=console,
        command=command_name,
        log_module="cli.translate.backfill",
    )
    metrics: list[Any] = []
    try:
        cli._update_run_context(
            repository,
            run_id=run_id,
            scope="default",
            granularity=granularity,
        )
        run_translation_backfill = cli._import_symbol(
            "recoleta.translation",
            attr_name="run_translation_backfill",
        )
        with cli._graceful_shutdown_signals():
            result = run_translation_backfill(
                repository=repository,
                settings=settings,
                granularity=granularity,
                include=include,
                limit=limit,
                force=force,
                context_assist=context_assist,
                legacy_source_language=legacy_source_language,
                emit_mirror_targets=emit_mirror_targets,
                all_history=all_history,
                run_id=run_id,
            )
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=not bool(result.aborted))
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            run_log.exception("Run finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=run_log,
            message="Translate backfill interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            run_log.exception("Run finish failed after lease loss")
        run_log.warning(
            "Translate backfill stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        run_log.exception("Translate backfill failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=run_log,
        )
    try:
        metrics = repository.list_metrics(run_id=run_id)
    except Exception as exc:  # noqa: BLE001
        run_log.warning(
            "Translate backfill billing metrics load failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )

    if json_output:
        cli._emit_json(
            {
                "status": "aborted" if result.aborted else "ok",
                "command": command_name,
                "run_id": run_id,
                "db_path": str(resolved_db_path),
                "granularity": granularity,
                "include": include,
                "legacy_source_language": legacy_source_language,
                "emit_mirror_targets": emit_mirror_targets,
                "all_history": all_history,
                "aborted": result.aborted,
                "abort_reason": result.abort_reason,
                "totals": {
                    "scanned": result.scanned_total,
                    "translated": result.translated_total,
                    "mirrored": result.mirrored_total,
                    "skipped": result.skipped_total,
                    "failed": result.failed_total,
                },
                "billing": cli._billing_summary_payload(metrics),
            }
        )
        return

    if result.aborted:
        console.print(
            f"[yellow]{command_name} aborted[/yellow] "
            f"translated={result.translated_total} "
            f"mirrored={result.mirrored_total} "
            f"skipped={result.skipped_total} "
            f"failed={result.failed_total} "
            f"reason={result.abort_reason}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
        return

    console.print(
        f"[green]{command_name} completed[/green] "
        f"translated={result.translated_total} "
        f"mirrored={result.mirrored_total} "
        f"skipped={result.skipped_total} "
        f"failed={result.failed_total}"
    )
    cli._print_billing_report(console=console, repository=repository, run_id=run_id)
