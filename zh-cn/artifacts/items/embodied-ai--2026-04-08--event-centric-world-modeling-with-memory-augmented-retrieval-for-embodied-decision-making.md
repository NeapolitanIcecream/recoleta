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
## 摘要
这篇论文提出了一种面向具身决策的事件中心世界模型。系统会存储过去的情境，并检索相似情境来选择动作。目标场景是动态、安全关键的控制任务，主要用 UAV 导航实验进行验证。

## 问题
- 动态环境中的自主智能体需要快速、符合物理规律、且便于检查的决策。
- 端到端策略可以把观测直接映射为动作，但论文认为，这类方法难以说明为什么会选择某个动作，也难以检查动作是否满足物理可行性。
- 这一点在 UAV 飞行等安全关键场景中很重要，因为不一致或不透明的动作可能导致碰撞或行为不稳定。

## 方法
- 系统将环境转换为一组语义事件，包括检测到的对象、它们的位置与运动、全局上下文、智能体状态和目标方向。
- 一个置换不变编码器将这组事件映射为潜在编码，使智能体能够把当前情境与存储的过往情境进行比较。
- 知识库存储由潜在事件编码、机动动作、奖励或可行性分数组成的三元组；动作选择通过最近邻检索，并对 top-k 匹配项按相似度加权。
- 为避免对彼此不兼容的动作直接求平均，系统会先按方向对检索到的机动动作进行聚类，再只在权重最高的簇内求最终动作平均值。
- 潜在动态受到收缩性和物理感知约束，具体做法包括稳定的线性转移模型、Lyapunov 风格边界、物理一致性正则项，以及用于实时运行的基于 FAISS 的 ANN 检索。

## 结果
- 在 NVIDIA Isaac Sim 的 UAV 实验中，用于预训练的专家数据集包含 **27,075** 条无碰撞轨迹，这些轨迹由 Virtual Potential Field 监督器生成。
- 控制回路按 **20-50 ms** 的更新间隔设计，论文称在嵌入式硬件上，基于 FAISS 的 ANN 搜索可实现**亚毫秒级**检索延迟。
- 在包含 **5 个 episode** 的对抗式课程训练中，训练损失据称在 Episode 2 升至约 **77.9**，随后到 Episode 5 降至约 **2.6**。
- 在论文报告的导航评估中，智能体在全部五个课程 episode 中达到 **100% 成功率**，且**0 次碰撞**。
- 平均轨迹长度约为每 **100 m** 任务 **680 步**。
- 这段摘录没有给出与其他方法的基线对比、消融实验，或除这些内部结果之外的标准基准指标。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07392v1](http://arxiv.org/abs/2604.07392v1)
