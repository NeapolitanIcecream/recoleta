---
source: arxiv
url: https://arxiv.org/abs/2607.14739v1
published_at: '2026-07-16T09:04:50'
authors:
- Wei Li
- Peijin Jia
- Yuan Ma
- Xuefeng Jiang
- Titong Jiang
- Sheng Sun
- Yujian Li
- Xin Wen
- Han Hong
- Zhikang Liu
- Bailin Li
- Kun Zhan
topics:
- vision-language-action
- robot-foundation-model
- visual-foresight
- motion-tracking
- generalist-robot-policy
- robot-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models

## Summary
FoMoVLA improves vision-language-action policies by combining predictions of a future visual state with sparse point trajectories that describe how task-relevant image regions move toward that state. The training-only supervision improves manipulation success and zero-shot robustness while adding only 9.4 ms median inference latency.

## Problem
- Standard VLA models react to the current image and language instruction but lack explicit spatio-temporal foresight for future scene changes and long-horizon object dynamics.
- Future-state prediction identifies where the robot should end up but does not specify the motion path; dense pixel prediction is also computationally expensive and includes static, control-irrelevant content.
- This matters for manipulation tasks that require physically constrained, continuous object interactions and reliable execution over longer horizons.

## Approach
- Add 16 learnable foresight tokens that encode the final visual feature state of an action chunk using an EMA vision teacher and a lightweight MAE decoder.
- Supervise 64 image-token-aligned grid points to predict 2D displacements, visibility, and smooth trajectories over the action horizon, using CoTracker-v3 as a frozen training-time teacher.
- Couple future-state and motion representations with an 8-head, zero-initialized future-conditioned cross-attention module, so predicted point motion is conditioned on the intended future state.
- Train these objectives jointly with the VLA's flow-matching action loss; discard auxiliary branches at inference while retaining the foresight tokens.

## Results
- On LIBERO, the full model reaches a 98.8% average success rate across Spatial, Object, Goal, and Long, exceeding the reported 98.5% of the strongest listed baseline, Spatial Forcing.
- On LIBERO-Long, FoMoVLA scores 97.6%, compared with 96.0% for Spatial Forcing; its ablations score 96.5% with the base backbone, 97.5% with future prediction, 97.8% with tracking, and 98.3% with both objectives but without FCCA.
- On zero-shot LIBERO-Plus, FoMoVLA achieves 80.5% overall across 10,030 perturbed instances, matching Abot-M0 and outperforming StarVLA by 6.4 percentage points; it scores 94.0% under language perturbations and 96.2% under background perturbations.
- The paper reports state-of-the-art performance on RoboCasa GR-1 Tabletop, but the provided excerpt does not include its quantitative results or baseline comparison values.
- Inference overhead is 9.4 ms median latency and 0.1 GB of GPU memory; the tracker and auxiliary prediction branches are removed at test time.

## Link
- [https://arxiv.org/abs/2607.14739v1](https://arxiv.org/abs/2607.14739v1)
