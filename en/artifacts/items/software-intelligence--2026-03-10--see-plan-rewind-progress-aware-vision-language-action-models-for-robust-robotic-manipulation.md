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
- robotic-manipulation
- vision-language-action
- progress-awareness
- error-recovery
- ood-robustness
relevance_score: 0.53
run_id: materialize-outputs
language_code: en
---

# See, Plan, Rewind: Progress-Aware Vision-Language-Action Models for Robust Robotic Manipulation

## Summary
SPR is a progress-aware vision-language-action framework for robotic manipulation that decomposes language tasks into verifiable 2D spatial subgoals and automatically "rewinds" when progress becomes abnormal before continuing execution. Its value lies in improving robustness for long-horizon manipulation, out-of-distribution scenarios, and real robots, without requiring additional failure data or auxiliary models.

## Problem
- Existing robotic VLA methods can usually “see and act,” but lack **explicit, actionable progress awareness** of what stage a task is in, causing errors to accumulate in long tasks.
- Many progress monitoring signals are abstract text descriptions or binary labels and **lack spatial grounding**, making it hard to directly guide robot-arm actions or judge whether the task has truly advanced.
- Existing recovery methods often rely on additional failure data, manual prompt engineering, or auxiliary models, which are costly and adapt poorly to unseen scenarios.

## Approach
- Automatically decompose tasks from demonstrations into a sequence of **spatialized subtask milestones**: for grasping tasks, use changes in gripper open/close state to find boundaries; for other tasks, use Gemini-3 to annotate subtask intervals and semantic descriptions.
- Use **DINOv3 + SAM** to automatically extract the gripper’s 2D position, generating each subtask’s target coordinates and 1-5 trajectory waypoints from the current state to the next subgoal as training supervision.
- The model autoregressively outputs, in order: depth perception, remaining number of subtasks, each subtask’s semantics + 2D coordinates, the 2D trajectory to the next subgoal, and the final action; the core idea is “first determine how many steps remain, then move toward the nearest one.”
- Design a **Rewind** recovery mechanism: maintain the subtask counts from the most recent 4 steps and the planned trajectories from the most recent 8 steps; if the count keeps increasing or the trajectory remains completely unchanged for a long time, execution is considered failed or stuck.
- During recovery, no new model is introduced; instead, successful demonstrations are reversed to construct training data for “returning to the initial position.” Once an anomaly is detected at runtime, the system switches to a rewind instruction for a fixed number of steps (set to **N=3** in the paper), then resumes the original task.

## Results
- On **LIBERO**, SPR outperforms **MolmoAct**: the abstract reports an improvement of **5%**, while Table 2 in the main text shows an increase from **86.8%** to **90.6%** (+**3.8** percentage points); the joint-training version **Ours\*** reaches **91.8%**, another **1.2** percentage points above 90.6%.
- LIBERO category results (Table 2): **Spatial 92.4%**, **Object 93.0%**, **Goal 94.2%**, **Long 82.8%**; the joint-training version achieves **93.2% / 95.4% / 93.2% / 85.4%** respectively, with an average of **91.8%**.
- In the **LIBERO-Plus** out-of-distribution robustness test, SPR achieves the highest average success rate of **71.8%**, with an average performance drop of only **18.8%**; this is better than **OpenVLA-OFT 70.6%, drop 27.0%** and **UniVLA 57.7%, drop 37.5%**.
- Success rates under each LIBERO-Plus perturbation are: **Background 86.0%**, **Robot 47.7%**, **Language 78.5%**, **Layout 69.6%**, **Light 85.0%**; the corresponding performance drops are **4.6% / 42.9% / 12.1% / 21.0% / 5.6%**.
- On 3 real-robot tasks, compared with **MolmoAct**’s **50% / 0% / 0%**, SPR reaches **70% / 30% / 40%** (Pick up / Tidy up / Push-T), indicating greater robustness on long-horizon tidying and continuous-contact pushing tasks as well.
- The paper also claims that this closed-loop error-correction capability **requires no additional training data or auxiliary models**, relying mainly on spatial-subgoal progress monitoring and a rewind strategy constructed from reversed demonstrations.

## Link
- [http://arxiv.org/abs/2603.09292v1](http://arxiv.org/abs/2603.09292v1)
