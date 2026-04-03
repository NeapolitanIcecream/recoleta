from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.vector_store import LanceVectorStore


def _int_with_default(value: Any, *, default: int) -> int:
    return default if value is None else int(value)


@dataclass(frozen=True, slots=True)
class SemanticSearchHit:
    chunk_id: int
    doc_id: int
    chunk_index: int
    score: float
    text_preview: str


@dataclass(frozen=True, slots=True)
class SummaryCorpusWindow:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    doc_type: str
    period_start: datetime
    period_end: datetime
    granularity: str | None = None


@dataclass(frozen=True, slots=True)
class SummaryVectorSyncRequest:
    window: SummaryCorpusWindow
    embedding_model: str
    embedding_dimensions: int | None
    max_batch_inputs: int
    max_batch_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    limit: int = 500
    offset: int = 0
    llm_connection: LLMConnectionConfig | None = None

    @classmethod
    def coerce(
        cls,
        request: SummaryVectorSyncRequest | None = None,
        /,
        **legacy_kwargs: Any,
    ) -> SummaryVectorSyncRequest:
        if request is not None:
            return request
        return cls(
            window=SummaryCorpusWindow(
                repository=legacy_kwargs["repository"],
                vector_store=legacy_kwargs["vector_store"],
                run_id=str(legacy_kwargs["run_id"]),
                doc_type=str(legacy_kwargs["doc_type"]),
                granularity=legacy_kwargs.get("granularity"),
                period_start=legacy_kwargs["period_start"],
                period_end=legacy_kwargs["period_end"],
            ),
            embedding_model=str(legacy_kwargs["embedding_model"]),
            embedding_dimensions=legacy_kwargs.get("embedding_dimensions"),
            max_batch_inputs=int(legacy_kwargs["max_batch_inputs"]),
            max_batch_chars=int(legacy_kwargs["max_batch_chars"]),
            embedding_failure_mode=str(
                legacy_kwargs.get("embedding_failure_mode") or "continue"
            ),
            embedding_max_errors=int(legacy_kwargs.get("embedding_max_errors") or 0),
            limit=_int_with_default(legacy_kwargs.get("limit"), default=500),
            offset=int(legacy_kwargs.get("offset") or 0),
            llm_connection=legacy_kwargs.get("llm_connection"),
        )


@dataclass(frozen=True, slots=True)
class SummarySearchRequest:
    window: SummaryCorpusWindow
    query: str
    embedding_model: str
    embedding_dimensions: int | None
    max_batch_inputs: int
    max_batch_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    limit: int = 10
    corpus_limit: int = 500
    metric_namespace: str | None = None
    llm_connection: LLMConnectionConfig | None = None
    auto_sync_vectors: bool = True

    @classmethod
    def coerce(
        cls,
        request: SummarySearchRequest | None = None,
        /,
        **legacy_kwargs: Any,
    ) -> SummarySearchRequest:
        if request is not None:
            return request
        return cls(
            window=SummaryCorpusWindow(
                repository=legacy_kwargs["repository"],
                vector_store=legacy_kwargs["vector_store"],
                run_id=str(legacy_kwargs["run_id"]),
                doc_type=str(legacy_kwargs["doc_type"]),
                granularity=legacy_kwargs.get("granularity"),
                period_start=legacy_kwargs["period_start"],
                period_end=legacy_kwargs["period_end"],
            ),
            query=str(legacy_kwargs["query"]),
            embedding_model=str(legacy_kwargs["embedding_model"]),
            embedding_dimensions=legacy_kwargs.get("embedding_dimensions"),
            max_batch_inputs=int(legacy_kwargs["max_batch_inputs"]),
            max_batch_chars=int(legacy_kwargs["max_batch_chars"]),
            embedding_failure_mode=str(
                legacy_kwargs.get("embedding_failure_mode") or "continue"
            ),
            embedding_max_errors=int(legacy_kwargs.get("embedding_max_errors") or 0),
            limit=_int_with_default(legacy_kwargs.get("limit"), default=10),
            corpus_limit=_int_with_default(
                legacy_kwargs.get("corpus_limit"),
                default=500,
            ),
            metric_namespace=legacy_kwargs.get("metric_namespace"),
            llm_connection=legacy_kwargs.get("llm_connection"),
            auto_sync_vectors=bool(legacy_kwargs.get("auto_sync_vectors", True)),
        )
