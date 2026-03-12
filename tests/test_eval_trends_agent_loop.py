from __future__ import annotations

import json
from pathlib import Path

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

    assert [window.granularity for window in windows] == ["day", "week", "month"]
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
