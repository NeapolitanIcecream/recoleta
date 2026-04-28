---
source: arxiv
url: http://arxiv.org/abs/2604.16067v1
published_at: '2026-04-17T13:49:57'
authors:
- Guransh Singh
topics:
- vision-language-action
- catastrophic-forgetting
- gradient-projection
- robot-fine-tuning
- knowledge-preservation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# AEGIS: Anchor-Enforced Gradient Isolation for Knowledge-Preserving Vision-Language-Action Fine-Tuning

## Summary
## 摘要
AEGIS 是一种用于视觉-语言-动作模型的微调方法。它在允许连续动作梯度更新主干网络的同时，保留预训练视觉-语言模型的视觉推理能力。它的做法是逐层检测动作训练梯度是否会把模型推离其预训练激活模式，并只去除其中冲突的分量。

## 问题
- 视觉-语言模型的预训练使用的是分布在许多语义方向上的交叉熵梯度，而机器人动作微调会注入幅值很高、集中在狭窄控制子空间中的 MSE 梯度。
- 这种不匹配会导致灾难性遗忘：论文称，朴素的直接 MSE 微调会在 **1,500 个训练步**内使 VQA 留出集损失持续恶化。
- 现有防御方法都有明确代价：**stop-gradient** 通过阻断动作梯度来保住 VQA，**LoRA** 只能减缓而不能阻止 VQA 能力下降，而混合批次的 VQA 联合训练在机器人训练期间可能要使用多达 **50%** 的 VQA 数据，增加计算和数据开销。

## 方法
- AEGIS 先在全部 **26 个 transformer 层**上，通过带掩码的 VQA 前向计算预先构建一个静态激活锚点，并存储每层高斯分布的均值和方差统计量。
- 在机器人微调期间，它用每层的 **Wasserstein-2** 距离来度量当前层激活相对该锚点的漂移，具体依据是均值偏移和标准差不匹配。
- 它在同一计算图上执行两次反向传播：一次针对动作损失，一次针对锚点恢复目标，从而得到任务梯度和锚点梯度。
- 对每个 transformer 层，它会检查动作梯度是否与锚点恢复方向冲突。如果点积为负，就用一次 Gram-Schmidt 步骤投影掉冲突分量；如果不是负值，就保持梯度不变。
- 这种方法只改动反向传播。论文称，前向过程、模型架构和任务损失都不变，训练也不需要 replay buffer、不需要联合训练批次，也不需要离散动作 token。

## 结果
- 论文称，朴素的直接 MSE 微调会在 **1,500 步**内导致 VQA 留出集损失出现**明显且持续**的上升。
- 文中说，stop-gradient 这个基线能让 VQA 损失保持**大致稳定**，但它会阻断来自动作专家的连续监督。
- LoRA 基线在 LLM 层上使用 **rank 16** 和 **alpha 32**，VQA 损失仍然呈现**持续上升**，只是比朴素微调更慢。
- AEGIS 使用 **3,000 个 VQAv2 样本**，在**单张 GPU 上约 5 分钟**内完成锚点构建。
- 根据摘要，这种投影平均移除的梯度能量不到 **1%**。
- 该摘录**没有提供完整的基准表或最终机器人任务成功率**，因此这里没有关于操作性能、全数据集 VQA 分数，或除上述具体说法之外其他基线的定量比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16067v1](http://arxiv.org/abs/2604.16067v1)
