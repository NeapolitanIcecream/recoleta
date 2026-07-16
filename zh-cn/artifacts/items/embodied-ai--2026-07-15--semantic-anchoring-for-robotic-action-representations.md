---
source: arxiv
url: https://arxiv.org/abs/2607.13597v1
published_at: '2026-07-15T08:45:15'
authors:
- Yuan Xu
- Youheng Shi
- Chengyang Li
- Wentao Zhu
- Yizhou Wang
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- sim2real
- representation-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Semantic Anchoring for Robotic Action Representations

## Summary
## 摘要
《Semantic Anchoring for Robotic Action Representations》表明，仅使用动作监督进行微调会侵蚀 VLA 模型继承的语义结构，而这种侵蚀程度与分布外性能的变化相一致。该方法在训练阶段进行语义锚定，在不改变部署时推理模型的情况下，提高了仿真环境和真实机器人上的成功率。

## 问题
- VLA 模型继承了预训练视觉—语言编码器中的语义表示，但有限且狭窄的机器人示范数据可能会使动作表示转向特定任务的捷径。
- 这一点很重要，因为语义退化与向新指令、物体、布局、视觉条件和任务组合迁移能力减弱有关，即使分布内成功率仍在上升。

## 方法
- 在 \(\pi_0\) 的完整微调过程中，将中间层动作特征与指令嵌入进行对比，使用双向对比检索和任务不相交的 LIBERO 评估。
- 添加训练阶段的对比对齐损失，将动作表示锚定到 EgoHOD 文本编码器提供的冻结语义流形上。
- 将动作特征分解为共享语义通道和执行特定的私有通道；仅对齐共享通道，同时重建原始特征并使两个通道去相关。
- 在推理时丢弃所有辅助对齐、分解和重建模块，因此部署的策略与仅使用动作监督的基线具有相同的推理图。

## 结果
- 在 LIBERO 上，\(\pi_0\) 的平均成功率从 89.3% 提高到 92.4%，增加 3.1 个百分点；各套件得分分别为：Spatial 从 94.0% 提高到 96.5%，Object 从 96.5% 提高到 98.5%，Goal 从 90.0% 提高到 92.5%，Long 从 76.5% 提高到 82.0%。
- 在 SimplerEnv 上，该方法将 \(\pi_0\) 的成功率从 35.4% 提高到 41.7%（增加 6.3 个百分点），将 SpatialVLA 的成功率从 43.8% 提高到 51.0%（增加 7.2 个百分点）。
- 在真实双臂机器人上，平均分布内成功率从 51.3% 上升到 70.0%（增加 18.7 个百分点），分布外成功率从 49.5% 上升到 71.0%（增加 21.5 个百分点）；每种任务条件进行了 20 次试验。
- 真实机器人在五个分布外维度上均取得提升：语言从 75.0% 提高到 85.0%，位置从 32.5% 提高到 57.5%，物体从 52.5% 提高到 77.5%，视觉从 57.5% 提高到 75.0%，任务组合从 30.0% 提高到 60.0%。
- 在 \(\pi_0\) 微调期间，动作—指令对齐度始终未恢复到预训练水平 62.74%；分布外成功率则随对齐度趋势变化，Spearman \(\rho=0.964\)。成功的单次运行轨迹也显示出高于失败轨迹的对齐度。
- 摘录报告的消融实验显示，对比对齐以及共享/私有通道分解会带来逐步提升，其中网络中间层 \(k=10\) 的收益最明显；但摘录未提供消融实验柱状图的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13597v1](https://arxiv.org/abs/2607.13597v1)
