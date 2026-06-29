---
source: arxiv
url: https://arxiv.org/abs/2605.30226v1
published_at: '2026-05-28T16:57:47'
authors:
- Zhongxi Chen
- Yifan Han
- Yanming Shao
- Huanming Liu
- Congsheng Xu
- Xiaoyu Chen
- Yao Mu
- Wenzhao Lian
topics:
- vision-language-action
- dexterous-manipulation
- offline-to-online-rl
- residual-adaptation
- human-in-the-loop
- robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models

## Summary
BORA is an offline-to-online RL training pipeline for dexterous VLA robot policies. It improves real-world success on five Franka arm plus 12-DoF hand tasks by training an action-conditioned critic offline, then adding a small human-guided residual policy online.

## Problem
- Dexterous VLA policies fail more often than simpler gripper policies because hand control has many degrees of freedom, contacts are hard to predict, and small execution errors build up over time.
- Offline imitation data can contain redundant or suboptimal hand motions, so pure imitation learning gives weak physical intent and poor generalization to unseen objects.
- Direct online RL on a dexterous hand can waste real-robot samples, create unsafe exploration, and damage pretrained VLM features during full-model updates.

## Approach
- BORA first trains the VLA policy offline with a consistency-policy action head that produces continuous action chunks in 1 to 3 denoising steps, which shortens RL credit assignment compared with long diffusion chains.
- Its critic reads both VLM cognition tokens and the generated action chunk, then scores each step inside the chunk. This lets value learning judge the proposed hand motion, not only the camera image.
- Offline policy updates combine IQL-style value learning, intra-chunk advantage estimates, clipped PPO-style updates, and behavior-cloning regularization to limit out-of-distribution actions.
- During online deployment, BORA freezes the base VLA and trains a small MLP residual actor that adds chunk-level corrections: A_final = A_base + lambda * A_res.
- Human interventions provide penalties when the policy enters risky states and recovery rewards after corrective actions. The online stage reuses the offline critic and mixes offline and online data at a 1:1 ratio.

## Results
- On five standard real-world tasks with 20 trials each, BORA-Full reached 86.0% average success. CP Base reached 53.0%, VITRA reached 54.0%, CP + Decoupled Critic reached 45.0%, and BORA-Offline reached 67.0%.
- The standard-setting gain over CP Base was 33 percentage points, matching the paper's main claim. Per-task BORA-Full success was 20/20 on Pick the plush toy, 18/20 on Pick and Place, 15/20 on Open the box, 16/20 on Pull the tissue, and 17/20 on Press the button.
- On unseen-object trials, BORA-Full reached 70.0% average success. CP Base reached 27.0%, VITRA reached 33.0%, CP + Decoupled Critic reached 41.0%, and BORA-Offline reached 52.0%.
- The unseen-object gain over CP Base was 43 percentage points. Per-task BORA-Full success was 17/20, 14/20, 10/20, 14/20, and 15/20 across the five tasks.
- BORA-Offline alone improved average success over CP Base by 14 points in the standard setting and 25 points in the unseen-object setting.
- The paper reports that online adaptation converged within 2 online RL rounds, with human intervention needed 1 to 2 times per task and about 20% of online trajectory execution time spent under human control.

## Link
- [https://arxiv.org/abs/2605.30226v1](https://arxiv.org/abs/2605.30226v1)
