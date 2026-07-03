---
source: arxiv
url: https://arxiv.org/abs/2607.01212v1
published_at: '2026-07-01T17:51:21'
authors:
- Chenyang Ma
- Yue Yang
- Radu Corcodel
- Siddarth Jain
- Andrew Wu
- Chiori Hori
- Diego Romeres
topics:
- vision-language-action
- bimanual-manipulation
- robot-furniture-assembly
- long-horizon-control
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model

## Summary
FurnitureVLA trains a vision-language-action policy for real-scale bimanual furniture assembly, using subtask progress prediction to handle long task horizons. It raises average simulated assembly success from 48% for a monolithic finetuned VLA to 80% across three IKEA-style furniture tasks.

## Problem
- Robot furniture assembly needs long sequences of precise actions; this paper tests tasks with 4 to 7 subtasks, 650 to 1550 control steps, and strict part alignment thresholds of 1 cm for small parts, 2 cm for large parts, and about 4 degrees per rotation axis.
- Prior work mostly covers toy-scale or single-arm assembly, so it does not address large parts that require two-arm coordination, reachability checks, and occlusion handling.
- A monolithic VLA can drift over long rollouts: small action errors move the robot into states that were rare or absent in training, which can make later subtasks fail.

## Approach
- The system decomposes each assembly into language-conditioned subtasks such as grasping, alignment, insertion, lifting, rotation, and retreat.
- The VLA predicts a 14-dimensional bimanual action for two Kinova Gen3 arms, plus a scalar progress value, giving a 15-dimensional output per step.
- Progress is continuous from 0 to 1 within each subtask and is assigned using action primitives; during inference, a progress threshold triggers the switch to the next subtask.
- Subtask boundaries are placed after the arms retreat from contact, so the next subtask starts from a more stable state than a contact-rich insertion state.
- The paper also builds an Isaac Gym simulation pipeline for expert demonstrations and a VR teleoperation setup for one operator to collect bimanual real-robot demonstrations.

## Results
- In simulation, zero-shot π0.5 gets 0.00 success on LACK, KALLAX, and IVAR; monolithic finetuning gets 0.91, 0.11, and 0.41; FurnitureVLA gets 0.98, 0.85, and 0.56.
- Average simulated full-assembly success improves from 0.48 for monolithic finetuning to 0.80 for FurnitureVLA, a 32-point gain across the three furniture types.
- The design-factor study reports average success of 0.80 for the best setting, compared with weaker settings such as 0.50 without the rear-camera setup, 0.47 for front-view depth replacement, and 0.60 at 224×224 input resolution.
- Temporal ensembling with λ = -0.1 gives the best average success in the reported sweep at 0.80, compared with 0.65 without ensembling and 0.75 with λ = -0.25.
- Data scaling improves success: 25% of demonstrations gives 0.50 average success, 50% gives 0.68, and 100% gives 0.80.
- The discrete-progress ablation fails with 0.00 success on all three simulated furniture tasks; the real-robot IVAR validation reports only a 16-point drop from the hardest simulation task, consistent with about 0.40 real success if compared to the 0.56 simulated IVAR result.

## Link
- [https://arxiv.org/abs/2607.01212v1](https://arxiv.org/abs/2607.01212v1)
