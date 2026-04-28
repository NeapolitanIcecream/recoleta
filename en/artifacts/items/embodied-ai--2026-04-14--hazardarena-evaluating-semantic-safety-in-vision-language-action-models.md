---
source: arxiv
url: http://arxiv.org/abs/2604.12447v1
published_at: '2026-04-14T08:32:02'
authors:
- Zixing Chen
- Yifeng Gao
- Li Wang
- Yunhan Zhao
- Yi Liu
- Jiayu Li
- Xiang Zheng
- Zuxuan Wu
- Cong Wang
- Xingjun Ma
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-safety
- benchmarking
- semantic-grounding
- embodied-ai
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models

## Summary
HazardArena is a benchmark for testing whether vision-language-action models understand when an action is unsafe even if they can execute it. The paper shows that safe-only fine-tuning often improves task skill and unsafe behavior at the same time, then proposes a training-free guard layer to block some risky actions.

## Problem
- Current VLA evaluations focus on task completion or trajectory success, so they miss cases where a model performs the right motion in the wrong semantic context.
- This matters because a robot can execute a learned action template such as pouring or inserting while ignoring risk-critical meaning in the scene or instruction, which can cause property, electrical, fire, privacy, chemical, food, or personal safety harm.
- Existing safety scores can also be misleading: a weak policy may look safe because it fails to act, not because it recognized the hazard.

## Approach
- The paper builds **HazardArena**, a benchmark with safe/unsafe twin scenarios. Each twin pair keeps the same objects, layout, skill template, and motor demands, and changes only the semantic factor that makes the action allowed or unsafe.
- HazardArena contains **40 risk-sensitive tasks**, **7 hazard categories**, **over 80 new household assets**, and **over 2,000 assets** in total according to the abstract and benchmark description.
- The evaluation uses stage-wise metrics beyond final success: **attempt_rate**, **commit_rate**, and **success_rate**. `commit` means the policy reached a task-specific pre-hazard configuration where unsafe completion is close.
- Models are fine-tuned only on safe demonstrations: **600 trajectories total**, from **6 safe tasks** with **100 trajectories each**. Unsafe twins are held out from training.
- To reduce unsafe execution without retraining, the paper adds a **Safety Option Layer (SOL)** at inference time. SOL either applies hand-written semantic attribute rules or asks an external vision-language judge whether to block the proposed action and replace it with a refusal action.

## Results
- Across four VLA models, higher safe-task performance usually came with higher unsafe completion on matched unsafe twins. For **pi_0**, `insert outlet` rose from **0.08 to 0.47** on safe twins and from **0.02 to 0.44** on unsafe twins from early to final checkpoints. For **NORA**, the same task rose from **0.10 to 0.39** safe and **0.12 to 0.34** unsafe.
- The same trend appears on other tasks. For **VLA-Adapter**, `spike drinkware` improved from **0.05 to 0.21** safe and **0.01 to 0.19** unsafe; `pour electronics` improved from **0.00 to 0.14** safe and **0.00 to 0.15** unsafe.
- Stage-wise metrics show that endpoint success understates risk. For **pi_0** on unsafe `insert outlet`, **attempt = 0.93**, **commit = 0.80**, **success = 0.44**. On unsafe `contaminate dogbowl`, **attempt = 0.67**, **commit = 0.42**, **success = 0.18**. The policy often gets close to hazard completion even when final success fails.
- Stage-wise metrics also change model comparisons. On unsafe `insert outlet`, **NORA** has lower unsafe success than **VLA-Adapter** (**0.34 vs 0.37**) but higher hazardous commit (**0.62 vs 0.48**), which means it progresses further into the unsafe action despite slightly lower terminal completion.
- Quantitative SOL results are only partially visible in the provided excerpt. The paper claims the training-free SOL reduces unsafe behavior with minimal impact on task performance, and that the rule-based **SOL-L1** is strong in the controlled benchmark setting, but the missing table or figure prevents a full numeric summary from the excerpt alone.

## Link
- [http://arxiv.org/abs/2604.12447v1](http://arxiv.org/abs/2604.12447v1)
