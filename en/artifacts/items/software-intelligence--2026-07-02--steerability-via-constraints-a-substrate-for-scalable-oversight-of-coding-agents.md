---
source: arxiv
url: https://arxiv.org/abs/2607.02389v1
published_at: '2026-07-02T16:24:47'
authors:
- Thomas Winninger
topics:
- coding-agents
- code-review
- software-security
- static-analysis
- agent-oversight
- developer-tools
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Steerability via constraints: a substrate for scalable oversight of coding agents

## Summary
The paper claims that coding agents are easier to review when the codebase enforces contracts through tools instead of relying on prompts or long guidance files. In a small Python backdoor test, constraints plus a 200-line documentation CLI raised Gemma 4 e4b reviewer recall from 54.5% to 90.9%.

## Problem
- Coding agents can write large amounts of code, but human or trusted-model review does not scale when the codebase exceeds the reviewer’s usable context.
- Unconstrained agents create security risk and codebase drift because prompts and prose rules can be ignored or forgotten during long tasks.
- The paper matters for automated software production because it targets the review bottleneck rather than only improving code generation.

## Approach
- The main mechanism is to move rules into enforceable codebase constraints: ruff, pyrefly, beartype, pydantic strict mode, jaxtyping shapes, frozen dataclasses, Literal discriminators, and a pure `core/` versus impure `runners/` split.
- Invariants live near the code in module docstrings, so a reviewer can inspect a function with its local contract instead of reading a full repository guide.
- A 200-line `docs` CLI built on griffe exposes module APIs, symbol signatures, dataclass fields, docstrings, and invariant blocks for narrow per-function review.
- The system sketch also adds a VM, network egress allowlist, and an inference proxy that can inspect model traffic, although the paper only evaluates the substrate and `docs` parts.

## Results
- On a synthetic 500-LoC Python LM-eval codebase with 11 hand-inserted backdoors, unconstrained code with no tools caught 6/11 backdoors: 54.5% recall and 100.0% precision.
- Adding only the `docs` CLI to the unconstrained code caught 9/11 backdoors: 81.8% recall and 100.0% precision.
- Adding only the constrained substrate caught 9/11 backdoors: 81.8% recall and 88.9% precision.
- Combining constrained substrate and `docs` caught 10/11 backdoors: 90.9% recall and 95.7% precision.
- In the best setting, Gemma 4 e4b caught L1 2/2, L2 1/2, L3 3/3, L4 1/1, and L5 3/3 backdoors.
- The authors call the experiment preliminary: it uses 11 synthetic backdoors, one small codebase, one small reviewer model, and a hand-built scoring setup.

## Link
- [https://arxiv.org/abs/2607.02389v1](https://arxiv.org/abs/2607.02389v1)
