from __future__ import annotations

from datetime import date
from typing import Any

import recoleta.cli as cli


def _parse_anchor_or_exit(*, anchor_date: str | None, console_cls: Any) -> date | None:
    parsed_anchor: date | None = None
    if anchor_date is not None and str(anchor_date).strip():
        raw_anchor = str(anchor_date).strip()
        try:
            parsed_anchor = cli._parse_anchor_date_option(raw_anchor)
        except Exception as exc:  # noqa: BLE001
            console = console_cls()
            console.print(
                f"[red]invalid date[/red] value={raw_anchor} expected=YYYY-MM-DD|YYYYMMDD"
            )
            raise cli.typer.Exit(code=2) from exc
    return parsed_anchor


def _print_trends_result(
    *,
    console: Any,
    result: Any,
) -> None:
    if len(getattr(result, "stream_results", []) or []) > 1:
        console.print(
            "[green]trends completed[/green] "
            f"streams={len(result.stream_results)} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
        for stream_result in result.stream_results:
            console.print(
                f"[cyan]{stream_result.stream}[/cyan] "
                f"doc_id={stream_result.doc_id}"
            )
        return
    console.print(
        "[green]trends completed[/green] "
        f"doc_id={result.doc_id} granularity={result.granularity} "
        f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
    )


def _serialize_trends_result(result: Any) -> dict[str, Any]:
    stream_results = list(getattr(result, "stream_results", []) or [])
    payload: dict[str, Any] = {
        "doc_id": int(getattr(result, "doc_id", 0) or 0),
        "pass_output_id": (
            int(getattr(result, "pass_output_id", 0) or 0)
            if getattr(result, "pass_output_id", None) is not None
            else None
        ),
        "granularity": str(getattr(result, "granularity", "") or ""),
        "period_start": cli._isoformat_or_none(getattr(result, "period_start", None)),
        "period_end": cli._isoformat_or_none(getattr(result, "period_end", None)),
        "title": str(getattr(result, "title", "") or ""),
        "stream": str(getattr(result, "stream", "") or "") or None,
    }
    if stream_results:
        payload["stream_results"] = [
            _serialize_trends_result(child) for child in stream_results
        ]
        payload["stream_results_total"] = len(stream_results)
    return payload


def run_trends_command(
    *,
    granularity: str,
    anchor_date: str | None,
    model: str | None,
    backfill: bool,
    backfill_mode: str,
    debug_pdf: bool,
    json_output: bool = False,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]

    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=anchor_date,
        console_cls=console_cls,
    )
    settings, repository, run_id, result = cli._execute_stage(
        stage_name="trends",
        stage_runner=lambda service, run_id: service.trends(
            run_id=run_id,
            granularity=granularity,
            anchor_date=parsed_anchor,
            llm_model=model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
        ),
    )
    cli._update_run_context(
        repository,
        run_id=run_id,
        command="trends",
        scope=(
            str(getattr(result, "stream", "") or "").strip() or "default"
            if not list(getattr(result, "stream_results", []) or [])
            else None
        ),
        granularity=str(getattr(result, "granularity", "") or "").strip() or None,
        period_start=getattr(result, "period_start", None),
        period_end=getattr(result, "period_end", None),
    )
    if json_output:
        metrics = repository.list_metrics(run_id=run_id)
        payload = {
            "status": "ok",
            "command": "trends",
            "run_id": run_id,
            "billing": cli._billing_summary_payload(metrics),
            **_serialize_trends_result(result),
        }
        cli._emit_json(payload)
        return
    console = console_cls(stderr=settings.log_json)
    _print_trends_result(console=console, result=result)
    cli._print_billing_report(console=console, repository=repository, run_id=run_id)
