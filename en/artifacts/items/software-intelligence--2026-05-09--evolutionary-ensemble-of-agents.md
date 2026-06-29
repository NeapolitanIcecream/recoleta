---
source: arxiv
url: https://arxiv.org/abs/2605.09018v2
published_at: '2026-05-09T15:56:10'
authors:
- Zongmin Yu
- Liu Yang
topics:
- code-intelligence
- coding-agents
- multi-agent-systems
- evolutionary-search
- automated-research
- operator-learning
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Evolutionary Ensemble of Agents

## Summary
EvE organizes coding agents into a live population that improves both code solvers and agent guidance during algorithm search. The paper tests it on ICON positional encoding and reports better example-count generalization than static-agent variants.

## Problem
- ICON models are trained with a fixed number of in-context examples, such as k=5, but users may want k=6 to k=10 at test time.
- The original learned positional table has no trained entries beyond the fifth example, so accuracy drops when the sequence exceeds the training limit.
- This matters because fixing the issue needs coordinated code changes across model code, training, and evaluation, which is a good target for coding-agent search.

## Approach
- EvE keeps two scored populations: solver code variants and agent guidance states.
- In each iteration, sampled agents edit identical workspaces with the same reference solvers, reference agents, and base repository.
- Each agent produces a new solver and may also revise its own guidance or skills.
- The solver is evaluated, then agents receive Elo updates based on pairwise wins from their solver outputs, so sampling favors agents that add value at the current search stage.
- New agent variants and their work logs enter the population, allowing later agents to reuse concrete successes and failures.

## Results
- The ICON task trains with k=5 examples and evaluates k=1 through k=10; k=6 through k=10 are out of distribution for sequence length.
- The search uses 15 iterations, 2 working agents per iteration, 8 reference solvers, and 4 reference agents; each candidate is trained for 2,000 steps during search.
- The benchmark uses 1D conservation laws with random cubic flux, 1,000 operator instances, and 100 initial conditions per instance; error is mean absolute error averaged over 100 spatial grid points.
- EvE discovers a rescale-then-interpolate positional encoding that maps unseen example slots back into the trained range and separates slot and role information.
- At k=10, EvE keeps error below 0.15 with 2,000 training steps and below 0.08 with 10,000 training steps; the Seed ICON positional encoding fails after k=5.
- Across two runs per condition, EvE is more stable than Static-Initial and Static-Final; one frozen best-agent run plateaus above even the worse Static-Initial run, which supports the paper's claim that agent adaptation must continue during search.

## Link
- [https://arxiv.org/abs/2605.09018v2](https://arxiv.org/abs/2605.09018v2)
