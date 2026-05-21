---
source: arxiv
url: https://arxiv.org/abs/2605.06192v1
published_at: '2026-05-07T13:06:19'
authors:
- Zhaoyang Yang
- Yurun Jin
- Lizhe Qi
- Cong Huang
- Kai Chen
topics:
- robot-world-model
- video-diffusion
- action-conditioned-video
- kinematic-projection
- robot-data-scaling
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields

## Summary
EA-WM improves robot video world modeling by turning robot actions into camera-aligned visual fields and using event-supervised fusion with video features. The paper claims better action-consistent rollouts on WorldArena, especially for robot motion, contact, and 3D consistency.

## Problem
- Robot video world models often condition generation on low-dimensional joint or end-effector vectors, which do not carry enough camera-space geometry for accurate rendered robot motion.
- Poor rollout geometry and weak robot-object contact modeling reduce the value of generated videos for planning, synthetic robot data, and VLA policy evaluation.
- Existing world-action models focus more on using videos to improve action prediction than on using actions to improve future video synthesis.

## Approach
- EA-WM converts robot joint states, gripper states, end-effector poses, and camera parameters into Structured Kinematic-to-Visual Action Fields, or KVAFs.
- KVAFs are built with forward kinematics and camera projection, then rendered as depth-aware arm skeletons, joint landmarks, gripper geometry, end-effector heatmaps, and pose axes in the target camera view.
- The model encodes both RGB video and KVAFs with the Wan2.2 video VAE, then processes them with a video branch and a KVAF branch in a diffusion-transformer backbone.
- Sparse bidirectional fusion layers exchange information between the branches through cross-attention.
- Event-Difference Latent Supervision encodes frame-difference videos as event targets, then uses them to train event gates that control where video and KVAF features interact.

## Results
- On WorldArena, EA-WM reports a P3CScore of 76.60, compared with 71.08 for CogVideoX, the strongest listed baseline, and 60.83 for Wan2.2.
- EA-WM improves Interaction Quality to 0.682 versus 0.594 for CogVideoX, and Trajectory Accuracy to 0.430 versus 0.353.
- It reports Depth Accuracy of 0.959 versus 0.910 for CogVideoX, and Perspectivity of 0.838 versus 0.796 for the best listed baseline on that metric.
- It reports Instruction Following of 0.792 versus 0.727 for CogVideoX, while Semantic Alignment is 0.895, slightly below the best listed value of 0.898 from CogVideoX.
- In ablations, full EA-WM scores 76.60 P3CScore, compared with 70.97 without KVAFs and 74.80 without event-aware fusion.

## Link
- [https://arxiv.org/abs/2605.06192v1](https://arxiv.org/abs/2605.06192v1)
