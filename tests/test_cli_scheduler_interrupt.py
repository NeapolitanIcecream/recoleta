from __future__ import annotations

import signal
from types import SimpleNamespace

from typer.testing import CliRunner

import recoleta.cli as cli


class _FakeSignalInterrupt(KeyboardInterrupt):
    def __init__(self, signum: int) -> None:
        super().__init__()
        self.signum = signum


class _FakeScheduler:
    latest: "_FakeScheduler | None" = None

    def __init__(self, **_: object) -> None:
        self.jobs: list[tuple[str, int]] = []
        self.shutdown_wait: list[bool] = []
        type(self).latest = self

    def add_job(
        self,
        _: object,
        __: str,
        *,
        minutes: int,
        id: str,
        replace_existing: bool,
    ) -> None:
        assert replace_existing is True
        self.jobs.append((id, minutes))

    def start(self) -> None:
        raise KeyboardInterrupt

    def shutdown(self, *, wait: bool) -> None:
        self.shutdown_wait.append(wait)


class _SigtermScheduler(_FakeScheduler):
    def start(self) -> None:
        raise _FakeSignalInterrupt(signal.SIGTERM)


def _install_scheduler_double(
    monkeypatch,
    scheduler_cls: type[_FakeScheduler],
) -> None:
    settings = SimpleNamespace(
        log_json=False,
        ingest_interval_minutes=5,
        analyze_interval_minutes=10,
        publish_interval_minutes=15,
    )
    monkeypatch.setattr(
        cli,
        "_build_runtime",
        lambda: (settings, object(), object()),
        raising=True,
    )
    original_import_symbol = cli._import_symbol

    def _fake_import_symbol(module_name: str, *, attr_name: str | None = None):
        if (
            module_name == "apscheduler.schedulers.blocking"
            and attr_name == "BlockingScheduler"
        ):
            return scheduler_cls
        return original_import_symbol(module_name, attr_name=attr_name)

    monkeypatch.setattr(cli, "_import_symbol", _fake_import_symbol, raising=True)


def test_run_scheduler_shuts_down_cleanly_on_keyboard_interrupt(
    monkeypatch,
) -> None:
    """Regression: scheduler mode should drain the current APScheduler job on Ctrl-C."""

    _FakeScheduler.latest = None
    _install_scheduler_double(monkeypatch, _FakeScheduler)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["run"])

    assert result.exit_code == 130
    scheduler = _FakeScheduler.latest
    assert scheduler is not None
    assert scheduler.jobs == [("ingest", 5), ("analyze", 10), ("publish", 15)]
    assert scheduler.shutdown_wait == [True]


def test_run_scheduler_preserves_sigterm_exit_code(monkeypatch) -> None:
    """Regression: SIGTERM should reuse graceful scheduler shutdown and exit 143."""

    _SigtermScheduler.latest = None
    _install_scheduler_double(monkeypatch, _SigtermScheduler)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["run"])

    assert result.exit_code == 143
    scheduler = _SigtermScheduler.latest
    assert scheduler is not None
    assert scheduler.shutdown_wait == [True]
