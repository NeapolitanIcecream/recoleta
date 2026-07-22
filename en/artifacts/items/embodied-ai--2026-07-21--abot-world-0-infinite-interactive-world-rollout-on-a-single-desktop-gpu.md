---
source: arxiv
url: https://arxiv.org/abs/2607.19191v1
published_at: '2026-07-21T15:26:50'
authors:
- Fan Jiang
- Zhaoxu Sun
- Mengchao Wang
- Ziyu Zhu
- Chiyu Wang
- Yunpeng Zhang
- Wenlin Liu
- Yun Wang
- Xue Zheng
- Rui Sun
- Junfeng Ni
- Hongyu Pan
- Zhongxu Sun
- Fei Yu
- Zengye Ge
- Mengmeng Du
- Nianfei Fan
- Mingchao Sun
- Yu Liu
- Yongchang
- Yanqing Zhu
- Jiahang Wang
- Ning Ying
- Yuze Xuan
- Di Yang
- Zhicheng Liu
- Zhe Gao
- Tingbing Xu
- Jiacheng Sui
- Wenjin Yang
- Junnan Lai
- Shufeng Liu
- Yuan Liu
- Zheng Zhou
- Yingliang Peng
- Dawei Cao
- Kaifeng Sheng
- Yuxiang Cai
- Fei Lu
- Mu Xu
- Ning Guo
topics:
- world-model
- interactive-video-generation
- long-horizon-rollout
- real-time-inference
- robot-data-scaling
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# ABot-World-0: Infinite Interactive World Rollout on a Single Desktop GPU

## Summary
ABot-World-0 is an action-conditioned video world model designed for persistent, interactive rollouts on a single desktop GPU. It combines multi-source data collection, long-horizon rollout training, keyboard-based control, and low-bit streaming inference to produce 720P video at up to 16 FPS.

## Problem
- Interactive world models must keep visual state coherent while user actions change the environment over long closed-loop rollouts.
- Existing systems face coupled limits in synchronized action data, controllability, autoregressive drift, latency, throughput, and GPU memory; solving these matters for local simulation, agent learning, and embodied-AI research.

## Approach
- WorldExplorer collects synchronized game and simulation trajectories, while internet videos add visual diversity; a unified pipeline applies 14 deterministic quality checks, VLM assessment, action labels, and text annotations.
- The model uses a shared frame-synchronous keyboard action space for camera movement and character control, with reference-character memory to preserve identity during third-person rollouts.
- A bidirectional action-conditioned teacher is progressively distilled into a causal student using teacher forcing and ODE distillation.
- LongForcing trains the student on its own long self-rollouts under supervision from an extended-horizon teacher, targeting accumulated autoregressive drift.
- A deployment stack combines a lightweight VAE decoder, memory-aware scheduling, low-bit DiT inference, efficient attention, and bounded KV caching for streaming generation.

## Results
- On a single NVIDIA RTX 5090, the system streams 720P video at up to 16 FPS with 1.2 seconds of action-to-first-frame latency and approximately 19 GiB peak VRAM.
- WorldExplorer reports cross-modal alignment error below 33 ms at 30 FPS for captured video, controls, camera parameters, and environment state.
- Experiments on WorldRoamBench and extended interactive rollouts demonstrate controllability, visual quality, physical plausibility, and temporal-memory consistency, with the paper excerpt describing the results as competitive.
- The provided text does not report numerical WorldRoamBench scores, ablations, or baseline-by-baseline comparisons, so the relative performance of LongForcing and the full system cannot be quantified from this excerpt.

## Link
- [https://arxiv.org/abs/2607.19191v1](https://arxiv.org/abs/2607.19191v1)
