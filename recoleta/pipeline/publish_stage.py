from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from recoleta.pipeline.publish_runtime import execute_publish_stage
from recoleta.ports import PublishRepositoryPort
from recoleta.types import PublishResult


class PublishStageService(Protocol):
    settings: Any
    telegram_sender: Any | None
    _progress_console: Any

    @property
    def repository(self) -> PublishRepositoryPort: ...

    def _invoke_repository_method(self, method_name: str, /, **kwargs: Any) -> Any: ...

    def _stage_candidate_limit(self, *, limit: int) -> int: ...

    @staticmethod
    def _rebalance_items_by_source(
        *,
        items: list[Any],
        limit: int,
    ) -> tuple[list[Any], dict[str, int], dict[str, int]]: ...

    def _record_stage_source_selection_metrics(
        self,
        *,
        run_id: str,
        stage: str,
        candidate_counts: dict[str, int],
        deferred_counts: dict[str, int],
    ) -> None: ...

    def _telegram_delivery_budget(self) -> tuple[str, int, int]: ...

    def _sanitize_error_message(self, message: str) -> str: ...

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None: ...

    def _record_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
        log: Any,
        failure_message: str,
    ) -> Path | None: ...

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]: ...


def run_publish_stage(
    service: PublishStageService,
    *,
    run_id: str,
    limit: int = 50,
    period_start: Any = None,
    period_end: Any = None,
) -> PublishResult:
    return execute_publish_stage(
        service,
        run_id=run_id,
        limit=limit,
        period_start=period_start,
        period_end=period_end,
    )
