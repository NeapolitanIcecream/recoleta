---
source: arxiv
url: http://arxiv.org/abs/2603.07520v1
published_at: '2026-03-08T08:18:42'
authors:
- Quanjun Zhang
- Chunrong Fang
- Haichuan Hu
- Yuan Zhao
- Weisong Sun
- Yun Yang
- Tao Zheng
- Zhenyu Chen
topics:
- automated-program-repair
- patch-correctness-assessment
- code-representation
- graph-neural-networks
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
---

# On the Effectiveness of Code Representation in Deep Learning-Based Automated Patch Correctness Assessment

## Summary
本文系统评估了深度学习式自动补丁正确性评估（APCA）中不同代码表示的效果，核心发现是图表示，尤其是 CPG，在补丁是否过拟合的判断上最稳定、总体最好。研究还表明，适当融合两类表示可以进一步提升效果，但融合过多表示并不一定有效。

## Problem
- 要解决的问题是：**如何更准确地判断 APR 生成的“看似通过测试”的补丁是否真的正确，而不是测试集过拟合的错误补丁**。
- 这很重要，因为 APR 长期受补丁过拟合困扰；论文引用背景指出开发者通常约 **50%** 的时间花在调试和修复上，而错误的 plausible patches 会增加人工筛查成本、降低 APR 的实际可用性。
- 虽然已有学习式 APCA 方法，但**代码表示**这一最基础环节缺乏系统比较，社区并不清楚 heuristic / sequence / tree / graph 各自的优劣及是否适合融合。

## Approach
- 作者构建并使用一个大规模补丁基准：来自 **Defects4J** 的 **2,274** 个带标签 plausible patches，由 **30+** 个修复工具生成，用于统一评测 APCA。
- 系统比较 **4 类、15 种代码表示**：heuristic-based、sequence-based、tree-based、graph-based；并配套评估 **11** 个分类模型，总计训练 **500+** 个 APCA 模型。
- 最简单地说，方法就是：把“buggy 代码 + patched 代码”转换成不同形式的表示（手工特征、token 序列、AST、程序图），再训练二分类器判断该补丁是正确还是过拟合。
- 图表示部分覆盖 **CFG/CDG/DDG/PDG/CPG**，并用 GNN（如 GCN/GAT/GGNN）学习补丁语义；作者还分析了图节点嵌入中“文本信息 vs. 类型信息”的作用。
- 进一步做表示融合实验，考察两类或多类表示组合后，是否能比单一表示更好地预测补丁正确性。

## Results
- 在 RQ1 中，四类表示里**图表示最好**。各类别最佳组合的准确率分别为：**XGBoost+TF-IDF 80.41%**、**Transformer+sequence 82.48%**、**TreeLSTM+AST 82.94%**、**GGNN+CPG 83.73%**。
- 摘要给出的图表示总体结果显示：**CPG** 在三个 GNN 模型上的**平均准确率为 82.69%**，说明这种此前较少被系统研究的表示最稳定。
- 在与已有 SOTA APCA 方法比较时，四类表示的平均综合表现分别为 **80.55% / 82.90% / 83.03% / 83.81%**（对应 heuristic / sequence / tree / graph）。其中 **CPG+GGNN** 相比 **Tian et al. 的 BERT+SVM**，在 **accuracy / recall / F1** 上分别提升 **9.34% / 14.96% / 8.83%**。
- 论文声称其方法能够达到或超过已有 APCA：例如 **TreeLSTM+AST** 可过滤掉 **87.09%** 的过拟合补丁。
- 表示融合方面，**把 sequence-based 表示融入 heuristic-based 表示**，在 **5 个指标** 上可带来**平均 13.58%** 的提升，是最明显的增益之一。
- 但融合并非越多越好：将 **tree-based** 再加入已有的 **heuristic+sequence** 组合，反而带来 **平均 3.34%** 的下降，说明多表示融合仍有明显局限与研究空间。

## Link
- [http://arxiv.org/abs/2603.07520v1](http://arxiv.org/abs/2603.07520v1)
