from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger
from pydantic_ai import Agent, RunContext

from recoleta.rag.semantic_search import semantic_search_summaries_in_period
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.storage import Repository
from recoleta.trends import TrendPayload


@dataclass(slots=True)
class TrendAgentDeps:
    repository: Repository
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0


def _normalize_pydantic_ai_model(model: str) -> str:
    normalized = str(model or "").strip()
    if not normalized:
        raise ValueError("llm_model must not be empty")
    if ":" in normalized:
        return normalized
    if "/" in normalized:
        provider, rest = normalized.split("/", 1)
        provider = provider.strip()
        rest = rest.strip()
        if provider and rest:
            return f"{provider}:{rest}"
    return normalized


def build_trend_agent(*, llm_model: str) -> Agent[TrendAgentDeps, TrendPayload]:
    model = _normalize_pydantic_ai_model(llm_model)
    agent: Agent[TrendAgentDeps, TrendPayload] = Agent(
        model,
        deps_type=TrendAgentDeps,
        output_type=TrendPayload,
        instructions=(
            "You are a research trend analyst. Use tools to explore the local corpus. "
            "Prefer summary chunks (chunk_index=0) first. "
            "When ready, return a TrendPayload with concise, grounded content."
        ),
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
        deps = ctx.deps
        docs = deps.repository.list_documents(
            doc_type=str(doc_type or "").strip().lower(),
            period_start=deps.period_start,
            period_end=deps.period_end,
            granularity=(str(granularity).strip().lower() if granularity else None),
            order_by=str(order_by or "event_desc").strip(),
            offset=int(offset or 0),
            limit=int(limit or 50),
        )
        out: list[dict[str, Any]] = []
        for doc in docs:
            published_at = getattr(doc, "published_at", None)
            period_start_value = getattr(doc, "period_start", None)
            period_end_value = getattr(doc, "period_end", None)
            out.append(
                {
                    "doc_id": int(getattr(doc, "id")),
                    "doc_type": str(getattr(doc, "doc_type") or ""),
                    "title": str(getattr(doc, "title") or ""),
                    "item_id": getattr(doc, "item_id", None),
                    "source": str(getattr(doc, "source") or ""),
                    "canonical_url": str(getattr(doc, "canonical_url") or ""),
                    "published_at": published_at.isoformat()
                    if isinstance(published_at, datetime)
                    else None,
                    "granularity": str(getattr(doc, "granularity") or ""),
                    "period_start": period_start_value.isoformat()
                    if isinstance(period_start_value, datetime)
                    else None,
                    "period_end": period_end_value.isoformat()
                    if isinstance(period_end_value, datetime)
                    else None,
                }
            )
        return {"docs": out, "returned": len(out)}

    @agent.tool
    def get_doc(ctx: RunContext[TrendAgentDeps], doc_id: int) -> dict[str, Any]:
        deps = ctx.deps
        doc = deps.repository.get_document(doc_id=int(doc_id or 0))
        if doc is None:
            return {"doc": None}
        published_at = getattr(doc, "published_at", None)
        period_start_value = getattr(doc, "period_start", None)
        period_end_value = getattr(doc, "period_end", None)
        return {
            "doc": {
                "doc_id": int(getattr(doc, "id")),
                "doc_type": str(getattr(doc, "doc_type") or ""),
                "title": str(getattr(doc, "title") or ""),
                "item_id": getattr(doc, "item_id", None),
                "source": str(getattr(doc, "source") or ""),
                "canonical_url": str(getattr(doc, "canonical_url") or ""),
                "published_at": published_at.isoformat()
                if isinstance(published_at, datetime)
                else None,
                "granularity": str(getattr(doc, "granularity") or ""),
                "period_start": period_start_value.isoformat()
                if isinstance(period_start_value, datetime)
                else None,
                "period_end": period_end_value.isoformat()
                if isinstance(period_end_value, datetime)
                else None,
            }
        }

    @agent.tool
    def read_chunk(
        ctx: RunContext[TrendAgentDeps], doc_id: int, chunk_index: int
    ) -> dict[str, Any]:
        deps = ctx.deps
        chunk = deps.repository.read_document_chunk(
            doc_id=int(doc_id or 0), chunk_index=int(chunk_index or 0)
        )
        if chunk is None:
            return {"chunk": None}
        return {
            "chunk": {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": str(getattr(chunk, "text") or ""),
            }
        }

    @agent.tool
    def search_text(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        deps = ctx.deps
        hits = deps.repository.search_chunks_text(
            query=str(query or ""),
            doc_type=str(doc_type or "").strip().lower(),
            period_start=deps.period_start,
            period_end=deps.period_end,
            limit=int(limit or 10),
        )
        return {"hits": hits, "returned": len(hits)}

    @agent.tool
    def search_semantic(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        limit: int = 10,
    ) -> dict[str, Any]:
        deps = ctx.deps
        hits = semantic_search_summaries_in_period(
            repository=deps.repository,
            vector_store=deps.vector_store,
            run_id=deps.run_id,
            doc_type=str(doc_type or "").strip().lower(),
            period_start=deps.period_start,
            period_end=deps.period_end,
            query=str(query or ""),
            embedding_model=deps.embedding_model,
            embedding_dimensions=deps.embedding_dimensions,
            max_batch_inputs=deps.embedding_batch_max_inputs,
            max_batch_chars=deps.embedding_batch_max_chars,
            embedding_failure_mode=str(deps.embedding_failure_mode or "continue"),
            embedding_max_errors=int(deps.embedding_max_errors or 0),
            limit=int(limit or 10),
            metric_namespace="pipeline.trends",
        )
        rows = [
            {
                "chunk_id": h.chunk_id,
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
                "text_preview": h.text_preview,
            }
            for h in hits
        ]
        return {"hits": rows, "returned": len(rows)}

    return agent


def _count_tool_calls(messages: list[Any]) -> int:
    total = 0
    for msg in messages:
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) == "tool-call":
                total += 1
    return total


def _estimate_cost_usd_from_tokens(
    *, model: str, input_tokens: int | None, output_tokens: int | None
) -> float | None:
    if input_tokens is None and output_tokens is None:
        return None
    prompt_tokens = int(input_tokens or 0)
    completion_tokens = int(output_tokens or 0)
    if prompt_tokens <= 0 and completion_tokens <= 0:
        return 0.0
    try:
        from litellm.cost_calculator import cost_per_token
    except Exception:
        return None

    candidates: list[str] = []
    raw = str(model or "").strip()
    if raw:
        candidates.append(raw)
        # pydantic-ai normalized form: provider:model
        if "/" in raw and ":" not in raw:
            provider, rest = raw.split("/", 1)
            provider = provider.strip()
            rest = rest.strip()
            if provider and rest:
                candidates.append(f"{provider}:{rest}")
                candidates.append(rest)
        if ":" in raw:
            _, rest = raw.split(":", 1)
            rest = rest.strip()
            if rest:
                candidates.append(rest)

    seen: set[str] = set()
    for candidate in candidates:
        normalized = str(candidate).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        try:
            prompt_cost, completion_cost = cost_per_token(
                model=normalized,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            return float(prompt_cost) + float(completion_cost)
        except Exception:
            continue
    return None


def generate_trend_payload(
    *,
    repository: Repository,
    vector_store: LanceVectorStore,
    run_id: str,
    llm_model: str,
    embedding_model: str,
    embedding_dimensions: int | None,
    embedding_batch_max_inputs: int,
    embedding_batch_max_chars: int,
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    include_debug: bool = False,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    log = logger.bind(module="rag.trend_agent", run_id=run_id)
    agent = build_trend_agent(llm_model=llm_model)
    deps = TrendAgentDeps(
        repository=repository,
        vector_store=vector_store,
        run_id=run_id,
        period_start=period_start,
        period_end=period_end,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        embedding_batch_max_inputs=embedding_batch_max_inputs,
        embedding_batch_max_chars=embedding_batch_max_chars,
        embedding_failure_mode=str(embedding_failure_mode or "continue"),
        embedding_max_errors=int(embedding_max_errors or 0),
    )

    prompt = json.dumps(
        {
            "task": "Generate research trends for the period.",
            "granularity": granularity,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "corpus": {"doc_type": corpus_doc_type, "granularity": corpus_granularity},
            "notes": [
                "Use tools to cite representative doc_id/chunk_index in clusters.",
                "Keep output concise and grounded in the corpus.",
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

    result = agent.run_sync(prompt, deps=deps)
    payload = result.output
    usage = result.usage()
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": usage_dict,
        "estimated_cost_usd": estimated_cost_usd,
    }
    if include_debug:
        messages = result.all_messages()
        debug["tool_calls_total"] = _count_tool_calls(messages)
    log.info(
        "Trend generation done include_debug={} cost_present={}",
        bool(include_debug),
        estimated_cost_usd is not None,
    )
    return payload, debug
