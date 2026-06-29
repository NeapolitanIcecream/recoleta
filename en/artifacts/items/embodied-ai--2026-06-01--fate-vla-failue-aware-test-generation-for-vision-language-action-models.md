---
source: arxiv
url: https://arxiv.org/abs/2606.02307v1
published_at: '2026-06-01T14:27:13'
authors:
- Arusa Kanwal
- Pablo Valle
- Shaukat Ali
- Aitor Arrieta
topics:
- vision-language-action
- robot-evaluation
- failure-discovery
- adaptive-testing
- surrogate-guided-testing
- embodied-ai
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# FATE-VLA:Failue-aware test generation for vision-language-action models

## Summary
FATE-VLA is an adaptive test generator for Vision-Language-Action robot policies that searches for failure-prone and diverse manipulation scenes. It reports higher failure discovery than random sampling and diversity-only adaptive random testing on four VLA models in SimplerEnv.

## Problem
- It solves the problem of weak VLA evaluation: fixed or randomly sampled task scenes can miss rare, clustered failures in high-dimensional robot scene spaces.
- This matters because a robot policy can look safe on a static benchmark while failing in specific object, position, orientation, or instruction conditions.
- The paper also measures whether discovered failures are diverse across trajectories and objects, not just how many failures occur.

## Approach
- The core method generates candidate manipulation scenes, executes one on the VLA policy, records success or failure, then uses the growing log to guide the next test.
- One variant combines FSCS-ART diversity selection with a surrogate classifier that predicts whether a candidate scene will fail.
- A second variant uses a Random Forest to estimate failure probability and scores each candidate with `score = alpha * p_fail + (1 - alpha) * normalized_distance`.
- The test space includes object choice, position, and orientation. The experiments use 7 objects and SimplerEnv workspace ranges of `x = [-0.5, -0.05]` and `y = [0.0, 0.4]`.
- The evaluated VLA models are OpenVLA, pi0, GR00T-N1.6, and EO-1, using the SimplerEnv pick-up task with 10 runs per configuration.

## Results
- Across non-ceiling VLA models, the proposed methods improve failure rate by 14-30 percentage points over random testing and 13-29 percentage points over FSCS-ART.
- On GR00T-N1.6, the best method raises failure rate from 35.6% with random testing and 36.5% with FSCS-ART to 65.3% with Sorting_RF. The paper also states this as success rate dropping from 64.4% to 34.7%.
- On EO-1, failure rate rises from 36.7% with random testing and 38.0% with FSCS-ART to 60.0% with Sorting_RF, a gain of +23.3 and +22.0 percentage points.
- On EO-1, trajectory coverage improves from 82.8% with random testing and 81.5% with FSCS-ART to 84.0% with Sorting_DT.
- On GR00T-N1.6, trajectory coverage under failure improves from 78.2% with random testing and 79.9% with FSCS-ART to 83.0% with Sorting_RF.
- Failed object coverage on EO-1 reaches 98.6% with Weighted_RF, compared with 96.1% for random testing and 98.6% for FSCS-ART.

## Link
- [https://arxiv.org/abs/2606.02307v1](https://arxiv.org/abs/2606.02307v1)
