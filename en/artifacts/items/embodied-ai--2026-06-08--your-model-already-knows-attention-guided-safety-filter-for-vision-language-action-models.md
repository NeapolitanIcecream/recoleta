---
source: arxiv
url: https://arxiv.org/abs/2606.09749v1
published_at: '2026-06-08T17:11:16'
authors:
- Seongbin Park
- Fan Zhang
- Baharan Mirzasoleiman
- Shahriar Talebi
- Nader Sehatbakhsh
topics:
- vision-language-action
- robot-safety
- control-barrier-functions
- attention-analysis
- collision-avoidance
- safe-libero
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Your Model Already Knows: Attention-Guided Safety Filter for Vision-Language-Action Models

## Summary
The paper claims that a frozen VLA policy already contains enough attention signal to identify its current target object, so a safety filter can avoid other objects without calling a separate VLM during control. The method adds a training-free wrapper around a VLA policy and reports large collision reductions on dynamic SafeLIBERO scenes.

## Problem
- VLA robot policies can complete manipulation tasks but may collide with task-irrelevant objects because their actions are not constrained by safety rules.
- Prior CBF safety filters often use a VLM or scene parser once at episode start to decide which object is the target and which objects are obstacles, so they fail when obstacles move.
- This matters for deployment in shared or changing scenes, where stale obstacle labels can turn a safe initial plan into a collision.

## Approach
- The authors find that a small number of attention heads in a frozen VLA attend to the object the policy is moving toward.
- At each control step, they read one selected attention head, project tracked object ellipsoids into the image, and assign attention mass to each object.
- The object with the highest attention density over a sliding window is treated as the active target; all other objects are treated as obstacles.
- A YOLOE segmentation tracker updates object positions online, while ellipsoid shapes are fit once at episode start.
- A discrete-time CBF-QP filter projects the VLA action to a nearby safe action that keeps the end-effector ellipsoid separated from obstacle ellipsoids.

## Results
- On SafeLIBERO Level III with moving obstacles, Knows reduces average collision rate from 70.75% for the init-only Naive filter to 26.88%, a 43.88 percentage-point drop across spatial, object, goal, and long suites.
- On the same dynamic Level III setting, average safe-success rate rises from 25.5% for Naive to 55.75% for Knows.
- Dynamic Level III safe-success improves over Naive in all four suites: spatial 54.5% vs 34.0%, object 70.5% vs 40.0%, goal 63.5% vs 9.5%, and long 34.5% vs 18.5%.
- Compared with no CBF on Level III, Knows cuts collision rate in spatial from 84.5% to 29.0%, in object from 48.5% to 14.0%, in goal from 90.0% to 30.5%, and in long from 82.0% to 34.0%.
- Runtime fits the 20 Hz control loop: total wrapper overhead is 49.3 ms per step, with attention extraction at 0.8 ms, YOLOE segmentation at 19.3 ms, depth plus centroid update at 9.1 ms, target identification at 9.4 ms, and OSQP safety solve at 11.4 ms.
- The selected attention head also predicts task outcome in 80 long episodes: early target mass reaches AUC 0.93, early target density reaches AUC 0.89, and density on the irrelevant destination is near chance at AUC 0.55.

## Link
- [https://arxiv.org/abs/2606.09749v1](https://arxiv.org/abs/2606.09749v1)
