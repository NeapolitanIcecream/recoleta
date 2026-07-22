---
source: arxiv
url: https://arxiv.org/abs/2607.18709v1
published_at: '2026-07-21T05:05:01'
authors:
- Ziqin Wang
- Hao Li
- Weijun Wang
- Junhao Cai
- Jia Zeng
- Yilun Chen
- Jiangmiao Pang
- Si Liu
topics:
- robot-foundation-model
- embodied-world-model
- vision-language-action
- robot-data-scaling
- robotic-manipulation
relevance_score: 0.99
run_id: materialize-outputs
language_code: en
---

# RoboInter1.5: A Holistic Intermediate Representation Suite for Embodied World Modeling and Robotic Manipulation

## Summary
RoboInter1.5 presents a unified dataset, benchmark, and model suite that uses dense intermediate representations to connect embodied reasoning, robotic manipulation, and world modeling. Its main resource contains over 230,000 manipulation episodes with synchronized spatial, temporal, and physical annotations.

## Problem
- Robot datasets are expensive, embodiment-specific, and usually pair observations only with instructions and low-level actions, leaving out the fine-grained structure needed for generalizable planning, control, and simulation.
- Sparse language or raw motor actions provide insufficient spatial and physical constraints, causing weak grounding and accumulated errors in long-horizon world-model rollouts.

## Approach
- RoboInter-Data annotates manipulation videos with more than 10 intermediate-representation types, including subtasks, primitive skills, object and gripper grounding, segmentation, affordances, grasp poses, contact points, placement proposals, and motion traces.
- RoboInter-VQA converts these annotations into spatial and temporal understanding and generation tasks, using a shared RoboInter-VLM Planner to predict intermediate representations.
- RoboInter-VLA uses the representations for implicit, explicit, and modular plan-then-execute action generation.
- RoboInter-World conditions future visual prediction on rendered object-point and gripper-trace control videos, providing structured spatial signals for long-horizon simulation.

## Results
- RoboInter-Data contains over 230,000 episodes from 571 scenes and 6 robot-arm types, with 15 primitive skills and dense per-frame annotations.
- The dataset includes nearly 61 million frames of object-grounding annotations, about 70 million frames of gripper traces, 190,000 affordance and placement annotations, and nearly 760,000 language clip annotations.
- RoboInter-VQA contains approximately 1 million spatial-generation entries, 172,000 spatial-understanding entries, 131,000 temporal-generation entries, and 935,000 temporal-understanding entries; 7,246 videos are reserved for evaluation-pool construction.
- RoboInter-CV contains 65,000 clip samples from 16,900 manipulation episodes covering DROID and RH20T, with aligned control videos, actions, language, observations, and future states.
- The excerpt reports improved planner reasoning, VLA performance and generalization, and more reliable long-horizon world-model predictions, but it does not provide downstream metric values or numerical comparisons against baselines.

## Link
- [https://arxiv.org/abs/2607.18709v1](https://arxiv.org/abs/2607.18709v1)
