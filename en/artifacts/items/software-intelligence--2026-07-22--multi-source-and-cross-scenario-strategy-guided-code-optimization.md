---
source: arxiv
url: https://arxiv.org/abs/2607.20353v1
published_at: '2026-07-22T16:38:56'
authors:
- Yuwei Zhao
- Qianyu Xiao
- Ye Cui
- Yijun Yu
- Yingfei Xiong
topics:
- code-optimization
- large-language-models
- cross-scenario-transfer
- static-analysis
- software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Multi-Source and Cross-Scenario Strategy-Guided Code Optimization

## Summary
MoST is an LLM-based framework for code optimization that combines evidence from commits and technical documents, then transfers optimization strategies across programming languages and architectures. It reports more developer-equivalent patches and larger performance gains than SemOpt and Codex on historical tasks and real-world projects.

## Problem
- Existing strategy-guided optimizers mainly mine historical commits, so they cannot use strategies described in manuals, textbooks, or web documents.
- They usually generate rules only for the language and architecture represented by the source example, limiting reuse across scenarios such as C to Rust.
- The problem matters because inefficient code increases execution time, resource consumption, operational cost, and user-facing latency, while many real optimizations require source changes beyond compiler-level transformations.

## Approach
- MoST converts heterogeneous inputs into "evidence objects" containing a natural-language strategy description, a before/after code example, applicable scenario tags, and the source type.
- It uses self-balanced weighted density clustering so higher-quality but less frequent document evidence is not overwhelmed by noisy or duplicated commit evidence.
- When a strategy lacks examples for the target language or architecture, it transfers examples from other scenarios and first checks whether the strategy applies to the target.
- It generates Semgrep rules from target-scenario examples and validates each rule by requiring it to match the pre-optimization code and reject the post-optimization code before using it to guide an LLM patch.
- The implementation processed 48,440 commit-derived and 189 document-derived evidence objects, producing 356 strategy clusters, including 39 cross-scenario clusters.

## Results
- On 351 historical optimization tasks—151 C/C++, 150 Python, and 50 Rust—MoST produced 24.44%–180.00% more patches exactly matching developer patches than SemOpt.
- MoST produced 21.88%–37.50% more patches semantically equivalent to developer patches than SemOpt on the same benchmark.
- On 15 real-world projects, MoST achieved 19.72%–717.42% maximum performance improvements and 4.44%–258.17% average improvements, outperforming SemOpt and Codex.
- The generated rule inventory covered target scenarios with 730 to 9,735 Semgrep rules per scenario in the reported table, including 24–137 clusters added entirely through other-scenario evidence.
- The excerpt does not provide the detailed per-baseline scores, statistical significance values, or complete ablation results; it also notes that residual overlap with data used to construct the strategy library may remain after exact-match filtering.

## Link
- [https://arxiv.org/abs/2607.20353v1](https://arxiv.org/abs/2607.20353v1)
