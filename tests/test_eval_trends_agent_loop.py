from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from scripts import eval_trends_agent_loop as harness
from recoleta.storage import Repository


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
    assert all(window.stream == "software_intelligence" for window in windows)


def test_render_eval_manifest_md_includes_window_rows(tmp_path: Path) -> None:
    windows = [
        harness.EvalWindow(
            window_id="month-agents",
            granularity="month",
            anchor_date="2026-03-12",
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
    assert "uv run recoleta trends --granularity month --date 2026-03-12 --backfill" in report


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
            "raw_tool_trace": {
                "status": "captured",
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "search_hybrid",
                        "args": {"query": "agent memory loops"},
                    }
                ],
                "events_total": 1,
                "tool_calls_total": 1,
                "events_truncated": False,
            },
        },
        capture_metadata={"capture_mode": "pipeline"},
    )

    artifact_dir = Path(window_manifest["artifact_dir"])
    assert (artifact_dir / "report.md").read_text(encoding="utf-8").startswith("- grounded")
    assert json.loads((artifact_dir / "payload.json").read_text(encoding="utf-8"))["title"] == "Weekly Trend"
    tool_trace_payload = json.loads(
        (artifact_dir / "tool-trace.json").read_text(encoding="utf-8")
    )
    assert tool_trace_payload["run_id"] == "run-week-baseline"
    assert tool_trace_payload["raw_tool_trace"]["status"] == "captured"
    assert tool_trace_payload["raw_tool_trace"]["events"][0]["tool_name"] == "search_hybrid"
    assert json.loads((artifact_dir / "rubric.json").read_text(encoding="utf-8"))["status"] == "pending_manual_review"
    prompt_payload = json.loads((artifact_dir / "prompt.json").read_text(encoding="utf-8"))
    assert prompt_payload["status"] == "not_captured_yet"
    capture_summary = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert capture_summary["capture_mode"] == "pipeline"


def test_capture_existing_trends_baseline_reuses_existing_docs(
    monkeypatch,
    tmp_path: Path,
) -> None:
    import recoleta.cli as cli

    manifest = harness.build_eval_manifest(
        fixtures_path=tmp_path / "windows.json",
        out_dir=tmp_path / "bench-out",
        windows=[
            harness.EvalWindow(
                window_id="week-2026-w10-software-intelligence",
                granularity="week",
                anchor_date="2026-03-05",
                stream="software_intelligence",
                topics=["agents"],
                notes="weekly baseline",
            )
        ],
    )

    fake_document = SimpleNamespace(
        id=285,
        scope="software_intelligence",
        granularity="week",
        period_start=datetime(2026, 3, 2),
        period_end=datetime(2026, 3, 9),
        title="Weekly Trend",
    )
    fake_repository = SimpleNamespace(
        list_documents=lambda **kwargs: [fake_document],  # noqa: ARG005
    )

    monkeypatch.setattr(
        cli,
        "_build_settings",
        lambda: SimpleNamespace(
            recoleta_db_path=tmp_path / "source.db",
            rag_lancedb_dir=tmp_path / "source-lancedb",
            llm_output_language="Chinese (Simplified)",
        ),
    )
    monkeypatch.setattr(
        cli,
        "_build_repository_for_db_path",
        lambda *, db_path: fake_repository,  # noqa: ARG005
    )
    monkeypatch.setattr(
        harness,
        "_load_payload_json",
        lambda *, repository, doc_id: {"title": "Weekly Trend", "clusters": []},  # noqa: ARG005
    )
    monkeypatch.setattr(
        harness,
        "_render_report_markdown",
        lambda **kwargs: "# Weekly Trend\n\nExisting doc baseline.\n",
    )
    monkeypatch.setattr(
        cli,
        "_execute_stage",
        lambda **kwargs: (_ for _ in ()).throw(AssertionError("pipeline should not run")),
    )

    summary = harness.capture_eval_baseline(
        manifest=manifest,
        llm_model=None,
        isolate_runtime=True,
        capture_mode="existing-trends",
    )

    assert summary["capture_mode"] == "existing-trends"
    assert summary["runtime"]["mode"] == "existing_docs"
    artifact_dir = Path(manifest["windows"][0]["artifact_dir"])
    tool_trace = json.loads((artifact_dir / "tool-trace.json").read_text(encoding="utf-8"))
    assert tool_trace["trace_status"] == "unavailable_from_existing_doc"
    capture_summary = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert capture_summary["capture_mode"] == "existing-trends"
    assert capture_summary["source_document"]["doc_id"] == 285


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

    called: dict[str, Any] = {}
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
        lambda *, artifact_dir, run_id: {  # noqa: ARG005
            "debug": {
                "tool_calls_total": 2,
                "raw_tool_trace": {
                    "status": "captured",
                    "events": [
                        {
                            "kind": "tool-call",
                            "tool_name": "search_hybrid",
                            "args": {"query": "agent memory"},
                        }
                    ],
                    "events_total": 1,
                    "tool_calls_total": 1,
                    "events_truncated": False,
                },
            }
        },
    )
    monkeypatch.setattr(
        harness,
        "prepare_isolated_eval_runtime",
        lambda *, out_dir: {
            "mode": "isolated_copy",
            "source_db_path": str(tmp_path / "source.db"),
            "active_db_path": str(tmp_path / "isolated.db"),
            "source_lancedb_dir": str(tmp_path / "source-lancedb"),
            "active_lancedb_dir": str(tmp_path / "isolated-lancedb"),
            "backup_bundle_dir": str(tmp_path / "backup"),
        },
    )

    class _FakeService:
        _explicit_topic_streams = False

        def trends(self, **kwargs: Any) -> Any:
            called.update(kwargs)
            return fake_result

    def _assert_runtime_overrides(*, stage_name: str, stage_runner: Any) -> Any:  # noqa: ARG001
        assert str(harness.os.environ["RECOLETA_DB_PATH"]).endswith("isolated.db")
        assert str(harness.os.environ["RAG_LANCEDB_DIR"]).endswith("isolated-lancedb")
        assert harness.os.environ["TRENDS_OVERVIEW_PACK_MAX_CHARS"] == "6000"
        assert harness.os.environ["TRENDS_ITEM_OVERVIEW_TOP_K"] == "12"
        assert harness.os.environ["TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS"] == "320"
        return (
            fake_settings,
            fake_repository,
            "run-week-baseline",
            stage_runner(_FakeService(), "run-week-baseline"),
        )

    monkeypatch.setattr(cli, "_execute_stage", _assert_runtime_overrides)

    summary = harness.capture_eval_baseline(
        manifest=manifest,
        llm_model="test/fake-model",
        isolate_runtime=True,
        capture_mode="existing-corpus",
    )

    assert summary["captured_total"] == 1
    assert summary["failed_total"] == 0
    assert summary["runtime"]["mode"] == "isolated_copy"
    assert summary["capture_mode"] == "existing-corpus"
    assert summary["capture_budget"] == {
        "overview_pack_max_chars": 6000,
        "item_overview_top_k": 12,
        "item_overview_item_max_chars": 320,
    }
    assert called["reuse_existing_corpus"] is True
    assert called["backfill"] is False
    artifact_dir = Path(manifest["windows"][0]["artifact_dir"])
    capture_summary = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert capture_summary["status"] == "captured"
    assert capture_summary["capture_budget"] == {
        "overview_pack_max_chars": 6000,
        "item_overview_top_k": 12,
        "item_overview_item_max_chars": 320,
    }
    tool_trace_payload = json.loads(
        (artifact_dir / "tool-trace.json").read_text(encoding="utf-8")
    )
    assert tool_trace_payload["raw_tool_trace"]["status"] == "captured"
    assert tool_trace_payload["llm_debug"]["raw_tool_trace"]["events_total"] == 1
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

    monkeypatch.setattr(
        harness,
        "prepare_isolated_eval_runtime",
        lambda *, out_dir: {
            "mode": "isolated_copy",
            "source_db_path": str(tmp_path / "source.db"),
            "active_db_path": str(tmp_path / "isolated.db"),
            "source_lancedb_dir": str(tmp_path / "source-lancedb"),
            "active_lancedb_dir": str(tmp_path / "isolated-lancedb"),
            "backup_bundle_dir": str(tmp_path / "backup"),
        },
    )

    summary = harness.capture_eval_baseline(
        manifest=manifest,
        llm_model=None,
        isolate_runtime=True,
        capture_mode="existing-corpus",
    )

    assert summary["captured_total"] == 0
    assert summary["failed_total"] == 1
    artifact_dir = Path(manifest["windows"][0]["artifact_dir"])
    capture_summary = json.loads(
        (artifact_dir / "capture-summary.json").read_text(encoding="utf-8")
    )
    assert capture_summary["status"] == "failed"
    assert capture_summary["error"]["type"] == "RuntimeError"


def test_run_window_trends_capture_targets_requested_topic_stream(monkeypatch) -> None:
    from recoleta.pipeline import trends_stage as trends_stage_module

    called: dict[str, Any] = {}

    class _FakeService:
        def __init__(
            self,
            *,
            settings: Any | None = None,
            repository: Any | None = None,
            analyzer: Any | None = None,
            triage: Any | None = None,
            telegram_sender: Any | None = None,
        ) -> None:
            self.settings = settings
            self.repository = repository or object()
            self.analyzer = analyzer or object()
            self.semantic_triage = triage or object()
            self._topic_streams = [
                SimpleNamespace(name="embodied_ai", publish_targets=["markdown"]),
                SimpleNamespace(
                    name="software_intelligence", publish_targets=["markdown"]
                ),
            ]
            self._explicit_topic_streams = True
            self.telegram_sender = telegram_sender

        def _settings_for_topic_stream(self, stream: Any) -> Any:
            return SimpleNamespace(scope=stream.name)

        def _telegram_sender_for_stream(self, stream: Any) -> Any:  # noqa: ARG002
            return None

    def _fake_run_trends_stage(service: Any, **kwargs: Any) -> Any:
        called["service_scope"] = getattr(service.settings, "scope", None)
        called.update(kwargs)
        return SimpleNamespace(doc_id=99)

    monkeypatch.setattr(trends_stage_module, "run_trends_stage", _fake_run_trends_stage)

    result = harness._run_window_trends_capture(
        _FakeService(),
        stage_run_id="run-stream-window",
        window_manifest={
            "granularity": "week",
            "anchor_date": "2026-03-05",
            "stream": "software_intelligence",
        },
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
        backfill=False,
    )

    assert result.doc_id == 99
    assert called["service_scope"] == "software_intelligence"
    assert called["scope"] == "software_intelligence"
    assert called["reuse_existing_corpus"] is True
    assert called["backfill"] is False


def test_prepare_isolated_eval_runtime_clones_db_and_lancedb(
    monkeypatch,
    tmp_path: Path,
) -> None:
    import recoleta.cli as cli

    source_db_path = tmp_path / "source.db"
    source_repository = Repository(db_path=source_db_path)
    source_repository.init_schema()
    source_lancedb_dir = tmp_path / "source-lancedb"
    source_lancedb_dir.mkdir(parents=True)
    (source_lancedb_dir / "sentinel.txt").write_text("live", encoding="utf-8")

    monkeypatch.setattr(
        cli,
        "_build_settings",
        lambda: SimpleNamespace(
            recoleta_db_path=source_db_path,
            rag_lancedb_dir=source_lancedb_dir,
        ),
    )
    monkeypatch.setattr(
        cli,
        "_build_repository_for_db_path",
        lambda *, db_path: source_repository,  # noqa: ARG005
    )

    runtime = harness.prepare_isolated_eval_runtime(out_dir=tmp_path / "bench-out")

    isolated_db_path = Path(runtime["active_db_path"])
    isolated_lancedb_dir = Path(runtime["active_lancedb_dir"])
    assert runtime["mode"] == "isolated_copy"
    assert isolated_db_path.exists()
    assert isolated_db_path != source_db_path
    assert (isolated_lancedb_dir / "sentinel.txt").read_text(encoding="utf-8") == "live"
    (isolated_lancedb_dir / "sentinel.txt").write_text("isolated", encoding="utf-8")
    assert (source_lancedb_dir / "sentinel.txt").read_text(encoding="utf-8") == "live"


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
        isolate_runtime: bool,
        capture_mode: str,
    ) -> dict[str, Any]:
        called["manifest"] = manifest
        called["llm_model"] = llm_model
        called["isolate_runtime"] = isolate_runtime
        called["capture_mode"] = capture_mode
        summary = {
            "generated_at": "2026-03-12T00:00:00+00:00",
            "captured_total": 1,
            "failed_total": 0,
            "capture_mode": "existing-corpus",
            "runtime": {"mode": "isolated_copy"},
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
    assert called["isolate_runtime"] is True
    assert called["capture_mode"] == "existing-corpus"
    cli_output = json.loads(capsys.readouterr().out)
    assert cli_output["baseline_summary"] == str(
        (out_dir.expanduser().resolve() / "baseline-summary.json")
    )


def test_main_with_live_workspace_disables_runtime_isolation(
    monkeypatch,
    tmp_path: Path,
) -> None:
    fixture_path = tmp_path / "windows.json"
    fixture_path.write_text(
        json.dumps(
            {
                "windows": [
                    {
                        "id": "day-agents",
                        "granularity": "day",
                        "anchor_date": "2026-03-05",
                        "stream": "default",
                        "topics": ["agents"],
                        "notes": "daily baseline",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    called: dict[str, Any] = {}

    def _fake_capture_eval_baseline(
        *,
        manifest: dict[str, Any],
        llm_model: str | None,
        isolate_runtime: bool,
        capture_mode: str,
    ) -> dict[str, Any]:
        called["manifest"] = manifest
        called["llm_model"] = llm_model
        called["isolate_runtime"] = isolate_runtime
        called["capture_mode"] = capture_mode
        (Path(manifest["out_dir"]) / "baseline-summary.json").write_text(
            json.dumps(
                {
                    "generated_at": "2026-03-12T00:00:00+00:00",
                    "captured_total": 0,
                    "failed_total": 0,
                    "capture_mode": "pipeline",
                    "runtime": {"mode": "live_workspace"},
                    "windows": [],
                }
            ),
            encoding="utf-8",
        )
        return {}

    monkeypatch.setattr(harness, "capture_eval_baseline", _fake_capture_eval_baseline)

    exit_code = harness.main(
        [
            "--fixtures",
            str(fixture_path),
            "--out",
            str(tmp_path / "bench-out"),
            "--capture-baseline",
            "--capture-mode",
            "pipeline",
            "--live-workspace",
        ]
    )

    assert exit_code == 0
    assert called["llm_model"] is None
    assert called["isolate_runtime"] is False
    assert called["capture_mode"] == "pipeline"
