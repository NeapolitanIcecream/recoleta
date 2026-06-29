---
source: arxiv
url: https://arxiv.org/abs/2605.27817v1
published_at: '2026-05-27T01:21:58'
authors:
- Sizhe Lester Li
- Evan Kim
- Xingjian Bai
- Tong Zhao
- Tao Pang
- Max Simchowitz
- Vincent Sitzmann
topics:
- video-world-models
- inverse-dynamics
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Turning Video Models into Generalist Robot Policies

## Summary
VERA turns a 14B video generative model into a closed-loop robot policy by keeping planning in video space and adding a robot-specific Jacobian inverse dynamics model. The paper claims this cuts the need for paired video-action-text training data while supporting Panda-arm manipulation and 16-DoF Allegro-hand cube reorientation.

## Problem
- Generalist robot policies often need action-labeled data tied to each robot body, and web-scale robot action data does not exist.
- Video models can predict what task success should look like, but robots need joint or end-effector commands, so the missing step is reliable video-to-action translation.
- Direct inverse dynamics models can fail with limited action data and lose accuracy as action dimensionality grows, which hurts high-DoF robots such as dexterous hands.

## Approach
- Use an action-free video planner that predicts future robot video frames from observation history and a goal, usually text.
- Train a separate Jacobian inverse dynamics model for each robot embodiment.
- The J-IDM predicts a dense image-space Jacobian: for each pixel, it estimates how each action dimension would move that pixel.
- At test time, optical flow between generated frames is inverted through the learned Jacobian to recover robot actions.
- Execute only a short prefix of the generated plan, observe the new state, then replan in closed loop.

## Results
- In simulation, J-IDM closed-loop success beats a UniPi-style direct IDM on all reported tasks: Allegro-Sim 70.0% vs 0.0%, Panda-Sim 94.0% vs 0.0%, and PushT-Sim 92.5% vs 74.4%.
- Action reconstruction MSE is lower for J-IDM on 3 of 4 reported settings: Allegro-Sim 0.031 vs 0.044/0.063, PushT-Sim 0.046 vs 0.059/0.071, and 5-joint fingers 0.017 vs 0.030/0.047; Panda-Sim is 0.19 vs best baseline 0.09.
- In a controlled 2D finger study at 5 DoF, the paper reports about 2× better data efficiency for J-IDM than direct IDM baselines.
- On real Panda basic instruction tasks, DreamZero reports 90% success, VERA 60%, and π0.5 30%.
- The paper claims zero-shot deployment on a real Panda arm in unseen scenes with varied cameras and prompts, plus RGB-only real Allegro-hand cube reorientation with 16 DoF.
- The same video planner is paired with different embodiment-specific J-IDMs for Panda and Allegro robots, supporting the cross-embodiment claim.

## Link
- [https://arxiv.org/abs/2605.27817v1](https://arxiv.org/abs/2605.27817v1)
