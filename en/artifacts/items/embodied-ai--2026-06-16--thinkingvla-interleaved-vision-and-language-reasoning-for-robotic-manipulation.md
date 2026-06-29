---
source: arxiv
url: https://arxiv.org/abs/2606.17937v1
published_at: '2026-06-16T13:45:17'
authors:
- Tianyi Lu
- Hui Zhang
- Zijie Diao
- Junke Wang
- Shengqi Xu
- Xingyao Lin
- Guojin Zhong
- Ziyi Ye
- Peng Wang
- Zuxuan Wu
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- world-model
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ThinkingVLA: Interleaved Vision and Language Reasoning for Robotic Manipulation

## Summary
ThinkingVLA is a VLA policy that generates a text subgoal, a future image, an action-focused text rationale, then robot actions in one autoregressive sequence. It targets long-horizon manipulation where direct observation-to-action policies lose task structure and spatial grounding.

## Problem
- Most VLA policies map the current image and instruction straight to actions, which weakens subgoal planning, future-state checking, and long-horizon execution.
- Text-only CoT lacks spatial precision, visual-only forecasting lacks task decomposition, and decoupled text/image reasoning does not condition each step on the previous generated modality.
- Better long-horizon robot control matters because tasks such as making breakfast or assembling objects need both prediction of the next scene and inference of the action needed to reach it.

## Approach
- The policy factors each decision into forward CoT, predicted future image, inverse CoT, and action: p(r_fwd, o_hat_{t+1}, r_inv, a_t | o_t, l).
- A thinking expert generates text tokens and discrete image tokens in one causal sequence using PaliGemma text tokenization, SigLIP observation encoding, and Cosmos image tokenization.
- The predicted image becomes the target state for the inverse CoT, which reasons about object positions, gripper intent, and action direction before action generation.
- A separate 300M-parameter action expert uses flow matching and attends to the full reasoning prefix through shared Mixture-of-Transformers attention.
- Training uses three stages: reasoning/image pretraining on Open X-Embodiment, end-to-end action learning, then target fine-tuning on RoboTwin and ALOHA demonstrations.

## Results
- On RoboTwin 2.0 Easy, ThinkingVLA reaches 77.9% average success across 20 tasks, above BagelVLA at 73.4%, XVLA at 69.2%, UP-VLA at 51.2%, and π0 at 49.8%.
- On RoboTwin 2.0 Hard, it reaches 29.3% average success; XVLA is higher at 35.4%, while BagelVLA is 16.8%, π0 is 17.2%, and UP-VLA is 13.3%.
- Gains increase on longer simulation tasks: Horizon=2 Easy/Hard is 71.0%/26.6% versus BagelVLA 55.8%/7.0%; Horizon=3 is 60.0%/23.6% versus BagelVLA 55.8%/6.8%.
- On five real ALOHA tasks with 50 demos and 20 trials each, the full model reports 90%, 90%, 85%, 70%, and 90% success, and beats π0.5 by 10 percentage points on Make Breakfast and Assemble Equation.
- Ablations show inverse CoT is the largest contributor: removing it lowers real-world average success from 85.0% to 70.0%; removing forward CoT lowers it by 6 percentage points.
- Stage 2 end-to-end pretraining improves 50-demo success by 5 points on Hang Cup, 25 points on Place Cubes, and 50 points on Assemble Equation compared with skipping Stage 2.

## Link
- [https://arxiv.org/abs/2606.17937v1](https://arxiv.org/abs/2606.17937v1)
