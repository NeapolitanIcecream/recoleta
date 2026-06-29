---
source: arxiv
url: https://arxiv.org/abs/2605.21434v1
published_at: '2026-05-20T17:25:52'
authors:
- Youcheng Sun
- Jiawen Liu
- Daniel Kroening
- Jason Xue
topics:
- bounded-model-checking
- code-verification
- llm-agents
- systems-software
- specification-inference
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Agentic Model Checking

## Summary
BMC-Agent verifies LLM-generated systems code by letting LLM agents write and refine specs while CBMC or Kani checks them. It targets low-level C and Rust bugs that need exhaustive bounded search and concrete counterexamples.

## Problem
- LLM-generated systems code often lacks formal specs and hides safety assumptions at call sites, so public APIs can crash on adversarial inputs.
- LLM-only review can flag risky patterns, but it cannot prove absence of integer, pointer, bounds, or panic bugs across input ranges.
- Plain bounded model checking needs specs and can produce counterexamples that may be unreachable or model artifacts, so findings need reachability and replay checks.

## Approach
- An LLM agent infers each function’s preconditions, postconditions, and optional functional-correctness checks from caller context and source code.
- The inferred specs use a restricted DSL that maps directly to `__CPROVER_assume` and `__CPROVER_assert` for C, or `kani::assume` and `kani::assert` for Rust.
- Each function is checked alone with CBMC or Kani; callees are replaced by stubs constrained by their postconditions.
- A validation pipeline checks counterexamples through input reachability, callee feasibility, dynamic replay, and a realism audit before reporting bugs.
- Unrealistic witnesses trigger spec or model refinements, which pass through a soundness guard before re-running the checker.

## Results
- On VibeOS, a 15,000 LoC LLM-generated ARM64 kernel in C, the paper claims 34 realistic bugs across 12 modules, with 16 reproduced as runtime faults.
- On five mature OSS-Fuzz-hardened targets, `jq`, OpenSSL, libcurl, libxml2, and protobuf upb, it reports 2 undefined-behavior defects in `jq` and bounded clean verification on heavily fuzzed parser surfaces.
- On an out-of-tree Realtek r8125 Linux driver, it reports 1 CAP_NET_ADMIN-gated MMIO bounds-check bypass in `rtl8125_tool_ioctl`.
- On `claudes-c-compiler`, a 50,000-line LLM-generated Rust C compiler, it claims 25 real bugs: 24 panic-class defects on public-API byte helpers and 1 functional-correctness violation found by behavioral specs.
- It also claims bounded functional equivalence for selected ELF hash and header-write helpers.
- The default BMC settings include unwind bound k=4 and a 120 second per-function timeout, with Kani retries that raise unwind from 4 to 16 or shrink slice bounds from 4 to 2 to 1 when needed.

## Link
- [https://arxiv.org/abs/2605.21434v1](https://arxiv.org/abs/2605.21434v1)
