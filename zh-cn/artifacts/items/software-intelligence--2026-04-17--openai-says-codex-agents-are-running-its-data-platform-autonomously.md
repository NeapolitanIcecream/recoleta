---
source: hn
url: https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/
published_at: '2026-04-17T23:48:56'
authors:
- tanelpoder
topics:
- code-agents
- data-platform-automation
- multi-agent-software-engineering
- ai-operations
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# OpenAI Says Codex Agents Are Running Its Data Platform Autonomously

## Summary
## 摘要
OpenAI 表示，基于 Codex 的代理现在在有限人工介入下处理其内部数据平台的部分工作，包括事件响应、发布管理和验证。核心判断是，有用的数据代理不仅取决于模型能力，还取决于统一且维护良好的数据基础。

## 问题
- OpenAI 的内部数据平台规模大、变化快：超过 3,500 名内部用户，600 多 PB 数据，约 70,000 个数据集，流式事件量在一年内增长了约 50 倍。
- 人工运维人员难以及时跟上管道故障、模式漂移、发布检查，以及分散在 Slack 线程、运行手册、仪表板和代码里的操作知识。
- 当底层数据资产碎片化时，数据代理就会失效。缺少元数据、血缘关系不清、所有权不明确、指标定义不一致，都会挡住可靠自动化。

## 方法
- OpenAI 将由 Codex 驱动的代理嵌入数据平台，让它们实时监控吞吐量、延迟和数据质量，然后调查卡住的作业、格式错误的事件和模式漂移等异常。
- 这些代理基于一个连通的内部数据基础工作，而不是只依赖代码仓库。这个基础包括表定义、所有权、文档、查询历史、血缘关系、仪表板、权限和生产代码。
- 代理可以执行运维动作，例如重启作业、重新分配资源、生成修复、验证修复、准备部署，以及生成供审查的拉取请求。
- OpenAI 描述了几类面向特定领域的代理：用于 Apache Spark 系统的发布代理、可检索历史修复和升级路径的值班助手，以及能启动本地服务、打开浏览器会话、测试界面改动并验证行为的开发代理。
- 信任和审查通过以下方式处理：展示假设、生成的查询、内部引用、置信度，以及针对经过验证的“黄金”来源（如已验证仪表板）的自检。

## 结果
- 已部署环境的规模：3,500 多名内部用户，600 多 PB 数据，约 70,000 个数据集。
- 增长压力：流式事件量同比增长约 50 倍。
- 文中提到的 Codex 产品使用量：每周用户超过 300 万。
- 文章声称的运维结果：损坏的管道可以触发代理，而不是等工程师处理；一些故障会在人工打开仪表板之前就被调查、调试，甚至修复；发布可以在没有人工编排的情况下继续推进。摘录没有给出这些内部部署的直接前后对比可靠性或 MTTR 数字。
- 声称的自动化范围：OpenAI 表示，Codex 已经自动生成了数百个用于大规模迁移的拉取请求。
- 文中提到的更广泛代理性能基准，不是这次数据平台部署的结果：OpenAI 的代理在 Terminal-Bench 2.0 上得分 77.3%，Claude 为 65.4%；Anthropic 模型在 SWE-bench verified 任务上的成绩被描述为中到高 60% 区间。

## Problem

## Approach

## Results

## Link
- [https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/](https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/)
