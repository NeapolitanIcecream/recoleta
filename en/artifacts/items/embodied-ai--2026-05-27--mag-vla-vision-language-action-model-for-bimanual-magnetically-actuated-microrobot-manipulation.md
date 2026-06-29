---
source: arxiv
url: https://arxiv.org/abs/2605.28486v1
published_at: '2026-05-27T13:44:00'
authors:
- Yongchen Wang
- Kangyi Lu
- Lan Wei
- Dandan Zhang
topics:
- vision-language-action
- magnetic-microrobots
- bimanual-manipulation
- action-chunking
- microscale-robotics
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Mag-VLA: Vision-Language-Action Model for Bimanual Magnetically Actuated Microrobot Manipulation

## Summary
Mag-VLA adapts a 7B vision-language model to control two magnet-mounted micromanipulators for microscale bimanual manipulation. It predicts phase-aware, multi-step dual-arm motion from microscope images, language instructions, and arm positions.

## Problem
- Magnetically actuated microrobots are hard to control because motion comes from indirect magnetic fields, with limited microscope sensing and nonlinear coupling between actuator motion and microrobot motion.
- Bimanual magnetic control can reorient and transport objects in ways a single arm cannot, but the two arms must move together in a shared workspace.
- Better autonomy matters for minimally invasive and microscale manipulation tasks where teleoperation is slow and high precision is required.

## Approach
- The system fine-tunes Qwen2.5-VL-7B with LoRA, using four RGB microscope frames, a language prompt, and the current 2D positions of the left and right magnet arms.
- A motion-aware phase classifier predicts whether the task is in the approach phase or transport phase.
- The predicted phase conditions an Action Chunking Transformer decoder, which outputs five future dual-arm action deltas in one pass: ΔxL, ΔyL, ΔxR, and ΔyR.
- During deployment, overlapping action chunks are blended with temporal ensembling to smooth receding-horizon control.
- Training uses 75 teleoperated episodes, 20,724 RGB frames, three task configurations, and 70 prompt variants.

## Results
- In real-robot tests, Mag-VLA achieves 90% approach success on Tasks A, B, and C.
- Transport success falls as path curvature increases: 80% on Task A, 70% on Task B, and 50% on Task C.
- With Qwen2.5-VL-7B fixed, the ACT action head reaches 79.56 ticks overall RMSE, versus 153.52 for Diffusion Policy and 140.50 for Flow Matching.
- ACT also improves endpoint error: 133.74 ticks mean and 107.82 ticks median, versus 275.96/260.79 for Diffusion Policy and 265.75/251.25 for Flow Matching.
- ACT reports 98.26% direction accuracy and 0.791 mean cosine similarity, higher than the diffusion and flow action heads reported in the paper.
- The phase head reaches 97.21% overall phase accuracy with ACT, with 97.36% on approach and 97.04% on transport.

## Link
- [https://arxiv.org/abs/2605.28486v1](https://arxiv.org/abs/2605.28486v1)
