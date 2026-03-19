---
source: arxiv
url: http://arxiv.org/abs/2603.09513v1
published_at: '2026-03-10T11:13:54'
authors:
- Wang Honghui
- Jing Zhi
- Ao Jicong
- Song Shiji
- Li Xuelong
- Huang Gao
- Bai Chenjia
topics:
- long-horizon-manipulation
- non-markovian-tasks
- vq-memory
- vision-language-action
- simulation-benchmark
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks

## Summary
This paper proposes a new simulation benchmark, RuleSafe, for long-horizon, non-Markovian manipulation tasks, as well as a plug-in temporal memory module called VQ-Memory. The core idea is to compress a robot’s past joint-state sequence into a small number of discrete memory tokens, allowing existing VLA/diffusion policies to more robustly remember “which stage of the task they are currently in.”

## Problem
- Existing robotic simulation benchmarks mostly focus on short-horizon, simple pick-and-place tasks, making them inadequate for evaluating the multi-stage, rule-dependent manipulation tasks that are common in the real world.
- For articulated objects such as locked safes, door handles, and knobs, the current visual frame is often insufficient to determine the task stage; such tasks are **non-Markovian** and require memory and temporal reasoning.
- Directly using visual history is computationally expensive; directly using raw joint-state history is lightweight, but it is easily affected by low-level noise and tends to overfit to trajectories.

## Approach
- Build **RuleSafe**: using LLM-assisted rule and program generation to create 20 safe-unlocking rules in SAPIEN, including key, password, logic lock, and others, requiring multi-step reasoning and manipulation.
- Organize tasks with two types of latent variables: **part-phase** (discrete part states, such as open/closed) and **task-phase** (task progress stages), thereby creating long-horizon tasks that are visually similar but semantically different.
- Propose **VQ-Memory**: feed a past proprioceptive joint-state sequence into a VQ-VAE and encode it into discrete latent tokens, preserving high-level task-stage information while filtering low-level continuous noise.
- After training the VQ-VAE, apply **K-means clustering** to the codebook, compressing 256 fine-grained codes into a smaller vocabulary (set to 4 in the paper), emphasizing semantic patterns shared across trajectories.
- This memory module is **model-agnostic**: for DP3, it maps memory tokens with a small convolutional network; for RDT, CogACT, and π0, it appends memory tokens as special language tokens to the input.

## Results
- The RuleSafe benchmark contains **20 lock rules** and **10 types of safes**; the average success rate of generated demonstrations is **71.7%**, and the average trajectory length is **638 frames**.
- Single-task training setting: **100 demonstrations** per task; multi-task setting: **1000 trajectories across 20 tasks**, i.e., **50 per task**.
- The VQ-Memory implementation provides a clear compression setup: time window **50**, stride **20**, about **20× compression ratio**; the original vocabulary size **256** is compressed by clustering to **4**, with memory token length **40**.
- Experiments cover SOTA policies such as **DP3, RDT, CogACT, and π0**; the authors claim that VQ-Memory **consistently improves long-horizon planning, generalization to unseen configurations, and reduces computational cost** in both single-task and multi-task settings.
- However, the currently provided paper excerpt does not include the specific **SR/PS values, dataset breakdowns, or exact improvement margins over baselines** from the full result tables, so more detailed quantitative comparisons cannot be listed reliably.

## Link
- [http://arxiv.org/abs/2603.09513v1](http://arxiv.org/abs/2603.09513v1)
