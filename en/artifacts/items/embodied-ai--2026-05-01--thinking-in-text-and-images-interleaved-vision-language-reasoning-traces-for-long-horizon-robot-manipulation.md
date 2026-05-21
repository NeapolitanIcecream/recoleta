---
source: arxiv
url: https://arxiv.org/abs/2605.00438v1
published_at: '2026-05-01T06:15:43'
authors:
- Jinkun Liu
- Haohan Chi
- Lingfeng Zhang
- Yifan Xie
- YuAn Wang
- Long Chen
- Hangjun Ye
- Xiaoshuai Hao
- Wenbo Ding
topics:
- vision-language-action
- long-horizon-manipulation
- robot-foundation-model
- multimodal-reasoning
- visual-planning
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation

## Summary
IVLR adds an explicit full-task trace to a robot policy: each stage has a text subgoal and an RGB keyframe. The model generates this trace once, caches it, and uses it with live camera observations to choose actions.

## Problem
- Long-horizon manipulation needs correct step order and spatial targets; many VLA policies keep this plan hidden in model activations.
- Text-only plans can encode order but miss pose and contact details; visual prediction can show geometry but may miss the intended task sequence.
- This matters for multi-stage tasks where a robot can fail by handling objects in the wrong order or placing them in the wrong location.

## Approach
- IVLR uses a Show-o2 1.5B multimodal transformer to generate an IVLR-Trace from the initial image and instruction.
- Each trace stage pairs a caption with an RGB keyframe: the caption names the subgoal, and the keyframe shows the intended visual state.
- During execution, the cached trace, original instruction, and current observation feed an ACT token and an MLP action decoder that predicts continuous actions in closed loop.
- Since robot datasets lack these traces, the authors create pseudo-traces by segmenting demonstrations with Universal Visual Decomposer, taking segment endpoints as keyframes, and captioning stages with Qwen3-VL.
- Training combines next-token loss for text, flow-matching loss for visual keyframes, and L1 action loss, with trace noise and masking during training.

## Results
- On LIBERO, IVLR reports 95.5% average success, with 92.4% on LIBERO-Long. Compared baselines include VLA-0 at 94.7% average and 87.6% Long, CoT-VLA at 81.1% average and 69.0% Long, and π0-FAST at 85.5% average and 60.2% Long.
- LIBERO trace ablations show the main effect on long-horizon tasks: no trace reaches 37.7% on Long, text-only reaches 62.0%, vision-only reaches 68.4%, and full IVLR reaches 92.4%.
- On SimplerEnv-WidowX, IVLR reports 59.4% overall success, compared with 42.7% for SpatialVLA, 37.5% for RoboVLMs, and 29.5% for Octo-Small.
- Stress tests on LIBERO show 95.5% average success in the base setting, 92.1% after a 2 cm execution perturbation, 92.2% with 30% text trace masking, and 90.0% with 30% visual keyframe masking.
- The method has an upfront cost: full trace generation takes about 10 seconds on one NVIDIA H20 GPU, then cached execution runs at 10 Hz with action chunking.
- The paper reports simulated results only; it names static, fully observed environments, stale or wrong global plans, and initial planning latency as current limits.

## Link
- [https://arxiv.org/abs/2605.00438v1](https://arxiv.org/abs/2605.00438v1)
