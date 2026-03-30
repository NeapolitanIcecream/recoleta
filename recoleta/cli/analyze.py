from __future__ import annotations

from datetime import datetime, timezone

import recoleta.cli as cli
from recoleta.trends import day_period_bounds


def run_analyze_command(
    *,
    limit: int | None,
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
        stage_name="analyze",
        stage_runner=lambda service, run_id: cli._invoke_service_method(
            service,
            "analyze",
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
    metrics = repository.list_metrics(run_id=run_id)
    if json_output:
        cli._emit_json(
            {
                "status": "ok",
                "command": "analyze",
                "run_id": run_id,
                "limit": limit,
                "processed": int(getattr(result, "processed", 0) or 0),
                "failed": int(getattr(result, "failed", 0) or 0),
                "period_start": cli._isoformat_or_none(period_start),
                "period_end": cli._isoformat_or_none(period_end),
                "billing": cli._billing_summary_payload(metrics),
            }
        )
        return
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]analyze completed[/green] processed={result.processed} failed={result.failed}"
    )
    cli._print_billing_report(console=console, repository=repository, run_id=run_id)
