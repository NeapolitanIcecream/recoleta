---
source: arxiv
url: https://arxiv.org/abs/2605.28527v1
published_at: '2026-05-27T14:23:29'
authors:
- Jiachen Zhang
- Junnan Nie
- Junyi Lao
- Wei Cheng
- Chenghao Liu
- Jiaxin Jiang
- Songfang Huang
topics:
- vision-language-action
- robot-foundation-models
- value-probing
- test-time-action-selection
- libero-goal
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# What Frozen VLAs Already Know About Success: A Probing Study of Value-Like Structure in Foundation Robot Policies

## Summary
Frozen VLA and visual representations contain a value-like success signal that a linear probe can read without retraining the policy. The paper shows the signal survives task/timestep controls and can improve Pi0.5 action selection on some hard LIBERO-Goal tasks.

## Problem
- VLA policies are trained to imitate actions, not to estimate reward, progress, or future task success.
- If frozen VLA features already encode success information, a robot can rank candidate actions at test time without retraining the policy or training a separate reward model.
- Simple probe results can be misleading because task identity, timestep, and dataset artifacts can correlate with success.

## Approach
- The authors build Monte Carlo outcome targets from completed trajectories: successful states get \(\gamma^{T-1-t}\) with \(\gamma=0.99\), and failed states get 0.
- They extract frozen features from Pi0.5, OpenVLA, OpenVLA-OFT, SmolVLA, DINOv2, CLIP, random projections, proprioception, and scalar nuisance features.
- They train standardized linear ridge probes to predict the value-like target, then compare demo-split and task-split performance.
- They test shortcut resistance with same-task, same-timestep matched pairs whose labels differ by at least 0.20, plus label-shuffled controls.
- They use the trained probe as a test-time selector over \(K=16\) sampled Pi0.5 action chunks, rolling out five-action prefixes in simulation and executing the selected prefix without changing policy weights.

## Results
- On LIBERO-Goal, probing uses 311,719 frame-level rows from 1,400 mixed successful and failed trajectories.
- Best task-split \(R^2\) scores are 0.5510 for Pi0.5, 0.5505 for OpenVLA-OFT, 0.5493 for OpenVLA, 0.5257 for SmolVLA, 0.5104 for DINOv2, and 0.5095 for CLIP.
- Scalar shortcuts are much weaker: progress and time-to-go each reach about \(R^2=0.03\), task one-hot is near 0, and proprioception reaches 0.1107 on the task split.
- The primary Pi0.5 same-task, same-timestep control reaches 94.22% pairwise ordering accuracy over 4,605 pairs, while the label-shuffled control is 50.05%.
- Across 10 same-step runs, mean pairwise accuracy is 92.16% and shuffle accuracy is 49.67%; no probe run drops below 89.58%.
- In online Pi0.5 selection, pooled hard-3 success is 42.44% for value-guided selection, 36.89% for random selection, and 31.11% for greedy decoding; on push-plate, success rises from 26.7% under greedy decoding to 44.3% with the probe-guided selector.

## Link
- [https://arxiv.org/abs/2605.28527v1](https://arxiv.org/abs/2605.28527v1)
