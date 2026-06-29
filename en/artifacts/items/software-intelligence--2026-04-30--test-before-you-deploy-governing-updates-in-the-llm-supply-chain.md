---
source: arxiv
url: https://arxiv.org/abs/2604.27789v1
published_at: '2026-04-30T12:32:13'
authors:
- Mohd Sameen Chishti
- Damilare Peter Oyinloye
- Jingyue Li
topics:
- llm-supply-chain
- behavioral-drift
- regression-testing
- llm-governance
- code-generation
- ci-cd
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Test Before You Deploy: Governing Updates in the LLM Supply Chain

## Summary
This paper treats hosted LLM updates as a software supply-chain risk and proposes deployer-side checks before adoption. Its main claim is that application-specific contracts and risk-category tests can catch regressions caused by provider-side model changes.

## Problem
- Hosted LLM APIs can change behavior without endpoint or version changes, which can break code generation, structured output, safety behavior, and workflow automation.
- Provider benchmarks and release notes do not test each application's requirements, such as valid JSON, secure authentication code, or code-only output.
- The paper cites prior drift evidence: GPT-4 direct code execution reportedly dropped from 52% to 10% over three months, and an Anthropic incident affected up to 16% of requests.

## Approach
- Define production contracts: explicit rules a model must satisfy before use, such as passing unit tests, producing valid JSON, or causing 0% security violations.
- Group tests by deployment risk, such as authentication, data validation, and structured output, instead of relying on one total score.
- Run each prompt multiple times and record the visible model name and timestamp to track drift under non-deterministic outputs.
- Use compatibility gates to compare category metrics against thresholds and block adoption when a threshold fails.
- Apply mitigation after failures, such as prompt changes, workflow revision, fallback activation, and revalidation.

## Results
- The exploratory validation used 7 Anthropic Claude models: Haiku 3.5, Opus 3, Sonnet 4, Opus 4.5, Sonnet 4.5, Haiku 4.5, and Opus 4.6.
- The test suite used 25 prompts across 3 risk domains: authentication functions, data validation, and structured output generation.
- Each prompt was run 3–5 times to measure output variability and category-level compliance.
- Structured JSON tasks showed more drift than SQL and authentication tasks; examples included empty JSON, premature errors, changed exception types, JavaScript output instead of Python, and metadata-wrapped outputs.
- A backend SQL function passed all tests with Sonnet 4, then failed a safe-encoding test the next day, while Sonnet 4.5 stayed stable across both days.
- The paper does not report a full quantitative pass-rate table; its strongest result is qualitative evidence that risk-category tests catch regressions that a single aggregate correctness metric could hide.

## Link
- [https://arxiv.org/abs/2604.27789v1](https://arxiv.org/abs/2604.27789v1)
