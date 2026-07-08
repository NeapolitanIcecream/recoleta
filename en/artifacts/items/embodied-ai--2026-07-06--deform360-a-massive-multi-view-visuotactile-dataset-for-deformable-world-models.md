---
source: arxiv
url: https://arxiv.org/abs/2607.05390v1
published_at: '2026-07-06T17:59:18'
authors:
- Hongyu Li
- Wanjia Fu
- Xiaoyan Cong
- Zekun Li
- Binghao Huang
- Hanxiao Jiang
- Xintong He
- Yiqing Liang
- Rao Fu
- Tao Lu
- Srinath Sridhar
- Kevin A. Smith
- George Konidaris
- Yunzhu Li
topics:
- deformable-world-models
- visuotactile-dataset
- robot-data-scaling
- multi-view-3d-tracking
- dexterous-manipulation
- model-predictive-control
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Deform360: A Massive Multi-view Visuotactile Dataset for Deformable World Models

## Summary
Deform360 is a large real-world visuotactile dataset for learning deformable object world models. It pairs 360-degree multi-view video, tactile sensing, dense 3D tracking, and robot interaction data for deformable manipulation.

## Problem
- Robots struggle to predict deformable object motion because cloth, rope, foam, and plush objects have many shape states and contact effects are often hidden by grippers or self-occlusion.
- Existing deformable-object datasets are often synthetic, small, narrow in object type, missing tactile data, or missing dense 3D annotations.
- The gap matters because deformable manipulation needs action-conditioned future prediction for planning, contact reasoning, and model comparison across 2D video and 3D particle methods.

## Approach
- The authors collect 198 daily-life deformable objects across 1,980 interaction sequences using 41 synchronized 720p cameras at 30 FPS and two tactile-equipped UMI grippers.
- The dataset covers 28 1D objects, 98 2D objects, and 72 3D volumetric deformable objects, with 13 manipulation primitive types across 17 categories.
- Their annotation pipeline reconstructs per-frame geometry with 3D Gaussian Splatting, tracks up to 1,600 2D points per view with CoTracker3, lifts those tracks into 3D with rendered depth, and fuses views with RANSAC.
- Tracking is refined with losses for surface alignment, local rigidity, velocity smoothness, and tactile contact consistency. In simple terms, the method turns many camera views and touch readings into moving 3D particles on the object surface.
- The dataset is used for contact prediction, 2D video model benchmarking, 3D particle model benchmarking, and early MPC-based robot planning tests.

## Results
- Dataset scale: 198 objects, 1,980 sequences, 41 camera views, 74,850 raw videos, about 23.3 million frames, 215.7 cumulative multi-view hours, and 10.34 seconds per episode on average.
- Compared with listed real-world deformable datasets, Deform360 has the largest object count in the table: 198 objects versus 27 for HCOS, 22 for DOT, 18 for PokeFlex, 17 for Robo360, and 11 for PhysTwin.
- Reconstruction quality on held-out views reaches a global average of 27.66 PSNR, 0.96 SSIM, and 0.0708 LPIPS. The best category PSNR is 30.00 dB for 3D volumetric deformables.
- Visuotactile tracking gives a Chamfer distance error of 2.71×10^-5 m^2, compared with 1.41×10^-4 m^2 for visual-only tracking, a roughly 5× error reduction.
- Visual-to-contact prediction reaches 88.67% mean accuracy across 36 synchronization-filtered views, compared with 50.31% random guessing, with an F1 score of 0.8909.
- The excerpt reports a qualitative benchmark finding: 3D particle models perform better in low-data settings due to physical structure, while 2D video models generalize better when trained with more data. The excerpt does not include the final numeric world-model benchmark table or robot-planning success rates.

## Link
- [https://arxiv.org/abs/2607.05390v1](https://arxiv.org/abs/2607.05390v1)
