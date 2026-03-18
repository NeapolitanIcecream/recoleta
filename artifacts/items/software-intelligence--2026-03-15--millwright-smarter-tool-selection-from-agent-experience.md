---
source: hn
url: https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/
published_at: '2026-03-15T22:50:17'
authors:
- dnautics
topics:
- tool-selection
- agent-experience
- tool-augmented-llm
- retrieval-ranking
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
---

# Millwright: Smarter Tool Selection from Agent Experience

## Summary
Millwright 是一种面向 AI 代理的大规模工具选择方案，用“语义相关性 + 历史使用反馈”来缩小工具候选集，并随着代理经验持续改进排序。它还把工具选择过程变成可观测的数据资产，用于发现坏工具、冷启动补种和新工具机会。

## Problem
- 代理面对数百到数千个工具时，把所有工具定义都塞进上下文会挤占 RAG、规划和对话历史空间，因此需要更高效的工具路由。
- 仅靠语义匹配无法反映工具在真实任务中的实际效果，不能在线适应“描述看起来对、实际却不好用/坏掉”的工具。
- 理想系统既要能按需返回少量高相关工具，也要支持失败后的更全面搜索，并能从使用反馈中持续学习。

## Approach
- 维护一个 `toolshed` 索引，只暴露两个接口：`suggest_tools` 用于开启会话并返回排序后的候选工具，`review_tools` 用于在任务结束后写回反馈。
- `suggest_tools` 先把任务拆成原子子需求，再对查询做向量化；一方面用查询向量和工具描述做余弦相似度得到语义推荐，另一方面从历史评论索引中找相似查询，按“工具在类似任务上的聚合适配度”做历史推荐。
- 将语义推荐与历史推荐合并去重，并加入“None of these are correct”或“Create a custom tool”；还可随机注入少量工具进行探索，类似 epsilon-greedy 多臂老虎机。
- `review_tools` 记录 `<tool, embedded query, reported fitness>` 的追加日志，反馈粒度是“工具 × 查询”而非全局分数，避免工具在不适用任务上被错误惩罚。
- 系统周期性地把评论日志压缩成 `<embedded query, tool, aggregate fitness>` 索引，可通过按工具聚类（如 k-means 思路）合并近邻查询，控制索引规模并支持影子测试与回滚。

## Results
- 文中**没有提供实验数据或标准基准上的定量结果**，没有报告准确率、成功率、延迟、成本或与 Toolshed/纯语义检索/Top-N 策略的数值对比。
- 明确的能力主张是：在 **128K 到 1M+** 上下文窗口仍有限的前提下，Millwright 通过只展示更少且更相关的工具，减少工具目录对上下文的占用。
- 相比仅做 RAG for tools 的方案，作者声称其新增了“经验驱动的动态重排序”，可根据代理给出的 **4 类反馈**（`perfect`、`related`、`unrelated`、`broken`）持续更新工具适配度。
- 系统声称支持大规模目录场景，从“**数百或数千**工具”中逐步学会更好的路由，并在候选用尽时触发“创建新工具”的工作流。
- 在实现层面，作者给出可落地组件而非性能数字：嵌入模型示例包括 **all-MiniLM-L6-v2（22M 参数、384 维）**、e5、`text-embedding-3-small`；存储可用 **SQLite/pg_vector**，更大规模可用 **Pinecone/Clickhouse**。
- 额外主张是可观测性收益：通过带时间戳的 review log，可以发现工具版本发布后的效果变化、查询分布漂移，以及 `broken` 反馈激增等问题，但文中未给出具体案例数字。

## Link
- [https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/](https://minor.gripe/posts/2026-03-13-millwright_smarter_tool_selection_with_adaptive_toolsheds/)
