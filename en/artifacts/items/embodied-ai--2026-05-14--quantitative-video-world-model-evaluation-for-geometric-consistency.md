---
source: arxiv
url: https://arxiv.org/abs/2605.15185v1
published_at: '2026-05-14T17:59:04'
authors:
- Jiaxin Wu
- Yihao Pi
- Yinling Zhang
- Yuheng Li
- Xueyan Zou
topics:
- video-world-models
- geometric-consistency
- benchmarking
- 3d-reconstruction
- physical-evaluation
relevance_score: 0.56
run_id: materialize-outputs
language_code: en
---

# Quantitative Video World Model Evaluation for Geometric-Consistency

## Summary
PDI-Bench gives generated videos a numeric test for 3D geometric consistency. It uses segmentation, monocular 3D reconstruction, and point tracking to score scale-depth alignment, 3D motion, and object rigidity.

## Problem
- The paper addresses a gap in video world model evaluation: visually convincing clips can still violate 3D geometry through scale drift, skating, object deformation, or broken perspective.
- Common metrics such as FVD and CLIP-based scores mainly measure visual distribution or semantic match, so they can miss physical geometry errors.
- The problem matters because video generators are being treated as implicit world models, but a world model should preserve basic projective geometry and object structure over time.

## Approach
- The method defines the Perspective Distortion Index (PDI), a weighted score over three residuals: scale-depth alignment, 3D trajectory consistency, and structural rigidity.
- It first isolates the target object with Florence-2 and SAM 2, then measures the object mask and pixel height over time.
- It reconstructs depth, camera poses, and world-space pointmaps with MegaSaM, so object motion can be measured in 3D rather than in screen coordinates.
- It tracks object anchor points with CoTracker3, lifts those 2D tracks into 3D coordinates, and checks whether pairwise distances stay stable.
- The final PDI uses weights 0.4 for scale, 0.4 for trajectory, and 0.2 for rigidity; lower PDI means better geometric consistency.

## Results
- The benchmark contains 183 videos from 28 text prompts: 15 real ground-truth videos and 168 generated videos from 6 models, across 5 scenarios.
- Ground truth scores best with PDI 0.1206, scale residual 0.0660, trajectory residual 0.1764, rigidity residual 0.1182, 0.0% outliers, and 86.7% MathPass.
- Seedance 2.0 is the best generated model overall with PDI 0.2422, 0.0% outliers, and 89.3% MathPass; CogVideoX-3 follows with PDI 0.2480 and the best generated trajectory and rigidity scores, 0.2033 and 0.2065.
- Veo 3.1, Wan 2.2, Sora, and HunyuanVideo score worse overall with PDI 0.4521, 0.5595, 0.8255, and 0.8825 respectively.
- Sora and HunyuanVideo show large scale errors: scale residuals 1.6753 and 1.8469, over 25 times the ground-truth scale residual of 0.0660, with 14.3% outliers for both.
- Scenario results show specific failure cases: Sora reaches PDI 2.1277 on curved motion with scale error 4.8660, and HunyuanVideo reaches PDI 2.4104 on partial occlusion with scale error 5.3793.

## Link
- [https://arxiv.org/abs/2605.15185v1](https://arxiv.org/abs/2605.15185v1)
