---
source: arxiv
url: http://arxiv.org/abs/2603.05185v1
published_at: '2026-03-05T13:55:33'
authors:
- Pengfei Yi
- Yingjie Ma
- Wenjiang Xu
- Yanan Hao
- Shuai Gan
- Wanting Li
- Shanlin Zhong
topics:
- vision-language-action
- long-horizon-manipulation
- hierarchical-control
- anomaly-detection
- ood-generalization
- robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation

## Summary
This paper proposes a tri-system Vision-Language-Action (VLA) framework that introduces a visual Critic for dynamic scheduling between high-level VLM planning and low-level VLA control, improving real-time performance and robustness in long-horizon manipulation. The core idea is to activate the slow reasoning module only when needed, thereby achieving stronger performance under OOD disturbances, stagnation, and failure recovery.

## Problem
- Existing hierarchical VLA systems often rigidly chain together a **slow but semantically capable VLM** with a **fast but semantically weaker VLA**, leading to inflexible switching, wasted computation, and slow responses to disturbances.
- In long-horizon manipulation, robots are prone to **stagnation, misgrasping, dropping objects, and infinite retries**; relying on collecting dedicated data for each such failure scales poorly.
- This matters because real-world robots need both **high-level semantic planning** and **low-level real-time closed-loop control**, especially in complex, open, and OOD settings.

## Approach
- The paper proposes **Tri-System**: System 2 is the VLM “Brain” responsible for generating semantic subtasks, System 1 is the flow-matching “Cerebellum” responsible for continuous actions, and System 3 is a lightweight visual **Critic** that monitors execution and decides when to switch.
- The Critic unifies subtask evaluation as VQA text generation: it outputs either a **progress value** (discretizing completion into 101 bins corresponding to the interval [-1,0]) or the anomaly token **`<aci>`**, thereby handling both progress tracking and failure detection.
- Scheduling is **event-driven and asynchronous**: under normal conditions, the VLA continuously executes at around 20Hz; the VLM is triggered for replanning and the old action cache is cleared only when a **subtask is completed, an accident is detected, or prolonged stagnation occurs**.
- To break infinite retry loops, the system incorporates **human-inspired heuristic rules**: if the Critic finds that progress has not improved for a long time (e.g., maximum stagnation threshold `N_stag=180` frames), it resets the robot state and lets the Brain replan based on short-term memory.
- The paper also proposes an automatic subtask annotation pipeline: it first uses end-effector trajectories and gripper states for keyframe proposals, then uses a VLM to retrieve semantic labels, reducing the cost of manual segment-by-segment annotation.

## Results
- On the real-robot **Arrange the Tableware** task, Tri-System achieves **10/10, 9/10, 7/10, 7/10** in the four scenarios **Ordered / Scattered / Left cup / Fallen**, outperforming Single-System at **8/10, 0/10, 0/10, 2/10** and Dual-System at **7/10, 6/10, 1/10, 5/10**.
- On the more complex long-horizon **Tidy up the Desk** task, Tri-System achieves stage-wise success counts of **Open 9/10, Bottle1 8/10, Bottle2 5/10, Overall 4/10**; the corresponding Single-System results are **7/10, 5/10, 2/10, 0/10**, and Dual-System results are **6/10, 5/10, 1/10, 0/10**.
- The paper claims the method achieves **state-of-the-art** across all evaluation scenarios, especially in the OOD left-cup scenario, where the training data contains no left-arm samples for that task, yet Tri-System still reaches **7/10**, significantly higher than Dual-System’s **1/10** and Single-System’s **0/10**.
- At the system runtime level, the authors report key mechanism figures: the control/observation loop runs at about **20 Hz**; an example success threshold is **`τ_succ ≈ -0.041`**; the stagnation threshold is **`N_stag=180`**; and the Critic uses Florence-2-base with about **0.2B** parameters to support real-time asynchronous evaluation.
- For training data, **200** teleoperated trajectories are collected for each task; the tableware arrangement task additionally includes **100** trajectories for recovery after “the cup is knocked over.” Despite these data, the authors specifically emphasize that using the left arm for the left cup remains an **out-of-distribution** test.

## Link
- [http://arxiv.org/abs/2603.05185v1](http://arxiv.org/abs/2603.05185v1)
