---
source: arxiv
url: http://arxiv.org/abs/2603.11800v1
published_at: '2026-03-12T11:02:03'
authors:
- Ye Wang
- Wenqing Wang
- Kun Hu
- Qiao Huang
- Liping Zhao
topics:
- requirements-traceability
- trace-link-recovery
- simcse
- pretrained-language-models
- software-engineering
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# Enhancing Requirements Traceability Link Recovery: A Novel Approach with T-SimCSE

## Summary
本文提出 T-SimCSE，用于在标注数据稀缺的情况下恢复需求与自然语言软件工件之间的可追踪链接。其核心是在 SimCSE 语义相似度基础上，再利用“specificity”对候选工件重排序，以提升检索质量。

## Problem
- 要解决的是**需求追踪链接恢复**：自动找出需求与用例、设计文档、测试等工件之间的正确关联。
- 这很重要，因为追踪链接直接影响软件质量、变更影响分析、调试、合规与维护效率。
- 现有 IR 方法常因词汇不匹配而不准，监督式深度学习方法又通常需要大量标注数据，而现实中这类数据非常少。

## Approach
- 使用**预训练的 SimCSE**句向量模型，直接计算需求（source artifact）与目标工件（target artifact）之间的语义相似度，无需在追踪数据集上额外训练或微调。
- 先按需求-目标工件相似度得到候选排序列表，再计算目标工件之间的相互相似度，寻找与高概率候选相近的其他工件。
- 引入**specificity**指标：一个目标工件如果与很多其他工件都很像，则它更“泛化”、specificity 更低；若只与少数工件相近，则 specificity 更高。
- 基于 specificity 设计**rewarding / reranking**机制：更具体的工件获得更高奖励并上升排名；语义过于通用、容易和很多工件都相似的候选会被适当降权。
- 最终将追踪链接建立在重排序后的 **top-K** 目标工件上，从而兼顾直接语义匹配与间接关联线索。

## Results
- 论文称在**10 个公开数据集**上评估了 T-SimCSE，并与其他方法进行了比较。
- 摘要明确声称：T-SimCSE 在**Recall** 和 **MAP** 上表现更优。
- 引言贡献部分进一步声称：T-SimCSE 在 **MODIS** 数据集上的 **F1** 和 **F2** 分数优于已有方法。
- 论文还声称其在**10 个数据集上的 MAP** 均优于基线方法。
- 但在给定摘录中**没有提供具体数值**（如 Recall/MAP/F1/F2 的绝对值、提升幅度、基线名称对应数字），因此无法精确列出定量增益。

## Link
- [http://arxiv.org/abs/2603.11800v1](http://arxiv.org/abs/2603.11800v1)
