---
source: arxiv
url: https://arxiv.org/abs/2606.09337v1
published_at: '2026-06-08T11:05:05'
authors:
- Huaihang Zheng
- Yi Yang
- Kai Ma
- Shenglin Xu
- Tian Xie
- Guozheng Li
- Xiangyu Wang
- Yiren Ma
- Si Liu
- Yinian Mao
- Baoxu Liu
topics:
- vision-language-action
- tactile-feedback
- online-rl
- contact-rich-manipulation
- robot-policy
- human-intervention
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# TORL-VLA: Tactile Guided Online Reinforcement Learning for Contact-Rich Manipulation

## Summary
TORL-VLA adds tactile-guided online RL to a vision-language-action robot policy so it can correct contact-rich manipulation during execution.

## Problem
- Offline VLA policies can fail when contact conditions shift after training, even when RGB observations look close to success.
- Contact-rich tasks such as tight cup placement, latch locking, and egg handling need force and torque feedback to avoid bad contact forces, repeated retries, or object damage.
- Human intervention during online learning can bias value estimates because a failed policy action may be followed by a human rescue and later success.

## Approach
- The robot maps two 6x8 fingertip tactile arrays into a 12D wrench signal: 6D force-torque per finger.
- A wrench-aware VLA fuses recent wrench history with visual-language tokens using attention, MoE routing, and a zero-initialized tactile bypass.
- The reference model predicts both an action chunk and a future wrench sequence with a joint action-wrench flow-matching loss.
- A lightweight stage-specific actor-critic refines only the executable action chunk online, conditioned on VLA tokens, proprioception, current wrench, wrench history, predicted wrench, and the VLA action reference.
- An intervention-censored critic removes bootstrapping across human-correction boundaries and applies an intervention cost, so post-intervention success is not credited to the preceding policy action.

## Results
- On 30 real-robot trials per task, TORL-VLA reached 30/30 Cup, 29/30 Latch, and 30/30 Egg success, compared with pi_0.5 at 18/30, 15/30, and 20/30.
- Full-task success improved to 28/30, compared with pi_0.5 at 12/30, ForceVLA at 15/30, TORL-VLA without RL at 21/30, and RLT at 23/30.
- Full-task average time on successful runs was 165.45 s for TORL-VLA, compared with 175.23 s for RLT, 191.91 s for TORL-VLA without RL, 195.34 s for ForceVLA, and 199.65 s for pi_0.5.
- In the reference-model ablation, removing MoE gave the largest drop: 18/30 Cup, 17/30 Latch, and 19/30 Egg, versus the full no-RL reference model at 25/30, 23/30, and 25/30.
- In the online adaptation ablation, the full model scored 30/30, 29/30, and 30/30, compared with 27/30, 27/30, and 26/30 without wrench context, and 27/30, 26/30, and 28/30 without the intervention-censored critic.

## Link
- [https://arxiv.org/abs/2606.09337v1](https://arxiv.org/abs/2606.09337v1)
