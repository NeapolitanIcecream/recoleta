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
- software-engineering
relevance_score: 0.02
run_id: materialize-outputs
---

# On the Effectiveness of Code Representation in Deep Learning-Based Automated Patch Correctness Assessment

## Summary
本文系统评估了在自动补丁正确性评估（APCA）中，不同代码表示方式对判断补丁是否真正正确的影响。核心发现是：图表示，尤其是代码属性图（CPG），整体上最有效，并且适当的表示融合还能进一步提升效果。

## Problem
- 该工作要解决的问题是：自动程序修复（APR）生成的“看似通过测试”的补丁里，很多其实是**过拟合补丁**，并不真正正确。
- 这很重要，因为弱测试集无法可靠区分真实修复与错误修复，开发者还需要花大量时间手动筛掉错误补丁，削弱 APR 的实用性。
- 虽然已有深度学习 APCA 方法会把代码编码成特征再做二分类，但**哪种代码表示最好、图表示是否更强、不同表示能否融合**，此前缺少系统研究。

## Approach
- 作者构建了一个大规模实验框架，基于 **2,274 个带标签的 plausible patches**，这些补丁来自真实 **Defects4J** 缺陷，由 **30+** 修复工具生成。
- 系统比较 **15 种代码表示**、分属四类：启发式表示、序列表示、树表示、图表示；并搭配 **11 个分类器/神经模型**，总计覆盖 **20 个表示-分类器场景** 和 **500+ 训练模型**。
- 最简单地说，方法就是：把 buggy/patched 代码片段分别变成不同形式的“机器可读表示”（如 TF-IDF、子词序列、AST、CFG/CDG/DDG/PDG/CPG），再训练分类器预测补丁是正确还是过拟合。
- 他们还专门研究了**表示融合**：测试 **22 个融合场景**、**11 种组合表示** 和两类融合策略（intermediate/backend fusion），看两种或多种表示一起用是否更强。
- 对表现最好的图表示，作者进一步分析节点嵌入，发现**节点文本信息比节点类型信息更关键**，因为前者承载了更丰富的补丁语义。

## Results
- 在四类表示中，**图表示最好**；各类别最佳模型的准确率分别为：**XGBoost+TF-IDF 80.41%**、**Transformer+sequence 82.48%**、**TreeLSTM+AST 82.94%**、**GGNN+CPG 83.73%**。
- 从整体平均表现看，四类表示在所有考察指标上的平均成绩分别为 **80.55%（启发式）**、**82.90%（序列）**、**83.03%（树）**、**83.81%（图）**，说明图表示整体最稳健。
- 摘要中还给出：**CPG** 在三种 GNN 上的平均准确率达到 **82.69%**，表明图结构表示不仅在单一模型上强，在不同 GNN 上也较一致。
- 与已有 APCA 方法相比，**CPG+GGNN** 相对 **Tian et al. 的 BERT+SVM**，在 **accuracy / recall / F1** 上分别提升 **9.34% / 14.96% / 8.83%**。
- 作者声称某些表示已达到或超过先前方法；例如，**TreeLSTM+AST** 可过滤掉 **87.09%** 的过拟合补丁。
- 表示融合方面，**将序列表示融入启发式表示** 可在五项指标上带来平均 **13.58%** 提升；但加入第三种表示可能变差，例如把树表示再加入“启发式+序列”后，平均反而**下降 3.34%**。

## Link
- [http://arxiv.org/abs/2603.07520v1](http://arxiv.org/abs/2603.07520v1)
