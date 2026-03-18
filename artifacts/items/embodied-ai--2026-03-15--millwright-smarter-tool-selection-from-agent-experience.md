---
source: hn
url: https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/
published_at: '2026-03-15T22:50:17'
authors:
- dnautics
topics:
- tool-selection
- agent-experience
- rag-tools
- adaptive-ranking
- vector-retrieval
relevance_score: 0.18
run_id: materialize-outputs
---

# Millwright: Smarter Tool Selection from Agent Experience

## Summary
Millwright提出了一种面向大规模工具目录的自适应选工具机制：先用语义检索缩小候选集，再用代理历史使用反馈重排。它的核心价值是让智能体在有限上下文内更快看到更合适的工具，并随着经验持续改进。

## Problem
- 大模型可用上下文有限；当工具数量达到数百到数千时，把大量工具定义直接塞进上下文会挤占RAG、规划和对话历史空间。
- 仅靠语义匹配无法反映工具在真实执行中的“是否好用”；同样语义相关的工具，实际成功率、稳定性和适配性可能差很多。
- 现有RAG式工具选择可做相关性检索，但缺少在线经验反馈闭环，无法根据代理实际使用结果持续更新工具优先级。

## Approach
- 维护一个“toolshed”索引，只暴露两个接口：`suggest_tools` 用于按任务查询返回排序后的候选工具，`review_tools` 用于在任务结束后写回工具反馈。
- 对任务查询先做子任务分解，再把子查询嵌入成向量；一条排序信号来自“查询向量 vs 工具描述向量”的余弦相似度，即语义相关性。
- 另一条排序信号来自历史经验：保存 `<tool, embedded query, reported fitness>` 的评论日志，并基于与当前查询相近的历史查询，按“相似度加权的聚合fitness”对工具做历史重排。
- 将语义排序与历史排序合并去重；保留“None of these are correct”用于继续探索，并可随机注入少量候选，类似 epsilon-greedy，以避免只利用不探索。
- 反馈按查询-工具对建模，而不是全局工具分数；后续通过聚类/压缩把相近查询合并成质心，形成更紧凑的历史索引，同时支持监控工具退化、任务分布变化和潜在新工具机会。

## Results
- 文本未提供标准基准、数据集或定量实验结果，因此没有可核验的准确率、成功率、延迟或成本数字。
- 论文/文章的最强主张是：在“数百到数千工具”的大目录下，Millwright能用可调上下文预算只呈现更少且更相关的工具，同时保留失败后的穷举/分页探索能力。
- 它声称相较仅做语义RAG或静态工具库，新增了基于代理使用反馈的在线学习闭环，使工具排序能“随时间变好”，并且分数是“按查询条件化”的，而非粗糙的全局评分。
- 它还声称能支持发现新工具机会：当现有工具不足时可触发“Create a custom tool”，并利用评论日志/索引进行观测，如检测“broken”评价激增来发现工具失效。

## Link
- [https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/](https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/)
