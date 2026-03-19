---
source: hn
url: https://github.com/janbjorge/gyml
published_at: '2026-03-08T22:55:51'
authors:
- jeeybee
topics:
- configuration-language
- yaml-subset
- json-semantics
- parser-tooling
- python-library
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# Show HN: GYML – YAML syntax, JSON semantics, zero runtime dependencies

## Summary
GYML proposes a stricter, more predictable configuration language: it preserves YAML's indentation-based writing style, but adopts JSON's type semantics and has no runtime dependencies. Its goal is to reduce production incidents caused by YAML's implicit type conversions, duplicate keys, and advanced features.

## Problem
- The YAML specification is complex and implementations vary widely, with features such as implicit type conversion, anchors, aliases, and tags, which can easily cause errors where "something that looks like a string is actually parsed as another type."
- A typical example is the *Norway Problem*: `NO` may be parsed as the boolean `false` in YAML 1.1, which can introduce subtle bugs in configurations, country codes, identifiers, and similar scenarios.
- Configuration files need predictable, debuggable, low-dependency parsing behavior; otherwise they can cause hard-to-diagnose problems in software engineering and production systems.

## Approach
- The core mechanism is simple: **keep only YAML's block indentation syntax, discard most YAML capabilities that create ambiguity, and enforce JSON-style type semantics**, so that "what you write is what you get."
- Only one canonical form is allowed for each type: booleans can only be `true`/`false`, null can only be `null`, numbers only accept decimal integers/floats, and strings use double quotes in reserved-word scenarios.
- Only block-style structures are supported; flow mapping/sequence (such as `{a: 1}` and `[a, b]`) are rejected, but empty literals `{}` and `[]` are allowed.
- Anchors, aliases, and tags are rejected directly at the lexical level, duplicate keys are treated as hard errors, and strict 2-space indentation is required with tabs forbidden.
- In implementation, it returns native Python objects (`dict/list/str/int/float/bool/None`), and provides precise line-and-column error messages as well as `.gyml -> JSON` CLI conversion capability.

## Results
- The article **does not provide standard benchmark tests or quantitative experimental results such as accuracy/speed/throughput**, so there are no academic-style numerical metrics to report.
- In terms of specification complexity, the author emphasizes that YAML has **211 grammar productions across 10 chapters**; GYML compresses the rules into a small set of constraints that can fit on a "sticky note," emphasizing understandability and predictability.
- In terms of functional constraints, GYML explicitly claims: **all valid GYML is valid YAML, but the reverse is not true**; this is a design breakthrough that trades for stable semantics through "strict subset" design.
- In engineering behavior, parsing results directly produce native Python types; in the examples, `port: 8080` is parsed as `int 8080`, and `debug: false` is parsed as `bool False`, avoiding them being treated as strings or implicitly converted incorrectly.
- For error reporting, the author claims it can precisely locate **line/column**; for example, `port: 0xFF` reports `line 1, col 7` and explains that hexadecimal/octal/binary literals are not allowed.
- The project also claims **zero runtime dependencies**, complete type annotations, and that tests/ruff/type-check must all pass, reflecting its engineering positioning for production-oriented configuration parsing.

## Link
- [https://github.com/janbjorge/gyml](https://github.com/janbjorge/gyml)
