from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.cli.workflows as workflow_cli
from recoleta.types import DEFAULT_TOPIC_STREAM


class _FakeConsole:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def print(self, *parts: object) -> None:
        self.lines.append(" ".join(str(part) for part in parts))


class _FakeHeartbeatMonitor:
    def raise_if_failed(self) -> None:
        return None

    def stop(self) -> None:
        return None


class _FakeLog:
    def exception(self, *_: object, **__: object) -> None:
        return None

    def warning(self, *_: object, **__: object) -> None:
        return None


@dataclass(slots=True)
class _FakePolicy:
    recursive_lower_levels: bool = True
    delivery_mode: str = "all"
    translation: str = "auto"
    translate_include: list[str] | None = None
    site_build: bool = True
    on_translate_failure: str = "partial_success"

    def __post_init__(self) -> None:
        if self.translate_include is None:
            self.translate_include = ["items", "trends", "ideas"]


class _FakeWorkflows:
    def __init__(
        self,
        *,
        day: _FakePolicy | None = None,
        week: _FakePolicy | None = None,
        month: _FakePolicy | None = None,
        deploy: SimpleNamespace | None = None,
    ) -> None:
        self._policies = {
            "day": day or _FakePolicy(),
            "week": week or _FakePolicy(),
            "month": month or _FakePolicy(),
        }
        self.deploy = deploy or SimpleNamespace(
            translation="auto",
            translate_include=["items", "trends", "ideas"],
            site_build=True,
            on_translate_failure="partial_success",
        )

    def policy_for_granularity(self, granularity: str) -> _FakePolicy:
        return self._policies[granularity]


class _FakeLocalization:
    def __init__(self) -> None:
        self.targets = [SimpleNamespace(code="zh-cn", llm_label="Chinese")]
        self.site_default_language_code = "en"


class _FakeSettings:
    def __init__(
        self,
        *,
        tmp_path: Path,
        localization: _FakeLocalization | None = None,
        workflows: _FakeWorkflows | None = None,
    ) -> None:
        self.log_json = False
        self.publish_targets = ["markdown"]
        self.markdown_output_dir = tmp_path / "outputs"
        self.obsidian_vault_path = tmp_path / "vault"
        self.obsidian_base_folder = "Recoleta"
        self.analyze_limit = 8
        self.localization = localization
        self.workflows = workflows or _FakeWorkflows()

    def safe_fingerprint(self) -> str:
        return "fp-v2"

    def workflow_policy_for_granularity(self, granularity: str) -> _FakePolicy:
        return self.workflows.policy_for_granularity(granularity)

    def localization_target_codes(self) -> list[str]:
        if self.localization is None:
            return []
        return [target.code for target in self.localization.targets]


class _FakeRepo:
    def __init__(self) -> None:
        self.updated: list[dict[str, object]] = []
        self.finished: list[tuple[str, bool, str | None]] = []

    def update_run_context(self, **kwargs: object) -> None:
        self.updated.append(dict(kwargs))

    def finish_run(
        self,
        run_id: str,
        *,
        success: bool,
        terminal_state: str | None = None,
    ) -> None:
        self.finished.append((run_id, bool(success), terminal_state))

    def list_metrics(self, *, run_id: str) -> list[object]:
        _ = run_id
        return []


type _ServiceCall = tuple[str, tuple[object, ...]]


class _FakeService:
    def __init__(self) -> None:
        self.calls: list[_ServiceCall] = []

    def prepare(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        period_start=None,
        period_end=None,
    ):
        self.calls.append(("prepare", (run_id, period_start, period_end)))
        return SimpleNamespace(inserted=1, updated=0, failed=0)

    def analyze(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        limit=None,
        period_start=None,
        period_end=None,
    ):
        self.calls.append(("analyze", (run_id, limit, period_start, period_end)))
        return SimpleNamespace(processed=1, failed=0)

    def publish(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        limit: int,
        period_start=None,
        period_end=None,
    ):
        self.calls.append(("publish", (run_id, limit, period_start, period_end)))
        return SimpleNamespace(sent=1, skipped=0, failed=0)

    def trends(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        granularity: str,
        anchor_date: date | None = None,
        backfill: bool = False,
        backfill_mode: str = "missing",
        reuse_existing_corpus: bool = False,
    ):
        self.calls.append(
            (
                "trends",
                (
                    run_id,
                    granularity,
                    anchor_date,
                    backfill,
                    backfill_mode,
                    reuse_existing_corpus,
                ),
            )
        )
        if granularity == "week":
            period_start = datetime(2026, 3, 16, tzinfo=UTC)
            period_end = datetime(2026, 3, 23, tzinfo=UTC)
        elif granularity == "month":
            period_start = datetime(2026, 3, 1, tzinfo=UTC)
            period_end = datetime(2026, 4, 1, tzinfo=UTC)
        else:
            assert anchor_date is not None
            period_start = datetime(
                anchor_date.year,
                anchor_date.month,
                anchor_date.day,
                tzinfo=UTC,
            )
            period_end = period_start + timedelta(days=1)
        return SimpleNamespace(period_start=period_start, period_end=period_end)

    def ideas(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        granularity: str,
        anchor_date: date | None = None,
    ):
        self.calls.append(("ideas", (run_id, granularity, anchor_date)))
        if granularity == "week":
            period_start = datetime(2026, 3, 16, tzinfo=UTC)
            period_end = datetime(2026, 3, 23, tzinfo=UTC)
        elif granularity == "month":
            period_start = datetime(2026, 3, 1, tzinfo=UTC)
            period_end = datetime(2026, 4, 1, tzinfo=UTC)
        else:
            assert anchor_date is not None
            period_start = datetime(
                anchor_date.year,
                anchor_date.month,
                anchor_date.day,
                tzinfo=UTC,
            )
            period_end = period_start + timedelta(days=1)
        return SimpleNamespace(period_start=period_start, period_end=period_end)


def _install_workflow_runtime(
    monkeypatch: pytest.MonkeyPatch,
    *,
    settings: _FakeSettings,
    repository: _FakeRepo,
    service: _FakeService,
    import_symbol_override=None,
) -> _FakeConsole:
    console = _FakeConsole()
    heartbeat_monitor = _FakeHeartbeatMonitor()
    log = _FakeLog()
    monkeypatch.setattr(
        recoleta.cli,
        "_begin_managed_run",
        lambda *, command, log_module: (  # noqa: ARG005
            settings,
            repository,
            service,
            console,
            "run-1",
            "owner-1",
            log,
            heartbeat_monitor,
        ),
    )
    monkeypatch.setattr(recoleta.cli, "_cleanup_managed_run", lambda **_: None)
    if import_symbol_override is not None:
        original_import_symbol = recoleta.cli._import_symbol

        def _fake_import_symbol(module_name: str, *, attr_name: str | None = None):
            override = import_symbol_override(module_name, attr_name)
            if override is not None:
                return override
            return original_import_symbol(module_name, attr_name=attr_name)

        monkeypatch.setattr(recoleta.cli, "_import_symbol", _fake_import_symbol)
    return console


def test_run_week_executes_recursive_day_and_week_synthesis_workflow(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    site_build_calls: list[tuple[str, str]] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (default_language_code, limit)
                site_build_calls.append((str(input_dir), str(output_dir)))
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 9, "ideas_total": 9, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "week", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    assert len(site_build_calls) == 1
    prepare_calls = [call for call in fake_service.calls if call[0] == "prepare"]
    analyze_calls = [call for call in fake_service.calls if call[0] == "analyze"]
    publish_calls = [call for call in fake_service.calls if call[0] == "publish"]
    day_trend_calls = [
        call
        for call in fake_service.calls
        if call[0] == "trends" and call[1][1] == "day"
    ]
    day_ideas_calls = [
        call
        for call in fake_service.calls
        if call[0] == "ideas" and call[1][1] == "day"
    ]
    week_trend_calls = [
        call
        for call in fake_service.calls
        if call[0] == "trends" and call[1][1] == "week"
    ]
    week_ideas_calls = [
        call
        for call in fake_service.calls
        if call[0] == "ideas" and call[1][1] == "week"
    ]

    assert len(prepare_calls) == 7
    assert len(analyze_calls) == 7
    assert len(publish_calls) == 7
    assert len(day_trend_calls) == 7
    assert len(day_ideas_calls) == 7
    assert len(week_trend_calls) == 1
    assert len(week_ideas_calls) == 1
    assert all(call[1][5] is True for call in day_trend_calls + week_trend_calls)
    assert week_trend_calls[0][1][2] == date(2026, 3, 16)
    assert week_ideas_calls[0][1][2] == date(2026, 3, 16)
    assert fake_repo.finished == [("run-1", True, "succeeded_clean")]
    assert any(
        update.get("target_granularity") == "week"
        and update.get("target_period_start") == datetime(2026, 3, 16, tzinfo=UTC)
        and update.get("target_period_end") == datetime(2026, 3, 23, tzinfo=UTC)
        and update.get("requested_steps")
        == [
            "ingest",
            "analyze",
            "publish",
            "trends:day",
            "ideas:day",
            "trends:week",
            "ideas:week",
            "site-build",
        ]
        and update.get("skipped_steps") == ["translate"]
        for update in fake_repo.updated
    )


def test_run_day_marks_terminal_state_partial_when_translation_fails_but_site_build_succeeds(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path, localization=_FakeLocalization())
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    site_build_calls: list[int] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.translation" and attr_name == "run_translation":
            def _failing_translate(**kwargs):  # type: ignore[no-untyped-def]
                _ = kwargs
                raise RuntimeError("provider timeout")

            return _failing_translate
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                site_build_calls.append(1)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    assert len(site_build_calls) == 1
    assert fake_repo.finished == [("run-1", True, "succeeded_partial")]
    assert any(
        update.get("requested_steps")
        == [
            "ingest",
            "analyze",
            "publish",
            "trends:day",
            "ideas:day",
            "translate",
            "site-build",
        ]
        for update in fake_repo.updated
    )


def test_run_day_allows_skipping_ingest_analyze_and_publish_for_downstream_replay(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path, localization=_FakeLocalization())
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    translation_calls: list[dict[str, object]] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.translation" and attr_name == "run_translation":
            def _fake_translate(**kwargs):  # type: ignore[no-untyped-def]
                translation_calls.append(dict(kwargs))
                return SimpleNamespace(
                    scanned_total=2,
                    translated_total=2,
                    mirrored_total=0,
                    skipped_total=0,
                    failed_total=0,
                    aborted=False,
                    abort_reason=None,
                )

            return _fake_translate
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "run",
            "day",
            "--date",
            "2026-03-16",
            "--skip",
            "ingest,analyze,publish",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["requested_steps"] == [
        "trends:day",
        "ideas:day",
        "translate",
        "site-build",
    ]
    assert payload["executed_steps"] == payload["requested_steps"]
    assert payload["skipped_steps"] == ["ingest", "analyze", "publish"]
    assert [call[0] for call in fake_service.calls] == ["trends", "ideas"]
    assert len(translation_calls) == 1
    assert translation_calls[0]["period_start"] == datetime(2026, 3, 16, tzinfo=UTC)
    assert translation_calls[0]["period_end"] == datetime(2026, 3, 17, tzinfo=UTC)
    assert fake_repo.finished == [("run-1", True, "succeeded_clean")]


def test_run_week_allows_skipping_recursive_day_steps_for_settled_week_replay(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path, localization=_FakeLocalization())
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "run",
            "week",
            "--date",
            "2026-03-22",
            "--skip",
            "ingest,analyze,publish,trends:day,ideas:day,translate,site-build",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["requested_steps"] == ["trends:week", "ideas:week"]
    assert payload["executed_steps"] == payload["requested_steps"]
    assert payload["skipped_steps"] == [
        "ingest",
        "analyze",
        "publish",
        "trends:day",
        "ideas:day",
        "translate",
        "site-build",
    ]
    assert [call[0] for call in fake_service.calls] == ["trends", "ideas"]
    assert fake_service.calls[0][1][1] == "week"
    assert fake_service.calls[0][1][2] == date(2026, 3, 16)
    assert fake_service.calls[1][1][1] == "week"
    assert fake_service.calls[1][1][2] == date(2026, 3, 16)
    assert fake_repo.finished == [("run-1", True, "succeeded_clean")]


def test_run_day_passes_incremental_translation_window_to_workflow_step(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path, localization=_FakeLocalization())
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    translation_calls: list[dict[str, object]] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.translation" and attr_name == "run_translation":
            def _fake_translate(**kwargs):  # type: ignore[no-untyped-def]
                translation_calls.append(dict(kwargs))
                return SimpleNamespace(
                    scanned_total=1,
                    translated_total=1,
                    mirrored_total=0,
                    skipped_total=0,
                    failed_total=0,
                    aborted=False,
                    abort_reason=None,
                )

            return _fake_translate
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    assert len(translation_calls) == 1
    assert translation_calls[0]["all_history"] is False
    assert translation_calls[0]["period_start"] == datetime(2026, 3, 16, tzinfo=UTC)
    assert translation_calls[0]["period_end"] == datetime(2026, 3, 17, tzinfo=UTC)


def test_run_day_keeps_default_scope_for_instance_first_workflows(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: instance-first workflows should always run against the default scope."""
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(
        tmp_path=tmp_path,
        localization=_FakeLocalization(),
    )
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    translation_calls: list[dict[str, object]] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.translation" and attr_name == "run_translation":
            def _fake_translate(**kwargs):  # type: ignore[no-untyped-def]
                translation_calls.append(dict(kwargs))
                return SimpleNamespace(
                    scanned_total=1,
                    translated_total=1,
                    mirrored_total=0,
                    skipped_total=0,
                    failed_total=0,
                    aborted=False,
                    abort_reason=None,
                )

            return _fake_translate
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    assert len(translation_calls) == 1
    assert translation_calls[0]["scope"] == DEFAULT_TOPIC_STREAM
    assert fake_repo.updated[0]["scope"] == DEFAULT_TOPIC_STREAM


def test_run_month_executes_recursive_day_week_and_month_synthesis_workflow(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    site_build_calls: list[tuple[str, str]] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (default_language_code, limit)
                site_build_calls.append((str(input_dir), str(output_dir)))
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 39, "ideas_total": 39, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "month", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert len(site_build_calls) == 1
    prepare_calls = [call for call in fake_service.calls if call[0] == "prepare"]
    analyze_calls = [call for call in fake_service.calls if call[0] == "analyze"]
    publish_calls = [call for call in fake_service.calls if call[0] == "publish"]
    day_trend_calls = [
        call
        for call in fake_service.calls
        if call[0] == "trends" and call[1][1] == "day"
    ]
    day_ideas_calls = [
        call
        for call in fake_service.calls
        if call[0] == "ideas" and call[1][1] == "day"
    ]
    week_trend_calls = [
        call
        for call in fake_service.calls
        if call[0] == "trends" and call[1][1] == "week"
    ]
    week_ideas_calls = [
        call
        for call in fake_service.calls
        if call[0] == "ideas" and call[1][1] == "week"
    ]
    month_trend_calls = [
        call
        for call in fake_service.calls
        if call[0] == "trends" and call[1][1] == "month"
    ]
    month_ideas_calls = [
        call
        for call in fake_service.calls
        if call[0] == "ideas" and call[1][1] == "month"
    ]

    assert len(prepare_calls) == 31
    assert len(analyze_calls) == 31
    assert len(publish_calls) == 31
    assert len(day_trend_calls) == 31
    assert len(day_ideas_calls) == 31
    assert len(week_trend_calls) == 6
    assert len(week_ideas_calls) == 6
    assert len(month_trend_calls) == 1
    assert len(month_ideas_calls) == 1
    assert [call[1][2] for call in week_trend_calls] == [
        date(2026, 2, 23),
        date(2026, 3, 2),
        date(2026, 3, 9),
        date(2026, 3, 16),
        date(2026, 3, 23),
        date(2026, 3, 30),
    ]
    assert month_trend_calls[0][1][2] == date(2026, 3, 1)
    assert month_ideas_calls[0][1][2] == date(2026, 3, 1)
    assert payload["operation_kind"] == "workflow.run.month"
    assert payload["target_granularity"] == "month"
    assert payload["target_period_start"] == "2026-03-01T00:00:00+00:00"
    assert payload["target_period_end"] == "2026-04-01T00:00:00+00:00"
    assert payload["requested_steps"] == [
        "ingest",
        "analyze",
        "publish",
        "trends:day",
        "ideas:day",
        "trends:week",
        "ideas:week",
        "trends:month",
        "ideas:month",
        "site-build",
    ]
    assert payload["executed_steps"] == payload["requested_steps"]
    assert payload["skipped_steps"] == ["translate"]
    assert fake_repo.finished == [("run-1", True, "succeeded_clean")]


def test_run_now_aliases_run_day_for_today_utc(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    monkeypatch.setattr(workflow_cli, "_today_utc", lambda: date(2026, 3, 16))
    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "now", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["command"] == "run now"
    assert payload["operation_kind"] == "workflow.run.day"
    assert payload["target_granularity"] == "day"
    assert payload["target_period_start"] == "2026-03-16T00:00:00+00:00"
    assert payload["target_period_end"] == "2026-03-17T00:00:00+00:00"
    assert payload["requested_steps"] == [
        "ingest",
        "analyze",
        "publish",
        "trends:day",
        "ideas:day",
        "site-build",
    ]
    assert payload["executed_steps"] == payload["requested_steps"]
    assert len([call for call in fake_service.calls if call[0] == "prepare"]) == 1
    assert len([call for call in fake_service.calls if call[0] == "trends"]) == 1
    assert len([call for call in fake_service.calls if call[0] == "ideas"]) == 1
    assert fake_service.calls[-2][1][2] == date(2026, 3, 16)
    assert fake_service.calls[-1][1][2] == date(2026, 3, 16)


def test_run_day_defaults_to_latest_complete_utc_day(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    monkeypatch.setattr(workflow_cli, "_today_utc", lambda: date(2026, 3, 26))
    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["command"] == "run day"
    assert payload["operation_kind"] == "workflow.run.day"
    assert payload["target_granularity"] == "day"
    assert payload["target_period_start"] == "2026-03-25T00:00:00+00:00"
    assert payload["target_period_end"] == "2026-03-26T00:00:00+00:00"
    assert fake_service.calls[-2][1][2] == date(2026, 3, 25)
    assert fake_service.calls[-1][1][2] == date(2026, 3, 25)


def test_run_day_json_stdout_stays_machine_readable_when_steps_write_stdout(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path, localization=_FakeLocalization())
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.translation" and attr_name == "run_translation":
            def _fake_translate(**kwargs):  # type: ignore[no-untyped-def]
                _ = kwargs
                print("TRANSLATION STDOUT NOISE")
                return SimpleNamespace(
                    scanned_total=2,
                    translated_total=2,
                    mirrored_total=0,
                    skipped_total=0,
                    failed_total=0,
                    aborted=False,
                    abort_reason=None,
                )

            return _fake_translate
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                print("SITE BUILD STDOUT NOISE")
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["terminal_state"] == "succeeded_clean"
    assert "TRANSLATION STDOUT NOISE" not in result.stdout
    assert "SITE BUILD STDOUT NOISE" not in result.stdout
    assert "TRANSLATION STDOUT NOISE" in result.stderr
    assert "SITE BUILD STDOUT NOISE" in result.stderr


def test_run_day_include_publish_executes_publish_when_delivery_mode_is_none(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(
        tmp_path=tmp_path,
        workflows=_FakeWorkflows(day=_FakePolicy(delivery_mode="none", site_build=False)),
    )
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--include", "publish", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    publish_calls = [call for call in fake_service.calls if call[0] == "publish"]
    assert len(publish_calls) == 1
    assert "publish" in payload["requested_steps"]
    assert "publish" in payload["executed_steps"]
    assert payload["skipped_steps"] == ["translate", "site-build"]
    publish_step = next(
        step for step in payload["steps"] if step["step_id"] == "publish"
    )
    assert publish_step["status"] == "ok"
    assert publish_step["payload"] == {"sent": 1, "skipped": 0, "failed": 0}


def test_run_day_include_site_build_removes_reenabled_step_from_skipped_metadata(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(
        tmp_path=tmp_path,
        workflows=_FakeWorkflows(day=_FakePolicy(site_build=False)),
    )
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    site_build_calls: list[int] = []

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":
            def _fake_site_build(*, input_dir, output_dir, default_language_code=None, limit=None):  # type: ignore[no-untyped-def]
                _ = (input_dir, default_language_code, limit)
                site_build_calls.append(1)
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        return None

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "2026-03-16", "--include", "site-build", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert len(site_build_calls) == 1
    assert "site-build" in payload["requested_steps"]
    assert "site-build" in payload["executed_steps"]
    assert payload["skipped_steps"] == ["translate"]


def test_run_day_cleans_up_and_marks_failed_when_plan_building_fails(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    cleanup_calls: list[dict[str, object]] = []

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
    )
    monkeypatch.setattr(
        recoleta.cli,
        "_cleanup_managed_run",
        lambda **kwargs: cleanup_calls.append(dict(kwargs)),
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "day", "--date", "not-a-date"],
    )

    assert result.exit_code == 1
    assert len(cleanup_calls) == 1
    assert fake_repo.finished == [("run-1", False, "failed")]


def test_run_deploy_cleans_up_and_marks_failed_when_plan_building_fails(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    tmp_path: Path = configured_env
    fake_settings = _FakeSettings(tmp_path=tmp_path)
    fake_repo = _FakeRepo()
    fake_service = _FakeService()
    cleanup_calls: list[dict[str, object]] = []

    _install_workflow_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=fake_repo,
        service=fake_service,
    )
    monkeypatch.setattr(
        recoleta.cli,
        "_cleanup_managed_run",
        lambda **kwargs: cleanup_calls.append(dict(kwargs)),
    )

    def _raise_plan_error(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise ValueError("broken deploy plan")

    monkeypatch.setattr(workflow_cli, "_build_deploy_plan", _raise_plan_error)

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "deploy"],
    )

    assert result.exit_code == 1
    assert len(cleanup_calls) == 1
    assert fake_repo.finished == [("run-1", False, "failed")]


def test_run_once_surfaces_v2_migration_error() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["run", "--once"])

    assert result.exit_code == 2
    assert "run --once" in result.stdout
    assert "run now" in result.stdout
