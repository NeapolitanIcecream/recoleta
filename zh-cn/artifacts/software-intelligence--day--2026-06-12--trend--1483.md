---
kind: trend
trend_doc_id: 1483
granularity: day
period_start: '2026-06-12T00:00:00'
period_end: '2026-06-13T00:00:00'
topics:
- coding agents
- agent harnesses
- AI workflow
- engineering judgment
- blockchain state
run_id: materialize-outputs
aliases:
- recoleta-trend-1483
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-harnesses
- topic/ai-workflow
- topic/engineering-judgment
- topic/blockchain-state
language_code: zh-CN
---

# Coding agents need bounded tools and deliberate human checkpoints

## 概览
当天最强的信号是对 AI 辅助编码的实际控制。Model Context Protocol harness、Agent Joe 和并行代理提示都把代理当作需要限定上下文、限制动作并设置明确审查点的工作者。

## 研究发现

### Coding-agent harnesses and action limits
实践重点在于代理设置和工具权限。一个 harness 故事把 Claude 设置从一个 1,800 行的 `CLAUDE.md` 迁到分范围的文件里，再迁到 `keystone-mcp`。这是一个 Model Context Protocol 服务器，它把规则、技能、状态、验证和预算数据暴露给代理。Agent Joe 把控制放在命令层：只做 Rust 工作、没有 shell 访问、可用操作更少。一个 prompt 模板项展示了更宽松的做法，把多个代理分配到不同目标上，之后再合并，但除了说这样可以更快、更详细之外，没有给出评估。

#### 资料来源
- [From a Single File to an MCP Server: Six Rewrites of My Own Harness](../Inbox/2026-06-12--from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness.md): Summarizes the harness rewrite, scoped rules, Keystone, and keystone-mcp capabilities.
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): Describes Agent Joe’s Rust-only design and lack of shell access.
- [Digg](../Inbox/2026-06-12--digg.md): Summarizes the parallel-agent prompt pattern and lack of benchmark results.

### Human judgment around AI-assisted work
两篇内容都在讲操作者，不是在讲代理。第一篇认为，AI 的即时响应去掉了过去会从搜索、等待和卡住中出现的停顿。它提到的失败模式是任务范围外扩：一个短任务会在检查原始目标之前，变成两个小时的提示、重构和加功能。给出的解决办法很直接：每 30 分钟停下来一次，不用模型，重新看目标。第二篇把工程“品味”拆成产品思维、系统思维和质量校准。在这个说法里，人要做的是选对问题、架构和适合当下的严格程度。

#### 资料来源
- [AI Doesn't Just Save Time. It Removes the Pauses](../Inbox/2026-06-12--ai-doesn-t-just-save-time-it-removes-the-pauses.md): Summarizes the claim that AI removes pauses and can create continuous scope expansion.
- [What Do Engineers Mean When We Say "Taste"?](../Inbox/2026-06-12--what-do-engineers-mean-when-we-say-taste.md): Defines engineering taste as product thinking, system thinking, and quality calibration.

### Public state and blockchain semantics
这篇区块链文章是概念性的，但它补出了一个相关主题：公共系统要先决定哪些现实世界的主张值得正式结算。文章把 Ethereum 看作可编程公共状态的前身，并把资产、身份、主张、收据和记录列为适合上链表示的对象。它还认为，在协议把某个主张固化之前，AI 工具和开放网络常常先提供语言、证据和修正。文中没有报告基准或对比性能结果。

#### 资料来源
- [The World Computer Has Children](../Inbox/2026-06-12--the-world-computer-has-children.md): Summarizes the Ethereum-as-parent argument and the role of AI and the open web in creating settleable claims.
