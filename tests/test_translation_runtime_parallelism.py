from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import time
from types import SimpleNamespace

import recoleta.translation as translation_module
import recoleta.translation_runtime as translation_runtime


class _FakeRepository:
    def __init__(self) -> None:
        self.metrics: list[SimpleNamespace] = []

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


class _FakeProviderFailures:
    def reset(self) -> None:
        return None


def _batch_context(*, repository: _FakeRepository) -> translation_runtime.TranslationBatchContext:
    return translation_runtime.TranslationBatchContext(
        repository=repository,
        settings=SimpleNamespace(),
        result=SimpleNamespace(
            translated_total=0,
            scanned_total=0,
            skipped_total=0,
            failed_total=0,
            aborted=False,
            abort_reason=None,
        ),
        provider_failures=_FakeProviderFailures(),
        log=SimpleNamespace(),
        force=False,
        run_id="run-translation",
        context_assist="direct",
        llm_model="test/model",
        source_language_code="en",
        source_language_label="English",
        llm_connection=None,
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
