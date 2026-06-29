---
source: hn
url: https://github.com/ahmetvural79/Vitrus
published_at: '2026-06-20T23:22:42'
authors:
- ahvural
topics:
- agent-memory
- code-intelligence
- knowledge-graph
- mcp
- api-verification
- retrieval-augmented-generation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: Vitrus – the company brain that tells you what it doesn't know

## Summary
Vitrus is a Markdown-based company memory for humans and agents that answers questions with sources, confidence, and a deterministic gap list. It targets agent workflows where unsupported claims, stale facts, and unauthorized retrieval can cause bad actions.

## Problem
- Teams and agents often search across chat, docs, tickets, and APIs, then receive raw results without a clear source trail.
- Company knowledge changes over time, so agents need to detect missing docs, stale decisions, contradictions, single-person ownership risk, and uncited claims before acting.
- API-using agents can invent endpoints or wrong arguments unless calls are checked against the actual OpenAPI spec.

## Approach
- Markdown files and optional `.edges.json` sidecars are the canonical record; PGLite or Postgres plus pgvector builds a disposable index from that record.
- Retrieval combines vector search, BM25, and entity match, then uses reciprocal rank fusion and graph-based re-scoring for connected or corroborated hits.
- Gap detection is deterministic and LLM-free: it checks graph structure and explicit signals for missing nodes, contradictions, stale facts, single-point risk, and uncited events.
- The `think` and `verify` commands return sourced answers, verdicts such as grounded/stale/contradicted/unsupported, confidence, freshness, and the exact undocumented gaps.
- Agents connect through MCP tools and API commands; OpenAPI import/search/verify/call checks endpoint names, missing args, wrong types, unknown args, deprecated endpoints, and permissions before execution.

## Results
- The repo reports `source-hit ≥90%` on its eval gate.
- Gap-Eval reports `100%` gap recall and `100%` gap precision on a controlled synthetic corpus; the authors state this does not prove real-world generalization.
- ACL leak testing reports `0` unauthorized results, with fail-closed index-layer enforcement.
- The project reports `200+` tests and four CI gates: typecheck, test, eval, and leak-test.
- The MCP surface grew from `13` to `30` tools, including search, think, verify, gap reports, API search/verify/call, onboarding paths, quizzes, schema checks, and briefings.
- Integration coverage includes `7` first-class live connectors, `8` one-token REST presets, `5` pagination styles, and hosted cloud support for `13` managed sources.

## Link
- [https://github.com/ahmetvural79/Vitrus](https://github.com/ahmetvural79/Vitrus)
