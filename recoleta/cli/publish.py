from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import recoleta.cli as cli
from recoleta.trends import day_period_bounds


@dataclass(frozen=True, slots=True)
class PublishPayloadContext:
    settings: Any
    run_id: str
    result: Any
    limit: int
    period_start: datetime | None
    period_end: datetime | None


def run_publish_command(
    *,
    limit: int,
    anchor_date: str | None = None,
    json_output: bool = False,
) -> None:
    period_start, period_end = _publish_window(anchor_date)
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
        scope="default",
        period_start=period_start,
        period_end=period_end,
    )
    if json_output:
        cli._emit_json(
            _publish_json_payload(
                context=PublishPayloadContext(
                    settings=settings,
                    run_id=run_id,
                    result=result,
                    limit=limit,
                    period_start=period_start,
                    period_end=period_end,
                )
            )
        )
        return
    _print_publish_summary(
        settings=settings,
        result=result,
        console=cli._runtime_symbols()["Console"](stderr=settings.log_json),
    )


def _publish_window(anchor_date: str | None) -> tuple[datetime | None, datetime | None]:
    if anchor_date is None or not str(anchor_date).strip():
        return None, None
    parsed_anchor = cli._parse_anchor_date_option(str(anchor_date).strip())
    period_start, period_end = day_period_bounds(parsed_anchor)
    return period_start.astimezone(timezone.utc), period_end.astimezone(timezone.utc)


def _publish_json_payload(
    *,
    context: PublishPayloadContext,
) -> dict[str, object]:
    publish_targets = list(getattr(context.settings, "publish_targets", []) or [])
    return {
        "status": "ok",
        "command": "publish",
        "run_id": context.run_id,
        "limit": context.limit,
        "sent": int(getattr(context.result, "sent", 0) or 0),
        "skipped": int(getattr(context.result, "skipped", 0) or 0),
        "failed": int(getattr(context.result, "failed", 0) or 0),
        "period_start": cli._isoformat_or_none(context.period_start),
        "period_end": cli._isoformat_or_none(context.period_end),
        "targets": publish_targets,
        "note_paths": [
            path
            for path in (
                cli._path_or_none(note_path)
                for note_path in getattr(context.result, "note_paths", []) or []
            )
            if path is not None
        ],
        "markdown_output_dir": _markdown_output_dir(
            settings=context.settings,
            publish_targets=publish_targets,
        ),
        "latest_index_path": _latest_index_path(
            settings=context.settings,
            publish_targets=publish_targets,
        ),
        "obsidian_inbox_path": _obsidian_inbox_path(
            settings=context.settings,
            publish_targets=publish_targets,
        ),
    }


def _markdown_output_dir(*, settings: Any, publish_targets: list[str]) -> str | None:
    markdown_output_dir = getattr(settings, "markdown_output_dir", None)
    if "markdown" not in publish_targets or markdown_output_dir is None:
        return None
    return cli._path_or_none(markdown_output_dir)


def _latest_index_path(*, settings: Any, publish_targets: list[str]) -> str | None:
    markdown_output_dir = getattr(settings, "markdown_output_dir", None)
    if "markdown" not in publish_targets or markdown_output_dir is None:
        return None
    return cli._path_or_none(markdown_output_dir / "latest.md")


def _obsidian_inbox_path(*, settings: Any, publish_targets: list[str]) -> str | None:
    obsidian_vault_path = getattr(settings, "obsidian_vault_path", None)
    if "obsidian" not in publish_targets or obsidian_vault_path is None:
        return None
    obsidian_base_folder = str(getattr(settings, "obsidian_base_folder", "") or "")
    return cli._path_or_none(obsidian_vault_path / obsidian_base_folder / "Inbox")


def _print_publish_summary(*, settings: Any, result: Any, console: Any) -> None:
    console.print(
        f"[green]publish completed[/green] "
        f"sent={result.sent} skipped={result.skipped} failed={result.failed}"
    )
    publish_targets = list(getattr(settings, "publish_targets", []) or [])
    if "markdown" in publish_targets:
        console.print(f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}")
        console.print(
            f"[cyan]latest index[/cyan] {settings.markdown_output_dir / 'latest.md'}"
        )
    if "obsidian" in publish_targets and settings.obsidian_vault_path is not None:
        console.print(
            f"[cyan]obsidian notes[/cyan] "
            f"{settings.obsidian_vault_path / settings.obsidian_base_folder / 'Inbox'}"
        )
