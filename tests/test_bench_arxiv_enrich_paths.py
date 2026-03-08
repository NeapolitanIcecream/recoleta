from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

from scripts import bench_arxiv_enrich_paths as bench


def test_summarize_enrich_metrics_includes_pandoc_and_fallback_diagnostics() -> None:
    by_name = {
        "pipeline.enrich.duration_ms": 321.0,
        "pipeline.enrich.processed_total": 4.0,
        "pipeline.enrich.skipped_total": 1.0,
        "pipeline.enrich.failed_total": 0.0,
        "pipeline.enrich.item_duration_ms_total": 300.0,
        "pipeline.enrich.db.sql_queries_total": 25.0,
        "pipeline.enrich.db.sql_commits_total": 8.0,
        "pipeline.enrich.arxiv.html_document.items_total": 5.0,
        "pipeline.enrich.arxiv.html_document.fetch_ms_sum": 100.0,
        "pipeline.enrich.arxiv.html_document.cleanup_ms_sum": 20.0,
        "pipeline.enrich.arxiv.html_document.pandoc_ms_sum": 80.0,
        "pipeline.enrich.arxiv.html_document.pandoc_failed_total": 1.0,
        "pipeline.enrich.arxiv.html_document.pandoc_warning_items_total": 2.0,
        "pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum": 7.0,
        "pipeline.enrich.arxiv.html_document.pandoc_warning_tex_math_convert_failed_sum": 6.0,
        "pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum": 42.0,
        "pipeline.enrich.arxiv.html_document.fallback_to_pdf_total": 2.0,
        "pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.http_404_total": 2.0,
        "pipeline.enrich.arxiv.html_document.db_read_ms_sum": 12.0,
        "pipeline.enrich.arxiv.html_document.db_write_ms_sum": 9.0,
    }

    summary = bench._summarize_enrich_metrics(by_name)

    assert summary["enrich_ms"] == 321
    assert summary["html_document_items_total"] == 5
    assert summary["pandoc_failed_total"] == 1
    assert summary["pandoc_warning_items_total"] == 2
    assert summary["pandoc_warning_count_sum"] == 7
    assert summary["pandoc_warning_tex_math_convert_failed_sum"] == 6
    assert summary["pandoc_math_replaced_sum"] == 42
    assert summary["fallback_to_pdf_total"] == 2
    assert summary["fallback_to_pdf_by_reason"]["http_404"] == 2
    assert summary["fallback_to_pdf_by_reason"]["http_429"] == 0


def test_render_report_md_includes_diagnostics_section() -> None:
    results = {
        "config_path": "/tmp/recoleta.yaml",
        "selected_n": 3,
        "candidates_requested": 6,
        "pull_drafts_ms": 123,
        "repeat": 1,
        "warmup": 0,
        "concurrency": 1,
        "methods": {
            "html_document": {
                "durations": {
                    "ingest_ms_median": 10,
                    "ingest_ms_p95": 11,
                    "enrich_ms_median": 20,
                    "enrich_ms_p95": 21,
                    "triage_ms_median": 0,
                    "triage_ms_p95": 0,
                    "pipeline_ms_median": 30,
                    "pipeline_ms_p95": 31,
                },
                "enrich_result": {
                    "html_document_items_total": 3,
                    "pandoc_failed_total": 1,
                    "pandoc_warning_items_total": 2,
                    "pandoc_warning_count_sum": 7,
                    "pandoc_warning_tex_math_convert_failed_sum": 6,
                    "pandoc_math_replaced_sum": 42,
                    "fallback_to_pdf_total": 2,
                    "fallback_to_pdf_by_reason": {
                        "http_404": 2,
                        "http_429": 0,
                        "http_5xx": 0,
                        "http_other": 0,
                        "timeout": 0,
                        "request_error": 0,
                        "missing_url": 0,
                        "empty_document": 0,
                        "other": 0,
                    },
                },
                "tokens": {
                    "html_document": {
                        "full_tokens_sum": 100,
                        "full_tokens_median": 50,
                        "full_tokens_p95": 80,
                        "prompt_tokens_sum": 90,
                        "prompt_tokens_median": 45,
                        "prompt_tokens_p95": 70,
                        "token_counter_warnings": [],
                    },
                    "html_document_md": {
                        "full_tokens_sum": 80,
                        "full_tokens_median": 40,
                        "full_tokens_p95": 60,
                        "prompt_tokens_sum": 70,
                        "prompt_tokens_median": 35,
                        "prompt_tokens_p95": 55,
                        "token_counter_warnings": [],
                    },
                    "delta": {
                        "full_tokens_sum_delta": -20,
                        "prompt_tokens_sum_delta": -20,
                    },
                },
                "per_item": [],
            }
        },
    }

    report = bench._render_report_md(results=results)

    assert "### diagnostics" in report
    assert "- pandoc_warning_count_sum: 7" in report
    assert "- pandoc_math_replaced_sum: 42" in report
    assert "- fallback_to_pdf_total: 2" in report
    assert "- fallback_to_pdf_reason.http_404_total: 2" in report


def test_build_settings_for_method_handles_disabled_source_blocks(
    configured_env: Path,
) -> None:
    base = cast(
        Any,
        SimpleNamespace(
        model_dump=lambda mode="python": {
            "recoleta_db_path": str(configured_env / "base.db"),
            "triage_enabled": True,
            "sources": {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                },
                "hn": {
                    "enabled": False,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                },
                "rss": {
                    "enabled": False,
                    "feeds": [],
                },
            },
        },
        ),
    )

    updated = bench._build_settings_for_method(
        base=base,
        method="html_document",
        db_path=configured_env / "bench.db",
        html_document_max_concurrency=1,
    )

    assert updated.sources.arxiv.enrich_method == "html_document"
    assert updated.recoleta_db_path == configured_env / "bench.db"
