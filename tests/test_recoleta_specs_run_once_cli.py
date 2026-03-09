from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import signal
from types import SimpleNamespace

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

    def acquire_workspace_lease(self, **_: object) -> None:
        return None

    def mark_stale_runs_failed(self, **_: object) -> int:
        return 0

    def create_run(
        self, *, config_fingerprint: str, run_id: str | None = None
    ) -> _FakeRun:  # noqa: ARG002
        self.created.append(config_fingerprint)
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
                name="pipeline.analyze.llm_calls_total", value=3.0, unit="count"
            ),
            SimpleNamespace(
                name="pipeline.analyze.llm_prompt_tokens_total",
                value=10.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.analyze.llm_completion_tokens_total",
                value=5.0,
                unit="count",
            ),
            SimpleNamespace(
                name="pipeline.analyze.estimated_cost_usd", value=0.012345, unit="usd"
            ),
        ]


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


class _InterruptingService(_FakeService):
    def prepare(self, *, run_id: str):  # type: ignore[no-untyped-def]
        self.calls.append(("prepare", run_id))
        raise KeyboardInterrupt


class _FakeSignalInterrupt(KeyboardInterrupt):
    def __init__(self, signum: int) -> None:
        super().__init__()
        self.signum = signum


class _SignalInterruptingService(_FakeService):
    def prepare(self, *, run_id: str):  # type: ignore[no-untyped-def]
        self.calls.append(("prepare", run_id))
        raise _FakeSignalInterrupt(signal.SIGTERM)


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
    assert "Billing report" in result.stdout
    assert fake_repo.finished == [("run-1", True)]
    assert fake_service.calls == [
        ("prepare", "run-1"),
        ("analyze", ("run-1", 7)),
        ("publish", ("run-1", 9)),
    ]


def test_run_once_prints_billing_report_on_keyboard_interrupt(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _InterruptingService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(recoleta.cli.app, ["run", "--once"])
    assert result.exit_code == 130
    assert "Billing report" in result.stdout
    assert fake_repo.finished == [("run-1", False)]


def test_run_once_preserves_sigterm_exit_code(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: SIGTERM should reuse run cleanup and billing-report output."""

    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _SignalInterruptingService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(recoleta.cli.app, ["run", "--once"])
    assert result.exit_code == 143
    assert "Billing report" in result.stdout
    assert fake_repo.finished == [("run-1", False)]
