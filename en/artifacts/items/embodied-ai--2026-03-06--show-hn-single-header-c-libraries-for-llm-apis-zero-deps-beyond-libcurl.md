---
source: hn
url: https://news.ycombinator.com/item?id=47282433
published_at: '2026-03-06T23:23:17'
authors:
- Shmungus
topics:
- llm-api
- c-plus-plus
- single-header-library
- inference-infrastructure
- structured-output
relevance_score: 0.1
run_id: materialize-outputs
language_code: en
---

# Show HN: Single-header C++ libraries for LLM APIs – zero deps beyond libcurl

## Summary
This is not a robotics or foundation model paper, but rather a set of single-header C++ utility libraries for LLM APIs, emphasizing zero extra dependencies beyond `libcurl`. It aims to solve engineering problems such as streaming calls, caching, cost estimation, retry fault tolerance, and structured output with an extremely simple integration approach.

## Problem
- The problem it addresses is that when C++ developers integrate LLM APIs such as OpenAI/Anthropic, they often need to introduce many third-party dependencies, increasing compilation, deployment, and maintenance complexity.
- This matters because LLM applications in production environments need not only to "make calls," but also to handle real engineering requirements such as streaming responses, caching, cost control, retry on failure, and structured output.
- Relative to the user's stated areas of interest, it is less directly related to embodied/robot foundation models, but it can serve as supporting infrastructure for integrating underlying inference services.

## Approach
- The core method is simple: split common LLM API engineering capabilities into multiple independent single-header `.hpp` libraries so that users can "copy the file, link `libcurl`, and use it."
- `llm-stream` provides streaming output for OpenAI and Anthropic, using callbacks to process incremental tokens/text.
- `llm-cache` provides a file-backed semantic cache with LRU eviction to reduce repeated requests.
- `llm-cost` performs offline token counting and cost estimation to help developers control budgets.
- `llm-retry` and `llm-format` handle exponential backoff/circuit breaking/provider switching and structured output enforcement with a hand-written JSON parser, respectively, avoiding dependencies such as nlohmann, boost, or Python.

## Results
- The text does not provide standard paper-style quantitative experimental results; it **does not** give datasets, baseline models, accuracy, latency, throughput, or cost-savings percentages.
- The strongest concrete engineering claim is that each component can be "drop in one `.hpp`, link `libcurl`, done," meaning zero extra dependencies beyond `libcurl`.
- In terms of feature coverage, it explicitly claims support for streaming calls to **2** major providers: OpenAI and Anthropic.
- In terms of component count, it lists **5** independent libraries: `llm-stream`, `llm-cache`, `llm-cost`, `llm-retry`, and `llm-format`.
- In terms of fault-tolerance mechanisms, `llm-retry` explicitly includes **3** types of capability: exponential backoff, circuit breaker, and provider failover.
- For structured output, `llm-format` explicitly uses a hand-written JSON parser, but the text does not provide numbers for its correctness, performance, or comparisons with existing parsers.

## Link
- [https://news.ycombinator.com/item?id=47282433](https://news.ycombinator.com/item?id=47282433)
