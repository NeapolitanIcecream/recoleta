---
source: hn
url: https://github.com/Replikanti/agentis
published_at: '2026-03-09T23:07:42'
authors:
- ylohnitram
topics:
- ai-programming-language
- llm-as-stdlib
- agent-runtime
- content-addressed-code
- version-control
relevance_score: 0.09
run_id: materialize-outputs
language_code: en
---

# Agentis – An AI-native programming language where the LLM is the stdlib

## Summary
Agentis proposes an AI-native programming language for agents that treats the LLM directly as the “standard library” and stores code as a version-controlled hashed DAG rather than text files. Its goal is to fuse prompts, execution constraints, branch exploration, and traceable version management into a single programming model.

## Problem
- Existing programming languages and toolchains are primarily designed for traditional deterministic software and are not well suited to agent workflows where LLM calls are the core primitive.
- Development based on text files and conventional VCS is not a natural fit for expressing prompt-driven execution, branch exploration, execution budget control, and content-addressed code management.
- Without built-in sandboxing, validation, and cost constraints, LLM agents can easily go out of control, are hard to reproduce, and are not conducive to safe execution.

## Approach
- `prompt` is designed as a language primitive rather than a library function; many operations that would normally be handled by a stdlib are delegated to the LLM, such as string extraction and classification.
- Typed outputs and a `validate` mechanism allow LLM results to be returned as structured types, with constraint checks improving controllability.
- Cognitive Budget (CB) is introduced as execution fuel, charging for operations and limiting infinite loops or excessive model calls by agents.
- `explore` is used for “evolutionary branching”: execution can fork to try different approaches, with successful ones retained as branches and failed ones discarded.
- At the lowest level, code is not stored as text files but as a SHA-256-hashed AST/DAG, integrated with a built-in VCS to support hash-based imports, commits, execution, branch switching, and more.

## Results
- The article does not provide standard paper-style quantitative experimental results, nor does it report accuracy, success rate, or cost comparisons on public benchmarks.
- The most specific performance claim given is that the first run of `agentis go examples/fast-demo.ag` produces output in about **3–8 seconds**.
- Functional system claims include: code is a **SHA-256** content-addressed AST, which is said to avoid traditional text merge conflicts and support hash-based imports.
- Security/engineering constraint claims include: file I/O is restricted to `.agentis/sandbox/`, and network access requires a domain whitelist.
- Minimal implementation claims include: the runtime/implementation has “Zero bloat,” depending only on **Rust + sha2 + ureq**.
- Example coverage claims include: the repository documentation says it provides **6 example programs**, from hello world to evolutionary branching.

## Link
- [https://github.com/Replikanti/agentis](https://github.com/Replikanti/agentis)
