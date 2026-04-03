from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Protocol

from recoleta.pipeline.ideas_runtime import _record_ideas_debug_artifact, execute_ideas_stage
from recoleta.passes import TrendIdeasPayload
from recoleta.ports import TrendStageRepositoryPort
from recoleta.types import IdeasResult


class IdeasStageService(Protocol):
    settings: Any
    analyzer: Any
    semantic_triage: Any
    telegram_sender: Any | None
    _llm_connection: Any

    @property
    def repository(self) -> TrendStageRepositoryPort: ...

    def ideas(
        self,
        *,
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
    ) -> IdeasResult: ...

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


def run_ideas_stage(
    service: IdeasStageService,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
) -> IdeasResult:
    return execute_ideas_stage(
        service,
        run_id=run_id,
        granularity=granularity,
        anchor_date=anchor_date,
        llm_model=llm_model,
    )


__all__ = [
    "IdeasStageService",
    "TrendIdeasPayload",
    "_record_ideas_debug_artifact",
    "run_ideas_stage",
]
