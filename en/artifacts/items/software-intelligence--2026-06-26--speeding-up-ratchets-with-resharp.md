---
source: hn
url: https://danverbraganza.com/writings/ratchets-run-faster-with-resharp
published_at: '2026-06-26T23:13:00'
authors:
- nvader
topics:
- code-intelligence
- agentic-coding
- software-quality
- rust
- regex-engine
- developer-tools
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# Speeding Up Ratchets with Resharp

## Summary
Ratchets v0.4.0 replaces Rust's regex crate with Resharp and runs about 15% faster on the Sculptor codebase. The change also adds proper lookaround support for regex-based rules used in agentic coding workflows.

## Problem
- Ratchet systems block new instances of forbidden code patterns while allowing existing debt to decline over time, which helps teams add rules without migrating a whole codebase at once.
- Coding agents can produce style violations or quick suppressions such as `# pyrefly: ignore`, so teams need low-cost checks that guide agents without long prompts or an agent-as-judge.
- Rust's widely used `regex` crate lacks proper lookaround support, which limited some Ratchets rules, especially comment-style rules.

## Approach
- Ratchets detects forbidden patterns with 2 mechanisms: tree-sitter abstract syntax tree queries and regular expressions.
- Tree-sitter handles syntax-aware checks where formatting or line wrapping could make regex counts wrong.
- Regex rules remain useful for patterns that are easier to express as text, such as comment style.
- The author replaced the Rust `regex` crate with Resharp in Ratchets v0.4.0 to support lookaround assertions.
- In the agent workflow described, a coding agent sees ratchet failures, while a planning agent can decide when a ratchet count may be raised.

## Results
- On the Sculptor codebase, replacing `regex` with Resharp made Ratchets run approximately 15% faster.
- The stated comparison is Ratchets before and after the engine swap, with no other code changes reported.
- Ratchets v0.4.0 is a breaking release because it changes the regex engine.
- The article reports 1 measured codebase, Sculptor, and does not provide absolute runtime, rule count, repeated-run variance, or hardware details.
- The strongest concrete claim beyond speed is functional: Resharp adds proper lookaround support that the Rust `regex` crate did not provide.

## Link
- [https://danverbraganza.com/writings/ratchets-run-faster-with-resharp](https://danverbraganza.com/writings/ratchets-run-faster-with-resharp)
