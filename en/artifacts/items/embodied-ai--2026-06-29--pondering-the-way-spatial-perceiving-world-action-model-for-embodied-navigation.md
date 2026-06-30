---
source: arxiv
url: https://arxiv.org/abs/2606.29908v1
published_at: '2026-06-29T07:43:47'
authors:
- Hong Chen
- Daqi Liu
- Zehan Zhang
- Haiguang Wang
- Tianhao Lu
- Longfei Yan
- Haiyang Sun
- Fangzhen Li
- Hongwei Xie
- Bing Wang
- Guang Chen
- Hangjun Ye
- Yihua Tan
topics:
- embodied-navigation
- world-action-model
- visual-navigation
- diffusion-world-model
- goal-conditioned-navigation
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Pondering the Way: Spatial-perceiving World Action Model for Embodied Navigation

## Summary
SWAM is a goal-conditioned navigation model that predicts the path and the visual route in one diffusion pass from start and goal RGB images. It cuts candidate rollout cost and improves trajectory accuracy on RECON, SCAND, and TartanDrive.

## Problem
- Visual navigation needs actions that match both the goal image and traversable space; errors can send a robot toward infeasible paths.
- Two-stage world-model planners sample candidate actions, render rollouts, and rank them, so quality depends on candidate coverage and runtime grows with the number of samples.
- RGB-only prediction can miss geometry, causing viewpoint jumps, scale drift, and weak final-position accuracy.

## Approach
- SWAM fine-tunes a CogVideoX Diffusion Transformer to denoise one combined token sequence containing future RGB latents, depth latents, and 2D action tokens.
- The model conditions on start and goal observations. DepthAnything v3 supplies depth pseudo-labels during training; inference needs only monocular RGB.
- Visual-Guided Action Refinement uses cross-attention from generated RGB-D tokens into action tokens before decoding actions.
- Trajectory-Scale Regularization supervises the integrated endpoint displacement, reducing long-horizon drift across different path lengths.

## Results
- On RECON, ATE drops to 0.93 versus 1.53 for NWM+NoMaD x16, a 39.2% reduction; RPE is 0.43 versus 0.49.
- On SCAND, ATE drops to 1.15 versus 2.18 for NWM+NoMaD x16, a 47.2% reduction; RPE is 0.34 versus 0.46.
- On TartanDrive, ATE drops to 1.55 versus 6.23 for NWM+NoMaD x16, a 75.1% reduction; RPE is 0.68 versus 1.30.
- SWAM takes 16.91 s per episode, compared with 245.98 s for NWM+NoMaD x16; direct policies are faster at 0.12 s for GNM and 0.21 s for NoMaD but have higher trajectory error.
- At success@0.25 on RECON, SWAM reports 2.1x the success rate of NWM+NoMaD x16; the excerpt does not provide the absolute success values.
- For video generation on TartanDrive, SWAM reports PSNR 18.11 and SSIM 0.532; the excerpt states best results across evaluated datasets, but the full comparison table is truncated.

## Link
- [https://arxiv.org/abs/2606.29908v1](https://arxiv.org/abs/2606.29908v1)
