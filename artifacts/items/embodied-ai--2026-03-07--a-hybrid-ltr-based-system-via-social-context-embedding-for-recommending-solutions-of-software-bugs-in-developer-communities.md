---
source: arxiv
url: http://arxiv.org/abs/2603.07229v1
published_at: '2026-03-07T14:24:25'
authors:
- Fouzi Harrag
- Mokdad Khemliche
topics:
- learning-to-rank
- bug-solution-recommendation
- stack-overflow-mining
- social-context-embedding
- developer-community
relevance_score: 0.01
run_id: materialize-outputs
---

# A Hybrid LTR-based System via Social Context Embedding for Recommending Solutions of Software Bugs in Developer Communities

## Summary
本文提出一个面向开发者社区的 Stack Overflow 缺陷解决方案推荐系统，用学习排序结合文本内容与社交上下文特征来重排候选答案。其目标是让开发者更快找到更相关的 bug 修复建议，而不必手工筛查大量帖子。

## Problem
- 开发者在 Stack Overflow 上查找软件错误/缺陷解决方案时，候选问答很多，人工检索耗时且常找不到最佳答案。
- 仅靠关键词搜索或基础相似度排序，难以充分利用帖子质量、用户互动和社区信号。
- 这很重要，因为 Stack Overflow 积累了大量众包软件工程知识，若不能高效挖掘，其实际调试价值会被浪费。

## Approach
- 将 bug report 预处理后作为查询，先用 **TF-IDF** 从 Stack Overflow 问题库中召回一批最相关问题/答案作为候选。
- 构建一个 **Learning-to-Rank (LTR)** 重排模型，融合四类特征：统计特征、文本特征、上下文/社交特征、流行度特征。
- 文本侧对标题、正文与代码片段做清洗、分词、停用词移除和词干提取，并提取长度、可读性、情感、代码比例、标题-正文相似度等特征。
- 社交与元数据侧使用帖子分数、评论、浏览、收藏、用户信息等 Stack Overflow 社区信号；答案得分被离散成 1-5 级相关性标签用于训练。
- 使用 TensorFlow Ranking 风格的深度学习排序框架，并比较不同 LTR 训练方式与两种基线变体。

## Results
- 论文称在 **29,395** 个来自 Stack Overflow 的查询与答案样本上评估了所提系统及 **2** 个基线变体。
- 最明确的主结果是：在为每个问题推荐 **Top-10** 答案时，系统可达到接近 **78%** 的“correct solutions”。
- 作者还声称所提系统 **优于两种基线**，并在面向 bug 解决方案推荐这一任务上优于 **Google 搜索** 与 **Stack Overflow 自带搜索**。
- 文本摘录中**未提供**更细的核心量化指标，如 NDCG/MAP/MRR/Precision@k 的具体数值，也未给出基线的精确分数差距。

## Link
- [http://arxiv.org/abs/2603.07229v1](http://arxiv.org/abs/2603.07229v1)
