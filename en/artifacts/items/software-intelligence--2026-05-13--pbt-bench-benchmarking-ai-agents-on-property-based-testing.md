---
source: arxiv
url: https://arxiv.org/abs/2605.15229v1
published_at: '2026-05-13T18:01:05'
authors:
- Lucas Jing
- Xinqi Wang
- Liao Zhang
- Simon S. Du
topics:
- property-based-testing
- code-intelligence
- coding-agents
- llm-evaluation
- software-testing
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PBT-Bench: Benchmarking AI Agents on Property-Based Testing

## Summary
PBT-Bench tests whether coding agents can turn API documentation into Hypothesis property tests that expose semantic bugs. The paper reports a 100-problem benchmark across 40 Python libraries and finds large model and prompt differences on this skill.

## Problem
- Existing code benchmarks usually test patch writing or concrete test-case generation, so they do not isolate property-based testing.
- Property-based testing matters because the agent must infer an invariant, then generate inputs that reach the bug trigger region under random search.
- Many real bugs are poor PBT targets, so the benchmark uses curated bugs that violate documented contracts and can be detected with deterministic Hypothesis strategies.

## Approach
- PBT-Bench contains 100 curated problems across 40 real Python libraries, with 365 injected semantic bugs.
- Each problem gives the agent the buggy library, documentation, and existing tests; the bug description is withheld.
- The required output is a `pbt_test.py` file with tests, and the harness scores each test function per bug using fail-on-buggy, pass-on-fixed behavior.
- Bugs are labeled by difficulty: L1 has 87 bugs, L2 has 184, and L3 has 94.
- The evaluation runs 8 LLMs through OpenHands under 2 prompt modes, open-ended Baseline and explicit Hypothesis PBT scaffolding, with 3 runs per setting for 4,800 trajectories.

## Results
- Under the PBT prompt, bug recall ranges from 42.1% to 83.4% across models; under the Baseline prompt, it ranges from 31.4% to 76.7%.
- Claude Sonnet 4.6 has the best tabled PBT recall at 83.4% ± 3.3, with 92.7% ± 2.8 problem coverage and 67.0% ± 5.2 full-recall rate.
- PBT scaffolding gives the largest gains to weaker or mid-tier baselines: Qwen 3.6 Plus rises by 24.5 percentage points, Qwen 3.5-30B-A3B by 22.9 points, and Step 3.5 Flash by 20.3 points.
- The same scaffolding hurts some models: DeepSeek V3.2 drops by 3.2 points and Grok 4.1 Fast drops by 8.0 points versus their Baseline runs.
- The paper reports 99.5% reliable union recall across all 16 model-mode pairs, 12.7 points above the best single cell reported for that analysis at 86.8%, with only 2 of 365 bugs never reliably found by any cell.

## Link
- [https://arxiv.org/abs/2605.15229v1](https://arxiv.org/abs/2605.15229v1)
