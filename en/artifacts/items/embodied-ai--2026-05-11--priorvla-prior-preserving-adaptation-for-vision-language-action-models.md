---
source: arxiv
url: https://arxiv.org/abs/2605.10925v1
published_at: '2026-05-11T17:56:02'
authors:
- Xinyu Guo
- Bin Xie
- Wei Chai
- Xianchi Deng
- Tiancai Wang
- Zhengxing Wu
- Xingyu Chen
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- vla-adaptation
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models

## Summary
PriorVLA adapts pretrained VLA robot policies without overwriting useful pretraining priors. It keeps a frozen action expert as a prior source and trains a separate adaptation expert, with the largest gains in OOD and few-shot robot manipulation.

## Problem
- Full fine-tuning of pretrained VLAs can overfit limited downstream robot data and reduce OOD generalization.
- This matters because new robot tasks, scenes, objects, and embodiments often have few demonstrations, so losing pretrained scene and motor priors wastes costly large-scale pretraining.

## Approach
- PriorVLA starts from pi0.5 and splits the action model into two paths: a frozen Prior Expert and a trainable Adaptation Expert initialized from the same weights.
- The frozen Prior Expert runs during denoising, but its final action prediction is discarded; its internal states provide motor-prior features.
- Learnable Scene Queries read task-relevant visual-language features from the VLM, Motor Queries read frozen action-denoising features, and Action Queries feed both into the Adaptation Expert.
- Training uses the same flow-matching MSE action loss as full fine-tuning, applied only to the Adaptation Expert.
- The method trains the Adaptation Expert, Expert Queries, and VLM vision encoder while freezing the rest, updating about 25% as many parameters as full fine-tuning.

## Results
- On RoboTwin 2.0 standard training across 13 tasks, PriorVLA reaches 77% Easy ID and 53% Hard OOD success, beating pi0.5 by +10 and +11 points.
- On RoboTwin 2.0 data scaling, Hard OOD gains over pi0.5 are +11 points in few-shot, +11 in standard data, and +6 in large-data settings; Easy ID is 41% vs 29% in few-shot and 77% vs 67% in standard data.
- On LIBERO, PriorVLA reports 99.1% average success across Spatial, Object, Goal, and Long, above OpenVLA-OFT at 97.1% and pi0.5 at 96.9%.
- In real-world standard-data tests over eight tasks and two robot embodiments, PriorVLA reaches 81% ID and 57% OOD success, improving over pi0.5 by +12 and +16 points.
- With 10 real-world demonstrations per task, PriorVLA reaches 48% ID and 32% OOD success, beating pi0.5 by +24 and +22 points.

## Link
- [https://arxiv.org/abs/2605.10925v1](https://arxiv.org/abs/2605.10925v1)
