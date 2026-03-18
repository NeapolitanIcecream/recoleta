---
source: arxiv
url: http://arxiv.org/abs/2603.14371v1
published_at: '2026-03-15T13:23:56'
authors:
- Xiangyu Li
- Huaizhi Tang
- Xin Ding
- Weijun Wang
- Ting Cao
- Yunxin Liu
topics:
- vision-language-action
- kv-cache
- multi-task-inference
- robotics
- continuous-batching
relevance_score: 0.69
run_id: materialize-outputs
---

# OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism

## Summary
OxyGen提出一种面向视觉-语言-动作模型的统一KV缓存管理机制，用于让机器人在同一观测下并行执行动作与语言等多任务推理。它把KV缓存当作跨任务、跨时间共享的核心资源，从而显著提升设备端推理效率。

## Problem
- 现有MoT视觉-语言-动作模型虽然架构上支持多任务输出，但推理系统通常仍按任务隔离执行，导致同一观测被重复编码。
- 这种隔离式KV缓存管理带来两类低效：**重复prefill计算**与**GPU资源争用**，尤其在动作需要硬实时、语言生成可跨帧延迟的场景中更严重。
- 该问题很重要，因为具身智能体需要一边控制机器人、一边对话/记忆/规划，而设备端通常只有单GPU等受限算力。

## Approach
- 核心方法是**unified KV cache management**：把由共享观测产生的KV缓存视为“一级共享资源”，而不是每个任务各自独立持有。
- **Cross-task KV sharing**：同一帧中先对观测做一次prefill，得到共享KV缓存，再同时供动作专家和语言专家复用，避免重复编码。
- **Cross-frame continuous batching**：把语言生成从逐帧控制循环中解耦，允许跨多个控制帧持续恢复和批处理多个语言请求；动作任务仍在每帧内完成以满足硬截止时间。
- 系统通过统一KV管理器保存“可恢复生成状态”，包括KV缓存、已生成token和终止标志，并支持store/retrieve/update/remove以及batch/unbatch操作。
- 作者将其实现到**π_{0.5}**之上，并在openpi框架上落地，作为一种位于模型之上的调度/执行优化层，无需修改模型本身。

## Results
- 论文声称在单张 **NVIDIA RTX 4090** 上、针对 **π_{0.5}** 的多任务并行推理，OxyGen相对隔离执行可实现**最高 3.7× 加速**。
- 在代表性机器人配置和**3个基准**（**LIBERO、DROID、ALOHA**）上，系统可同时达到**超过 200 tokens/s** 的语言吞吐与**70 Hz** 的动作频率。
- 作者明确指出，隔离式执行中的两类额外开销包括：**重复计算导致 1.4× slowdown**，以及**资源争用导致 2.6× slowdown**（文中引用Sec. 4.3）。
- 论文还宣称上述加速是**without action quality degradation**，并在 **LIBERO** 上检查任务成功率以验证不会降低动作质量。
- 给定摘录中，除上述吞吐/频率/加速数据外，未提供更细的逐基准数值表、成功率具体百分比或与Parallel baseline的完整量化对比。

## Link
- [http://arxiv.org/abs/2603.14371v1](http://arxiv.org/abs/2603.14371v1)
