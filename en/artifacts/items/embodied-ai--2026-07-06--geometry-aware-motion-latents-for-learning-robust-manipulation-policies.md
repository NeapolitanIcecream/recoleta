---
source: arxiv
url: https://arxiv.org/abs/2607.04714v1
published_at: '2026-07-06T06:34:14'
authors:
- Yunchao Zhang
- Yijia Weng
- Ruizhe Liu
- Ming Hu
- Leonidas Guibas
- Yanchao Yang
topics:
- robot-manipulation
- motion-latents
- 3d-geometry
- diffusion-policy
- rgb-d
- sim2real
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Geometry-Aware Motion Latents for Learning Robust Manipulation Policies

## Summary
GeoMoLa learns discrete motion codes by predicting future 3D point-cloud changes during manipulation. On RLBench single-view RGB-D tasks, it reports the best average success rate in the excerpt: 84.7%.

## Problem
- Robot policies need reusable motion abstractions, but many latent-action methods learn them from 2D video and miss depth, pose, approach angle, and object geometry.
- This matters because manipulation often fails when a policy cannot handle changed viewpoints, clutter, occlusion, or new object layouts.
- Existing 3D policies often use static scene features, so they do not directly learn how the 3D scene changes over time.

## Approach
- GeoMoLa converts RGB-D observations into pointmaps, then trains motion latents to predict future pointmaps. In simple terms, the code must describe what physical 3D change will happen next.
- It uses a vision-language encoder with VQ-style discrete codes, so similar motions can map to shared latent tokens.
- A pointmap diffusion model predicts future 3D geometry from recent pointmaps and the latent code. An RGB prediction branch is trained too, but the paper says geometry prediction drives the gains.
- A separate 3D denoising transformer uses the learned motion code, scene tokens, proprioception, and noisy action chunks to generate 6-DoF end-effector poses plus gripper commands.

## Results
- On RLBench single-view evaluation across 10 tasks and 166 variations, GeoMoLa reports 84.7% average success over 5 seeds.
- The strongest RLBench baseline in the table is RVT2 at 80.4%; other averages are 3D Diffuser Actor 77.0%, SkillDiffuser 74.4%, Act3D 65.3%, ManiGaussian 44.8%, and GNFactor 31.7%.
- GeoMoLa ranks first on 8 of 10 RLBench tasks.
- On Stack Blocks, GeoMoLa reaches 54.2% success versus RVT2 at 34.8% and 3D Diffuser Actor at 4.0%.
- On Push Buttons, GeoMoLa reaches 93.0% success versus RVT2 at 85.4% and 3D Diffuser Actor at 84.0%.
- The excerpt also claims real-world ALOHA gains in clutter with limited demonstrations, but it does not provide real-world success-rate numbers in the visible text.

## Link
- [https://arxiv.org/abs/2607.04714v1](https://arxiv.org/abs/2607.04714v1)
