---
source: arxiv
url: https://arxiv.org/abs/2605.07931v3
published_at: '2026-05-08T16:04:43'
authors:
- Zuojin Tang
- Shengchao Yuan
- Xiaoxin Bai
- Zhiyuan Jing
- De Ma
- Gang Pan
- Bin Liu
topics:
- vision-language-action
- world-models
- robot-policy
- long-horizon-manipulation
- visual-token-compression
- latent-rollout
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy

## Summary
OneWM-VLA adds a compact latent world module to a frozen $\pi_0$ VLA and shows that one semantic visual token per frame can support long-horizon robot control. The main claim is that low visual bandwidth plus joint latent-action flow matching improves success rates without training a large new backbone.

## Problem
- World-model-augmented VLAs often roll out dense visual features or future pixels, which raises compute and memory cost as the planning horizon grows.
- Long-horizon robot tasks need policies that track how the scene will change under future actions; reactive VLAs tend to accumulate errors.
- The paper targets the constrained adaptation setting: a mostly frozen pretrained VLA with a small LoRA budget.

## Approach
- OneWM-VLA uses Adaptive Attention Pooling to compress each camera view and each frame into one semantic latent token.
- The pooling scores visual tokens with max response, summed response, and a learned MLP score, then combines the pooled outputs with learned weights.
- A single flow-matching model generates future latent tokens and future action chunks together, so latent rollout and action generation share attention and flow time.
- The model is built on $\pi_0$ with a PaliGemma-2B vision-language backbone, a Gemma-300M latent-action expert, and 14.71M LoRA trainable parameters.
- At inference, the model denoises latent and action streams together, then executes only the action stream on the robot.

## Results
- On MetaWorld MT50, the abstract reports average success rising from 47.9% for $\pi_0$ to 61.3% for OneWM-VLA. In Table 1, at horizon $H=30$, OneWM-VLA reaches 53.13% versus 37.98% for $\pi_0$ and 26.83% for $\pi_{0.5}$.
- On LIBERO, OneWM-VLA reaches 98.1% average success across Spatial, Object, Goal, and Long. On LIBERO-Long, it reaches 95.6% versus 85.2% for $\pi_0$ and 92.4% for $\pi_{0.5}$.
- On the real Piper arm under clean conditions, OneWM-VLA reaches 71.7% average success versus 50.0% for $\pi_0$ and 58.3% for $\pi_{0.5}$ across Pick Banana, Fold Cloth, and Pull Drawer.
- On real Fold Cloth, OneWM-VLA reaches 60.0% under clean conditions versus 20.0% for $\pi_0$ and 25.0% for $\pi_{0.5}$. Under observation noise, it reaches 40.0% versus 0.0% and 10.0%.
- The paper reports a bandwidth sweep from 1 to 12 tokens per frame where success decreases as token count grows under the matched training budget; the excerpt does not include the exact sweep values.

## Link
- [https://arxiv.org/abs/2605.07931v3](https://arxiv.org/abs/2605.07931v3)
