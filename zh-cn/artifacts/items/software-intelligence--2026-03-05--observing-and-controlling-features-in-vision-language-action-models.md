---
source: arxiv
url: http://arxiv.org/abs/2603.05487v1
published_at: '2026-03-05T18:53:50'
authors:
- Hugo Buurmeijer
- Carmen Amo Alonso
- Aiden Swann
- Marco Pavone
topics:
- vision-language-action
- activation-steering
- mechanistic-interpretability
- robot-control
- linear-probes
relevance_score: 0.3
run_id: materialize-outputs
language_code: zh-CN
---

# Observing and Controlling Features in Vision-Language-Action Models

## Summary
本文研究如何直接观察并控制视觉-语言-动作模型（VLA）的内部表征，从而在不微调模型的情况下实时引导机器人行为。核心思想是把LLM中的激活可解释与激活操控方法迁移到VLA，并形式化为“特征可观测性”和“特征可控性”。

## Problem
- VLA虽然能力强，但其行为常常不可预测、难以实时纠正，也可能偏离用户偏好或安全要求，这对真实机器人部署很关键。
- 现有LLM激活操控方法不能直接套用到VLA，因为VLA有多模态输入、连续动作输出，以及闭环控制特性。
- 需要一种**既能精确操控行为、又尽量保持原始自然闭环行为**的方法，而不是依赖昂贵的微调或重训练。

## Approach
- 提出两个形式化概念：**feature-observability**（某层隐藏状态里能否读出行为相关特征）和 **feature-controllability**（能否通过修改该层隐藏状态把特征推到目标区间）。
- 用**线性观察器**从Transformer某层激活中读取机器人状态或动作特征，即训练一个线性 probe / classifier / regressor 来预测这些特征。
- 用**最小范数线性干预**控制内部表征：如果观察到的特征超出目标范围，就沿着线性探针权重方向施加闭式求解的最小加性扰动。
- 该控制器可在推理时在线运行，直接插入VLA的Transformer层中，计算开销很小，不需要微调或重训练。
- 方法在两类VLA架构上验证：纯Transformer型 OpenVLA，以及Transformer + flow-matching混合型 $\pi_{0.5}$。

## Results
- 论文声称在 **$\pi_{0.5}$（Libero 数据集）** 和 **OpenVLA（BridgeData V2 数据集）** 上，机器人**状态与动作特征可以被线性探针从内部表示中读出**，说明VLA内部存在可解释结构。
- 作者进一步声称这些线性观察结果对小扰动具有**鲁棒性**，并据此支持在线控制；但给定摘录中**没有提供明确的数值表格或完整指标**（如具体 MAE、R²、准确率数值）。
- 控制方面，论文声称**轻量级、定向的线性干预能够可靠地引导机器人行为，同时保持闭环能力**，并可实现**无需微调的在线适配**以满足用户偏好和任务约束。
- 摘录中提到图3展示了与基线比较的 **MAE** 和 **accuracy**，图4展示了对 $\pi_{0.5}$ 不同层施加干预后对 **delta yaw action** 的平均变化；但**具体数字在提供文本中未给出**。
- 相比作者引用的相关工作，本文最强的具体主张是：该方法可在**不同VLA架构**上实现**实时行为转向（real-time policy steering）**、**保留自然行为**、并支持**闭环在线对齐**，且**无需fine-tuning**。

## Link
- [http://arxiv.org/abs/2603.05487v1](http://arxiv.org/abs/2603.05487v1)
