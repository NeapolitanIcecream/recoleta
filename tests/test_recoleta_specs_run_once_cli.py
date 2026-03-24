from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli


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
        self.topic_streams: list[object] = []

    def safe_fingerprint(self) -> str:
        return "fp-v2"

    def workflow_policy_for_granularity(self, granularity: str) -> _FakePolicy:
        return self.workflows.policy_for_granularity(granularity)

    def localization_target_codes(self) -> list[str]:
        if self.localization is None:
            return []
        return [target.code for target in self.localization.targets]

    def topic_stream_runtimes(self) -> list[SimpleNamespace]:
        return [SimpleNamespace(name="default", explicit=False)]


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


class _FakeService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

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
        anchor_date=None,
        backfill=False,
        backfill_mode="missing",
        reuse_existing_corpus=False,
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
        period_start, period_end = (
            (datetime(2026, 3, 16, tzinfo=UTC), datetime(2026, 3, 23, tzinfo=UTC))
            if granularity == "week"
            else (datetime(2026, 3, 1, tzinfo=UTC), datetime(2026, 4, 1, tzinfo=UTC))
            if granularity == "month"
            else (
                datetime(anchor_date.year, anchor_date.month, anchor_date.day, tzinfo=UTC),
                datetime(anchor_date.year, anchor_date.month, anchor_date.day, tzinfo=UTC)
                + timedelta(days=1),
            )
        )
        return SimpleNamespace(period_start=period_start, period_end=period_end)

    def ideas(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        granularity: str,
        anchor_date=None,
    ):
        self.calls.append(("ideas", (run_id, granularity, anchor_date)))
        period_start, period_end = (
            (datetime(2026, 3, 16, tzinfo=UTC), datetime(2026, 3, 23, tzinfo=UTC))
            if granularity == "week"
            else (datetime(2026, 3, 1, tzinfo=UTC), datetime(2026, 4, 1, tzinfo=UTC))
            if granularity == "month"
            else (
                datetime(anchor_date.year, anchor_date.month, anchor_date.day, tzinfo=UTC),
                datetime(anchor_date.year, anchor_date.month, anchor_date.day, tzinfo=UTC)
                + timedelta(days=1),
            )
        )
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
                    '{"trends_total": 9, "ideas_total": 9, "topics_total": 1, "streams_total": 1}',
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
                    '{"trends_total": 1, "ideas_total": 1, "topics_total": 1, "streams_total": 1}',
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


def test_run_once_surfaces_v2_migration_error() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["run", "--once"])

    assert result.exit_code == 2
    assert "run --once" in result.stdout
    assert "run now" in result.stdout
