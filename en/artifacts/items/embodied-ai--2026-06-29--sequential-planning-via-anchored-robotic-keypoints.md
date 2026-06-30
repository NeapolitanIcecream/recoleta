---
source: arxiv
url: https://arxiv.org/abs/2606.30613v1
published_at: '2026-06-29T17:48:01'
authors:
- Bryce Grant
- Aryeh Rothenberg
- Logan Senning
- Zonghe Chua
- Zach Patterson
- Peng Wang
topics:
- robot-manipulation
- vision-language-action
- behavior-trees
- open-vocabulary-perception
- test-time-compute
- sim2real
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Sequential Planning via Anchored Robotic Keypoints

## Summary
Spark is a training-free neurosymbolic robot manipulation system that uses one LLM-planned behavior tree and spends extra test-time compute on object grounding. It reports 43.7% mean success on six Libero-Pro position/task cells and 68% mean success across 11 physical robot task cells.

## Problem
- Vision-language-action policies that score 95%+ on standard LIBERO fall close to 0% on Libero-Pro position and task perturbations because they often bind actions to fixed scene layouts.
- CaP-Agent0 recovers some performance with multi-turn code generation, but it uses about 9 frontier-model calls per turn and rewrites plans after failures.
- The paper targets the failure mode where the plan is still valid, but the robot needs to re-find objects after positions or task wording change.

## Approach
- Gemini writes a YAML behavior tree in one planning call. The tree contains typed robot actions rather than raw Python control code.
- Five base primitives, including move_to_keypoint, move_relative, grasp, release, and wait, compose into longer manipulation skills. The controller handles IK, grasping, depth geometry, and post-condition checks outside the LLM plan.
- SAM3 grounds text labels to object masks and 3D keypoints using RGB-D cameras. Each action resolves its object label to the latest detected 3D position at execution time.
- In simulation, a second Gemini call proposes 3 alternative text prompts per object. SAM3 scores the prompts, and Spark keeps the prompt-label pair with the cleanest confident detection.
- If a primitive fails, Spark first perturbs or retries contact, then retracts 10 cm, re-runs SAM3, and retries the same behavior tree without a new LLM call.

## Results
- On six Libero-Pro position/task cells, Spark Adaptive reports 43.7% mean success, versus CaP-Agent0 original at 18.2%, MolmoAct2 at 18.6%, pi_0.5 at 12.8%, and RATs at 43.8%.
- On the Libero-Pro spatial suite, Spark averages 64.2% across position and task perturbations, compared with RATs at 30.0%; the two Spark spatial cells are 56.0% and 72.4%.
- Adaptive perception adds +27.7 percentage points on the spatial suite and +10.0 points on the object suite compared with Spark Fair. It hurts goal-task perturbations by 8.4 points, falling from 22.4% to 14.0%.
- The recovery loop adds about +5 points overall on Libero-Pro by fixing first-frame SAM3 misses after retract-and-re-detect.
- On CaP-Bench pick-and-place tasks, Spark reaches Lift 100% versus about 100% for CaP-Agent0, Stack 97% versus about 95%, and CubeRestack 100% versus about 95%. It trails on Wipe at 60% versus about 85%, TwoArmLift at 63% versus about 70%, and TwoArmHandover at 24% versus about 30%.
- On physical robots, the same primitive grammar runs on UR10e, Franka FR3, and bimanual Franka setups with no retraining, averaging 68% success across 11 task-embodiment cells, 9 unique tasks, and 20 trials per cell.

## Link
- [https://arxiv.org/abs/2606.30613v1](https://arxiv.org/abs/2606.30613v1)
