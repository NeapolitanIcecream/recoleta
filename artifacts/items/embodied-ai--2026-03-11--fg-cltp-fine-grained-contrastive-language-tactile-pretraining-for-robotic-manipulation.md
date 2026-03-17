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
- tactile-learning
- vision-language-action
- robot-manipulation
- sim2real
- contrastive-pretraining
relevance_score: 0.93
run_id: materialize-outputs
---

# FG-CLTP: Fine-Grained Contrastive Language Tactile Pretraining for Robotic Manipulation

## Summary
FG-CLTP提出一种把3D触觉点云与带数字令牌的语言对齐的预训练框架，用于让机器人不仅理解“接触是什么样”，还理解“接触有多大、多深、朝哪个方向”。它同时配套了一个10万级Contact3D数据集和下游3D-TLA策略，用于接触密集型操作。

## Problem
- 现有触觉-语言表示大多停留在**定性描述**，如“硬”“粗糙”“按得很深”，却难以表达机器人控制真正需要的**定量接触状态**，如力大小、接触深度、位置和主轴方向。
- 2D触觉图像表示往往**强依赖传感器外观与照明**，跨传感器泛化差，不利于统一的机器人基础模型。
- 缺少既覆盖**多维接触物理量**、又适合语言对齐和策略学习的大规模触觉数据，这限制了精细操作能力与sim2real迁移。

## Approach
- 构建**Contact3D**数据集：包含**100k**触觉-语言样本、**136**个物体、**4种传感器**，每个样本含3D形变点云、触觉图像、力/力矩和接触状态标注。
- 以**3D触觉点云**作为统一表示，避免2D触觉图像中的传感器特有伪影，强调几何形变与剪切等物理线索。
- 提出**离散数字令牌化**：把连续接触属性（如深度、面积、位置、主轴角度）分箱后写入语言提示词，使模型把“数字物理量”与“语言语义”对齐。
- 用**对比学习**联合对齐触觉点云、语言和触觉图像；冻结原有CLIP词表，仅学习新增数字token，减少遗忘。
- 加入**辅助回归损失**直接监督深度、位置、主轴等连续物理量；并在下游提出**3D-TLA**，将该表示接入基于flow matching的VLA策略进行动作生成。

## Results
- 论文摘要声称，FG-CLTP在接触状态理解上达到**95.9% classification accuracy**，并且相对SOTA将**回归MAE降低52.6%**。
- 在线性探针分类实验中，模型达到**90.6%**的形状分类准确率，以及**97.6%**的深度分类和**97.6%**的位置分类准确率。
- 论文声称基于3D点云表示实现了**3.5% sim-to-real gap**，并具备更强的跨传感器泛化；但给定摘录中未展开更细的实验表格与对比细节。
- 数据规模方面，Contact3D覆盖**136 objects**、**100k samples**，相较表中TCL3D的**117 objects / 50k**、TacQuad的**124 objects / 72k**更大更全。
- 回归表摘录显示，FG-CLTP比较的基线包括**TVL、AnyTouch、UniTouch、CLTP**；完整FG-CLTP逐项数值在提供文本中被截断，但作者明确宣称其整体最优。
- 下游操作实验部分，作者声称在**contact-rich manipulation tasks**上显著优于强基线，但当前提供内容未包含具体成功率数字、任务名和统计显著性数值。

## Link
- [http://arxiv.org/abs/2603.10871v1](http://arxiv.org/abs/2603.10871v1)
