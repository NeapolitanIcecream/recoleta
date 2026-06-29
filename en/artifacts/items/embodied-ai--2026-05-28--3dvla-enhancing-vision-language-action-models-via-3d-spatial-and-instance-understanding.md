---
source: arxiv
url: https://arxiv.org/abs/2605.29416v1
published_at: '2026-05-28T06:07:57'
authors:
- Zhongyu Xia
- Yousen Tang
- Bingqing Wei
- Yongtao Wang
topics:
- vision-language-action
- 3d-scene-understanding
- robot-manipulation
- occlusion-reasoning
- instance-understanding
- spatial-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# 3DVLA: Enhancing Vision-Language-Action Models via 3D Spatial and Instance Understanding

## Summary
3DVLA adds 3D spatial, instance, and occlusion reasoning to pretrained Vision-Language-Action models for robot manipulation. It claims higher success rates on LIBERO-Plus and RoboTwin 2.0 while keeping the base VLA architecture largely intact.

## Problem
- Most VLAs use 2D visual tokens, so they struggle to reason about metric 3D positions, 6-DoF relationships, object extent, and occluded parts.
- Directly adding 3D perception models can break compatibility with VLM pretraining and often needs costly instance-level 3D labels.
- The problem matters because manipulation policies fail when camera views shift, objects overlap, or task-relevant parts are hidden.

## Approach
- Multi-View Spatial Fusion lifts multi-camera 2D features into a shared 3D memory using camera geometry, 3D coordinate embeddings, and 3D RoPE for view-consistent spatial features.
- An Object-Centric 3D Instance Module uses 3D probes to estimate object instances, matches them in 3D, and trains from pseudo boxes and masks produced by a frozen perception model rather than manual 3D labels.
- A Coordinate-Driven 3D Self-Supervised Predictor keeps the masked-token predictor after pretraining and uses it at inference to fill visual tokens at occluded 3D locations.
- Spatially-Conditioned Geometry Aggregation adds end-effector-relative 3D offsets to instance and completion tokens, then feeds those tokens into the downstream action expert.
- Uncertainty-guided routing injects completed 3D geometry more when the 2D instance prediction is uncertain.

## Results
- On LIBERO-Plus, $\pi_{0.5}$+3DVLA reaches 86.0% average success, compared with 84.2% for $\pi_{0.5}$, 69.6% for OpenVLA-OFT, and 68.4% for RIPT-VLA.
- On LIBERO-Plus category scores, $\pi_{0.5}$+3DVLA improves over $\pi_{0.5}$ on camera changes (75.6% vs 71.2%), light changes (97.4% vs 94.7%), background changes (97.7% vs 94.0%), noise (85.3% vs 84.2%), and layout changes (86.6% vs 84.3%); it is lower on language perturbations (88.6% vs 89.9%).
- On RoboTwin 2.0, $\pi_{0}$+3DVLA improves Easy success from 46.4% to 54.5% and Hard success from 16.3% to 23.2%.
- On RoboTwin 2.0, X-VLA+3DVLA improves Easy success from 70.0% to 72.6% and Hard success from 39.0% to 42.1%.
- Ablations on RoboTwin 2.0 show additive gains for $\pi_{0}$: 3D instances alone reach 50.1% Easy and 18.9% Hard, adding the predictor reaches 53.4% and 21.8%, and adding routing reaches 54.5% and 23.2%.

## Link
- [https://arxiv.org/abs/2605.29416v1](https://arxiv.org/abs/2605.29416v1)
