from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.site


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
    markdown_output_dir = Path("/tmp/recoleta-output")

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
        debug_pdf: bool = False,
    ):
        self.calls.append(
            {
                "run_id": run_id,
                "granularity": granularity,
                "anchor_date": anchor_date,
                "llm_model": llm_model,
                "backfill": bool(backfill),
                "backfill_mode": str(backfill_mode),
                "debug_pdf": bool(debug_pdf),
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


def test_trends_cli_forwards_debug_pdf_flag(
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
            "--debug-pdf",
        ],
    )

    assert result.exit_code == 0
    assert fake_service.calls
    assert fake_service.calls[0]["debug_pdf"] is True


def test_site_build_cli_uses_settings_default_directories(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    calls: dict[str, object] = {}

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "topics_total": 5}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        recoleta.site,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["site", "build"],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["output_dir"] == fake_settings.markdown_output_dir / "site"
    assert calls["limit"] is None
    assert "site build completed" in result.stdout


def test_site_stage_cli_uses_repo_local_default_output_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    calls: dict[str, object] = {}

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)
    monkeypatch.chdir(tmp_path)

    def _fake_stage_trend_site_source(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 4, "pdf_total": 2}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        recoleta.site,
        "stage_trend_site_source",
        _fake_stage_trend_site_source,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["site", "stage"],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["output_dir"] == tmp_path / "site-content" / "Trends"
    assert calls["limit"] is None
    assert "site stage completed" in result.stdout


def test_site_build_cli_with_explicit_paths_does_not_require_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "topics_total": 5}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(recoleta.cli, "_build_settings", _fail_build_settings)
    monkeypatch.setattr(
        recoleta.site,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir(parents=True, exist_ok=True)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "site",
            "build",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == input_dir.resolve()
    assert calls["output_dir"] == output_dir.resolve()
    assert calls["limit"] is None
    assert "site build completed" in result.stdout


def test_site_stage_cli_with_explicit_paths_does_not_require_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_stage_trend_site_source(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 4, "pdf_total": 2}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(recoleta.cli, "_build_settings", _fail_build_settings)
    monkeypatch.setattr(
        recoleta.site,
        "stage_trend_site_source",
        _fake_stage_trend_site_source,
    )

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir(parents=True, exist_ok=True)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "site",
            "stage",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == input_dir.resolve()
    assert calls["output_dir"] == output_dir.resolve()
    assert calls["limit"] is None
    assert "site stage completed" in result.stdout
