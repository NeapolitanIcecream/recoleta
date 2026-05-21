---
source: arxiv
url: https://arxiv.org/abs/2605.17486v1
published_at: '2026-05-17T14:55:32'
authors:
- Sixu Lin
- Yunpeng Qing
- Litao Liu
- Ming Zhou
- Ruixing Jin
- Xiaoyi Fan
- Guiliang Liu
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- reinforcement-finetuning
- sim2real
- multi-task-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization

## Summary
DyGRO-VLA addresses RL fine-tuning of VLA robot policies across many tasks without damaging shared features. It freezes a base VLA and learns routed residual RL experts that correct its action chunks.

## Problem
- RL post-training can raise single-task robot success, but in multi-task VLA training it can distort shared representations and cause forgetting.
- The issue matters because VLA models are meant to reuse vision-language-action features across tasks; task-specific RL turns them into narrower controllers.
- In LIBERO analysis, SAC-based reinforcement fine-tuning became unstable as task count grew, and 20-task training caused the average success rate to drop sharply; the excerpt does not give the exact drop.

## Approach
- The offline stage trains a base VLA on demonstrations with an information bottleneck loss: keep features needed for action prediction and discard observation details such as background and lighting.
- The VLA encoder uses wrist and third-view camera images, language instructions, proprioception, DINOv2, SigLIP, and Qwen2.5-0.5B to produce fused latent features.
- The online stage freezes the base VLA and learns a Mixture-of-RL-Residuals that predicts a delta action chunk added to the base action chunk.
- A router selects the top-m residual experts using a task embedding trained with a contrastive loss against task prototypes.
- Training mixes offline and online replay, adds load-balancing regularization to avoid expert collapse, and samples harder tasks more often based on recent success rate.

## Results
- On LIBERO, DyGRO-VLA reports 97.1% average success rate, an absolute +4.4 percentage-point gain over its offline base model.
- On LIBERO-Long, it reports a +9.8 percentage-point improvement, the largest stated LIBERO gain in the excerpt.
- On RoboTwin2 simulation, it reports 79.2% overall success and the best overall result among the compared methods named in the excerpt.
- Under Sim2Real transfer on RoboTwin2, it surpasses RFT baselines, with the strongest stated gains on complex bimanual and long-horizon tasks; the excerpt does not provide exact real-world success rates.
- The representation analysis embeds 40 LIBERO tasks with 10 samples per task before and after single-task RFT, showing that RFT pushes the tuned task into an isolated cluster.

## Link
- [https://arxiv.org/abs/2605.17486v1](https://arxiv.org/abs/2605.17486v1)
