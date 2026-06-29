---
source: arxiv
url: https://arxiv.org/abs/2605.16395v1
published_at: '2026-05-12T13:43:53'
authors:
- Jiajian Li
- Jingyuan Huang
- Junru Gong
- Qi Wang
- Xiaokang Yang
- Yunbo Wang
topics:
- robot-world-model
- differentiable-simulation
- vision-language-action
- sim2real
- robot-policy-optimization
- embodied-ai
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# OrbiSim: World Models as Differentiable Physics Engines for Embodied Intelligence

## Summary
OrbiSim trains a robot world model to act like a differentiable physics engine: it predicts explicit physical states and renders pixels from those states. The claimed payoff is better long-horizon robot simulation and direct gradient-based policy training.

## Problem
- Classical simulators such as MuJoCo, PhysX, Bullet, and Isaac Sim give useful robot rollouts, but their contact and rendering pipelines often block gradients needed for direct policy or parameter optimization.
- Recent generative world models can predict video, but many do not expose physical states, scene assets, mass, friction, or other parameters needed for closed-loop robot control.
- This matters because robot learning needs simulators that connect assets, physics, pixels, and rewards in one trainable execution path.

## Approach
- OrbiSim splits simulation into two neural parts: OrbiSim-Dynamics predicts the next explicit physical state, and OrbiSim-Vision renders the next RGB observation from that state.
- The dynamics model treats the robot and each object as separate tokens, then uses a Transformer coupling module to model contacts, constraints, and multi-object interaction.
- Actions, object attributes, and world parameters such as mass, friction, geometry, and gravity condition the dynamics through Adaptive Layer Normalization.
- The vision model uses latent diffusion conditioned on predicted states, recent frames, and scene descriptors to generate pixels while keeping the physical state as the anchor.
- Because the rollout is differentiable, OrbiSim can optimize scene parameters for real-to-sim identification and compute analytical policy gradients through the dynamics.

## Results
- On robosuite Push, OrbiSim Final reports PSNR10 26.7105 and PSNR100 19.9819, compared with Vid2World at 22.2014 and 17.8856, and AdaWorld at 26.6647 and 12.8346.
- OrbiSim Final reports LPIPS10 0.1078 and LPIPS100 0.1428, better than Vid2World at 0.1312 and 0.2551, and AdaWorld at 0.1183 and 0.3482.
- OrbiSim Final reports FVD 533.9, compared with Vid2World at 1750.1 and AdaWorld at 1305.8.
- OrbiSim Final reports trajectory error 0.4468, compared with Vid2World at 0.6754 and AdaWorld at 1.8597.
- The ablation without dynamics-vision decoupling has higher PSNR10 at 27.9346, but worse long-horizon metrics: FVD 689.1 and trajectory error 0.8134 versus OrbiSim Final at 533.9 and 0.4468.
- The paper also claims stable autoregressive rollout on Isaac Lab Stack over a 225-step horizon, plus qualitative generalization to articulated objects in AdaManip and deformable cloth in Physion Drape.

## Link
- [https://arxiv.org/abs/2605.16395v1](https://arxiv.org/abs/2605.16395v1)
