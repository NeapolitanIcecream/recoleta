---
source: arxiv
url: https://arxiv.org/abs/2605.12624v2
published_at: '2026-05-12T18:09:42'
authors:
- Yuzhou Huang
- Benjin Zhu
- Hengtong Lu
- Victor Shea-Jay Huang
- Haiming Zhang
- Wei Chen
- Jifeng Dai
- Yan Xie
- Hongsheng Li
topics:
- autonomous-driving
- vision-language-action
- streaming-memory
- flow-matching
- trajectory-planning
- language-conditioned-control
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# MindVLA-U1: VLA Beats VA with Unified Streaming Architecture for Autonomous Driving

## Summary
MindVLA-U1 is a streaming vision-language-action model for autonomous driving that keeps language output discrete and vehicle trajectories continuous inside one shared VLM backbone. It claims better planning than prior VA and VLA systems on WOD-E2E while keeping near-VA latency.

## Problem
- Driving VLA models often trail vision-to-action planners because language tokens, temporal context, and continuous control are joined through weak interfaces.
- Discrete trajectory tokens limit control precision, while separate action heads reduce coupling between VLM reasoning and trajectory generation.
- Chunked video-action planning adds temporal cost and can create discontinuities between chunks, which matters for long-tail driving events.

## Approach
- The model processes vision, ego state, language, memory, and noisy action tokens through one VLM backbone in a single pass.
- Language uses autoregressive token prediction; actions use flow matching to generate continuous waypoint trajectories.
- A FIFO streaming memory stores compressed past-frame features, aligns them to the current ego pose, and updates them after each frame.
- A predicted driving intent token conditions the action diffusion through classifier-free guidance, giving language a measured path into trajectory generation.
- Attention masks support fast and slow modes, including action-only inference and language-then-action inference, from one checkpoint.

## Results
- On WOD-E2E, MindVLA-U1 claims 8.20 RFS versus 8.13 GT RFS for experienced human drivers, using 2 diffusion steps.
- It reports about 16 FPS at roughly 1B parameters, compared with RAP at about 18 FPS at a matched roughly 1B scale.
- The paper claims state-of-the-art planning ADEs over prior VA and VLA methods, but the excerpt does not include the ADE values.
- WOD-E2E contains 4,021 roughly 20-second driving segments, with 2,037 training sequences and 479 validation sequences from an 8-camera 360-degree rig.
- MindLabel adds about 3.8M VQA pairs and about 250K dreamed trajectories across about 18.8K clips, though the reported runs use only basic scene VQA and official intent labels.

## Link
- [https://arxiv.org/abs/2605.12624v2](https://arxiv.org/abs/2605.12624v2)
