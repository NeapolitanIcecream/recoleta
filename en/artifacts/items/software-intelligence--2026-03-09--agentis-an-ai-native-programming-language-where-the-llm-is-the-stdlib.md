---
source: hn
url: https://github.com/Replikanti/agentis
published_at: '2026-03-09T23:07:42'
authors:
- ylohnitram
topics:
- ai-native-language
- agent-programming
- llm-as-stdlib
- content-addressed-code
- evolutionary-branching
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Agentis – An AI-native programming language where the LLM is the stdlib

## Summary
Agentis proposes a programming language for AI agents that treats the LLM directly as the “standard library” and represents code as a version-controlled binary hashed DAG rather than text files. Its goal is to make programs naturally centered around prompts, validation, branch exploration, and controlled execution.

## Problem
- Traditional programming languages treat LLMs as external APIs rather than language-level primitives, which makes building agent programs centered on reasoning, classification, and extraction relatively cumbersome.
- The text-file + conventional VCS model is not necessarily well suited to AI-generated/evolutionary code, making merge conflicts more likely and lacking native branching and tracing mechanisms centered on agent execution.
- Autonomous agents can easily produce runaway calls, unbounded resource consumption, or unsafe I/O, so budget constraints, sandboxing, and a verifiable execution model are needed.

## Approach
- Design `prompt` as a language primitive: many operations traditionally handled by a stdlib are instead turned into direct requests to the LLM, with support for typed outputs such as `prompt(...) -> list<string>` or structured types.
- Use a `validate` mechanism to enforce constraints on LLM outputs, such as confidence thresholds, thereby incorporating generated results into program logic and failure-handling flows.
- Introduce a Cognitive Budget (CB) / fuel mechanism to limit operation costs, preventing agents from running indefinitely and encouraging more efficient prompt design.
- Use `explore` for evolutionary branching: execution can fork, successful results form new branches, and failed branches are discarded, making it suitable for search-style problem solving.
- Store code as a SHA-256 content-addressed AST/DAG and fuse it with a built-in VCS; also provide sandboxed file I/O and domain-whitelist network access to improve security.

## Results
- The text **does not provide formal experiments, benchmarks, or peer-reviewed quantitative results**, so its performance gains relative to existing languages/frameworks cannot be verified.
- It provides one operability claim: the first run of `agentis go examples/fast-demo.ag` produces output in about **3–8 seconds**, but does not specify hardware, model, task, or comparison baseline.
- It presents several concrete feature claims: support for typed prompt outputs, validation rules, evolutionary branching, content-addressed code storage, a merge-conflict-free design, sandboxed I/O, and network whitelisting.
- At the toolchain level, it lists commands and workflows such as `init`, `go`, `commit`, `run`, `branch`, `switch`, and `log`, indicating that this is not just a language concept but also includes execution and version-management implementation.
- The implementation-complexity claim is strong: it asserts “Zero bloat,” is based on **Rust**, and mentions dependencies only on **sha2** and **ureq**, but this is an engineering description rather than an outcome metric.

## Link
- [https://github.com/Replikanti/agentis](https://github.com/Replikanti/agentis)
