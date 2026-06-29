---
source: arxiv
url: https://arxiv.org/abs/2606.26006v1
published_at: '2026-06-24T16:23:18'
authors:
- Shuyi Zhang
- Yunfan Lou
- Hongyang Cheng
- Yichen Guo
- Chuyao Fu
- Yaoxu Lyu
- Xiaojie Zhang
- Haoran Li
- Pengwei Wang
- Zhongyuan Wang
- Shanghang Zhang
topics:
- vision-language-action
- robot-rl-finetuning
- offline-to-online-rl
- value-guided-distillation
- robot-manipulation
- sample-efficiency
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation

## Summary
FORCE is a three-stage RL fine-tuning method for VLA robot policies that aims to improve over imitation learning without human intervention. It targets sample efficiency and early training collapse during offline-to-online robot learning.

## Problem
- VLA policies trained by imitation can inherit weak or inconsistent actions from demonstrations, which limits task success after deployment.
- Direct RL fine-tuning on robots can waste samples because the critic is poorly calibrated when online rollouts begin, causing early performance drops.
- Online exploration produces many low-value actions, and prior real-robot methods often use human correction to keep training safe and useful.

## Approach
- FORCE starts with offline Cal-QL on expert demonstrations to train a conservative critic and a behavior-regularized actor.
- It then runs a value-calibrated warm-up: the current policy collects a small on-policy rollout batch, and the critic is updated on mixed offline and rollout data before actor updates.
- During online fine-tuning, it keeps an expert buffer and a policy buffer, sampling from both so the policy retains useful demonstrated behavior while learning from new rollouts.
- Its Value-Guided Policy Self-Distillation samples candidate actions, scores them with the critic, keeps actions above a state-level mean Q baseline, and trains the policy toward those higher-value actions.
- The method uses a one-step consistency policy actor to reduce the cost of diffusion or flow-style action generation and to make Q-guided updates easier to apply.

## Results
- In ManiSkill simulation across 6 tasks, FORCE with an Octo backbone reaches 82.3% average success, compared with 71.1% for ConRFT without human-in-the-loop, 50.2% for PA-RL, 45.2% for Cal-QL, and 3.58% for Octo behavior cloning.
- With a pi0 backbone, FORCE reaches 86.9% average success on the same ManiSkill tasks, including 100% on PullCube and PushCube, 97.5% on PlaceSphere, and 94.1% on PickCube.
- The paper claims a 79 percentage-point absolute success-rate gain, a 10 percentage-point improvement over prior RL methods, and 32.5% faster training.
- On 6 real-world Franka tasks, average success improves from 45.0% for behavior cloning to 98.3% after FORCE online fine-tuning.
- Real-world average execution steps drop from 112.8 for behavior cloning to 38.9 after FORCE fine-tuning; task results include Open Drawer 35% to 100%, Insert USB 75% to 100%, and Stack Cube 40% to 100% success.
- The reported real-world training uses no human intervention during online fine-tuning.

## Link
- [https://arxiv.org/abs/2606.26006v1](https://arxiv.org/abs/2606.26006v1)
