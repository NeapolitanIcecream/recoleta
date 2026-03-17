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
- robot-manipulation
- long-horizon-planning
- non-markovian-tasks
- vq-vae
- temporal-memory
relevance_score: 0.16
run_id: materialize-outputs
---

# Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks

## Summary
本文提出了一个面向机器人长时程、非马尔可夫操作的新基准 RuleSafe，以及一种轻量级时间记忆方法 VQ-Memory。核心思想是把过去的本体关节状态压缩成离散记忆 token，帮助策略分辨视觉上相似但阶段不同的操作过程。

## Problem
- 现有机器人仿真基准多为短时程、简单抓放任务，难以覆盖真实世界中带锁、带多关节依赖的复杂操作。
- 这类任务具有**非马尔可夫性**：只看当前图像，往往无法判断任务进行到哪一步，因此策略容易在长链条操作中失败。
- 直接使用视觉历史计算代价高，而直接使用原始关节历史又容易受噪声影响并对轨迹过拟合。

## Approach
- 提出 **RuleSafe**：一个基于 LLM 辅助生成的保险箱操作基准，包含 key、password、logic 等 20 种锁规则，强调多阶段推理与操作依赖。
- 用两类隐藏状态构造任务：**part-phase** 表示部件离散状态，**task-phase** 表示多阶段任务进度，从而系统性地产生长时程、非马尔可夫任务。
- 提出 **VQ-Memory**：先用 VQ-VAE 将过去一段关节状态序列编码为离散 token，再通过后处理聚类把冗余码本进一步压缩成更粗粒度、更稳定的语义记忆。
- 该记忆表示是模型无关的：对 VLA 模型可作为特殊语言 token 注入，对 diffusion policy 则映射为额外潜变量输入。
- 为提升效率，作者使用较大时间窗与步长（window=50, stride=20），声称约实现 **20× compression ratio**，在保留阶段信息的同时减少计算负担。

## Results
- RuleSafe 基准包含 **20** 条锁规则、**10** 类保险箱；演示生成的平均成功率为 **71.7%**，平均轨迹长度为 **638 frames**，表明任务具有较高复杂度。
- 评测覆盖 DP3、RDT、CogACT、π0 等多种策略；文中明确声称 VQ-Memory 在单任务、多任务以及不同架构上都能**持续提升 long-horizon planning、unseen configuration generalization，并降低计算成本**。
- VQ-Memory 的离散记忆由原始码本 **256** 聚类到最终词表 **4**，记忆 token 长度为 **40**；相较直接保留连续历史，方法强调更强鲁棒性与更低冗余。
- 论文摘录中未给出各模型在具体数据集/规则上的完整定量对比表（如 SR/PS 提升幅度、相对 baseline 数值），因此无法精确列出逐项性能增益。
- 从实验设置看，单任务训练使用 **100 demonstrations/task**；多任务训练使用总计 **1000 trajectories**（每任务 **50** 条），用于验证其跨任务泛化与适配性。

## Link
- [http://arxiv.org/abs/2603.09513v1](http://arxiv.org/abs/2603.09513v1)
