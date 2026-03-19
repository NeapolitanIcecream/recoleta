---
source: hn
url: https://soapbox.pub/blog/announcing-sheila/
published_at: '2026-03-06T23:08:29'
authors:
- knewter
topics:
- ai-agent
- workflow-automation
- accounting-automation
- human-in-the-loop
- tool-using-agents
relevance_score: 0.07
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Sheila, an AI agent that replaced our accounting flow

## Summary
Sheila 是一个用于会计与付款运营的 AI 代理，作者声称它已替代 Soapbox 的整套 accounting flow。文章的核心贡献不是新模型，而是一种可落地的 agent 构建模式：用细粒度脚本加自然语言工作流说明，并在人类监督下持续迭代。

## Problem
- 文章要解决的是**真实业务中 AI agent 难以稳定完成端到端流程**的问题，尤其是发票处理、付款、记账、报销归档这类跨多个系统的会计工作。
- 这很重要，因为现有很多 agent 平台更像演示系统；一旦进入生产环境，复杂多步流程、边界情况和外部系统集成会让 agent 变得脆弱。
- 对中小团队而言，会计运营重复、繁琐且高频，若能被可靠自动化，就能显著节省人工时间并降低流程摩擦。

## Approach
- 核心方法很简单：**不要先做复杂自治系统，而是先做很多只完成单一动作的小脚本**，例如查余额、发起付款、上传文件、读邮件、写表格。
- 作者共测试了**50+ 个脚本**，让每个脚本先单独可靠，再让代理在执行任务时把它们按顺序串起来。
- 再写一份约 **600 行** 的 `AGENTS.md`，用自然语言描述完整工作流；当用户说“process invoices”时，agent 读取说明并选择合适脚本执行。
- 系统运行在 OpenCode 中，并采用**human-in-the-loop**：代理可以起草邮件、准备付款，但人会在终端中观察和确认关键动作。
- 作者强调自底向上的迭代式开发：脚本测试、发现边界情况、修改说明、端到端重测，经过数百轮反馈把流程做稳。

## Results
- 最强的实际结果主张是：Sheila 已“**replaced our entire accounting flow**”，覆盖**承包商发票、法币付款（ACH/wire via Mercury）、比特币付款（Kraken/Lightning/Boltz）、记账、报销跟踪、P&L、1099 报告**等完整流程。
- 文章给出的具体实现规模包括：**50+ scripts** 和约 **600-line AGENTS.md**，表明系统主要依赖工具化动作与文字工作流编排，而非单一大而全 agent。
- 作者明确表示 Sheila **不是完全自治**，而是在终端中由人监督执行；因此其结果更像“高可靠半自动生产系统”而非无人值守代理。
- 文中**没有提供标准基准、成功率、节省时间百分比、成本下降、错误率或与其他方法/平台的定量对比**。
- 没有公开实验数据支持“OpenCode 比 OpenClaw 更适合真实 agent”的结论；这是一篇基于单一实际部署案例的经验性主张。

## Link
- [https://soapbox.pub/blog/announcing-sheila/](https://soapbox.pub/blog/announcing-sheila/)
