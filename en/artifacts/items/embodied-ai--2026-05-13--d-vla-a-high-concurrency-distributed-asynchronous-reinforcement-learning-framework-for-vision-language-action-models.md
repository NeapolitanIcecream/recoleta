---
source: arxiv
url: https://arxiv.org/abs/2605.13276v2
published_at: '2026-05-13T09:54:31'
authors:
- Yucheng Guo
- Yongjian Guo
- Zhong Guan
- Wen Huang
- Haoran Sun
- Haodong Yue
- Xiaolong Xiang
- Shuai Di
- Zhen Sun
- Luqiao Wang
- Junwu Xiong
- Yicheng Gong
topics:
- vision-language-action
- robot-rl
- distributed-training
- robot-data-scaling
- embodied-ai
- sim2real
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# D-VLA: A High-Concurrency Distributed Asynchronous Reinforcement Learning Framework for Vision-Language-Action Models

## Summary
D-VLA is a distributed RL training system for large Vision-Language-Action models that reduces simulator-training contention. It reports higher throughput on ManiSkill with π0.5 and OpenVLA-OFT than RLinf-VLA and RL-VLA³ baselines.

## Problem
- Large VLA RL runs mix GPU-heavy physics simulation with GPU-heavy model inference and training, which causes memory contention, communication delay, and idle hardware.
- SFT-based robot policies need costly demonstration data and often fail under new tasks or shifted state distributions; online RL can add exploration, but current systems are slow for large VLA models.
- The bottleneck matters because low rollout throughput limits how much interaction data a robot policy can collect during training.

## Approach
- D-VLA splits traffic into a high-frequency data plane for rollouts and a lower-frequency weight control plane for parameter updates.
- A four-thread “Swimlane” pipeline runs sampling, weight receiving, gradient training, and weight distribution in parallel.
- Rollout workers co-locate PhysX-style simulation with a frozen policy copy to reduce observation transfer overhead; actor workers compute GRPO advantages and clipped policy gradients under FSDP.
- The system uses NCCL all-to-all for trajectory transfer and a CPU/Gloo path for background weight broadcast to avoid CUDA stream contention with simulation.
- A dual-pool GPU memory design separates model memory from physics-engine temporary memory, and local topology replication keeps high-frequency sampling-inference traffic inside each node.

## Results
- On π0.5 in the reported single-node setting, D-VLA reaches 147.0 steps/s at 1:1 placement versus RLinf-co at 127.24 steps/s, a 22.25% gain; at 3:1 placement it reaches 237.0 steps/s, an 86.26% gain over RLinf-co.
- On OpenVLA-OFT, D-VLA reports 156.0 steps/s versus RLinf-co at 108.24 steps/s and RL-VLA³ at 110.88 steps/s, a 44.44% gain over RLinf-co.
- In the 16-GPU ManiSkill table for π0.5, D-VLA reaches 336.04 steps/s at 1:1 and 376.00 steps/s at 3:1; the best RL-VLA³ result shown is 250.77 steps/s.
- In the 16-GPU ManiSkill table for OpenVLA-OFT, D-VLA reaches 250.90 steps/s at 1:1; RL-VLA³ reaches 170.48 steps/s at 1:1 and RLinf-dis reaches 107.23 steps/s at 1:1.
- D-VLA cuts π0.5 step time to 488.32 in the 16-GPU 1:1 table, compared with 669.80 for RL-VLA³ 1:1 and 705.50 for RLinf-co.
- The excerpt gives no numeric final success-rate values; it says the ManiSkill success-rate curves show competitive policy quality while training throughput rises.

## Link
- [https://arxiv.org/abs/2605.13276v2](https://arxiv.org/abs/2605.13276v2)
