from __future__ import annotations

import recoleta.cli as cli


def run_ingest_command() -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]

    settings, repository, run_id, result = cli._execute_stage(
        stage_name="ingest",
        stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )
    cli._print_ingest_html_document_summary(
        console=console,
        repository=repository,
        run_id=run_id,
    )
