from __future__ import annotations

from datetime import datetime, timezone

import recoleta.cli as cli
from recoleta.trends import day_period_bounds


def run_publish_command(
    *,
    limit: int,
    anchor_date: str | None = None,
    json_output: bool = False,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    period_start: datetime | None = None
    period_end: datetime | None = None
    if anchor_date is not None and str(anchor_date).strip():
        parsed_anchor = cli._parse_anchor_date_option(str(anchor_date).strip())
        period_start, period_end = day_period_bounds(parsed_anchor)
        period_start = period_start.astimezone(timezone.utc)
        period_end = period_end.astimezone(timezone.utc)

    settings, repository, run_id, result = cli._execute_stage(
        stage_name="publish",
        stage_runner=lambda service, run_id: cli._invoke_service_method(
            service,
            "publish",
            run_id=run_id,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
        ),
    )
    cli._update_run_context(
        repository,
        run_id=run_id,
        scope=None if cli._has_explicit_topic_streams(settings) else "default",
        period_start=period_start,
        period_end=period_end,
    )
    if json_output:
        publish_targets = list(getattr(settings, "publish_targets", []) or [])
        markdown_output_dir = getattr(settings, "markdown_output_dir", None)
        obsidian_vault_path = getattr(settings, "obsidian_vault_path", None)
        obsidian_base_folder = str(getattr(settings, "obsidian_base_folder", "") or "")
        cli._emit_json(
            {
                "status": "ok",
                "command": "publish",
                "run_id": run_id,
                "limit": limit,
                "sent": int(getattr(result, "sent", 0) or 0),
                "skipped": int(getattr(result, "skipped", 0) or 0),
                "failed": int(getattr(result, "failed", 0) or 0),
                "period_start": cli._isoformat_or_none(period_start),
                "period_end": cli._isoformat_or_none(period_end),
                "targets": publish_targets,
                "note_paths": [
                    path
                    for path in (
                        cli._path_or_none(note_path)
                        for note_path in getattr(result, "note_paths", []) or []
                    )
                    if path is not None
                ],
                "markdown_output_dir": (
                    cli._path_or_none(markdown_output_dir)
                    if "markdown" in publish_targets and markdown_output_dir is not None
                    else None
                ),
                "latest_index_path": (
                    cli._path_or_none(markdown_output_dir / "latest.md")
                    if "markdown" in publish_targets and markdown_output_dir is not None
                    else None
                ),
                "obsidian_inbox_path": (
                    cli._path_or_none(
                        obsidian_vault_path
                        / obsidian_base_folder
                        / "Inbox"
                    )
                    if "obsidian" in publish_targets and obsidian_vault_path is not None
                    else None
                ),
            }
        )
        return
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
