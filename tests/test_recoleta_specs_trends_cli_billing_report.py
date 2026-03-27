from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.cli.site
import recoleta.site


@dataclass(slots=True)
class _FakeRun:
    id: str


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
        return _FakeRun(id="run-1")

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(self, **_: object) -> None:
        return None

    def release_workspace_lease(self, **_: object) -> bool:
        return True

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
    localization: object | None = None

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


class _FakeSiteServer:
    def __init__(self, *, host: str, port: int) -> None:
        self.server_address = (host, port)
        self.served = False

    def __enter__(self) -> _FakeSiteServer:
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:  # type: ignore[no-untyped-def]
        return False

    def serve_forever(self) -> None:
        self.served = True
        raise KeyboardInterrupt


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


def test_trends_cli_emits_json_output_with_billing_summary(
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
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "trends"
    assert payload["run_id"] == "run-1"
    assert payload["doc_id"] == 1
    assert payload["granularity"] == "day"
    assert payload["period_start"] == "2026-01-01T00:00:00+00:00"
    assert payload["period_end"] == "2026-01-02T00:00:00+00:00"
    assert payload["billing"]["components"]["trends_llm"]["calls"] == 1
    assert payload["billing"]["components"]["trends_llm"]["input_tokens"] == 123
    assert payload["billing"]["components"]["trends_llm"]["output_tokens"] == 45
    assert payload["billing"]["total_cost_usd"] == 0.0067


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


def test_trends_week_cli_surfaces_v2_migration_guidance() -> None:
    runner = CliRunner()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "trends-week",
            "--date",
            "20260101",
        ],
    )
    assert result.exit_code == 2
    assert "run week" in result.stdout


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


def test_site_build_cli_emits_json_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        _ = (input_dir, limit)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "ideas_total": 2, "topics_total": 5, "streams_total": 2}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        recoleta.site,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    result = runner.invoke(recoleta.cli.app, ["site", "build", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "site build"
    assert payload["manifest"]["trends_total"] == 3
    assert payload["manifest"]["ideas_total"] == 2
    assert payload["output_dir"] == str(fake_settings.markdown_output_dir / "site")


def test_site_build_cli_passes_default_language_from_settings_localization(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    fake_settings.localization = SimpleNamespace(site_default_language_code="en")
    calls: dict[str, object] = {}

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        output_dir,
        limit=None,
        default_language_code=None,
    ):
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["default_language_code"] = default_language_code
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text('{"trends_total": 1, "topics_total": 2}\n', encoding="utf-8")
        return manifest_path

    monkeypatch.setattr(
        recoleta.site,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    result = runner.invoke(recoleta.cli.app, ["site", "build"])

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["default_language_code"] == "en"


def test_site_build_cli_accepts_explicit_default_language_code_without_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_export_trend_static_site(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        output_dir,
        limit=None,
        default_language_code=None,
    ):
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        calls["default_language_code"] = default_language_code
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text('{"trends_total": 3, "topics_total": 5}\n', encoding="utf-8")
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
            "--default-language-code",
            "zh-CN",
        ],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == input_dir.resolve()
    assert calls["output_dir"] == output_dir.resolve()
    assert calls["default_language_code"] == "zh-CN"


def test_site_build_cli_formats_ideas_and_stream_counts_cleanly(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        _ = (input_dir, limit)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "ideas_total": 2, "topics_total": 5, "streams_total": 2}\n',
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
    assert "trends=3 ideas=2 topics=5 streams=2" in result.stdout


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


def test_site_stage_cli_emits_json_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)
    monkeypatch.chdir(tmp_path)

    def _fake_stage_trend_site_source(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        _ = (input_dir, limit)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 4, "ideas_total": 2, "pdf_total": 2, "streams_total": 2}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        recoleta.site,
        "stage_trend_site_source",
        _fake_stage_trend_site_source,
    )

    result = runner.invoke(recoleta.cli.app, ["site", "stage", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "site stage"
    assert payload["manifest"]["trends_total"] == 4
    assert payload["manifest"]["pdf_total"] == 2
    assert payload["output_dir"] == str(tmp_path / "site-content" / "Trends")


def test_site_stage_cli_formats_ideas_and_stream_counts_cleanly(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)
    monkeypatch.chdir(tmp_path)

    def _fake_stage_trend_site_source(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        _ = (input_dir, limit)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 4, "ideas_total": 2, "pdf_total": 2, "streams_total": 2}\n',
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
    assert "trends=4 ideas=2 pdfs=2 streams=2" in result.stdout


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


def test_site_build_cli_uses_trends_subdirectory_even_when_legacy_topic_streams_are_present(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    fake_settings.topic_stream_runtimes = lambda: [  # type: ignore[attr-defined]
        SimpleNamespace(
            name="agents_lab",
            explicit=True,
            markdown_output_dir=fake_settings.markdown_output_dir / "Streams" / "agents_lab",
        ),
        SimpleNamespace(
            name="bio_watch",
            explicit=True,
            markdown_output_dir=fake_settings.markdown_output_dir / "Streams" / "bio_watch",
        ),
    ]
    calls: dict[str, object] = {}

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "topics_total": 5, "streams_total": 2}\n',
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


def test_site_stage_cli_uses_trends_subdirectory_even_when_legacy_topic_streams_are_present(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    fake_settings.topic_stream_runtimes = lambda: [  # type: ignore[attr-defined]
        SimpleNamespace(
            name="agents_lab",
            explicit=True,
            markdown_output_dir=fake_settings.markdown_output_dir / "Streams" / "agents_lab",
        ),
        SimpleNamespace(
            name="bio_watch",
            explicit=True,
            markdown_output_dir=fake_settings.markdown_output_dir / "Streams" / "bio_watch",
        ),
    ]
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
            '{"trends_total": 4, "pdf_total": 2, "streams_total": 2}\n',
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


def test_site_serve_cli_builds_then_serves_with_defaults(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.markdown_output_dir = tmp_path / "output"
    calls: dict[str, object] = {}
    fake_server = _FakeSiteServer(host="127.0.0.1", port=8000)

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)

    def _fake_export_trend_static_site(*, input_dir, output_dir, limit=None):  # type: ignore[no-untyped-def]
        calls["input_dir"] = input_dir
        calls["output_dir"] = output_dir
        calls["limit"] = limit
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "index.html").write_text("site\n", encoding="utf-8")
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 3, "topics_total": 5}\n',
            encoding="utf-8",
        )
        return manifest_path

    def _fake_create_site_server(*, directory, host, port):  # type: ignore[no-untyped-def]
        calls["serve_directory"] = directory
        calls["serve_host"] = host
        calls["serve_port"] = port
        return fake_server

    monkeypatch.setattr(
        recoleta.site,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )
    monkeypatch.setattr(
        recoleta.cli.site,
        "_create_site_server",
        _fake_create_site_server,
    )

    result = runner.invoke(recoleta.cli.app, ["site", "serve"])

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["output_dir"] == fake_settings.markdown_output_dir / "site"
    assert calls["serve_directory"] == fake_settings.markdown_output_dir / "site"
    assert calls["serve_host"] == "127.0.0.1"
    assert calls["serve_port"] == 8000
    assert fake_server.served is True
    assert "site build completed" in result.stdout
    assert "site serve ready" in result.stdout


def test_site_serve_cli_forwards_default_language_code_to_build(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}
    fake_server = _FakeSiteServer(host="127.0.0.1", port=8100)
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "site"
    input_dir.mkdir(parents=True, exist_ok=True)

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_run_site_build_command(**kwargs):  # type: ignore[no-untyped-def]
        calls["build_kwargs"] = dict(kwargs)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "index.html").write_text("site\n", encoding="utf-8")
        (output_dir / "manifest.json").write_text(
            '{"trends_total": 1, "topics_total": 2}\n',
            encoding="utf-8",
        )

    def _fake_create_site_server(*, directory, host, port):  # type: ignore[no-untyped-def]
        calls["serve_directory"] = directory
        calls["serve_host"] = host
        calls["serve_port"] = port
        return fake_server

    monkeypatch.setattr(recoleta.cli, "_build_settings", _fail_build_settings)
    monkeypatch.setattr(
        recoleta.cli.site,
        "run_site_build_command",
        _fake_run_site_build_command,
    )
    monkeypatch.setattr(
        recoleta.cli.site,
        "_create_site_server",
        _fake_create_site_server,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "site",
            "serve",
            "--input-dir",
            str(input_dir),
            "--output-dir",
            str(output_dir),
            "--default-language-code",
            "zh-CN",
        ],
    )

    assert result.exit_code == 0
    build_kwargs = calls["build_kwargs"]
    assert isinstance(build_kwargs, dict)
    assert build_kwargs["default_language_code"] == "zh-CN"
    assert calls["serve_directory"] == output_dir.resolve()
    assert fake_server.served is True


def test_site_serve_cli_with_explicit_output_and_no_build_does_not_require_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}
    fake_server = _FakeSiteServer(host="127.0.0.1", port=9000)

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_create_site_server(*, directory, host, port):  # type: ignore[no-untyped-def]
        calls["serve_directory"] = directory
        calls["serve_host"] = host
        calls["serve_port"] = port
        return fake_server

    monkeypatch.setattr(recoleta.cli, "_build_settings", _fail_build_settings)
    monkeypatch.setattr(
        recoleta.cli.site,
        "_create_site_server",
        _fake_create_site_server,
    )

    output_dir = tmp_path / "site"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text("site\n", encoding="utf-8")

    result = runner.invoke(
        recoleta.cli.app,
        [
            "site",
            "serve",
            "--output-dir",
            str(output_dir),
            "--no-build",
            "--port",
            "9000",
        ],
    )

    assert result.exit_code == 0
    assert calls["serve_directory"] == output_dir.resolve()
    assert calls["serve_host"] == "127.0.0.1"
    assert calls["serve_port"] == 9000
    assert fake_server.served is True
    assert "site build completed" not in result.stdout
    assert "site serve ready" in result.stdout


def test_site_serve_logs_warning_when_server_start_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from loguru import logger as loguru_logger

    output_dir = tmp_path / "site"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text("site\n", encoding="utf-8")

    def _raise_server_error(**_: object):  # type: ignore[no-untyped-def]
        raise OSError("address already in use")

    monkeypatch.setattr(
        recoleta.cli.site,
        "_create_site_server",
        _raise_server_error,
    )

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="WARNING", serialize=True)
    try:
        with pytest.raises(OSError, match="address already in use"):
            recoleta.cli.site.run_site_serve_command(
                input_dir=None,
                output_dir=output_dir,
                limit=None,
                host="127.0.0.1",
                port=8000,
                build=False,
            )
    finally:
        loguru_logger.remove(sink_id)

    payload = stream.getvalue()
    assert "cli.site.serve" in payload
    assert "site preview server failed" in payload
