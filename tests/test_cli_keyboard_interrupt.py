from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
import typer

import recoleta.cli as cli


class _FakeRun:
    def __init__(self, run_id: str) -> None:
        self.id = run_id


class _FakeRepository:
    def __init__(self) -> None:
        self.finished: list[tuple[str, bool]] = []

    def create_run(self, *, config_fingerprint: str) -> _FakeRun:  # noqa: ARG002
        return _FakeRun("run-1")

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, success))


def test_execute_stage_marks_run_failed_on_keyboard_interrupt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Regression: Ctrl-C should finish the run and exit cleanly."""

    settings = SimpleNamespace(safe_fingerprint=lambda: "fp")  # noqa: E731
    repo = _FakeRepository()
    service = object()

    monkeypatch.setattr(cli, "_build_runtime", lambda: (settings, repo, service), raising=True)

    def _runner(_: Any, __: str) -> Any:  # noqa: ANN401
        raise KeyboardInterrupt

    with pytest.raises(typer.Exit) as exc:
        cli._execute_stage(stage_name="ingest", stage_runner=_runner)

    assert exc.value.exit_code == 130
    assert repo.finished == [("run-1", False)]

