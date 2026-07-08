---
source: arxiv
url: https://arxiv.org/abs/2607.04816v1
published_at: '2026-07-06T08:50:05'
authors:
- Yifu Xiong
- Wenhao Yu
- Jiaxuan Lin
- Bojun Zou
- Jiahao Li
- Lu Zhang
- Yanyong Zhang
- Jianmin Ji
topics:
- vision-language-action
- robot-manipulation
- latent-actions
- action-conditioning
- context-gating
- libero
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# CAC-VLA: Context-Gated Action Conditioning for Vision-Language-Action Models

## Summary
CAC-VLA adds latent action prediction and gated action conditioning to a Vision-Language-Action robot policy. It reports 98.3% average success on LIBERO and 89.5% on LIBERO-Plus supervised fine-tuning.

## Problem
- Standard VLA policies pass visual-language features to an action expert, so the expert must infer action structure and low-level robot commands from features trained mainly for perception and language.
- Prior action-reasoning methods often add separate modules that produce action plans, reference trajectories, or action priors, which adds system complexity.
- The problem matters because small errors in the link between instruction understanding and motor control can cause manipulation failures, especially in long-horizon tasks or shifted visual conditions.

## Approach
- CAC-VLA trains VLM query tokens to predict latent actions from the current image and language instruction.
- The latent actions are raw latents from an ordered action tokenizer, encoded from future robot action segments with a configurable latent-action horizon.
- The robot does not execute these latent actions directly. The continuous action expert uses them as conditioning while still producing the final action chunk.
- A cross-attention module retrieves latent-action information for each expert layer, and a context gate controls the residual update strength channel by channel.
- During training, the frozen tokenizer supplies latent targets and conditioning tokens; during inference, the tokenizer is removed and the VLM-predicted latent actions condition the expert.

## Results
- On LIBERO, CAC-VLA reports 98.3% average success rate, with 98.4% Spatial, 99.8% Object, 99.6% Goal, and 95.4% Long. It ranks second overall behind ACoT-VLA at 98.5%.
- On LIBERO Object and Goal, CAC-VLA reports the best listed scores: 99.8% Object and 99.6% Goal.
- On LIBERO-Plus supervised fine-tuning, CAC-VLA reports 89.5% average success, compared with 88.0% for ACoT-VLA and 85.7% for the reproduced π0.5 baseline.
- On LIBERO-Plus supervised fine-tuning, CAC-VLA reports 91.2% Camera, 78.4% Robot, 83.3% Language, 97.5% Light, 97.1% Background, 95.4% Noise, and 87.8% Layout.
- On LIBERO-Plus zero-shot transfer, CAC-VLA reports 83.8% average success, compared with 81.5% for reproduced π0.5, 69.6% for OpenVLA-OFT, and 68.4% for RIPT-VLA.
- The excerpt states that ablations support the latent-action horizon and context gate, but the provided ablation table is truncated and does not include all quantitative comparisons.

## Link
- [https://arxiv.org/abs/2607.04816v1](https://arxiv.org/abs/2607.04816v1)
