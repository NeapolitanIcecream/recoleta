---
source: arxiv
url: https://arxiv.org/abs/2605.20752v1
published_at: '2026-05-20T05:51:30'
authors:
- Zijian Zhang
- Yuqing Jiang
- Qian Cheng
- Si Liu
- Ding Zhao
- Ping Luo
- Weitao Zhou
- Haibao Yu
topics:
- vision-language-action
- robot-world-model
- 3d-gaussian-splatting
- manipulation-policy
- future-prediction
- dense-geometric-supervision
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation

## Summary
GaussianDream adds training-time 3D Gaussian reconstruction and short-horizon future prediction to a VLA robot policy, then uses only the learned prefix tokens at inference.

## Problem
- Standard VLA policies learn mostly from action imitation, so 3D geometry, depth, contact-relevant structure, and short-term scene changes get weak supervision.
- This matters for manipulation because small geometric errors can move a grasp point, miss a target pose, or fail a spatial relation task.
- Prior 3D or world-model methods often add depth or point clouds for the current scene, or require heavy prediction rollouts during control.

## Approach
- GaussianDream encodes three temporal context frames, listed as t-10, t-5, and t, into 1024 GaussianDream prefix tokens in the PaliGemma/Gemma-2B prefix space.
- During training, a static Gaussian head decodes the prefix into a current 3D Gaussian scene, with depth used to back-project 256 × 256 Gaussian centers.
- A dynamic head predicts future Gaussian center displacements for horizons t+1 through t+5, conditioned on a learned horizon embedding.
- Training uses RGB rendering loss, depth loss, and pseudo 3D scene-flow loss, plus the base flow-matching action loss.
- At inference, the Gaussian decoding, rendering, depth, and velocity heads are removed; the policy receives only the learned prefix tokens and samples actions with the base policy.

## Results
- On LIBERO, GaussianDream reports 98.4% average success, compared with π0.5 at 96.7%, GeoPredict at 96.5%, GeoVLA at 97.7%, VLA-4D at 97.4%, 3D-CAVLA at 98.1%, and Spatial Forcing (PyTorch) at 97.6%.
- On LIBERO sub-suites, it reports 99.0% on Spatial, 99.6% on Object, 99.0% on Goal, and 96.0% on Long; LingBot-VA has a slightly higher LIBERO average at 98.5%.
- On RoboCasa Human-50, the paper reports 52.6% average success over 24 long-horizon kitchen tasks with 50 trials per task across five scenes.
- In real-robot evaluation, the paper reports 50.0% success on tasks covering attribute grounding, spatial relations, stacking and unstacking, and long-horizon goals.
- The reported efficiency claim is that inference needs no Gaussian rendering, no future video rollout, and no separate planner, because only prefix tokens condition the action policy.

## Link
- [https://arxiv.org/abs/2605.20752v1](https://arxiv.org/abs/2605.20752v1)
