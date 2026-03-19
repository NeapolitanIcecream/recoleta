from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import recoleta.cli as cli


def _load_settings_for_translate(
    *,
    db_path: Path | None,
    config_path: Path | None,
) -> tuple[Path, object, object, object]:
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
    scope: str,
    granularity: str | None,
    include: str,
    limit: int | None,
    force: bool,
    context_assist: str,
    json_output: bool = False,
) -> None:
    (
        resolved_db_path,
        settings,
        repository,
        console,
    ) = _load_settings_for_translate(db_path=db_path, config_path=config_path)
    console = cast(Any, console)

    owner_token, lease_log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="translate run",
        log_module="cli.translate.run",
    )
    try:
        run_translation = cli._import_symbol(
            "recoleta.translation",
            attr_name="run_translation",
        )
        result = run_translation(
            repository=repository,
            settings=settings,
            scope=scope,
            granularity=granularity,
            include=include,
            limit=limit,
            force=force,
            context_assist=context_assist,
        )
        heartbeat_monitor.raise_if_failed()
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=lease_log,
        )

    if json_output:
        cli._emit_json(
            {
                "status": "aborted" if result.aborted else "ok",
                "command": "translate run",
                "db_path": str(resolved_db_path),
                "scope": scope,
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
            }
        )
        return

    if result.aborted:
        console.print(
            "[yellow]translate run aborted[/yellow] "
            f"translated={result.translated_total} "
            f"skipped={result.skipped_total} "
            f"failed={result.failed_total} "
            f"reason={result.abort_reason}"
        )
        return

    console.print(
        "[green]translate run completed[/green] "
        f"translated={result.translated_total} "
        f"skipped={result.skipped_total} "
        f"failed={result.failed_total}"
    )


def run_translate_backfill_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    scope: str,
    granularity: str | None,
    include: str,
    limit: int | None,
    force: bool,
    context_assist: str,
    legacy_source_language: str | None,
    emit_mirror_targets: bool,
    all_history: bool,
    json_output: bool = False,
) -> None:
    (
        resolved_db_path,
        settings,
        repository,
        console,
    ) = _load_settings_for_translate(db_path=db_path, config_path=config_path)
    console = cast(Any, console)

    owner_token, lease_log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="translate backfill",
        log_module="cli.translate.backfill",
    )
    try:
        run_translation_backfill = cli._import_symbol(
            "recoleta.translation",
            attr_name="run_translation_backfill",
        )
        result = run_translation_backfill(
            repository=repository,
            settings=settings,
            scope=scope,
            granularity=granularity,
            include=include,
            limit=limit,
            force=force,
            context_assist=context_assist,
            legacy_source_language=legacy_source_language,
            emit_mirror_targets=emit_mirror_targets,
            all_history=all_history,
        )
        heartbeat_monitor.raise_if_failed()
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=lease_log,
        )

    if json_output:
        cli._emit_json(
            {
                "status": "aborted" if result.aborted else "ok",
                "command": "translate backfill",
                "db_path": str(resolved_db_path),
                "scope": scope,
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
            }
        )
        return

    if result.aborted:
        console.print(
            "[yellow]translate backfill aborted[/yellow] "
            f"translated={result.translated_total} "
            f"mirrored={result.mirrored_total} "
            f"skipped={result.skipped_total} "
            f"failed={result.failed_total} "
            f"reason={result.abort_reason}"
        )
        return

    console.print(
        "[green]translate backfill completed[/green] "
        f"translated={result.translated_total} "
        f"mirrored={result.mirrored_total} "
        f"skipped={result.skipped_total} "
        f"failed={result.failed_total}"
    )
