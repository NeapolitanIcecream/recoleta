from __future__ import annotations

import signal
from datetime import date
from types import SimpleNamespace

from typer.testing import CliRunner

import recoleta.cli as cli
import recoleta.cli.workflows as workflows
from recoleta.cli.workflow_runner import scheduled_anchor_dates


class _FakeSignalInterrupt(KeyboardInterrupt):
    def __init__(self, signum: int) -> None:
        super().__init__()
        self.signum = signum


class _FakeScheduler:
    latest: "_FakeScheduler | None" = None

    def __init__(self, **_: object) -> None:
        self.jobs: list[tuple[str, str, dict[str, object]]] = []
        self.shutdown_wait: list[bool] = []
        type(self).latest = self

    def add_job(
        self,
        _: object,
        trigger: str,
        *,
        id: str,
        replace_existing: bool,
        **kwargs: object,
    ) -> None:
        assert replace_existing is True
        self.jobs.append((id, trigger, dict(kwargs)))

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
    *,
    schedules: list[SimpleNamespace] | None = None,
) -> None:
    resolved_schedules = schedules or [
        SimpleNamespace(
            workflow="day",
            interval_minutes=60,
            weekday=None,
            hour_utc=None,
            minute_utc=None,
        ),
        SimpleNamespace(
            workflow="week",
            interval_minutes=None,
            weekday="mon",
            hour_utc=2,
            minute_utc=0,
        ),
        SimpleNamespace(
            workflow="deploy",
            interval_minutes=None,
            weekday="mon",
            hour_utc=2,
            minute_utc=30,
        ),
    ]
    settings = SimpleNamespace(
        log_json=False,
        daemon=SimpleNamespace(schedules=resolved_schedules),
    )
    monkeypatch.setattr(cli, "_build_settings", lambda: settings, raising=True)
    original_import_symbol = cli._import_symbol

    def _fake_import_symbol(module_name: str, *, attr_name: str | None = None):
        if (
            module_name == "apscheduler.schedulers.blocking"
            and attr_name == "BlockingScheduler"
        ):
            return scheduler_cls
        return original_import_symbol(module_name, attr_name=attr_name)

    monkeypatch.setattr(cli, "_import_symbol", _fake_import_symbol, raising=True)


def test_daemon_start_shuts_down_cleanly_on_keyboard_interrupt(monkeypatch) -> None:
    _FakeScheduler.latest = None
    _install_scheduler_double(monkeypatch, _FakeScheduler)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["daemon", "start"])

    assert result.exit_code == 130
    scheduler = _FakeScheduler.latest
    assert scheduler is not None
    assert scheduler.jobs == [
        ("workflow:day:interval:60:0", "interval", {"minutes": 60}),
        (
            "workflow:week:cron:mon:2:0:1",
            "cron",
            {"day_of_week": "mon", "hour": 2, "minute": 0},
        ),
        (
            "workflow:deploy:cron:mon:2:30:2",
            "cron",
            {"day_of_week": "mon", "hour": 2, "minute": 30},
        ),
    ]
    assert scheduler.shutdown_wait == [True]


def test_daemon_start_keeps_multiple_schedule_entries_for_same_workflow(
    monkeypatch,
) -> None:
    _FakeScheduler.latest = None
    _install_scheduler_double(
        monkeypatch,
        _FakeScheduler,
        schedules=[
            SimpleNamespace(
                workflow="day",
                interval_minutes=60,
                weekday=None,
                hour_utc=None,
                minute_utc=None,
            ),
            SimpleNamespace(
                workflow="day",
                interval_minutes=None,
                weekday="mon",
                hour_utc=2,
                minute_utc=0,
            ),
        ],
    )

    runner = CliRunner()
    result = runner.invoke(cli.app, ["daemon", "start"])

    assert result.exit_code == 130
    scheduler = _FakeScheduler.latest
    assert scheduler is not None
    assert scheduler.jobs == [
        ("workflow:day:interval:60:0", "interval", {"minutes": 60}),
        (
            "workflow:day:cron:mon:2:0:1",
            "cron",
            {"day_of_week": "mon", "hour": 2, "minute": 0},
        ),
    ]
    assert scheduler.jobs[0][0] != scheduler.jobs[1][0]


def test_daemon_start_preserves_sigterm_exit_code(monkeypatch) -> None:
    _SigtermScheduler.latest = None
    _install_scheduler_double(monkeypatch, _SigtermScheduler)

    runner = CliRunner()
    result = runner.invoke(cli.app, ["daemon", "start"])

    assert result.exit_code == 143
    scheduler = _SigtermScheduler.latest
    assert scheduler is not None
    assert scheduler.shutdown_wait == [True]


def test_scheduled_anchor_dates_use_only_closed_periods_and_bound_catch_up() -> None:
    today = date(2026, 7, 22)

    assert scheduled_anchor_dates(
        workflow_name="day", today=today, catch_up_windows=3
    ) == [date(2026, 7, 19), date(2026, 7, 20), date(2026, 7, 21)]
    assert scheduled_anchor_dates(
        workflow_name="week", today=today, catch_up_windows=2
    ) == [date(2026, 7, 6), date(2026, 7, 13)]
    assert scheduled_anchor_dates(
        workflow_name="month", today=today, catch_up_windows=2
    ) == [date(2026, 5, 1), date(2026, 6, 1)]


def test_scheduled_runner_reconciles_bounded_windows_oldest_first(
    monkeypatch,
) -> None:
    calls: list[dict[str, object]] = []
    monkeypatch.setattr(workflows, "_today_utc", lambda: date(2026, 7, 22))
    monkeypatch.setattr(
        workflows,
        "execute_granularity_workflow",
        lambda **kwargs: calls.append(dict(kwargs)),
    )
    schedule = SimpleNamespace(catch_up_windows=2)

    workflows._scheduled_workflow_runner("week", schedule)()

    assert [call["anchor_date"] for call in calls] == ["2026-07-06", "2026-07-13"]
    assert all(call["command"] == "daemon week" for call in calls)
