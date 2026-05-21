---
source: arxiv
url: https://arxiv.org/abs/2605.08215v1
published_at: '2026-05-06T11:21:25'
authors:
- Sangwu Park
- Wonjoong Kim
- Yeonjun In
- Sein Kim
- Hongseok Kang
- Chanyoung Park
topics:
- vision-language-action
- test-time-training
- visual-foresight
- out-of-distribution
- robot-manipulation
- libero-plus
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Test-Time Training for Visual Foresight Vision-Language-Action Models

## Summary
T³VF adds test-time training to Visual Foresight VLA models so they can adapt when visual conditions shift at deployment. It uses the gap between a predicted future image and the later observed image as supervision, then filters updates with action variance.

## Problem
- Visual Foresight VLA models first predict a future visual state, then generate actions from that prediction, so an out-of-distribution visual shift can damage both image prediction and action generation.
- The paper targets LIBERO-Plus perturbations such as robot state, language, noise, layout, background, camera, and light changes.
- This matters because VF-VLA success can drop under deployment shifts even when the base model works well on in-distribution LIBERO tasks.

## Approach
- At step `t`, the model predicts a future observation `ô_{t+n}` and executes an action. After `n` steps, the environment gives the actual observation `o_{t+n}`.
- T³VF treats `(ô_{t+n}, o_{t+n})` as a self-supervised training pair and updates the image-prediction path with the same image loss used in training.
- The update changes only the learnable query tokens `q`; the VLM backbone, image head, and action head stay frozen.
- To avoid noisy updates, the method samples `K=5` actions, computes their squared L2 variance, and accepts an update only when the variance is in the lower `ρ=0.3` quantile of a recent buffer.
- The reported hyperparameters are prediction gap `n=4`, batch size `B=4`, variance buffer size `10`, action samples `K=5`, and percentile threshold `ρ=0.3`.

## Results
- On LIBERO-Plus with perturbed training, Mantis + T³VF reaches `52.1%` average success versus `49.3%` for Mantis, a `+2.8` percentage-point gain, about `+5.7%` relative.
- In the same setting, the largest listed gains are Camera `55.3%` vs `50.5%` (`+4.8` points), Light `72.4%` vs `67.8%` (`+4.6` points), Background `63.0%` vs `60.3%` (`+2.7` points), and Layout `44.9%` vs `42.3%` (`+2.6` points).
- Without perturbed training, T³VF gives a smaller gain: `40.3%` average success versus `39.8%` for Mantis, or `+0.5` points.
- The Robot-perturbation ablation reports `29.0%` for Mantis, `29.8%` with unfiltered test-time training, `28.6%` with a fixed variance threshold, and `31.8%` with the full adaptive buffer.
- Runtime on the Robot perturbation is about `1.3×` the base per-episode time for T³VF, compared with about `1.7×` for unfiltered test-time training.

## Link
- [https://arxiv.org/abs/2605.08215v1](https://arxiv.org/abs/2605.08215v1)
