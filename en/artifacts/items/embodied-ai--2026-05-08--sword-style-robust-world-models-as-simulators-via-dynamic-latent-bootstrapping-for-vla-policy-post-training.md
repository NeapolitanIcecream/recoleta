---
source: arxiv
url: https://arxiv.org/abs/2605.07288v1
published_at: '2026-05-08T05:54:33'
authors:
- Jiaxuan Gao
- Yongjian Guo
- Zhong Guan
- Wen Huang
- Wanlun Ma
- Xi Xiao
- Junwu Xiong
- Sheng Wen
topics:
- vision-language-action
- world-model
- robot-policy-post-training
- sim2real
- robot-data-scaling
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training

## Summary
Sword trains a Wan-based action-conditioned world model for LIBERO manipulation rollouts that stays stable under style shifts and long autoregressive use. It targets VLA policy post-training by making imagined rollouts closer to the visual and action-conditioned behavior of the real dataset.

## Problem
- Existing learned simulators such as WoVR break under initial-state visual changes in LIBERO, including lighting, saturation, background, tabletop, and robot-arm color changes.
- Teacher forcing trains on ground-truth context frames, while inference uses the model’s own generated frames; this mismatch causes error buildup in long rollouts.
- The problem matters because RL post-training for VLA policies needs many interactions, and physical robot interaction is costly.

## Approach
- Sword uses Structure-Guided Style Augmentation: Cosmos-Transfer 2.5 changes visual style while depth maps, segmentation masks, and task prompts preserve scene geometry and task semantics.
- The world model predicts future observations from current observations and actions with a Wan 2.2 TI2V diffusion Transformer backbone.
- Dynamic Latent Bootstrapping stores the model’s predicted VAE latents in a dynamic cache and gradually replaces ground-truth context latents with cached predictions during training.
- The latent cache avoids pixel-space unrolling storage; the paper reports reducing context-frame storage from hundreds of GB to under 20 GB, about a 60x compression in latent space.
- At inference, the model uses 4 context frames and predicts the next 8 frames; the first episode frame is also used as a global condition for temporal consistency.

## Results
- On LIBERO-Original, Sword improves over WoVR on all reported generation metrics: LPIPS 0.11 vs 0.13, FID 18.39 vs 22.01, FVD 35.61 vs 61.26, and FloLPIPS 0.23 vs 0.26.
- On LIBERO-Mixed with raw plus OOD style-shifted data, Sword has LPIPS 0.20 vs 0.39, FID 32.59 vs 119.62, FVD 111.19 vs 198.84, and FloLPIPS 0.30 vs 0.46 against WoVR.
- The DLB ablation shows gains on LIBERO: full Sword reaches LPIPS 0.12, FID 18.51, FVD 32.17, FloLPIPS 0.23, compared with 0.13, 20.80, 48.46, 0.25 without DLB.
- Under the Mixed ablation setting, full Sword reaches LPIPS 0.17, FID 28.09, FVD 86.84, FloLPIPS 0.26, compared with 0.22, 37.84, 110.71, 0.32 without DLB.
- The paper reports GRPO post-training of OpenVLA-OFT on LIBERO-Spatial with higher policy success rates than WoVR across training steps, but the excerpt does not include the success-rate values.
- The experiments use 1,600 rollout episodes of 512 frames, with 1,500 for training and 100 for evaluation, and report about 13,000 A100 GPU hours of compute.

## Link
- [https://arxiv.org/abs/2605.07288v1](https://arxiv.org/abs/2605.07288v1)
