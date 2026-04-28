from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from functools import partial
import time
from types import SimpleNamespace

import recoleta.translation as translation_module
import recoleta.translation_runtime as translation_runtime


class _FakeRepository:
    def __init__(self) -> None:
        self.metrics: list[SimpleNamespace] = []
        self.localized_outputs: dict[tuple[str, int, str], SimpleNamespace] = {}

    def record_metric(
        self,
        *,
        run_id: str,
        name: str,
        value: float,
        unit: str | None = None,
    ) -> None:
        self.metrics.append(
            SimpleNamespace(run_id=run_id, name=name, value=value, unit=unit)
        )

    def get_localized_output(
        self,
        *,
        source_kind: str,
        source_record_id: int,
        language_code: str,
    ) -> SimpleNamespace | None:
        return self.localized_outputs.get(
            (source_kind, source_record_id, language_code)
        )


class _FakeProviderFailures:
    def record(self, exc: Exception) -> str | None:
        _ = exc
        return None

    def reset(self) -> None:
        return None


class _AbortingProviderFailures(_FakeProviderFailures):
    def record(self, exc: Exception) -> str | None:
        _ = exc
        return "abort requested"


class _ResetSensitiveProviderFailures(_FakeProviderFailures):
    def __init__(self) -> None:
        self.abort_armed = True

    def record(self, exc: Exception) -> str | None:
        _ = exc
        return "abort requested" if self.abort_armed else None

    def reset(self) -> None:
        self.abort_armed = False


class _FakeLog:
    def bind(self, **kwargs) -> _FakeLog:
        _ = kwargs
        return self

    def warning(self, *args, **kwargs) -> None:
        _ = (args, kwargs)


class _FakeFuture:
    def __init__(self, *, value: object | None = None, exc: Exception | None = None) -> None:
        self._value = value
        self._exc = exc

    def result(self) -> object | None:
        if self._exc is not None:
            raise self._exc
        return self._value


class _FakeExecutor:
    def __init__(
        self,
        futures: list[_FakeFuture],
        *,
        max_workers: int | None = None,
    ) -> None:
        self._futures = list(futures)
        self._max_workers = max_workers

    def __enter__(self) -> _FakeExecutor:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        _ = (exc_type, exc, tb)

    def submit(self, fn, **kwargs) -> _FakeFuture:  # type: ignore[no-untyped-def]
        _ = (fn, kwargs)
        return self._futures.pop(0)


def _batch_context(
    *,
    repository: _FakeRepository,
    provider_failures: _FakeProviderFailures | None = None,
) -> translation_runtime.TranslationBatchContext:
    return translation_runtime.TranslationBatchContext(
        repository=repository,
        settings=SimpleNamespace(translation_llm_max_attempts=5),
        result=SimpleNamespace(
            translated_total=0,
            mirrored_total=0,
            scanned_total=0,
            skipped_total=0,
            failed_total=0,
            aborted=False,
            abort_reason=None,
        ),
        provider_failures=provider_failures or _FakeProviderFailures(),
        log=_FakeLog(),
        force=False,
        run_id="run-translation",
        context_assist="direct",
        llm_model="test/model",
        source_language_code="en",
        source_language_label="English",
        llm_connection=None,
        llm_max_attempts=5,
    )


def test_translation_parallelism_uses_settings_cap() -> None:
    settings = SimpleNamespace(translation_parallelism=12)

    assert translation_module._translation_parallelism(1, settings=settings) == 1
    assert translation_module._translation_parallelism(6, settings=settings) == 6
    assert translation_module._translation_parallelism(100, settings=settings) == 12


def test_parallel_translation_batch_processes_completed_tasks_without_submission_head_of_line_blocking() -> None:
    repository = _FakeRepository()
    context = _batch_context(repository=repository)
    persisted_order: list[str] = []
    prepared_tasks = [
        SimpleNamespace(
            name="slow",
            delay_s=0.15,
            candidate=SimpleNamespace(source_kind="analysis"),
            target=SimpleNamespace(code="zh-CN"),
        ),
        SimpleNamespace(
            name="fast",
            delay_s=0.01,
            candidate=SimpleNamespace(source_kind="analysis"),
            target=SimpleNamespace(code="zh-CN"),
        ),
        SimpleNamespace(
            name="next",
            delay_s=0.01,
            candidate=SimpleNamespace(source_kind="analysis"),
            target=SimpleNamespace(code="zh-CN"),
        ),
    ]

    def _execute_task(**kwargs):  # type: ignore[no-untyped-def]
        task = kwargs["task"]
        time.sleep(task.delay_s)
        return SimpleNamespace(name=task.name)

    def _persist_task(**kwargs):  # type: ignore[no-untyped-def]
        persisted_order.append(kwargs["task"].name)

    translation_runtime._run_prepared_tasks_in_parallel(
        translation_runtime.ParallelExecutionRequest(
            context=context,
            prepared_tasks=prepared_tasks,
            parallelism=2,
            execute_task_fn=_execute_task,
            persist_task_fn=_persist_task,
            executor_class=ThreadPoolExecutor,
        )
    )

    assert persisted_order[0] == "fast"
    assert set(persisted_order) == {"slow", "fast", "next"}
    assert context.result.translated_total == 3


def test_parallel_translation_batch_persists_successes_completed_in_same_aborting_drain(
    monkeypatch,
) -> None:
    """Regression: a sibling success in the same wait() drain must survive an aborting failure."""
    repository = _FakeRepository()
    context = _batch_context(
        repository=repository,
        provider_failures=_AbortingProviderFailures(),
    )
    persisted_order: list[str] = []
    failure_future = _FakeFuture(exc=RuntimeError("provider unavailable"))
    success_future = _FakeFuture(value=SimpleNamespace(name="translated"))
    prepared_tasks = [
        SimpleNamespace(
            name="failure",
            candidate=SimpleNamespace(source_kind="analysis", source_record_id="failure"),
            target=SimpleNamespace(code="zh-CN"),
        ),
        SimpleNamespace(
            name="success",
            candidate=SimpleNamespace(source_kind="analysis", source_record_id="success"),
            target=SimpleNamespace(code="zh-CN"),
        ),
    ]

    def _wait(futures, return_when):  # type: ignore[no-untyped-def]
        assert return_when == translation_runtime.FIRST_COMPLETED
        assert set(futures) == {failure_future, success_future}
        return [failure_future, success_future], ()

    def _persist_task(**kwargs):  # type: ignore[no-untyped-def]
        persisted_order.append(kwargs["task"].name)

    monkeypatch.setattr(translation_runtime, "wait", _wait)

    translation_runtime._run_prepared_tasks_in_parallel(
        translation_runtime.ParallelExecutionRequest(
            context=context,
            prepared_tasks=prepared_tasks,
            parallelism=2,
            execute_task_fn=lambda **kwargs: None,
            persist_task_fn=_persist_task,
            executor_class=partial(_FakeExecutor, [failure_future, success_future]),
        )
    )

    assert persisted_order == ["success"]
    assert context.result.translated_total == 1
    assert context.result.failed_total == 1
    assert context.result.aborted is True
    assert context.result.abort_reason == "abort requested"


def test_parallel_translation_batch_uses_deterministic_abort_policy_with_same_done_batch(
    monkeypatch,
) -> None:
    def _run_with_done_order(done_order: tuple[str, str]) -> tuple[bool, int]:
        repository = _FakeRepository()
        context = _batch_context(
            repository=repository,
            provider_failures=_ResetSensitiveProviderFailures(),
        )
        failure_future = _FakeFuture(exc=RuntimeError("provider unavailable"))
        success_future = _FakeFuture(value=SimpleNamespace(name="translated"))
        prepared_tasks = [
            SimpleNamespace(
                name="failure",
                candidate=SimpleNamespace(
                    source_kind="analysis",
                    source_record_id="failure",
                ),
                target=SimpleNamespace(code="zh-CN"),
            ),
            SimpleNamespace(
                name="success",
                candidate=SimpleNamespace(
                    source_kind="analysis",
                    source_record_id="success",
                ),
                target=SimpleNamespace(code="zh-CN"),
            ),
        ]
        future_by_name = {
            "failure": failure_future,
            "success": success_future,
        }

        def _wait(futures, return_when):  # type: ignore[no-untyped-def]
            assert return_when == translation_runtime.FIRST_COMPLETED
            assert set(futures) == {failure_future, success_future}
            return [future_by_name[name] for name in done_order], ()

        monkeypatch.setattr(translation_runtime, "wait", _wait)
        translation_runtime._run_prepared_tasks_in_parallel(
            translation_runtime.ParallelExecutionRequest(
                context=context,
                prepared_tasks=prepared_tasks,
                parallelism=2,
                execute_task_fn=lambda **kwargs: None,
                persist_task_fn=lambda **kwargs: None,
                executor_class=partial(
                    _FakeExecutor,
                    [failure_future, success_future],
                ),
            )
        )
        return context.result.aborted, context.result.translated_total

    first_result = _run_with_done_order(("failure", "success"))
    second_result = _run_with_done_order(("success", "failure"))

    assert first_result == second_result == (True, 1)


def test_run_translation_batch_records_batch_parallelism_metrics() -> None:
    repository = _FakeRepository()
    context = _batch_context(repository=repository)

    def _prepare_task(**kwargs):  # type: ignore[no-untyped-def]
        candidate = kwargs["candidate"]
        target = kwargs["target"]
        task = SimpleNamespace(
            candidate=candidate,
            target=target,
            delay_s=0.0,
        )
        return "pending", task

    def _execute_task(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return SimpleNamespace()

    def _persist_task(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs

    result = translation_runtime.run_translation_batch(
        context,
        candidates=[SimpleNamespace(source_kind="analysis")],
        targets=[SimpleNamespace(code="zh-CN")],
        deps=translation_runtime.TranslationBatchDeps(
            prepare_task_fn=_prepare_task,
            execute_task_fn=_execute_task,
            persist_task_fn=_persist_task,
            parallelism_fn=lambda task_total: 3 if task_total else 0,
            executor_class=ThreadPoolExecutor,
        ),
    )

    metric_names = [metric.name for metric in repository.metrics]
    assert result.translated_total == 1
    assert "pipeline.translate.batch.prepare.duration_ms" in metric_names
    assert "pipeline.translate.batch.prepared_tasks_total" in metric_names
    assert "pipeline.translate.parallelism.effective" in metric_names
    assert "pipeline.translate.llm_max_attempts" in metric_names


def test_run_translation_batch_records_result_totals() -> None:
    repository = _FakeRepository()
    context = _batch_context(repository=repository)

    def _prepare_task(**kwargs):  # type: ignore[no-untyped-def]
        candidate = kwargs["candidate"]
        if getattr(candidate, "source_record_id", None) == 1:
            return "skipped", None
        return "pending", SimpleNamespace(
            candidate=candidate,
            target=kwargs["target"],
        )

    result = translation_runtime.run_translation_batch(
        context,
        candidates=[
            SimpleNamespace(source_kind="analysis", source_record_id=1),
            SimpleNamespace(source_kind="analysis", source_record_id=2),
        ],
        targets=[SimpleNamespace(code="zh-CN")],
        deps=translation_runtime.TranslationBatchDeps(
            prepare_task_fn=_prepare_task,
            execute_task_fn=lambda **kwargs: SimpleNamespace(),
            persist_task_fn=lambda **kwargs: None,
            parallelism_fn=lambda task_total: 1 if task_total else 0,
            executor_class=ThreadPoolExecutor,
        ),
    )

    metric_values = {metric.name: metric.value for metric in repository.metrics}
    assert result.scanned_total == 2
    assert result.translated_total == 1
    assert result.mirrored_total == 0
    assert result.skipped_total == 1
    assert metric_values["pipeline.translate.scanned_total"] == 2
    assert metric_values["pipeline.translate.translated_total"] == 1
    assert metric_values["pipeline.translate.mirrored_total"] == 0
    assert metric_values["pipeline.translate.skipped_total"] == 1
    assert metric_values["pipeline.translate.llm_max_attempts"] == 5


def test_prepare_translation_task_records_up_to_date_source_hash_skip_reason() -> None:
    repository = _FakeRepository()
    repository.localized_outputs[("analysis", 42, "zh-CN")] = SimpleNamespace(
        source_hash="same-hash"
    )
    status, prepared = translation_runtime.prepare_translation_task(
        translation_runtime.PrepareTaskRequest(
            repository=repository,
            settings=SimpleNamespace(),
            candidate=SimpleNamespace(
                source_kind="analysis",
                source_record_id=42,
                payload={"title": "same payload"},
            ),
            target=SimpleNamespace(code="zh-CN"),
            context_assist="direct",
            force=False,
            run_id="run-translation",
        ),
        translation_runtime.PrepareTaskDeps(
            payload_hash_fn=lambda _payload: "same-hash",
            candidate_context_fn=lambda **kwargs: {"unused": kwargs},
            task_factory=lambda **kwargs: kwargs,
        ),
    )

    metric_values = {metric.name: metric.value for metric in repository.metrics}
    assert status == "skipped"
    assert prepared is None
    assert (
        metric_values["pipeline.translate.skipped_total.up_to_date_source_hash"] == 1
    )
