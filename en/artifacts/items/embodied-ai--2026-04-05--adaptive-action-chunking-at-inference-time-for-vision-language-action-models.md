---
source: arxiv
url: http://arxiv.org/abs/2604.04161v1
published_at: '2026-04-05T16:03:32'
authors:
- Yuanchang Liang
- Xiaobo Wang
- Kai Wang
- Shuo Wang
- Xiaojiang Peng
- Haoyu Chen
- David Kim Huat Chua
- Prahlad Vadakkepat
topics:
- vision-language-action
- robot-policy-inference
- action-chunking
- robot-manipulation
- uncertainty-estimation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Adaptive Action Chunking at Inference-time for Vision-Language-Action Models

## Summary
AAC is an inference-time method for vision-language-action models that picks action chunk size on the fly instead of using one fixed value for a whole episode. It uses action entropy from sampled candidate trajectories to choose shorter chunks when predictions are uncertain and longer chunks when predictions are stable.

## Problem
- VLA policies often execute action chunks: several future actions are planned and then run without replanning at every step.
- Fixed chunk size creates a trade-off. Large chunks reduce responsiveness to new observations, while small chunks can cause discontinuities, jerky motion, and more mode-jumping between replans.
- The best chunk size changes across tasks and even across phases of one task, so manual tuning with one fixed value limits performance and scalability.

## Approach
- AAC runs only at inference time and does not change training or model architecture.
- The model samples **N** candidate action chunks in parallel, then estimates uncertainty at each future timestep using entropy: Gaussian differential entropy for continuous translation/rotation actions and standard entropy for the discrete gripper action.
- For each possible execution length **h**, AAC computes the average action entropy over the first **h** steps of the predicted chunk.
- It selects the chunk size at the point where the average entropy changes most across chunk lengths, with a lower bound **ξ** so the robot still executes a minimum number of actions before replanning.
- In practice, high entropy leads to short execution and frequent replanning; low entropy leads to longer execution for smoother behavior and fewer model calls.

## Results
- On **RoboCasa**, GR00T with default fixed chunk size **h=16** gets **59.7%** average success, while **GR00T + AAC** reaches **62.0%**, a **+2.3 point** gain across **24 tasks**.
- On RoboCasa **Rotation** tasks, success improves from **57.6%** to **61.4%** with AAC. On **Container** tasks, it improves from **80.3%** to **82.2%**. On **Relocation**, it improves from **42.1%** to **44.4%**.
- On **LIBERO**, GR00T with fixed **h=16** gets **94.1%** average success, while **AAC** reaches **95.0%**. On the harder **LIBERO-Long** suite, performance rises from **88.8%** to **92.8%**, a **+4.0 point** gain.
- Against other fixed chunk sizes on RoboCasa, AAC's **62.0%** average beats **h=2: 47.0%**, **h=4: 56.2%**, **h=8: 61.2%**, **h=12: 60.2%**, and **h=16: 59.7%**.
- With a different backbone, **pi-0.5** on LIBERO improves from **97.0%** average success to **97.9%** with AAC; the biggest listed gain is on **Long** tasks, from **92.5%** to **95.2%**.
- On **LIBERO-Pro** OOD perturbation tests, **GR00T** improves from **3.9%** average to **6.3%** with AAC, and **pi-0.5** improves from **30.9%** to **34.8%**.

## Link
- [http://arxiv.org/abs/2604.04161v1](http://arxiv.org/abs/2604.04161v1)
