---
source: arxiv
url: http://arxiv.org/abs/2604.19826v1
published_at: '2026-04-20T14:47:46'
authors:
- "\xC9ric Jacopin"
topics:
- code-generation
- testing
- foundation-models
- mechanistic-interpretability
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation

## Summary
The paper claims that test placement changes code generation quality for AI coding models. Tests embedded next to the code, such as Python doctests, lead to much better preservation and high correctness than separated test blocks in Rust.

## Problem
- The paper studies whether test syntax structure changes how foundation models generate code, especially whether they keep prompt-provided tests and produce code that passes them.
- This matters for AI-assisted development because teams now ask models to generate implementation and tests together, so test organization can affect code quality, CI behavior, and model evaluation.
- Prior code benchmarks focus on correctness, but they usually do not measure whether models preserve provided tests or whether preservation and correctness move together.

## Approach
- The authors run a large empirical study with 830+ generated files, 12 models, and 3 providers on one non-trivial task: implementing a d-ary heap.
- They compare inline tests in Python doctest form against separated Rust `#[test]` blocks, using repeated runs at temperature 0.
- They evaluate with SEGA, a three-part scheme: **Determinism** (% identical outputs across runs), **Preservation** (% prompt tests kept in the output), and **Correctness** (% tests passing).
- They add mechanistic analysis on 7 open models, including 6 transformers and RWKV-6, to measure whether test markers attend to function tokens more strongly in inline syntax than in separated syntax.
- They use knockout and steering experiments to test whether those internal signals causally affect behavior.

## Results
- In the Python baseline where models generate their own doctests, all 9 tested models reached **100% preservation** and **100% correctness**; determinism still varied from **0%** for Mistral Medium to **100%** for several Claude models.
- With prompt-provided inline Python doctests, preservation was **100%** for all models except **Claude 3.5 Haiku**, which dropped to **0% preservation** by stripping all doctests. Correctness stayed high at **92–97%** in one setup with 64 tests and **98.6–99%** in a refined 73-test setup.
- With separated Rust `#[test]` blocks, model behavior split sharply: **Haiku 4.5, Sonnet 4/4.5, and Opus 4.6** achieved **100% preservation** and **100% pass rate**, while **Opus 4/4.1/4.5** had **0% preservation** because they suppressed all tests, even though the generated Rust code still compiled and was described as functionally correct.
- **Haiku 3** failed badly on Rust with **0% preservation**, no compilation, and **0% pass rate**. **Mistral Medium** preserved all 28 Rust tests across 50 runs, but only **62%** of runs compiled and passed.
- Mechanistic analysis on 7 open architectures found that inline Python test markers received **2.8x to 4.4x** stronger attention than Rust test markers in **5 of 7 models**; example ratios include **3.51x** for Qwen2.5-Coder-7B, **4.35x** for CodeGemma-7B, and **2.96x** for RWKV-6, with reported **p < 0.0002**.
- The paper also reports that **temperature 0 does not ensure determinism**: examples include **0%** determinism for Mistral Medium, **52%** for Devstral-2512, and **30–64%** for Claude Opus 4.6, while some models remained at **100%**.

## Link
- [http://arxiv.org/abs/2604.19826v1](http://arxiv.org/abs/2604.19826v1)
