from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.search_models import SummarySearchRequest, SummaryCorpusWindow
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload


@dataclass(frozen=True, slots=True)
class TrendPromptRequest:
    granularity: str
    period_start: datetime
    period_end: datetime
    corpus_doc_type: str
    corpus_granularity: str | None = None
    overview_pack_md: str | None = None
    history_pack_md: str | None = None
    rag_sources: list[dict[str, Any]] | None = None
    ranking_n: int | None = None
    rep_source_doc_type: str | None = None
    evolution_max_signals: int | None = None

    @classmethod
    def coerce(
        cls,
        request: TrendPromptRequest | None = None,
        /,
        **legacy_kwargs: Any,
    ) -> TrendPromptRequest:
        if request is not None:
            return request
        return cls(
            granularity=str(legacy_kwargs["granularity"]),
            period_start=legacy_kwargs["period_start"],
            period_end=legacy_kwargs["period_end"],
            corpus_doc_type=str(legacy_kwargs["corpus_doc_type"]),
            corpus_granularity=legacy_kwargs.get("corpus_granularity"),
            overview_pack_md=legacy_kwargs.get("overview_pack_md"),
            history_pack_md=legacy_kwargs.get("history_pack_md"),
            rag_sources=legacy_kwargs.get("rag_sources"),
            ranking_n=legacy_kwargs.get("ranking_n"),
            rep_source_doc_type=legacy_kwargs.get("rep_source_doc_type"),
            evolution_max_signals=legacy_kwargs.get("evolution_max_signals"),
        )


@dataclass(frozen=True, slots=True)
class TrendGenerationRequest:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    llm_model: str
    granularity: str
    period_start: datetime
    period_end: datetime
    corpus_doc_type: str
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    output_language: str | None = None
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    corpus_granularity: str | None = None
    overview_pack_md: str | None = None
    history_pack_md: str | None = None
    rag_sources: list[dict[str, Any]] | None = None
    ranking_n: int | None = None
    rep_source_doc_type: str | None = None
    evolution_max_signals: int | None = None
    include_debug: bool = False
    metric_namespace: str = "pipeline.trends"
    llm_connection: LLMConnectionConfig | None = None

    @classmethod
    def coerce(
        cls,
        request: TrendGenerationRequest | None = None,
        /,
        **legacy_kwargs: Any,
    ) -> TrendGenerationRequest:
        if request is not None:
            return request
        return cls(
            repository=legacy_kwargs["repository"],
            vector_store=legacy_kwargs["vector_store"],
            run_id=str(legacy_kwargs["run_id"]),
            llm_model=str(legacy_kwargs["llm_model"]),
            output_language=legacy_kwargs.get("output_language"),
            embedding_model=str(legacy_kwargs["embedding_model"]),
            embedding_dimensions=legacy_kwargs.get("embedding_dimensions"),
            embedding_batch_max_inputs=int(legacy_kwargs["embedding_batch_max_inputs"]),
            embedding_batch_max_chars=int(legacy_kwargs["embedding_batch_max_chars"]),
            embedding_failure_mode=str(
                legacy_kwargs.get("embedding_failure_mode") or "continue"
            ),
            embedding_max_errors=int(legacy_kwargs.get("embedding_max_errors") or 0),
            granularity=str(legacy_kwargs["granularity"]),
            period_start=legacy_kwargs["period_start"],
            period_end=legacy_kwargs["period_end"],
            corpus_doc_type=str(legacy_kwargs["corpus_doc_type"]),
            corpus_granularity=legacy_kwargs.get("corpus_granularity"),
            overview_pack_md=legacy_kwargs.get("overview_pack_md"),
            history_pack_md=legacy_kwargs.get("history_pack_md"),
            rag_sources=legacy_kwargs.get("rag_sources"),
            ranking_n=legacy_kwargs.get("ranking_n"),
            rep_source_doc_type=legacy_kwargs.get("rep_source_doc_type"),
            evolution_max_signals=legacy_kwargs.get("evolution_max_signals"),
            include_debug=bool(legacy_kwargs.get("include_debug", False)),
            metric_namespace=str(
                legacy_kwargs.get("metric_namespace") or "pipeline.trends"
            ),
            llm_connection=legacy_kwargs.get("llm_connection"),
        )

    def prompt_request(self) -> TrendPromptRequest:
        return TrendPromptRequest(
            granularity=self.granularity,
            period_start=self.period_start,
            period_end=self.period_end,
            corpus_doc_type=self.corpus_doc_type,
            corpus_granularity=self.corpus_granularity,
            overview_pack_md=self.overview_pack_md,
            history_pack_md=self.history_pack_md,
            rag_sources=self.rag_sources,
            ranking_n=self.ranking_n,
            rep_source_doc_type=self.rep_source_doc_type,
            evolution_max_signals=self.evolution_max_signals,
        )


@dataclass(frozen=True, slots=True)
class RepresentativeBackfillRequest:
    payload: TrendPayload
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    rep_source_doc_type: str | None = None
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    metric_namespace: str = "pipeline.trends"
    llm_connection: LLMConnectionConfig | None = None
    max_reps: int = 6

    def search_request(self, *, query: str, limit: int) -> SummarySearchRequest:
        normalized_doc_type = str(self.rep_source_doc_type or "").strip().lower()
        doc_type = normalized_doc_type if normalized_doc_type in {"item", "trend"} else "item"
        return SummarySearchRequest(
            window=SummaryCorpusWindow(
                repository=self.repository,
                vector_store=self.vector_store,
                run_id=self.run_id,
                doc_type=doc_type,
                period_start=self.period_start,
                period_end=self.period_end,
            ),
            query=query,
            embedding_model=self.embedding_model,
            embedding_dimensions=self.embedding_dimensions,
            max_batch_inputs=self.embedding_batch_max_inputs,
            max_batch_chars=self.embedding_batch_max_chars,
            embedding_failure_mode=self.embedding_failure_mode,
            embedding_max_errors=self.embedding_max_errors,
            limit=limit,
            metric_namespace=self.metric_namespace,
            llm_connection=self.llm_connection,
        )
