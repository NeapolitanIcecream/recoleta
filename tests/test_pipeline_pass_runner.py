from __future__ import annotations

from datetime import UTC, datetime

from recoleta.passes.base import PassOutputEnvelope, PassStatus
from recoleta.pipeline.pass_runner import (
    PassDefinition,
    PassExecutionResult,
    PassPersistSpec,
    ProjectionSpec,
    run_pass_definition,
    persist_pass_output_envelope,
    run_projection_specs,
)


class _FakeLog:
    def __init__(self) -> None:
        self.warnings: list[tuple[str, dict[str, object]]] = []

    def warning(self, message: str, **kwargs: object) -> None:
        self.warnings.append((message, kwargs))


class _FakeRow:
    def __init__(self, row_id: int) -> None:
        self.id = row_id


class _FakeRepository:
    def __init__(self, *, row_id: int = 1, should_fail: bool = False) -> None:
        self.row_id = row_id
        self.should_fail = should_fail
        self.calls: list[dict[str, object]] = []

    def create_pass_output(self, **kwargs: object) -> _FakeRow:
        self.calls.append(kwargs)
        if self.should_fail:
            raise RuntimeError("simulated pass output failure")
        return _FakeRow(self.row_id)


type _ProjectionState = dict[str, int | None]


def test_run_projection_specs_returns_named_results_and_records_metrics() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    results = run_projection_specs(
        record_metric=_record_metric,
        specs=[
            ProjectionSpec(
                name="markdown",
                enabled=True,
                metric_base="pipeline.trends.projection.trend_markdown",
                log=_FakeLog(),
                failure_message="unused",
                execute=lambda: "note.md",
            ),
            ProjectionSpec(
                name="obsidian",
                enabled=True,
                metric_base="pipeline.trends.projection.trend_obsidian",
                log=_FakeLog(),
                failure_message="projection failed error_type={error_type} error={error}",
                execute=lambda: (_ for _ in ()).throw(
                    RuntimeError("simulated projection failure")
                ),
                reraise=False,
            ),
        ],
    )

    assert results == {"markdown": "note.md", "obsidian": None}
    assert recorded_metrics == [
        ("pipeline.trends.projection.trend_markdown.emitted_total", 1, "count"),
        ("pipeline.trends.projection.trend_obsidian.failed_total", 1, "count"),
    ]


def test_persist_pass_output_envelope_records_failure_metric_when_nonfatal() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []
    captured_failures: list[str] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    log = _FakeLog()
    envelope = PassOutputEnvelope(
        pass_kind="trend_synthesis",
        status=PassStatus.SUCCEEDED,
        run_id="run-pass-runner-failure",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
    )

    persisted_id = persist_pass_output_envelope(
        repository=_FakeRepository(should_fail=True),
        record_metric=_record_metric,
        spec=PassPersistSpec(
            envelope=envelope,
            period_start=datetime(2026, 3, 2, tzinfo=UTC),
            period_end=datetime(2026, 3, 3, tzinfo=UTC),
            log=log,
            failure_message=(
                "Pass output persist failed pass_kind={pass_kind} "
                "error_type={error_type} error={error}"
            ),
            sanitize_error=lambda message: message.upper(),
            on_failure=lambda exc: captured_failures.append(type(exc).__name__),
            reraise=False,
        ),
    )

    assert persisted_id is None
    assert captured_failures == ["RuntimeError"]
    assert recorded_metrics == [
        ("pipeline.trends.pass_outputs.persist_failed_total", 1, "count")
    ]
    assert log.warnings == [
        (
            "Pass output persist failed pass_kind={pass_kind} error_type={error_type} error={error}",
            {
                "pass_kind": "trend_synthesis",
                "error_type": "RuntimeError",
                "error": "SIMULATED PASS OUTPUT FAILURE",
            },
        )
    ]


def test_persist_pass_output_envelope_returns_id_and_records_success_metric() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    envelope = PassOutputEnvelope(
        pass_kind="trend_ideas",
        status=PassStatus.SUCCEEDED,
        run_id="run-pass-runner-success",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
    )
    repository = _FakeRepository(row_id=9)

    persisted_id = persist_pass_output_envelope(
        repository=repository,
        record_metric=_record_metric,
        spec=PassPersistSpec(
            envelope=envelope,
            period_start=datetime(2026, 3, 2, tzinfo=UTC),
            period_end=datetime(2026, 3, 3, tzinfo=UTC),
            log=_FakeLog(),
            failure_message="unused",
            persisted_metric_name="pipeline.trends.pass.ideas.persisted_total",
        ),
    )

    assert persisted_id == 9
    assert repository.calls and repository.calls[0]["pass_kind"] == "trend_ideas"
    assert recorded_metrics == [
        ("pipeline.trends.pass.ideas.persisted_total", 1, "count")
    ]


def test_run_pass_definition_persists_then_runs_projection_specs() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    envelope = PassOutputEnvelope(
        pass_kind="trend_ideas",
        status=PassStatus.SUCCEEDED,
        run_id="run-pass-definition",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
    )
    repository = _FakeRepository(row_id=17)

    def _build_markdown_projection(
        pass_output_id: int | None,
        state: _ProjectionState | None,
    ) -> list[ProjectionSpec]:
        if state is None:
            raise RuntimeError("projection state is required")
        return [
            ProjectionSpec(
                name="markdown",
                enabled=True,
                metric_base="pipeline.trends.projection.ideas_markdown",
                log=_FakeLog(),
                failure_message="unused",
                execute=lambda: f"ideas-{pass_output_id}-{state['pass_output_id']}",
            )
        ]

    result = run_pass_definition(
        repository=repository,
        record_metric=_record_metric,
        definition=PassDefinition[_ProjectionState](
            persist=PassPersistSpec(
                envelope=envelope,
                period_start=datetime(2026, 3, 2, tzinfo=UTC),
                period_end=datetime(2026, 3, 3, tzinfo=UTC),
                log=_FakeLog(),
                failure_message="unused",
                persisted_metric_name="pipeline.trends.pass.ideas.persisted_total",
            ),
            prepare_projection_state=lambda pass_output_id: {
                "pass_output_id": pass_output_id
            },
            build_projection_specs=_build_markdown_projection,
        ),
    )

    assert isinstance(result, PassExecutionResult)
    assert result.pass_output_id == 17
    assert result.projection_state == {"pass_output_id": 17}
    assert result.projection_results == {"markdown": "ideas-17-17"}
    assert recorded_metrics == [
        ("pipeline.trends.pass.ideas.persisted_total", 1, "count"),
        ("pipeline.trends.projection.ideas_markdown.emitted_total", 1, "count"),
    ]


def test_run_pass_definition_skips_projection_by_default_when_persist_fails() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []
    prepared_ids: list[int | None] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    envelope = PassOutputEnvelope(
        pass_kind="trend_synthesis",
        status=PassStatus.SUCCEEDED,
        run_id="run-pass-definition-failure",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
    )

    def _build_markdown_projection(
        pass_output_id: int | None,
        _state: _ProjectionState | None,
    ) -> list[ProjectionSpec]:
        return [
            ProjectionSpec(
                name="markdown",
                enabled=True,
                metric_base="pipeline.trends.projection.trend_markdown",
                log=_FakeLog(),
                failure_message="unused",
                execute=lambda: pass_output_id,
            )
        ]

    result = run_pass_definition(
        repository=_FakeRepository(should_fail=True),
        record_metric=_record_metric,
        definition=PassDefinition[_ProjectionState](
            persist=PassPersistSpec(
                envelope=envelope,
                period_start=datetime(2026, 3, 2, tzinfo=UTC),
                period_end=datetime(2026, 3, 3, tzinfo=UTC),
                log=_FakeLog(),
                failure_message="unused",
                reraise=False,
            ),
            prepare_projection_state=lambda pass_output_id: (
                prepared_ids.append(pass_output_id)
                or {"pass_output_id": pass_output_id}
            ),
            build_projection_specs=_build_markdown_projection,
        ),
    )

    assert result.pass_output_id is None
    assert result.projection_state == {"pass_output_id": None}
    assert result.projection_results == {}
    assert prepared_ids == [None]
    assert recorded_metrics == [
        ("pipeline.trends.pass_outputs.persist_failed_total", 1, "count")
    ]


def test_run_pass_definition_can_project_without_pass_output_when_enabled() -> None:
    recorded_metrics: list[tuple[str, float, str | None]] = []

    def _record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        recorded_metrics.append((name, value, unit))

    envelope = PassOutputEnvelope(
        pass_kind="trend_synthesis",
        status=PassStatus.SUCCEEDED,
        run_id="run-pass-definition-nonfatal",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
    )

    def _build_markdown_projection(
        pass_output_id: int | None,
        _state: None,
    ) -> list[ProjectionSpec]:
        return [
            ProjectionSpec(
                name="markdown",
                enabled=True,
                metric_base="pipeline.trends.projection.trend_markdown",
                log=_FakeLog(),
                failure_message="unused",
                execute=lambda: f"trend-{pass_output_id}",
            )
        ]

    result = run_pass_definition(
        repository=_FakeRepository(should_fail=True),
        record_metric=_record_metric,
        definition=PassDefinition[None](
            persist=PassPersistSpec(
                envelope=envelope,
                period_start=datetime(2026, 3, 2, tzinfo=UTC),
                period_end=datetime(2026, 3, 3, tzinfo=UTC),
                log=_FakeLog(),
                failure_message="unused",
                reraise=False,
            ),
            build_projection_specs=_build_markdown_projection,
            allow_projection_without_pass_output=True,
        ),
    )

    assert result.pass_output_id is None
    assert result.projection_results == {"markdown": "trend-None"}
    assert recorded_metrics == [
        ("pipeline.trends.pass_outputs.persist_failed_total", 1, "count"),
        ("pipeline.trends.projection.trend_markdown.emitted_total", 1, "count"),
    ]
