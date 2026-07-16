---
source: arxiv
url: https://arxiv.org/abs/2607.12287v1
published_at: '2026-07-14T02:48:31'
authors:
- Yuzhou Wu
- Yuxin Zheng
- Muchun Niu
- Yishan Yang
- Tianhao Liu
- hanwen kang
- Jiajian Jing
- Linfeng Zhang
- Chuan Wen
topics:
- vision-language-action
- generalist-robot-policy
- efficient-inference
- temporal-token-reuse
- flow-policy-compression
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference

## Summary
The paper accelerates vision-language-action inference by removing redundant computation in visual encoding and flow-based action generation. On LIBERO and RoboTwin, it reports roughly 2.4x faster inference with similar manipulation success, including 8.2 FPS and 93.8% success on LIBERO.

## Problem
- Large VLA models repeatedly encode nearly unchanged video frames and run 8–10 iterative policy-sampling steps, creating latency that limits high-frequency closed-loop robot control.
- Existing acceleration methods often optimize only perception or language modules, while the action expert remains the main latency bottleneck.
- This matters because deployment requires faster responses without sacrificing task success or changing the pretrained backbone.

## Approach
- Reuse cached visual token representations across consecutive frames and recompute only tokens with the largest cosine-similarity changes, using the selected token indices through later ViT layers. The paper reports that about 60% of tokens are recomputed per frame.
- Exploit the low-rank structure of flow-matching velocity trajectories: most velocity variation lies in two dominant directions.
- Train a lightweight adaptor to replace the original 8–10-step flow solver with a 2-step schedule that reconstructs the final action trajectory.
- Apply both mechanisms jointly so that perception and action-generation costs are reduced at the system level.

## Results
- On LIBERO, the method applied to $\pi_{0.5}$ reduces sampling from 10 to 2 steps, lowers latency from 286.9 ms to 121.2 ms, increases throughput from 3.5 to 8.2 FPS, and achieves 93.8% mean success versus 94.4% for the original $\pi_{0.5}$.
- In the detailed LIBERO efficiency table, the method reaches 121.8 ms total latency, 8.2 FPS, and 1.23 TFLOPs, compared with 293.2 ms, 3.4 FPS, and 4.48 TFLOPs for the $\pi_{0.5}$ baseline.
- On RoboTwin 2.0, it reports 125.4 ms latency, 8.0 FPS, 2.80 TFLOPs, and 81.5% TOP10 success, compared with 298.46 ms, 3.35 FPS, 4.38 TFLOPs, and 82.2% for $\pi_{0}$.
- The paper reports nearly 2.6x end-to-end acceleration in simulation and 1.6x on real robot platforms, while maintaining comparable task performance; the excerpt does not provide a detailed real-robot success-rate table.
- The strongest reported gains come from reducing action-expert latency to about 19% of the baseline, while ViT and LLM latency remain close to their original values.

## Link
- [https://arxiv.org/abs/2607.12287v1](https://arxiv.org/abs/2607.12287v1)
