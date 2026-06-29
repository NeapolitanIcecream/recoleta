---
source: hn
url: https://github.com/mirkofr/FERNme
published_at: '2026-06-20T23:34:03'
authors:
- mirkofr
topics:
- agent-memory
- user-owned-data
- hebbian-learning
- human-ai-interaction
- action-based-personalization
- ai-agents
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: FERNme – agent memory that updates with ~zero LLM calls

## Summary
## 摘要
FERNme 是一个由用户拥有的 AI 代理记忆层，能在很少使用或不使用 LLM 的情况下更新用户偏好图。最有力的证据来自合成数据或 LLM 编写的数据，因此该主张支持的是一个经过测试的机制，尚未证明其在真实用户中的表现。

## 问题
- 许多代理记忆系统在每一轮都用 LLM 写入记忆，这会提高成本，也可能引入提取错误。
- 该项目面向行动驱动型代理，例如购物、支持、预订、辅导、医疗和政府网站。在这些场景中，记忆应改进结果，而不是回答记忆问题。
- 它也处理用户控制问题：用户可以查看、编辑、导出和删除系统记住的内容。

## 方法
- 每个用户都有一个稀疏的站点级图，其中用 0-9 的加权边连接用户、偏好、主题、目标和上下文。
- 新事件用 Hebbian 共现规则更新图：相关属性会在有用行为后增强，在不良结果后减弱，并随时间衰减。
- 检索在图上使用扩散激活，然后为代理提示生成一张约 25 个 token 的有界记忆卡片。
- 群体先验有助于冷启动，存储的卡片保留相对该先验的偏差，而不是重复常见偏好。
- LLM 的使用是可选的：热写入路径使用确定性映射，只有在确定性映射无法处理新的自由文本时，才会运行受控的 LLM 标注。

## 结果
- 该仓库报告了 88 项测试，覆盖引擎、SQLite 和 Postgres 存储、supernode 和登录、触发器、安全性、REST 和 MCP 接口、UI 视图以及评估脚本。
- 在冷启动消融中，群体先验在第 1-3 轮为 precision@5 增加 +0.06，到第 10 轮时影响消退。
- 在合成的模拟店铺试点中，FERNme 报告相对于流行度基线的相对转化提升为 +16%；它在第 1 次访问时持平，并随着用户行为累积而改进。
- 在成本和质量的 Pareto 分析中，FERNme 加受控或离线 LLM 模式被报告达到建模 LLM 上限质量的约 80-90%，同时每 1,000 次交互的成本低 1-2 个数量级。
- 召回质量实验使用 5 个种子 × 40 名用户，并将 precision@5 与真实偏好进行比较；摘录给出了设置，但没有给出具体 precision 数值。
- Mem0 LLM 正面对比尚未运行，作者说明主要数值来自合成数据或 LLM 编写的数据，而不是真实用户。

## Problem

## Approach

## Results

## Link
- [https://github.com/mirkofr/FERNme](https://github.com/mirkofr/FERNme)
