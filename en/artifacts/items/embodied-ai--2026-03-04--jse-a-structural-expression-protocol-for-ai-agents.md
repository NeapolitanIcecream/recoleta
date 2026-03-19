---
source: hn
url: https://news.ycombinator.com/item?id=47255567
published_at: '2026-03-04T23:41:43'
authors:
- mars_liu
topics:
- structured-output
- json-format
- agent-protocol
- s-expression
- llm-tooling
relevance_score: 0.15
run_id: materialize-outputs
language_code: en
---

# JSE: A Structural Expression Protocol for AI Agents

## Summary
JSE proposes a lightweight protocol for encoding S-expression-like "structured intent" into standard JSON, with the goal of enabling AI to output more stable, interpretable, and executable structures without relying on tool-call interfaces tied to specific systems. It is essentially an early format specification, not a model or systems paper validated through experiments.

## Problem
- Although existing AI systems are good at generating JSON, JSON is usually treated only as a data container and is not well suited to directly expressing structured operations such as "intent, computation, planning, or DSL instructions."
- Today, these needs are often addressed through ad-hoc JSON schemas, tool-specific protocols, or embedded code strings, which leads to fragmented representations, tightly coupled protocols, and poor cross-system reuse.
- This matters because agent orchestration, toolchain invocation, structured reasoning traces, and cross-model communication all need a unified expression format that is machine-interpretable and easy for models to generate.

## Approach
- The core method is to define **JSE (JSON Structural Expression)**: while **remaining 100% valid JSON**, it uses a small set of conventions to interpret JSON as an S-expression-like structure.
- The simplest mechanism is: **strings beginning with `$` are treated as symbols**, and **JSON arrays or objects are used to represent expressions/call structures**; for example, `["$add", 1, 2]` represents an addition expression.
- The object form supports **metadata and expressions coexisting**, for example `{"$call":"$search","query":"JSON S-expression","top_k":5}` can represent a structured call with parameters.
- Through the **`$quote`** mechanism, raw data regions can be marked so that not everything is interpreted as an executable expression.
- By design, it **does not aim to be a full Lisp or Turing-complete** system; instead, different implementations can support subsets of the expression system as needed, so it can be embedded in prompts, API responses, and agent protocols.

## Results
- The text **does not provide experiments, benchmarks, or quantitative results**; there are no datasets, accuracy figures, latency or cost measurements, or numerical comparisons with JSON Schema / tool calling / MCP.
- The strongest concrete claim is that the format can remain **100% valid JSON** while also expressing **S-expression style logic**.
- The author claims that compared with ad-hoc schemas or tool-specific protocols, JSE can provide a more **uniform** structured intent representation for reasoning plans, tool pipelines, structured transformations, query languages, and cross-model communication.
- The claimed design advantages include being **deterministic, machine interpretable, easy for LLMs to generate, easy for humans to read**, but these are all specification-level claims and are not empirically validated.

## Link
- [https://news.ycombinator.com/item?id=47255567](https://news.ycombinator.com/item?id=47255567)
