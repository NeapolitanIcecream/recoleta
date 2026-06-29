---
source: arxiv
url: https://arxiv.org/abs/2605.30117v1
published_at: '2026-05-28T15:50:56'
authors:
- Haoyuan Shi
- Xiancong Ren
- Yingji Zhang
- Qinfan Zhang
- Jiayu Hu
- Haozhe Shan
- Han Dong
- Jinpeng Lu
- Yinda Chen
- Yi Zhang
- Yong Dai
- Xiaozhu Ju
topics:
- vision-language-action
- robot-policy-diagnostics
- mechanistic-interpretability
- attention-knockout
- representation-analysis
- semantic-grounding
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# VLA-Trace: Diagnosing Vision-Language-Action Models through Representation and Behavior Tracing

## Summary
VLA-Trace is a diagnostic suite for vision-language-action policies that links representation drift, attention-based causal tests, and rollout behavior. It finds that π0.5 and OpenVLA use different routes for action decoding and both struggle with fine-grained language changes.

## Problem
- VLA models can execute robot tasks, but their internal use of vision and language during action generation is hard to inspect.
- This matters because representation damage, weak language use, or visual shortcuts can cause policy failures that normal success rates do not explain.

## Approach
- The method compares three checkpoints: the pretrained VLM, the pretrained VLA, and the task-finetuned VLA.
- It uses cross-modal CKA and checkpoint-drift CKA to measure how vision, text, and joint representations change during robot adaptation.
- It blocks selected attention paths during inference to test whether action tokens depend on image tokens, text tokens, or cross-modal prefill interaction.
- It runs behavioral probes with attention localization, visual patch masking, and input editing to test spatial grounding, shortcut use, and instruction following.

## Results
- On LIBERO-10, π0.5 reaches 93.5% success in the all-paths baseline. Removing image access during generation drops it to 0.0%, while removing text access during generation leaves 39.0% success.
- On LIBERO Goal, Spatial, and Object, π0.5 keeps high success when generation text access is removed: 96.5%, 99.0%, and 98.0%. Removing generation image access gives 4.0%, 0.0%, and 0.0%.
- OpenVLA reaches 58.0% success on LIBERO-10 in the baseline. Removing generation text access drops it to 0.0% across LIBERO-10, Goal, Spatial, and Object; removing generation image access gives 1.0%, 16.0%, 44.0%, and 32.5%.
- Attention localization on LIBERO-10 shows action attention overlaps more with Robot+Object regions than object-only regions. For π0.5, full-rollout Robot+Object mass is 0.6328, IoU90 is 0.2233, and hit rate is 0.6349; for OpenVLA, the same metrics are 0.5882, 0.1965, and 0.9597.
- Visual masking reports strong dependence on visible task objects for π0.5. In one setup, its baseline success is 75.00% on LIBERO-10, 95.60% on LIBERO-Object, 95.80% on LIBERO-Spatial, and 80.00% on LIBERO-Goal; background replacement of target objects drops these by an average of 76.45 points.
- The main qualitative claim is that both models generate visually grounded trajectories, but both have limited fine-grained semantic following when prompts or inputs are edited.

## Link
- [https://arxiv.org/abs/2605.30117v1](https://arxiv.org/abs/2605.30117v1)
