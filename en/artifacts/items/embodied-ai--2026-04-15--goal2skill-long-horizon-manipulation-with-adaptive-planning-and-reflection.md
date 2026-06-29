---
source: arxiv
url: http://arxiv.org/abs/2604.13942v1
published_at: '2026-04-15T14:53:09'
authors:
- Zhen Liu
- Xinyu Ning
- Zhe Hu
- Xinxin Xie
- Weize Li
- Zhipeng Tang
- Chongyu Wang
- Zejun Yang
- Hanlin Wang
- Yitong Liu
- Zhongzhu Pu
topics:
- vision-language-action
- long-horizon-manipulation
- robot-planning
- memory-augmented-policy
- adaptive-replanning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection

## Summary
Goal2Skill targets long-horizon robot manipulation by splitting planning from control and adding memory, verification, and failure recovery. The paper claims this closed-loop design improves success on RMBench tasks where reactive VLA policies often fail.

## Problem
- Existing vision-language-action policies usually act from short observation windows and direct action prediction, which makes them fragile on long tasks with partial observability, occlusion, distractors, and multi-stage dependencies.
- Long-horizon manipulation needs the robot to remember prior outcomes, break a goal into sub-tasks, check whether each step worked, and recover when execution goes off track.
- This matters because locally reasonable actions can still ruin a multi-step task when the system lacks memory and explicit correction.

## Approach
- The method uses two modules: a high-level VLM planner and a low-level VLA executor. The planner decides what sub-task to do next; the executor turns that sub-task into continuous motor actions.
- The planner keeps structured memory with episodic history, a compact working-memory summary, and an error register. It uses this memory to decompose the goal, track progress, verify post-conditions, and decide whether to continue, retry, or replan.
- Each sub-task includes a language instruction, pre/post-conditions, an execution horizon, distractor regions, and a selected primitive skill index.
- The executor applies geometry-preserving visual filtering: the planner predicts task-irrelevant regions, a segmentation model masks them, and the VLA policy acts on the filtered image plus proprioception and the sub-task instruction.
- When a step fails or times out, a reflection module diagnoses the cause and picks a recovery action such as retrying, adjusting parameters like grasp hints or distractor constraints, or rebuilding the rest of the plan.

## Results
- On five RMBench tasks, Goal2Skill reaches **32.4% average success rate**, compared with **9.8%** for the strongest baseline.
- On memory-intensive **M(n)** tasks, it reaches **38.7%** success versus **9.0%** for the best competing method.
- The paper states that ablations show **structured memory** is a main source of gains on memory-sensitive tasks.
- It also states that **verification plus reflection** improves robustness on failure-prone tasks.
- The excerpt does not provide the full ablation tables, per-task scores, variance, or baseline names, so the quantitative evidence available here is limited to the headline success-rate comparisons.

## Link
- [http://arxiv.org/abs/2604.13942v1](http://arxiv.org/abs/2604.13942v1)
