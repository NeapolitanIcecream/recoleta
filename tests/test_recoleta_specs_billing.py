from __future__ import annotations

import io
from types import SimpleNamespace

from rich.console import Console

from recoleta.billing import build_billing_table, summarize_billing_metrics


def _metric(name: str, value: float, unit: str = "count") -> SimpleNamespace:
    return SimpleNamespace(name=name, value=value, unit=unit)


def test_billing_summary_and_table_include_ideas_llm_metrics() -> None:
    metrics = [
        _metric("pipeline.trends.pass.ideas.llm_requests_total", 1),
        _metric("pipeline.trends.pass.ideas.llm_input_tokens_total", 120),
        _metric("pipeline.trends.pass.ideas.llm_output_tokens_total", 45),
        _metric("pipeline.trends.pass.ideas.estimated_cost_usd", 0.0042, "usd"),
    ]

    summary = summarize_billing_metrics(metrics)

    assert summary is not None
    assert summary["components"]["ideas_llm"]["calls"] == 1
    assert summary["components"]["ideas_llm"]["input_tokens"] == 120
    assert summary["components"]["ideas_llm"]["output_tokens"] == 45
    assert summary["components"]["ideas_llm"]["cost_usd"] == 0.0042
    assert summary["total_cost_usd"] == 0.0042

    table = build_billing_table(metrics=metrics)
    assert table is not None
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, width=120)
    console.print(table)
    rendered = buffer.getvalue()
    assert "Ideas LLM" in rendered
    assert "No billing metrics recorded" not in rendered


def test_billing_summary_ignores_legacy_scope_metrics() -> None:
    metrics = [
        _metric("pipeline.trends.llm_requests_total", 1),
        _metric("pipeline.trends.llm_input_tokens_total", 100),
        _metric("pipeline.trends.llm_output_tokens_total", 20),
        _metric("pipeline.trends.estimated_cost_usd", 0.01, "usd"),
        _metric("pipeline.trends.scope.agents_lab.llm_requests_total", 2),
        _metric("pipeline.trends.scope.agents_lab.llm_input_tokens_total", 200),
        _metric("pipeline.trends.scope.agents_lab.llm_output_tokens_total", 40),
        _metric("pipeline.trends.scope.agents_lab.estimated_cost_usd", 0.02, "usd"),
        _metric("pipeline.trends.scope.agents_lab.pass.ideas.llm_requests_total", 1),
        _metric("pipeline.trends.scope.agents_lab.pass.ideas.llm_input_tokens_total", 80),
        _metric("pipeline.trends.scope.agents_lab.pass.ideas.llm_output_tokens_total", 16),
        _metric(
            "pipeline.trends.scope.agents_lab.pass.ideas.estimated_cost_usd",
            0.008,
            "usd",
        ),
        _metric("pipeline.trends.scope.robotics.embedding_calls_total", 3),
        _metric("pipeline.trends.scope.robotics.embedding_prompt_tokens_total", 150),
        _metric(
            "pipeline.trends.scope.robotics.embedding_estimated_cost_usd",
            0.003,
            "usd",
        ),
    ]

    summary = summarize_billing_metrics(metrics)

    assert summary is not None
    assert summary["components"]["trends_llm"]["calls"] == 1
    assert summary["components"]["trends_llm"]["input_tokens"] == 100
    assert summary["components"]["trends_llm"]["output_tokens"] == 20
    assert summary["components"]["trends_llm"]["cost_usd"] == 0.01
    assert "ideas_llm" not in summary["components"]
    assert "trends_embeddings" not in summary["components"]
    assert summary["total_cost_usd"] == 0.01
    assert "by_scope" not in summary


def test_billing_summary_includes_translation_rag_sync_and_doctor_components() -> None:
    metrics = [
        _metric("pipeline.translate.llm_requests_total", 2),
        _metric("pipeline.translate.llm_input_tokens_total", 210),
        _metric("pipeline.translate.llm_output_tokens_total", 98),
        _metric("pipeline.translate.estimated_cost_usd", 0.0123, "usd"),
        _metric("pipeline.translate.context.embedding_calls_total", 1),
        _metric("pipeline.translate.context.embedding_prompt_tokens_total", 32),
        _metric(
            "pipeline.translate.context.embedding_estimated_cost_usd",
            0.0004,
            "usd",
        ),
        _metric("pipeline.rag.sync.embedding_calls_total", 4),
        _metric("pipeline.rag.sync.embedding_prompt_tokens_total", 400),
        _metric("pipeline.rag.sync.embedding_estimated_cost_usd", 0.0031, "usd"),
        _metric("pipeline.doctor.llm.requests_total", 1),
        _metric("pipeline.doctor.llm.input_tokens_total", 8),
        _metric("pipeline.doctor.llm.output_tokens_total", 1),
        _metric("pipeline.doctor.llm.estimated_cost_usd", 0.00012, "usd"),
    ]

    summary = summarize_billing_metrics(metrics)

    assert summary is not None
    assert summary["components"]["translation_llm"]["calls"] == 2
    assert summary["components"]["translation_context_embeddings"]["calls"] == 1
    assert summary["components"]["rag_sync_embeddings"]["calls"] == 4
    assert summary["components"]["doctor_llm"]["calls"] == 1
    assert summary["total_cost_usd"] == 0.01592
    assert "by_scope" not in summary
