---
source: arxiv
url: http://arxiv.org/abs/2603.29090v1
published_at: '2026-03-31T00:11:29'
authors:
- Jaber Jaber
- Osama Jaber
topics:
- object-centric-world-model
- robotics
- causal-representation-learning
- state-space-models
- slot-attention
- hierarchical-dynamics
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling

## Summary
## 摘要
HCLSM 是一个面向机器人场景的、以对象为中心的视频世界模型，结合了 slots、多时间尺度动力学和学习得到的交互图。论文的核心主张是，需要分阶段训练，先得到类似对象的 slots，再进行未来预测；否则未来预测会把模型推向扁平的分布式编码。

## 问题
- 标准视频世界模型用单一的扁平状态预测未来潜变量，因此会把不同对象混在一起，忽略不同时间尺度，也无法显式表示因果交互。
- 对机器人规划和反事实推理来说，模型应能跟踪独立对象，处理连续运动和离散事件，并捕捉哪些对象会影响其他对象。
- 论文对比表中的现有系统只覆盖了这些需求的一部分：SlotFormer 有对象表示，但没有层级结构或因果性；DreamerV3 有潜在动力学，但没有对象分解；V-JEPA 风格模型使用非结构化潜变量。

## 方法
- HCLSM 先用 ViT 对视频帧编码，再用 slot attention 将场景拆分为对象 slots。空间广播解码器按 slot 重建冻结的 ViT 特征，让 slots 竞争空间归属。
- 它的动力学堆栈分为三层：逐对象的 selective state space model 处理逐帧物理过程，只在检测到事件的帧上运行的 sparse transformer，以及汇总更高层目标的 compressed transformer。
- GNN 用学习得到的边权在 slots 之间传递消息，模型还加入了 NOTEARS 风格的 DAG 正则项来学习因果结构，不过论文称显式因果图在实践中效果不好。
- 训练分为两个阶段。第 1 阶段只使用重建损失和多样性项，覆盖前 40% 的训练步数，让 slots 先分化。第 2 阶段在 slots 已经带有空间结构后，再开启 JEPA 风格的未来预测。
- 为了让训练可行，实现在 selective SSM scan 上加入了自定义 Triton kernel、GPU Sinkhorn 跟踪，以及分块的 GNN 边计算。

## 结果
- 在 LeRobot / Open X-Embodiment 的 PushT 上，一个 6800 万参数的 HCLSM 用 206 个 episode、25,650 帧训练后，采用两阶段方法达到 **0.008 的下一状态预测 MSE**。
- 同一两阶段训练还报告了 **0.008 的 SBD loss** 和 **0.132 的 diversity loss**，而不使用 SBD 的变体 **diversity loss 为 0.154**。不使用 SBD 的模型取得了更低的预测损失 **0.002**，作者将其归因于更容易形成分布式编码，而不是对象分解。
- 表 3 中，两阶段模型在报告设置下的吞吐量为 **2.9 steps/s**，不使用 SBD 的变体为 **2.3 steps/s**。
- 自定义 Triton SSM kernel 在 tiny 配置上带来 **39.3x 加速**（**6.22 ms -> 0.16 ms**），在 base 配置上带来 **38.0x**（**69.64 ms -> 1.83 ms**），测试硬件为 NVIDIA T4。
- 定性结果显示，基于 slot 的空间分解开始出现，但分解较弱：在一个大约只有 **3 个对象** 的场景里，**32 个 slots** 全部保持活跃，而且每个对象都被拆分到多个 slots 中。
- 事件检测在每个 16 帧序列中找到大约 **2-3 个事件**。因果邻接矩阵没有学到有用的边，而且由于 bf16 NaN 不稳定，**4 次**训练运行中只有 **2 次**完成。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29090v1](http://arxiv.org/abs/2603.29090v1)
