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
HCLSM 是一个面向机器人场景、以对象为中心的视频世界模型，把 slot、多时间尺度动力学和学习到的交互图结合起来。论文的核心观点是，模型要先通过分阶段训练学出像对象一样的 slot，再做未来预测；否则，预测会把表示推回到扁平的分布式编码。

## 问题
- 标准视频世界模型用一个扁平状态预测未来 latent，结果会把对象混在一起，漏掉不同时间尺度，也看不出因果交互。
- 对机器人规划和反事实推理来说，模型应该跟踪不同对象，处理连续运动和离散事件，并捕捉哪些对象会影响其他对象。
- 论文对比表里的现有系统只覆盖了其中一部分：SlotFormer 有对象但没有层次或因果，DreamerV3 有 latent 动力学但没有对象分解，V-JEPA 风格模型使用的是无结构 latent。

## 方法
- HCLSM 先用 ViT 编码视频帧，再用 slot attention 把场景拆成对象 slot。空间广播解码器对每个 slot 重建冻结的 ViT 特征，这样 slot 会争夺空间归属。
- 它的动力学堆栈有三层：面向单个对象的 selective state space model 处理帧到帧的物理变化，稀疏 transformer 只在检测到事件帧时运行，压缩 transformer 总结更高层的目标。
- GNN 用学到的边权在 slot 之间传递消息，模型还加入了类似 NOTEARS 的 DAG 正则项来学习因果结构，不过论文说显式因果图在实践中效果不好。
- 训练分两阶段。第一阶段在前 40% 的步数里只用重建项和多样性项，让 slot 先分化。第二阶段在 slot 已经带有空间结构后，再开启 JEPA 风格的未来预测。
- 实现里加了 selective SSM scan 的自定义 Triton kernel、GPU Sinkhorn 跟踪，以及分块 GNN 边计算，保证训练可行。

## 结果
- 在 LeRobot / Open X-Embodiment 的 PushT 上，68M 参数的 HCLSM 用 206 个 episode 和 25,650 帧训练后，采用两阶段方法达到 **0.008 的 next-state prediction MSE**。
- 同一次两阶段训练报告 **SBD loss 0.008** 和 **diversity loss 0.132**；没有 SBD 的版本对应的 **diversity loss 是 0.154**。没有 SBD 的模型预测损失更低，为 **0.002**，作者把这归因于更容易形成分布式编码，而不是对象分解。
- 表 3 里的吞吐量显示，两阶段模型在给定设置下为 **2.9 steps/s**，没有 SBD 的版本为 **2.3 steps/s**。
- 在 NVIDIA T4 上，自定义 Triton SSM kernel 在 tiny 配置下带来 **39.3x** 加速（**6.22 ms -> 0.16 ms**），在 base 配置下带来 **38.0x** 加速（**69.64 ms -> 1.83 ms**）。
- 定性结果显示 slot 式空间分解开始出现，但分解很弱：大约 **3 个对象** 的场景里，**32 个 slot** 都保持激活，每个对象又被拆到很多 slot 里。
- 事件检测在每个 **16 帧** 序列里找出大约 **2-3 个事件**。因果邻接矩阵没有学到有用的边，而且由于 bf16 NaN 不稳定性，**4 次**训练运行里只有 **2 次**完成。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29090v1](http://arxiv.org/abs/2603.29090v1)
