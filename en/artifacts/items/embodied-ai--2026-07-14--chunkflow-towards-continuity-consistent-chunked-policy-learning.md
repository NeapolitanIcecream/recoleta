---
source: arxiv
url: https://arxiv.org/abs/2607.12992v1
published_at: '2026-07-14T17:43:25'
authors:
- Zhao Yang
- Yinan Shi
- Mingyuan Yao
- Wenyao Xue
- Yawei Jueluo
- Longjun Liu
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning

## Summary
ChunkFlow addresses temporal jitter in vision-language-action policies that generate overlapping action chunks. It combines seam-aware training with deterministic overlap blending to improve continuity, long-horizon success, and inference efficiency without adding a policy forward pass at deployment.

## Problem
- Consecutive action chunks can disagree in their overlapping steps because they use shifted observations and executed histories, creating boundary jitter and unstable robot motion.
- Inference-only smoothing methods reweight conflicting actions but do not correct the policy errors that cause seam mismatch, allowing residual errors to accumulate over long rollouts.

## Approach
- Partition each chunk into frozen, editable seam, and future zones, then linearly blend overlapping actions so control shifts deterministically from the previous chunk to the current one.
- Train raw chunk predictions with a boundary loss plus first-order total-variation and second-order curvature penalties.
- Corrupt action histories and use scheduled sampling so the policy is exposed to execution-history errors during training.
- Fine-tune with advantage-weighted actor-critic updates using post-blending histories while retaining the seam and continuity regularizers.

## Results
- On CALVIN ABC-D, ChunkFlow reports an average episode length of 4.30, with MSD-Δa of 0.075, MSD-Δ²a of 0.154, seam jump of 0.209, HF ratio of 0.431, and TV-L1 of 0.001.
- On LIBERO-Long, it achieves 93.4% success versus 92.6% for PI0.5, 83.7% for PI0.5-RTC, 83.8% for CLIP-RT, and 53.7% for OpenVLA.
- On LIBERO-Long, it reports the lowest listed motion and artifact metrics: MSD-Δa 0.042, MSD-Δ²a 0.197, MSD-Δ³a 0.235, seam jump 0.082, HF ratio 0.135, and TV-L1 0.011.
- Its average reasoning latency on LIBERO is 4.43 ms, compared with 18.47 ms for PI0.5-RTC and 9.04 ms for PI0.5.
- In two real-robot tasks, the paper reports 9/10 successful trials; the excerpt does not provide task-level baselines or statistical uncertainty.

## Link
- [https://arxiv.org/abs/2607.12992v1](https://arxiv.org/abs/2607.12992v1)
