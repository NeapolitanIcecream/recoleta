---
source: arxiv
url: https://arxiv.org/abs/2605.07278v1
published_at: '2026-05-08T05:43:33'
authors:
- Wenyuan Li
- Guang Li
- Keisuke Maeda
- Takahiro Ogawa
- Miki Haseyama
topics:
- latent-world-models
- goal-conditioned-control
- reachability-learning
- latent-planning
- pixel-control
- robot-manipulation
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Predictive but Not Plannable: RC-aux for Latent World Models

## Summary
A latent world model can predict short horizons accurately while still giving a latent space that misleads planning. RC-aux adds multi-step rollout training and finite-budget reachability supervision so latent distances better match what an agent can reach within its action budget.

## Problem
- Goal-conditioned pixel control often plans by rolling out actions in latent space and choosing trajectories whose terminal latent is close to the goal latent.
- One-step or short-horizon prediction loss can produce latent shortcuts: states look close in Euclidean latent distance even when no feasible finite-horizon action sequence reaches them.
- This matters because planners can select action sequences that score well in latent space and fail in the environment, especially in obstacle or long-horizon tasks.

## Approach
- RC-aux keeps the LeWorldModel backbone and changes the training signals rather than adding a new world-model architecture.
- It replaces local one-step supervision with multi-horizon open-loop prediction: predicted latents are fed back into the dynamics model and matched to encoded future latents across K steps.
- It trains a reachability head R_phi(z, z', h) that predicts whether target latent z' is reachable from source latent z within budget h.
- Reachability labels use same-trajectory positives, temporal hard negatives where the target appears later than the sampled budget, cross-trajectory batch negatives, and predicted-rollout pairs.
- At test time, an optional reachability-aware planner discounts the base terminal latent cost when an intermediate predicted state can reach the goal within the remaining horizon; lambda_plan = 0 recovers the base planner.

## Results
- On five pixel-based goal-conditioned control tasks, RC-aux improves 4 of 5 matched LeWM-family comparisons: TwoRoom +9.2, Reacher +4.4, Push-T -0.4, Wall +33.2, Cube +3.2 success-rate points.
- Wall shows the largest gain: LeWM gets 50.4 ± 6.5 success, while RC-aux gets 83.6 ± 3.6.
- TwoRoom improves from the LeWM-family control at 88.8 ± 3.0 to 98.0 ± 1.4 with RC-aux.
- Reacher improves from 82.8 ± 7.2 to 87.2 ± 6.4, and Cube improves from 72.8 ± 5.2 to 76.0 ± 7.5.
- Planner ablations show that training alone helps on Wall: control 50.4 ± 6.5, RC-aux with lambda_plan = 0 reaches 72.4 ± 3.6, and full RC-aux reaches 83.6 ± 3.6.

## Link
- [https://arxiv.org/abs/2605.07278v1](https://arxiv.org/abs/2605.07278v1)
