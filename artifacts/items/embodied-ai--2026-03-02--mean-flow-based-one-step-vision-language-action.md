---
source: arxiv
url: http://arxiv.org/abs/2603.01469v1
published_at: '2026-03-02T05:30:30'
authors:
- Yang Chen
- Xiaoguang Ma
- Bin Zhao
topics:
- vision-language-action
- flow-matching
- one-step-generation
- robot-manipulation
- mean-flow
relevance_score: 0.95
run_id: materialize-outputs
---

# Mean-Flow based One-Step Vision-Language-Action

## Summary
本文提出一种基于 MeanFlow 的单步 Vision-Language-Action 框架，把传统需要多步积分的 FlowMatching 动作生成改为直接预测“平均去噪方向”，从而显著降低机器人动作生成延迟。它面向真实机器人操作，重点解决高频连续动作生成在实时部署中的效率瓶颈。

## Problem
- 现有 FlowMatching-based VLA 虽然比扩散策略更高效，但仍依赖多步数值积分；步数一降，动作质量会明显变差。
- 这会造成**实时控制中的延迟—精度权衡**：想快就会失真，想准就得多步推理，难以用于灵巧操作。
- 对机器人而言，这很重要，因为高频、连续、低延迟的动作生成直接影响抓取、堆叠、分拣等真实世界任务的成功率和稳定性。

## Approach
- 核心方法是把学习目标从传统 FlowMatching 的**瞬时向量场**，改成 MeanFlow 的**区间平均去噪向量场**；直观上，就是不再一步步“沿路走”，而是直接预测从噪声动作到目标动作的平均方向。
- 模型使用一个预训练且冻结的 VLM 主干融合多视角图像、语言指令和本体状态；动作专家基于 Transformer，条件生成未来动作块。
- 训练时随机采样时间对 \(r,t\)，同时学习局部瞬时信息和跨区间平均流；作者引入 `flow-ratio` 控制两类样本配比，以兼顾局部精度与全局稳定性。
- 为缓解 MeanFlow 目标中的高方差与多模态动作数据带来的训练不稳，作者将普通 \(L_2\) 损失替换为自适应损失，在不做蒸馏、预训练或一致性正则的情况下提升收敛稳定性。
- 推理时可直接单步生成：从高斯噪声动作出发，一次前向就得到整段连续动作；也支持少步生成作为折中。

## Results
- 在真实机器人实验中，作者声称该方法的动作生成速度比 **SmolVLA 快 8.7 倍**，比 **Diffusion Policy 快 83.9 倍**。
- 数据与平台：3 个真实操作任务（pick-place、stacking、sorting），共 **300 条轨迹**；每个任务 **100 个示范**；机器人为 **6-DoF + gripper** 的 SO-101，输入含双目 RGB、语言和本体状态，动作空间 **7 维**。
- 超参数实验（pick-place，**NFE=5**）显示：`flow-ratio=0.2` 时成功率 **84.5%**，优于 `0.5` 的 **80.5%**，远高于 `1.0` 的 **4.5%**。
- 损失实验（`flow-ratio=0.2`, **NFE=5**）显示：自适应损失 `gamma=0.5` 成功率 **86.0%**，优于 `gamma=0.3` 的 **79.5%**，显著高于纯 \(L_2\)（`gamma=1.0`）的 **9.5%**。
- 论文摘要明确宣称其在**单步与多步生成模式**下都具有稳健表现，但给定摘录中未提供各真实任务相对 SmolVLA / Diffusion Policy 的完整任务成功率表格或更细粒度定量对比。

## Link
- [http://arxiv.org/abs/2603.01469v1](http://arxiv.org/abs/2603.01469v1)
