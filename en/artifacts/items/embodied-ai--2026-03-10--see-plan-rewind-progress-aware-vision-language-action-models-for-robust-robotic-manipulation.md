---
source: arxiv
url: http://arxiv.org/abs/2603.09292v1
published_at: '2026-03-10T07:22:51'
authors:
- Tingjun Dai
- Mingfei Han
- Tingwen Du
- Zhiheng Liu
- Zhihui Li
- Salman Khan
- Jun Yu
- Xiaojun Chang
topics:
- vision-language-action
- robot-manipulation
- progress-monitoring
- failure-recovery
- ood-robustness
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# See, Plan, Rewind: Progress-Aware Vision-Language-Action Models for Robust Robotic Manipulation

## Summary
SPR is a progress-aware vision-language-action framework for robotic manipulation that decomposes language tasks into verifiable 2D spatial subgoals and triggers “rewind” recovery when progress becomes abnormal. It aims to improve manipulation success rate, OOD robustness, and real-robot recovery capability without adding failure data or auxiliary models.

## Problem
- Existing VLA robotic policies can usually “see and act,” but lack an explicit, actionable representation of **task progress**, leading to error accumulation in long-horizon manipulation and making recovery difficult once the agent gets stuck.
- Many progress-monitoring methods provide only abstract textual reasoning or binary signals, lacking **spatially grounded** intermediate goals that are directly useful for robot actions.
- Existing failure-recovery solutions often rely on additional failure data, hand-crafted rules, or auxiliary models, which are costly and have limited adaptability in unseen scenarios.

## Approach
- SPR organizes task execution into a closed-loop **See-Plan-Rewind** process: it first predicts the remaining subtasks and their 2D coordinates, then plans a 2D trajectory to the next subgoal, and finally executes a rewind when an anomaly is detected.
- It automatically decomposes demonstration data into a sequence of **spatial subgoals**: for grasping tasks, subtask boundaries are identified using gripper open/close changes; for other tasks, Gemini-3 is used to annotate segments and semantic descriptions.
- To obtain supervision for subgoals and trajectories, the method uses **DINOv3 + SAM** to automatically localize the gripper and extract discretized 2D waypoints and 1–5 intermediate trajectory points from demonstrations.
- The model generates autoregressively: depth tokens, the number of remaining subtasks, the semantics + 2D coordinates of each subtask, the 2D trajectory to the next subgoal, and the final action tokens.
- The rewind mechanism requires no additional recovery data: the authors reverse successful demonstrations into “return to initial position” data, and use a state recorder to monitor the recent 4-step subtask counts and 8-step trajectories; if the count keeps increasing or the trajectory remains unchanged for too long, a fixed-duration rewind is triggered (empirically set to **N=3**).

## Results
- On **LIBERO**, SPR achieves an average success rate of **90.6%**, improving over **MolmoAct 86.8%** by **3.8 percentage points**; category scores are Spatial **92.4%**, Object **93.0%**, Goal **94.2%**, and Long **82.8%**.
- Under the jointly trained one-policy-for-all setting, SPR (Ours*) reaches **91.8%**, a further **1.2 percentage point** improvement over the separately trained version at **90.6%**; among these, Long reaches **85.4%**.
- On the **LIBERO-Plus** OOD benchmark, SPR achieves an average success rate of **71.8%**, with an average performance drop of only **18.8%**, outperforming **OpenVLA-OFT 70.6% / ↓27.0%** and **UniVLA 57.7% / ↓37.5%**; the paper therefore claims a new SOTA in robustness.
- By perturbation type, SPR achieves the following on LIBERO-Plus: Background **86.0% (↓4.6%)**, Robot **47.7% (↓42.9%)**, Language **78.5% (↓12.1%)**, Layout **69.6% (↓21.0%)**, Light **85.0% (↓5.6%)**.
- On 3 real-robot tasks, compared with MolmoAct, SPR improves from **50%→70%** (Pick up), **0%→30%** (Tidy up), and **0%→40%** (Push-T), indicating that its recovery mechanism is more effective for long-horizon and continuous-contact tasks.
- The paper also claims that the method enables closed-loop error correction and stronger generalization **without additional training data or auxiliary models**, but the excerpt does not provide more detailed ablation numbers.

## Link
- [http://arxiv.org/abs/2603.09292v1](http://arxiv.org/abs/2603.09292v1)
