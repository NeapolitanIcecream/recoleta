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
OpenAI 表示，基于 Codex 的智能体现在可以在其内部数据平台中以有限人工干预处理部分工作，包括事故响应、发布管理和验证。核心观点是，有用的数据智能体与其说取决于模型能力本身，不如说更取决于统一且维护良好的数据基础。

## 问题
- OpenAI 的内部数据平台规模大且变化快：有 3,500 多名内部用户、超过 600 PB 的数据、约 70,000 个数据集，而且流式事件量一年内增长了约 50 倍。
- 人工运维人员难以跟上管道故障、模式漂移、发布检查，以及分散在 Slack 线程、运行手册、仪表板和代码中的操作知识。
- 底层数据资产碎片化时，数据智能体会失效。缺失元数据、血缘关系薄弱、所有权不清和指标定义不一致，都会阻碍可靠的自动化。

## 方法
- OpenAI 将由 Codex 驱动的智能体嵌入数据平台，让它们实时监控吞吐量、延迟和数据质量，然后调查作业停滞、事件格式错误和模式漂移等异常。
- 这些智能体运行在一个互联的内部数据基础之上，其中包括表定义、所有权、文档、查询历史、血缘、仪表板、权限和生产代码，而不只是一个代码仓库。
- 智能体可以执行重启作业、重新分配资源、生成修复、验证这些修复、准备部署以及生成供审查的拉取请求等运维操作。
- OpenAI 描述了几个面向特定领域的智能体：用于 Apache Spark 系统的发布智能体、用于检索以往修复方案和升级路径的值班助手，以及能够启动本地服务、打开浏览器会话、测试 UI 变更并验证行为的开发智能体。
- 信任和审查通过展示假设、生成的查询、内部引用、置信度，以及针对受信任“黄金”来源（如已验证仪表板）的自检来处理。

## 结果
- 已部署环境的规模：3,500+ 名内部用户、600+ PB 数据、约 70,000 个数据集。
- 增长压力：流式事件量同比增长约 50 倍。
- 文章提到的 Codex 产品使用情况：每周用户超过 300 万。
- 宣称的运维结果：损坏的管道可以触发智能体，而不是等待工程师；一些故障会在人类打开仪表板之前就被调查、调试，有时还会被解决；发布可以在没有人工编排的情况下继续进行。摘录没有给出这些内部部署在可靠性或 MTTR 方面的直接前后对比数据。
- 宣称的自动化范围：OpenAI 表示，Codex 已自动为大规模迁移生成了数百个拉取请求。
- 文中提到的更广泛智能体性能基准数字，并非这个数据平台部署本身：OpenAI 的智能体在 Terminal-Bench 2.0 上得分为 77.3%，Claude 为 65.4%；Anthropic 模型在 SWE-bench verified tasks 上达到 60% 中段到高段。

## Problem

## Approach

## Results

## Link
- [https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/](https://www.forbes.com/sites/victordey/2026/04/17/openai-says-codex-agents-are-running-its-data-platform-autonomously/)
