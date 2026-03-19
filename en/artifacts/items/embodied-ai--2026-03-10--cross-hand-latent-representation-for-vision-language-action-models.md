---
source: arxiv
url: http://arxiv.org/abs/2603.10158v1
published_at: '2026-03-10T18:50:57'
authors:
- Guangqi Jiang
- Yutong Liang
- Jianglong Ye
- Jia-Yang Huang
- Changwei Jing
- Rocky Duan
- Pieter Abbeel
- Xiaolong Wang
- Xueyan Zou
topics:
- vision-language-action
- dexterous-manipulation
- cross-embodiment
- latent-action-space
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Cross-Hand Latent Representation for Vision-Language-Action Models

## Summary
This paper proposes XL-VLA, which changes vision-language-action models from “learning separately in each hand’s raw joint space” to “first mapping into a unified action semantics space and then decoding to the specific hand” through a latent action space shared across different dexterous hands. This addresses the difficulty of reusing data across multiple hand types and significantly outperforms standard VLA baselines in real-world multi-hand, multi-task dexterous manipulation.

## Problem
- Existing VLA systems in dexterous hand settings are limited by **action spaces that depend heavily on the specific hardware embodiment**: different hands have different numbers of joints, actuation methods, and kinematics, making it difficult to directly train a unified policy across hands.
- New dexterous hands continue to appear, but **collecting large amounts of demonstration data separately for each new hand** is costly and impractical, which hinders data scaling and long-term reuse for robot foundation models.
- This matters because if action representations cannot be shared across embodiments, dexterous manipulation cannot benefit from large-scale, multi-source data in the same way as vision and language.

## Approach
- The paper introduces **XL-VLA**: a **shared latent action space** is inserted into a standard VLA architecture, so that different dexterous hands first encode actions into the same latent and then use their own decoders to reconstruct the corresponding joint commands.
- The latent space is learned with a **multi-head VAE-style autoencoder**: each hand has its own encoder/decoder, but they share the same latent distribution, so the policy network only needs to predict embodiment-agnostic latent actions.
- Latent training uses three types of constraints: **reconstruction loss** ensures each hand can recover its original joint poses, **retargeting loss** aligns fingertip geometry/grasp relations across hands through differentiable forward kinematics, and **KL regularization** makes the latent space smooth and interpolable.
- Training the latent space **does not require paired trajectories or demonstrations across hands**; instead, poses are randomly sampled from each hand’s joint ranges, and self-supervised alignment is achieved through cross-hand decoding and FK geometric consistency.
- During VLA training, these pretrained encoder/decoder modules are frozen, and only the backbone is fine-tuned to predict the next latent chunk from vision, language, and historical latent actions.

## Results
- Data scale: the authors collected a real-world teleoperation dataset covering **4 dexterous hands, 10 tasks, 2000 demonstrations, and about 2M state-action pairs**; each task for each hand has **50** demonstrations.
- Compared with the standard **pi0** baseline, Table 2 shows that XL-VLA substantially improves average success rate across all four hands: **Ability 0.37→0.73**, **Inspire 0.27→0.68**, **Paxini 0.35→0.78**, **XHand 0.29→0.70**.
- The overall mean in Table 2 shows that XL-VLA achieves about **0.72** cross-hand multi-task success rate, while the baseline is about **0.32**, for an **absolute gain of 0.40**; the authors also report a task-mean row with baseline around **0.55** and XL-VLA around **0.90**, corresponding to **+0.35**, which the paper describes as a significant and consistent improvement.
- Looking at the task dimension, several challenging dexterous tasks improve substantially, for example **PF 0.20→0.70**, **HB 0.40→0.95**, **RB 0.45→0.90**, **PoS 0.23→0.88**, **PC 0.55→0.90**.
- The paper also claims that XL-VLA has **zero-shot generalization to unseen hand-task combinations**, and that it also brings gains when jointly trained across different robot systems (desktop xArm and humanoid G1), but the excerpt does not provide the corresponding full numerical tables.

## Link
- [http://arxiv.org/abs/2603.10158v1](http://arxiv.org/abs/2603.10158v1)
