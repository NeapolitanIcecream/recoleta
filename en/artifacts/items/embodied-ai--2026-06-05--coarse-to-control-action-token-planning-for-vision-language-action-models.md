---
source: arxiv
url: https://arxiv.org/abs/2606.07107v1
published_at: '2026-06-05T10:01:37'
authors:
- Jinhao Wu
- Shiduo Zhang
- Yicheng Liu
- Xiaopeng Yu
- Sixian Li
- Siyin Wang
- Hang Zhao
- Jing Huo
- Yang Gao
- Jingjing Gong
- Xipeng Qiu
- Yu-Gang Jiang
topics:
- vision-language-action
- action-token-planning
- action-tokenization
- robot-foundation-models
- long-horizon-manipulation
- sim2real
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models

## Summary
Coarse-to-Control adds an internal coarse action-token plan before a VLA emits executable action tokens, improving long-horizon robot manipulation in simulation and real robot tests.

## Problem
- Direct VLA policies map images, language, and robot state straight to motor actions, so long tasks can fail when early action errors compound.
- Textual or visual intermediate reasoning can describe goals or subgoals, while wrist pose, motion direction, gripper timing, and waypoint structure remain under-specified.
- The problem matters because multi-stage manipulation needs a policy to keep future task structure while producing precise low-level control.

## Approach
- The model first predicts coarse planning tokens from the current observation, instruction, and proprioceptive state.
- It then predicts executable action tokens conditioned on those planning tokens; only executable tokens are decoded into robot actions at inference.
- A joint residual-VQ tokenizer encodes both coarse long-horizon plans and short-horizon executable action chunks into one shared discrete action vocabulary.
- The coarse plan is built by compressing a future action horizon into K chunks: each chunk stores net relative motion and the final gripper state.
- Training uses teacher-forced autoregressive next-token prediction over the concatenated plan-token and execution-token sequence.

## Results
- On LIBERO, Coarse-to-Control reports 97.9% overall success, above OpenVLA-OFT at 97.1%, π0.5 at 96.8%, and π0 at 94.2%; suite scores are 98.8 Spatial, 100.0 Object, 97.8 Goal, and 95.0 Long.
- On SimplerEnv-WidowX, it reports 83.3% overall success, above UD-VLA at 62.5%, F1 at 59.4%, CogACT at 51.3%, and π0 at 40.1%; task scores are 100.0 Put Spoon, 95.8 Put Carrot, 79.2 Stack Block, and 58.3 Put Eggplant.
- In real-world tests with 50 demonstrations per task and 20 rollouts per task, the plan-based policy reports 62.5% average success over four manipulation tasks and the best result on 3 of 4 tasks.
- The LIBERO planning-horizon ablation improves overall success from 96.45% with no plan to 97.55% at H_p=40 and 97.90% at H_p=160.
- The tokenizer ablation reports 95.40% overall for Faster-AR, 96.60% with separate planning and execution tokenizers, and 97.90% with the shared joint-mode tokenizer; Long-suite success rises from 88.60% to 91.60% to 95.00%.

## Link
- [https://arxiv.org/abs/2606.07107v1](https://arxiv.org/abs/2606.07107v1)
