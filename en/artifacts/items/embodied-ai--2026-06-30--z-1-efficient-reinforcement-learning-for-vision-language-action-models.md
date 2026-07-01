---
source: arxiv
url: https://arxiv.org/abs/2606.31846v1
published_at: '2026-06-30T15:46:57'
authors:
- Lang Cao
- Renhong Chen
- Luyi Li
- Peng Wang
- Mofan Peng
- Yitong Li
topics:
- vision-language-action
- robot-reinforcement-learning
- grpo
- robocasa
- robot-policy-post-training
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Z-1: Efficient Reinforcement Learning for Vision-Language-Action Models

## Summary
Z-1 is an RL post-training method for flow-based vision-language-action robot policies, built on π0.5 and tested on 24 RoboCasa tasks. It raises average success from 67.4% after SFT to 80.6% after GRPO using public RoboCasa demonstrations.

## Problem
- VLA robot policies trained with behavior cloning or SFT copy fixed demonstrations, so long-horizon errors can move the robot into states missing from the training data.
- Online RL can improve task success through trial and error, but flow-based VLA rollouts are expensive, sparse rewards give weak credit assignment, and a frozen vision-language module can miss visual grounding failures.
- The problem matters because better post-training could improve robot manipulation without extra private demonstrations.

## Approach
- Z-1 starts from a pretrained π0.5 policy, runs per-scene SFT on 1,199 public RoboCasa demonstrations, then applies per-task GRPO post-training.
- Shared-Prefix GRPO runs a common approach prefix once, clones the simulator state, and samples separate suffixes so the group comparison focuses on the manipulation phase.
- Tree-Structured Prefix Branching adds intermediate branch points inside the prefix, which keeps more approach-phase action chunks trainable than a flat shared prefix.
- Success-Aware Reward Decay gives earlier successful completions higher calibrated reward while keeping failed rollouts unchanged.
- Selective VLM-Action Expert joint training updates the vision-language backbone only on tasks where action-expert-only GRPO is weak, based on training diagnostics before final evaluation.

## Results
- On 24 RoboCasa tasks, Z-1 RL reports 80.6% average success, up from 67.4% for Z-1 SFT, a +13.2 percentage-point gain.
- It reports higher average success than GR00T by +30.9 points, GR00T N1.5 by +20.9 points, Video Policy by +17.3 points, and X-WAM by +1.4 points.
- Against X-WAM, the paper reports 80.6% for Z-1 RL versus 79.2% for X-WAM, with Z-1 ahead in 5 of 7 task categories.
- Category gains over Z-1 SFT include door tasks from 93.2% to 97.0%, drawer tasks from 83.4% to 96.1%, and sink/faucet tasks from 63.2% to 94.3%.
- The comparison uses reported numbers from prior papers rather than a fully controlled reproduction, so the strongest controlled result is the +13.2-point gain over the authors' own SFT initialization.

## Link
- [https://arxiv.org/abs/2606.31846v1](https://arxiv.org/abs/2606.31846v1)
