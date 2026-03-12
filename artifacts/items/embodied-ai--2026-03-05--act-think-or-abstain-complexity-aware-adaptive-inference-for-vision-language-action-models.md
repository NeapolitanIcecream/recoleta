---
source: arxiv
url: http://arxiv.org/abs/2603.05147v1
published_at: '2026-03-05T13:14:41'
authors:
- Riccardo Andrea Izzo
- Gianluca Bardaro
- Matteo Matteucci
topics:
- vision-language-action
- adaptive-inference
- ood-detection
- robot-safety
- uncertainty-estimation
relevance_score: 0.95
run_id: materialize-outputs
---

# Act, Think or Abstain: Complexity-Aware Adaptive Inference for Vision-Language-Action Models

## Summary
本文提出一个面向视觉-语言-动作（VLA）模型的自适应推理框架，根据当前状态复杂度在**直接执行（Act）**、**额外推理（Think）**和**拒绝执行（Abstain）**之间切换，以兼顾效率、泛化与安全。核心发现是：用于判断任务复杂度时，**视觉嵌入比语言或融合特征更可靠**。

## Problem
- 现有VLA常通过链式思维等推理提升泛化，但**所有时刻都推理**会增加计算成本和延迟，对简单任务浪费资源。
- 这些方法通常**缺少不确定性/分布外识别能力**，在OOD任务上可能过度自信并导致灾难性执行失败。
- 机器人部署需要同时满足**实时性、泛化性和安全性**，因此需要一种能先判断“该不该直接做”的机制。

## Approach
- 从预训练VLA/SmolVLA的VLM骨干中提取**vision、text、fused**三类嵌入；作者还专门让文本编码不看图像，以分离语言不确定性。
- 先用**PCA降到64维**，再用两类新颖度估计器给特征打分：**GMM+Mahalanobis距离**建模全局分布，**1-NN**捕捉局部异常；GMM使用**Ledoit-Wolf shrinkage**稳定协方差估计。
- 将分数汇总为一个小向量（主要含视觉/文本/融合的GMM分数和视觉kNN分数），输入轻量**MLP**，输出三类决策：**Act / Think / Abstain**。
- “Think”分支只在**每个episode首个时刻**触发一次，追加场景线索和子目标到文本提示中，再交给VLA执行；“Abstain”则直接拒绝高风险OOD任务。
- 为了训练中间态“部分OOD/Think”，作者除使用**LIBERO-PRO**外，还用**Beta(0.5,0.5) mixup**在ID与OOD特征之间合成中间样本。

## Results
- 在**LIBERO / LIBERO-PRO / 真实机器人（SO-ARM 101）**上评估；最佳配置为**MLP + GMM（vision-only）**，**Macro F1 = 84.34%**，优于所有替代方案。
- 与直接在原始嵌入上训练的**Baseline MLP**相比，作者方法显著更强：Baseline仅**63.81% Macro F1**；且**86% 的“Think”样本被误判为“Act”**，说明基线对模糊场景过度自信。
- **视觉kNN**也有竞争力，达到**73.90% F1**，并且作者称其在混淆矩阵中**“Act”和“Abstain”之间无混淆**，即不会把应停止的任务误放行为直接执行。
- 多模态并未带来收益：**ensemble（all GMM + kNN）71.41% F1**，**text-only 54.76% F1**，且text-only对“Think”类别**一个也没识别对**。这支持“语言语义不变性会掩盖物理异常”的论点。
- 数据效率方面，baseline在不同数据量下几乎停留在**F1≈0.60**；而**vision-only GMM**在仅用**1%数据**（少于1000样本）时就比baseline**高15%**，并在**5%数据**时接近峰值性能。摘要还报告其**vision-only配置仅用5%训练数据即可达到80% F1**。
- GMM组件数消融显示最佳为**k=3**；**k=1**明显不足，而更大k带来收益递减和额外计算开销。

## Link
- [http://arxiv.org/abs/2603.05147v1](http://arxiv.org/abs/2603.05147v1)
