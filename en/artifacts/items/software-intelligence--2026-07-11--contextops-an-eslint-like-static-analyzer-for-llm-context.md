---
source: hn
url: https://github.com/Abhijeet777ui/contextops
published_at: '2026-07-11T22:36:06'
authors:
- Abhijeet_Buag
topics:
- llm-context-analysis
- static-analysis
- prompt-engineering
- rag-systems
- ai-quality-gates
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# ContextOps, an ESLint-like static analyzer for LLM context

## Summary
ContextOps is a deterministic, model-independent static analyzer that checks the structural quality of LLM context before inference. It produces a 0–100 Context Health Score, diagnostics, token estimates, and CI-compatible quality gates without model calls or network access.

## Problem
- LLM applications often send duplicated retrieval chunks, oversized system prompts, long conversation histories, and excessive tool output to models.
- These structural problems increase token cost and latency, reduce predictability, and can exhaust context windows in long-running agent workflows.
- Existing prompt and model evaluations do not directly measure context structure before inference.

## Approach
- ContextOps accepts structured context dictionaries, OpenAI message lists, or plain strings and analyzes them with lexical methods such as n-gram overlap, Jaccard similarity, and exact matching.
- It scores four dimensions: redundancy, density, structure, and source concentration. The score is `max(0, min(100, round(100 - total_penalty)))`.
- It reports duplicated tokens, near-duplicate chunks, token breakdowns, estimated savings, structural findings, and recommended fixes. It does not assess semantic relevance, factual correctness, hallucinations, reasoning, or output quality.
- Profiles such as `rag` adjust warning thresholds, while the global 0–100 score remains unchanged. CLI checks, snapshot diffs, stability reports, Python APIs, LangChain callbacks, and GitHub Actions support quality gates and regression tracking.

## Results
- The provided example received a Context Health Score of 81/100, with 214 duplicated tokens, retrieval occupying 78% of the context, two near-duplicate retrieval chunks, and estimated token savings of 12%.
- ContextOps claims runtime below 2 seconds for payloads up to 5,000 tokens and below 10 seconds for payloads of 50,000 tokens.
- The engine is deterministic and requires only Python dependencies such as `tiktoken` and `click`; it uses no GPU, embeddings, inference API, network connection, or external service.
- ContextBench contains 1,500 samples across five categories and applies a quality-floor requirement of CHS ≥78 to optimizer submissions, but the excerpt provides no measured accuracy, false-positive rate, optimizer leaderboard result, or comparison with another analyzer.
- ContextSecBench adds 9,500 adversarial payloads covering prompt-injection hiding, truncation smuggling, semantic denial of service, context poisoning, and format corruption, but the excerpt provides no performance results on this set.

## Link
- [https://github.com/Abhijeet777ui/contextops](https://github.com/Abhijeet777ui/contextops)
