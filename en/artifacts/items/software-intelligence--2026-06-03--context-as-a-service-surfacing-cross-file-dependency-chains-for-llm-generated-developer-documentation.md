---
source: arxiv
url: https://arxiv.org/abs/2606.04397v1
published_at: '2026-06-03T03:26:56'
authors:
- Ameya Gawde
- Vyzantinos Repantis
- Harshvardhan Singh
- Lucy Moys
topics:
- code-intelligence
- llm-agents
- developer-documentation
- retrieval-augmented-generation
- repository-analysis
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Context-as-a-Service: Surfacing Cross-File Dependency Chains for LLM-Generated Developer Documentation

## Summary
CaaS is a tool-callable retrieval layer that helps LLM coding agents check developer documentation against evidence spread across a repository. In two production-SDK case studies, it found 8 documentation or tutorial issues missed by a baseline agent with normal repository tools.

## Problem
- LLM-generated developer documentation can read well while making wrong claims about behavior defined in other files, tests, examples, or platform documentation.
- Standard tools such as file reads, keyword search, and symbol navigation often miss semantic dependency chains, such as deferred cleanup behavior or required components created elsewhere.
- This matters because wrong API comments and tutorials can lead developers to use an SDK incorrectly or write examples that fail at compile time or runtime.

## Approach
- CaaS indexes source code, API references, tests, examples, and upstream documentation for a target codebase.
- It combines BM25 keyword search with DRAMA dense retrieval, then merges rankings with reciprocal rank fusion.
- An LLM agent calls CaaS during documentation review or generation, receives ranked snippets with file metadata, and then opens the source files needed to verify a claim.
- Retrieved snippets are treated as candidate evidence. A finding is kept only when the evidence supports a concrete documentation correction or tutorial fix.

## Results
- Evaluation used Claude Sonnet 4.6 on 2 documentation workflows in one production SDK with roughly 200 source files; each efficiency condition ran 5 times.
- API reference review: the baseline found 5 missing public-member docs; CaaS found the same 5 plus 4 extra issues, made up of 2 cross-file factual errors and 2 underspecified API comments.
- Tutorial validation: the baseline validated 17 API claims; CaaS found 4 extra issues, made up of 1 executable URI bug, 1 API-usage improvement, and 2 missing prerequisites.
- Across both studies, retained findings increased from 5 with the baseline to 13 with CaaS, so CaaS added 8 findings missed by normal repository tools.
- Efficiency improved in both tasks: API review wall-clock time fell from 4.1 ± 0.7 min to 3.2 ± 0.4 min, and input tokens fell from 17.4K ± 1.8K to 14.6K ± 1.3K.
- Tutorial validation wall-clock time fell from 17.2 ± 2.1 min to 11.4 ± 1.3 min, and input tokens fell from 112.3K ± 8.6K to 76.8K ± 6.2K; the tradeoff was more LLM calls, rising from 17.4 ± 1.9 to 30.2 ± 2.4.

## Link
- [https://arxiv.org/abs/2606.04397v1](https://arxiv.org/abs/2606.04397v1)
