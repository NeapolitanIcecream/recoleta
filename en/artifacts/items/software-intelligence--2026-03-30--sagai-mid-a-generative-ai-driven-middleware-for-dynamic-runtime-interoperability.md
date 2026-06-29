---
source: arxiv
url: http://arxiv.org/abs/2603.28731v1
published_at: '2026-03-30T17:46:41'
authors:
- Oliver Aleksander Larsen
- Mahyar T. Moghaddam
topics:
- llm-middleware
- runtime-interoperability
- schema-matching
- code-generation
- distributed-systems
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# SAGAI-MID: A Generative AI-Driven Middleware for Dynamic Runtime Interoperability

## Summary
SAGAI-MID is an LLM-driven FastAPI middleware that detects schema mismatches between heterogeneous services at runtime and rewrites requests to fit the target schema. It turns API and payload adaptation into a live middleware function instead of a hand-coded adapter for each schema pair.

## Problem
- Distributed systems often connect REST APIs, GraphQL services, and IoT devices whose payloads differ in field names, types, units, and nesting.
- Static adapters and mapping rules need manual work for each source-target schema pair and break when new combinations appear at runtime.
- This matters because schema evolution and protocol heterogeneity create ongoing maintenance cost and interoperability failures in production systems.

## Approach
- The middleware intercepts HTTP requests, looks up the source and target JSON schemas for the route, and checks for mismatches.
- Detection has two parts: a deterministic structural diff for missing fields, type differences, nesting, and cardinality; and an LLM semantic check for naming and unit mismatches.
- Resolution uses two strategies: **DIRECT**, where the LLM maps fields and transforms each request, and **CODEGEN**, where the LLM writes a Python adapter function that is compiled, validated, and cached for reuse.
- Reliability comes from a three-tier safeguard stack: JSON Schema and Pydantic validation, ensemble voting with 3 parallel LLM calls when validation fails, and a rule-based fallback for known renames, unit conversions, type coercions, and array/single-value cases.
- Cached CODEGEN adapters are keyed by SHA-256 hashes of the source and target schemas, so repeated schema pairs can run with zero LLM calls after the first compile.

## Results
- On 10 interoperability scenarios across REST, GraphQL, and IoT, and across 6 LLMs from OpenAI and xAI, the best setup reached **0.90 pass@1**: **Grok 4.1 Fast (reasoning) + CODEGEN**.
- Averaged over all 6 models, **CODEGEN beat DIRECT on pass@1: 0.83 vs 0.77**. It also improved value accuracy from **0.95 to 0.97**.
- Cross-model results: GPT-4o **0.70 -> 0.83**, GPT-5 **0.80 -> 0.80**, GPT-5.2 **0.83 -> 0.87**, GPT-5-nano **0.73 -> 0.73**, Grok 4.1 Fast non-reasoning **0.70 -> 0.87**, Grok 4.1 Fast reasoning **0.87 -> 0.90** for DIRECT -> CODEGEN.
- Field-level mapping quality stayed high across models with **Field F1 >= 0.98**, so most errors came from wrong transformed values rather than missing field correspondences.
- Scenario difficulty varied: stock casing, nested-to-flat, missing fields, and array-single transformations reached **1.00 pass@1** across models, while sensor analytics and metric normalization were hardest at about **0.50-0.56** mean pass@1.
- Cost and latency varied sharply across models. Total benchmark cost ranged from **$0.18** to **$6.25** and mean latency from about **9 s** to **104 s**. The paper claims the most accurate model was also the cheapest in this setup: **Grok 4.1 Fast (reasoning), 0.90 pass@1 at $0.18**.

## Link
- [http://arxiv.org/abs/2603.28731v1](http://arxiv.org/abs/2603.28731v1)
