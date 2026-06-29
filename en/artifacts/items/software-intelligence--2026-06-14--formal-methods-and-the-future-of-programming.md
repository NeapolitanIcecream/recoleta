---
source: hn
url: https://blog.janestreet.com/formal-methods-at-jane-street-index/
published_at: '2026-06-14T23:00:33'
authors:
- dcre
topics:
- formal-methods
- agentic-coding
- programming-languages
- code-verification
- type-systems
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Formal Methods and the Future of Programming

## Summary
Jane Street says agentic coding makes formal methods more practical and more valuable for software production. The piece argues that proof tools can cut review burden, give agents better feedback, and help enforce codebase invariants that tests miss.

## Problem
- Agent-generated code often needs heavy human review before release.
- Tests cover only part of the state space, so they miss some bugs and invariant violations.
- Full formal verification has been too expensive for most software, so adoption stayed limited.

## Approach
- Use agents and models to lower the cost of writing and maintaining proofs.
- Treat formal methods as a feedback signal for coding agents, alongside tests and property-based testing.
- Extend the programming language, OxCaml, with stronger type-level constraints, modular specifications, and proof-friendly features.
- Combine language design and proof tooling so guarantees become easier to express and check in day-to-day development.

## Results
- No quantitative experimental results are reported in the excerpt.
- The strongest claim is strategic: agentic coding changes the cost/benefit balance enough that Jane Street is building a formal methods team.
- The text cites seL4 as the cost baseline for old-style verification: 25 person-years to verify 8,700 lines of C, about 23 lines of proof per line of code, and roughly half a person-day per line.
- It claims types can already eliminate whole classes of defects such as data races and cross-site scripting when those constraints are encoded in the type system.
- It argues formal methods can reduce verification work for agent-written code and improve agent performance on hard tasks, but gives no benchmark numbers.

## Link
- [https://blog.janestreet.com/formal-methods-at-jane-street-index/](https://blog.janestreet.com/formal-methods-at-jane-street-index/)
