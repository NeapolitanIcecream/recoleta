---
source: arxiv
url: https://arxiv.org/abs/2606.27079v1
published_at: '2026-06-25T14:19:36'
authors:
- Mingyang Lyu
- Yinqian Sun
- Yiyang Jia
- Sicheng Shen
- Moquan Sha
- Huangrui Li
- Feifei Zhao
- Yi Zeng
topics:
- vision-language-action
- robot-safety
- vla-benchmark
- embodied-evaluation
- manipulation-safety
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models

## Summary
ForesightSafety-VLA is a safety benchmark for vision-language-action robot policies. It tests whether a policy can finish manipulation tasks without unsafe contacts, risky proximity, bad sequencing, or failures triggered by language and visual changes.

## Problem
- Current VLA benchmarks often score task success while missing unsafe execution, such as hitting nearby objects, entering hot zones, violating clearance margins, or completing a task after risky motion.
- This matters for robot deployment because a policy can succeed at the instruction and still cause injury, damage, spills, or unsafe human-robot interaction.
- Existing safety checks are often sparse endpoint checks; this benchmark measures risk during the whole trajectory.

## Approach
- The benchmark defines 13 safety categories across Safe-Core physical safety, Safe-Lang instruction safety, and Safe-Vis perception safety.
- It builds 66 safety-augmented RoboTwin scenarios across 5 robot embodiments by adding hazards, tightening constraints, and inserting temporal preconditions.
- It varies three inputs separately: scene structure (L0-L2), language command (W0-W4), and visual observation (V0-V4), so failures can be tied to layout, wording, or perception.
- It scores each rollout with four outcomes: safe success, unsafe success, safe failure, and unsafe failure.
- It adds process metrics: cumulative safety cost (CC), risk exposure time (RET), and safety-adjusted success rate (SASR).

## Results
- On four completed baselines, no model reaches zero risk: CC ranges from 0.18 to 0.39, unsafe success rate ranges from 0.06 to 0.12, and unsafe failure rate ranges from 0.15 to 0.37.
- OpenVLA-oft is the best reported baseline with SSR 0.42, USR 0.06, SFR 0.37, UFR 0.15, CC 0.18, and SASR 0.35.
- ACT is the weakest completed baseline with SSR 0.20, USR 0.12, SFR 0.31, UFR 0.37, CC 0.39, and SASR 0.12.
- RDT reports SSR 0.30, USR 0.10, UFR 0.26, CC 0.29, and SASR 0.22; DP reports SSR 0.24, USR 0.10, UFR 0.32, CC 0.34, and SASR 0.16.
- Among successful episodes, the unsafe share is 12.5% for OpenVLA-oft, 25.0% for RDT, 29.4% for DP, and 37.5% for ACT.
- In the Safe-Core suite breakdown, ACT reaches CC 0.54 on Thermal/Energy, while OpenVLA-oft ranges from CC 0.14 on Temporal Sequence to CC 0.26 on Thermal/Energy; the paper also claims structure and visual variation degrade safety more than ordinary language variation.

## Link
- [https://arxiv.org/abs/2606.27079v1](https://arxiv.org/abs/2606.27079v1)
