from __future__ import annotations

from datetime import UTC, datetime

from recoleta.passes.base import PassOutputEnvelope, PassStatus
from recoleta.pipeline.pass_runner import (
    ProjectionSpec,
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
        envelope=envelope,
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        record_metric=_record_metric,
        log=log,
        failure_message=(
            "Pass output persist failed pass_kind={pass_kind} "
            "error_type={error_type} error={error}"
        ),
        sanitize_error=lambda message: message.upper(),
        on_failure=lambda exc: captured_failures.append(type(exc).__name__),
        reraise=False,
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
        envelope=envelope,
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        record_metric=_record_metric,
        log=_FakeLog(),
        failure_message="unused",
        persisted_metric_name="pipeline.trends.pass.ideas.persisted_total",
    )

    assert persisted_id == 9
    assert repository.calls and repository.calls[0]["pass_kind"] == "trend_ideas"
    assert recorded_metrics == [
        ("pipeline.trends.pass.ideas.persisted_total", 1, "count")
    ]
