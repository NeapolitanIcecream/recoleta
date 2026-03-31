from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, cast

from rich.table import Table


@dataclass(frozen=True, slots=True)
class _BillingComponentSpec:
    key: str
    label: str
    calls_metric: str
    input_tokens_metric: str | None
    output_tokens_metric: str | None
    cost_metric: str | None
    cost_missing_metric: str | None


_COMPONENT_SPECS: tuple[_BillingComponentSpec, ...] = (
    _BillingComponentSpec(
        key="triage_embeddings",
        label="Triage embeddings",
        calls_metric="pipeline.triage.embedding_calls_total",
        input_tokens_metric="pipeline.triage.embedding_prompt_tokens_total",
        output_tokens_metric=None,
        cost_metric="pipeline.triage.estimated_cost_usd",
        cost_missing_metric="pipeline.triage.cost_missing_total",
    ),
    _BillingComponentSpec(
        key="analyze_llm",
        label="Analyze LLM",
        calls_metric="pipeline.analyze.llm_calls_total",
        input_tokens_metric="pipeline.analyze.llm_prompt_tokens_total",
        output_tokens_metric="pipeline.analyze.llm_completion_tokens_total",
        cost_metric="pipeline.analyze.estimated_cost_usd",
        cost_missing_metric="pipeline.analyze.cost_missing_total",
    ),
    _BillingComponentSpec(
        key="trends_embeddings",
        label="Trends embeddings",
        calls_metric="pipeline.trends.embedding_calls_total",
        input_tokens_metric="pipeline.trends.embedding_prompt_tokens_total",
        output_tokens_metric=None,
        cost_metric="pipeline.trends.embedding_estimated_cost_usd",
        cost_missing_metric="pipeline.trends.embedding_cost_missing_total",
    ),
    _BillingComponentSpec(
        key="trends_llm",
        label="Trends LLM",
        calls_metric="pipeline.trends.llm_requests_total",
        input_tokens_metric="pipeline.trends.llm_input_tokens_total",
        output_tokens_metric="pipeline.trends.llm_output_tokens_total",
        cost_metric="pipeline.trends.estimated_cost_usd",
        cost_missing_metric="pipeline.trends.cost_missing_total",
    ),
    _BillingComponentSpec(
        key="ideas_llm",
        label="Ideas LLM",
        calls_metric="pipeline.trends.pass.ideas.llm_requests_total",
        input_tokens_metric="pipeline.trends.pass.ideas.llm_input_tokens_total",
        output_tokens_metric="pipeline.trends.pass.ideas.llm_output_tokens_total",
        cost_metric="pipeline.trends.pass.ideas.estimated_cost_usd",
        cost_missing_metric="pipeline.trends.pass.ideas.cost_missing_total",
    ),
    _BillingComponentSpec(
        key="translation_llm",
        label="Translation LLM",
        calls_metric="pipeline.translate.llm_requests_total",
        input_tokens_metric="pipeline.translate.llm_input_tokens_total",
        output_tokens_metric="pipeline.translate.llm_output_tokens_total",
        cost_metric="pipeline.translate.estimated_cost_usd",
        cost_missing_metric="pipeline.translate.cost_missing_total",
    ),
    _BillingComponentSpec(
        key="translation_context_embeddings",
        label="Translation context embeddings",
        calls_metric="pipeline.translate.context.embedding_calls_total",
        input_tokens_metric="pipeline.translate.context.embedding_prompt_tokens_total",
        output_tokens_metric=None,
        cost_metric="pipeline.translate.context.embedding_estimated_cost_usd",
        cost_missing_metric="pipeline.translate.context.embedding_cost_missing_total",
    ),
    _BillingComponentSpec(
        key="rag_sync_embeddings",
        label="RAG sync embeddings",
        calls_metric="pipeline.rag.sync.embedding_calls_total",
        input_tokens_metric="pipeline.rag.sync.embedding_prompt_tokens_total",
        output_tokens_metric=None,
        cost_metric="pipeline.rag.sync.embedding_estimated_cost_usd",
        cost_missing_metric="pipeline.rag.sync.embedding_cost_missing_total",
    ),
    _BillingComponentSpec(
        key="doctor_llm",
        label="Doctor LLM",
        calls_metric="pipeline.doctor.llm.requests_total",
        input_tokens_metric="pipeline.doctor.llm.input_tokens_total",
        output_tokens_metric="pipeline.doctor.llm.output_tokens_total",
        cost_metric="pipeline.doctor.llm.estimated_cost_usd",
        cost_missing_metric="pipeline.doctor.llm.cost_missing_total",
    ),
)


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


def _json_number(value: float | None) -> int | float | None:
    if value is None:
        return None
    normalized = round(float(value), 12)
    if normalized.is_integer():
        return int(normalized)
    return normalized


def _metric_total(
    *,
    totals: dict[str, float],
    exact_name: str | None,
) -> float | None:
    if exact_name is None or exact_name not in totals:
        return None
    return float(totals[exact_name])


def _component_payload(
    *,
    calls: float | None,
    input_tokens: float | None,
    output_tokens: float | None,
    cost_usd: float | None,
    cost_missing: float | None,
) -> dict[str, int | float | None] | None:
    if all(
        value is None
        for value in (calls, input_tokens, output_tokens, cost_usd, cost_missing)
    ):
        return None
    return {
        "calls": _json_number(calls),
        "input_tokens": _json_number(input_tokens),
        "output_tokens": _json_number(output_tokens),
        "cost_usd": _json_number(cost_usd),
        "cost_missing": _json_number(cost_missing),
    }


def summarize_billing_metrics(metrics: Iterable[Any]) -> dict[str, Any] | None:
    totals = _sum_metrics(metrics)

    components: dict[str, dict[str, int | float | None]] = {}
    total_cost_usd = 0.0
    any_cost = False
    for spec in _COMPONENT_SPECS:
        payload = _component_payload(
            calls=_metric_total(
                totals=totals,
                exact_name=spec.calls_metric,
            ),
            input_tokens=_metric_total(
                totals=totals,
                exact_name=spec.input_tokens_metric,
            ),
            output_tokens=_metric_total(
                totals=totals,
                exact_name=spec.output_tokens_metric,
            ),
            cost_usd=_metric_total(
                totals=totals,
                exact_name=spec.cost_metric,
            ),
            cost_missing=_metric_total(
                totals=totals,
                exact_name=spec.cost_missing_metric,
            ),
        )
        if payload is None:
            continue
        components[spec.key] = payload
        raw_cost = payload.get("cost_usd")
        if isinstance(raw_cost, (int, float)):
            total_cost_usd += float(raw_cost)
            any_cost = True

    if not components:
        return None

    summary: dict[str, Any] = {
        "components": components,
        "total_cost_usd": _json_number(total_cost_usd) if any_cost else None,
    }
    return summary


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
    summary = summarize_billing_metrics(metrics)

    table = Table(title=title)
    table.add_column("Component", no_wrap=True)
    table.add_column("Calls", justify="right")
    table.add_column("Input tokens", justify="right")
    table.add_column("Output tokens", justify="right")
    table.add_column("Cost (USD)", justify="right")
    table.add_column("Cost missing", justify="right")
    if summary is None:
        table.add_row("No billing metrics recorded", "-", "-", "-", "-", "-")
        return table

    for spec in _COMPONENT_SPECS:
        component = summary["components"].get(spec.key)
        if not isinstance(component, dict):
            continue
        table.add_row(
            spec.label,
            _fmt_int(cast(float | None, component.get("calls"))),
            _fmt_int(cast(float | None, component.get("input_tokens"))),
            _fmt_int(cast(float | None, component.get("output_tokens"))),
            _fmt_usd(cast(float | None, component.get("cost_usd"))),
            _fmt_int(cast(float | None, component.get("cost_missing"))),
        )
    total_cost_usd = summary.get("total_cost_usd")
    if isinstance(total_cost_usd, (int, float)):
        table.add_section()
        table.add_row("Total", "-", "-", "-", _fmt_usd(float(total_cost_usd)), "-")
    return table
