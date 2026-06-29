---
source: arxiv
url: https://arxiv.org/abs/2606.01772v1
published_at: '2026-06-01T06:53:56'
authors:
- "Jan-Philipp Stegh\xF6fer"
topics:
- requirements-engineering
- ai-assisted-development
- human-ai-interaction
- tool-integration
- software-teams
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Faster than the Team, Faster than the Customer: Tool Integration, Collaboration, and Organisational Lag in AI-assisted RE

## Summary
## 总结
这项质性行业研究发现，AI 辅助的需求工程已经在 XITASO 改变了产品负责人的工作，主要体现在待办列表、招标、文档和领域理解任务上。当天工具能连接 Jira、Confluence、代码或招标来源时，产品负责人的速度会提升；而团队和客户往往适应得更慢。

## 问题
- 这篇论文研究生成式 AI 在日常工业工作中如何影响需求工程。在这种工作里，产品负责人要把不完整的客户输入转成可用的待办项、投标书、原型和共享的产品方向。
- 这个问题重要，因为需求工作依赖工具上下文、团队讨论、客户规则和可追溯性；只看孤立的 LLM 任务测试会漏掉这些条件。
- 这项研究也检查了一个协作风险：AI 可能让某个产品负责人比开发者、客户和团队流程更快地产出工件，而这些人和流程来不及审查或吸收。

## 方法
- 作者在 2024 年对 XITASO 做了全公司调查，收集了 11 个实践社区中的 20 个 AI 使用场景。
- 一个委员会先选出与需求相关的领域，再通过访谈把它们细化为 15 个使用场景，分成 4 类：产品待办管理、招标管理、需求与领域理解，以及文档和工件创建。
- 这项研究在 2025 年末和 2026 年春季对 8 名产品负责人进行了两轮半结构化访谈；他们都有至少 5 年产品负责人经验，并且正在使用 AI。
- 涉及的工具包括 ChatXiPT、Product Copilot、MS Copilot、Claude Desktop、Claude Code、TenderZen、Curly 和 Rovo。
- 核心机制很直接：产品负责人把项目工件、招标文档、待办项、代码上下文、会议数据或提示词输入 AI 工具；工具起草、重组、搜索、提取、总结或生成原型输出，再由产品负责人审核。

## 结果
- 这篇论文没有对准确性、质量或生产率做受控基准测试。证据是质性的，主要来自参与者数量、工具数量和使用场景数量。
- 研究识别出 15 个 AI 辅助需求工程使用场景，分属 4 类，基于最初调查中的 20 个场景和对 8 名产品负责人的访谈。
- 待办项细化是最常见的使用场景：8 名产品负责人里有 6 人用 AI 拆分 epic、查找重复项、补充验收标准、发现缺口或改进待办项。
- 待办项冷启动由 8 人中的 4 人使用，输入 Excel 表、截图或规格文档，让 AI 生成大量产品待办项；参与者报告节省了大量时间，但节省了多少小时，摘录中没有给出测量值。
- 招标管理主要由 8 人中的 2 人使用，流程分为 4 个阶段：招标发现、招标分析、参考匹配和投标书撰写。
- 主要经验证据是工具连接决定价值：像 Jira 加上通过 MCP 访问源代码这样的集成设置，让产品负责人可以结合实现上下文细化需求；而工具之间缺少连接时，仍然要靠人工交接。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.01772v1](https://arxiv.org/abs/2606.01772v1)
