---
source: arxiv
url: https://arxiv.org/abs/2606.24472v1
published_at: '2026-06-23T12:02:36'
authors:
- Yue Peng
- Yongzhe Zhao
- Artur Habuda
- Khuyen Pham
- Yanheng Zhu
- Tran Nguyen Le
- Fares Abu-Dakka
- Li Guo
topics:
- vision-language-action
- robot-foundation-model
- multi-camera-geometry
- geometric-distillation
- sim2real
- robot-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models

## Summary
G3VLA adds camera calibration to the visual tokens of pretrained vision-language-action policies, which improves robot manipulation tasks that depend on object position, spatial relations, and camera viewpoint changes.

## Problem
- Standard VLA policies such as pi0, pi0.5, and GR00T 1.5 process camera images mostly as 2D token streams, so they must learn camera intrinsics, extrinsics, and cross-view geometry indirectly from action labels.
- This matters most in multi-camera robot setups, where the camera calibration is known and useful for estimating where objects are in 3D space.
- Prior 3D manipulation methods often need depth, point clouds, voxels, changed action spaces, or task-specific model designs, which makes them harder to attach to pretrained VLA policies.

## Approach
- G3VLA inserts a camera-aware geometric module into the visual-token stream before action prediction. It keeps the pretrained VLA backbone, action space, and imitation objective unchanged.
- The module adds intrinsic-conditioned ray embeddings: each image patch token gets a direction derived from K^-1, so the model can distinguish pixels that look similar but correspond to different camera rays.
- It uses Projective Positional Encoding, or PRoPE, to give cross-view attention a camera-calibrated signal based on intrinsics and extrinsics.
- It fuses tokens across views with bidirectional cross-view attention, then passes the fused tokens to the same action pathway used by the base VLA.
- Training uses a two-stage recipe. Stage 1 trains the new geometry module with dense point-map supervision from ground-truth depth or confidence-gated pi3X teacher predictions. Stage 2 fine-tunes the full policy with the original action loss plus a smaller geometry distillation loss.

## Results
- On LIBERO with pi0, ground-truth geometric supervision raises average success from 84.6% to 88.1%, a +3.5 point gain. The largest suite gains are Object, 89.4% to 94.4% (+5.0), and Spatial, 85.2% to 89.2% (+4.0). With pi3X supervision, the average is 87.0%.
- On RoboCasa24 with pi0, success rises from 34.2% to 37.1% with ground-truth supervision and to 36.5% with pi3X supervision.
- On RoboTwin2.0 handover_block with pi0, ground-truth supervision improves success from 44.0% to 49.0%. The pi3X version drops to 41.0%, which the paper links to unreliable teacher point maps in the synthetic domain.
- On pi0.5 LIBERO, the reproduced baseline averages 95.85%, while G3VLA with pi3X reaches 97.0%. The gain is small because the baseline is already near saturation.
- On GR00T 1.5 LIBERO, results are mixed: the baseline averages 94.90%, G3VLA with ground-truth supervision reaches 94.50%, and G3VLA with pi3X reaches 95.25%.
- Ablations on pi0 LIBERO show that removing ray embeddings lowers average success from 87.0% to 85.0%, removing PRoPE lowers it to 85.9%, and replacing two-stage training with one-stage training lowers it to 86.3%. In real-world pouring, pi0 OOD success improves from 70.8-75.0% to 83.3-87.5%, and overall success improves from 82.5-85.0% to 90.0-92.5%.

## Link
- [https://arxiv.org/abs/2606.24472v1](https://arxiv.org/abs/2606.24472v1)
