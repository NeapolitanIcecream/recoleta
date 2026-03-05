from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli


@dataclass(slots=True)
class _FakeRun:
    id: str


class _FakeRepo:
    def __init__(self) -> None:
        self.finished: list[tuple[str, bool]] = []

    def create_run(self, *, config_fingerprint: str) -> _FakeRun:  # noqa: ARG002
        return _FakeRun(id="run-1")

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))

    def list_metrics(self, *, run_id: str):  # type: ignore[no-untyped-def]
        _ = run_id
        return [
            SimpleNamespace(
                name="pipeline.trends.llm_requests_total", value=1.0, unit="count"
            ),
            SimpleNamespace(
                name="pipeline.trends.llm_input_tokens_total", value=123.0, unit="count"
            ),
            SimpleNamespace(
                name="pipeline.trends.llm_output_tokens_total", value=45.0, unit="count"
            ),
            SimpleNamespace(
                name="pipeline.trends.estimated_cost_usd", value=0.0067, unit="usd"
            ),
        ]


class _FakeSettings:
    log_json = False

    def safe_fingerprint(self) -> str:
        return "fp-1"


class _FakeService:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def trends(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        granularity: str,
        anchor_date=None,
        llm_model=None,
        backfill: bool = False,
        backfill_mode: str = "missing",
    ):
        self.calls.append(
            {
                "run_id": run_id,
                "granularity": granularity,
                "anchor_date": anchor_date,
                "llm_model": llm_model,
                "backfill": bool(backfill),
                "backfill_mode": str(backfill_mode),
            }
        )
        return SimpleNamespace(
            doc_id=1,
            granularity=str(granularity),
            period_start=datetime(2026, 1, 1, tzinfo=UTC),
            period_end=datetime(2026, 1, 2, tzinfo=UTC),
            title="Daily Trend",
        )


def test_trends_cli_prints_billing_report_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "trends",
            "--granularity",
            "day",
            "--date",
            "2026-01-01",
            "--model",
            "openai/gpt-4o-mini",
        ],
    )
    assert result.exit_code == 0
    assert "trends completed" in result.stdout
    assert "Billing report" in result.stdout
    assert fake_repo.finished == [("run-1", True)]
    assert fake_service.calls and fake_service.calls[0]["run_id"] == "run-1"


def test_trends_cli_accepts_yyyymmdd_date(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "trends",
            "--granularity",
            "day",
            "--date",
            "20260101",
        ],
    )
    assert result.exit_code == 0
    assert fake_service.calls and fake_service.calls[0]["anchor_date"] == date(
        2026, 1, 1
    )


def test_trends_week_cli_accepts_yyyymmdd_date_and_enables_backfill(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "trends-week",
            "--date",
            "20260101",
        ],
    )
    assert result.exit_code == 0
    assert "Billing report" in result.stdout
    assert fake_service.calls
    call = fake_service.calls[0]
    assert call["granularity"] == "week"
    assert call["backfill"] is True
    assert call["backfill_mode"] == "missing"
    assert call["anchor_date"] == date(2026, 1, 1)
