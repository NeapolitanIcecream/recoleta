from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import BaseModel

from recoleta.analyzer import (
    _extract_content,
    _extract_token_counts,
    _extract_usage_dict,
    _get_completion,
    _resolve_response_cost_usd,
)
from recoleta.config import LocalizationConfig, Settings
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.models import Document
from recoleta.storage.common import _to_json
from recoleta.translation_candidates import (
    IncrementalCandidatesRequest,
    incremental_candidates as _candidate_incremental_candidates,
)
from recoleta.translation_context import build_candidate_context as _context_build_candidate_context
from recoleta.translation_llm import (
    TranslationLLMDeps,
    TranslationLLMRequest,
    build_translation_system_message as _llm_build_translation_system_message,
    translate_structured_payload_with_debug as _llm_translate_structured_payload_with_debug,
)
from recoleta.translation_runtime import (
    ExecuteTaskDeps,
    ExecuteTaskRequest,
    PersistTaskDeps,
    PersistTaskRequest,
    PrepareTaskDeps,
    PrepareTaskRequest,
    TranslateCandidateDeps,
    TranslateCandidateRequest,
    TranslationBackfillContext,
    TranslationBackfillDeps,
    TranslationBatchContext,
    TranslationBatchDeps,
    execute_prepared_translation_task as _runtime_execute_prepared_translation_task,
    persist_completed_translation_task as _runtime_persist_completed_translation_task,
    prepare_translation_task as _runtime_prepare_translation_task,
    run_translation_backfill_batch as _runtime_run_translation_backfill_batch,
    run_translation_batch as _runtime_run_translation_batch,
    translate_candidate_into_language as _runtime_translate_candidate_into_language,
    translation_parallelism as _runtime_translation_parallelism,
)
from recoleta.types import sha256_hex

TRANSLATION_CONTEXT_ASSIST_VALUES = {"none", "direct", "hybrid"}
TRANSLATION_INCLUDE_VALUES = {"items", "trends", "ideas"}
_PROVIDER_FAILURE_ERROR_TYPES = {
    "APIConnectionError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ServiceUnavailableError",
    "Timeout",
}
_PROVIDER_FAILURE_ABORT_THRESHOLD = 5
_DEFAULT_TRANSLATION_PARALLELISM = 4


class _AnalysisTranslationPayload(BaseModel):
    summary: str


@dataclass(frozen=True, slots=True)
class TranslationTarget:
    code: str
    llm_label: str


@dataclass(frozen=True, slots=True)
class TranslationCandidate:
    source_kind: str
    source_record_id: int
    payload: dict[str, Any]
    payload_model: type[BaseModel] | None
    canonical_language_code: str | None
    item_id: int | None = None
    document_id: int | None = None
    granularity: str | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(slots=True)
class TranslationRunResult:
    scanned_total: int = 0
    translated_total: int = 0
    mirrored_total: int = 0
    skipped_total: int = 0
    failed_total: int = 0
    aborted: bool = False
    abort_reason: str | None = None


@dataclass(frozen=True, slots=True)
class _PreparedTranslationTask:
    candidate: TranslationCandidate
    target: TranslationTarget
    source_hash: str
    context: dict[str, Any]


@dataclass(frozen=True, slots=True)
class _CompletedTranslationTask:
    translated_payload: dict[str, Any]
    debug: dict[str, Any]
    duration_ms: int


@dataclass(frozen=True, slots=True)
class TranslateStructuredPayloadRequest:
    model: str
    source_kind: str
    payload: dict[str, Any]
    source_language_code: str
    target_language_code: str
    source_language_label: str | None = None
    target_language_label: str | None = None
    context: dict[str, Any] | None = None
    payload_model: type[BaseModel] | None = None
    llm_connection: LLMConnectionConfig | None = None
    return_debug: bool = False


@dataclass(frozen=True, slots=True)
class IncrementalCandidatesCompatRequest:
    repository: Any
    granularity: str | None
    include: set[str]
    limit: int | None
    source_language_code: str
    period_start: datetime | None = None
    period_end: datetime | None = None
    all_history: bool = True


@dataclass(frozen=True, slots=True)
class PrepareTranslationTaskCompatRequest:
    repository: Any
    settings: Settings
    candidate: TranslationCandidate
    target: TranslationTarget
    context_assist: str
    force: bool
    run_id: str | None = None


@dataclass(frozen=True, slots=True)
class PersistTranslationTaskCompatRequest:
    repository: Any
    task: _PreparedTranslationTask
    completed: _CompletedTranslationTask
    context_assist: str
    source_language_code: str
    run_id: str | None = None


@dataclass(frozen=True, slots=True)
class TranslateCandidateCompatRequest:
    repository: Any
    settings: Settings
    candidate: TranslationCandidate
    target: TranslationTarget
    llm_model: str
    source_language_code: str
    source_language_label: str
    context_assist: str
    llm_connection: LLMConnectionConfig
    force: bool
    run_id: str | None = None


@dataclass(frozen=True, slots=True)
class RunTranslationRequest:
    repository: Any
    settings: Settings
    granularity: str | None = None
    include: str | list[str] | None = None
    limit: int | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None
    all_history: bool = True
    force: bool = False
    context_assist: str = "direct"
    run_id: str | None = None


@dataclass(frozen=True, slots=True)
class RunTranslationBackfillRequest:
    repository: Any
    settings: Settings
    granularity: str | None = None
    include: str | list[str] | None = None
    limit: int | None = None
    force: bool = False
    context_assist: str = "direct"
    legacy_source_language: str | None = None
    emit_mirror_targets: bool = False
    all_history: bool = False
    run_id: str | None = None


@dataclass(frozen=True, slots=True)
class _TranslationCandidatesRequest:
    repository: Any
    granularity: str | None
    include: str | list[str] | None
    limit: int | None
    source_language_code: str
    period_start: datetime | None = None
    period_end: datetime | None = None
    all_history: bool = True


@dataclass(frozen=True, slots=True)
class _TranslationBatchContextRequest:
    repository: Any
    settings: Settings
    force: bool
    run_id: str | None
    context_assist: str
    llm_model: str
    source_language_code: str


@dataclass(frozen=True, slots=True)
class _TranslationBackfillContextRequest:
    repository: Any
    settings: Settings
    localization: LocalizationConfig
    force: bool
    run_id: str | None
    context_assist: str
    llm_model: str
    source_language_code: str
    emit_mirror_targets: bool


@dataclass(slots=True)
class _ProviderFailureTracker:
    last_signature: tuple[str, str] | None = None
    consecutive_count: int = 0

    def record(self, exc: Exception) -> str | None:
        signature = _provider_failure_signature(exc)
        if signature is None:
            self.last_signature = None
            self.consecutive_count = 0
            return None
        if signature == self.last_signature:
            self.consecutive_count += 1
        else:
            self.last_signature = signature
            self.consecutive_count = 1
        if self.consecutive_count < _PROVIDER_FAILURE_ABORT_THRESHOLD:
            return None
        error_type, message = signature
        return (
            "aborting after "
            f"{self.consecutive_count} consecutive provider failures "
            f"({error_type}: {message})"
        )

    def reset(self) -> None:
        self.last_signature = None
        self.consecutive_count = 0


def coerce_translate_structured_payload_request(
    *,
    request: TranslateStructuredPayloadRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> TranslateStructuredPayloadRequest:
    if request is not None:
        return request
    return TranslateStructuredPayloadRequest(
        model=legacy_kwargs["model"],
        source_kind=legacy_kwargs["source_kind"],
        payload=legacy_kwargs["payload"],
        source_language_code=legacy_kwargs["source_language_code"],
        target_language_code=legacy_kwargs["target_language_code"],
        source_language_label=legacy_kwargs.get("source_language_label"),
        target_language_label=legacy_kwargs.get("target_language_label"),
        context=legacy_kwargs.get("context"),
        payload_model=legacy_kwargs.get("payload_model"),
        llm_connection=legacy_kwargs.get("llm_connection"),
        return_debug=bool(legacy_kwargs.get("return_debug", False)),
    )


def coerce_incremental_candidates_request(
    *,
    request: IncrementalCandidatesCompatRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> IncrementalCandidatesCompatRequest:
    if request is not None:
        return request
    return IncrementalCandidatesCompatRequest(
        repository=legacy_kwargs["repository"],
        granularity=legacy_kwargs.get("granularity"),
        include=legacy_kwargs["include"],
        limit=legacy_kwargs.get("limit"),
        source_language_code=legacy_kwargs["source_language_code"],
        period_start=legacy_kwargs.get("period_start"),
        period_end=legacy_kwargs.get("period_end"),
        all_history=bool(legacy_kwargs.get("all_history", True)),
    )


def coerce_prepare_translation_task_request(
    *,
    request: PrepareTranslationTaskCompatRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> PrepareTranslationTaskCompatRequest:
    if request is not None:
        return request
    return PrepareTranslationTaskCompatRequest(
        repository=legacy_kwargs["repository"],
        settings=legacy_kwargs["settings"],
        candidate=legacy_kwargs["candidate"],
        target=legacy_kwargs["target"],
        context_assist=legacy_kwargs["context_assist"],
        force=bool(legacy_kwargs["force"]),
        run_id=legacy_kwargs.get("run_id"),
    )


def coerce_persist_translation_task_request(
    *,
    request: PersistTranslationTaskCompatRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> PersistTranslationTaskCompatRequest:
    if request is not None:
        return request
    return PersistTranslationTaskCompatRequest(
        repository=legacy_kwargs["repository"],
        task=legacy_kwargs["task"],
        completed=legacy_kwargs["completed"],
        context_assist=legacy_kwargs["context_assist"],
        source_language_code=legacy_kwargs["source_language_code"],
        run_id=legacy_kwargs.get("run_id"),
    )


def coerce_translate_candidate_request(
    *,
    request: TranslateCandidateCompatRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> TranslateCandidateCompatRequest:
    if request is not None:
        return request
    return TranslateCandidateCompatRequest(
        repository=legacy_kwargs["repository"],
        settings=legacy_kwargs["settings"],
        candidate=legacy_kwargs["candidate"],
        target=legacy_kwargs["target"],
        llm_model=legacy_kwargs["llm_model"],
        source_language_code=legacy_kwargs["source_language_code"],
        source_language_label=legacy_kwargs["source_language_label"],
        context_assist=legacy_kwargs["context_assist"],
        llm_connection=legacy_kwargs["llm_connection"],
        force=bool(legacy_kwargs["force"]),
        run_id=legacy_kwargs.get("run_id"),
    )


def coerce_run_translation_request(
    *,
    request: RunTranslationRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> RunTranslationRequest:
    if request is not None:
        return request
    return RunTranslationRequest(
        repository=legacy_kwargs["repository"],
        settings=legacy_kwargs["settings"],
        granularity=legacy_kwargs.get("granularity"),
        include=legacy_kwargs.get("include"),
        limit=legacy_kwargs.get("limit"),
        period_start=legacy_kwargs.get("period_start"),
        period_end=legacy_kwargs.get("period_end"),
        all_history=bool(legacy_kwargs.get("all_history", True)),
        force=bool(legacy_kwargs.get("force", False)),
        context_assist=str(legacy_kwargs.get("context_assist", "direct")),
        run_id=legacy_kwargs.get("run_id"),
    )


def coerce_run_translation_backfill_request(
    *,
    request: RunTranslationBackfillRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> RunTranslationBackfillRequest:
    if request is not None:
        return request
    return RunTranslationBackfillRequest(
        repository=legacy_kwargs["repository"],
        settings=legacy_kwargs["settings"],
        granularity=legacy_kwargs.get("granularity"),
        include=legacy_kwargs.get("include"),
        limit=legacy_kwargs.get("limit"),
        force=bool(legacy_kwargs.get("force", False)),
        context_assist=str(legacy_kwargs.get("context_assist", "direct")),
        legacy_source_language=legacy_kwargs.get("legacy_source_language"),
        emit_mirror_targets=bool(legacy_kwargs.get("emit_mirror_targets", False)),
        all_history=bool(legacy_kwargs.get("all_history", False)),
        run_id=legacy_kwargs.get("run_id"),
    )


def normalize_context_assist(value: str | None) -> str:
    normalized = str(value or "").strip().lower() or "direct"
    if normalized not in TRANSLATION_CONTEXT_ASSIST_VALUES:
        allowed = ", ".join(sorted(TRANSLATION_CONTEXT_ASSIST_VALUES))
        raise ValueError(f"context_assist must be one of: {allowed}")
    return normalized


def normalize_include(value: str | list[str] | None) -> set[str]:
    if value is None:
        return set(TRANSLATION_INCLUDE_VALUES)
    raw_values = (
        [part.strip().lower() for part in value.split(",")]
        if isinstance(value, str)
        else [str(part).strip().lower() for part in value]
    )
    normalized = {part for part in raw_values if part}
    unknown = sorted(normalized - TRANSLATION_INCLUDE_VALUES)
    if unknown:
        allowed = ", ".join(sorted(TRANSLATION_INCLUDE_VALUES))
        raise ValueError(f"include must only contain: {allowed}")
    return normalized or set(TRANSLATION_INCLUDE_VALUES)


def language_slug(value: str) -> str:
    return str(value or "").strip().lower().replace("_", "-")


def _payload_hash(payload: dict[str, Any]) -> str:
    return sha256_hex(_to_json(payload))


def _provider_failure_signature(exc: Exception) -> tuple[str, str] | None:
    error_type = type(exc).__name__
    if error_type not in _PROVIDER_FAILURE_ERROR_TYPES:
        return None
    message = " ".join(str(exc).strip().split()).lower()
    if not message:
        message = error_type.lower()
    if len(message) > 240:
        message = message[:240]
    return error_type, message


def _build_translation_system_message() -> str:
    return _llm_build_translation_system_message()


def _translation_llm_deps() -> TranslationLLMDeps:
    return TranslationLLMDeps(
        _get_completion,
        _extract_usage_dict,
        _extract_token_counts,
        _extract_content,
        _resolve_response_cost_usd,
    )


def translate_structured_payload(
    *,
    request: TranslateStructuredPayloadRequest | None = None,
    **legacy_kwargs: Any,
) -> dict[str, Any] | tuple[dict[str, Any], dict[str, Any]]:
    normalized_request = coerce_translate_structured_payload_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return _translate_structured_payload_impl(request=normalized_request)


def _translate_structured_payload_impl(
    *,
    request: TranslateStructuredPayloadRequest,
) -> dict[str, Any] | tuple[dict[str, Any], dict[str, Any]]:
    translated = _llm_translate_structured_payload_with_debug(
        TranslationLLMRequest(
            request.model,
            request.source_kind,
            request.payload,
            request.source_language_code,
            request.target_language_code,
            request.source_language_label,
            request.target_language_label,
            request.context,
            request.payload_model,
            request.llm_connection,
        ),
        _translation_llm_deps(),
    )
    return translated if request.return_debug else translated[0]


def _incremental_candidates(
    *,
    request: IncrementalCandidatesCompatRequest | None = None,
    **legacy_kwargs: Any,
) -> list[TranslationCandidate]:
    normalized_request = coerce_incremental_candidates_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return _candidate_incremental_candidates(
        IncrementalCandidatesRequest(
            repository=normalized_request.repository,
            granularity=normalized_request.granularity,
            include=normalized_request.include,
            limit=normalized_request.limit,
            source_language_code=normalized_request.source_language_code,
            candidate_factory=TranslationCandidate,
            analysis_payload_model=_AnalysisTranslationPayload,
            period_start=normalized_request.period_start,
            period_end=normalized_request.period_end,
            all_history=normalized_request.all_history,
        )
    )


def _candidate_context(
    *,
    repository: Any,
    settings: Settings,
    candidate: TranslationCandidate,
    context_assist: str,
    run_id: str | None,
) -> dict[str, Any]:
    return _context_build_candidate_context(
        repository=repository,
        settings=settings,
        candidate=candidate,
        context_assist=context_assist,
        run_id=run_id,
    )


def _translation_parallelism(task_total: int) -> int:
    return _runtime_translation_parallelism(
        task_total,
        default_parallelism=_DEFAULT_TRANSLATION_PARALLELISM,
    )


def _prepare_translation_task(
    *,
    request: PrepareTranslationTaskCompatRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[str, _PreparedTranslationTask | None]:
    normalized_request = coerce_prepare_translation_task_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return _runtime_prepare_translation_task(
        PrepareTaskRequest(
            repository=normalized_request.repository,
            settings=normalized_request.settings,
            candidate=normalized_request.candidate,
            target=normalized_request.target,
            context_assist=normalized_request.context_assist,
            force=normalized_request.force,
            run_id=normalized_request.run_id,
        ),
        PrepareTaskDeps(
            payload_hash_fn=_payload_hash,
            candidate_context_fn=_candidate_context,
            task_factory=_PreparedTranslationTask,
        ),
    )


def _execute_prepared_translation_task(
    *,
    task: _PreparedTranslationTask,
    llm_model: str,
    source_language_code: str,
    source_language_label: str,
    llm_connection: LLMConnectionConfig,
) -> _CompletedTranslationTask:
    return _runtime_execute_prepared_translation_task(
        ExecuteTaskRequest(
            task=task,
            llm_model=llm_model,
            source_language_code=source_language_code,
            source_language_label=source_language_label,
            llm_connection=llm_connection,
        ),
        ExecuteTaskDeps(
            translate_structured_payload_fn=translate_structured_payload,
            completed_task_factory=_CompletedTranslationTask,
        ),
    )


def _record_translation_llm_metrics(
    *,
    repository: Any,
    run_id: str,
    debug: dict[str, Any] | None,
    duration_ms: int,
) -> None:
    usage = debug.get("usage") if isinstance(debug, dict) else None
    if isinstance(usage, dict):
        for key, metric_name in (
            ("requests", "pipeline.translate.llm_requests_total"),
            ("input_tokens", "pipeline.translate.llm_input_tokens_total"),
            ("output_tokens", "pipeline.translate.llm_output_tokens_total"),
        ):
            value = usage.get(key)
            if isinstance(value, (int, float)):
                repository.record_metric(
                    run_id=run_id,
                    name=metric_name,
                    value=float(value),
                    unit="count",
                )
    cost_usd = debug.get("estimated_cost_usd") if isinstance(debug, dict) else None
    if isinstance(cost_usd, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.translate.estimated_cost_usd",
            value=float(cost_usd),
            unit="usd",
        )
    else:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.translate.cost_missing_total",
            value=1,
            unit="count",
        )
    repository.record_metric(
        run_id=run_id,
        name="pipeline.translate.duration_ms",
        value=float(max(0, int(duration_ms))),
        unit="ms",
    )


def _persist_completed_translation_task(
    *,
    request: PersistTranslationTaskCompatRequest | None = None,
    **legacy_kwargs: Any,
) -> None:
    normalized_request = coerce_persist_translation_task_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    _runtime_persist_completed_translation_task(
        PersistTaskRequest(
            repository=normalized_request.repository,
            task=normalized_request.task,
            completed=normalized_request.completed,
            context_assist=normalized_request.context_assist,
            source_language_code=normalized_request.source_language_code,
            run_id=normalized_request.run_id,
        ),
        PersistTaskDeps(
            record_translation_llm_metrics_fn=_record_translation_llm_metrics,
        ),
    )


def _translate_candidate_into_language(
    *,
    request: TranslateCandidateCompatRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[str, bool]:
    normalized_request = coerce_translate_candidate_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return _runtime_translate_candidate_into_language(
        TranslateCandidateRequest(
            repository=normalized_request.repository,
            settings=normalized_request.settings,
            candidate=normalized_request.candidate,
            target=normalized_request.target,
            llm_model=normalized_request.llm_model,
            source_language_code=normalized_request.source_language_code,
            source_language_label=normalized_request.source_language_label,
            context_assist=normalized_request.context_assist,
            llm_connection=normalized_request.llm_connection,
            force=normalized_request.force,
            run_id=normalized_request.run_id,
        ),
        TranslateCandidateDeps(
            prepare_task_fn=_prepare_translation_task,
            execute_task_fn=_execute_prepared_translation_task,
            persist_task_fn=_persist_completed_translation_task,
        ),
    )


def _normalized_translation_granularity(granularity: str | None) -> str | None:
    return str(granularity or "").strip().lower() or None if granularity is not None else None


def _translation_localization(
    *,
    settings: Settings,
    require_targets: bool,
    error_message: str,
) -> LocalizationConfig:
    localization = settings.localization
    if localization is None or (require_targets and not localization.targets):
        raise ValueError(error_message)
    return localization


def _resolved_translation_model(*, settings: Settings) -> str:
    llm_model = str(settings.llm_model or "").strip()
    if not llm_model:
        raise ValueError("llm_model must not be empty")
    return llm_model


def _translation_targets(*, localization: LocalizationConfig) -> list[TranslationTarget]:
    return [
        TranslationTarget(code=target.code, llm_label=target.llm_label)
        for target in localization.targets
    ]


def _translation_candidates(
    request: _TranslationCandidatesRequest,
) -> list[TranslationCandidate]:
    return _incremental_candidates(
        repository=request.repository,
        granularity=request.granularity,
        include=normalize_include(request.include),
        limit=request.limit,
        source_language_code=request.source_language_code,
        period_start=request.period_start,
        period_end=request.period_end,
        all_history=request.all_history,
    )


def _translation_batch_context(
    request: _TranslationBatchContextRequest,
) -> TranslationBatchContext:
    return TranslationBatchContext(
        repository=request.repository,
        settings=request.settings,
        result=TranslationRunResult(),
        provider_failures=_ProviderFailureTracker(),
        log=logger.bind(module="translation.run"),
        force=request.force,
        run_id=request.run_id,
        context_assist=normalize_context_assist(request.context_assist),
        llm_model=request.llm_model,
        source_language_code=request.source_language_code,
        source_language_label=str(
            request.settings.llm_output_language or request.source_language_code
        ).strip(),
        llm_connection=request.settings.llm_connection_config(),
    )


def _backfill_source_language_code(
    *,
    legacy_source_language: str | None,
    localization: LocalizationConfig,
) -> str:
    source_language_code = str(
        legacy_source_language or localization.legacy_backfill_source_language_code or ""
    ).strip()
    if not source_language_code:
        raise ValueError(
            "legacy_source_language or localization.legacy_backfill_source_language_code is required for translation backfill"
        )
    return source_language_code


def _translation_backfill_context(
    request: _TranslationBackfillContextRequest,
) -> TranslationBackfillContext:
    canonical_language_code = str(request.localization.source_language_code).strip()
    return TranslationBackfillContext(
        repository=request.repository,
        settings=request.settings,
        result=TranslationRunResult(),
        provider_failures=_ProviderFailureTracker(),
        log=logger.bind(module="translation.backfill"),
        force=request.force,
        run_id=request.run_id,
        context_assist=normalize_context_assist(request.context_assist),
        llm_model=request.llm_model,
        source_language_code=request.source_language_code,
        source_language_label=_target_language_label(
            language_code=request.source_language_code,
            localization=request.localization,
            fallback=None,
        ),
        llm_connection=request.settings.llm_connection_config(),
        translation_target=TranslationTarget(
            code=canonical_language_code,
            llm_label=_target_language_label(
                language_code=canonical_language_code,
                localization=request.localization,
                fallback=request.settings.llm_output_language,
            ),
        ),
        emit_mirror_targets=request.emit_mirror_targets,
    )


def _target_language_label(
    *,
    language_code: str,
    localization: LocalizationConfig,
    fallback: str | None,
) -> str:
    if language_code == localization.source_language_code and fallback:
        return str(fallback).strip()
    for target in localization.targets:
        if target.code == language_code:
            return str(target.llm_label).strip()
    return language_code


def _mirror_candidate_into_language(
    *,
    repository: Any,
    candidate: TranslationCandidate,
    language_code: str,
    force: bool,
) -> tuple[str, bool]:
    source_hash = _payload_hash(candidate.payload)
    existing = repository.get_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=language_code,
    )
    if (
        existing is not None
        and str(getattr(existing, "source_hash", "") or "") == source_hash
        and not force
    ):
        return "skipped", False
    repository.upsert_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=language_code,
        status="succeeded",
        source_hash=source_hash,
        payload=candidate.payload,
        diagnostics={"mirrored_at": datetime.now(tz=UTC).isoformat()},
        variant_role="mirror",
    )
    return "mirrored", True


def run_translation(
    *,
    request: RunTranslationRequest | None = None,
    **legacy_kwargs: Any,
) -> TranslationRunResult:
    normalized_request = coerce_run_translation_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    localization = _translation_localization(
        settings=normalized_request.settings,
        require_targets=True,
        error_message="localization.targets must be configured for translation",
    )
    normalized_granularity = _normalized_translation_granularity(normalized_request.granularity)
    llm_model = _resolved_translation_model(settings=normalized_request.settings)
    source_language_code = str(localization.source_language_code).strip()
    return _runtime_run_translation_batch(
        _translation_batch_context(
            _TranslationBatchContextRequest(
                repository=normalized_request.repository,
                settings=normalized_request.settings,
                force=normalized_request.force,
                run_id=normalized_request.run_id,
                context_assist=normalized_request.context_assist,
                llm_model=llm_model,
                source_language_code=source_language_code,
            )
        ),
        candidates=_translation_candidates(
            _TranslationCandidatesRequest(
                repository=normalized_request.repository,
                granularity=normalized_granularity,
                include=normalized_request.include,
                limit=normalized_request.limit,
                source_language_code=source_language_code,
                period_start=normalized_request.period_start,
                period_end=normalized_request.period_end,
                all_history=normalized_request.all_history,
            )
        ),
        targets=_translation_targets(localization=localization),
        deps=TranslationBatchDeps(
            prepare_task_fn=_prepare_translation_task,
            execute_task_fn=_execute_prepared_translation_task,
            persist_task_fn=_persist_completed_translation_task,
            parallelism_fn=_translation_parallelism,
            executor_class=ThreadPoolExecutor,
        ),
    )


def run_translation_backfill(
    *,
    request: RunTranslationBackfillRequest | None = None,
    **legacy_kwargs: Any,
) -> TranslationRunResult:
    normalized_request = coerce_run_translation_backfill_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    localization = _translation_localization(
        settings=normalized_request.settings,
        require_targets=False,
        error_message="localization must be configured for translation backfill",
    )
    normalized_granularity = _normalized_translation_granularity(normalized_request.granularity)
    llm_model = _resolved_translation_model(settings=normalized_request.settings)
    source_language_code = _backfill_source_language_code(
        legacy_source_language=normalized_request.legacy_source_language,
        localization=localization,
    )
    return _runtime_run_translation_backfill_batch(
        _translation_backfill_context(
            _TranslationBackfillContextRequest(
                repository=normalized_request.repository,
                settings=normalized_request.settings,
                localization=localization,
                force=normalized_request.force,
                run_id=normalized_request.run_id,
                context_assist=normalized_request.context_assist,
                llm_model=llm_model,
                source_language_code=source_language_code,
                emit_mirror_targets=normalized_request.emit_mirror_targets,
            )
        ),
        candidates=_translation_candidates(
            _TranslationCandidatesRequest(
                repository=normalized_request.repository,
                granularity=normalized_granularity,
                include=normalized_request.include,
                limit=normalized_request.limit,
                source_language_code=source_language_code,
                all_history=normalized_request.all_history,
            )
        ),
        deps=TranslationBackfillDeps(
            mirror_language_codes_by_candidate=lambda _candidate: {
                target.code
                for target in localization.targets
                if target.code == source_language_code
            },
            translate_candidate_fn=_translate_candidate_into_language,
            mirror_candidate_fn=_mirror_candidate_into_language,
        ),
    )


def materialize_localized_languages(
    *,
    repository: Any,
    localization: LocalizationConfig,
) -> list[str]:
    _ = repository
    languages = [target.code for target in localization.targets]
    ordered: list[str] = []
    seen: set[str] = set()
    for language in languages:
        if language in seen:
            continue
        seen.add(language)
        ordered.append(language)
    return ordered


def localized_language_root(*, output_dir: Path, language_code: str) -> Path:
    return output_dir / "Localized" / language_slug(language_code)


_VULTURE_USED_TRANSLATION_APIS = (
    run_translation_backfill,
    Document,
    TranslationCandidate.document_id,
    _build_translation_system_message,
)
