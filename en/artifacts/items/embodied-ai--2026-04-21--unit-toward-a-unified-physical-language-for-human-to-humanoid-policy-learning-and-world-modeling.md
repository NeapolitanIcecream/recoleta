---
source: arxiv
url: http://arxiv.org/abs/2604.19734v1
published_at: '2026-04-21T17:57:27'
authors:
- Boyu Chen
- Yi Chen
- Lu Qiu
- Jerry Bai
- Yuying Ge
- Yixiao Ge
topics:
- humanoid-policy-learning
- vision-language-action
- world-model
- cross-embodiment-transfer
- latent-action-tokenization
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# UniT: Toward a Unified Physical Language for Human-to-Humanoid Policy Learning and World Modeling

## Summary
UniT learns a shared discrete action language for human and humanoid behavior, using visual outcomes to align different bodies. The paper applies this tokenizer to both policy learning and world modeling so human data can improve humanoid control.

## Problem
- Humanoid foundation models need large robot datasets, but high-quality humanoid data is scarce and expensive to collect.
- Human egocentric motion data is abundant, but human and humanoid action spaces do not match because they have different joints, control modes, and degrees of freedom.
- Existing fixes have clear limits: motion retargeting is manual and hard to scale, action-only latent spaces track embodiment-specific kinematics, and vision-only latent spaces can mix physical intent with appearance noise.

## Approach
- UniT builds three encoders from the same transition: a visual branch for before/after frames, an action branch for state plus action chunk, and a fusion branch that combines both.
- All three branches share one residual-quantization codebook, which turns their features into the same discrete tokens.
- Each token must reconstruct both future visual features and embodiment-specific actions. In simple terms, actions must explain what changes in the scene, and visual changes must explain what action happened.
- This cross-reconstruction is the main mechanism: it pushes human and humanoid behaviors with similar visible effects toward the same latent tokens while filtering out body-specific noise and irrelevant image details.
- The paper then uses these tokens in two systems: VLA-UniT predicts UniT tokens and decodes them into humanoid actions, while WM-UniT uses UniT action features as a shared control signal for action-conditioned video prediction.

## Results
- Policy learning is tested on RoboCasa GR1 with 24 tabletop tasks, evaluated over 50 episodes per task, under both full-data (24,000 robot trajectories) and few-shot (2,400 robot trajectories) settings.
- Human-to-humanoid transfer uses 27,419 EgoDex basic_pick_place human trajectories, mixed with the few-shot robot set and then fine-tuned on robot data.
- Real-world policy tests use an IRON-R01-1.11 humanoid with a 50-dimensional action space and only 120 robot trajectories per task for Pick & Place and Pouring.
- World modeling is evaluated with cross-embodiment data from RoboCasa and the DROID dataset, which contains 95,599 trajectories from 564 scenes.
- The excerpt claims state-of-the-art data efficiency, stronger out-of-distribution generalization, zero-shot task transfer for humanoid policy learning, and improved controllability for humanoid video generation.
- The excerpt does not provide the actual quantitative outcome numbers, baseline margins, or exact success-rate gains, so the strength of those claims cannot be checked from the provided text alone.

## Link
- [http://arxiv.org/abs/2604.19734v1](http://arxiv.org/abs/2604.19734v1)
