from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

import recoleta.cli


class _FakeRun:
    def __init__(self, run_id: str) -> None:
        self.id = run_id


class _FakeRepo:
    def __init__(self) -> None:
        self.finished: list[tuple[str, bool]] = []

    def acquire_workspace_lease(self, **_: object) -> None:
        return None

    def mark_stale_runs_failed(self, **_: object) -> int:
        return 0

    def create_run(
        self, *, config_fingerprint: str, run_id: str | None = None
    ) -> _FakeRun:  # noqa: ARG002
        _ = run_id
        return _FakeRun("run-analyze")

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(self, **_: object) -> None:
        return None

    def release_workspace_lease(self, **_: object) -> bool:
        return True

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))


class _FakeSettings:
    def __init__(self) -> None:
        self.log_json = False

    def safe_fingerprint(self) -> str:
        return "fp-analyze"


class _FakeService:
    def analyze(
        self,
        *,
        run_id: str,
        limit: int | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ):  # type: ignore[no-untyped-def]
        assert run_id == "run-analyze"
        assert limit == 3
        assert period_start == datetime(2026, 1, 2, tzinfo=UTC)
        assert period_end == datetime(2026, 1, 3, tzinfo=UTC)
        return type("AnalyzeResult", (), {"processed": 4, "failed": 1})()


def test_analyze_cli_passes_target_day_window_to_analyze(
    configured_env: Path,  # noqa: ARG001
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
        ["analyze", "--limit", "3", "--date", "2026-01-02"],
    )

    assert result.exit_code == 0
    assert "analyze completed processed=4 failed=1" in result.stdout
    assert fake_repo.finished == [("run-analyze", True)]


def test_analyze_cli_emits_json_output(
    configured_env: Path,  # noqa: ARG001
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
        ["analyze", "--limit", "3", "--date", "2026-01-02", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "analyze"
    assert payload["run_id"] == "run-analyze"
    assert payload["processed"] == 4
    assert payload["failed"] == 1
    assert payload["limit"] == 3
    assert payload["period_start"] == "2026-01-02T00:00:00+00:00"
    assert payload["period_end"] == "2026-01-03T00:00:00+00:00"
    assert fake_repo.finished == [("run-analyze", True)]
