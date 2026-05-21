---
source: arxiv
url: https://arxiv.org/abs/2605.08732v1
published_at: '2026-05-09T06:36:23'
authors:
- Hoang Nguyen
- Xiaohao Xu
- Xiaonan Huang
topics:
- world-model-planning
- inverse-dynamics
- goal-conditioned-control
- latent-representations
- amortized-planning
- robot-manipulation
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Latent Geometry Beyond Search: Amortizing Planning in World Models

## Summary
GC-IDM replaces online trajectory search in a pretrained LeWorldModel with a small goal-conditioned inverse dynamics model. It keeps success rates near or above CEM while cutting per-decision planning cost by about 100 to 130 times.

## Problem
- Vision-based world models can predict latent futures cheaply, but choosing actions often still needs expensive online search.
- In LeWorldModel, default CEM uses 9,000 candidate rollouts and 45,000 predictor forward passes for each planning step, so action selection dominates compute.
- The paper asks whether a smooth, action-sensitive latent space can make goal-directed control a supervised inverse-dynamics problem.

## Approach
- The method freezes a pretrained LeWorldModel encoder and trains GC-IDM on the same offline trajectories used for the world model.
- Each training example uses the current latent state, a future goal latent state, the sampled horizon, and the dataset action at the current step.
- GC-IDM is a 3-layer MLP with hidden size 512, LayerNorm, GELU, 10% dropout, and horizon conditioning through a 64-dimensional sinusoidal encoding plus AdaLN-Zero.
- At test time, the controller encodes the goal once, re-encodes the current observation after every action, and predicts the next action with one forward pass. It performs no rollout search.
- The inverse model has about 1.5M parameters and takes about 20 minutes per environment to train on one GPU.

## Results
- Across Two-Room, Push-T, OGBench-Cube, and Reacher, GC-IDM matches or beats CEM in 7 of 8 environment-protocol settings.
- Planning cost drops by 100 to 130 times per decision. CEM uses a 10.8M-parameter predictor with 45,000 calls per plan, while GC-IDM adds a 1.5M-parameter MLP with 0 predictor calls.
- At n=200, Two-Room success is 100.0% ± 0.0 for GC-IDM versus 84.0% ± 2.8 for CEM, with 104x planning speedup.
- At n=200, OGBench-Cube success is 98.7% ± 0.6 versus 67.0% ± 2.1, with 130x planning speedup.
- At n=200, Reacher success is 99.7% ± 0.3 versus 70.3% ± 4.3, with 110x planning speedup.
- Push-T is the closest case: at n=50, GC-IDM gets 84.7% ± 5.0 versus CEM at 89.3% ± 6.4; at n=200, GC-IDM gets 84.2% ± 2.8 versus CEM at 82.5% ± 1.3.

## Link
- [https://arxiv.org/abs/2605.08732v1](https://arxiv.org/abs/2605.08732v1)
