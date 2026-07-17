---
source: arxiv
url: https://arxiv.org/abs/2607.14698v1
published_at: '2026-07-16T08:01:49'
authors:
- Marino Watanabe
- Takami Sato
- Kentaro Yoshioka
topics:
- vision-language-action
- robot-foundation-model
- adversarial-robustness
- sim2real
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Lights, Camera, Malfunction: When Illumination Robustness Leaves VLA Models Blind to Color

## Summary
FLARE shows that fixed physical spotlights can severely disrupt VLA robot policies, while naive color augmentation can hide this vulnerability by making models ignore color. ChromaGuard preserves hue cues during adversarial training and improves the balance between lighting robustness and color-dependent manipulation.

## Problem
- VLA models can fail under small, physically plausible illumination changes, which matters because incorrect trajectories can create manipulation failures and collision risks in real deployments.
- Naive color and lighting augmentation may improve attack success rates by discarding color information rather than learning illumination-invariant visual features.

## Approach
- FLARE treats the attacker as black-box: it optimizes a fixed spotlight's hue, saturation, intensity, height, and cutoff angle using Bayesian optimization and evaluates both task failure and trajectory deviation.
- The study trains SmolVLA models on LIBERO-Spatial, LIBERO-Object, and LIBERO-10, then tests baseline and naive-augmentation policies under benign, random, and optimized lighting.
- A grayscale diagnostic tests whether naive augmentation caused the model to stop relying on color cues.
- ChromaGuard performs adversarial illumination augmentation while fixing hue perturbation to zero, preserving chroma while varying saturation, brightness, contrast, and sharpness.
- Real-world tests use SmolVLA and pi_0.5 on a 6-DoF SO-101 arm with color-invariant and color-dependent tasks.

## Results
- In simulation, optimized FLARE attacks reduced baseline success to 0.0% on all three LIBERO suites and produced maximum trajectory errors of up to 115.5 cm; baseline benign success was 83.0% on LIBERO-Spatial, 89.4% on LIBERO-Object, and 58.4% on LIBERO-10.
- Naive augmentation appeared robust in simulation, with optimized-attack success rates of 78.8%, 93.2%, and 47.2% on the three suites, but its grayscale success remained high—for example, 90.5% versus 89.8% RGB on LIBERO-Object—indicating that it had largely discarded color cues.
- On the real color-dependent task, naive augmentation reduced SmolVLA success to 47.5% under benign lighting, compared with 77.5% for the baseline.
- ChromaGuard produced 97.5% benign and 92.5% attacked success for SmolVLA on the color-dependent task, while achieving 70.0% benign and 70.0% attacked success on the color-invariant task.
- For pi_0.5, ChromaGuard achieved 55.0% benign and 70.0% attacked success on the color-dependent task; the paper attributes its lower benign color discrimination partly to the pretrained model, with incorrectly colored grasps accounting for 66.7% of failures.
- The evaluation covers fixed spotlights and limited physical tasks; the authors do not test time-varying illumination or adaptive closed-loop attacks.

## Link
- [https://arxiv.org/abs/2607.14698v1](https://arxiv.org/abs/2607.14698v1)
