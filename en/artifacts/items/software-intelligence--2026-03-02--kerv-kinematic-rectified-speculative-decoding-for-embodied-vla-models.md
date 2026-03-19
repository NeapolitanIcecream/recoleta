---
source: arxiv
url: http://arxiv.org/abs/2603.01581v1
published_at: '2026-03-02T08:12:03'
authors:
- Zihao Zheng
- Zhihao Mao
- Maoliang Li
- Jiayu Chen
- Xinhao Sun
- Zhaobo Zhang
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- speculative-decoding
- robot-kinematics
- embodied-ai
- kalman-filter
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models

## Summary
KERV proposes an acceleration framework that introduces robotic kinematics into VLA inference decoding, aiming to solve the problems that embodied VLA models are not fast enough under Speculative Decoding and that the threshold is hard to tune. The core idea is to use lightweight kinematic prediction to replace expensive re-inference, and to dynamically adjust the acceptance threshold with kinematic signals, achieving significant speedup with almost no loss in success rate.

## Problem
- Embodied VLA models represent actions as tokens generated step by step, but inference is slow; when Speculative Decoding is applied directly, token errors usually require re-inference, which instead brings high computational overhead.
- Existing methods such as SpecVLA rely on a fixed loose acceptance threshold, making it difficult to balance speed and success rate across different tasks/environments; errors also accumulate over time.
- The paper points out that the “error magnitude” in the token domain does not necessarily equal “action acceptability” in robot kinematics, so tuning only in the token domain is insufficient, which is important for real robot control.

## Approach
- Proposes KERV (Kinematic-Rectified Speculative Decoding), combining token-domain VLA decoding with kinematic-domain prediction.
- When an SD draft token first becomes incorrect at some position, instead of performing expensive re-inference for the remaining degrees of freedom of that action segment, it uses a kinematics-based Kalman Filter to directly predict and complete subsequent actions from historical action caches; the paper sets Prediction Length=1 and Action Context=10.
- Builds a mapping from tokens to robot actions, and caches historical actions by 7 DoF (X/Y/Z, orientation angles, gripper), allowing the KF to perform low-cost compensation within short-term context.
- Designs a dynamic threshold adjustment mechanism based on kinematic variability `K_var`: rather than using a fixed acceptance threshold, it adaptively updates the acceptance threshold according to the changes after mapping the current action error into kinematics; most tasks preset `r_max=15`,`r_min=5`.
- In system implementation, it adopts CPU-GPU collaboration: the draft model and verification model are placed on the GPU, while KF compensation and threshold adjustment are placed on the CPU, to leverage their characteristics of low FLOPs but heavier logical control.

## Results
- Tested on the four LIBERO task suites (Goal/Object/Spatial/Long), with 50 trials per task; the verification model is finetuned OpenVLA, and the draft model is a single-layer LLaMA block.
- Compared with naive VLA+SD, KERV achieves **1.48×-1.57×** speedup and claims **no success rate loss or almost no loss**; the overall conclusion given in the abstract is **27%-37% acceleration with nearly no Success Rate loss**.
- Compared with SpecVLA, the paper claims KERV achieves an additional **27%-37%** speedup; it also mentions only **1.5%** and **0.4%** success-rate drops in two environments.
- Goal environment: naive VLA+SD is **76.2% SR, 1.00×, 159.2 steps**; SpecVLA’s best speed is about **1.23×** (`r=15`, but SR drops to **71.0%**); KERV is **75.6% SR, 1.54×, 153.5 steps**.
- Object environment: naive is **68.6% SR, 1.00×, 195.9 steps**; SpecVLA peaks at about **1.10×**; KERV reaches **72.3% SR, 1.49×, 186.8 steps**, while its success rate is also higher than naive.
- The paper also provides quantitative evidence for why naive integration fails: on Goal/Object/Spatial/Long, naive VLA+SD reaches only **0.86×/0.96×/0.98×/0.91×** speed (relative to AR), with AFEP of **2.04/1.75/1.59/1.67**, indicating that frequent early errors cause re-inference to offset the benefits of SD.

## Link
- [http://arxiv.org/abs/2603.01581v1](http://arxiv.org/abs/2603.01581v1)
