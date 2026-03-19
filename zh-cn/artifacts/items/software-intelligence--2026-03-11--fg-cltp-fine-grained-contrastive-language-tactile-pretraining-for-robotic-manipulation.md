---
source: arxiv
url: http://arxiv.org/abs/2603.10871v1
published_at: '2026-03-11T15:21:54'
authors:
- Wenxuan Ma
- Chaofan Zhang
- Yinghao Cai
- Guocai Yao
- Shaowei Cui
- Shuo Wang
topics:
- robotic-manipulation
- tactile-learning
- multimodal-pretraining
- contrastive-learning
- vision-language-action
relevance_score: 0.33
run_id: materialize-outputs
language_code: zh-CN
---

# FG-CLTP: Fine-Grained Contrastive Language Tactile Pretraining for Robotic Manipulation

## Summary
FG-CLTP提出一种把触觉3D点云与包含数值信息的语言对齐的预训练框架，用于更精细的机器人接触感知与操控。它试图把“粗略语义触觉”升级为“可量化物理触觉”，并进一步接入动作策略。

## Problem
- 现有触觉-语言模型大多只学到**定性描述**，如“粗糙”“硬”“强压”，却难以表达操控真正需要的**定量接触状态**，如力大小、接触深度、位置、主轴方向。
- 2D触觉图像表征往往**传感器相关**，容易混入硬件和光照伪差，限制跨传感器泛化与sim-to-real迁移。
- 缺少既有**大规模多模态数据**、又能把语言和物理量精确对应起来的预训练方式，会让高层语义难以转化为低层精细控制。

## Approach
- 构建了**Contact3D**数据集，包含**100k**触觉3D点云-语言配对样本，覆盖**136**个物体，并带有力/扭矩、接触位置、面积、主轴、滑动/扭转等接触状态标注。
- 用**离散数值tokenization**把连续物理量分桶成语言token，例如深度、面积、位置、角度等，让模型能把“数字化物理状态”直接写进文本提示中。
- 采用**3D触觉点云 + 语言 + 触觉图像**的多模态对比学习，在共享特征空间中对齐；语言编码器冻结原有词表，只学习新增数值token，减少遗忘。
- 增加**辅助回归损失**，直接监督深度、位置、主轴等连续属性，增强表示对精细物理量的敏感性。
- 在下游提出**3D-TLA**，将预训练触觉编码器接入基于flow matching的策略网络，用于接触密集型 manipulation。

## Results
- 论文宣称FG-CLTP达到**95.9%**分类准确率，并且相对SOTA将回归**MAE降低52.6%**。
- 在离线分类基准中，报告**90.6%**的形状分类准确率，以及**97.6%**的深度分类准确率、**97.6%**的位置分类准确率。
- 论文摘要声称使用3D点云表征可实现**3.5% sim-to-real gap**，并提供更强的跨传感器泛化。
- 数据集规模上，Contact3D包含**4种传感器、136个物体、100k样本**，相比表中多个已有数据集更完整地覆盖depth、force、language和dynamic属性。
- 回归表格在节选中被截断，无法完整核对所有任务上的具体数值、最佳基线名称和逐项改进幅度；但文中明确主张其在接触状态理解和真实操控任务上显著优于强基线。

## Link
- [http://arxiv.org/abs/2603.10871v1](http://arxiv.org/abs/2603.10871v1)
