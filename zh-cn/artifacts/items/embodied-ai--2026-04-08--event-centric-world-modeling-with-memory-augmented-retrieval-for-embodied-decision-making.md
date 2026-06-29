---
source: arxiv
url: http://arxiv.org/abs/2604.07392v1
published_at: '2026-04-08T06:14:46'
authors:
- Fan Zhaowen
topics:
- world-model
- memory-augmented-retrieval
- uav-navigation
- interpretable-control
- embodied-decision-making
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making

## Summary
## 概述
本文提出一种面向具身决策的事件中心世界模型，系统会保存过去情境，并检索相似情境来选择动作。该系统面向动态且安全关键的控制任务，主要用 UAV 导航实验做验证。

## 问题
- 动态环境中的自主智能体需要快速、物理一致且易于检查的决策。
- 端到端策略可以把观测映射到动作，但文中认为，这类方法会掩盖动作选择原因，也让物理可行性更难检查。
- 这在 UAV 飞行等安全关键场景中很重要，因为不一致或不透明的动作可能导致碰撞或不稳定行为。

## 方法
- 系统把环境转成一组语义事件：检测到的目标、它们的位置和运动、全局上下文、智能体状态以及目标方向。
- 一个对置换不敏感的编码器把这组事件映射成潜在编码，这样智能体就能把当前情境和存储的历史情境进行比较。
- 知识库保存潜在事件编码、机动动作以及奖励或可行性评分三元组；动作选择使用最近邻检索，并对 top-k 匹配按相似度加权。
- 为了避免把不相容的动作平均在一起，检索到的机动动作会按方向聚类，最终动作只在权重最高的簇内求平均。
- 潜在动力学加入收缩性和物理感知约束，使用稳定的线性转移模型、Lyapunov 风格界限、物理一致性正则项，并用 FAISS 做基于 ANN 的检索，以支持实时使用。

## 结果
- 在 NVIDIA Isaac Sim 的 UAV 实验中，用于预训练的专家数据集包含 **27,075** 条无碰撞轨迹，这些轨迹由 Virtual Potential Field supervisor 生成。
- 控制循环设计为 **20-50 ms** 的更新间隔，文中声称在嵌入式硬件上使用基于 FAISS 的 ANN 搜索时，检索延迟可低于 **1 毫秒**。
- 在一个包含 **5 个 episode** 的对抗式课程学习设置中，训练损失在第 2 个 episode 上升到约 **77.9**，随后在第 5 个 episode 降到约 **2.6**。
- 在报告的导航评估中，智能体在全部五个课程 episode 中都取得了 **100% 成功率**，且 **0 次碰撞**。
- 平均轨迹长度约为每 **100 m** 任务 **680 步**。
- 这段摘要没有给出与其他方法的基线比较，也没有消融实验，标准基准指标之外也没有更多结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07392v1](http://arxiv.org/abs/2604.07392v1)
