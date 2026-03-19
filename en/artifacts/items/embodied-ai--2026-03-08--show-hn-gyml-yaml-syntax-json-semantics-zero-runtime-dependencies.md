---
source: hn
url: https://github.com/janbjorge/gyml
published_at: '2026-03-08T22:55:51'
authors:
- jeeybee
topics:
- config-language
- yaml-subset
- json-semantics
- parser-design
- zero-dependencies
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: GYML – YAML syntax, JSON semantics, zero runtime dependencies

## Summary
GYML proposes a strict subset configuration format with **YAML syntax and JSON semantics**, aiming to eliminate production issues caused by YAML’s common implicit type coercion, duplicate keys, and advanced features. It emphasizes predictability, readability, and zero runtime dependencies, positioning itself as a safer configuration parsing solution.

## Problem
- Traditional YAML is overly complex: the specification contains **211 grammar productions**, multiple scalar styles, anchors/aliases/tags, and implicit type coercion rules that vary across implementations.
- This flexibility can cause real bugs, such as the well-known **Norway Problem**: `NO` is parsed as the boolean `False` in YAML 1.1 rather than as a string.
- Duplicate keys, implicit types, flow style syntax, and “program-like” features in configuration files reduce predictability and can affect production system stability, which is why this problem matters.

## Approach
- The core approach is to design GYML as a **strict subset of YAML**: any valid GYML is valid YAML, but many valid YAML documents are rejected by GYML.
- It preserves YAML’s block-indentation writing style while adopting **JSON’s type semantics**: booleans can only be written as `true/false`, null can only be written as `null`, numbers use decimal integers/floats, and strings use double quotes, ensuring that “what you write is what you get.”
- It explicitly disables complex features: it rejects **anchors (`&`), aliases (`*`), and tags (`!!`)**, and does not support flow mappings `{a:1}` or flow sequences `[a,b]`, reducing ambiguity and side effects at the source.
- It strengthens configuration safety: **duplicate keys are immediate errors**, indentation must be in **multiples of 2 spaces**, and tabs are forbidden; when parsing fails, it returns precise line and column numbers along with fix suggestions.
- At the implementation level, it returns native Python types (`dict/list/str/int/float/bool/None`) and highlights **zero runtime dependencies**, reducing integration complexity.

## Results
- The text **does not provide standard benchmark tests, accuracy, throughput, or performance figures**, so there are no verifiable quantitative SOTA results.
- The clear design outcome is that it compresses many error-prone YAML features into a memorable set of rules, summarized by the author as “the rules fit on a sticky note.”
- Compared with general YAML, GYML claims to eliminate implicit type surprises; for example, `port: 8080` is parsed as an `int`, and `debug: false` is parsed as a `bool`, rather than as strings.
- For invalid input, it provides precise error locations; in the example, `port: 0xFF` raises an error at **line 1, col 7** and explicitly states that **hex/octal/binary literals are not allowed**.
- In terms of semantic constraints, it claims several strong guarantees: **one spelling per type**, **duplicate keys are hard errors**, **tabs are completely rejected**, and **anchors/aliases/tags are rejected at the lexing stage**.
- On the engineering side, the project supports converting `.gyml` to formatted JSON and requires all four checks—test, lint, format, and type-check—to pass before accepting changes, but it does not provide coverage or quality metric figures.

## Link
- [https://github.com/janbjorge/gyml](https://github.com/janbjorge/gyml)
