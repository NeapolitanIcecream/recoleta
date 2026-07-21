---
source: arxiv
url: https://arxiv.org/abs/2607.18161v1
published_at: '2026-07-20T17:06:19'
authors:
- Alex Mathai
- Shobini Iyer
- Aleksandr Nogikh
- Petros Maniatis
- Franjo Ivancic
- Junfeng Yang
- Baishakhi Ray
topics:
- code-intelligence
- automated-software-production
- coding-agents
- code-quality
- program-repair
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization

## Summary
TRIM reduces unnecessary edits in AI-generated repair patches by using the agent's repair trajectory to guide behavior-preserving minimization. Across four agent scaffolds and two benchmarks, it removes 17.8%–32.9% of CodeSlop with negligible correctness regression and about half the validation cost of Delta Debugging.

## Problem
- Coding agents often leave speculative, abandoned, and temporary edits in patches that pass tests, increasing patch size and review and maintenance effort.
- The paper defines this residual, removable functional redundancy as CodeSlop and targets it because test passing alone does not identify the smallest correct repair.

## Approach
- TRIM (Trajectory-guided Redundancy Identification and Minimization) reconstructs the agent's repair trajectory, retaining surviving edits and task-related feedback requests.
- It performs hierarchical counterfactual search: it first tests removal of edit sequences, then files, and finally individual edits.
- Each candidate removal is accepted only when execution tests still pass and the patch becomes smaller, using trajectory order to approximate dependencies and reduce the search space.

## Results
- Evaluated with CrashFixer, SWE Agent, MiniSWE Agent, and OpenHands on Live-kBench and SWE-Bench.
- Reduced CodeSlop by 17.8%–32.9% across the reported settings; the abstract reports 17.9%–32.9%.
- Achieved a 1.6×–3.1× improvement over agent-based minimization baselines, with negligible regression in correctness.
- Required roughly half the validation cost of algorithmic baselines such as Delta Debugging.
- In some cases, the minimized patch exactly matched the developer-written patch; one example reduced a three-file, five-hunk SWE-Bench patch to the human fix's single line.

## Link
- [https://arxiv.org/abs/2607.18161v1](https://arxiv.org/abs/2607.18161v1)
