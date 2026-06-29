---
source: arxiv
url: https://arxiv.org/abs/2605.20811v1
published_at: '2026-05-20T07:05:49'
authors:
- Jingyang He
- Guangrun Li
- Jieyu Zhang
- Chengkai Hou
- Zhengping Che
- Shanghang Zhang
topics:
- cross-embodiment-imitation
- world-models
- latent-planning
- robot-manipulation
- jepa
- one-shot-imitation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Demo-JEPA: Joint-Embedding Predictive Architecture for One-shot Cross-Embodiment Imitation

## Summary
Demo-JEPA turns a visual demonstration from another embodiment into latent subgoals that a target robot can plan toward with its own dynamics model. It reports stronger cross-embodiment and zero-shot results than VPP and XSkill, while in-domain behavior grounding remains mixed.

## Problem
- It addresses one-shot cross-embodiment imitation, where a target robot must follow a human or different robot using visual demonstrations without shared actions.
- The problem matters because morphology, kinematics, and action spaces differ across robots, so action copying and manual retargeting can fail or require costly paired data.
- The target use case is a robot that learns from source videos and its own interaction data, then executes the task with its own controller.

## Approach
- A V-JEPA-style encoder maps observations into predictive latent states, reducing reliance on pixels or source actions.
- The Dreamer Predictor takes the current target observation and a source demonstration frame pair, then predicts a target-compatible future latent goal.
- Cross-attention modules estimate source-target correspondence and source motion; a 3D convolution fuses these features; a transformer predicts the latent goal.
- The target robot uses its own action-conditioned world model and Cross-Entropy Method planning to find actions whose predicted latent rollout reaches the inferred goal.
- Training uses Stage I latent goal prediction from paired visual trajectories and Stage II action co-training to align the target dynamics model with Dreamer Predictor goals.

## Results
- Simulation training used 86 Stage I tasks with 13,444 trajectories and 39 Stage II tasks with 8,324 trajectories; real-world training used 22 Stage I tasks with 4,508 trajectories and 19 Stage II tasks with 3,903 trajectories.
- In RLBench simulation behavior grounding, Demo-JEPA averaged 0.31 success, below VPP at 0.47 and XSkill at 0.39.
- In simulation cross-embodiment bridging, Demo-JEPA averaged 0.45 success, above VPP at 0.28 and XSkill at 0.17.
- In simulation zero-shot generalization, Demo-JEPA averaged 0.36 success, above VPP at 0.04 and XSkill at 0.03.
- In real-world behavior grounding, Demo-JEPA averaged 0.43 success, below VPP at 0.65 and close to XSkill at 0.45.
- In real-world transfer settings, Demo-JEPA averaged 0.55 on cross-embodiment bridging versus VPP 0.53 and XSkill 0.40, and 0.25 on zero-shot generalization versus VPP 0.00 and XSkill 0.05.

## Link
- [https://arxiv.org/abs/2605.20811v1](https://arxiv.org/abs/2605.20811v1)
