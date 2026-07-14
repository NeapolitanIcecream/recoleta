---
source: arxiv
url: https://arxiv.org/abs/2607.11498v1
published_at: '2026-07-13T12:50:32'
authors:
- Byungkun Lee
- Dongyoon Hwang
- Dongjin Kim
- Hojoon Lee
- Minho Park
- Jaegul Choo
topics:
- vision-language-action
- robot-centric-geometry
- pointmaps
- viewpoint-generalization
- 3d-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models

## Summary
Robot-centric pointmaps give VLAs dense 3D scene coordinates in the same frame used for robot actions. This reduces viewpoint-related frame mismatch while reusing pretrained 2D visual encoders.

## Problem
- VLAs usually observe scenes in camera coordinates but predict actions in the robot frame, forcing the policy to learn the camera-to-robot transformation.
- The problem grows when demonstrations use varied camera placements or deployment uses an unseen viewpoint.
- Camera-aware inputs, depth maps, and point clouds either leave the transformation to the policy or discard the image grid used by pretrained VLAs.

## Approach
- Lift each RGB-D pixel into 3D, transform it from the camera frame into the robot base frame, and subtract the current end-effector position.
- Store the resulting XYZ coordinates in an image-shaped pointmap with the same H×W layout as the RGB image.
- Encode the pointmap with a visual tower initialized from the RGB encoder, then add its tokens element-wise to the RGB tokens.
- This adds robot-frame metric geometry without a point-cloud encoder, voxelization, extra token sequence, or inference-time rendering stage.

## Results
- On RoboCasa, the 24-task average success rate increased from 55.3% to 62.9% for π₀.₅, a gain of 7.6 points, and from 37.2% to 41.4% for SmolVLA, a gain of 4.2 points.
- The π₀.₅ pointmap model scored 62.9%, above KYC at 59.1%, PointVLA at 57.3%, and GeoVLA at 57.1%.
- In controlled RoboCasa studies, RGB + pointmap reached 34.7% versus 31.6% for RGB plus Plücker rays and depth; end-effector centering raised this to 36.9%.
- Under increasing training-camera variation, RGB success fell 9.6 points, from 34.5% to 24.9%, while the pointmap model fell 1.8 points, from 37.6% to 35.8%.
- In real-robot Franka experiments, the gain over RGB increased from 5.0 points at a training camera placement to 11.7 points at an unseen camera placement.

## Link
- [https://arxiv.org/abs/2607.11498v1](https://arxiv.org/abs/2607.11498v1)
