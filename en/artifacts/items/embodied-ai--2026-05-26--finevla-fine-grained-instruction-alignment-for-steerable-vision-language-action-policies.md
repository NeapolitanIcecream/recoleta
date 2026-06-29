---
source: arxiv
url: https://arxiv.org/abs/2605.27284v1
published_at: '2026-05-26T17:01:10'
authors:
- Xintong Hu
- Xuhong Huang
- Jinyu Zhang
- Yutong Yao
- Yuchong Sun
- Qiuyue Wang
- Mingsheng Li
- Sicheng Xie
- Yitao Liu
- Junhao Chen
- Yixuan Chen
- Yingming Zheng
- Shuai Bai
- Tao Yu
topics:
- vision-language-action
- robot-foundation-models
- steerable-robot-policy
- robot-data-scaling
- fine-grained-annotation
- dual-arm-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies

## Summary
FineVLA adds action-aligned, fine-grained instructions to robot trajectories so VLA policies can follow execution details such as arm choice, approach direction, contact region, and final pose. The paper reports gains in simulated and real dual-arm manipulation without lowering goal-level task success.

## Problem
- Open robot datasets usually pair each trajectory with a short goal label, so policies lack supervision for execution choices that affect manipulation.
- This matters because the same task can require different valid executions, for example using the left arm, approaching from a given direction, or touching a specific object region.
- The field also lacks a held-out benchmark and a trained annotator for checking whether VLMs understand process-level robot actions.

## Approach
- FineVLA-Tool converts 972,247 trajectories from 10 open-source robot datasets into a shared LeRobot-style format and cleans inconsistent action-state logs.
- It uses dynamic time warping over canonicalized action sequences, then clusters demonstrations to select 47,159 representative trajectories for annotation.
- Each selected trajectory gets human-verified fine-grained instructions across 10 dimensions: action sequence, active actor, target object, initial and final configuration, contact and approach, trajectory and orientation, object interaction, failure and recovery, and body motion.
- RoboFine-Bench holds out 500 videos with 10,816 atomic facts and 1,030 VQA questions to test robotic video understanding.
- FineVLA-Policy trains StarVLA-OFT and StarVLA-GR00T variants while changing only the language mixture: raw goal-level instructions, fine-grained instructions, or controlled FG:Raw ratios.

## Results
- FineVLA-Data covers 47,159 trajectories and 220,606 steps; average instruction length rises from 9.3 to 96.8 words, a 10.4x increase over coarse labels.
- Fine-grained-only training improves over raw-only by +1.4 to +8.1 success-rate points across tested architecture and data-scale settings.
- Mixed fine-grained and raw training peaks near FG:Raw = 1:2 to 1:1; the best AlohaMix-OFT setting reaches 86.8% Easy and 82.5% Hard on RoboTwin, compared with 71.8% and 71.4% for raw-only.
- In real-world dual-arm manipulation, FG:Raw = 1:1 scores 62.7/100 versus 49.9 for raw-only.
- The largest real-world gains over raw-only are pose +23, color +18, and approach direction +18, all tied to instruction-specified execution factors.
- RoboFine-VLM reaches 71.0% VQA accuracy and 83.6% hard caption score on RoboFine-Bench, ahead of the listed general VLM baselines.

## Link
- [https://arxiv.org/abs/2605.27284v1](https://arxiv.org/abs/2605.27284v1)
