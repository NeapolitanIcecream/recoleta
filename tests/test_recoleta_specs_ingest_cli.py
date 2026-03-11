from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli


class _FakeRun:
    def __init__(self, run_id: str) -> None:
        self.id = run_id


class _FakeRepo:
    def __init__(self, *, metrics: list[SimpleNamespace]) -> None:
        self.metrics = metrics
        self.finished: list[tuple[str, bool]] = []

    def acquire_workspace_lease(self, **_: object) -> None:
        return None

    def mark_stale_runs_failed(self, **_: object) -> int:
        return 0

    def create_run(
        self, *, config_fingerprint: str, run_id: str | None = None
    ) -> _FakeRun:  # noqa: ARG002
        _ = run_id
        return _FakeRun("run-ingest")

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(self, **_: object) -> None:
        return None

    def release_workspace_lease(self, **_: object) -> bool:
        return True

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))

    def list_metrics(self, *, run_id: str) -> list[SimpleNamespace]:
        assert run_id == "run-ingest"
        return list(self.metrics)


class _FakeSettings:
    def __init__(self, *, tmp_path: Path) -> None:
        self.log_json = False
        self.publish_targets = []
        self.markdown_output_dir = tmp_path / "outputs"
        self.obsidian_vault_path = tmp_path / "vault"
        self.obsidian_base_folder = "Recoleta"

    def safe_fingerprint(self) -> str:
        return "fp-ingest"


class _FakeService:
    def prepare(self, *, run_id: str):  # type: ignore[no-untyped-def]
        assert run_id == "run-ingest"
        return type("IngestResult", (), {"inserted": 2, "updated": 0, "failed": 0})()


class _WindowedFakeService:
    def prepare(
        self,
        *,
        run_id: str,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ):  # type: ignore[no-untyped-def]
        assert run_id == "run-ingest"
        assert period_start == datetime(2026, 1, 2, tzinfo=UTC)
        assert period_end == datetime(2026, 1, 3, tzinfo=UTC)
        return type("IngestResult", (), {"inserted": 1, "updated": 0, "failed": 0})()


def test_ingest_cli_prints_arxiv_html_document_summary(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings(tmp_path=configured_env)
    fake_repo = _FakeRepo(
        metrics=[
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.items_total",
                value=5.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.pandoc_failed_total",
                value=1.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.pandoc_warning_items_total",
                value=2.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum",
                value=7.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum",
                value=42.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.fallback_to_pdf_total",
                value=2.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.http_404_total",
                value=2.0,
                unit="count",
            ),
        ]
    )
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(recoleta.cli.app, ["ingest"])

    assert result.exit_code == 0
    assert "ingest completed inserted=2 updated=0 failed=0" in result.stdout
    assert "arxiv html_document items=5 pandoc_failed=1" in result.stdout
    assert "pandoc_warning_items=2" in result.stdout
    assert "pandoc_warning_count=7" in result.stdout
    assert "pdf_fallbacks=2 math_replaced=42" in result.stdout
    assert "arxiv html_document fallback reasons http_404=2" in result.stdout
    assert fake_repo.finished == [("run-ingest", True)]


def test_ingest_cli_passes_target_day_window_to_prepare(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings(tmp_path=configured_env)
    fake_repo = _FakeRepo(metrics=[])
    fake_service = _WindowedFakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(recoleta.cli.app, ["ingest", "--date", "2026-01-02"])

    assert result.exit_code == 0
    assert "ingest completed inserted=1 updated=0 failed=0" in result.stdout
