from __future__ import annotations

import recoleta.cli as cli


def run_publish_command(*, limit: int) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]

    settings, _, _, result = cli._execute_stage(
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
