from __future__ import annotations

import json
from pathlib import Path

from scripts import compare_shadow_day_runs as compare


def _write_shadow_fixture(
    root: Path,
    *,
    fleet_real_seconds: float,
    steps: list[tuple[str, int]],
    metrics: dict[str, float],
    billing_by_step: dict[str, dict[str, float] | None],
    terminal_state: str = "succeeded_clean",
) -> None:
    instance_root = root / "instances" / "embodied_ai"
    instance_root.mkdir(parents=True, exist_ok=True)
    summary = {
        "manifest_path": "/tmp/fleet.yaml",
        "date": "2026-04-13",
        "children": [
            {
                "instance": "embodied_ai",
                "time": {"real_seconds": fleet_real_seconds},
                "run_id": "run-1",
                "terminal_state": terminal_state,
                "steps": [
                    {
                        "step_id": step_id,
                        "status": "ok",
                        "duration_ms": duration_ms,
                    }
                    for step_id, duration_ms in steps
                ],
                "ranked_steps": [
                    {
                        "step_id": step_id,
                        "status": "ok",
                        "duration_ms": duration_ms,
                    }
                    for step_id, duration_ms in sorted(
                        steps, key=lambda item: (-item[1], item[0])
                    )
                ],
                "metrics": {
                    name: {"value": value, "unit": "count"}
                    for name, value in metrics.items()
                },
            }
        ],
        "aggregate": {
            "real_seconds_total": fleet_real_seconds,
            "step_totals": [
                {"step_id": step_id, "duration_ms": duration_ms}
                for step_id, duration_ms in steps
            ],
        },
    }
    inspect_payload = {
        "run": {
            "id": "run-1",
            "billing_by_step": {
                step_id: (
                    {
                        "total_cost_usd": payload["total_cost_usd"],
                    }
                    if payload is not None
                    else None
                )
                for step_id, payload in billing_by_step.items()
            },
            "started_at": "2026-04-22T00:00:00+00:00",
            "finished_at": "2026-04-22T00:01:00+00:00",
        }
    }
    (root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (instance_root / "inspect.json").write_text(
        json.dumps(inspect_payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def test_build_comparison_reports_step_metric_and_billing_deltas(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "baseline"
    candidate_dir = tmp_path / "candidate"
    _write_shadow_fixture(
        baseline_dir,
        fleet_real_seconds=100.0,
        steps=[
            ("ingest", 60_000),
            ("translate", 30_000),
            ("site-build", 10_000),
        ],
        metrics={
            "pipeline.enrich.source.hn.fetch_ms_sum": 50_000.0,
            "pipeline.translate.translated_total": 20.0,
            "pipeline.translate.materialize_localized.duration_ms": 8_000.0,
        },
        billing_by_step={
            "translate": {"total_cost_usd": 1.4},
            "analyze": {"total_cost_usd": 0.9},
        },
    )
    _write_shadow_fixture(
        candidate_dir,
        fleet_real_seconds=82.0,
        steps=[
            ("ingest", 44_000),
            ("translate", 28_000),
            ("site-build", 10_000),
        ],
        metrics={
            "pipeline.enrich.source.hn.fetch_ms_sum": 34_000.0,
            "pipeline.translate.translated_total": 20.0,
            "pipeline.translate.materialize_localized.duration_ms": 5_000.0,
        },
        billing_by_step={
            "translate": {"total_cost_usd": 1.1},
            "analyze": {"total_cost_usd": 0.9},
        },
    )

    comparison = compare._build_comparison(
        baseline_dir=baseline_dir,
        candidate_dir=candidate_dir,
    )

    assert comparison["fleet"]["real_seconds_total"]["delta"] == -18.0
    assert comparison["fleet"]["real_seconds_total"]["improvement_pct"] == 18.0
    assert comparison["aggregate_steps"]["ingest"]["delta_ms"] == -16_000
    assert comparison["aggregate_steps"]["ingest"]["improvement_pct"] == 26.67
    child = comparison["children"]["embodied_ai"]
    assert child["metrics"]["pipeline.enrich.source.hn.fetch_ms_sum"]["delta"] == -16000.0
    assert child["metrics"]["pipeline.translate.materialize_localized.duration_ms"]["delta"] == -3000.0
    assert child["billing_by_step"]["translate"]["delta_usd"] == -0.3


def test_build_comparison_treats_missing_metrics_and_billing_as_zero(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "baseline"
    candidate_dir = tmp_path / "candidate"
    _write_shadow_fixture(
        baseline_dir,
        fleet_real_seconds=40.0,
        steps=[("translate", 20_000)],
        metrics={
            "pipeline.translate.scanned_total": 10.0,
        },
        billing_by_step={"translate": None},
    )
    _write_shadow_fixture(
        candidate_dir,
        fleet_real_seconds=44.0,
        steps=[("translate", 24_000)],
        metrics={
            "pipeline.translate.scanned_total": 12.0,
            "pipeline.translate.skipped_total.up_to_date_source_hash": 7.0,
        },
        billing_by_step={"translate": {"total_cost_usd": 0.5}},
        terminal_state="succeeded_partial",
    )

    comparison = compare._build_comparison(
        baseline_dir=baseline_dir,
        candidate_dir=candidate_dir,
    )

    child = comparison["children"]["embodied_ai"]
    assert child["metrics"]["pipeline.translate.skipped_total.up_to_date_source_hash"]["baseline"] == 0.0
    assert child["metrics"]["pipeline.translate.skipped_total.up_to_date_source_hash"]["delta"] == 7.0
    assert child["billing_by_step"]["translate"]["baseline_usd"] == 0.0
    assert child["billing_by_step"]["translate"]["candidate_usd"] == 0.5
    assert child["terminal_state"]["baseline"] == "succeeded_clean"
    assert child["terminal_state"]["candidate"] == "succeeded_partial"


def test_build_comparison_flags_workload_metric_mismatches(tmp_path: Path) -> None:
    baseline_dir = tmp_path / "baseline"
    candidate_dir = tmp_path / "candidate"
    _write_shadow_fixture(
        baseline_dir,
        fleet_real_seconds=100.0,
        steps=[("ingest", 60_000), ("translate", 40_000)],
        metrics={
            "pipeline.ingest.source.arxiv.in_window_total": 14.0,
            "pipeline.enrich.source.arxiv.content_chars_sum": 1_000_000.0,
            "pipeline.translate.translated_total": 25.0,
        },
        billing_by_step={},
    )
    _write_shadow_fixture(
        candidate_dir,
        fleet_real_seconds=70.0,
        steps=[("ingest", 30_000), ("translate", 40_000)],
        metrics={
            "pipeline.ingest.source.arxiv.in_window_total": 0.0,
            "pipeline.enrich.source.arxiv.content_chars_sum": 0.0,
            "pipeline.translate.translated_total": 24.0,
        },
        billing_by_step={},
    )

    comparison = compare._build_comparison(
        baseline_dir=baseline_dir,
        candidate_dir=candidate_dir,
    )

    warnings = comparison["workload_comparability_warnings"]
    warning_keys = {(entry["instance"], entry["metric"]) for entry in warnings}
    assert ("embodied_ai", "pipeline.ingest.source.arxiv.in_window_total") in warning_keys
    assert ("embodied_ai", "pipeline.enrich.source.arxiv.content_chars_sum") in warning_keys
    assert ("embodied_ai", "pipeline.translate.translated_total") in warning_keys

    report = compare._render_report(comparison)
    assert "## Workload Comparability Warnings" in report
    assert "Treat wall-time deltas as non-comparable" in report
