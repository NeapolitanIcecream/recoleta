---
source: arxiv
url: https://arxiv.org/abs/2605.25477v1
published_at: '2026-05-25T06:31:03'
authors:
- Perry Dong
- Kuo-Han Hung
- Tian Gao
- Dorsa Sadigh
- Chelsea Finn
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- rl-finetuning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models

## Summary
EXPO-FT fine-tunes pretrained VLA robot policies with off-policy RL so they reach high real-world task success with little online robot data. It reports 30/30 success on 8 manipulation tasks after 19.1 minutes of online data on average.

## Problem
- Pretrained VLA policies can handle many manipulation tasks, but their zero-shot success rates are often too low for real robot use where failures are costly.
- RL from scratch cannot use the behavior learned by large pretrained VLAs, while prior VLA fine-tuning methods often need too much robot interaction or stop below reliable success.
- Many modern VLAs output action chunks, so RL fine-tuning must optimize multi-step action sequences rather than single actions.

## Approach
- EXPO-FT builds on EXPO, an off-policy RL method for flow-matching and diffusion-style policies.
- The method keeps the pretrained VLA as the base policy and trains a lightweight edit policy that proposes small action corrections; a Q-function chooses the highest-value base or edited action.
- It extends EXPO to temporally extended actions by editing and scoring executed action chunks, with TD backups over chunk boundaries.
- Human operators can correct individual timesteps inside action chunks during online rollouts; the corrected actions are stored in the replay buffer.
- The reported system uses π0.5 as the VLA backbone, two RGB cameras, proprioception, sparse binary rewards, a ResNet-50 critic encoder, and a separate actor-learner setup.

## Results
- The paper evaluates EXPO-FT on 8 real-world manipulation tasks: Egg Flip, String Light Routing Route I, String Light Routing Route II, String Light Insert, Candy Scoop, Cube Pick, Flower Insert, and Pool Shot.
- It claims perfect final evaluation performance: 30/30 successes on every evaluated task.
- It reports an average of 19.1 minutes of online robot data to reach that performance; the introduction also describes this as about 20 minutes.
- Experiments use 8k to 20k environment steps per task, 10 Hz Cartesian end-effector and gripper velocity control, and 30 evaluation trials per task.
- Rule-based task success detectors are reported to exceed 95% accuracy, while final evaluation success is judged by a human observer.
- The excerpt states that EXPO-FT outperforms both RL-from-scratch methods and prior VLA fine-tuning methods, but it does not provide the full baseline table or per-baseline numbers.

## Link
- [https://arxiv.org/abs/2605.25477v1](https://arxiv.org/abs/2605.25477v1)
