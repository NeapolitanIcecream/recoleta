---
source: arxiv
url: https://arxiv.org/abs/2607.09185v1
published_at: '2026-07-10T08:20:27'
authors:
- Yufan Wei
- Kun Zhou
- Lingjun Mao
- Zijun Zhang
- Ziming Xu
- Ziqiao Xi
- Shuang Liang
- Ruobing Han
- Yuchen Yan
- Xinyue Wang
- Fan Feng
- Biwei Huang
topics:
- embodied-world-model
- latent-action-model
- robot-action-following
- causal-debiasing
- robot-data-efficiency
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Causally Debiased Latent Action Model for Embodied Action Conditioned World Models

## Summary
CD-LAM improves latent action representations for action-conditioned world models by removing visual factors that do not describe embodiment actions. It reports better action following, visual fidelity, robustness, and robot-action adaptation efficiency on 2B and 14B models.

## Problem
- Action-conditioned world models need action-labeled robot data, which is costly to collect.
- Latent action models learn from unlabeled videos, but reconstruction-only training can encode backgrounds, camera shifts, and non-interacted objects into the action representation.
- These confounders make world-model rollouts visually plausible while reducing compliance with supplied latent or robot actions.

## Approach
- CD-LAM fine-tunes the latent action model with embodiment-centric reconstruction, which gives higher loss weight to the robot and interacted objects than to the background.
- Action-centric contrastive learning brings transitions with the same coarse manipulation primitive together and separates transitions with different primitives across visual contexts.
- Latent-space calibration anchors duplicated-frame inputs near a zero-transition vector and controls capacity with a free-bit KL penalty.
- A three-stage pipeline debiases the LAM, trains the world model on the debiased latents, and learns a lightweight MLP that maps executable robot actions into the same latent space.

## Results
- On the latent-action audit, CD-LAM reduced the median zero-transition response from 0.527 to 0.043 and the median absolute latent norm from 3.119 to 0.226.
- Camera-shift response fell from 0.555 to 0.156 for horizontal shifts and from 0.545 to 0.110 for vertical shifts; shortcut leakage fell from 0.151 to 0.014.
- Latent-action FDCE decreased by 42% for the 2B backbone and 26% for the 14B backbone relative to DreamDojo.
- After robot-action adaptation, FDCE decreased by a further 35% at 2B and 30% at 14B, with the debiased 14B model leading on every reported metric.
- CD-LAM matched the DreamDojo reference using more than 12x fewer robot-action adaptation updates and surpassed it at the 6,000-step checkpoint; the debiasing stages used 1,000 LAM updates and 2,000 world-model updates.
- Evaluations used 300 held-out EgoDex clips for latent-action rollouts and 300 AgiBot clips for robot-action tests across 2B and 14B ACWM backbones.

## Link
- [https://arxiv.org/abs/2607.09185v1](https://arxiv.org/abs/2607.09185v1)
