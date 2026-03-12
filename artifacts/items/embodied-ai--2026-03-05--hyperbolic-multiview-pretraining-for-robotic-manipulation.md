---
source: arxiv
url: http://arxiv.org/abs/2603.04848v1
published_at: '2026-03-05T06:04:01'
authors:
- Jin Yang
- Ping Wei
- Yixin Chen
topics:
- robotic-manipulation
- self-supervised-pretraining
- hyperbolic-representation-learning
- multiview-3d
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
---

# Hyperbolic Multiview Pretraining for Robotic Manipulation

## Summary
本文提出 HyperMVP，一种把机器人操作的3D多视角自监督预训练从欧氏空间扩展到双曲空间的方法，以学习更有结构的视觉表示。它还构建了大规模 3D-MOV 数据集，并在仿真与真实场景中报告了更强的泛化与鲁棒性。

## Problem
- 现有机器人操作视觉预训练大多在**欧氏空间**中学习表示，平坦几何难以表达层次化、结构化的空间关系。
- 这会限制机器人在**场景扰动、跨任务和真实环境**中的空间感知与泛化能力，而这正是部署到现实世界的关键。
- 单纯扩大数据规模成本高，因此需要一种**更高效地提升表示质量**的方法，而不仅是继续堆数据。

## Approach
- 提出 **HyperMVP**：先在3D点云渲染得到的五视角正交图像上做自监督预训练，再把预训练编码器与 **RVT** 联合微调用于机器人操作策略学习。
- 核心机制很简单：先用 ViT/MAE 风格编码器提取多视角特征，再把这些欧氏特征“抬升”到**双曲空间（Lorentz model）**，让表示更容易组织出层次和结构关系。
- 设计 **GeoLink encoder**，并用两个自监督约束学习双曲表示：**Top-K 邻域排序相关损失**保持欧氏/双曲空间中邻居次序一致，**entailment loss**约束全局与局部特征形成偏层次化的包含关系。
- 预训练任务不只有常规的**单视角重建**，还加入**跨视角重建**，让模型从其他视角预测锚视角，强化3D与多视角一致性。
- 构建 **3D-MOV** 作为预训练数据：共 **200,052** 个3D点云、约 **100万** 张渲染图像，包含物体、室内场景和桌面场景等四类数据；并且该方法在微调时可扩展到**任意数量输入视角**。

## Results
- 在 **COLOSSEUM** 泛化基准上，作者声称 HyperMVP 相比此前最优基线在所有扰动设置下取得**平均 33.4% 提升**。
- 在 COLOSSEUM 最困难的 **All Perturbations** 设置中，作者报告达到 **2.1×** 的性能增益，说明对复杂环境扰动更稳健。
- 在 **RLBench** 多任务操作中，结合 **GeoLink encoder** 的 RVT 相比**从头训练 RVT**以及采用**欧氏空间表示**的方法都有显著提升，但摘要/节选中**未给出具体数值**。
- 在**真实世界实验**中，论文声称 HyperMVP 也表现出较强有效性，同时保持可比或更好的泛化；但节选中**没有提供明确量化指标**。
- 数据规模方面，预训练使用的 **3D-MOV** 含 **200,052** 个点云与约 **1M** 多视角图像；实现上预训练 **100 epochs**、mask ratio **0.75**、图像分辨率 **224×224**、每个点云 **5** 个正交视角。

## Link
- [http://arxiv.org/abs/2603.04848v1](http://arxiv.org/abs/2603.04848v1)
