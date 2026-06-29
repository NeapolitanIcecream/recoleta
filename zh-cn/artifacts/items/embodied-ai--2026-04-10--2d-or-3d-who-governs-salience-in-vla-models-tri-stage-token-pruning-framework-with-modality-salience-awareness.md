---
source: arxiv
url: http://arxiv.org/abs/2604.09244v1
published_at: '2026-04-10T11:58:39'
authors:
- Zihao Zheng
- Sicheng Tian
- Zhihao Mao
- Lingyue Zhang
- Chenyue Li
- Ziyun Zhang
- Hong Gao
- Yuchen Huang
- Yutong Xu
- Guojie Luo
- Xiang Chen
topics:
- vision-language-action
- token-pruning
- multimodal-robotics
- 3d-perception
- inference-acceleration
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# 2D or 3D: Who Governs Salience in VLA Models? -- Tri-Stage Token Pruning Framework with Modality Salience Awareness

## Summary
## 摘要
本文研究了同时使用 2D 图像和 3D 点云的视觉-语言-动作模型的 token 剪枝。核心观点是，剪枝应当跟随 2D 和 3D 重要性在预处理、语义推理和动作展开三个阶段中的变化，这样可以在较小精度损失下提升推理速度。

## 问题
- 多视觉模态 VLA 模型把 3D token 加到 2D 输入上，序列长度更长，推理也更慢。论文指出，这类模型通常只有 **3 到 5 Hz**，低于实时控制所需的约 **20 到 30 Hz**。
- 现有 token 剪枝方法是为仅使用 2D 的 VLA 模型设计的，因此没有覆盖 **2D 和 3D token 在模态、语义区域和时间步上的差异**。
- 在机器人控制中，剪错 token 会损害任务成功率。论文展示，朴素剪枝会带来很大的下降，例如在 **Close Box** 任务中，剪掉 **50%** 的 2D token 后，成功率从 **55.00%** 降到 **6.67%**。

## 方法
- 该方法围绕 MVLA 推理的三个阶段构建了一个 **三阶段 token 剪枝框架**：数据预处理、语义合成和动作迭代。
- 在第一阶段，它用模型最后一层特征的 **L1 范数**衡量模态重要性，并分别计算 **2D** 和 **3D** token 的重要性分数。这些分数用于给两种模态设定不同的剪枝阈值。
- 在第二阶段，它用基于注意力的聚类把 patch 分成 **背景、机器人、物体** 等语义集合，再衡量 2D 和 3D 在每个集合中的作用。论文还把 3D 注意力拆成重叠部分和独有部分，用来估计 3D token 的独特价值。
- 在第三阶段，它跟踪动作步骤中模态重要性的变化，并加入 **时间分段和重要性预测**，让剪枝在执行过程中可以调整。
- 最终的剪枝策略把这三类信号结合起来，决定保留哪些 2D 和 3D token。

## 结果
- 摘要声称，该方法最多可实现 **2.55× 的推理加速**，精度损失很小，额外开销只有 **5.8%**。
- 在论文第一阶段对 **RLBench** 任务和 **MLA** 模型的分析中，剪枝 **3D** token 往往比剪枝 **2D** token 造成的损害更小，这支持按模态进行剪枝。例如在 **Close Box** 任务中，基线成功率是 **55.00%**；剪掉 **50% 2D token** 后降到 **6.67%**；剪掉 **50% 3D token** 后是 **40.00%**。
- 一些任务在朴素的 3D 剪枝后反而提升。以 **50% 剪枝** 为例：**Close Fridge** 从 **56.66%** 提高到 **70.00%**，**Close Laptop** 从 **80.00%** 提高到 **90.00%**，**Sweep Dustpan** 从 **66.67%** 提高到 **96.67%**。
- 第一阶段的重要性指标显示，列出的任务里 2D 重要性远高于 3D 重要性，例如 **Close Box** 为 **90.16% vs 9.84%**，**Close Fridge** 为 **81.47% vs 18.53%**，**Close Laptop** 为 **90.38% vs 9.62%**。
- 对于第二和第三阶段，这段摘要只给出定性结论：在 **机器人** 和 **物体** 语义区域中，3D 重要性高于 2D，而且在操作过程中，模态重要性会随时间变化。除摘要中的加速结果外，节选内容没有给出这两个阶段的完整端到端基准表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09244v1](http://arxiv.org/abs/2604.09244v1)
