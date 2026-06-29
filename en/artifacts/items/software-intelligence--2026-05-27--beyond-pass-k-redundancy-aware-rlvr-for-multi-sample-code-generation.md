---
source: arxiv
url: https://arxiv.org/abs/2605.28022v1
published_at: '2026-05-27T06:26:52'
authors:
- Le Bronnec Florian
- Alexandre Verine
- Rio Yokota
- Benjamin Negrevergne
topics:
- code-generation
- rlvr
- pass-at-k
- code-diversity
- software-foundation-models
- program-similarity
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Beyond pass@k: Redundancy-Aware RLVR for Multi-Sample Code Generation

## Summary
The paper claims that multi-sample code generation needs to reduce near-duplicate programs, not only raise single-sample correctness. It adds a JPlag-based anti-redundancy reward to RLVR and reports better Pass@k results across code benchmarks.

## Problem
- Pass@k rewards a model when one of k sampled programs passes tests, but it does not measure whether the samples cover distinct implementations.
- Correctness-only RLVR can make models repeat similar correct programs, which wastes a finite sampling budget when users ask for many candidates.
- This matters for code intelligence systems because multi-sample generation is common in benchmark evaluation and practical program synthesis workflows.

## Approach
- The paper measures implementation redundancy with JPlag, a code-similarity tool that is less affected by variable renaming, formatting, and comments than lexical overlap.
- It defines JPlag diversity as 1 minus mean pairwise JPlag similarity within a sampled group.
- It compares correctness-only RLVR, Pass@k-RLVR, PKPO, and a new JPlag-RLVR objective on Qwen3-4B, Qwen3-8B, and Olmo3-7B.
- JPlag-RLVR keeps the executable correctness reward and adds a group-level anti-redundancy reward, with leave-one-out advantages that reward samples that make the group less redundant.
- Evaluation uses 200 sampled generations per prompt on MBPP, Code-Contest, and TACO-Cobalt.

## Results
- Across 2745 prompt-level comparisons, correctness-only Base-RLVR decreased JPlag diversity in 57.2% of cases and had mean JDiv change of -0.046, while Pass@k-RLVR increased JPlag diversity in 66.9% of cases with mean JDiv change of +0.123.
- In the same aggregate comparison, JPlag-RLVR increased JPlag diversity in 77.4% of cases, with mean JDiv change of +0.298. It also had mean Pass@1, Pass@10, and Pass@100 changes of +16.4, +19.7, and +17.3.
- On Qwen3-4B MBPP, JPlag-RLVR reached Pass@1 93.2, Pass@10 98.9, Pass@100 99.3, and JDiv 0.822. Base-RLVR scored 72.4, 82.4, 86.8, and 0.301 on the same metrics.
- On Qwen3-8B MBPP, JPlag-RLVR reached Pass@10 98.5 and Pass@100 99.2, compared with Base-RLVR at 88.0 and 90.8 and PKPO at 97.1 and 99.0.
- On Qwen3-8B TACO, JPlag-RLVR reached Pass@10 55.5 and Pass@100 68.7, compared with Base-RLVR at 48.2 and 58.5 and PKPO at 51.0 and 64.7.
- The paper claims the JPlag reward often matches or beats specialized Pass@k-aware objectives while also producing less redundant code samples.

## Link
- [https://arxiv.org/abs/2605.28022v1](https://arxiv.org/abs/2605.28022v1)
