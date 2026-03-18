from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import recoleta.cli as cli


def _parse_anchor_or_exit(*, anchor_date: str | None, console_cls: Any) -> date | None:
    parsed_anchor: date | None = None
    if anchor_date is not None and str(anchor_date).strip():
        raw_anchor = str(anchor_date).strip()
        try:
            parsed_anchor = cli._parse_anchor_date_option(raw_anchor)
        except Exception as exc:
            console = console_cls()
            console.print(
                f"[red]invalid date[/red] value={raw_anchor} expected=YYYY-MM-DD|YYYYMMDD"
            )
            raise cli.typer.Exit(code=2) from exc
    return parsed_anchor


def _print_ideas_result(
    *,
    console: Any,
    result: Any,
) -> None:
    if len(getattr(result, "stream_results", []) or []) > 1:
        console.print(
            "[green]ideas completed[/green] "
            f"streams={len(result.stream_results)} granularity={result.granularity} "
            f"period_start={result.period_start.isoformat()} period_end={result.period_end.isoformat()}"
        )
        for stream_result in result.stream_results:
            note_suffix = (
                f" note_path={Path(stream_result.note_path).as_posix()}"
                if getattr(stream_result, "note_path", None)
                else ""
            )
            console.print(
                f"[cyan]{stream_result.stream}[/cyan] "
                f"status={stream_result.status} pass_output_id={stream_result.pass_output_id}{note_suffix}"
            )
        return
    note_suffix = f" note_path={Path(result.note_path).as_posix()}" if result.note_path else ""
    console.print(
        "[green]ideas completed[/green] "
        f"status={result.status} pass_output_id={result.pass_output_id} "
        f"granularity={result.granularity} period_start={result.period_start.isoformat()} "
        f"period_end={result.period_end.isoformat()}{note_suffix}"
    )


def _serialize_ideas_result(result: Any) -> dict[str, Any]:
    stream_results = list(getattr(result, "stream_results", []) or [])
    payload: dict[str, Any] = {
        "pass_output_id": (
            int(getattr(result, "pass_output_id", 0) or 0)
            if getattr(result, "pass_output_id", None) is not None
            else None
        ),
        "upstream_pass_output_id": (
            int(getattr(result, "upstream_pass_output_id", 0) or 0)
            if getattr(result, "upstream_pass_output_id", None) is not None
            else None
        ),
        "granularity": str(getattr(result, "granularity", "") or ""),
        "period_start": cli._isoformat_or_none(getattr(result, "period_start", None)),
        "period_end": cli._isoformat_or_none(getattr(result, "period_end", None)),
        "title": str(getattr(result, "title", "") or ""),
        "status": str(getattr(result, "status", "") or ""),
        "note_path": cli._path_or_none(getattr(result, "note_path", None)),
        "stream": str(getattr(result, "stream", "") or "") or None,
    }
    if stream_results:
        payload["stream_results"] = [
            _serialize_ideas_result(child) for child in stream_results
        ]
        payload["stream_results_total"] = len(stream_results)
    return payload


def run_ideas_command(
    *,
    granularity: str,
    anchor_date: str | None,
    model: str | None,
    json_output: bool = False,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=anchor_date,
        console_cls=console_cls,
    )
    settings, repository, run_id, result = cli._execute_stage(
        stage_name="ideas",
        stage_runner=lambda service, run_id: service.ideas(
            run_id=run_id,
            granularity=granularity,
            anchor_date=parsed_anchor,
            llm_model=model,
        ),
    )
    cli._update_run_context(
        repository,
        run_id=run_id,
        command="ideas",
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
        result_payload = _serialize_ideas_result(result)
        result_status = result_payload.pop("status", None)
        metrics = repository.list_metrics(run_id=run_id)
        payload = {
            "status": "ok",
            "command": "ideas",
            "run_id": run_id,
            "result_status": result_status,
            "billing": cli._billing_summary_payload(metrics),
            **result_payload,
        }
        cli._emit_json(payload)
        return
    console = console_cls(stderr=settings.log_json)
    _print_ideas_result(console=console, result=result)
    cli._print_billing_report(console=console, repository=repository, run_id=run_id)
