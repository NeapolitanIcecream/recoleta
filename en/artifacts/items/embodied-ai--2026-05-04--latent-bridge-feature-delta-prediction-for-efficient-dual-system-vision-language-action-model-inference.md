---
source: arxiv
url: https://arxiv.org/abs/2605.02739v1
published_at: '2026-05-04T15:37:55'
authors:
- Yudong Liu
- Yuan Li
- Zijia Tang
- Yuxi Zheng
- Yueqian Lin
- Qinsi Wang
- Yi Li
- Shuangjun Liu
- Shuai Zhang
- Taotao Jing
- Dashan Gao
- Ning Bi
- Jingwei Sun
- Yiran Chen
- Hai Li
topics:
- vision-language-action
- generalist-robot-policy
- robot-inference
- latent-dynamics
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference

## Summary
Latent Bridge speeds up dual-system vision-language-action models by predicting the next VLM feature or KV-cache state between full backbone calls. It keeps success rates close to synchronous inference while cutting many VLM calls.

## Problem
- Dual-system VLAs such as GR00T-N1.6 and $\pi_{0.5}$ run a large VLM backbone at every robot control step, and that backbone dominates latency.
- Consecutive VLM outputs change little over time, so repeated full backbone calls waste compute during real-time manipulation.
- Lower latency matters because robot policies often need 10-50 Hz control, and slow inference can lengthen episodes or reduce task success.

## Approach
- The method trains a small bridge model to predict the feature delta: add a learned change $\Delta_t$ to the latest VLM feature instead of running the VLM again.
- For GR00T, the bridge predicts feature-space deltas used by the action head; for $\pi_{0.5}$, it predicts per-layer KV-cache deltas.
- The bridge uses cached stable visual context, robot state, and the previous action. It copies near-constant text tokens rather than predicting them.
- The VLM runs every $f=2$ to $4$ steps. On skipped steps, the action head consumes bridge-predicted features.
- Training uses synchronous VLM rollouts, then one DAgger refinement round where the bridge acts in simulation and the VLM supplies feature targets along the bridge-induced trajectory.

## Results
- The paper claims 50-75% fewer VLM calls with 95-100% task performance retention across LIBERO, RoboCasa, and ALOHA sim.
- On four LIBERO suites with GR00T-N1.6-3B, synchronous inference gets 96.58% average success rate at 90 ms per step. Latent Bridge gets 94.54% at 49 ms, with 1.73x net episode speedup.
- On four LIBERO suites with $\pi_{0.5}$, synchronous inference gets 96.96% average success rate at 76 ms per step. Latent Bridge gets 96.92% at 46 ms, with 1.65x net episode speedup.
- The replaced VLM backbone costs 46-63 ms per call; bridge steps cost 2 ms for GR00T and 6 ms for $\pi_{0.5}$.
- Feature caching is much weaker: 34.25% average LIBERO success for GR00T and 56.38% for $\pi_{0.5}$ at matched skip settings.
- Cross-benchmark tests report 63.16% success on 24 RoboCasa tasks versus 66.22% sync, and 86.00% on ALOHA transfer-cube versus 88.00% sync.

## Link
- [https://arxiv.org/abs/2605.02739v1](https://arxiv.org/abs/2605.02739v1)
