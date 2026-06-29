---
source: arxiv
url: https://arxiv.org/abs/2605.19957v1
published_at: '2026-05-19T15:10:27'
authors:
- Zuyao Lin
- Jianhui Zhang
- Peidong Jia
- Xiaoguang Zhao
- Shanghang Zhang
- Xingyu Chen
topics:
- embodied-world-model
- robot-world-model
- long-horizon-rollout
- navigation-manipulation
- video-diffusion
- robot-data-benchmark
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# World-Ego Modeling for Long-Horizon Evolution in Hybrid Embodied Tasks

## Summary
WEM separates long-horizon embodied video prediction into scene-level world state and robot/object ego state. It targets hybrid navigation-manipulation rollouts, where a single video generator tends to lose scene consistency or instruction-conditioned contact dynamics.

## Problem
- Existing embodied world models mix persistent scene structure, viewpoint change, robot motion, and contact dynamics in one prediction path, which hurts long-horizon rollouts.
- Hybrid tasks need both navigation scene consistency and manipulation physics across multiple instructions; existing benchmarks focus on short manipulation or single-prompt generation.
- This matters because world models are used for planning, policy simulation, and synthetic robot data.

## Approach
- WEM predicts two latent states for each step: a world state from visual history and past instructions, and an ego state from the current instruction plus recent context.
- It defines the world-ego split in three ways, then uses the semantic split by default: robot and manipulated objects are ego; background and inactive objects are world.
- A frozen Qwen3-VL-2B-Instruct state predictor uses 256 queries, split into 192 world queries and 64 ego queries, with role-conditioned attention.
- A Wan2.2-TI2V-5B diffusion transformer is split into a shared preceding expert plus world and ego experts. A predicted semantic mask routes video tokens to the matching expert and recombines them before decoding.
- Training uses flow matching for video latents plus BCE and Dice losses for the world-ego mask.

## Results
- The paper introduces HTEWorld: 125K training video clips, more than 4.5M frames, fine-grained action annotations, 300 evaluation trajectories, and more than 2K instructions.
- HTEWorld uses the 16-metric EWMScore from WorldArena and adds 6 metrics for multi-turn and hybrid navigation-manipulation evaluation.
- In the boundary ablation, the semantic world-ego split beats the motion-based split by 2.12 EWMScore points and the intention-based split by 2.79 points.
- WEM is reported to outperform fine-tuned Cosmos-Predict 2.5 2B/14B and WoW-7B on HTEWorld, but the excerpt does not give absolute scores or full baseline margins.
- The paper says WEM remains competitive on existing manipulation-only benchmarks, but the excerpt does not provide the benchmark scores.

## Link
- [https://arxiv.org/abs/2605.19957v1](https://arxiv.org/abs/2605.19957v1)
