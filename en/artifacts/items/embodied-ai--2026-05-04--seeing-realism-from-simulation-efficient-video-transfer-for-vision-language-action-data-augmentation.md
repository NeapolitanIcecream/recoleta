---
source: arxiv
url: https://arxiv.org/abs/2605.02757v1
published_at: '2026-05-04T15:57:07'
authors:
- Chenyu Hui
- Xiaodi Huang
- Siyu Xu
- Yunke Wang
- Shan You
- Fei Wang
- Tao Huang
- Chang Xu
topics:
- vision-language-action
- sim2real
- robot-data-augmentation
- video-transfer
- coreset-sampling
- diffusion-acceleration
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation

## Summary
The paper claims that realistic video transfer can make simulated robot data more useful for training vision-language-action policies. It turns simulated trajectories into visually varied videos while keeping the same actions, then trains VLA models on the mixed data.

## Problem
- VLA policies need large real robot datasets, but collecting those trajectories is slow and expensive.
- Simulated trajectories are cheap, but clean visuals, fixed layouts, and narrow scene variation cause poor transfer to clutter, lighting changes, texture changes, and instruction shifts.
- The paper targets data augmentation for robot policies, especially when full video generation over a large dataset costs too much.

## Approach
- The pipeline captions each simulated robot video with VideoChat2, rewrites the caption with Qwen3-8B to vary scene appearance, and extracts depth maps as geometry conditions.
- Cosmos-Transfer 2.5 generates realistic videos conditioned on the rewritten caption and depth, aiming to keep the original task semantics and action trajectory.
- A three-stage velocity caching method skips repeated diffusion velocity predictions during stable denoising steps, using parameters such as k=0.4, alpha=8, and m=3 final adjustment steps.
- A coreset sampler selects trajectories for augmentation using RDT-1B action prediction loss for difficulty and Cosmos-Embed1 video embeddings for visual diversity.

## Results
- On RoboTwin 2.0 single-task learning with RDT-1B, average success rose from 29.0% to 39.0% on Hard settings (+10.0 points) and from 49.0% to 55.0% on Easy settings (+6.0 points), using 50 demonstrations and 50 tests per task.
- On RoboTwin 2.0 multi-task learning with RDT-1B, 32 tasks and 9,600 trajectories were used; augmenting a 10% coreset raised Hard-setting average success from 23.0% to 31.0% (+8.0 points).
- On LIBERO-Plus spatial suite with 2,402 evaluation settings, pi_0 improved from 42.7% to 47.8% (+5.1 points), with large gains on object layout (+16.6 points) and language instructions (+22.0 points).
- On the same LIBERO-Plus suite, pi_0.5 improved from 89.8% to 90.8% (+1.0 point); gains were smaller because the baseline was already high.
- On standard LIBERO, augmented training slightly reduced performance: pi_0 dropped by 0.2 points on average and pi_0.5 dropped by 0.5 points, which the paper attributes to LIBERO’s train-test similarity.
- The diffusion velocity caching method cut generation time by an average of 61.2% on RoboTwin 2.0, with the paper claiming little quality loss.

## Link
- [https://arxiv.org/abs/2605.02757v1](https://arxiv.org/abs/2605.02757v1)
