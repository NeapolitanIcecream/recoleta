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
---

# Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks

## Summary
本文提出了一个面向长时程、非马尔可夫操作任务的新仿真基准 RuleSafe，以及一种可插拔的时序记忆模块 VQ-Memory。核心思想是把机器人过去的关节状态序列压缩成少量离散记忆 token，从而让现有 VLA/扩散策略更稳健地记住“任务进行到哪一步了”。

## Problem
- 现有机器人仿真基准大多偏向短时程、简单抓放，难以评估真实世界中常见的多阶段、带规则依赖的操作任务。
- 对于带锁的保险箱、门把、旋钮等关节物体，当前视觉帧往往不足以判断任务阶段；任务具有**非马尔可夫性**，需要记忆与时序推理。
- 直接使用视觉历史计算开销大；直接使用原始关节状态历史虽轻量，但容易受低层噪声影响并对轨迹过拟合。

## Approach
- 构建 **RuleSafe**：基于 LLM 辅助生成规则与程序，在 SAPIEN 中创建 20 种保险箱解锁规则，包括 key、password、logic lock 等，需要多步推理与操作。
- 用两类隐变量组织任务：**part-phase**（部件离散状态，如开/关）和 **task-phase**（任务进度阶段），从而制造视觉上相似但语义不同的长时程任务。
- 提出 **VQ-Memory**：将过去一段本体关节状态序列输入 VQ-VAE，编码成离散 latent token，保留高层任务阶段信息、过滤低层连续噪声。
- 在 VQ-VAE 训练后，再对 codebook 做 **K-means 聚类**，把 256 个细粒度码压缩成更小词表（文中配置为 4），强调跨轨迹共享的语义模式。
- 该记忆模块是**模型无关**的：对 DP3 用小卷积网络映射记忆 token；对 RDT、CogACT、π0 则把记忆 token 当作特殊语言 token 拼接输入。

## Results
- RuleSafe 基准包含 **20 个锁规则**、**10 类保险箱**；演示生成的平均成功率为 **71.7%**，平均轨迹长度为 **638 帧**。
- 单任务训练设置：每个任务 **100 条 demonstrations**；多任务设置：**20 个任务共 1000 条轨迹**，即每任务 **50 条**。
- VQ-Memory 的实现配置给出了明确压缩比：时间窗口 **50**、步幅 **20**，约 **20× compression ratio**；原始词表 **256** 经聚类压缩到 **4**，记忆 token 长度 **40**。
- 实验覆盖 **DP3、RDT、CogACT、π0** 等 SOTA 策略，作者声称 VQ-Memory 在单任务和多任务设置下都能**持续提升长时程规划、泛化到未见配置，并降低计算开销**。
- 但当前提供的论文摘录未包含完整结果表格中的具体 **SR/PS 数值、数据集分项、以及相对 baseline 的精确提升幅度**，因此无法可靠列出更细的定量比较。

## Link
- [http://arxiv.org/abs/2603.09513v1](http://arxiv.org/abs/2603.09513v1)
