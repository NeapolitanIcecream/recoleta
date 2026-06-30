---
source: arxiv
url: https://arxiv.org/abs/2606.30318v1
published_at: '2026-06-29T14:00:17'
authors:
- Yulin Zhou
- Yimeng Wang
- Nengyu Wang
- Shaojia Xing
- Shiyun Tu
- Xiang Li
- Jingkai Zhang
- Ningbo Jiang
- Yuankai Lin
- Hua Yang
- Xiangrui Zeng
- Zhouping Yin
topics:
- vision-language-action
- generalist-robot-policy
- long-horizon-manipulation
- robot-memory
- state-space-models
- imitation-learning
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Chronos: A Physics-Informed Full-History Framework for Non-Markovian Long-Horizon Manipulation

## Summary
Chronos is a robot imitation-learning method for long-horizon manipulation where the current camera view can hide the task phase. It claims large gains on memory-dependent manipulation by making the full observation history the policy state and refining action chunks with a learned acceleration field.

## Problem
- Current-frame or short-window VLA policies can choose the wrong action when two identical observations come after different histories.
- This matters for tasks such as removing, inspecting, and returning an object, where the scene can look the same before and after a key step while the correct next move differs.
- Long-horizon imitation needs temporal credit assignment across complete demonstrations, since the event that determines the action may occur far before the current step.

## Approach
- At each physical control step, Chronos fuses observation and proprioception into one state token, so the sequence length matches the trajectory length.
- A Mamba-style selective state space model processes the full token sequence causally and stores task-phase information in a recurrent state.
- Training backpropagates losses through complete demonstration sequences, so late errors can update earlier memory formation.
- An IMLE generator samples a coarse multimodal action chunk from the history-conditioned state.
- A second-order Schrödinger-inspired bridge refines that chunk by predicting acceleration fields, aiming for smoother robot motion than direct regression, diffusion, or first-order flow heads.

## Results
- On RMBench, Chronos reports 73.6% average success, beating π_0.5 by +62.4 percentage points, a 6.6x relative gain, with 10x fewer parameters.
- On RMBench, it exceeds Mem-0 by 22.8 percentage points while using more than 30x fewer parameters.
- In real-world dual-arm tests with one RGB camera, Chronos reports 78% average success across 4 tasks.
- On the 3 memory-dependent real-world tasks, Chronos reports 72% average success, while π_0.5 reports 0% on the same subset.
- The paper evaluates 16 simulated tasks and 4 real-world experiments, including precision insertion, general manipulation, and memory-dependent long-horizon control.

## Link
- [https://arxiv.org/abs/2606.30318v1](https://arxiv.org/abs/2606.30318v1)
