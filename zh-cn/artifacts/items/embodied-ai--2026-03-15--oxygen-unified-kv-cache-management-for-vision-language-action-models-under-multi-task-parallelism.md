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
- robot-inference
- parallel-serving
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# OxyGen: Unified KV Cache Management for Vision-Language-Action Models under Multi-Task Parallelism

## Summary
OxyGen提出了一种面向视觉-语言-动作模型（VLA）的统一KV缓存管理方法，用于让机器人在同一观测下并行执行动作生成与语言生成等多任务推理。核心贡献是把KV cache当作跨任务、跨时间共享的资源来调度，从而显著提升设备端推理效率。

## Problem
- 现有MoT VLA虽然架构上支持多模态多任务输出，但推理系统通常仍按任务独立执行，导致共享观测被重复prefill，产生冗余计算。
- 即使能共享部分计算，不同任务也会在单GPU等受限硬件上争用资源；尤其动作任务有硬实时频率要求，而语言生成可跨多帧完成，二者时限不对称。
- 这很重要，因为真实具身智能体需要一边操控、一边对话/记忆/规划；若推理不能高效并行，MoT VLA的多任务能力难以真正落地到机器人端侧部署。

## Approach
- 核心机制是**统一KV缓存管理**：把由共享观测产生的VLM backbone KV cache视为“第一类共享资源”，而不是每个任务各自维护隔离缓存。
- **Cross-task KV sharing**：对同一帧观测只做一次prefill，得到的KV同时供动作专家和语言专家复用，避免重复编码相同输入。
- **Cross-frame continuous batching**：把语言生成从逐帧控制循环中解耦出来；动作任务仍在当前帧内完成，语言请求则保留可恢复状态，在跨帧过程中持续批量解码。
- 系统通过统一KV manager维护每个语言请求的可恢复状态（KV、已生成token、终止标记），支持store/retrieve/update/remove以及batch/unbatch操作，实现中断后无重算恢复。
- 该方法实现于$pi_{0.5}$和openpi之上，属于推理/调度层优化，基本不修改模型本身，因此与压缩、剪枝、异步控制等方法兼容。

## Results
- 论文宣称在单张**NVIDIA RTX 4090**上、基于**$pi_{0.5}$**、跨**3个基准（LIBERO、DROID、ALOHA）**评测时，OxyGen对多任务并行推理可实现**最高3.7×加速**，相对隔离执行基线更快。
- 在同一系统中可**同时**达到**200+ tokens/s**的语言解码吞吐和**70 Hz**的动作频率，满足高频控制与持续语言生成并行需求。
- 文中将低效根因拆为两部分：**重复prefill**会带来约**1.4× slowdown**，而任务间**资源争用**会带来约**2.6× slowdown**；OxyGen分别通过跨任务共享与跨帧批处理缓解这两类问题。
- 论文明确声称在**LIBERO**上使用官方$pi_{0.5}$-LIBERO checkpoint评估时，OxyGen在加速推理的同时**不降低动作质量/任务成功率**，但给定摘录中未提供具体成功率数值。
- 相比简单并行化（如多进程共享GPU）或顺序隔离执行，作者认为其突破在于：不是仅靠任务并发，而是通过统一管理KV缓存来同时降低延迟并提高吞吐。

## Link
- [http://arxiv.org/abs/2603.14371v1](http://arxiv.org/abs/2603.14371v1)
