# ADR 0008: Semantic Triage Before LLM Analysis

## Status
Accepted

## Context
Stage 4 (Analyze/LLM) is the dominant cost driver. Today, `recoleta analyze` selects candidates by state + recency only, so LLM calls are not prioritized by relevance to user `TOPICS`. Post-LLM ranking cannot reduce Stage 4 spend.

## Decision
Add an optional **Stage 3.5: Triage (Semantic Pre-Ranking)** that scores candidates against `TOPICS` before Stage 4, prioritizing (and optionally filtering) which items enter LLM analysis. Use **LiteLLM embeddings** (`litellm.embedding()`) as the default semantic signal, with a lexical fallback, fail-open behavior, and first-class observability (metrics + optional scrubbed artifacts).

## Consequences
Recoleta can increase “high-signal LLM calls” under backlog and reduce cost in filter mode, at the expense of additional embedding calls and selection bias (mitigated via exploration and recency floors). Persistent caching of scores is optional and can be introduced if repeated re-scoring becomes material.

