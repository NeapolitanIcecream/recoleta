---
source: arxiv
url: https://arxiv.org/abs/2606.19990v1
published_at: '2026-06-18T09:29:30'
authors:
- Pu Li
- Zhigang Lin
- Qiang Wu
- Yongxuan Lv
- Fei Wang
- Shan You
topics:
- embodied-world-models
- robot-foundation-models
- diffusion-rl
- reward-modeling
- grpo
- robotics-evaluation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Reward as An Agent for Embodied World Models

## Summary
The paper proposes RL post-training for embodied world models using an agent-style reward evaluator and a dynamic-aware GRPO rollout method. Its main claim is that broader exploration can improve world models when the reward signal checks physical plausibility, instruction following, and task completion.

## Problem
- Existing RL methods for world models keep rollouts close to the training distribution because reward models fail under wider exploration.
- In embodied settings, weak rewards can give high scores to videos with blur, static motion, simplified backgrounds, or broken physics, so optimization can improve the reward without improving the task.
- This matters because robot world models need plausible object interaction and task completion, not only good-looking video.

## Approach
- The reward system uses a frontier VLM as an evaluator across four dimensions: visual quality, instruction following, physical compliance, and task completion.
- It first makes a global plan for what to score, then uses a curriculum so basic video validity gates later checks such as task completion and physics.
- It breaks hard checks into smaller votes, such as goal consistency, agent consistency, viewpoint consistency, interaction realism, deformation, and penetration.
- It adds a reflection pass where the evaluator rechecks its own score and explanation.
- DynDiff-GRPO adds diffusion noise mainly in dynamic regions detected from temporal changes, so moving objects and contacts get more exploration than static scene areas.

## Results
- The excerpt does not provide the final numeric accuracy gains from Table 1 because the table is truncated.
- The paper claims gains across two open-source embodied world models: Kairos-3.0-Robot and Cosmos-Predict2.5-2B.
- Evaluation uses the robotics subset of PAI-Bench and reports Domain Score and Overall/Quality Score per prompt, with Qwen3.5 used as the judge model.
- Reward hacking examples show high proxy scores for bad rollouts: visual occlusion gets 0.79/1.0 on VideoAlign VQ, background simplification gets 0.80/1.0 on VideoAlign VQ, motion degradation gets 2.76/5.0 on UnifiedReward Alignment Score, and physical invalidation gets 3.0/5.0 on UnifiedReward Physics Score.
- The reward design was refined through more than 20 iteration rounds, with several hundred sampled trajectories manually checked in each iteration when needed.

## Link
- [https://arxiv.org/abs/2606.19990v1](https://arxiv.org/abs/2606.19990v1)
