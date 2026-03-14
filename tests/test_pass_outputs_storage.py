from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

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
        scope="default",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "failed"},
    )
    repository.create_pass_output(
        run_id="run-2",
        pass_kind="trend_synthesis",
        status="succeeded",
        scope="default",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "older-success"},
    )
    latest = repository.create_pass_output(
        run_id="run-3",
        pass_kind="trend_synthesis",
        status="succeeded",
        scope="default",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload={"title": "latest-success"},
    )
    repository.create_pass_output(
        run_id="run-4",
        pass_kind="trend_synthesis",
        status="succeeded",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_start + timedelta(days=1),
        payload={"title": "wrong-granularity"},
    )

    got = repository.get_latest_pass_output(
        pass_kind="trend_synthesis",
        status="succeeded",
        scope="default",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
    )

    assert got is not None
    assert got.id == latest.id
    assert json.loads(got.payload_json)["title"] == "latest-success"
