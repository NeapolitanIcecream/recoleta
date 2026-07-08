---
source: arxiv
url: https://arxiv.org/abs/2607.05188v1
published_at: '2026-07-06T15:08:26'
authors:
- "Andr\xE9 Silva"
- Han Tu
- Martin Monperrus
topics:
- code-intelligence
- coding-agents
- mechanistic-interpretability
- software-engineering-benchmarks
- automated-software-production
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Latent Programming Horizons in Coding Agents

## Summary
This paper finds that coding agents' residual streams encode current and future program properties during multi-step repair tasks. Linear probes can predict correctness, partial progress, regressions, and parsing signals, with future-edit signals still above chance about 25 steps ahead.

## Problem
- Coding agents read files, edit code, run tests, and revise changes, but their internal program state during this process is poorly understood.
- Prior probing work mainly studied single-step code generation with the full program in context; this paper studies iterative agents working on partly observed real repositories.
- The problem matters because internal signals about correctness, regressions, and future edits could support better debugging, monitoring, and interpretability for coding agents.

## Approach
- The authors run mini-swe-agent v2.2.8 with Laguna-XS.2 and Qwen3.6-35B-A3B on SWE-Bench-Verified and SWE-Bench-Pro.
- They collect hidden states from the residual stream every 5 tokens across agent trajectories, using layers 1, 11, 21, 31, and 40.
- They label each program version after edits for four binary properties: well-formedness, full correctness, partial correctness, and regression.
- They train logistic-regression probes on frozen hidden states to predict current labels at k=0 and future labels at k steps ahead, with k swept up to 50.
- They test shuffled-label controls and cross-benchmark transfer to check whether probes read signal from the model state rather than memorizing task artifacts.

## Results
- The dataset contains 22,714 trajectories over 1,231 tasks, 79,480 code edits, 22.4M hidden-state vectors, and a median trajectory length of 52 steps.
- Current-program probes decode all four properties above the 0.50 random baseline; reported best AUC reaches 0.83 for full correctness and 0.84 for partial correctness on Qwen3.6-35B-A3B.
- Well-formedness reaches AUC up to 0.78 on SWE-Bench-Pro, while SWE-Bench-Verified well-formedness stays below 0.60 because most programs already parse or compile.
- Qwen3.6-35B-A3B gives stronger decoding than Laguna-XS.2, with about 0.10 AUC higher full-correctness and partial-correctness scores across both benchmarks.
- Cross-benchmark transfer keeps full-correctness and partial-correctness AUC at 0.63-0.78, compared with 0.71-0.84 in-distribution, a drop of 0.04-0.09.
- Future-label probes stay above chance for about 25 steps. For Laguna-XS.2 full correctness, AUC starts near 0.77 on SWE-Bench-Verified and 0.82 on SWE-Bench-Pro at k=0, falls to about 0.55 and 0.65 at k=25, and remains around 0.52 and 0.60 at k=50.

## Link
- [https://arxiv.org/abs/2607.05188v1](https://arxiv.org/abs/2607.05188v1)
