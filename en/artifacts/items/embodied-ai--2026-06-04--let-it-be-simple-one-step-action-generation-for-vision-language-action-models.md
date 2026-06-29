---
source: arxiv
url: https://arxiv.org/abs/2606.05737v1
published_at: '2026-06-04T05:58:30'
authors:
- Yitong Chen
- Shiduo Zhang
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- generalist-robot-policy
- diffusion-policy
- robot-data-scaling
- sim2real
- action-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models

## Summary
This paper claims that VLA diffusion policies can generate action chunks in one inference step when the observation, language, and state condition already pin down the action. A high-noise-biased training-time schedule makes standard flow matching competitive with 10-step decoding on LIBERO-family benchmarks and a small real-robot check.

## Problem
- Diffusion VLA policies often spend 10 or more denoising steps per action query, which adds latency for robot control.
- Image-generation methods for one-step diffusion often need teacher models, distillation, consistency losses, or extra training stages; the paper argues that compact robot action chunks may not need that machinery.
- The question matters because faster action decoding can reduce control delay while keeping continuous actions and avoiding action tokenization.

## Approach
- The model uses conditional flow matching with velocity prediction: sample noise and a clean action chunk, interpolate between them, and train a decoder to predict the velocity from the noised action, time, images, language, and robot state.
- The main change is the training-time distribution: it shifts samples toward the high-noise endpoint with t = u / (1 + (alpha - 1)(1 - u)), so the model gets more practice near the point used by one-step decoding.
- The architecture pairs a SigLIP/PaliGemma vision-language encoder with a small Transformer action head; actions stay continuous.
- A MNIST grid-to-sequence task tests the same condition-target shape: a rich visual condition maps to a compact sequence target.
- Ablations vary noise shift, action horizon, input channels, and action-loss masking to test when one-step decoding holds.

## Results
- On standard LIBERO H10 with the tiny model, alpha=4 one-step reaches 96.4% Spatial, 99.6% Object, 96.8% Goal, and 85.2% Long; uniform one-step gets 88.8%, 92.8%, 90.2%, and 70.2%.
- On the same standard LIBERO H10 setting, uniform 10-step gets 96.6% Spatial, 96.2% Object, 93.2% Goal, and 80.8% Long, so alpha=4 one-step beats that baseline on Object, Goal, and Long and is close on Spatial.
- With the full encoder, one-step mask7 reaches 97.4% Spatial, 98.4% Object, 97.8% Goal, and 92.8% Long; full32 one-step reaches 98.4%, 100.0%, 97.0%, and 95.6%.
- On LIBERO-Plus, all 18 comparable recipes place one-step at or above 10-step decoding, with a mean one-step margin of 5.4 success points.
- On LIBERO-Pro zero-shot perturbations from the standard-LIBERO checkpoint, one-step averages 44.2% and 10-step averages 43.5%; 14 of 16 cells differ by no more than 5 points.
- On real bimanual YAM RSS tasks using fine-tuned pi_0.5 checkpoints, one-step matches or improves the 10-step baseline: 80% vs 80% for insert mouse battery, 60% vs 35% for seal water bottle cap, and 100% vs 50% for Tower of Hanoi, with five one-step trials per task.

## Link
- [https://arxiv.org/abs/2606.05737v1](https://arxiv.org/abs/2606.05737v1)
