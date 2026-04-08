from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger
from pydantic_ai import Agent, RunContext

from recoleta.llm_costs import (
    estimate_cost_usd_from_tokens as estimate_llm_cost_usd_from_tokens,
)
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.ports import TrendRepositoryPort
from recoleta.prompt_style import reader_facing_ai_tropes_prompt
from recoleta.rag.corpus_tools import CorpusSpec, SearchService
from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload


@dataclass(slots=True)
class IdeasAgentDeps:
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
    metric_namespace: str = "pipeline.trends.pass.ideas"
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    llm_connection: LLMConnectionConfig | None = None


@dataclass(frozen=True, slots=True)
class TrendIdeasGenerationRequest:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    llm_model: str
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    granularity: str
    period_start: datetime
    period_end: datetime
    trend_payload: TrendPayload
    trend_snapshot_pack_md: str
    output_language: str | None = None
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    rag_sources: list[dict[str, Any]] | None = None
    include_debug: bool = False
    metric_namespace: str = "pipeline.trends.pass.ideas"
    llm_connection: LLMConnectionConfig | None = None


def _coerce_trend_ideas_generation_request(
    *,
    request: TrendIdeasGenerationRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> TrendIdeasGenerationRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return TrendIdeasGenerationRequest(
        repository=values["repository"],
        vector_store=values["vector_store"],
        run_id=str(values["run_id"]),
        llm_model=str(values["llm_model"]),
        output_language=values.get("output_language"),
        embedding_model=str(values["embedding_model"]),
        embedding_dimensions=values.get("embedding_dimensions"),
        embedding_batch_max_inputs=int(values["embedding_batch_max_inputs"]),
        embedding_batch_max_chars=int(values["embedding_batch_max_chars"]),
        embedding_failure_mode=str(values.get("embedding_failure_mode") or "continue"),
        embedding_max_errors=int(values.get("embedding_max_errors") or 0),
        granularity=str(values["granularity"]),
        period_start=values["period_start"],
        period_end=values["period_end"],
        trend_payload=values["trend_payload"],
        trend_snapshot_pack_md=str(values["trend_snapshot_pack_md"]),
        rag_sources=values.get("rag_sources"),
        include_debug=bool(values.get("include_debug", False)),
        metric_namespace=str(
            values.get("metric_namespace") or "pipeline.trends.pass.ideas"
        ),
        llm_connection=values.get("llm_connection"),
    )


def _search_service_from_deps(deps: IdeasAgentDeps) -> SearchService:
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


def _build_trend_ideas_instructions(*, output_language: str | None) -> str:
    base = (
        "You are a research opportunity analyst. Use the trend snapshot pack as the"
        " primary frame, then use tools to verify and sharpen high-value ideas."
        " Return a TrendIdeasPayload."
    )
    base += (
        " Focus on why-now opportunities: things newly buildable, revived unmet"
        " needs, research-to-product wedges, missing infrastructure, or workflow shifts."
    )
    base += (
        " Avoid generic advice such as 'build an AI platform' or 'make an assistant'."
        " Each idea must identify a concrete user/job, what changed, and the next validation step during analysis."
    )
    base += (
        " Emit 0 to 3 ideas total, ordered by confidence and practical upside."
        " Use ordering to express priority; do not expose priority as tier labels."
    )
    base += (
        " Every emitted idea must include at least one evidence_refs entry with"
        " concrete doc_id and chunk_index values grounded in the local corpus."
    )
    base += (
        " If the evidence is too weak for a high-confidence opportunity brief,"
        " return an empty ideas list and explain that briefly in summary_md instead of guessing."
    )
    base += (
        " Do not invent new umbrella terms, branded labels, or slogan-like phrasing."
        " Prefer established domain terminology."
    )
    base += (
        " If a technical term does not have a stable translation in the requested"
        " output language, prefer the original source-language term instead of forcing a translation."
    )
    base += (
        " Prefer plain, literal wording over compressed jargon, clever metaphors,"
        " or catchy headings."
    )
    base += (
        " Do not translate paper titles, framework names, product names, or acronyms"
        " unless a widely accepted translation already exists."
    )
    base += (
        " Idea titles should be factual descriptive noun phrases, not slogans,"
        " coined categories, or rhetorical questions."
    )
    base += (
        " Name the concrete buyer trigger or operational pain directly."
        " Do not hide the user/job behind generic platform language."
    )
    base += (
        " Use internal reasoning to decide why now, what changed, who it helps,"
        " what would falsify the idea, and what to test next."
        " Do not expose those axes as separate reader-facing fields."
    )
    base += (
        " Each idea must be a finished short note."
        " Use ideas[].title for a literal idea label, ideas[].content_md for the prose body,"
        " and ideas[].evidence_refs for grounded supporting references."
    )
    base += (
        " Start with search_hybrid for broad discovery, then use get_doc_bundle"
        " or read_chunk to confirm specific evidence before finalizing ideas."
    )
    base = f"{base}\n\n{reader_facing_ai_tropes_prompt()}"
    if not output_language:
        return base
    return (
        f"{base}\n\nUse {output_language} for all natural-language fields"
        " (title, summary_md, ideas[].title, ideas[].content_md, evidence reason text). Keep JSON keys"
        " and enum values in English."
    )


def build_trend_ideas_prompt_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    trend_payload: TrendPayload,
    trend_snapshot_pack_md: str,
    rag_sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "task": "Extract evidence-grounded why-now ideas from the trend snapshot.",
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "trend_title": str(trend_payload.title or "").strip(),
        "trend_topics": list(trend_payload.topics or []),
        "trend_snapshot_pack_md": trend_snapshot_pack_md,
        "notes": _trend_ideas_prompt_notes(),
    }
    if rag_sources is not None:
        payload["rag_sources"] = rag_sources
    return payload


def _trend_ideas_prompt_notes() -> list[str]:
    return [
        "Use tools to verify and sharpen candidate ideas against the active local corpus.",
        "Prefer 0-3 ideas; omit weak ideas instead of filling the list.",
        "Use idea ordering to express priority; do not emit best-bet or alternate labels.",
        "Each idea must answer what to build or investigate, why now, what changed, and who it helps during analysis.",
        "Name the buyer trigger or operational pain directly instead of using generic platform language.",
        "Use evidence_refs to point to the strongest supporting documents.",
        "Do not restate the trend summary as the final output.",
        "Do not coin new umbrella terms or marketing-style labels.",
        "If a technical term lacks a stable translation in the requested output language, keep the original term.",
        "Prefer direct, readable phrasing over compressed jargon.",
        "Keep paper titles, framework names, product names, and acronyms in their original form unless a widely accepted translation exists.",
        "Idea titles should read like factual descriptive labels, not slogans, coined categories, or rhetorical questions.",
        "Return finished short prose in ideas[].content_md instead of labeled method fields.",
    ]


def build_trend_ideas_agent(
    *,
    llm_model: str,
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> Agent[IdeasAgentDeps, TrendIdeasPayload]:
    model = build_pydantic_ai_model(llm_model, llm_connection=llm_connection)
    agent: Agent[IdeasAgentDeps, TrendIdeasPayload] = Agent(
        model,
        deps_type=IdeasAgentDeps,
        output_type=TrendIdeasPayload,
        instructions=_build_trend_ideas_instructions(output_language=output_language),
        output_retries=4,
        defer_model_check=True,
    )

    @agent.tool
    def list_docs(
        ctx: RunContext[IdeasAgentDeps],
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """List documents in the active ideas window."""
        return _search_service_from_deps(ctx.deps).list_docs(
            doc_type=doc_type,
            granularity=granularity,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

    @agent.tool
    def get_doc(ctx: RunContext[IdeasAgentDeps], doc_id: int) -> dict[str, Any]:
        """Fetch one document with metadata."""
        return _search_service_from_deps(ctx.deps).get_doc(doc_id=doc_id)

    @agent.tool
    def get_doc_bundle(
        ctx: RunContext[IdeasAgentDeps],
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
        ctx: RunContext[IdeasAgentDeps], doc_id: int, chunk_index: int
    ) -> dict[str, Any]:
        """Read one indexed chunk from a document."""
        return _search_service_from_deps(ctx.deps).read_chunk(
            doc_id=doc_id,
            chunk_index=chunk_index,
        )

    @agent.tool
    def search_text(
        ctx: RunContext[IdeasAgentDeps],
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
        ctx: RunContext[IdeasAgentDeps],
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
        ctx: RunContext[IdeasAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Blend lexical and semantic retrieval for opportunity discovery."""
        return _search_service_from_deps(ctx.deps).search_hybrid(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    return agent


def _summarize_tool_calls(messages: list[Any]) -> tuple[int, dict[str, int]]:
    total = 0
    breakdown: dict[str, int] = {}
    for msg in messages:
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) == "tool-call":
                total += 1
                tool_name = str(getattr(part, "tool_name", "") or "").strip()
                if tool_name:
                    breakdown[tool_name] = int(breakdown.get(tool_name, 0)) + 1
    return total, {name: breakdown[name] for name in sorted(breakdown)}


def _estimate_cost_usd_from_tokens(
    *, model: str, input_tokens: int | None, output_tokens: int | None
) -> float | None:
    return estimate_llm_cost_usd_from_tokens(
        model=model,
        prompt_tokens=input_tokens,
        completion_tokens=output_tokens,
    )


def generate_trend_ideas_payload(
    request: TrendIdeasGenerationRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[TrendIdeasPayload, dict[str, Any] | None]:
    resolved_request = _coerce_trend_ideas_generation_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    log = logger.bind(module="rag.ideas_agent", run_id=resolved_request.run_id)
    agent = build_trend_ideas_agent(
        llm_model=resolved_request.llm_model,
        output_language=resolved_request.output_language,
        llm_connection=resolved_request.llm_connection,
    )
    deps = IdeasAgentDeps(
        repository=resolved_request.repository,
        vector_store=resolved_request.vector_store,
        run_id=resolved_request.run_id,
        period_start=resolved_request.period_start,
        period_end=resolved_request.period_end,
        rag_sources=resolved_request.rag_sources,
        embedding_model=resolved_request.embedding_model,
        embedding_dimensions=resolved_request.embedding_dimensions,
        embedding_batch_max_inputs=resolved_request.embedding_batch_max_inputs,
        embedding_batch_max_chars=resolved_request.embedding_batch_max_chars,
        embedding_failure_mode=str(
            resolved_request.embedding_failure_mode or "continue"
        ),
        embedding_max_errors=int(resolved_request.embedding_max_errors or 0),
        metric_namespace=resolved_request.metric_namespace,
        llm_connection=resolved_request.llm_connection,
    )
    prompt = json.dumps(
        build_trend_ideas_prompt_payload(
            granularity=resolved_request.granularity,
            period_start=resolved_request.period_start,
            period_end=resolved_request.period_end,
            trend_payload=resolved_request.trend_payload,
            trend_snapshot_pack_md=resolved_request.trend_snapshot_pack_md,
            rag_sources=resolved_request.rag_sources,
        ),
        ensure_ascii=False,
        separators=(",", ":"),
    )

    result = agent.run_sync(prompt, deps=deps)
    payload = result.output
    usage = result.usage()
    messages_getter = getattr(result, "all_messages", None)
    raw_messages = messages_getter() if callable(messages_getter) else None
    messages: list[Any] = raw_messages if isinstance(raw_messages, list) else []
    tool_calls_total, tool_call_breakdown = _summarize_tool_calls(messages)
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=resolved_request.llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": usage_dict,
        "estimated_cost_usd": estimated_cost_usd,
        "tool_calls_total": tool_calls_total,
        "tool_call_breakdown": tool_call_breakdown,
        "prompt_chars": len(prompt),
        "trend_snapshot_pack_chars": len(
            str(resolved_request.trend_snapshot_pack_md or "")
        ),
        "include_debug": bool(resolved_request.include_debug),
    }
    log.info(
        "Ideas generation done include_debug={} cost_present={}",
        bool(resolved_request.include_debug),
        estimated_cost_usd is not None,
    )
    return payload, debug


__all__ = [
    "IdeasAgentDeps",
    "TrendIdeasPayload",
    "TrendIdeasGenerationRequest",
    "build_trend_ideas_agent",
    "build_trend_ideas_prompt_payload",
    "generate_trend_ideas_payload",
]
