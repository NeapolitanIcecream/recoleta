---
source: arxiv
url: http://arxiv.org/abs/2603.07229v1
published_at: '2026-03-07T14:24:25'
authors:
- Fouzi Harrag
- Mokdad Khemliche
topics:
- learning-to-rank
- stack-overflow-mining
- bug-solution-recommendation
- social-context-embedding
- software-repository-mining
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# A Hybrid LTR-based System via Social Context Embedding for Recommending Solutions of Software Bugs in Developer Communities

## Summary
本文提出一个面向软件缺陷求解的 Stack Overflow 答案推荐系统，把文本内容与社区社交上下文一起送入学习排序模型，为开发者返回更相关的 Top-k 解决方案。核心目标是减少开发者在海量问答中手工搜索的时间，并提升找到可用修复建议的成功率。

## Problem
- 开发者在 Stack Overflow 中查找 bug 解决方案时，候选答案很多，手工筛选耗时且未必能找到最佳答案。
- 仅靠关键词匹配或普通搜索，往往难以同时利用问题文本、答案质量、用户互动和帖子流行度等信号。
- 这很重要，因为 Stack Overflow 是软件调试与维护中的高价值众包知识库，若无法高效检索，会直接影响修复效率与开发体验。

## Approach
- 把 bug report 视为查询：先对 bug 标题、描述、复现步骤做清洗、分词、去停用词、词干化，再用 TF-IDF 从 Stack Overflow 问题库中召回相关候选。
- 对问答对提取四类特征并统一建模：**statistical**、**textual**、**context**、**popularity**；其中还纳入社交上下文，如评论、用户信息、投票等社区信号。
- 使用深度学习的 Learning-to-Rank 框架对候选答案重新排序，比较 point-wise、pair-wise、list-wise 等排序学习设置。
- 用答案投票分数作为相关性标签，并将每个问题下的答案按分数划分为 5 档相关性等级，作为训练监督信号。
- 系统实现上解析 2019-03-04 的 Stack Overflow 数据转储，重点使用 Posts、Comments、Users 三类数据，并构建原型系统用于实时推荐。

## Results
- 论文声称：在“为每个问题推荐前 10 个答案”时，系统可达到**接近 78% 的 correct solutions**。
- 评估基准包含 **29,395** 个从 Stack Overflow 提取的查询与答案；作者称所提方法优于**两个基线变体**，但摘录中**未给出更细的数值指标**（如 MAP、MRR、NDCG 或显著性检验）。
- 作者还报告了一个**小规模用户研究**，由 **2 名评估者** 将系统结果与 **Google search** 和 **Stack Overflow search** 比较；结论是该系统在 bug solution recommendation 任务上表现更好。
- 除“Top-10 接近 78%”外，摘录中没有提供与基线的具体数值差距，因此无法精确量化提升幅度。

## Link
- [http://arxiv.org/abs/2603.07229v1](http://arxiv.org/abs/2603.07229v1)
