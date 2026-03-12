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
- self-supervised-learning
- hyperbolic-embeddings
- 3d-pretraining
- multiview-learning
relevance_score: 0.19
run_id: materialize-outputs
---

# Hyperbolic Multiview Pretraining for Robotic Manipulation

## Summary
该论文提出 HyperMVP，用双曲空间而非欧氏空间做3D多视角自监督预训练，以提升机器人操作中的空间感知、鲁棒性与泛化。它还构建了大规模 3D-MOV 数据集，并在模拟与真实场景中报告了优于强基线的结果。

## Problem
- 现有机器人操作的3D视觉预训练大多在**Euclidean**嵌入空间中进行，难以表达层次化、结构化的空间关系，导致场景理解和扰动泛化不足。
- 机器人在真实部署中必须面对视角变化、环境扰动和场景多样性；仅靠任务级多任务训练，常在这些条件下性能下降。
- 高质量预训练数据昂贵，因此除了扩数据，还需要提升表示空间本身的建模能力，使同等数据下学到更强的空间表征。

## Approach
- 提出 **HyperMVP**：一个遵循“预训练-微调”范式的3D多视角自监督框架，把点云渲染成5个正交视图，用类似 MAE 的方式学习表示，但把表示提升到**Lorentz model** 下的双曲空间。
- 设计 **GeoLink encoder**：先用 ViT 提取每个视图的 patch/CLS 特征，再通过指数映射把欧氏特征映射到双曲空间；之后再用对数映射送回欧氏空间，以兼容下游机器人策略网络。
- 为了在无监督下学到“有结构”的双曲表示，使用两个关键约束：**Top-K neighborhood rank correlation loss** 保持欧氏与双曲空间中 patch 邻域排序一致；**entailment loss** 用局部-全局的包含关系建模层次结构。
- 预训练任务不只做单视图重建，还联合 **intra-view reconstruction** 与 **inter-view reconstruction**，让模型既重建本视图，也根据其他视图预测锚视图，从而学习跨视角3D一致性。
- 构建 **3D-MOV** 数据集：包含 200,052 个点云样本、约 1M 多视图图像，覆盖 object、indoor scene、tabletop 等四类3D数据，用于支持大规模预训练。

## Results
- 在 **COLOSSEUM** 上，论文声称 HyperMVP 在所有扰动设置下，相比“此前最佳基线”取得**平均 33.4% 提升**。
- 在 COLOSSEUM 最困难的 **All Perturbations** 设置中，论文报告相对性能达到**2.1× gain**。
- 在 **RLBench** 多任务操作中，作者称将 GeoLink 编码器与 RVT 结合，明显优于 **RVT from scratch** 以及在欧氏空间预训练的模型，但给定摘录中**未提供具体数值表格**。
- 在真实世界实验中，作者声称 HyperMVP 具有**强现实有效性**，同时保持与模拟中一致的泛化优势；摘录中**未给出具体成功率数字**。
- 预训练数据规模方面，3D-MOV 含 **180K** Objaverse-XL 对象点云、**6,052** 细分 indoor scene 点云、**3,999** vanilla tabletop 与 **10,001** crowd tabletop 点云，总计 **200,052** 个点云、约 **1M** 渲染图像。
- 方法层面，作者宣称这是**首个**将3D多视角双曲预训练用于机器人操作的框架，并且由于 view-decoupled 设计，微调时可扩展到**任意数量输入视图**。

## Link
- [http://arxiv.org/abs/2603.04848v1](http://arxiv.org/abs/2603.04848v1)
