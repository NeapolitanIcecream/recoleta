---
source: arxiv
url: https://arxiv.org/abs/2606.09577v1
published_at: '2026-06-08T14:52:43'
authors:
- Yuling Shi
- Caiqi Zhang
- Yuexian Li
- Haopeng Wang
- Yeheng Chen
- Nigel Collier
- Xiaodong Gu
topics:
- code-generation
- uncertainty-estimation
- code-intelligence
- software-foundation-models
- self-generated-tests
- llm-calibration
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Code Is More Than Text: Uncertainty Estimation for Code Generation

## Summary
The paper proposes code-specific uncertainty estimation for LLM code generation. It combines token-level entropy spikes, agreement between sampled pseudo-code plans, and pass rates on self-generated tests to predict whether generated code will pass hidden tests.

## Problem
- LLM code generators can produce wrong programs that look plausible, which creates risk in IDE assistants, coding agents, and multi-step software pipelines.
- Existing uncertainty methods mostly come from natural-language generation and treat code as a token sequence, missing code properties such as single-token breakage, algorithm mismatch, and executability.
- Better uncertainty scores can route outputs to human review, trigger retries, or block low-confidence code in automated software production.

## Approach
- The lexical signal computes token entropy for a generated program and averages the Top-K most uncertain positions. The paper uses K=5, so rare high-risk token choices are not washed out by the rest of the file.
- The algorithmic signal samples N=10 natural-language solution plans, compares them with step-aware ROUGE-L, and assigns higher uncertainty when the plans disagree.
- The functional signal generates M=10 tests, runs the candidate program in a sandbox, and uses the fraction of failed self-tests as uncertainty.
- The final score rank-normalizes the three signals and combines them with fixed weights: lexical 0.2, functional 0.4, algorithmic 0.4.

## Results
- Across five code LLMs and four benchmarks, the three-axis ensemble improves average AUROC from 0.696 for the strongest NL-derived baseline to 0.776, a gain of 8.1 points.
- On Qwen3-14B, the ensemble reaches 0.800 average AUROC and 0.835 average PRAUC across APPS-Intro, APPS-Interview, HumanEval, and MBPP.
- On Qwen3-14B, Top-5 entropy reaches 0.728 average AUROC, matching the strongest multi-pass NL baseline, Consistency VR at 0.728, while costing over 3x less.
- Wall-clock time on HumanEval with Qwen3-14B is 2.29 seconds per problem for Top-K entropy, 3.06 seconds for generated tests, 6.55 seconds for pseudo-code consistency, and 7.10 seconds for Consistency VR.
- On Table 1 models, the ensemble reaches 0.770 average AUROC for DeepSeek-Coder-V2 and 0.791 for Devstral-Small-2505.
- A token split finds code-token entropy is useful while comment-token entropy is harmful: code-only AUROC is 0.716, while comment-only AUROC is 0.375.

## Link
- [https://arxiv.org/abs/2606.09577v1](https://arxiv.org/abs/2606.09577v1)
