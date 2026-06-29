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
AEGIS 是一种用于视觉-语言-动作模型的微调方法。它在让连续动作梯度更新骨干网络的同时，保留了预训练视觉-语言模型的视觉推理能力。它通过逐层检测动作训练梯度何时会把模型推离预训练的激活模式，并只去掉那一部分冲突分量来实现这一点。

## Problem
- 视觉-语言模型的预训练使用的是分布在许多语义方向上的交叉熵梯度，而机器人动作微调会注入集中在狭窄控制子空间里的高幅值 MSE 梯度。
- 这种不匹配会导致灾难性遗忘：论文报告称，直接进行朴素的 MSE 微调会让 VQA 留出集损失在 **1,500** 个训练步内持续恶化。
- 现有防御有明确代价：**stop-gradient** 通过阻断动作梯度来保留 VQA，**LoRA** 会放慢但不会阻止 VQA 退化，而混合批次的 VQA 共训练在机器人训练期间最多会使用 **50%** 的 VQA 数据，增加计算和数据开销。

## Approach
- AEGIS 先基于跨所有 **26** 个 Transformer 层的 masked VQA 前向传播，预先计算一个静态激活锚点，并保存每层的高斯均值和方差统计量。
- 在机器人微调期间，它使用每层的 **Wasserstein-2** 距离，结合均值偏移和标准差不匹配，衡量当前层激活与该锚点的漂移程度。
- 它在同一计算图上运行两次反向传播：一次对应动作损失，另一次对应锚点恢复目标，得到任务梯度和锚点梯度。
- 对每个 Transformer 层，它检查动作梯度是否与锚点恢复方向冲突。如果点积为负，就用 Gram-Schmidt 步骤去掉冲突分量；如果不冲突，就保持梯度不变。
- 这个方法只改反向传播。论文说前向传播、架构和任务损失都不变，训练也不需要 replay buffer、共训练批次或离散动作 token。

## Results
- 论文声称，朴素的直接 MSE 微调会在 **1,500** 步内让 VQA 留出集损失出现 **明显且持续** 的上升。
- 文中的 stop-gradient 基线让 VQA 损失 **大致保持不变**，但会阻断来自动作专家的连续监督。
- LoRA 基线在 LLM 层上使用 **rank 16** 和 **alpha 32**，VQA 损失仍然会 **持续上升**，只是比朴素微调慢。
- AEGIS 用 **3,000 个 VQAv2 样本**，在 **单个 GPU** 上大约 **5 分钟** 就能构建锚点。
- 摘要说，这个投影平均去掉的梯度能量不到 **1%**。
- 这段摘录**没有给出完整的基准表或端任务机器人成功率**，因此这里没有关于操作性能、全数据集 VQA 分数，或除上述具体结论之外的基线对比的定量结果。

## Link
- [http://arxiv.org/abs/2604.16067v1](http://arxiv.org/abs/2604.16067v1)
