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
- information-retrieval
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Enhancing Requirements Traceability Link Recovery: A Novel Approach with T-SimCSE

## Summary
本文提出 T-SimCSE，用于在缺少标注数据的情况下恢复软件需求与自然语言工件之间的可追踪链接。核心思想是先用 SimCSE 做语义匹配，再用“specificity（特异性）”对候选工件重排序，以减少泛化语义带来的误连。

## Problem
- 该论文解决**需求可追踪链接恢复**问题：自动找出需求与用例、设计文档、测试用例等自然语言工件之间的关联。
- 这很重要，因为可追踪性直接影响软件质量、需求变更分析、调试、合规和维护效率，但人工建链成本高、易出错、难扩展。
- 现有方法要么依赖词面匹配导致语义错配，要么依赖大量标注数据训练深度模型，而现实中标注数据非常少。

## Approach
- 先使用**预训练的 SimCSE**句向量模型，把需求和目标工件编码成向量，并用**余弦相似度**得到初始排序；作者明确说明**不做额外训练或微调**。
- 定义高概率目标工件（HPTA）：对每个需求，先取与其最相似的一批候选工件。
- 对每个 HPTA，再找与它相似的其他目标工件（TRTA），把这些“与正确候选相近”的工件视为可能的间接相关项，并给予奖励提升排名。
- 引入新指标**specificity**：如果某个目标工件与很多其他工件都相似，说明它更“泛”，specificity 低；如果只和少数工件相似，则更“专”，specificity 高。
- 最终通过**相似度 + 基于 specificity 的差异化奖励/降权**重新排序：更具体的工件得到更高奖励，语义过于通用的工件被适当降权，然后取 top-K 建立 trace links。

## Results
- 论文称在**10个公开数据集**上评估了 T-SimCSE，并与其他方法进行了比较。
- 作者声称：T-SimCSE 在**10个数据集上的 MAP（Mean Average Precision）优于基线**。
- 作者还声称：在**MODIS 数据集**上，T-SimCSE 在**F1 和 F2**指标上优于已有方法。
- 摘要中还特别指出，T-SimCSE 在**recall 和 MAP**方面表现更好。
- 但在给定摘录中，**没有提供具体数值**（如 MAP/F1/F2 的绝对值、提升幅度、具体基线名称或显著性检验），因此无法精确报告数值级突破，只能确认其最强具体主张是“跨 10 个公开数据集优于对比方法，尤其在 MAP、recall，以及 MODIS 上的 F1/F2 更好”。

## Link
- [http://arxiv.org/abs/2603.11800v1](http://arxiv.org/abs/2603.11800v1)
