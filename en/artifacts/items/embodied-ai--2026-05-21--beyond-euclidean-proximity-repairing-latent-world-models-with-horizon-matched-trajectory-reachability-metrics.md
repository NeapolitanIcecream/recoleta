---
source: arxiv
url: https://arxiv.org/abs/2605.22164v1
published_at: '2026-05-21T08:34:57'
authors:
- Liangyu Li
- Shengzhi Wang
- Qingwen Liu
topics:
- latent-world-models
- model-predictive-control
- reachability-metrics
- trajectory-data
- robot-planning
- continuous-manipulation
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Beyond Euclidean Proximity: Repairing Latent World Models with Horizon-Matched Trajectory Reachability Metrics

## Summary
TRM is a post-hoc terminal cost for fixed latent world-model MPC that ranks candidate endpoints with learned trajectory reachability instead of raw latent MSE. The paper claims large gains on hard TwoRoom because the latent state contains position, while the planner's Euclidean cost gives that signal too little weight.

## Problem
- Latent MPC often scores action candidates by Euclidean distance between the predicted terminal latent and the goal latent, which can rank blocked or unreachable endpoints ahead of feasible routes.
- This matters for control because a world model can encode the needed state while the planner still chooses bad actions through a poor terminal metric.
- The failure is shown in TwoRoom: LeWM's latent encodes XY position with linear-probe R² = 0.998, yet raw latent MSE gives only 7.0% mean success on the hard n100 manifest.

## Approach
- TRM trains a small pairwise head m_phi(z_i, z_j) on encoded pairs from logged trajectories.
- The target is same-episode temporal separation |t_i - t_j|, used as a simple reachability proxy: states close in time along a valid trajectory should be easier to connect.
- Pair sampling is horizon-matched: the head sees broad, balanced temporal gaps across the full episode so training matches long-horizon terminal candidate ranking.
- At planning time, the encoder, dynamics model, CEM sampler, optimizer, and evaluation manifest stay fixed; only the terminal cost changes.
- The learned metric can replace raw latent MSE in reachability-heavy tasks or be combined with standardized raw latent cost as a hybrid cost in continuous manipulation.

## Results
- On hard n100 TwoRoom with LeWM, raw latent MSE reaches 7.0% mean success, while full-horizon TRM reaches 97.0%; shuffled-label heads with the same architecture and data volume reach 0.0%.
- On the same hard n100 manifest with PLDM, raw latent MSE reaches 32.7% mean success, while full-horizon TRM reaches 84.0%; shuffled-label heads again reach 0.0%.
- Horizon matching matters: broad random full-episode coverage reaches 90.0%, balanced full-episode pairs reach 97.5%, and a short-horizon TRM with max Δ = 50 reaches 35.0% using the same 100,000-pair budget.
- Same-candidate selection audit on LeWM seed 3072 shows geodesic Spearman rising from 0.018 for raw latent MSE to 0.729 for true-label TRM; the oracle-best candidate moves from rank percentile 31.71 to 3.86.
- The XY-probe rowspace accounts for less than 1% of terminal-goal latent MSE while carrying most candidate-quality signal, which supports the claim that raw latent distance underweights control-relevant variables.
- On PushT go50/go75, the excerpt reports better SCSA ranking and selected final distance for TRM-style task-state metrics, but it does not give numeric PushT success or SCSA values in the provided text.

## Link
- [https://arxiv.org/abs/2605.22164v1](https://arxiv.org/abs/2605.22164v1)
