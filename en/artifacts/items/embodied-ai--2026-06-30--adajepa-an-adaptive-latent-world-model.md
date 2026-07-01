---
source: arxiv
url: https://arxiv.org/abs/2606.32026v1
published_at: '2026-06-30T17:53:48'
authors:
- Ying Wang
- Oumayma Bounou
- Yann LeCun
- Mengye Ren
topics:
- latent-world-model
- test-time-adaptation
- model-predictive-control
- jepa
- robot-planning
- distribution-shift
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# AdaJEPA: An Adaptive Latent World Model

## Summary
AdaJEPA adapts a JEPA latent world model during MPC using the transition just observed after each executed action. The paper reports higher goal-reaching success under shape, visual, dynamics, and maze-layout shifts with one gradient step per replan.

## Problem
- Frozen latent world models can give MPC wrong rollouts after visual or dynamics shifts, so the planner optimizes actions that fail in the real environment.
- This matters for robot planning because small one-step prediction errors can compound across the MPC horizon and lower goal-reaching success.
- The paper targets adaptation without reward labels, expert demonstrations, or a separate target-domain data collection phase.

## Approach
- AdaJEPA runs a plan, act, adapt, replan loop inside MPC.
- After executing the first action or action chunk, it stores the observed transition `(o_t, a_t, o_{t+1})` in a small online buffer.
- It applies the same JEPA latent prediction loss used in training: predict the next latent state from the current latent state and action, then compare it to the encoded next observation with stop-gradient on the target.
- At test time it updates only a small parameter subset, usually final encoder and predictor layers, then immediately uses the updated model for the next MPC plan.
- The default experiment uses one gradient step per MPC replan, a buffer of the 5 most recent transitions, a maximum of 20 MPC steps, and 50 episodes across each of 3 test-data seeds.

## Results
- On PushObj in-distribution training shapes, the paper reports the largest gain as over 20% relative to the frozen model when adapting to the current shape.
- On unseen PushObj shapes, the text says AdaJEPA nearly doubles planning success versus the frozen model; exact percentages are not provided in the excerpt.
- On PointMaze-Medium with low-mass dynamics, `predlast + enclast` improves GD success from 77.3 ± 8.2 to 80.0 ± 3.3 and CEM success from 82.0 ± 2.8 to 86.7 ± 2.5.
- On PointMaze-Medium with high damping, `predfirst + enclast` improves CEM success from 76.0 ± 2.8 to 82.0 ± 3.3, while GD rises from 77.3 ± 5.0 to 78.7 ± 4.7.
- On unseen PointMaze layouts, `predfirst + enclast` improves GD success from 53.3 ± 8.2 to 78.7 ± 5.0 and CEM success from 49.3 ± 6.2 to 70.7 ± 3.8.
- Latency increases are small in the reported table: for the global-feature Temporal Straightening world model, GD time changes from 3.14 s to 3.17 s and CEM time from 0.24 s to 0.27 s; for the spatial-feature variant, GD changes from 3.37 s to 3.38 s and CEM from 5.37 s to 5.39 s.

## Link
- [https://arxiv.org/abs/2606.32026v1](https://arxiv.org/abs/2606.32026v1)
