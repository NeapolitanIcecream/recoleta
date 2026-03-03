from __future__ import annotations

from typing import Any, Iterable

from rich.table import Table


def _sum_metrics(metrics: Iterable[Any]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for metric in metrics:
        name = str(getattr(metric, "name", "") or "").strip()
        if not name:
            continue
        raw_value = getattr(metric, "value", None)
        if not isinstance(raw_value, (int, float)):
            continue
        totals[name] = float(totals.get(name, 0.0)) + float(raw_value)
    return totals


def _fmt_int(value: float | None) -> str:
    if value is None:
        return "-"
    try:
        return str(int(round(float(value))))
    except Exception:
        return "-"


def _fmt_usd(value: float | None) -> str:
    if value is None:
        return "-"
    try:
        v = float(value)
    except Exception:
        return "-"
    return f"${v:.6f}"


def build_billing_table(
    *, metrics: Iterable[Any], title: str = "Billing report"
) -> Table | None:
    totals = _sum_metrics(metrics)

    rows: list[tuple[str, str, str, str, str, str]] = []
    total_cost_usd = 0.0
    any_cost = False

    def metric(name: str) -> float | None:
        if name not in totals:
            return None
        return float(totals[name])

    spec = [
        (
            "Triage embeddings",
            "pipeline.triage.embedding_calls_total",
            "pipeline.triage.embedding_prompt_tokens_total",
            None,
            "pipeline.triage.estimated_cost_usd",
            "pipeline.triage.cost_missing_total",
        ),
        (
            "Analyze LLM",
            "pipeline.analyze.llm_calls_total",
            "pipeline.analyze.llm_prompt_tokens_total",
            "pipeline.analyze.llm_completion_tokens_total",
            "pipeline.analyze.estimated_cost_usd",
            "pipeline.analyze.cost_missing_total",
        ),
        (
            "Trends embeddings",
            "pipeline.trends.embedding_calls_total",
            "pipeline.trends.embedding_prompt_tokens_total",
            None,
            "pipeline.trends.embedding_estimated_cost_usd",
            "pipeline.trends.embedding_cost_missing_total",
        ),
        (
            "Trends LLM",
            "pipeline.trends.llm_requests_total",
            "pipeline.trends.llm_input_tokens_total",
            "pipeline.trends.llm_output_tokens_total",
            "pipeline.trends.estimated_cost_usd",
            "pipeline.trends.cost_missing_total",
        ),
    ]

    for (
        label,
        calls_name,
        prompt_tokens_name,
        completion_tokens_name,
        cost_name,
        cost_missing_name,
    ) in spec:
        calls = metric(calls_name)
        prompt_tokens = metric(prompt_tokens_name)
        completion_tokens = (
            metric(completion_tokens_name) if completion_tokens_name else None
        )
        cost = metric(cost_name)
        cost_missing = metric(cost_missing_name)
        if all(
            v is None
            for v in (calls, prompt_tokens, completion_tokens, cost, cost_missing)
        ):
            continue
        rows.append(
            (
                label,
                _fmt_int(calls),
                _fmt_int(prompt_tokens),
                _fmt_int(completion_tokens),
                _fmt_usd(cost),
                _fmt_int(cost_missing),
            )
        )
        if cost is not None:
            total_cost_usd += float(cost)
            any_cost = True

    table = Table(title=title)
    table.add_column("Component", no_wrap=True)
    table.add_column("Calls", justify="right")
    table.add_column("Input tokens", justify="right")
    table.add_column("Output tokens", justify="right")
    table.add_column("Cost (USD)", justify="right")
    table.add_column("Cost missing", justify="right")
    if not rows:
        table.add_row("No billing metrics recorded", "-", "-", "-", "-", "-")
        return table
    for r in rows:
        table.add_row(*r)
    if any_cost:
        table.add_section()
        table.add_row("Total", "-", "-", "-", _fmt_usd(total_cost_usd), "-")
    return table
