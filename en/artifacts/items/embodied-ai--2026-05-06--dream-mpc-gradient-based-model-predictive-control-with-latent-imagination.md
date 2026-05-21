---
source: arxiv
url: https://arxiv.org/abs/2605.04568v1
published_at: '2026-05-06T07:13:11'
authors:
- Jonathan Spieler
- Sven Behnke
topics:
- world-models
- model-predictive-control
- gradient-based-planning
- model-based-rl
- continuous-control
- robot-learning
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination

## Summary
Dream-MPC is a gradient-based MPC method that plans through a learned latent world model using a policy prior, an uncertainty penalty, and action reuse. It targets faster planning for high-dimensional continuous control while improving over the base policy and, in BMPC experiments, over MPPI.

## Problem
- Sampling-based MPC methods such as CEM and MPPI often evaluate hundreds or thousands of action sequences per step, which is costly for high-dimensional control and harder to run on limited hardware.
- Pure policy networks are cheaper at inference time, but they can generalize poorly because they do no online planning at test time.
- Prior gradient-based planners with learned models often underperformed gradient-free planners, partly because gradients can drive actions into model-error regions.

## Approach
- Dream-MPC samples a small number of candidate action sequences from a stochastic policy prior, then rolls them out in a learned latent world model.
- It optimizes each action sequence by gradient ascent on predicted return, using predicted rewards and a terminal Q-value.
- It penalizes epistemic uncertainty estimated from an ensemble of Q-functions, so plans with high model uncertainty get lower objective values.
- It reuses previously optimized actions across MPC steps with a reuse coefficient, which carries optimization work forward in the receding-horizon loop.
- The reported default planner uses 5 candidates, 1 gradient step, horizon 3, step size 0.1, reuse coefficient 0.1, and uncertainty coefficient 0.01.

## Results
- On 24 continuous-control tasks from DeepMind Control Suite, HumanoidBench, and Meta-World, Dream-MPC with BMPC improves IQM normalized score by 26.7% and mean normalized score by 20.5% over BMPC.
- With TD-MPC2 as the base model, Dream-MPC improves over the TD-MPC2 policy-only baseline by 144.7% in IQM and 43.4% in mean score, but it does not consistently match TD-MPC2 with MPPI.
- The planner uses 15 world-model evaluations per time step in the given setup, compared with 9216 for MPPI under the cited TD-MPC2 configuration.
- Mean domain scores for Dream-MPC on TD-MPC2 are 433 ± 259 on DMControl, 379 ± 897 on HumanoidBench, and 0.62 ± 0.31 on Meta-World; TD-MPC2 with MPPI scores 657 ± 225, 761 ± 1617, and 0.67 ± 0.33 on the same domains.
- On 6 image-observation DMControl tasks with BMPC, Dream-MPC scores 725 ± 141 on Cartpole Swingup Sparse, 643 ± 9 on Cheetah Run, 275 ± 3 on Hopper Hop, 435 ± 76 on Quadruped Walk, and 762 ± 6 on Walker Run; it is roughly tied on Acrobot Swingup at 288 ± 31 versus BMPC policy-only 292 ± 18.
- The paper claims Dream-MPC can outperform gradient-free MPC when paired with a strong policy prior from BMPC, while using far fewer model evaluations than MPPI.

## Link
- [https://arxiv.org/abs/2605.04568v1](https://arxiv.org/abs/2605.04568v1)
