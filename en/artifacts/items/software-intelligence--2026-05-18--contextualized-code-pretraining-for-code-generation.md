---
source: arxiv
url: https://arxiv.org/abs/2605.17957v1
published_at: '2026-05-18T07:12:14'
authors:
- Chen Liu
- Qingyuan Liang
- Hanwen Zhang
- Zeyu Sun
- Yakun Zhang
- Lu Zhang
topics:
- code-generation
- code-pretraining
- caller-context
- repository-level-code
- static-analysis
- code-benchmarks
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Contextualized Code Pretraining for Code Generation

## Summary
CallerGen trains code models to generate missing Python functions using the caller code that already invokes them. The paper claims this caller-conditioned pretraining improves pass@1 on real-repository generation tasks, especially for small models.

## Problem
- Real projects often need a missing function implemented after caller code already exists, so the call site can reveal expected inputs, return shape, errors, and side effects.
- Common code models are trained mainly on code or natural-language descriptions, so they may ignore caller-side usage when the function signature is under-specified.
- Retrieval-based repository methods can fail when similar examples do not exist or are not retrieved, which matters for new modules, small repositories, and early-stage code.

## Approach
- The method extracts caller-callee pairs from 800 Python GitHub repositories using AST-based static analysis, symbol tables, import alias resolution, and a function-level call graph.
- Each training sample pairs a target callee with its direct caller function bodies and optional docstring, then asks the model to generate the missing callee implementation.
- CallerGen is trained at 60M, 220M, and 0.5B parameter scales with an invocation-aware objective.
- The paper applies the idea to both encoder-decoder CodeT5-style models and decoder-only Qwen2.5-Coder-style models.
- CallerEval is introduced as a benchmark of real caller-callee cases with execution-based tests tied to caller-constrained behavior.

## Results
- On CallerEval, CallerGen-220M reaches 16.58% pass@1 and CallerGen-0.5B reaches 22.81% pass@1.
- On CoderEval with calling contexts, CallerGen-220M reports 21.22% pass@1, compared with 8.78% for CodeGen-350M.
- CallerGen-0.5B reaches 22.81% pass@1 on CallerEval and is reported to beat Qwen2.5-Coder-32B-Instruct by nearly 2 percentage points.
- Without calling contexts, CallerGen-220M reaches 10.00% pass@1 from function headers on CoderEval, compared with 7.39% for CodeGen-350M.
- The evaluation compares CallerGen with nine open-source code models across CoderEval and CallerEval.

## Link
- [https://arxiv.org/abs/2605.17957v1](https://arxiv.org/abs/2605.17957v1)
