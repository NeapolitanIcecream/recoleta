from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest
from typer.testing import CliRunner

import recoleta.cli


@dataclass(slots=True)
class _FakeRun:
    id: str


class _FakeRepo:
    def __init__(self) -> None:
        self.created: list[str] = []
        self.finished: list[tuple[str, bool]] = []

    def create_run(self, *, config_fingerprint: str) -> _FakeRun:  # noqa: ARG002
        self.created.append(config_fingerprint)
        return _FakeRun(id="run-1")

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))


class _FakeSettings:
    def __init__(self, *, tmp_path: Path) -> None:
        self.log_json = False
        self.publish_targets = ["markdown", "obsidian"]
        self.markdown_output_dir = tmp_path / "outputs"
        self.obsidian_vault_path = tmp_path / "vault"
        self.obsidian_base_folder = "Recoleta"

    def safe_fingerprint(self) -> str:
        return "fp-1"


class _FakeService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def prepare(self, *, run_id: str):  # type: ignore[no-untyped-def]
        self.calls.append(("prepare", run_id))
        return type("IngestResult", (), {"inserted": 1, "updated": 2, "failed": 0})()

    def analyze(self, *, run_id: str, limit=None):  # type: ignore[no-untyped-def]
        self.calls.append(("analyze", (run_id, limit)))
        return type("AnalyzeResult", (), {"processed": 3, "failed": 0})()

    def publish(self, *, run_id: str, limit: int):  # type: ignore[no-untyped-def]
        self.calls.append(("publish", (run_id, limit)))
        return type("PublishResult", (), {"sent": 4, "skipped": 0, "failed": 0})()


def test_run_once_does_not_start_scheduler_and_runs_stages_in_order(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    def explode_apscheduler_import(module_name: str, *, attr_name: str | None = None):
        if module_name.startswith("apscheduler"):
            raise AssertionError("scheduler import should not happen for --once")
        return recoleta.cli._import_symbol(module_name, attr_name=attr_name)

    monkeypatch.setattr(recoleta.cli, "_import_symbol", explode_apscheduler_import)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "run",
            "--once",
            "--analyze-limit",
            "7",
            "--publish-limit",
            "9",
        ],
    )
    assert result.exit_code == 0
    assert "run --once completed" in result.stdout
    assert fake_repo.finished == [("run-1", True)]
    assert fake_service.calls == [
        ("prepare", "run-1"),
        ("analyze", ("run-1", 7)),
        ("publish", ("run-1", 9)),
    ]
