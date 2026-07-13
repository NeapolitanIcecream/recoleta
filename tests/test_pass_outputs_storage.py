from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from recoleta.pass_output_selection import (
    latest_canonical_pass_outputs_by_window,
    pass_output_window_key,
)
from recoleta.storage import Repository


def test_get_latest_pass_output_returns_latest_successful_target_match(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)
    for run_id in ("run-1", "run-2", "run-3", "run-4"):
        repository.create_run(config_fingerprint=f"fp-{run_id}", run_id=run_id)

    repository.create_pass_output(
        run_id="run-1",
        pass_kind="trend_synthesis",
        status="failed",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "failed"},
    )
    repository.create_pass_output(
        run_id="run-2",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "older-success"},
    )
    latest = repository.create_pass_output(
        run_id="run-3",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "latest-success"},
    )
    repository.create_pass_output(
        run_id="run-4",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_start + timedelta(days=1),
        payload={"title": "wrong-granularity"},
    )

    got = repository.get_latest_pass_output(
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
    )

    assert got is not None
    assert got.id == latest.id
    assert json.loads(got.payload_json)["title"] == "latest-success"


def test_mark_suppressed_pass_output_projection_complete_preserves_diagnostics(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    repository.create_run(config_fingerprint="fp-run", run_id="run-1")
    row = repository.create_pass_output(
        run_id="run-1",
        pass_kind="trend_synthesis",
        status="suppressed",
        diagnostics={
            "suppression_projection_complete": False,
            "trace": {"retained": True},
        },
    )
    assert row.id is not None

    completed = repository.mark_suppressed_pass_output_projection_complete(
        pass_output_id=row.id
    )

    assert json.loads(completed.diagnostics_json) == {
        "suppression_projection_complete": True,
        "trace": {"retained": True},
    }


def test_batch_canonical_selector_handles_mixed_null_granularity_windows(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)
    selected_rows = []
    for index, granularity in enumerate((None, "day"), start=1):
        run_id = f"run-{index}"
        repository.create_run(config_fingerprint=f"fp-{index}", run_id=run_id)
        selected_rows.append(
            repository.create_pass_output(
                run_id=run_id,
                pass_kind="trend_synthesis",
                status="succeeded",
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                payload={"index": index},
            )
        )

    selected = latest_canonical_pass_outputs_by_window(
        repository=repository,
        pass_kind="trend_synthesis",
        windows=(pass_output_window_key(row) for row in selected_rows),
    )

    assert {row.id for row in selected.values()} == {
        row.id for row in selected_rows
    }
