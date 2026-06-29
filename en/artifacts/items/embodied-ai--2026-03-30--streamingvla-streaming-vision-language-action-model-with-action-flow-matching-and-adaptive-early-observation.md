---
source: arxiv
url: http://arxiv.org/abs/2603.28565v1
published_at: '2026-03-30T15:23:27'
authors:
- Yiran Shi
- Dongqi Guo
- Tianchen Zhao
- Feng Gao
- Liangzhi Shi
- Chao Yu
- ZhiJian Mo
- Qihua Xiao
- XiaoShuai Peng
- Qingmin Liao
- Yu Wang
topics:
- vision-language-action
- robot-foundation-models
- streaming-inference
- action-flow-matching
- early-observation
- libero-benchmark
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation

## Summary
StreamingVLA speeds up vision-language-action inference by running observation, action generation, and execution in parallel instead of waiting for each stage to finish. It targets edge and real-world robot deployment where VLA latency causes slow, stop-and-go motion.

## Problem
- Standard VLA pipelines such as $\pi_{0.5}$ run observation, action generation, and execution in sequence, so the robot waits between action bursts.
- This creates high per-action latency and a large halting gap $T_{\text{halt}} = T_{o}+T_{g}$, which makes execution stutter.
- The issue matters for embodied systems on resource-limited hardware because a strong policy is less useful if control is too slow or jerky for real tasks.

## Approach
- The paper proposes **StreamingVLA**, a staged asynchronous execution scheme that overlaps action generation with execution and overlaps observation with ongoing execution.
- For generation/execution overlap, it replaces chunked diffusion-style action prediction with **action flow matching (AFM)**, which predicts one action as a state update along a trajectory. In simple terms, the model outputs the next small action directly, so the robot can execute it at once instead of waiting for a full action chunk.
- To make AFM work in larger VLA systems, the authors add an extended action-space state formulation and modify normalization so additivity is preserved when states are updated by accumulated actions.
- For observation/execution overlap, they add **adaptive early observation (AEO)**. A lightweight transformer predicts how much remaining actions will change the next observation embedding, and the system only observes early when those skipped actions have low saliency.
- The runtime analysis formalizes two overlap terms, $O_{ge}$ and $O_{oe}$, showing that overlapping stages reduces both time per action and halting gap without needing to shrink the base model.

## Results
- On **LIBERO** with **$\pi_{0.5}$** as the base model, the baseline at $h=5$ gets **96.9% average success**, **74.5 ms** time per action, and **232.3 ms** halting gap.
- **StreamingVLA (AFM)** keeps **97.1% average success** while reducing time per action to **33.7 ms (2.21x speedup)** and halting gap to **76.1 ms (3.05x reduction)**.
- **StreamingVLA (AFM + AEO)** reports the best balanced streaming result: **94.9% average success**, **31.625 ms** time per action (**2.36x speedup** vs. baseline), and **36.0 ms** halting gap (**6.45x reduction**).
- The abstract reports an overall **2.4x latency speedup** and **6.5x lower execution halting** without sacrificing performance.
- Compared with prior fast-execution baselines on LIBERO, **VLASH** shows **40.6 ms** per action at **97.1%** average success, while **StreamingVLA (AFM)** is faster at **33.7 ms** with the same **97.1%** average success; adding AEO cuts latency further with some success-rate drop.
- Naive early observation hurts performance: **AFM+NEO** reaches **29.3 ms** per action and **23.0 ms** halting gap, but average success falls to **86.2%**. The saliency-aware AEO variant recovers much of that loss to **94.9%** average success.

## Link
- [http://arxiv.org/abs/2603.28565v1](http://arxiv.org/abs/2603.28565v1)
