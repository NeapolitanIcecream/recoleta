---
source: arxiv
url: https://arxiv.org/abs/2605.29438v1
published_at: '2026-05-28T06:33:05'
authors:
- Ye Li
- Huanan Liu
- Kangye Ji
- Yuan Meng
- Jiajun Fan
- Yuansong Wang
- Shiyu Qin
- Chenglei Wu
- Shu-Tao Xia
- Zhi Wang
topics:
- vision-language-action
- robot-policy-acceleration
- dynamic-compute
- temporal-caching
- reinforcement-learning
- real-time-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models

## Summary
ElegantVLA speeds up vision-language-action robot policies by learning which control steps need full computation and which can reuse cached work. It keeps the base VLA model frozen and adds a small scheduler for the vision encoder, LLM, and action head.

## Problem
- VLA policies such as GR00T and CogACT run a vision encoder, LLM, and action generator at each robot control step, which limits real-time manipulation.
- Fixed acceleration rules waste compute during stable motion and can damage accuracy near contact, alignment, grasping, insertion, or placement.
- This matters because low control frequency can make robots miss moving objects or react late during precise manipulation.

## Approach
- ElegantVLA adds a learned scheduler to a frozen VLA policy. The scheduler chooses a compute mode at each step instead of changing the base model weights.
- For the vision encoder and LLM, it uses a five-level mode: full recomputation, partial LLM recomputation, or reuse of cached visual-language representations for several steps.
- It estimates visual-language stability with CKA similarity from the first LLM layer, comparing the current hidden state with a recent full-compute anchor.
- For the action head, it uses a three-level mode: recompute all denoising or refinement steps, reuse middle steps, or reuse all steps after the first refinement.
- The scheduler is trained with Maskable PPO using CKA similarity, gripper speed, end-effector translation speed, end-effector rotation speed, and episode progress as inputs.

## Results
- On GR00T in SimplerEnv, ElegantVLA raises overall success from 64.00% to 65.88% and reports up to 2.55× average FLOPs speedup.
- On GR00T Google Robot tasks in SimplerEnv, average success is 75.00% with 2.35× speedup, compared with GR00T at 71.08% and 1.00×.
- On GR00T WidowX tasks in SimplerEnv, average success is 58.07% with 2.55× speedup, compared with GR00T at 57.93% and 1.00×.
- On CogACT Visual Matching in SimplerEnv, average success is 77.59% with 3.72× speedup, compared with CogACT at 74.80% and 1.00×.
- On CogACT Variant Aggregation in SimplerEnv, average success is 72.54% with 3.77× speedup, compared with CogACT at 61.30% and 1.00×.
- In GR00T-based real-world tests across six tasks, it reports 2.18× compute reduction, control frequency rising from 13.8 Hz to 26.3 Hz, and average success rising from 61.67% to 65.00%.

## Link
- [https://arxiv.org/abs/2605.29438v1](https://arxiv.org/abs/2605.29438v1)
