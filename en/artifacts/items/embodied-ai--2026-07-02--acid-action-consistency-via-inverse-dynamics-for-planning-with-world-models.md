---
source: arxiv
url: https://arxiv.org/abs/2607.02403v1
published_at: '2026-07-02T16:38:10'
authors:
- Gawon Seo
- Dongwon Kim
- Suha Kwak
topics:
- world-model
- decision-time-planning
- inverse-dynamics
- embodied-control
- robot-manipulation
- visual-navigation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# ACID: Action Consistency via Inverse Dynamics for Planning with World Models

## Summary
ACID adds an inverse-dynamics consistency check to decision-time planning with action-conditioned world models. It improves goal-conditioned control across four world models and six tasks without retraining the world model.

## Problem
- Standard MPC/CEM planning with a world model scores a candidate action sequence mainly by the predicted final state's distance to the goal.
- This misses whether each predicted transition can be produced by the action that conditioned it, so the planner can choose action sequences whose imagined rollout reaches the goal while the real rollout drifts away.
- The issue matters for robot manipulation, deformable-object control, and visual navigation because execution depends on realizable intermediate transitions, not only a goal-like final prediction.

## Approach
- ACID uses an inverse dynamics model, `G_phi`, as a decision-time verifier: given two consecutive predicted latents, it predicts the action that would explain that transition.
- For each predicted step, it compares the original sampled action `a_t` with the inferred action `G_phi(z_t, z_{t+1})` using squared error.
- It averages this per-step error over the planning horizon as an action consistency cost and adds it to the normal goal cost.
- The weight is adaptive: `w_a = lambda * sigma_g / sigma_a`, where the sigmas are the across-candidate standard deviations of the goal cost and consistency cost at the current CEM iteration.
- The method changes only the planning cost, so it can be used with latent JEPA-style predictors and pixel/video world models.

## Results
- On Le-WM, success rate improved from 70.0% to 74.0% on Cube, 76.0% to 88.0% on Reacher, and 96.0% to 100.0% on PushT.
- On PLDM, success rate improved from 58.0% to 68.0% on Cube, 76.0% to 90.0% on Reacher, and 72.0% to 76.0% on PushT.
- On DINO-WM for deformable manipulation, Chamfer distance dropped from 1.38 to 0.56 on Rope and from 0.49 to 0.30 on Granular.
- On NWM with CompACT for visual navigation, ATE dropped from 1.3141 to 1.2835, a 2.3% reduction, and translational RPE dropped from 0.3831 to 0.3773, a 1.5% reduction.
- In a Reacher CEM budget sweep with 30, 50, 150, and 300 samples, ACID beat the original planner for both Le-WM and PLDM at every tested budget; for PLDM at 50 samples, it reached 84% versus the original planner's 76% at 300 samples.
- In the Le-WM adaptive-weight ablation, ACID had a total success-rate gain of +20.0 points across Cube, PushT, and Reacher, while the best tested constant weight reached +14.0 points and some constants reduced total performance.

## Link
- [https://arxiv.org/abs/2607.02403v1](https://arxiv.org/abs/2607.02403v1)
