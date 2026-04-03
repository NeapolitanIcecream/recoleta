from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import time
from typing import Any, cast


@dataclass(frozen=True, slots=True)
class PrepareTaskRequest:
    repository: Any
    settings: Any
    candidate: Any
    target: Any
    context_assist: str
    force: bool
    run_id: str | None


@dataclass(frozen=True, slots=True)
class PrepareTaskDeps:
    payload_hash_fn: Any
    candidate_context_fn: Any
    task_factory: Any


@dataclass(frozen=True, slots=True)
class ExecuteTaskRequest:
    task: Any
    llm_model: str
    source_language_code: str
    source_language_label: str
    llm_connection: Any


@dataclass(frozen=True, slots=True)
class ExecuteTaskDeps:
    translate_structured_payload_fn: Any
    completed_task_factory: Any


@dataclass(frozen=True, slots=True)
class PersistTaskRequest:
    repository: Any
    task: Any
    completed: Any
    context_assist: str
    source_language_code: str
    run_id: str | None


@dataclass(frozen=True, slots=True)
class PersistTaskDeps:
    record_translation_llm_metrics_fn: Any


@dataclass(frozen=True, slots=True)
class TranslateCandidateRequest:
    repository: Any
    settings: Any
    candidate: Any
    target: Any
    llm_model: str
    source_language_code: str
    source_language_label: str
    context_assist: str
    llm_connection: Any
    force: bool
    run_id: str | None


@dataclass(frozen=True, slots=True)
class TranslateCandidateDeps:
    prepare_task_fn: Any
    execute_task_fn: Any
    persist_task_fn: Any


@dataclass(slots=True)
class TranslationBatchContext:
    repository: Any
    settings: Any
    result: Any
    provider_failures: Any
    log: Any
    force: bool
    run_id: str | None
    context_assist: str
    llm_model: str
    source_language_code: str
    source_language_label: str
    llm_connection: Any


@dataclass(frozen=True, slots=True)
class TranslationBatchDeps:
    prepare_task_fn: Any
    execute_task_fn: Any
    persist_task_fn: Any
    parallelism_fn: Any
    executor_class: Any


@dataclass(frozen=True, slots=True)
class ParallelExecutionRequest:
    context: Any
    prepared_tasks: list[Any]
    parallelism: int
    execute_task_fn: Any
    persist_task_fn: Any
    executor_class: Any


@dataclass(slots=True)
class TranslationBackfillContext(TranslationBatchContext):
    translation_target: Any
    emit_mirror_targets: bool


@dataclass(frozen=True, slots=True)
class TranslationBackfillDeps:
    mirror_language_codes_by_candidate: Any
    translate_candidate_fn: Any
    mirror_candidate_fn: Any


@dataclass(frozen=True, slots=True)
class FailureLogRequest:
    log: Any
    candidate: Any
    language_code: str
    exc: Exception
    prefix: str
    field_name: str


def translation_parallelism(task_total: int, *, default_parallelism: int) -> int:
    if task_total <= 1:
        return 1
    return max(1, min(default_parallelism, int(task_total)))


def prepare_translation_task(
    request: PrepareTaskRequest,
    deps: PrepareTaskDeps,
) -> tuple[str, Any | None]:
    source_hash = deps.payload_hash_fn(request.candidate.payload)
    if _has_up_to_date_localized_output(
        repository=request.repository,
        candidate=request.candidate,
        language_code=request.target.code,
        source_hash=source_hash,
        force=request.force,
    ):
        return "skipped", None
    context = deps.candidate_context_fn(
        repository=request.repository,
        settings=request.settings,
        candidate=request.candidate,
        context_assist=request.context_assist,
        run_id=request.run_id,
    )
    return "pending", deps.task_factory(
        candidate=request.candidate,
        target=request.target,
        source_hash=source_hash,
        context=context,
    )


def execute_prepared_translation_task(
    request: ExecuteTaskRequest,
    deps: ExecuteTaskDeps,
) -> Any:
    started = time.perf_counter()
    translated_result = deps.translate_structured_payload_fn(
        model=request.llm_model,
        source_kind=request.task.candidate.source_kind,
        payload=request.task.candidate.payload,
        source_language_code=request.source_language_code,
        target_language_code=request.task.target.code,
        source_language_label=request.source_language_label,
        target_language_label=request.task.target.llm_label,
        context=request.task.context,
        payload_model=request.task.candidate.payload_model,
        llm_connection=request.llm_connection,
        return_debug=True,
    )
    translated_payload, debug = _split_translated_result(translated_result)
    return deps.completed_task_factory(
        translated_payload=translated_payload,
        debug=debug,
        duration_ms=int((time.perf_counter() - started) * 1000),
    )


def persist_completed_translation_task(
    request: PersistTaskRequest,
    deps: PersistTaskDeps,
) -> None:
    if str(request.run_id or "").strip():
        deps.record_translation_llm_metrics_fn(
            repository=request.repository,
            run_id=str(request.run_id),
            debug=request.completed.debug,
            duration_ms=request.completed.duration_ms,
        )
    request.repository.upsert_localized_output(
        source_kind=request.task.candidate.source_kind,
        source_record_id=request.task.candidate.source_record_id,
        language_code=request.task.target.code,
        status="succeeded",
        source_hash=request.task.source_hash,
        payload=request.completed.translated_payload,
        diagnostics={
            "context_assist": request.context_assist,
            "source_language_code": request.source_language_code,
            "target_language_code": request.task.target.code,
            "translated_at": datetime.now(tz=UTC).isoformat(),
            "context_keys": sorted(request.task.context.keys()),
            "hybrid_status": request.task.context.get("hybrid_status"),
            "hybrid_query": request.task.context.get("hybrid_query"),
        },
        variant_role="translation",
    )


def translate_candidate_into_language(
    request: TranslateCandidateRequest,
    deps: TranslateCandidateDeps,
) -> tuple[str, bool]:
    status, prepared = deps.prepare_task_fn(
        repository=request.repository,
        settings=request.settings,
        candidate=request.candidate,
        target=request.target,
        context_assist=request.context_assist,
        force=request.force,
        run_id=request.run_id,
    )
    if status == "skipped" or prepared is None:
        return "skipped", False
    completed = deps.execute_task_fn(
        task=prepared,
        llm_model=request.llm_model,
        source_language_code=request.source_language_code,
        source_language_label=request.source_language_label,
        llm_connection=request.llm_connection,
    )
    deps.persist_task_fn(
        repository=request.repository,
        task=prepared,
        completed=completed,
        context_assist=request.context_assist,
        source_language_code=request.source_language_code,
        run_id=request.run_id,
    )
    return "translated", True


def run_translation_batch(
    context: TranslationBatchContext,
    *,
    candidates: list[Any],
    targets: list[Any],
    deps: TranslationBatchDeps,
) -> Any:
    prepared_tasks = _prepare_batch_tasks(
        context=context,
        candidates=candidates,
        targets=targets,
        prepare_task_fn=deps.prepare_task_fn,
    )
    if prepared_tasks is None:
        return context.result
    parallelism = deps.parallelism_fn(len(prepared_tasks))
    if parallelism <= 1:
        return _run_prepared_tasks_serially(
            context=context,
            prepared_tasks=prepared_tasks,
            execute_task_fn=deps.execute_task_fn,
            persist_task_fn=deps.persist_task_fn,
        )
    return _run_prepared_tasks_in_parallel(
        ParallelExecutionRequest(
            context=context,
            prepared_tasks=prepared_tasks,
            parallelism=parallelism,
            execute_task_fn=deps.execute_task_fn,
            persist_task_fn=deps.persist_task_fn,
            executor_class=deps.executor_class,
        )
    )


def run_translation_backfill_batch(
    context: TranslationBackfillContext,
    *,
    candidates: list[Any],
    deps: TranslationBackfillDeps,
) -> Any:
    for candidate in candidates:
        context.result.scanned_total += 1
        if _run_backfill_translation(
            context=context,
            candidate=candidate,
            translate_candidate_fn=deps.translate_candidate_fn,
        ):
            return context.result
        _run_backfill_mirrors(
            context=context,
            candidate=candidate,
            mirror_language_codes_by_candidate=deps.mirror_language_codes_by_candidate,
            mirror_candidate_fn=deps.mirror_candidate_fn,
        )
    return context.result


def _prepare_batch_tasks(
    *,
    context: TranslationBatchContext,
    candidates: list[Any],
    targets: list[Any],
    prepare_task_fn: Any,
) -> list[Any] | None:
    prepared_tasks: list[Any] = []
    for candidate in candidates:
        for target in targets:
            context.result.scanned_total += 1
            try:
                status, prepared = prepare_task_fn(
                    repository=context.repository,
                    settings=context.settings,
                    candidate=candidate,
                    target=target,
                    context_assist=context.context_assist,
                    force=context.force,
                    run_id=context.run_id,
                )
            except Exception as exc:  # noqa: BLE001
                if _handle_translation_failure(
                    context=context,
                    candidate=candidate,
                    language_code=target.code,
                    exc=exc,
                ):
                    return None
                continue
            if status == "skipped":
                context.result.skipped_total += 1
                context.provider_failures.reset()
                continue
            if prepared is not None:
                prepared_tasks.append(prepared)
    return prepared_tasks


def _run_prepared_tasks_serially(
    *,
    context: TranslationBatchContext,
    prepared_tasks: list[Any],
    execute_task_fn: Any,
    persist_task_fn: Any,
) -> Any:
    for task in prepared_tasks:
        completed = _complete_prepared_task(
            context=context,
            task=task,
            execute_task_fn=execute_task_fn,
        )
        if completed is None:
            if context.result.aborted:
                return context.result
            continue
        _persist_completed_task(
            context=context,
            task=task,
            completed=completed,
            persist_task_fn=persist_task_fn,
        )
    return context.result


def _run_prepared_tasks_in_parallel(request: ParallelExecutionRequest) -> Any:
    with request.executor_class(max_workers=request.parallelism) as executor:
        in_flight: list[tuple[Any, Any]] = []
        next_task_index = 0
        while (
            next_task_index < len(request.prepared_tasks)
            and len(in_flight) < request.parallelism
        ):
            next_task_index = _submit_task(
                request=request,
                executor=executor,
                in_flight=in_flight,
                next_task_index=next_task_index,
            )
        while in_flight:
            task, future = in_flight.pop(0)
            try:
                completed = future.result()
            except Exception as exc:  # noqa: BLE001
                if _handle_translation_failure(
                    context=request.context,
                    candidate=task.candidate,
                    language_code=task.target.code,
                    exc=exc,
                ):
                    return request.context.result
            else:
                _persist_completed_task(
                    context=request.context,
                    task=task,
                    completed=completed,
                    persist_task_fn=request.persist_task_fn,
                )
            if next_task_index < len(request.prepared_tasks):
                next_task_index = _submit_task(
                    request=request,
                    executor=executor,
                    in_flight=in_flight,
                    next_task_index=next_task_index,
                )
    return request.context.result


def _submit_task(
    *,
    request: ParallelExecutionRequest,
    executor: Any,
    in_flight: list[tuple[Any, Any]],
    next_task_index: int,
) -> int:
    task = request.prepared_tasks[next_task_index]
    future = executor.submit(
        request.execute_task_fn,
        task=task,
        llm_model=request.context.llm_model,
        source_language_code=request.context.source_language_code,
        source_language_label=request.context.source_language_label,
        llm_connection=request.context.llm_connection,
    )
    in_flight.append((task, future))
    return next_task_index + 1


def _complete_prepared_task(
    *,
    context: TranslationBatchContext,
    task: Any,
    execute_task_fn: Any,
) -> Any | None:
    try:
        return execute_task_fn(
            task=task,
            llm_model=context.llm_model,
            source_language_code=context.source_language_code,
            source_language_label=context.source_language_label,
            llm_connection=context.llm_connection,
        )
    except Exception as exc:  # noqa: BLE001
        _handle_translation_failure(
            context=context,
            candidate=task.candidate,
            language_code=task.target.code,
            exc=exc,
        )
        return None


def _persist_completed_task(
    *,
    context: TranslationBatchContext,
    task: Any,
    completed: Any,
    persist_task_fn: Any,
) -> None:
    context.provider_failures.reset()
    persist_task_fn(
        repository=context.repository,
        task=task,
        completed=completed,
        context_assist=context.context_assist,
        source_language_code=context.source_language_code,
        run_id=context.run_id,
    )
    context.result.translated_total += 1


def _run_backfill_translation(
    *,
    context: TranslationBackfillContext,
    candidate: Any,
    translate_candidate_fn: Any,
) -> bool:
    try:
        status, changed = translate_candidate_fn(
            repository=context.repository,
            settings=context.settings,
            candidate=candidate,
            target=context.translation_target,
            llm_model=context.llm_model,
            source_language_code=context.source_language_code,
            source_language_label=context.source_language_label,
            context_assist=context.context_assist,
            llm_connection=context.llm_connection,
            force=context.force,
            run_id=context.run_id,
        )
    except Exception as exc:  # noqa: BLE001
        return _handle_translation_failure(
            context=context,
            candidate=candidate,
            language_code=context.translation_target.code,
            exc=exc,
            prefix="backfill translation failed",
        )
    context.provider_failures.reset()
    if status == "skipped":
        context.result.skipped_total += 1
    elif changed:
        context.result.translated_total += 1
    return False


def _run_backfill_mirrors(
    *,
    context: TranslationBackfillContext,
    candidate: Any,
    mirror_language_codes_by_candidate: Any,
    mirror_candidate_fn: Any,
) -> None:
    if not context.emit_mirror_targets:
        return
    for language_code in sorted(mirror_language_codes_by_candidate(candidate)):
        try:
            status, changed = mirror_candidate_fn(
                repository=context.repository,
                candidate=candidate,
                language_code=language_code,
                force=context.force,
            )
        except Exception as exc:  # noqa: BLE001
            _log_failure(
                FailureLogRequest(
                    log=context.log,
                    candidate=candidate,
                    language_code=language_code,
                    exc=exc,
                    prefix="backfill mirror failed",
                    field_name="mirror_language_code",
                )
            )
            context.result.failed_total += 1
            continue
        if status == "skipped":
            context.result.skipped_total += 1
        elif changed:
            context.result.mirrored_total += 1


def _handle_translation_failure(
    *,
    context: TranslationBatchContext,
    candidate: Any,
    language_code: str,
    exc: Exception,
    prefix: str = "translation failed",
) -> bool:
    context.result.failed_total += 1
    _log_failure(
        FailureLogRequest(
            log=context.log,
            candidate=candidate,
            language_code=language_code,
            exc=exc,
            prefix=prefix,
            field_name="target_language_code",
        )
    )
    abort_reason = context.provider_failures.record(exc)
    if abort_reason is None:
        return False
    context.result.aborted = True
    context.result.abort_reason = abort_reason
    context.log.warning(abort_reason)
    return True


def _log_failure(request: FailureLogRequest) -> None:
    request.log.bind(
        source_kind=request.candidate.source_kind,
        source_record_id=request.candidate.source_record_id,
        **{request.field_name: request.language_code},
    ).warning(
        f"{request.prefix} error_type={{}} error={{}}",
        type(request.exc).__name__,
        str(request.exc),
    )


def _has_up_to_date_localized_output(
    *,
    repository: Any,
    candidate: Any,
    language_code: str,
    source_hash: str,
    force: bool,
) -> bool:
    existing = repository.get_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=language_code,
    )
    return (
        existing is not None
        and str(getattr(existing, "source_hash", "") or "") == source_hash
        and not force
    )


def _split_translated_result(
    translated_result: Any,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if (
        isinstance(translated_result, tuple)
        and len(translated_result) == 2
        and isinstance(translated_result[0], dict)
        and isinstance(translated_result[1], dict)
    ):
        return cast(tuple[dict[str, Any], dict[str, Any]], translated_result)
    if not isinstance(translated_result, dict):
        raise ValueError("translated payload must be a JSON object")
    return translated_result, {}
