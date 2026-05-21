---
source: arxiv
url: https://arxiv.org/abs/2604.24447v1
published_at: '2026-04-27T13:12:16'
authors:
- Kaijun Zhou
- Qiwei Chen
- Da Peng
- Zhiyang Li
- Xijun Li
- Jinyu Gu
topics:
- vision-language-action
- robot-foundation-models
- on-robot-inference
- edge-accelerators
- vla-acceleration
- hardware-profiling
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment

## Summary
This paper measures Vision-Language-Action inference across GPUs, NPUs, and XPUs, then adds two latency optimizations for on-robot use. Its main claim is that the best robot accelerator depends on latency, cost, and energy, not peak GPU speed alone.

## Problem
- VLA robot policies must run inside a closed observe-infer-act loop; high latency can cause stuttering, oscillation, or task failure.
- Most VLA evaluations use desktop GPUs such as RTX 4090, which hides cost, energy, memory, and control-rate limits on mobile robots.
- Model size alone does not predict latency: Diffusion Policy can be slower than larger pi0 because it uses 100 denoising steps while pi0 uses 4.

## Approach
- The paper builds a model-hardware leaderboard for VLA pairs and ranks them with CET: cost, energy, and time.
- It profiles VLA inference across RTX 4090, Jetson Thor, AGX Orin, Intel B60 Pro, and Ascend NPUs, with VRAM and control-frequency filters before ranking.
- It identifies two recurring phases: a compute-bound VLM backbone and a memory-bound Action Expert.
- DP-Cache reuses stable intermediate computation inside iterative diffusion to cut redundant denoising work.
- V-AEFusion overlaps the VLM and Action Expert stages with asynchronous pipeline parallelism.

## Results
- For pi0, the leaderboard reports RTX 4090 at 102.3 ms and 2.398 kJ, Jetson Thor at 246.0 ms and 1.282 kJ, AGX Orin at 920.6 ms and 1.866 kJ, Intel B60 Pro at 306.5 ms and 6.363 kJ, and Ascend 310P at 818.0 ms and 2.618 kJ.
- Profiling pi0 shows the VLM backbone usually above 90% SM utilization, while the Action Expert runs at about 20% to 40% SM utilization and takes about 2x the VLM latency.
- Roofline analysis reports pi0 VLM DecoderLayer intensity near 840 FLOPs/Byte, above the RTX 4090 ridge point of 330 FLOPs/Byte, so it is compute-bound; the Action Expert is 64.5 FLOPs/Byte, so it is memory-bound on RTX 4090, Jetson Thor, and AGX Orin.
- Compilation speeds up pi0 from 102.3 ms to 35.2 ms on RTX 4090, a 2.90x gain and 28.41 Hz; from 246.0 ms to 163.0 ms on Jetson Thor, a 1.51x gain and 6.13 Hz; and from 818.0 ms to 350.0 ms on Ascend 310P, a 2.34x gain and 2.86 Hz.
- On OpenVLA, Speculative plus Cache reaches 1.29x speedup and 6.99 Hz, but average LIBERO success drops from the 76.5% baseline to 68.5%.
- The paper claims DP-Cache and V-AEFusion reach up to 2.9x speedup on GPUs and 6x on edge NPUs, with only small task-success loss.

## Link
- [https://arxiv.org/abs/2604.24447v1](https://arxiv.org/abs/2604.24447v1)
