---
source: arxiv
url: https://arxiv.org/abs/2606.03598v1
published_at: '2026-06-02T13:04:15'
authors:
- Ziyang Chen
- Shaoguang Wang
- Weiyu Guo
- Qianyi Cai
- He Zhang
- Pengteng Li
- Yiren Zhao
- Yandong Guo
topics:
- vision-language-action
- continual-learning
- experience-replay
- robot-manipulation
- catastrophic-forgetting
- libero-benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models

## Summary
PHASER improves continual learning for vision-language-action robot policies by changing replay memory from uniform frame storage to phase-aware storage and phase-level replay routing. It targets catastrophic forgetting in sequential LIBERO manipulation tasks and reports large ASR gains across 3 VLA backbones.

## Problem
- VLA robot policies forget earlier manipulation tasks when trained on a sequence of new language-conditioned tasks.
- Uniform experience replay stores frames in proportion to phase length, so short contact-heavy phases such as grasping can get too few examples.
- Uniform replay also spends memory on old tasks without checking which past phases are most likely to conflict with the current task.

## Approach
- PHASER splits each trajectory into sub-skill phases such as approach, grasp, and transport.
- Each phase gets an equal frame budget, with stride-3 temporal subsampling and reservoir sampling inside the phase boundary.
- A replay router scores old phases against the current phase using language similarity, visual similarity, and action divergence.
- Replay sampling uses a Boltzmann distribution over cached phase scores, computed once at each task transition, so inner-loop replay cost matches standard ER.
- Auto-PC can replace human phase labels by using action-signal change-point detection followed by VLM semantic verification.

## Results
- On LIBERO-Goal with OpenVLA-OFT-7B, PHASER reaches 87.8% ASR and 7.8 NBT, compared with ER at 77.6% ASR and 22.2 NBT.
- On LIBERO-Long with OpenVLA-OFT-7B, PHASER reaches 85.8% ASR, compared with ER at 54.6% and MIR at 82.2%.
- Across the main table, PHASER improves ASR over ER by +10.2 to +39.6 points depending on backbone and suite; the abstract reports up to +31 points over matched-budget ER.
- On QwenGR00T-3B, PHASER improves LIBERO-Goal ASR from 51.6% to 78.0% and LIBERO-Long ASR from 31.4% to 48.6% versus ER.
- On QwenOFT-3B, PHASER improves LIBERO-Goal ASR from 39.4% to 79.0% and LIBERO-Long ASR from 33.0% to 51.6% versus ER.
- Auto-PC phase discovery stays close to human phase labels on LIBERO-Long: 89.6 vs 85.8 ASR on OpenVLA-OFT-7B, 48.0 vs 48.6 on QwenGR00T-3B, and 49.0 vs 51.6 on QwenOFT-3B.

## Link
- [https://arxiv.org/abs/2606.03598v1](https://arxiv.org/abs/2606.03598v1)
