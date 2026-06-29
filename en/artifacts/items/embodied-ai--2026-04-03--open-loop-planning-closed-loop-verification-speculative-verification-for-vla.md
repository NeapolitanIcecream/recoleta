---
source: arxiv
url: http://arxiv.org/abs/2604.02965v1
published_at: '2026-04-03T10:55:51'
authors:
- Zihua Wang
- Zhitao Lin
- Ruibo Li
- Yu Zhang
- Xu Yang
- Siya Mi
- Xiu-Shen Wei
topics:
- vision-language-action
- robot-control
- action-chunking
- closed-loop-verification
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA

## Summary
SV-VLA cuts VLA control cost by planning action chunks with a large model and checking them online with a small verifier. The goal is to keep most of the speed of open-loop chunking while recovering some of the adaptability of closed-loop control.

## Problem
- VLA models for manipulation are strong but expensive to run at every control step.
- Action chunking reduces inference cost by predicting multiple future actions at once, but later actions use stale observations and can drift when the environment changes.
- Speculative decoding from language modeling does not transfer cleanly to robotics because future action validity depends on future observations that appear only after real execution.

## Approach
- SV-VLA uses the heavy VLA as a low-frequency macro-planner. At a planning boundary, it outputs an action chunk of length K and a planning-context feature from an internal transformer layer.
- A lightweight verifier runs at each control step on the latest observation, encodes the image with a small vision backbone such as ViT-Tiny, fuses that feature with the saved planning context, and predicts a reference action.
- The system compares the planned action and the verifier's reference action with a normalized L1 distance. If the distance stays below a threshold \(\tau\), it executes the planned action.
- If the distance exceeds \(\tau\), the system discards the rest of the chunk and calls the heavy VLA again to replan from the current state.
- The heavy VLA stays frozen during verifier training; only the verifier is trained with an L1 regression loss against ground-truth actions, which keeps the method compatible with pretrained VLAs.

## Results
- The paper reports experiments on the LIBERO benchmark and says SV-VLA improves the average success rate across three subtasks by 11.4 percentage points over the open-loop baseline, from 79.5% to 90.90%.
- The excerpt does not provide the names of the three subtasks, per-task scores, latency numbers, chunk size used in the main result, or a comparison against step-wise closed-loop VLA.
- The method claims to preserve the efficiency profile of chunked control: best-case per-step cost approaches \(C_{VLA}/K + C_{verify}\), while worst-case cost approaches \(C_{VLA}\) if replanning triggers every step.
- The text gives one concrete chunking example, noting that long chunks such as \(K=64\) increase exposure to drift in standard open-loop execution.

## Link
- [http://arxiv.org/abs/2604.02965v1](http://arxiv.org/abs/2604.02965v1)
