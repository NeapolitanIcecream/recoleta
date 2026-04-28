---
source: arxiv
url: http://arxiv.org/abs/2604.16788v1
published_at: '2026-04-18T02:25:30'
authors:
- Xueyao Chen
- Jingkai Jia
- Tong Yang
- Yibo Fu
- Wei Li
- Wenqiang Zhang
topics:
- robot-benchmark
- long-horizon-manipulation
- real-world-evaluation
- vision-language-action
- context-dependent-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks

## Summary
LongBench is a real-world benchmark for long-horizon robotic manipulation that separates two kinds of difficulty: long execution under full observability and long-context reasoning under ambiguity. It evaluates six current policies on more than 1,000 real-world episodes and shows that long-horizon failure has multiple causes rather than one single bottleneck.

## Problem
- Existing long-horizon manipulation benchmarks are often simulation-only or report only aggregate success, so they do not show why a policy fails over long real-world rollouts.
- Long-horizon tasks mix different sources of difficulty: execution drift, phase-transition errors, missed timing windows, and cases where the current view is ambiguous and earlier context is required.
- This matters because short-horizon or aggregate metrics can hide the actual weakness of a robot policy, which makes model comparison and progress on long-horizon manipulation less reliable.

## Approach
- The paper introduces **LongBench**, a real-world benchmark with **10 tasks** and **over 1,000 real-world episodes/demonstrations**, collected on an **ARX-R5 6-DoF** tabletop setup with **two RGB cameras** at **320x240** and **20 Hz**.
- It splits tasks into two regimes: **Context-Independent** tasks, where the next action is determined from the current observation, and **Context-Dependent** tasks, where visually similar states require memory of earlier context.
- The benchmark further labels tasks by mechanism. Context-Independent tasks are grouped by **phase dependence (PD)**, **iterative progress (IP)**, **error accumulation (EA)**, and **temporal windows (TW)**. Context-Dependent tasks are grouped by **completion ambiguity (CP)**, **count ambiguity (CT)**, **subtask-branch ambiguity (SB)**, and **cross-episode ambiguity (CE)**.
- Evaluation uses a **stage-wise score** rather than binary success: if a task has **N** atomic sub-steps, each finished sub-step gives **100/N** points. Each task is tested on **10 episodes** with distinct initializations.
- The benchmark compares **six policies** under a unified interface: **pi_0, OpenVLA-OFT, SmolVLA, Diffusion Policy, MemoryVLA, and CronusVLA**, all using **16-step open-loop action chunks**.

## Results
- On **Context-Independent** tasks, **pi_0** is the strongest model with **86.3** average stage-wise score, ahead of **Diffusion Policy 51.2**, **MemoryVLA 49.1**, **SmolVLA 46.6**, **CronusVLA 42.4**, and **OpenVLA-OFT 32.7**.
- Task-level Context-Independent scores for **pi_0** are **100.0** on *waste sorting*, **72.0** on *thread rope*, **95.0** on *pull drawer*, **91.3** on *stack block*, and **73.3** on *dynamic grasping*.
- The hardest fully observable task in the shown results is **dynamic grasping**, a temporal-window task. Scores drop to **0.0** for **OpenVLA-OFT**, **10.0** for **SmolVLA**, **13.3** for **Diffusion Policy**, **10.0** for **MemoryVLA**, and **13.3** for **CronusVLA**, while **pi_0** reaches **73.3**.
- The paper claims that long-horizon performance is not explained by one factor. In fully observable settings, execution robustness drives results more than explicit memory, and **memory-based methods do not consistently solve contextual difficulty** across tasks.
- The excerpt does **not** provide the quantitative table for **Context-Dependent** task scores, so no numeric benchmark results for that regime are available here.

## Link
- [http://arxiv.org/abs/2604.16788v1](http://arxiv.org/abs/2604.16788v1)
