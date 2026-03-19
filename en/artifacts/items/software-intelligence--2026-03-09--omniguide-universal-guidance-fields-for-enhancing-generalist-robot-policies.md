---
source: arxiv
url: http://arxiv.org/abs/2603.10052v1
published_at: '2026-03-09T17:18:13'
authors:
- Yunzhou Song
- Long Le
- Yong-Hyun Park
- Jie Wang
- Junyao Shi
- Lingjie Liu
- Jiatao Gu
- Eric Eaton
- Dinesh Jayaraman
- Kostas Daniilidis
topics:
- robotics
- vision-language-action
- test-time-guidance
- flow-matching
- collision-avoidance
- semantic-grounding
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# OmniGuide: Universal Guidance Fields for Enhancing Generalist Robot Policies

## Summary
OmniGuide is a unified framework that enhances generalist robot policies at inference time by using 3D guidance fields provided by external perception/foundation models to “push” or “pull” action sampling. It can improve VLA performance on complex manipulation, obstacle avoidance, and fine-grained semantic localization tasks without requiring additional robot data or retraining.

## Problem
- Existing vision-language-action (VLA) models cover a broad range of tasks, but they often suffer from “last-mile” failures in complex spatial understanding, manipulation in cluttered environments, fine manipulation, and safe obstacle avoidance.
- Traditional remedies usually rely on additional high-quality robot data from the target environment and post-training/fine-tuning, which are costly and scarce.
- Different external capability sources (3D geometry, VLM semantic reasoning, human demonstrations) are powerful, but there is a lack of a unified, composable, retraining-free way to guide VLAs in real time.

## Approach
- Core idea: represent various forms of external guidance in a unified way as **differentiable energy functions** defined in 3D space, where target points create attractive fields and obstacles create repulsive fields, then backpropagate these gradients into the action generation process.
- For flow-matching / diffusion-based VLAs, at each denoising step the method first estimates a “clean action,” then maps the action to a robot Cartesian trajectory through differentiable kinematics/dynamics, computes task energy, and uses its gradient to correct the original generated vector field.
- The framework supports multiple guidance sources: SDF-based collision avoidance, semantic target localization obtained via VLM + depth back-projection, and one-shot attractive trajectories extracted from human demonstrations via hand pose estimation.
- It can also perform energy-based filtering on the initial noise distribution and combine this with intermediate denoising guidance, to better balance the “action naturalness prior” against task/safety constraints.

## Results
- The paper claims significant improvements across simulation and real-world environments, across multiple types of guidance sources, and across two SOTA generalist policies (e.g., **π0.5**, **GR00T N1.6**).
- The strongest quantitative results given in the paper are: **success rate improved from 24.2% to 92.4%**, and **collision-free/safety rate improved from 7.0% to 93.5%**; it also states **no significant execution latency** and **no retraining required**.
- The authors also claim that this unified framework **matches or exceeds** prior methods designed specifically for particular guidance sources, but the provided excerpt does not include more detailed tables, task-by-task breakdowns, error bars, or significance test values.
- The simulation experiments are based on **RoboCasa**, and use **NVIDIA GR00T N1.6-3B** as one of the backbone policies; the excerpt also indicates that real-robot experiments were conducted, but does not provide more complete per-task quantitative results.

## Link
- [http://arxiv.org/abs/2603.10052v1](http://arxiv.org/abs/2603.10052v1)
