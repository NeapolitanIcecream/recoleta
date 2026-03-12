from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from scripts import eval_trends_agent_loop as harness


def test_load_eval_windows_normalizes_topics(tmp_path: Path) -> None:
    fixture_path = tmp_path / "windows.json"
    fixture_path.write_text(
        json.dumps(
            {
                "windows": [
                    {
                        "id": "week-agents",
                        "granularity": "week",
                        "anchor_date": "2026-03-05",
                        "stream": " default ",
                        "topics": [" Agents ", "evaluation", ""],
                        "notes": "  weekly baseline  ",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    windows = harness.load_eval_windows(fixture_path)

    assert len(windows) == 1
    assert windows[0].window_id == "week-agents"
    assert windows[0].stream == "default"
    assert windows[0].topics == ["agents", "evaluation"]
    assert windows[0].notes == "weekly baseline"


def test_build_eval_manifest_includes_trends_commands_and_artifacts(tmp_path: Path) -> None:
    windows = [
        harness.EvalWindow(
            window_id="day-agents",
            granularity="day",
            anchor_date="2026-03-05",
            stream="default",
            topics=["agents"],
            notes="daily baseline",
        ),
        harness.EvalWindow(
            window_id="week-agents",
            granularity="week",
            anchor_date="2026-03-05",
            stream="default",
            topics=["agents"],
            notes="weekly baseline",
        ),
    ]

    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=windows,
    )

    assert manifest["window_count"] == 2
    assert manifest["windows"][0]["artifact_dir"].endswith("day-agents")
    assert (
        manifest["windows"][0]["commands"]["trends"]
        == "uv run recoleta trends --granularity day --date 2026-03-05"
    )
    assert (
        manifest["windows"][1]["commands"]["trends"]
        == "uv run recoleta trends --granularity week --date 2026-03-05 --backfill"
    )


def test_default_eval_fixture_is_valid() -> None:
    fixture_path = Path("benchmarks/trends_agent_eval_windows.json")

    windows = harness.load_eval_windows(fixture_path)

    assert [window.granularity for window in windows] == ["day", "week"]
    assert all(window.stream == "default" for window in windows)


def test_render_eval_manifest_md_includes_window_rows(tmp_path: Path) -> None:
    windows = [
        harness.EvalWindow(
            window_id="month-agents",
            granularity="month",
            anchor_date="2026-03-15",
            stream="default",
            topics=["agents", "evaluation"],
            notes="monthly baseline",
        )
    ]
    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=windows,
    )

    report = harness.render_eval_manifest_md(manifest=manifest)

    assert "# trends agent eval manifest" in report
    assert "month-agents" in report
    assert "uv run recoleta trends --granularity month --date 2026-03-15 --backfill" in report


def test_render_eval_runbook_sh_includes_window_commands(tmp_path: Path) -> None:
    windows = [
        harness.EvalWindow(
            window_id="week-agents",
            granularity="week",
            anchor_date="2026-03-05",
            stream="default",
            topics=["agents"],
            notes="weekly baseline",
        )
    ]
    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=windows,
    )

    runbook = harness.render_eval_runbook_sh(manifest=manifest)

    assert "#!/usr/bin/env bash" in runbook
    assert 'mkdir -p "' in runbook
    assert 'uv run recoleta trends --granularity week --date 2026-03-05 --backfill' in runbook
    assert 'tee "' in runbook


def test_summarize_run_metrics_extracts_tool_breakdown() -> None:
    metrics = [
        SimpleNamespace(name="pipeline.trends.tool_calls_total", value=5.0, unit="count"),
        SimpleNamespace(
            name="pipeline.trends.tool.search_hybrid.calls_total",
            value=2.0,
            unit="count",
        ),
        SimpleNamespace(
            name="pipeline.trends.tool.get_doc_bundle.calls_total",
            value=3.0,
            unit="count",
        ),
        SimpleNamespace(name="pipeline.trends.prompt_chars", value=1024.0, unit="chars"),
        SimpleNamespace(name="pipeline.trends.duration_ms", value=321.0, unit="ms"),
    ]

    summary = harness.summarize_run_metrics(metrics)

    assert summary["tool_calls_total"] == 5
    assert summary["tool_call_breakdown"] == {
        "get_doc_bundle": 3,
        "search_hybrid": 2,
    }
    assert summary["prompt_chars"] == 1024
    assert summary["duration_ms"] == 321


def test_write_window_capture_artifacts_materializes_expected_files(tmp_path: Path) -> None:
    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=[
            harness.EvalWindow(
                window_id="week-agents",
                granularity="week",
                anchor_date="2026-03-05",
                stream="default",
                topics=["agents"],
                notes="weekly baseline",
            )
        ],
    )
    window_manifest = manifest["windows"][0]

    harness.write_window_capture_artifacts(
        window_manifest=window_manifest,
        run_id="run-week-baseline",
        doc_id=42,
        report_markdown="- grounded weekly trend\n",
        payload_json={"title": "Weekly Trend", "clusters": []},
        tool_trace={
            "tool_calls_total": 3,
            "tool_call_breakdown": {"search_hybrid": 1, "get_doc_bundle": 2},
        },
    )

    artifact_dir = Path(window_manifest["artifact_dir"])
    assert (artifact_dir / "report.md").read_text(encoding="utf-8").startswith("- grounded")
    assert json.loads((artifact_dir / "payload.json").read_text(encoding="utf-8"))["title"] == "Weekly Trend"
    assert json.loads((artifact_dir / "tool-trace.json").read_text(encoding="utf-8"))["run_id"] == "run-week-baseline"
    assert json.loads((artifact_dir / "rubric.json").read_text(encoding="utf-8"))["status"] == "pending_manual_review"
    prompt_payload = json.loads((artifact_dir / "prompt.json").read_text(encoding="utf-8"))
    assert prompt_payload["status"] == "not_captured_yet"


def test_write_window_capture_failure_artifacts_records_error_context(tmp_path: Path) -> None:
    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=[
            harness.EvalWindow(
                window_id="day-agents",
                granularity="day",
                anchor_date="2026-03-05",
                stream="default",
                topics=["agents"],
                notes="daily baseline",
            )
        ],
    )
    window_manifest = manifest["windows"][0]

    harness.write_window_capture_failure_artifacts(
        window_manifest=window_manifest,
        error_type="RuntimeError",
        error_message="capture failed",
    )

    artifact_dir = Path(window_manifest["artifact_dir"])
    summary_payload = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert summary_payload["status"] == "failed"
    assert summary_payload["error"]["type"] == "RuntimeError"
    tool_trace_payload = json.loads(
        (artifact_dir / "tool-trace.json").read_text(encoding="utf-8")
    )
    assert tool_trace_payload["status"] == "failed"
    assert json.loads((artifact_dir / "payload.json").read_text(encoding="utf-8"))["status"] == "failed"


def test_capture_eval_baseline_writes_window_and_aggregate_artifacts(
    monkeypatch,
    tmp_path: Path,
) -> None:
    import recoleta.cli as cli

    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=[
            harness.EvalWindow(
                window_id="week-agents",
                granularity="week",
                anchor_date="2026-03-05",
                stream="default",
                topics=["agents"],
                notes="weekly baseline",
            )
        ],
    )

    fake_repository = SimpleNamespace(
        list_metrics=lambda *, run_id: [
            SimpleNamespace(
                name="pipeline.trends.tool.search_hybrid.calls_total",
                value=2.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.trends.tool_calls_total",
                value=2.0,
                unit="count",
            ),
        ]
    )
    fake_settings = SimpleNamespace(llm_output_language="Chinese (Simplified)")
    fake_result = SimpleNamespace(doc_id=42)

    monkeypatch.setattr(
        cli,
        "_execute_stage",
        lambda *, stage_name, stage_runner: (  # noqa: ARG005
            fake_settings,
            fake_repository,
            "run-week-baseline",
            fake_result,
        ),
    )
    monkeypatch.setattr(
        harness,
        "_load_payload_json",
        lambda *, repository, doc_id: {"title": "Weekly Trend", "clusters": []},  # noqa: ARG005
    )
    monkeypatch.setattr(
        harness,
        "_render_report_markdown",
        lambda **kwargs: "# Weekly Trend\n\nCaptured baseline.\n",
    )
    monkeypatch.setattr(
        harness,
        "_load_debug_payload",
        lambda *, artifact_dir, run_id: {"debug": {"tool_calls_total": 2}},  # noqa: ARG005
    )

    summary = harness.capture_eval_baseline(manifest=manifest, llm_model="test/fake-model")

    assert summary["captured_total"] == 1
    assert summary["failed_total"] == 0
    artifact_dir = Path(manifest["windows"][0]["artifact_dir"])
    assert json.loads((artifact_dir / "capture-summary.json").read_text(encoding="utf-8"))["status"] == "captured"
    baseline_summary = json.loads(
        (Path(manifest["out_dir"]) / "baseline-summary.json").read_text(encoding="utf-8")
    )
    assert baseline_summary["windows"][0]["run_id"] == "run-week-baseline"


def test_capture_eval_baseline_records_failed_window_when_stage_raises(
    monkeypatch,
    tmp_path: Path,
) -> None:
    import recoleta.cli as cli

    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=[
            harness.EvalWindow(
                window_id="day-agents",
                granularity="day",
                anchor_date="2026-03-05",
                stream="default",
                topics=["agents"],
                notes="daily baseline",
            )
        ],
    )

    def _raise_execute_stage(*, stage_name: str, stage_runner: Any) -> Any:  # noqa: ARG001
        raise RuntimeError("stage boom")

    monkeypatch.setattr(cli, "_execute_stage", _raise_execute_stage)

    summary = harness.capture_eval_baseline(manifest=manifest, llm_model=None)

    assert summary["captured_total"] == 0
    assert summary["failed_total"] == 1
    artifact_dir = Path(manifest["windows"][0]["artifact_dir"])
    capture_summary = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert capture_summary["status"] == "failed"
    assert capture_summary["error"]["type"] == "RuntimeError"


def test_main_with_capture_baseline_emits_summary_path(
    monkeypatch,
    tmp_path: Path,
    capsys,
) -> None:
    fixture_path = tmp_path / "windows.json"
    fixture_path.write_text(
        json.dumps(
            {
                "windows": [
                    {
                        "id": "week-agents",
                        "granularity": "week",
                        "anchor_date": "2026-03-05",
                        "stream": "default",
                        "topics": ["agents"],
                        "notes": "weekly baseline",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    out_dir = tmp_path / "bench-out"
    called: dict[str, Any] = {}

    def _fake_capture_eval_baseline(
        *,
        manifest: dict[str, Any],
        llm_model: str | None,
    ) -> dict[str, Any]:
        called["manifest"] = manifest
        called["llm_model"] = llm_model
        summary = {
            "generated_at": "2026-03-12T00:00:00+00:00",
            "captured_total": 1,
            "failed_total": 0,
            "windows": [],
        }
        (Path(manifest["out_dir"]) / "baseline-summary.json").write_text(
            json.dumps(summary),
            encoding="utf-8",
        )
        return summary

    monkeypatch.setattr(harness, "capture_eval_baseline", _fake_capture_eval_baseline)

    exit_code = harness.main(
        [
            "--fixtures",
            str(fixture_path),
            "--out",
            str(out_dir),
            "--capture-baseline",
            "--model",
            "test/fake-model",
        ]
    )

    assert exit_code == 0
    assert called["llm_model"] == "test/fake-model"
    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["baseline_summary"] == str(
        (out_dir.expanduser().resolve() / "baseline-summary.json")
    )
