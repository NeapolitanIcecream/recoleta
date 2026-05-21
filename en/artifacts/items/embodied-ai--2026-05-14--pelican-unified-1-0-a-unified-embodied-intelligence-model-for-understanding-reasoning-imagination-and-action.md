---
source: arxiv
url: https://arxiv.org/abs/2605.15153v1
published_at: '2026-05-14T17:50:42'
authors:
- Yi Zhang
- Yinda Chen
- Che Liu
- Zeyuan Ding
- Jin Xu
- Shilong Zou
- Junwei Liao
- Jiayu Hu
- Xiancong Ren
- Xiaopeng Zhang
- Yechi Liu
- Haoyuan Shi
- Zecong Tang
- Haosong Sun
- Renwen Cui
- Kuishu Wu
- Wenhai Liu
- Yang Xu
- Yingji Zhang
- Yidong Wang
- Senkang Hu
- Jinpeng Lu
- Nga Teng Chan
- Yechen Wu
- Yong Dai
- Jian Tang
- Xiaozhu Ju
topics:
- embodied-foundation-model
- vision-language-action
- robot-world-model
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Pelican-Unified 1.0: A Unified Embodied Intelligence Model for Understanding, Reasoning, Imagination and Action

## Summary
Pelican-Unified 1.0 trains one embodied model to reason in language, predict future video, and output robot action chunks from the same latent state. It targets the gap between perception-heavy VLMs, video world models, and executable robot policies.

## Problem
- Robot systems often split perception, reasoning, future prediction, and control into separate models, which can create mismatched states during long tasks.
- VLA policies such as RT-2, OpenVLA, and π0 map observations to actions, but the excerpt says they usually lack explicit future video prediction.
- Video world models can predict visual futures, but task reasoning and low-level robot actions may stay disconnected.

## Approach
- A Qwen3-VL 4B-based VLM reads observations, action history, and a language instruction, then writes a task- and action-oriented chain of thought.
- The final hidden state of that reasoning trace is projected into a dense latent state `z`, which conditions both future video generation and action prediction.
- A Wan2.2-5B-based diffusion transformer denoises future video latents and continuous action chunks in the same process, with separate input and output heads for each modality.
- Training combines text loss, video flow-matching loss, and action SmoothL1 loss, and all three losses update the shared latent state.

## Results
- On 8 VLM benchmarks, Pelican-Unified scores 64.7 average, compared with 58.2 for Qwen3-VL-4B-Instruct and 27.5 for MolmoAct.
- On embodied VLM benchmarks, it improves over Qwen3-VL-4B-Instruct by +28.2 points on Where2Place and +20.6 points on PhyX.
- On RoboTwin 50-task dual-arm manipulation, it reaches 93.5% average success, with 93.6% in clean settings and 93.3% under randomized conditions.
- On RoboTwin, it beats π0 at 62.2%, π0.5 at 79.8%, starVLA at 88.3%, LingBot-VA at 92.3%, and AIM at 93.1%; the excerpt says it is second-best among compared action methods.
- On RoboTwin, 31 of 50 tasks reach at least 95% success, 39 tasks reach at least 90%, and 15 tasks reach 100%.
- On WorldArena, it reports an EWM Score of 66.03 and ranks first among the compared world-model methods in the excerpt.

## Link
- [https://arxiv.org/abs/2605.15153v1](https://arxiv.org/abs/2605.15153v1)
