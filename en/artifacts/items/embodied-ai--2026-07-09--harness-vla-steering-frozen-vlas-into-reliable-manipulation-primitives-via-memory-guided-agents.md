---
source: arxiv
url: https://arxiv.org/abs/2607.08448v1
published_at: '2026-07-09T13:08:54'
authors:
- Yixian Zhang
- Huanming Zhang
- Feng Gao
- Xiao Li
- Zhihao Liu
- Chunyang Zhu
- Jiaxing Qiu
- Yuchen Yan
- Jiyuan Liu
- Wenhao Tang
- Zhengru Fang
- Yi Nie
- Changxu Wei
- Yu Wang
- Wenbo Ding
- Chao Yu
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- dexterous-manipulation
- robot-data-scaling
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents

## Summary
Harness VLA turns a frozen vision-language-action model into a reusable local manipulation primitive and uses a memory-guided planner to handle grounding, staging, transport, retries, and long-horizon composition. It improves robustness under instruction, layout, household, and clean-to-randomized perturbations without VLA fine-tuning or deployment-time expansion of the primitive library.

## Problem
- End-to-end VLAs often fail when object targets are re-bound, layouts change, tasks become longer, or contact attempts become unstable outside the training distribution.
- Analytic robot primitives handle transport and positioning well but struggle with irregular grasps, constrained placement, articulated objects, and other contact-rich actions.
- Reliable language-conditioned manipulation matters because deployment scenes and instructions vary, while a single failed contact can derail an entire task.

## Approach
- A planner selects calls from a fixed JSON primitive library instead of emitting low-level actions directly.
- Analytic primitives handle target grounding, free-space motion, wrist and gripper control, navigation, release, and re-staging.
- The frozen VLA is exposed through `vla_act`, which performs short, retryable bursts for local contact-rich actions such as grasping, insertion, fixture actuation, and constrained placement.
- Task-specific memory stores successful primitive traces with symbolic spatial queries; global memory stores reusable success rules and failure models, including empty-grasp and false-success cases.
- The planner bootstraps on one reference task instance, then re-grounds the stored trace on held-out layouts and seeds without adding new primitives or fine-tuning the VLA.

## Results
- On standard LIBERO, Harness VLA with Claude Code reaches 96.0% overall success, or 384/400 trials, compared with 95.3% for the frozen RLinf VLA baseline.
- On LIBERO-Pro perturbations, Harness VLA reaches 82.4% overall with Claude Code and 72.1% with Codex. The Claude Code result is 38.6 percentage points above the strongest reported prior baseline, RATS at 43.8%, and 32.4 points above the direct RLinf baseline at 50.0%.
- On RoboCasa365, Harness VLA with Codex reaches 55.4% overall versus 30.0% for RLDX-1, a 25.4-point improvement. It reaches 91.6% on Atomic-Seen and 56.3% on Composite-Seen.
- On RoboTwin clean-to-randomized transfer, the paper reports 58.4% success.
- The reported gains support the claim that planner-controlled staging and retries extend a frozen VLA beyond its original trajectory distribution, although the excerpt does not provide a complete ablation of every memory and primitive component.

## Link
- [https://arxiv.org/abs/2607.08448v1](https://arxiv.org/abs/2607.08448v1)
