---
source: arxiv
url: https://arxiv.org/abs/2605.25620v1
published_at: '2026-05-25T09:21:43'
authors:
- Minghao Fu
- Fan Feng
- Nicklas Hansen
- Biwei Huang
topics:
- world-models
- robot-planning
- visual-foundation-models
- latent-representation-learning
- offline-control
- proprioceptive-alignment
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations

## Summary
TC-WM learns compact world-model latents from frozen visual foundation embeddings and proprioception. The paper claims these latents improve reward-free offline planning and control across navigation, manipulation, and locomotion benchmarks.

## Problem
- World models need latents that support action-conditioned prediction and planning, but pixel latents can lack semantic structure and frozen visual embeddings can carry task-irrelevant details such as texture, lighting, and background.
- This matters more in high-dimensional robot control: the excerpt cites Robomimic with a 7-DoF arm and a 43-D proprioceptive state, where extra latent factors can waste planning capacity.
- Reward-free offline settings make the problem harder because the model must learn useful state structure from fixed trajectories without reward labels or online correction.

## Approach
- TC-WM encodes each image with a frozen visual encoder such as DINOv2, embeds proprioception with a trainable layer, and concatenates both into a joint embedding.
- A linear encoder projects the joint embedding into a compact latent state used for rollouts.
- An InfoNCE-style contrastive loss aligns a sparse subspace of the latent with the current proprioceptive state, while the remaining latent dimensions keep visual information needed for reconstruction.
- A ViT dynamics model predicts the next latent from recent latents and actions; a separate head predicts next-step proprioception.
- A linear decoder reconstructs the frozen embedding from the compact latent, and the trained latent supports CEM planning, latent diffusion planning with an inverse dynamics model, or SAC.

## Results
- The excerpt reports evaluation across 9 benchmarks covering Robomimic, D4RL, navigation, locomotion, manipulation, and simulated plus real-world settings.
- It claims better world-modeling quality and more precise control than state-of-the-art approaches, but the excerpt does not provide exact success-rate, return, or MSE values.
- Figure 2 is described as showing Robomimic gains in success rate, lower latent-rollout MSE, stronger linear probing on Lift and Can, and better latent-space use against representation collapse.
- The method targets harder manipulation settings with a 7-DoF arm and 43-D proprioceptive state, while the excerpt contrasts these with 2-D action tasks such as Maze and Push-T.
- For continuous-control results, the paper reports mean episode return across 3 seeds, but the excerpt does not include the numeric returns.

## Link
- [https://arxiv.org/abs/2605.25620v1](https://arxiv.org/abs/2605.25620v1)
