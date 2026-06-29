---
source: arxiv
url: https://arxiv.org/abs/2605.20473v1
published_at: '2026-05-19T20:39:14'
authors:
- Yifeng He
- Ethan Wang
- Jicheng Wang
- Xuanxin Ouyang
- Hao Chen
topics:
- code-generation
- test-time-scaling
- differential-testing
- coverage-guided-fuzzing
- code-intelligence
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Code Generation by Differential Test Time Scaling

## Summary
DIFFCODEGEN selects one code solution from many LLM-generated candidates by fuzzing a candidate, comparing runtime behavior across candidates, and choosing the center of the largest behavior cluster. It targets practical code generation where no public tests exist and extra LLM calls for selection are too slow or costly.

## Problem
- Code models can sample many possible solutions, but a coding assistant must usually return one final program, so candidate selection matters for real use.
- Prior test-time scaling methods often assume public tests or call an LLM again to synthesize inputs or judge candidates, which adds latency and token cost.
- The paper addresses the missing-oracle case: there may be no expected outputs for new code, so the system needs a way to compare candidates without ground-truth tests.

## Approach
- DIFFCODEGEN first generates multiple code candidates from the same prompt using stochastic sampling, beam search, or 18 semantic-preserving prompt perturbations.
- It chooses one reference candidate and runs coverage-guided fuzzing to create inputs that exercise its code paths. It uses AFL++ or py-afl for script programs, and libFuzzer or Atheris for library functions.
- It executes every candidate on the fuzzed inputs and records outputs, errors, return values, exceptions, and exit codes as each program’s dynamic behavior.
- It computes pairwise behavioral distance as the fraction of shared valid inputs where two candidates produce different normalized execution results.
- It clusters candidates into 2 behavior groups with average-linkage agglomerative clustering, then returns the medoid of the larger cluster.

## Results
- The evaluation covers 4 LLMs, including open-weight and proprietary models, and reports consistent performance gains over baseline generation.
- Against state-of-the-art test-time scaling methods that do not need public tests, the paper claims competitive or better PASS@1 performance, but the excerpt does not include the exact PASS@1 values.
- On LiveCodeBench, DIFFCODEGEN reportedly uses about 20% of the execution time of prior TTS methods for locally served LLMs.
- On API-based LLMs, it reportedly uses about 5% of the time of prior TTS methods.
- It reportedly consumes about 4% of the input tokens used by previous work because candidate selection adds no extra LLM calls after initial generation.
- The differential prompting variant uses 18 prompt perturbation methods to create candidate diversity without changing the task semantics.

## Link
- [https://arxiv.org/abs/2605.20473v1](https://arxiv.org/abs/2605.20473v1)
