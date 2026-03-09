from __future__ import annotations

import recoleta.cli as cli


def run_analyze_command(*, limit: int | None) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]

    settings, _, _, result = cli._execute_stage(
        stage_name="analyze",
        stage_runner=lambda service, run_id: service.analyze(
            run_id=run_id, limit=limit
        ),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]analyze completed[/green] processed={result.processed} failed={result.failed}"
    )
