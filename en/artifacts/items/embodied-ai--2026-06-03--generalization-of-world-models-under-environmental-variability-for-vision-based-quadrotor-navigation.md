---
source: arxiv
url: https://arxiv.org/abs/2606.05015v1
published_at: '2026-06-03T15:38:36'
authors:
- Luca Zanatta
- Grzegorz Malczyk
- Kostas Alexis
topics:
- world-model
- quadrotor-navigation
- sim2real
- model-based-rl
- vision-based-navigation
- robot-generalization
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation

## Summary
The paper tests when DreamerV3 world models trained in simulation generalize to real vision-based quadrotor navigation. Its main claim is that cross-environment self-supervised reconstruction quality predicts real-world transfer better than simulated policy win rate.

## Problem
- It targets collision-free 3D quadrotor navigation using onboard depth images and state estimates.
- The key problem is domain shift: obstacle layouts, spawn points, goals, textures, lighting, and viewpoint changes can break a learned predictive model.
- This matters because a world-model policy can look strong in simulation while failing on a real drone if the learned dynamics and visual predictions do not transfer.

## Approach
- The authors train DreamerV3-style Recurrent State-Space Model world models on four simulated randomness levels: fixed obstacles (L1), five fixed layouts (L2), Sobol-sampled obstacle placements (L3), and fully uniform random placements (L4).
- Each model learns from depth images, robot state, and actions through self-supervised reconstruction, reward prediction, and KL regularization.
- They cross-evaluate every trained world model on every environment level using reconstruction MSE and SSIM, split into a context phase with real observations and an imagination phase with open-loop model rollout.
- They fine-tune actor-critic policies inside the learned latent model, with randomized low-level controller parameters to test dynamics mismatch.
- They deploy the trained systems on a real quadrotor in unseen indoor layouts, including closed-loop flight and one open-loop run after only 2.5 s of real sensor context.

## Results
- Hyperparameter search found the best models used RSSM deterministic and hidden sizes of 1024, batch sequence length 64, and discrete latent size 64 for L1/L2 or 32 for L3/L4.
- Discrete latent size and batch length had the largest effect on reconstruction loss: batch length gave about a 35% relative loss gap, discrete latent size gave about 35% to 50%, RSSM size about 20%, and random seed under 5%.
- In simulation policy evaluation, WM3 had the best cross-environment performance: win rates of 97.0% on L1, 96.5% on L2, 92.5% on L3, 89.5% on L4, and 72.0% on the 10-cuboid OOD layout.
- WM1 overfit the fixed layout: it reached 99.5% win rate on L1 but dropped to 54.5% on OOD, with OOD crash rate rising to 44.5%.
- Real closed-loop tests used a 13 m corridor with seven planar panels and gaps as narrow as 0.67 m and 0.85 m; WM1, WM2, and WM4 reached the target, while WM3, the strongest simulation policy, failed.
- The paper reports an open-loop real-world run where the drone received 2.5 s of real input, then flew using imagined observations over a 12 m traverse after sensors were cut off.

## Link
- [https://arxiv.org/abs/2606.05015v1](https://arxiv.org/abs/2606.05015v1)
