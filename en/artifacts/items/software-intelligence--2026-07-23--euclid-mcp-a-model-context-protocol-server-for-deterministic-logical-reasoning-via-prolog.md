---
source: arxiv
url: https://arxiv.org/abs/2607.21412v1
published_at: '2026-07-23T15:15:37'
authors:
- Bartolomeo Bogliolo
topics:
- model-context-protocol
- neuro-symbolic-reasoning
- prolog
- rule-enforcement
- security-compliance
- llm-agents
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Euclid-MCP: A Model Context Protocol Server for Deterministic Logical Reasoning via Prolog

## Summary
Euclid-MCP is an open-source Model Context Protocol server that lets LLM applications delegate rule-based deduction to SWI-Prolog. It combines an LLM-generated logical representation with deterministic inference and proof traces for business, security, and compliance policies.

## Problem
- LLMs can hallucinate or produce inconsistent results on multi-step reasoning, while rule-enforcement tasks require conclusions that follow from explicit facts and policies.
- Semantic RAG can retrieve similar text without guaranteeing that the rule set is logically sufficient, consistent, or auditable.
- This matters in security and compliance settings, where decisions need reproducible answers and traceable derivations.

## Approach
- Euclid-IR represents facts, Horn-clause rules, queries, conjunctions, closed-world negation, arithmetic, and wildcards in a human-readable format designed for LLM generation.
- The server deterministically compiles Euclid-IR into sanitized SWI-Prolog code, excluding dangerous constructs, capping input at 500 KB, and applying a default 30-second execution timeout.
- Four MCP tools support deduction with proof trees (`reason`), failure and success analysis (`diagnose`), counterfactual changes (`what_if`), and knowledge-base validation (`check_kb`).
- A translate-run-inspect-repair loop lets an LLM generate rules, validate them, execute queries, inspect derivations, and revise the encoded knowledge base without performing the deduction itself.
- The intermediate representation is intended to support future backends such as Datalog or SMT solvers, although the current prototype uses SWI-Prolog.

## Results
- The demonstrated IT security and compliance model contains 30 users, 50 resources, and CIS AWS benchmark, internal policy, and access-control rules; a larger stress-test variant contains 200 users, 300 resources, and approximately 3,872 facts.
- The system covers 10 canonical queries spanning single-hop permissions, multi-hop policy reasoning, and temporal or threshold conditions in the reported use case.
- The excerpt reports that LLM-only reasoning hallucinates systematically on larger knowledge bases, while Euclid-MCP produces exact answers with lower latency and more compact outputs.
- No numerical accuracy, latency, output-size, or baseline-comparison measurements are provided in the supplied text, so the strength of those performance claims cannot be independently quantified here.
- The concrete implementation claims include four MCP tools, two transport modes (stdio and HTTP), proof-tree outputs, and deterministic execution relative to the encoded facts and rules.

## Link
- [https://arxiv.org/abs/2607.21412v1](https://arxiv.org/abs/2607.21412v1)
