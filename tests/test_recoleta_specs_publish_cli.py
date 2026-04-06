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
        return _FakeRun("run-publish")

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(self, **_: object) -> None:
        return None

    def release_workspace_lease(self, **_: object) -> bool:
        return True

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))


class _FakeSettings:
    log_json: bool
    publish_targets: list[str]
    obsidian_vault_path: Path | None
    obsidian_base_folder: str
    markdown_output_dir: Path

    def __init__(self) -> None:
        self.log_json = False
        self.publish_targets = []
        self.obsidian_vault_path = None
        self.obsidian_base_folder = "Inbox"
        self.markdown_output_dir = Path("/tmp/recoleta-output")

    def safe_fingerprint(self) -> str:
        return "fp-publish"


class _FakeService:
    def publish(
        self,
        *,
        run_id: str,
        limit: int,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ):  # type: ignore[no-untyped-def]
        assert run_id == "run-publish"
        assert limit == 9
        assert period_start == datetime(2026, 1, 2, tzinfo=UTC)
        assert period_end == datetime(2026, 1, 3, tzinfo=UTC)
        return type(
            "PublishResult",
            (),
            {
                "sent": 2,
                "skipped": 1,
                "failed": 0,
                "note_paths": [
                    Path("/tmp/recoleta-output/Inbox/2026-01-02-example.md")
                ],
            },
        )()


def test_publish_cli_passes_target_day_window_to_publish(
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
        ["publish", "--limit", "9", "--date", "2026-01-02"],
    )

    assert result.exit_code == 0
    assert "publish completed sent=2 skipped=1 failed=0" in result.stdout
    assert fake_repo.finished == [("run-publish", True)]


def test_publish_cli_emits_json_output(
    configured_env: Path,  # noqa: ARG001
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_settings.publish_targets = ["markdown", "obsidian"]
    fake_settings.markdown_output_dir = tmp_path / "output"
    fake_settings.obsidian_vault_path = tmp_path / "vault"
    fake_settings.obsidian_base_folder = "Research"
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["publish", "--limit", "9", "--date", "2026-01-02", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert fake_settings.obsidian_vault_path is not None
    assert payload["status"] == "ok"
    assert payload["command"] == "publish"
    assert payload["run_id"] == "run-publish"
    assert payload["sent"] == 2
    assert payload["skipped"] == 1
    assert payload["failed"] == 0
    assert payload["period_start"] == "2026-01-02T00:00:00+00:00"
    assert payload["period_end"] == "2026-01-03T00:00:00+00:00"
    assert payload["targets"] == ["markdown", "obsidian"]
    assert payload["markdown_output_dir"] == str(fake_settings.markdown_output_dir)
    assert payload["latest_index_path"] == str(
        fake_settings.markdown_output_dir / "latest.md"
    )
    assert payload["obsidian_inbox_path"] == str(
        fake_settings.obsidian_vault_path / fake_settings.obsidian_base_folder / "Inbox"
    )
    assert payload["note_paths"] == ["/tmp/recoleta-output/Inbox/2026-01-02-example.md"]
    assert fake_repo.finished == [("run-publish", True)]
