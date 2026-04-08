from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic_ai import Agent, RunContext

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.prompt_style import reader_facing_ai_tropes_prompt
from recoleta.rag.agent_models import (
    TrendGenerationRequest,
    TrendPromptRequest,
)
from recoleta.rag.corpus_tools import (
    CorpusSpec,
    SearchService,
    _reciprocal_rank_fuse_search_hits as _shared_reciprocal_rank_fuse_search_hits,
    resolve_corpus_query_sources,
)
from recoleta.rag.search_models import SummarySearchRequest
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload


@dataclass(slots=True)
class TrendAgentDeps:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    rag_sources: list[dict[str, Any]] | None
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    metric_namespace: str = "pipeline.trends"
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    llm_connection: LLMConnectionConfig | None = None


def _search_service_from_deps(deps: TrendAgentDeps) -> SearchService:
    return SearchService(
        repository=deps.repository,
        vector_store=deps.vector_store,
        run_id=deps.run_id,
        period_start=deps.period_start,
        period_end=deps.period_end,
        corpus_spec=CorpusSpec.from_rag_sources(deps.rag_sources),
        embedding_model=deps.embedding_model,
        embedding_dimensions=deps.embedding_dimensions,
        embedding_batch_max_inputs=deps.embedding_batch_max_inputs,
        embedding_batch_max_chars=deps.embedding_batch_max_chars,
        metric_namespace=deps.metric_namespace,
        embedding_failure_mode=str(deps.embedding_failure_mode or "continue"),
        embedding_max_errors=int(deps.embedding_max_errors or 0),
        llm_connection=deps.llm_connection,
    )


_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES = 24
_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS = 15.0


def _build_trend_instructions(*, output_language: str | None) -> str:
    base = (
        "You are a research trend analyst. Use tools to explore the local corpus. "
        "Prefer summary chunks (chunk_index=0) first. "
        "When ready, return a TrendPayload with grounded, readable content."
    )
    base += (
        " Start with search_hybrid when you need to discover themes quickly, "
        "then use get_doc_bundle to inspect promising evidence bundles before falling back to get_doc or read_chunk."
    )
    base += (
        " When available, use trend documents (doc_type=trend) for synthesis and higher-level themes, "
        "and use item documents (doc_type=item) for concrete citations and grounded evidence. "
        "Do not force a Top-N must-read section; that workflow is legacy and should only appear if the prompt explicitly requires it."
    )
    base += (
        " Write the title as a direct editorial judgment, not a topic inventory. "
        "Keep the opening overview short, lead with the period-level judgment, and avoid opening with a flat list of systems or papers. "
        "Limit the opening overview to at most three named systems, papers, or benchmarks. "
        "Do not leave raw prev_n tokens in title, overview_md, or clusters[].content_md."
    )
    base += (
        " In overview_md, write body content only: do not add an extra Overview/总览 heading because the publisher adds it. "
        "The opening overview prose must stay under 200 Chinese characters or 200 words before any later sub-sections. "
        "Keep topics only in the topics field; do not add a Topics/主题 section inside overview_md. "
        "Make the title direct and specific to the content; do not prepend dates or generic labels such as Daily Trend/研究趋势日报/每日趋势. "
        "Do not append explanatory field labels inside prose."
    )
    base += (
        " Prioritize readability over compression: use short sentences, avoid long multi-clause lines, "
        "and avoid stacking many technical terms in a single sentence. "
        "Introduce acronyms once with a brief explanation in the output language, then reuse them. "
        "Avoid repetitive phrasing across overview and clusters; each section should add new value."
    )
    base += (
        " Use any history change, contradictory evidence, or representative examples as internal analysis tools, "
        "but do not expose them as separate reader-facing sections. "
        "The public output should contain only overview_md and 1 to 4 cluster briefs."
    )
    base += (
        " Each cluster brief must be a finished short note, not a worksheet. "
        "Use clusters[].title for a literal topic label, clusters[].content_md for the prose body, "
        "and clusters[].evidence_refs for grounded supporting references. "
        "Each cluster must include at least one evidence_refs entry with concrete doc_id and chunk_index values."
    )
    base = f"{base}\n\n{reader_facing_ai_tropes_prompt()}"
    if not output_language:
        return base
    return (
        f"{base}\n\nUse {output_language} for all natural language fields "
        "(title, overview_md, clusters[].title, clusters[].content_md). "
        "Keep all JSON keys in English and keep topics as concise English tags."
    )


def resolve_rag_query_sources(
    *,
    doc_type: str,
    granularity: str | None,
    rag_sources: list[dict[str, Any]] | None,
) -> list[tuple[str, str | None]]:
    return resolve_corpus_query_sources(
        doc_type=doc_type,
        granularity=granularity,
        rag_sources=rag_sources,
    )


def build_trend_agent(
    *,
    llm_model: str,
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> Agent[TrendAgentDeps, TrendPayload]:
    from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model

    model = build_pydantic_ai_model(llm_model, llm_connection=llm_connection)
    agent: Agent[TrendAgentDeps, TrendPayload] = Agent(
        model,
        deps_type=TrendAgentDeps,
        output_type=TrendPayload,
        instructions=_build_trend_instructions(output_language=output_language),
        output_retries=4,
        defer_model_check=True,
    )

    @agent.tool
    def list_docs(
        ctx: RunContext[TrendAgentDeps],
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """List documents in the active trend window."""
        return _search_service_from_deps(ctx.deps).list_docs(
            doc_type=doc_type,
            granularity=granularity,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

    @agent.tool
    def get_doc(ctx: RunContext[TrendAgentDeps], doc_id: int) -> dict[str, Any]:
        """Fetch one document with metadata."""
        return _search_service_from_deps(ctx.deps).get_doc(doc_id=doc_id)

    @agent.tool
    def get_doc_bundle(
        ctx: RunContext[TrendAgentDeps],
        doc_id: int,
        content_limit: int = 2,
        content_chars: int = 600,
    ) -> dict[str, Any]:
        """Fetch a compact evidence bundle for one document."""
        return _search_service_from_deps(ctx.deps).get_doc_bundle(
            doc_id=doc_id,
            content_limit=content_limit,
            content_chars=content_chars,
        )

    @agent.tool
    def read_chunk(
        ctx: RunContext[TrendAgentDeps],
        doc_id: int,
        chunk_index: int,
    ) -> dict[str, Any]:
        """Read one indexed chunk from a document."""
        return _search_service_from_deps(ctx.deps).read_chunk(
            doc_id=doc_id,
            chunk_index=chunk_index,
        )

    @agent.tool
    def search_text(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus lexically via FTS."""
        return _search_service_from_deps(ctx.deps).search_text(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_semantic(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus semantically over summary chunks."""
        return _search_service_from_deps(ctx.deps).search_semantic(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_hybrid(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Blend lexical and semantic retrieval for theme discovery."""
        return _search_service_from_deps(ctx.deps).search_hybrid(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    return agent


def _reciprocal_rank_fuse_search_hits(
    *,
    text_hits: list[dict[str, Any]],
    semantic_hits: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    return _shared_reciprocal_rank_fuse_search_hits(
        text_hits=text_hits,
        semantic_hits=semantic_hits,
        limit=limit,
    )


def _compact_tool_trace_value(value: Any, *, depth: int = 0) -> Any:
    from recoleta.rag.agent_runtime import _compact_tool_trace_value as _impl

    return _impl(value, depth=depth)


def _extract_raw_tool_trace(messages: list[Any]) -> dict[str, Any]:
    from recoleta.rag.agent_runtime import _extract_raw_tool_trace as _impl

    return _impl(messages)


def semantic_search_summaries_in_period(
    *,
    request: SummarySearchRequest | None = None,
    **legacy_kwargs: Any,
) -> Any:
    from recoleta.rag.semantic_search import (
        semantic_search_summaries_in_period as _impl,
    )

    return _impl(request=request, **legacy_kwargs)


def build_trend_prompt_payload(
    *,
    request: TrendPromptRequest | None = None,
    **legacy_kwargs: Any,
) -> dict[str, Any]:
    from recoleta.rag.agent_runtime import build_trend_prompt_payload as _impl

    return _impl(TrendPromptRequest.coerce(request, **legacy_kwargs))


def generate_trend_payload(
    *,
    request: TrendGenerationRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    from recoleta.rag.agent_runtime import generate_trend_payload as _impl

    return _impl(TrendGenerationRequest.coerce(request, **legacy_kwargs))


__all__ = [
    "TrendAgentDeps",
    "TrendGenerationRequest",
    "TrendPromptRequest",
    "build_trend_agent",
    "build_trend_prompt_payload",
    "generate_trend_payload",
    "resolve_rag_query_sources",
    "semantic_search_summaries_in_period",
]
