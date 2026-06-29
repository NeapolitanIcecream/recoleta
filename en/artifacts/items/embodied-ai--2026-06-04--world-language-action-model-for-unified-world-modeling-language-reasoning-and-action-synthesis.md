---
source: arxiv
url: https://arxiv.org/abs/2606.05979v1
published_at: '2026-06-04T10:23:01'
authors:
- Yi Yang
- Zhihong Liu
- Siqi Kou
- Yiyang Chen
- Yanzhe Hu
- Jianbo Zhou
- Boyuan Zhao
- Zhijie Wei
- Xiao Xia
- Xueqi Li
- Pengfei Liu
- Zhijie Deng
topics:
- world-language-action
- robot-foundation-model
- world-model
- vision-language-action
- long-horizon-manipulation
- cross-embodiment-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis

## Summary
WLA proposes a world-language-action robot model that predicts textual subtasks, future visual states, and actions in one policy. The reported WLA-0 prototype reaches strong simulation and real-robot results with 2B active inference parameters and about 40 ms latency on an NVIDIA RTX 5090.

## Problem
- Existing world-action models mainly predict future images, which gives useful physical supervision but weak high-level language planning for long-horizon tasks.
- Existing vision-language-action models can follow language but often lack direct future-state supervision for physical dynamics.
- This matters because long-horizon robot manipulation needs semantic progress tracking, memory, and fast action generation under changing visual conditions.

## Approach
- WLA takes images, text instructions, and robot state as input, then predicts a textual subtask, a compact physical-dynamics representation, and an action chunk.
- An autoregressive Transformer backbone generates the language subtask and meta-query outputs that encode the physical transition.
- A World Expert trains those meta-query outputs to predict a future visual frame, while an Action Expert maps the same transition signal plus proprioception to executable actions.
- The World Expert can be removed during normal inference, so action generation keeps the training benefit of world prediction without paying image-generation cost at test time.
- A test-time scaling mode samples multiple action chunks, predicts the future frame for each one, scores those imagined states with a value model, and executes the highest-scoring action chunk.

## Results
- WLA-0 has 3.4B total parameters, uses about 2B active parameters at inference, and reports about 40 ms inference latency on an NVIDIA RTX 5090.
- On RoboTwin 2.0, WLA-0 reports 92.94% success on Clean and 90.02% on Randomized, with no embodied pretraining; Lingbot-VA reports 92.90% and 91.50%, and Fast-WAM reports 91.88% and 91.78%.
- On LIBERO, WLA-0 reports 98.6% average success across Spatial, Object, Goal, and Long; test-time scaling with 6 candidates and horizon 2 raises the average to 98.9%.
- Removing the world-modeling loss lowers RoboTwin Clean from 92.94% to 90.98% and LIBERO average from 98.6% to 97.9%, which supports the claim that future-state supervision improves action learning.
- On RMBench, WLA-0 reports 56.5% average success, compared with 28.5% for Mem-0, 13.3% for Fast-WAM, 7.3% for X-VLA, and 5.5% for pi-0.5; removing language subtask loss drops WLA-0 to 17.3%.
- For unseen RoboTwin 2.0 tasks with video-only data, the excerpt reports average gains over the seen-action baseline: same-embodiment video reaches 34.4 / 30.0 versus 13.0 / 11.6, and cross-embodiment video reaches 28.8 / 27.4.

## Link
- [https://arxiv.org/abs/2606.05979v1](https://arxiv.org/abs/2606.05979v1)
