---
source: arxiv
url: https://arxiv.org/abs/2606.29936v1
published_at: '2026-06-29T08:12:58'
authors:
- Iok Tong Lei
- Qingchen Xie
- Yifan Wang
- Yap Ying Jie
- Zhidong Deng
topics:
- robot-manipulation
- vision-language-action
- spatial-pose-memory
- flow-matching-policy
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model

## Summary
OpenSPM stores object-relative key poses from demonstrations and uses them to guide a small flow-matching action model. The paper claims strong LIBERO-GOAL results with far fewer parameters and much higher action output frequency than large VLA baselines.

## Problem
- Open-environment tabletop manipulation needs language understanding, object-level 6D geometry, and fast control for grasping, placing, pushing, and other contact phases.
- Large VLA policies can generalize semantically, but they need large robot datasets and often lack object-relative pose constraints for precise manipulation.
- The problem matters because small pose errors can accumulate across action segments and cause failed grasps, bad placement, or collisions.

## Approach
- OpenSPM extracts key spatial poses from human demonstrations, such as approach, grasp, lift, pre-place, and release.
- Each key pose is stored as an SE(3) relative transform between the end effector and an object frame, so the same local geometry can transfer to a new scene after estimating the target object pose.
- A semantically conditioned 3D perception module uses multi-view masks, 3D reconstruction, and Kalman filtering to estimate continuous 6D object poses.
- At inference time, the system retrieves a memory entry from the language instruction, transfers the stored relative poses to the current scene, checks feasibility, and generates short action chunks between adjacent poses.
- A 240K-parameter conditional flow-matching model outputs action chunks of length H=5, with real-time proprioceptive feedback and terminal residual correction near grasp and placement poses.

## Results
- On 10 LIBERO-GOAL tasks with 50 initial states each, OpenSPM reports 85.6% success over 500 evaluation episodes.
- It beats the listed baselines on success rate: Diffusion Policy 68.3%, TraceVLA 75.1%, SpatialVLA 78.6%, OpenVLA 79.2%, WorldVLA 83.4%, and Octo-Base 84.6%.
- It reports 4.8 ms action-chunk generation latency and 1033.3 Hz equivalent action output frequency with H=5.
- The reported frequency is higher than Diffusion Policy 14.2 Hz, TraceVLA 2.2 Hz, SpatialVLA 6.7 Hz, OpenVLA 4.9 Hz, WorldVLA 2.4 Hz, and Octo-Base 54.7 Hz.
- The action model has 0.24M parameters, compared with about 260M for Diffusion Policy, 200M for Octo-Base, 4B for SpatialVLA, and 7B for TraceVLA, OpenVLA, and WorldVLA.
- Kalman pose prediction reports average errors of 5.8 mm position MAE and 2.12° orientation MAE against frame-by-frame SAM 3 + SAM 3D visual references across the 10 tasks.

## Link
- [https://arxiv.org/abs/2606.29936v1](https://arxiv.org/abs/2606.29936v1)
