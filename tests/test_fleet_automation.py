from __future__ import annotations

from contextlib import contextmanager
from datetime import date
import importlib
from pathlib import Path
import subprocess
import sys
import textwrap
from types import SimpleNamespace
from typing import Iterator

import pytest
from typer.testing import CliRunner
import yaml

import recoleta.cli as cli
import recoleta.cli.fleet as fleet_cli
from recoleta.fleet import (
    FleetSequenceBusyError,
    fleet_sequence_lease,
    fleet_sequence_lock_path,
    load_fleet_manifest,
)


def _write_manifest(tmp_path: Path) -> Path:
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    config_path = tmp_path / "child.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "recoleta_db_path": str(tmp_path / "child.db"),
                "llm_model": "openai/gpt-4o-mini",
                "topics": ["agents"],
                "publish_targets": ["markdown"],
                "markdown_output_dir": str(output_dir),
            }
        ),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "fleet.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "daemon": {
                    "schedules": [
                        {
                            "workflow": "week",
                            "weekday": "mon",
                            "hour_utc": 2,
                            "minute_utc": 0,
                            "catch_up_windows": 2,
                        }
                    ]
                },
                "instances": [
                    {"name": "agents", "config_path": str(config_path)}
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def test_fleet_manifest_owns_validated_daemon_schedules(tmp_path: Path) -> None:
    manifest = load_fleet_manifest(_write_manifest(tmp_path))

    assert len(manifest.daemon.schedules) == 1
    schedule = manifest.daemon.schedules[0]
    assert schedule.workflow == "week"
    assert schedule.catch_up_windows == 2


def test_fleet_sequence_lease_rejects_overlapping_process_owner(
    tmp_path: Path,
) -> None:
    manifest_path = _write_manifest(tmp_path)

    with fleet_sequence_lease(manifest_path):
        with pytest.raises(FleetSequenceBusyError, match="already running"):
            with fleet_sequence_lease(manifest_path):
                pytest.fail("overlapping fleet lease must not be admitted")


def test_fleet_sequence_lease_supports_read_only_manifest_mount(
    tmp_path: Path,
) -> None:
    config_dir = tmp_path / "readonly-config"
    config_dir.mkdir()
    manifest_path = _write_manifest(config_dir)
    config_dir.chmod(0o555)
    try:
        with fleet_sequence_lease(manifest_path):
            assert fleet_sequence_lock_path(manifest_path).parent != config_dir
    finally:
        config_dir.chmod(0o755)


def test_fleet_module_does_not_import_unix_locking_directly() -> None:
    """The fleet CLI must remain importable on platforms without ``fcntl``."""
    script = textwrap.dedent(
        """
        import builtins

        original_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            importer = (globals or {}).get("__name__")
            if name == "fcntl" and importer == "recoleta.fleet":
                raise ModuleNotFoundError("No module named 'fcntl'")
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = guarded_import

        import recoleta.fleet
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_scheduled_fleet_runner_reconciles_oldest_outstanding_windows_under_one_lease(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path = _write_manifest(tmp_path)
    calls: list[dict[str, object]] = []
    lease_events: list[str] = []

    @contextmanager
    def _fake_lease(path: Path) -> Iterator[None]:
        assert path == manifest_path
        lease_events.append("acquire")
        yield
        lease_events.append("release")

    monkeypatch.setattr(fleet_cli, "_today_utc", lambda: date(2026, 7, 22))
    monkeypatch.setattr(fleet_cli, "fleet_sequence_lease", _fake_lease)
    monkeypatch.setattr(
        fleet_cli,
        "_fleet_completed_workflow_anchor_dates",
        lambda **_kwargs: [
            date(2026, 7, 16),
            date(2026, 7, 20),
            date(2026, 7, 21),
        ],
        raising=False,
    )
    monkeypatch.setattr(
        fleet_cli,
        "execute_fleet_granularity_workflow",
        lambda **kwargs: calls.append(dict(kwargs)),
    )

    fleet_cli._scheduled_fleet_workflow_runner(
        manifest_path=manifest_path,
        workflow_name="day",
        schedule=SimpleNamespace(catch_up_windows=2),
        run_history_repositories=[object()],
    )()

    assert lease_events == ["acquire", "release"]
    assert [call["anchor_date"] for call in calls] == [
        "2026-07-17",
        "2026-07-18",
    ]
    assert all(call["_sequence_lock_held"] is True for call in calls)


def test_fleet_daemon_start_cli_forwards_manifest(tmp_path: Path, monkeypatch) -> None:
    manifest_path = _write_manifest(tmp_path)
    app_module = importlib.import_module("recoleta.cli.app")
    captured: dict[str, object] = {}
    monkeypatch.setattr(
        app_module,
        "run_fleet_daemon_start_command",
        lambda **kwargs: captured.update(kwargs),
    )

    result = CliRunner().invoke(
        cli.app,
        ["fleet", "daemon", "start", "--manifest", str(manifest_path)],
    )

    assert result.exit_code == 0, result.stdout
    assert captured == {"manifest_path": manifest_path}
