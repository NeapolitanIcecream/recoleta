---
source: arxiv
url: https://arxiv.org/abs/2605.29054v1
published_at: '2026-05-27T19:57:15'
authors:
- Linxin Song
- Jiefeng Chen
- Yue Huang
- Bhavana Dalvi Mishra
- Chi Wang
- Jieyu Zhao
- Jinsung Yoon
- Tomas Pfister
topics:
- codebase-conversion
- code-agents
- code-intelligence
- software-engineering-benchmarks
- pytorch-to-jax
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Converted, Not Equivalent: Benchmarking Codebase Conversion via Observational Equivalence

## Summary
T2J-Bench tests whether PyTorch training codebases converted to JAX preserve observable training behavior beyond simple execution. Across 355 blind attempts, top systems still pass under 30% at pass@1, which shows large gaps in current coding agents.

## Problem
- Coding agents often accept conversions that run locally but break the training behavior users need, such as gradients, optimizer updates, reward terms, or short training traces.
- Prior conversion benchmarks often score final outcomes or shallow execution checks, which can miss semantic drift inside a training pipeline.
- This matters for software modernization because a converted ML codebase can appear usable while producing different training dynamics.

## Approach
- The paper introduces T2J-Bench, a benchmark for converting full PyTorch training codebases to JAX.
- Each task uses a fixed equivalence contract derived from the source codebase, with bounded configs for seed, precision, small datasets, batch size, and replay steps.
- The verifier runs three ordered stages: Spec checks interfaces and schemas; Numeric checks outputs, losses, gradients, and method-specific tensors; Behavioral checks short training dynamics under fixed seeds.
- The dataset covers 45 datapoints: 15 model families across SFT, DPO, and PPO.
- Agents receive a frozen minimum constraint prompt that defines the public training interface without revealing evaluator internals.

## Results
- On T2J-Bench, the best controlled model at pass@1 is Claude Opus 4.7 with 28.9% overall pass rate; the best native coding agent at pass@1 is Claude Code with Opus 4.7 at 26.7%.
- At pass@3, Claude Opus 4.7 under the shared scaffold reaches 46.7% overall, while Claude Code with Opus 4.7 reaches 42.2%; more than half of tasks remain unsolved.
- Spec pass rates are much higher than end-to-end pass rates: Claude Code with Opus 4.7 reaches 91.1% Spec at pass@1 but only 26.7% overall after Numeric and Behavioral checks.
- Numeric checks are a major failure point: for the strongest controlled model at pass@1, Spec is 84.4%, Numeric conditional on Spec is 39.5%, Behavioral conditional on Numeric is 86.7%, and overall is 28.9%.
- Token spend does not scale cleanly with success: a 4.7x spread in mean tokens per attempt yields only a 2.2x spread in overall pass rate.
- All evaluated systems overestimate their own success by 66.6 to 97.8 percentage points relative to the fixed verifier.

## Link
- [https://arxiv.org/abs/2605.29054v1](https://arxiv.org/abs/2605.29054v1)
