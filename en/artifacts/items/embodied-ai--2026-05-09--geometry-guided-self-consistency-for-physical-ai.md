---
source: arxiv
url: https://arxiv.org/abs/2605.08638v1
published_at: '2026-05-09T03:14:30'
authors:
- Yinwei Dai
- Zhuofu Chen
- Lijie Yang
- Ravi Netravali
topics:
- vision-language-action
- robot-foundation-model
- world-action-model
- diffusion-policy
- test-time-scaling
- robot-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Geometry Guided Self-Consistency for Physical AI

## Summary
KeyStone improves stochastic diffusion and flow-matching robot action generation by sampling several action chunks at inference and choosing the most central chunk in the largest action-space cluster. It reports success-rate gains up to 13.3 percentage points across VLA and WAM manipulation benchmarks with little added per-round latency.

## Problem
- Diffusion and flow-matching robot policies generate one open-loop action chunk per control round; a bad random sample can derail the episode, and errors compound across many rounds.
- Existing multi-sample selectors such as TACO train an extra scorer per task or embodiment, adding training cost and inference passes.
- Robot deployment depends on reliable per-round action choices under tight latency limits.

## Approach
- KeyStone draws K independent action chunks from the same observation, robot state, and instruction context.
- It flattens each chunk and computes pairwise L2 distances, using action-space distance as a measure of similar robot motion.
- If samples look unimodal, it returns the global medoid; otherwise it runs small k-means clustering, finds the largest cluster, and executes that cluster's medoid.
- The selected chunk is an actual model sample, so the method avoids averaging between action modes.
- It batches the K diffusion chains while sharing the encoded context or cache tensors; the paper profiles K and uses K=4 for GR00T N1.6 and X-VLA, K=16 for the other tested models.

## Results
- On SimplerEnv-WidowX with GR00T N1.6, success rose from 50.0 ± 4.3% to 63.3 ± 2.9% at K=4, a +13.3 point gain.
- On SimplerEnv-Google Robot with GR00T N1.6, success rose from 79.4 ± 3.5% to 86.7 ± 1.5% at K=4, a +7.3 point gain.
- On LIBERO with SmolVLA, success rose from 50.4 ± 2.1% to 57.2 ± 1.3% at K=16, a +6.8 point gain; with π0.5, LIBERO rose from 96.8 ± 0.7% to 97.8 ± 1.1%, a +1.0 point gain.
- On SimplerEnv-WidowX, StarVLA rose from 52.8 ± 1.6% to 59.7 ± 1.3% at K=16, a +6.9 point gain; X-VLA rose from 92.7 ± 1.0% to 95.8 ± 1.0% at K=4, a +3.1 point gain.
- On RoboTwin 2.0 with Fast-WAM, success rose from 90.0 ± 1.5% to 93.0 ± 1.0% at K=16, a +3.0 point gain; this is the WAM test case.
- The paper says KeyStone reaches accuracy on par with model-based selectors such as TACO without selector training. It also reports stable per-round latency and peak GPU memory for K in {1,4,8,16}, but the excerpt does not give exact latency values.

## Link
- [https://arxiv.org/abs/2605.08638v1](https://arxiv.org/abs/2605.08638v1)
