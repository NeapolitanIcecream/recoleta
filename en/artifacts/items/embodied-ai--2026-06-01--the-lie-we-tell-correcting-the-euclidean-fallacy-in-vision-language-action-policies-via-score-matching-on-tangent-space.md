---
source: arxiv
url: https://arxiv.org/abs/2606.01847v1
published_at: '2026-06-01T07:59:29'
authors:
- Bing-Cheng Chuang
- I-Hsuan Chu
- Bor-Jiun Lin
- YuanFu Yang
- Min Sun
- Chun-Yi Lee
topics:
- vision-language-action
- diffusion-policy
- lie-groups
- se3-robotics
- robot-manipulation
- equivariant-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# The Lie We Tell: Correcting the Euclidean Fallacy in Vision Language Action Policies via Score Matching on Tangent Space

## Summary
Lie Diffuser Actor keeps diffusion-based robot pose generation on SE(3) instead of flattening poses into Euclidean vectors. The paper claims this reduces invalid rotations, preserves coordinate-frame equivariance, and improves manipulation benchmarks over 3D Diffuser Actor and OpenVLA-OFT variants.

## Problem
- Diffusion VLA policies often encode a robot gripper pose as a 12D Euclidean vector, using a flattened rotation matrix plus translation.
- Adding Gaussian noise to rotation matrices can produce non-orthogonal rotations, frame-dependent scores, and inefficient pose paths.
- This matters for manipulation because invalid or unstable pose trajectories can raise control cost and hurt transfer across camera or workspace frames.

## Approach
- The method, Lie Diffuser Actor, adds noise in the tangent space se(3) as a 6D twist with angular and linear velocity components.
- It maps each noisy twist back to SE(3) with the exponential map, so every denoising step stays a valid rigid transform.
- The reverse diffusion model predicts score vectors in se(3), then updates poses through group multiplication rather than vector addition.
- The architecture extends 3D Diffuser Actor with RGB-D point-cloud encoding, CLIP text features, a Transformer denoiser, and a tangent-space prediction head.
- The paper gives theoretical claims for manifold closure, left-invariant equivariance, and geodesic-like screw-motion trajectories.

## Results
- On CALVIN ABC→D, Lie Diffuser Actor reaches an average task length of 3.512 versus 3D Diffuser Actor at 3.27, a reported +7.3% gain.
- On CALVIN ABC→D, step success rates are SR1 93.7, SR2 83.4, SR3 70.3, SR4 57.6, and SR5 46.2 for Lie Diffuser Actor.
- On CALVIN ABCD→D, Lie Diffuser Actor reaches average task length 3.584 versus 3D Diffuser Actor at 3.288; SR5 improves from 41.6 to 53.7.
- In OpenVLA-OFT cross-architecture validation, SE(3) score matching improves LIBERO Long success rate from 92.20% to 94.13%.
- In rotation constraint analysis, the method reports lower orthogonality violation than 3D Diffuser Actor: 5.7% lower at median, 11.8% at P90, 5.4% at P95, and 2.6% at P99.
- Real-robot experiments are said to outperform the baseline on most tasks, but the excerpt does not provide task-level counts or success rates.

## Link
- [https://arxiv.org/abs/2606.01847v1](https://arxiv.org/abs/2606.01847v1)
