---
source: arxiv
url: https://arxiv.org/abs/2605.18743v2
published_at: '2026-05-18T17:58:51'
authors:
- Kunqi Xu
- Jitao Li
- Jianglong Ye
- Tianshu Tang
- Isabella Liu
- Sifei Liu
- Xueyan Zou
topics:
- world-model
- actionable-object-representation
- 3d-occupancy
- articulated-objects
- rgb-d-reconstruction
- robotics
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# WorldString: Actionable World Representation

## Summary
WorldString learns a controllable 3D object model that takes sparse object state keypoints as input and predicts the occupied 3D shape. The paper positions it as a building block for physical world models, with tests on rigid, articulated, skinned, and soft objects.

## Problem
- Robots and physical world models need object states that can be changed by actions, queried in 3D, and used for prediction or control.
- Video generators can make plausible rollouts but often lack 3D consistency and direct state control.
- Classical models handle rigid joints, skinning, or soft deformation separately, which makes mixed real-world objects hard to model with one method.

## Approach
- WorldString stores a learnable canonical object embedding and conditions it on sparse state keypoints, such as joints or tracked surface anchors.
- A State Transformer uses cross-attention to inject the keypoint state into the canonical object embedding.
- An Object Transformer spreads the local keypoint effects across the object so the full deformed state is encoded.
- A Voxel Transformer queries 3D coordinates and predicts occupancy, producing the deformed object shape as a voxel or point cloud output.
- For RGB-D video, the data pipeline uses Grounded-SAM2 for masks, CoTracker for dense tracks, TRELLIS for an initial mesh, farthest-point sampling for keypoints, and voxelized warped meshes as training targets.

## Results
- On rigid shape reconstruction, WorldString reports IoU/F1 of 92.17/95.92 on Utah Teapot, 75.38/85.96 on Stanford Bunny, 67.36/80.50 on Armadillo, and 70.20/82.49 on Lucy.
- On four articulated objects, WorldString averages 86.61 IoU and 92.73 F1. The baselines average 53.61/67.81 for NN, 47.62/62.18 for Optimized NN, and 44.79/60.73 for Dr. Robot.
- On Robot 1 Hand, WorldString reaches 90.28 IoU and 94.89 F1, compared with the best listed baseline at 73.41 IoU and 84.58 F1.
- On Robot 2 Arm, WorldString reaches 77.00 IoU and 87.01 F1, compared with Dr. Robot at 57.43 IoU and 72.94 F1.
- On IKEA-style furniture cases, WorldString reports 90.17/94.83 IoU/F1 for Furniture 21 and 88.98/94.17 for Furniture 09; the best listed baseline IoUs are 74.21 and 49.21.
- The excerpt claims coverage of articulated, skinned, and soft objects, but the provided text only includes full quantitative tables for rigid and articulated cases.

## Link
- [https://arxiv.org/abs/2605.18743v2](https://arxiv.org/abs/2605.18743v2)
