---
source: hn
url: https://news.ycombinator.com/item?id=47255567
published_at: '2026-03-04T23:41:43'
authors:
- mars_liu
topics:
- agent-protocols
- structured-output
- json-representation
- ai-orchestration
- tool-calling
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# JSE: A Structural Expression Protocol for AI Agents

## Summary
JSE proposes a lightweight protocol for encoding S-expression-like structured intent into standard JSON, aiming to let AI agents express calls, plans, and transformations more consistently. It emphasizes preserving JSON compatibility while providing a representation closer to an “executable structure” than ordinary JSON data patterns.

## Problem
- Although existing AI systems can easily generate JSON, JSON is usually treated only as static data, making it hard to uniformly express structured intent such as reasoning plans, tool pipelines, and DSL instructions.
- Common current approaches rely on ad-hoc JSON schemas, tool-specific protocols, or embedded code strings, leading to fragmented representations that are hard to reuse and have poor cross-system compatibility.
- This matters because multi-agent collaboration, tool invocation, and structured software automation all need a general intermediate representation that is both machine-interpretable and easy for models to generate reliably.

## Approach
- The core method is to define **JSE (JSON Structural Expression)**: encoding **S-expression-style** structures inside **fully valid JSON**.
- The mechanism is very simple: strings starting with `$` are treated as symbols, such as `"$add"`; JSON arrays or objects can represent expressions; `$quote` is used to preserve raw data so it is not interpreted.
- For example, ` ["$add", 1, 2] ` represents a structured call; an object form such as `{"$call":"$search","query":"JSON S-expression","top_k":5}` can carry both metadata and operational intent.
- By design, it does not aim to be a full Lisp or Turing-complete system, but rather a minimal rule set that allows different implementations to support subsets of the expression space as needed.
- Its target properties include determinism, machine interpretability, ease of generation by LLMs, human readability, embeddability in prompts or API responses, and allowing systems that do not understand JSE to still treat it as ordinary JSON.

## Results
- The text **does not provide quantitative experimental results**: there are no datasets, benchmarks, accuracy numbers, latency measurements, or numerical comparisons with JSON Schema / tool calling.
- The strongest concrete claim is that JSE remains **100% valid JSON** while supporting S-expression-style logical expressions, coexistence with metadata, and `$quote` raw data sections.
- The author claims that compared with ad-hoc schemas or tool-specific formats, JSE is better suited as a unified representation of structured intent for **agent communication protocols、AI orchestration systems、structured reasoning traces、prompt-embedded DSLs、cross-model communication formats**.
- In terms of contribution type, this looks more like an **early protocol/specification proposal** than an experimentally validated research result; its current state is a public spec with examples, actively seeking feedback on prior art, semantic boundaries, and usability.

## Link
- [https://news.ycombinator.com/item?id=47255567](https://news.ycombinator.com/item?id=47255567)
