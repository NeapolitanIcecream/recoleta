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
- robot-manipulation
- flow-matching
- one-step-generation
- mean-flow
relevance_score: 0.42
run_id: materialize-outputs
---

# Mean-Flow based One-Step Vision-Language-Action

## Summary
本文提出一种用于机器人操作的 Mean-Flow 单步 Vision-Language-Action 框架，把传统需要多步积分的 FlowMatching 动作生成改成可一步完成的均值向量场预测，从而显著降低延迟。核心价值是在尽量保持动作质量与稳定性的同时，把 VLA 控制速度提升到更适合实时机器人应用的水平。

## Problem
- 现有 FlowMatching/diffusion 类 VLA 虽然能生成连续、高频动作，但推理通常依赖多步迭代采样，导致机器人控制延迟高。
- 当 FlowMatching 把推理步数压低时，Euler 积分误差会放大，动作会偏向数据均值，质量明显下降，形成“速度 vs. 精度”的硬权衡。
- 这对灵巧操作和实时控制很关键，因为机器人需要快速响应新视觉输入，同时保持轨迹连续、稳定、可执行。

## Approach
- 方法核心是把学习目标从**瞬时去噪向量场**改成**区间上的平均去噪向量场（mean vector field）**，也就是直接学习“从噪声到动作的大方向”，而不是每个微小时间步的局部方向。
- 训练时引入 MeanFlow Identity，用网络预测均值向量场，并用由瞬时场和时间导数修正项构造的目标进行监督；实现上用 JVP 计算导数项，并用 stop-gradient 避免高阶反传不稳定。
- 推理时可直接一步生成动作块：从噪声动作 $A_1$ 出发，计算 $A_0 = A_1 - u_\theta(A_1,0,1)$，从而省掉传统多步数值积分。
- 在 VLA 架构上，冻结预训练 VLM（SmolVLM-2）作为多模态编码器，只训练基于 Transformer 的 Mean-Flow action expert 来输出未来动作 chunk。
- 论文还做了关键训练设计：混合学习瞬时场与均值场（flow-ratio），并用 adaptive loss 替代纯 $L_2$ 以提升收敛稳定性。

## Results
- 真实机器人实验声称：该方法的动作生成速度比 **SmolVLA 快 8.7 倍**，比 **Diffusion Policy 快 83.9 倍**。
- 在超参数实验中，**flow-ratio=0.2**、**NFE=5** 时成功率最佳，为 **84.5%**；相比之下，flow-ratio=0.5 为 **80.5%**，flow-ratio=1.0 仅 **4.5%**。
- 在损失函数实验中，adaptive loss 的 **$\gamma=0.5$** 最优，成功率 **86.0%**；$\gamma=0.3$ 为 **79.5%**，而纯 $L_2$（$\gamma=1.0$）只有 **9.5%**。
- 实验平台为 6-DoF SO-101 机械臂，覆盖 **3 个真实任务**（pick-place、stacking、sorting），总计 **300 条轨迹**、每任务 **100 条示范**。
- 摘要和正文明确宣称其在**单步或少步生成**下仍具鲁棒表现，但提供的摘录中未完整给出所有任务上相对 SmolVLA / Diffusion Policy 的成功率表格，因此无法逐项列出完整精度对比数字。

## Link
- [http://arxiv.org/abs/2603.01469v1](http://arxiv.org/abs/2603.01469v1)
