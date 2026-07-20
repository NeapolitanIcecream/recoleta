---
source: arxiv
url: https://arxiv.org/abs/2607.16074v1
published_at: '2026-07-17T15:58:20'
authors:
- Haoran Sun
- Wentao Zhang
- Junyang Hua
- Hedan Yang
- Yongjian Guo
- Yifei Zhang
- Xiaolong Xiang
- Mingxi Luo
- Jing Long
- Chen Zhao
- Chen Zhou
- Wanting Xu
- Qiming Yang
- Hui Zhang
- Song Wang
- Xiaodong Bai
- Shuai Di
- Xu Chu
- Xiaotie Deng
- Yicheng Gong
- Junwu Xiong
topics:
- robot-foundation-model
- vision-language-action
- robot-data-scaling
- sim2real
- generalist-robot-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models

## Summary
JoyNexus presents a service-oriented platform for multi-tenant post-training of vision-language-action models. It shares resident VLA backbones across supervised fine-tuning, reinforcement learning, rollout, and evaluation workloads while isolating each tenant’s trainable modules and state.

## Problem
- VLA post-training spans heterogeneous robot embodiments, simulators, datasets, action schemas, and objectives, making infrastructure management difficult for individual users.
- Exclusive GPU allocation and fixed card-hour accounting can waste resources during rollout, data loading, evaluation, or other bursty phases.
- Existing service-oriented post-training systems mainly target language models and do not directly provide VLA-specific environment interaction, policy synchronization, and evaluation workflows.

## Approach
- JoyNexus separates the Training Model Service, Inference Model Service, and Environment Service behind APIs coordinated by a Master Service.
- A shared base VLM remains resident, while tenant-specific action modules, optimizer states, checkpoints, and policy versions occupy isolated slots and remain separately addressable.
- High-level APIs compile SFT, RL, and evaluation specifications into service workflows; lower-level APIs allow users to compose custom algorithms.
- Global Training and Inference Queues schedule concurrent tenant workloads, while fault isolation, monitoring, and elastic rollout scaling support long-running jobs.
- Group batching combines heterogeneous samples with a compatible model-facing prefix so multiple tenants can reuse one shared-backbone forward pass.

## Results
- Workload simulation and a group-batching pipeline in a realistic embodied scenario reportedly reduce aggregate GPU time and improve service utilization compared with isolated single-tenant execution.
- The provided text reports no numerical values for GPU-time reduction, utilization, latency, throughput, or comparison workload size, so the magnitude of the efficiency improvement cannot be determined from this excerpt.
- The paper evaluates system efficiency rather than proposing a new VLA policy, training objective, or robot-control benchmark.

## Link
- [https://arxiv.org/abs/2607.16074v1](https://arxiv.org/abs/2607.16074v1)
