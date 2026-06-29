---
source: arxiv
url: https://arxiv.org/abs/2606.23623v1
published_at: '2026-06-22T17:19:03'
authors:
- Yuhao Wu
- Yitian Liu
- Weijie Shen
- Mishuo Han
- Wenjie Xu
- Haotian Liang
- Zhongshan Liu
- Yinan Mao
- Lei Xu
- Xinping Guan
- Ru Ying
- Ran Zheng
- Wei Sui
- Xiaokang Yang
- Wenbo Ding
- Yao Mu
topics:
- vision-language-action
- discrete-diffusion
- reinforcement-learning
- robot-manipulation
- ppo
- bimanual-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# dVLA-RL: Reinforcement Learning over Denoising Trajectories for Discrete Diffusion Vision-Language-Action Models

## Summary
dVLA-RL applies PPO to discrete diffusion VLA policies by training on the sampled denoising path. The paper reports 99.7% average success on LIBERO and a 30.6 percentage-point gain over its SFT MM-ACT backbone on RoboTwin 2.0.

## Problem
- Discrete diffusion VLAs generate an action through several masked-token denoising steps, so the exact probability of the final action requires summing over many possible intermediate paths.
- Standard PPO needs a policy likelihood; using only the last denoising step ignores the path that produced the executed action.
- This matters because SFT-only robot policies can drift during closed-loop execution, and RL can optimize task success directly from rewards.

## Approach
- The method treats the K-step denoising process inside one environment action as a Markov chain and optimizes the probability of the sampled path.
- It factorizes the path likelihood into step-wise token generation probabilities for tokens that are newly unmasked at each denoising step.
- The Gumbel-TopK mask scheduler is treated as a non-differentiable system dynamic, so PPO gradients are applied only to newly generated action tokens.
- The same likelihood form supports 1-step, 2-step, and 4-step decoding, which lets the authors assign shorter or longer denoising horizons by task.

## Results
- On LIBERO, dVLA-RL reports 99.7% average success across Spatial, Object, Goal, and Long, with success above 99% on all four suites.
- On LIBERO, the reported average exceeds OpenVLA at 76.5%, π0 at 94.2%, and UniVLA at 95.2% in the excerpted table.
- On RoboTwin 2.0, dVLA-RL improves the MM-ACT SFT backbone from 61.4% to 92.0% average success across eight selected tasks, a +30.6 percentage-point gain.
- The largest listed RoboTwin 2.0 gains are Handover Mic at +47.9 points, Move Can Pot at +47.5 points, and Lift Pot at +43.1 points.
- The reported dVLA-RL scores are best online rollout success rates during RL training, with 512 rollout episodes per LIBERO task and 64 rollout episodes per RoboTwin 2.0 task.

## Link
- [https://arxiv.org/abs/2606.23623v1](https://arxiv.org/abs/2606.23623v1)
