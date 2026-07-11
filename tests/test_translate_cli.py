from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

import pytest

import recoleta.cli.translate as translate_cli
import recoleta.translation as translation_module


class _FakeConsole:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def print(self, *parts: object) -> None:
        self.lines.append(" ".join(str(part) for part in parts))


class _FakeHeartbeatMonitor:
    def raise_if_failed(self) -> None:
        return None


class _FakeLog:
    def exception(self, *_args: object, **_kwargs: object) -> None:
        return None

    def warning(self, *_args: object, **_kwargs: object) -> None:
        return None


class _FakeRepository:
    def __init__(self) -> None:
        self.updated: list[dict[str, object]] = []
        self.finished: list[tuple[str, bool]] = []

    def update_run_context(self, **kwargs: object) -> None:
        self.updated.append(dict(kwargs))

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))

    def list_metrics(self, *, run_id: str) -> list[object]:
        _ = run_id
        return []


def _translation_result(
    *,
    failed_total: int,
    aborted: bool,
    abort_reason: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        scanned_total=4,
        translated_total=2,
        mirrored_total=1,
        skipped_total=1,
        failed_total=failed_total,
        aborted=aborted,
        abort_reason=abort_reason,
    )


def _run_translate_json_with_result(
    *,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    result: object,
    command_kwargs: dict[str, object] | None = None,
) -> tuple[
    dict[str, Any],
    _FakeRepository,
    object,
    list[dict[str, object]],
    list[dict[str, object]],
]:
    class _WorkspaceLeaseLostError(Exception):
        pass

    fake_repo = _FakeRepository()
    fake_settings = SimpleNamespace(log_json=False)
    fake_console = _FakeConsole()
    materialize_calls: list[dict[str, object]] = []
    translation_calls: list[dict[str, object]] = []

    def _fake_runtime_symbols() -> dict[str, object]:
        return {"WorkspaceLeaseLostError": _WorkspaceLeaseLostError}

    def _fake_load_runtime(*, request: object) -> object:
        _ = request
        return SimpleNamespace(
            resolved_db_path=tmp_path / "recoleta.sqlite",
            repository=fake_repo,
            settings=fake_settings,
            console=fake_console,
        )

    @contextmanager
    def _fake_managed_run_for_settings(
        *,
        settings: object,
        repository: object,
        console: object,
        command: str,
        log_module: str,
    ) -> Iterator[object]:
        _ = (settings, repository, console, command, log_module)
        yield SimpleNamespace(
            run_id="run-translate",
            owner_token="owner-token",
            log=_FakeLog(),
            heartbeat_monitor=_FakeHeartbeatMonitor(),
        )

    def _fake_run_translation(**kwargs: Any) -> object:
        translation_calls.append(dict(kwargs))
        return result

    def _fake_materialize_localized_projections(
        *,
        repository: object,
        settings: object,
    ) -> None:
        materialize_calls.append({"repository": repository, "settings": settings})

    monkeypatch.setattr(translate_cli.cli, "_runtime_symbols", _fake_runtime_symbols)
    monkeypatch.setattr(translate_cli, "load_runtime", _fake_load_runtime)
    monkeypatch.setattr(
        translate_cli,
        "managed_run_for_settings",
        _fake_managed_run_for_settings,
    )
    monkeypatch.setattr(translation_module, "run_translation", _fake_run_translation)
    monkeypatch.setattr(
        translation_module,
        "materialize_localized_projections",
        _fake_materialize_localized_projections,
    )

    base_kwargs: dict[str, object] = {
        "db_path": None,
        "config_path": None,
        "granularity": "week",
        "include": "items,trends",
        "limit": 3,
        "force": False,
        "context_assist": "direct",
        "model": None,
        "json_output": True,
        "command_name": "run translate",
    }
    if command_kwargs is not None:
        base_kwargs.update(command_kwargs)

    translate_cli.run_translate_run_command(**base_kwargs)

    payload: dict[str, Any] = json.loads(capsys.readouterr().out)
    return payload, fake_repo, fake_settings, materialize_calls, translation_calls


def _assert_translate_json_payload(
    *,
    payload: dict[str, Any],
    fake_repo: _FakeRepository,
    fake_settings: object,
    materialize_calls: list[dict[str, object]],
    expected_status: str,
    expected_failed: int,
    expected_aborted: bool,
    expected_abort_reason: str | None,
    expected_materialized: bool,
) -> None:
    assert payload["status"] == expected_status
    assert payload["command"] == "run translate"
    assert payload["run_id"] == "run-translate"
    assert payload["aborted"] is expected_aborted
    assert payload["abort_reason"] == expected_abort_reason
    assert payload["totals"] == {
        "scanned": 4,
        "translated": 2,
        "mirrored": 1,
        "skipped": 1,
        "failed": expected_failed,
    }
    expected_materialize_calls = (
        [{"repository": fake_repo, "settings": fake_settings}]
        if expected_materialized
        else []
    )
    assert materialize_calls == expected_materialize_calls
    assert fake_repo.finished == [("run-translate", not expected_aborted)]


def test_translate_run_json_reports_ok_when_outputs_are_clean(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = _translation_result(failed_total=0, aborted=False)
    payload, fake_repo, fake_settings, materialize_calls, _translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
        )
    )

    _assert_translate_json_payload(
        payload=payload,
        fake_repo=fake_repo,
        fake_settings=fake_settings,
        materialize_calls=materialize_calls,
        expected_status="ok",
        expected_failed=0,
        expected_aborted=False,
        expected_abort_reason=None,
        expected_materialized=True,
    )


def test_translate_run_json_reports_partial_failure_when_outputs_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Regression: non-aborted translation failures must not emit status=ok."""

    result = _translation_result(failed_total=1, aborted=False)
    payload, fake_repo, fake_settings, materialize_calls, _translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
        )
    )

    _assert_translate_json_payload(
        payload=payload,
        fake_repo=fake_repo,
        fake_settings=fake_settings,
        materialize_calls=materialize_calls,
        expected_status="partial_failure",
        expected_failed=1,
        expected_aborted=False,
        expected_abort_reason=None,
        expected_materialized=True,
    )


def test_translate_run_json_reports_aborted_when_translation_aborts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = _translation_result(
        failed_total=2,
        aborted=True,
        abort_reason="translation aborted",
    )
    payload, fake_repo, fake_settings, materialize_calls, _translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
        )
    )

    _assert_translate_json_payload(
        payload=payload,
        fake_repo=fake_repo,
        fake_settings=fake_settings,
        materialize_calls=materialize_calls,
        expected_status="aborted",
        expected_failed=2,
        expected_aborted=True,
        expected_abort_reason="translation aborted",
        expected_materialized=False,
    )


def test_translate_run_force_rejects_unbounded_history_without_explicit_all_history(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Regression: forced standalone translate reruns must not scan history implicitly."""

    runtime_calls: list[object] = []

    def _fake_load_runtime(*, request: object) -> object:
        runtime_calls.append(request)
        raise AssertionError("runtime should not load for invalid forced scope")

    monkeypatch.setattr(translate_cli, "load_runtime", _fake_load_runtime)

    with pytest.raises(translate_cli.cli.typer.Exit) as exc_info:
        translate_cli.run_translate_run_command(
            db_path=None,
            config_path=None,
            granularity="day",
            include="items,trends,ideas",
            limit=None,
            force=True,
            all_history=False,
            context_assist="direct",
            json_output=True,
            command_name="run translate",
        )

    payload: dict[str, Any] = json.loads(capsys.readouterr().out)
    assert exc_info.value.exit_code == 2
    assert payload["status"] == "error"
    assert "--force" in payload["error"]
    assert "--all-history" in payload["error"]
    assert "--granularity is not a date filter" in payload["error"]
    assert runtime_calls == []


def test_translate_run_force_with_date_uses_bounded_granularity_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = _translation_result(failed_total=0, aborted=False)

    payload, fake_repo, _fake_settings, _materialize_calls, translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
            command_kwargs={
                "granularity": "week",
                "force": True,
                "date": "2026-03-18",
            },
        )
    )

    assert len(translation_calls) == 1
    assert translation_calls[0]["force"] is True
    assert translation_calls[0]["all_history"] is False
    assert translation_calls[0]["period_start"] == datetime(2026, 3, 16, tzinfo=UTC)
    assert translation_calls[0]["period_end"] == datetime(2026, 3, 23, tzinfo=UTC)
    assert payload["all_history"] is False
    assert payload["period_start"] == "2026-03-16T00:00:00+00:00"
    assert payload["period_end"] == "2026-03-23T00:00:00+00:00"
    assert fake_repo.updated == [
        {
            "run_id": "run-translate",
            "scope": "default",
            "granularity": "week",
            "period_start": datetime(2026, 3, 16, tzinfo=UTC),
            "period_end": datetime(2026, 3, 23, tzinfo=UTC),
        }
    ]


def test_translate_run_force_with_date_defaults_to_day_granularity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Regression: default dated force reruns must not include week/month trend docs."""

    result = _translation_result(failed_total=0, aborted=False)

    payload, fake_repo, _fake_settings, _materialize_calls, translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
            command_kwargs={
                "granularity": None,
                "force": True,
                "date": "2026-03-18",
            },
        )
    )

    assert len(translation_calls) == 1
    assert translation_calls[0]["granularity"] == "day"
    assert translation_calls[0]["all_history"] is False
    assert translation_calls[0]["period_start"] == datetime(2026, 3, 18, tzinfo=UTC)
    assert translation_calls[0]["period_end"] == datetime(2026, 3, 19, tzinfo=UTC)
    assert payload["granularity"] == "day"
    assert payload["period_start"] == "2026-03-18T00:00:00+00:00"
    assert payload["period_end"] == "2026-03-19T00:00:00+00:00"
    assert fake_repo.updated == [
        {
            "run_id": "run-translate",
            "scope": "default",
            "granularity": "day",
            "period_start": datetime(2026, 3, 18, tzinfo=UTC),
            "period_end": datetime(2026, 3, 19, tzinfo=UTC),
        }
    ]


def test_translate_run_force_all_history_allows_unbounded_rerun(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = _translation_result(failed_total=0, aborted=False)

    payload, _fake_repo, _fake_settings, _materialize_calls, translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
            command_kwargs={
                "granularity": "day",
                "force": True,
                "all_history": True,
            },
        )
    )

    assert len(translation_calls) == 1
    assert translation_calls[0]["force"] is True
    assert translation_calls[0]["all_history"] is True
    assert translation_calls[0]["period_start"] is None
    assert translation_calls[0]["period_end"] is None
    assert payload["all_history"] is True
    assert payload["period_start"] is None
    assert payload["period_end"] is None


def test_translate_run_rejects_all_history_with_bounded_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    runtime_calls: list[object] = []

    def _fake_load_runtime(*, request: object) -> object:
        runtime_calls.append(request)
        raise AssertionError("runtime should not load for invalid translate scope")

    monkeypatch.setattr(translate_cli, "load_runtime", _fake_load_runtime)

    with pytest.raises(translate_cli.cli.typer.Exit) as exc_info:
        translate_cli.run_translate_run_command(
            db_path=None,
            config_path=None,
            granularity="day",
            include="items,trends,ideas",
            limit=None,
            force=True,
            date="2026-03-16",
            all_history=True,
            context_assist="direct",
            json_output=True,
            command_name="run translate",
        )

    payload: dict[str, Any] = json.loads(capsys.readouterr().out)
    assert exc_info.value.exit_code == 2
    assert payload == {
        "status": "error",
        "error": "--all-history cannot be combined with --date or --period-start/--period-end",
    }
    assert runtime_calls == []


def test_translate_run_command_passes_model_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result = _translation_result(failed_total=0, aborted=False)
    _payload, _repo, _settings, _materialize_calls, translation_calls = (
        _run_translate_json_with_result(
            tmp_path=tmp_path,
            monkeypatch=monkeypatch,
            capsys=capsys,
            result=result,
            command_kwargs={"model": "test/translation-override"},
        )
    )

    assert translation_calls
    assert translation_calls[0]["llm_model"] == "test/translation-override"


def test_translate_backfill_command_passes_model_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _WorkspaceLeaseLostError(Exception):
        pass

    fake_repo = _FakeRepository()
    fake_settings = SimpleNamespace(log_json=False)
    fake_console = _FakeConsole()
    backfill_calls: list[dict[str, Any]] = []

    def _fake_runtime_symbols() -> dict[str, object]:
        return {"WorkspaceLeaseLostError": _WorkspaceLeaseLostError}

    def _fake_load_runtime(*, request: object) -> object:
        _ = request
        return SimpleNamespace(
            resolved_db_path=tmp_path / "recoleta.sqlite",
            repository=fake_repo,
            settings=fake_settings,
            console=fake_console,
        )

    @contextmanager
    def _fake_managed_run_for_settings(
        *,
        settings: object,
        repository: object,
        console: object,
        command: str,
        log_module: str,
    ) -> Iterator[object]:
        _ = (settings, repository, console, command, log_module)
        yield SimpleNamespace(
            run_id="run-translate-backfill",
            owner_token="owner-token",
            log=_FakeLog(),
            heartbeat_monitor=_FakeHeartbeatMonitor(),
        )

    def _fake_run_translation_backfill(**kwargs: Any) -> object:
        backfill_calls.append(dict(kwargs))
        return _translation_result(failed_total=0, aborted=False)

    monkeypatch.setattr(translate_cli.cli, "_runtime_symbols", _fake_runtime_symbols)
    monkeypatch.setattr(translate_cli, "load_runtime", _fake_load_runtime)
    monkeypatch.setattr(
        translate_cli,
        "managed_run_for_settings",
        _fake_managed_run_for_settings,
    )
    monkeypatch.setattr(
        translation_module,
        "run_translation_backfill",
        _fake_run_translation_backfill,
    )

    translate_cli.run_translate_backfill_command(
        db_path=None,
        config_path=None,
        granularity="week",
        include="items,trends",
        limit=3,
        force=False,
        context_assist="direct",
        model="test/translation-backfill-override",
        legacy_source_language=None,
        emit_mirror_targets=False,
        all_history=False,
        json_output=False,
        command_name="stage translate backfill",
    )

    assert backfill_calls
    assert backfill_calls[0]["llm_model"] == "test/translation-backfill-override"
