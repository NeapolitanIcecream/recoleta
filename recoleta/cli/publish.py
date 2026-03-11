from __future__ import annotations

from datetime import datetime, timezone

import recoleta.cli as cli
from recoleta.trends import day_period_bounds


def run_publish_command(*, limit: int, anchor_date: str | None = None) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    period_start: datetime | None = None
    period_end: datetime | None = None
    if anchor_date is not None and str(anchor_date).strip():
        parsed_anchor = cli._parse_anchor_date_option(str(anchor_date).strip())
        period_start, period_end = day_period_bounds(parsed_anchor)
        period_start = period_start.astimezone(timezone.utc)
        period_end = period_end.astimezone(timezone.utc)

    settings, _, _, result = cli._execute_stage(
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
