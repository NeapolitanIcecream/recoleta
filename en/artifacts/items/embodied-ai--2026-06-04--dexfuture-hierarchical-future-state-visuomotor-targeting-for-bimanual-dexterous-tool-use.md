---
source: arxiv
url: https://arxiv.org/abs/2606.05699v1
published_at: '2026-06-04T04:37:23'
authors:
- Runfa Blark Li
- Kuang-Ting Tu
- Nikola Raicevic
- Dwait Bhatt
- Xinshuang Liu
- Keito Suzuki
- Ki Myung Brian Lee
- Nikolay Atanasov
- Truong Nguyen
topics:
- dexterous-manipulation
- bimanual-tool-use
- vision-language-action
- generalist-robot-policy
- world-models
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use

## Summary
DexFuture predicts future hand-tool-object targets from egocentric RGB and robot state, then uses a target-conditioned dexterous policy to execute bimanual tool use. It aims to keep the control benefit of demonstration targets at deployment, where future demonstration states are unavailable.

## Problem
- Target-conditioned dexterous policies often need future targets taken from demonstrations, but a deployed robot cannot access future hand, tool, or object states.
- Action-conditioned world-model planning over high-dimensional bimanual hand actions is too slow for stable contact-rich control.
- The problem matters because tool use such as cutting, pouring, wiping, and shearing needs coordinated future guidance across two hands, the tool, and the object.

## Approach
- A high-level Future-State Visuomotor Target Predictor reads recent egocentric RGB frames, proprioception, and geometric cues.
- The predictor builds structured tokens for hand links, the tool, and the object. Hand-link tokens come from projected link locations and local image features.
- A horizon-conditioned transformer predicts sparse future targets at horizons {0, 2, 4, ..., 16}; intermediate targets are linearly interpolated during execution.
- A low-level per-link transformer policy tracks the predicted 900-D target and outputs bimanual actions at control rate.
- The predictor is trained with supervised future state and target losses, while the policy is trained with PPO using tracking rewards.

## Results
- On OakInk2 bimanual tool-use tasks, DexFuture reports 59.69% average success versus 66.52% for the privileged PhysGraph target baseline, reaching about 90% of oracle performance.
- The no-target PhysGraph policy reaches about 7% average success in the abstract, showing that current-state feedback alone performs poorly on these tasks.
- DexFuture runs at 60 Hz and is reported as about 250x faster than DexWM-style CEM planning with a future action-conditioned world model.
- On fruit-knife cutting, DexFuture reaches 89.79% success versus 87.87% for privileged PhysGraph, with 0.61 cm tool/object translation error versus 0.98 cm.
- On bread cutting, wiping, and shearing tasks, DexFuture remains close to privileged PhysGraph: 83.49% versus 90.05% on bread cutting, 56.96% versus 62.24% on big-brush wiping, and 30.69% versus 35.84% on one scissor-shearing task.
- Future target prediction accuracy varies by task: examples include 0.87 cm 3D error and 99.78 PCK@10 on fruit-knife cutting, but 5.54 cm 3D error and 32.93 PCK@10 on one shearing task.

## Link
- [https://arxiv.org/abs/2606.05699v1](https://arxiv.org/abs/2606.05699v1)
