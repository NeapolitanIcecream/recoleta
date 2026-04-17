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
这篇论文研究同时使用 2D 图像和 3D 点云的视觉-语言-动作模型中的 token 剪枝。论文的核心观点是，剪枝策略应当根据 2D 和 3D 显著性在预处理、语义推理和动作展开这几个阶段的变化来设计，这样可以在精度损失较小的情况下加快推理。

## 问题
- 多视觉模态 VLA 模型在 2D 输入之外加入了 3D token，这会增加序列长度并拖慢推理。论文称，这类模型通常只能以 **3 到 5 Hz** 运行，低于实时控制大约需要的 **20 到 30 Hz**。
- 现有 token 剪枝方法是为仅使用 2D 的 VLA 模型设计的，因此无法捕捉 **2D 和 3D token 在模态、语义区域和时间步上 usefulness 的差异**。
- 在机器人控制中，如果剪掉了错误的 token，任务成功率会下降。论文展示了简单剪枝会带来明显下滑，例如在 Close Box 任务中，对 2D token 进行 **50%** 剪枝时，成功率会从 **55.00%** 降到 **6.67%**。

## 方法
- 该方法围绕 MVLA 推理的三个阶段构建了一个**三阶段 token 剪枝框架**：数据预处理、语义综合和动作迭代。
- 在第 1 阶段，方法用模型最终层特征的 **L1 范数**来度量模态显著性，并分别计算 **2D** 和 **3D** token 的显著性分数。这些分数用于为两种模态设置不同的剪枝阈值。
- 在第 2 阶段，方法使用基于注意力的聚类，将图像块分成 **背景、机器人和物体** 等语义集合，然后衡量每个集合内部 2D 和 3D 的重要性。论文还将 3D 注意力分解为重叠部分和独有部分，用来估计 3D token 的独特价值。
- 在第 3 阶段，方法跟踪模态显著性在动作步骤中的变化，并加入**时间分段和显著性预测**，使剪枝能够在执行过程中动态调整。
- 最终的剪枝策略结合这三类信号，决定保留哪些 2D 和 3D token。

## 结果
- 摘要称，该框架可实现**最高 2.55× 推理加速**，同时**精度损失很小**，额外开销只有 **5.8%**。
- 在论文对 **RLBench** 任务和 **MLA** 模型进行的第 1 阶段分析中，剪掉 **3D** token 往往比剪掉 **2D** token 带来的损害更小，这支持按模态区分的剪枝方式。例子：在 **Close Box** 上，基线成功率为 **55.00%**；进行 **50% 2D 剪枝**后降到 **6.67%**；进行 **50% 3D 剪枝**后为 **40.00%**。
- 在这项简单剪枝研究中，有些任务在进行 3D 剪枝后反而提升。**50% 剪枝**时的例子包括：**Close Fridge** 从 **56.66%** 升到 **70.00%**，**Close Laptop** 从 **80.00%** 升到 **90.00%**，**Sweep Dustpan** 从 **66.67%** 升到 **96.67%**。
- 第 1 阶段的显著性指标显示，在列出的任务中，2D 显著性明显高于 3D 显著性，例如 Close Box 上为 **90.16% vs 9.84%**，Close Fridge 上为 **81.47% vs 18.53%**，Close Laptop 上为 **90.38% vs 9.62%**。
- 对于第 2 阶段和第 3 阶段，摘录只给出了定性结论：在 **robot** 和 **object** 语义区域中，3D 显著性高于 2D；在操作过程中，模态显著性会随时间变化。除摘要中的加速结论外，这段摘录没有提供这些阶段完整的端到端基准表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09244v1](http://arxiv.org/abs/2604.09244v1)
