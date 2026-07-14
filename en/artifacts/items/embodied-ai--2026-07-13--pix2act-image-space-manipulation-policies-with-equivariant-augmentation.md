---
source: arxiv
url: https://arxiv.org/abs/2607.11167v1
published_at: '2026-07-13T07:03:29'
authors:
- Haojie Huang
- Linfeng Zhao
- Haotian Liu
- Zhang Ye
- Si-Yuan Huang
- Mingxi Jia
- Boce Hu
- Fangzhou Lin
- Yu Qi
- Dian Wang
- Robin Walters
- Robert Platt
topics:
- robot-manipulation
- imitation-learning
- image-space-actions
- equivariant-augmentation
- multi-view-diffusion
- sim-to-real
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Pix2Act: Image-Space Manipulation Policies with Equivariant Augmentation

## Summary
Pix2Act learns robot manipulation policies by predicting continuous 2D gripper-keypoint trajectories in paired camera views, then recovering 3D actions through triangulation. Its equivariant augmentation and multi-view diffusion architecture improve simulated manipulation success and robustness to camera transformations.

## Problem
- Standard policies predict 3D translation and rotation directly from images, leaving the geometric link between observations and actions implicit. This increases ambiguity, overfitting, and the difficulty of learning precise manipulation.
- Earlier image-action methods use discretized pixels or independent per-view predictions, which cause precision loss, out-of-frame failures, triangulation errors, and inconsistent trajectories.
- The problem matters because precise, spatially varying manipulation tasks need action representations that generalize across camera poses and object configurations.

## Approach
- Represent each gripper pose with four 3D keypoints and project those keypoints into continuous, unbounded coordinates on two in-hand camera planes. Triangulation recovers the 3D keypoint trajectories and reconstructs translation and rotation.
- Train a diffusion policy to generate image-space keypoint trajectories instead of directly generating 3D poses. The model uses two in-hand views and one head-mounted view for local manipulation detail and global context.
- Apply independent planar rotations and translations to each camera image together with its corresponding action trajectory. This enforces per-camera equivariance while keeping the recovered 3D action invariant to these transformations.
- Use Diffusion X-Net, which combines per-view visual encoders, a multi-view transformer, and shared per-view diffusion heads to fuse camera information while supporting camera permutation equivariance.

## Results
- On 10 MimicGen simulation tasks, Pix2Act achieved 75.2% mean success across 50 unseen tests per task after training with 100 demonstrations per task.
- Pix2Act led on 9 of 10 tasks and exceeded the strongest reported baseline, EquiDiff-Voxel, by 12.1 percentage points: 75.2% versus 63.1% average success.
- It exceeded the strongest image-based baseline, EquiDiff-Img, by 21.6 percentage points: 75.2% versus 53.6%.
- Task-level success rates ranged from 50% on Square to 94% on StackThree; Pix2Act scored 52% on Threading and 90% on NutAssembly, two high-precision tasks.
- The excerpt states that Pix2Act also outperforms baselines in real-world tasks and remains robust under camera perturbations, but it does not provide the corresponding real-world numerical results.

## Link
- [https://arxiv.org/abs/2607.11167v1](https://arxiv.org/abs/2607.11167v1)
