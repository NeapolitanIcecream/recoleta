---
source: hn
url: https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection
published_at: '2026-06-03T23:06:36'
authors:
- pssah4
topics:
- llm-agents
- tool-selection
- mcp
- stigmergy
- code-intelligence
- prompt-caching
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Stigmergy for capability selection in LLM agent loops (skills, tools, MCP)

## Summary
## 摘要
本文提出一个本地的蚁巢式协调层，让 LLM agent 学会哪些工具、MCP 工具和技能更适合按顺序使用。它的目标是在保留缓存工具定义稳定性的同时，减少反复失败的工具探索。

## 问题
- LLM agent 会在每一步把能力描述放进上下文；Anthropic 报告称，58 个工具大约占 55,000 个 token，另一个配置甚至超过 140,000 个 token，因此大型工具目录在工作开始前就会占掉大部分 prompt。
- 随着目录变大，工具选择会变差；选错工具会带来额外调用、重试、已加载的技能文本和错误信息。
- 现有的检索、延迟加载、路由器和技能披露机制，都不会把过去的结果带到下一次选择里，所以同样的坏路径会反复出现。

## 方法
- 该方法把能力存成本地图中的节点，把能力之间的迁移存成边。
- 每条边都有信息素值、衰减后的成功和失败证据、时间戳，以及可选的用户固定标记。
- 在每一步，它会根据前一个能力到当前能力的迁移信息素，以及任务和能力描述之间的语义相似度，对候选下一步能力打分。
- 走向已接受结果的边会被强化；未使用或过时的边会衰减，这样旧路径会随着代码库和工作流变化而淡出。
- Prompt 缓存改变了默认优化方式：在可能时，论文保持完整工具块稳定，并在缓存断点之后追加一个很小的已学习路径提示，而不是每轮重写可见的工具列表。

## 结果
- 论文没有给出所提方法已经完成的受控实证研究；它定义了实验协议，并说明核心的 token 降低测试仍待执行。
- 论文报告了 1 次初步自测机制检查，显示 token 大幅减少，但冷启动成功率下降；节选没有给出这次运行的具体 token 数或成功率数值。
- 论文用已公开的平台数据作为动机：58 个工具大约会占 55,000 个 token，Anthropic 优化前报告过 134,000 个工具定义 token，社区中的一个 MCP 配置报告过约 144,800 个 token。
- 论文引用了 Anthropic 的工具搜索结果：当搜索替代一次性加载全部工具时，一个模型的选择准确率从 49% 提升到 74%，另一个模型从 79.5% 提升到 88.1%。
- 论文声称的技术结果是一个已实现的本地设计，包含确定性的带种子选择、无网络外发、带界限的信息素值 [τ_min, τ_max]、惰性指数衰减，以及明确的评估转折条件。

## Problem

## Approach

## Results

## Link
- [https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection](https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection)
