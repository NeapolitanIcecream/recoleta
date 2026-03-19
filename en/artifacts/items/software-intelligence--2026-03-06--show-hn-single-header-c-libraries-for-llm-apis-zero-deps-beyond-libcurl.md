---
source: hn
url: https://news.ycombinator.com/item?id=47282433
published_at: '2026-03-06T23:23:17'
authors:
- Shmungus
topics:
- c-plus-plus
- llm-api
- single-header-library
- code-infrastructure
- structured-output
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Show HN: Single-header C++ libraries for LLM APIs – zero deps beyond libcurl

## Summary
This is a set of single-header LLM API libraries for C++, emphasizing near-zero dependencies beyond `libcurl`, and covering streaming calls, caching, cost estimation, retry/fault tolerance, and structured output. Its value lies in making it easier for native C++ projects to integrate and operationalize large models without introducing a heavy dependency stack.

## Problem
- Many LLM toolchains are oriented toward Python or heavyweight dependency ecosystems, making them unsuitable for C++ projects in dependency-sensitive environments, deployment-constrained settings, or native systems software scenarios.
- Directly calling LLM APIs often lacks production-oriented capabilities such as streaming, semantic caching, cost control, retry on failure, and structured output constraints.
- This matters because in software infrastructure, code intelligence, and automated engineering, a low-dependency, embeddable, controllable LLM integration layer can significantly reduce integration and operations costs.

## Approach
- Provides multiple independently usable single-header libraries: `llm-stream`, `llm-cache`, `llm-cost`, `llm-retry`, and `llm-format`; users only need to include one `.hpp` and link `libcurl`.
- `llm-stream` supports streaming output from OpenAI and Anthropic via callbacks, simplifying integration of incremental generation.
- `llm-cache` provides a file-backed semantic cache with LRU eviction to reduce duplicate requests and latency.
- `llm-cost` performs offline token counting and cost estimation; `llm-retry` provides exponential backoff, a circuit breaker, and provider failover; `llm-format` uses a hand-written JSON parser to enforce structured output.
- Overall, the mechanism can be understood as splitting the most common “engineering glue” around calling large models into several ultra-lightweight C++ components, while avoiding external dependencies such as nlohmann, boost, or Python as much as possible.

## Results
- The text does not provide benchmark experiments, public datasets, or quantitative metrics, so there are **no reportable numerical results**.
- The strongest concrete claim is about engineering properties: “zero additional dependencies” beyond `libcurl`, delivered as single-header files, with direct drop-in integration support.
- The functionality covers 5 areas: streaming calls, file-backed semantic caching (with LRU), offline token/cost estimation, exponential backoff + circuit breaker + failover, and structured output constraints.
- Supports at least 2 model providers: OpenAI and Anthropic (explicitly mentioned in the `llm-stream` description).

## Link
- [https://news.ycombinator.com/item?id=47282433](https://news.ycombinator.com/item?id=47282433)
