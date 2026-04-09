---
source: arxiv
url: http://arxiv.org/abs/2603.28301v1
published_at: '2026-03-30T11:27:34'
authors:
- Chanyoung Kim
- Minwoo Kim
- Minseok Kang
- Hyunwoo Kim
- Dahuin Jung
topics:
- vision-language-action
- robot-benchmark
- paraphrase-robustness
- instruction-following
- language-grounding
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models

## Summary
LIBERO-Para is a benchmark for testing whether vision-language-action models can follow paraphrased robot instructions after limited fine-tuning. The paper shows that current VLA models often fail on meaning-preserving rewrites and introduces PRIDE to measure robustness by paraphrase difficulty, not only binary success.

## Problem
- Current VLA benchmarks such as LIBERO usually train and test on the same instruction wording, so they miss failures caused by paraphrased commands.
- In real robot deployment, fine-tuning data is limited, which can make models memorize surface phrasing instead of grounding the instruction semantics.
- Binary success rate hides whether a model handles hard paraphrases or only easy ones, so it gives a weak picture of language robustness.

## Approach
- The paper builds **LIBERO-Para**, a controlled benchmark on top of LIBERO-Goal that changes only the instruction text while keeping tasks and environments fixed.
- It separates paraphrases along two axes: **action expression** and **object reference**, with 43 variation types and about 100 samples per type, for a total of **4,092 paraphrased instructions**.
- Action variation includes lexical, structural, and pragmatic changes; object variation focuses on lexical changes in noun phrases such as synonym-like substitutions and additions.
- The paper introduces **PRIDE**, which scores robustness by combining: (1) keyword similarity over action/object content words using Sentence-BERT embeddings, and (2) structural similarity using dependency-tree edit distance.
- PRIDE gives credit only when the task succeeds, weighted by paraphrase deviation, so success on harder paraphrases counts more than success on easy ones.

## Results
- Across **7 VLA configurations** spanning **0.6B to 7.5B** parameters, success drops by **22.8 to 51.9 percentage points** from LIBERO-Goal to LIBERO-Para.
- Example drops: **Xiaomi-Robotics-0** goes from **98.8%** to **76.0%** (**-22.8 pp**); **VLA-Adapter** goes from **98.2%** to **46.3%** (**-51.9 pp**); **OpenVLA-OFT_goal** goes from **97.9%** to **64.7%** (**-33.2 pp**).
- PRIDE is consistently below raw success rate, showing that binary SR overstates robustness by **8.4% to 22.0%** depending on the model. For example, **VLA-Adapter** has **46.3 SR** vs **36.1 PRIDE**; **pi_0.5** has **71.4 SR** vs **65.4 PRIDE**.
- Object paraphrasing is the main failure source: replacing object names with common alternatives causes drops from **19.8 pp** to **51.0 pp** across models, larger than many action-side changes.
- Harder action forms also hurt performance: average success along the action axis falls from **82.7%** for explicit forms to about **48%** for indirect forms such as **Question** and **Hint**.
- The paper claims **80% to 96%** of failures come from planning-level trajectory divergence rather than execution errors, which suggests paraphrases often break task identification early.

## Link
- [http://arxiv.org/abs/2603.28301v1](http://arxiv.org/abs/2603.28301v1)
