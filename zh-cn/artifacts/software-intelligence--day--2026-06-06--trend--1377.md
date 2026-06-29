---
kind: trend
trend_doc_id: 1377
granularity: day
period_start: '2026-06-06T00:00:00'
period_end: '2026-06-07T00:00:00'
topics:
- agent control
- coding agents
- MCP
- desktop automation
- AI cost governance
- LLM safety
- context management
run_id: materialize-outputs
aliases:
- recoleta-trend-1377
tags:
- recoleta/trend
- topic/agent-control
- topic/coding-agents
- topic/mcp
- topic/desktop-automation
- topic/ai-cost-governance
- topic/llm-safety
- topic/context-management
language_code: zh-CN
---

# 代理系统正被上下文、工具、成本和安全控制限制住

## Overview
这一时期最清楚的信号是，代理在真正做事时开始被操作控制包住。Context Sculpting 测试可编辑上下文，clawdcursor 暴露带保护的桌面操作，Cursor 增加支出控制。证据很实用，但不均衡：很多条目在讲机制，少数条目给出基准。

## Clusters

### 可编辑的代理上下文
Context Sculpting 测试了一个双模型框架，较强的外层模型可以重写较弱任务代理的工作上下文。这个设置有用，因为长时间运行的代理常会带着过时文件、失败路径、工具噪声和干扰证据。

结果支持可行性，但成本上限很清楚。在第一个演示里，8 次运行全部通过验证，框架没有做任何重写。在更嘈杂的第二个演示里，外层代理在 2 次受框架约束的运行中做了 14 次上下文重写。编码修复示例在两种形式下都通过了：对照组用了 7 轮、42.7 秒、约 0.015 美元；受框架约束的运行用了 12 轮、566.9 秒、约 1.06 美元，并触发了最大轮次护栏。结果给出一个直接的提醒：上下文编辑能起作用，但策略选择会让它很快变贵。

#### Evidence
- [Context Sculpting](../Inbox/2026-06-06--context-sculpting.md): Summarizes the two-model context rewriting harness, run counts, rewrite counts, verification results, cost, latency, and guardrail outcome.

### 桌面和工具运行时控制
模型上下文协议（MCP）正在成为代理工具的实际边界。clawdcursor 通过一个 MCP 入口提供桌面控制，先用无障碍元数据，再用 OCR 或截图。它的精简接口有 6 组工具，而 94 个工具的细粒度接口仍保留，用于兼容和调试。每次调用都会经过安全检查，破坏性操作需要确认。

Aquifer 解决的是另一类运行问题：突发式工具流量。代理通过 MCP 或 HTTP 提交作业，Aquifer 将其存入 SQLite，并由每个上游对应的 worker 按配置速率发请求。示例限制包括 OpenAI 每秒 10 个请求、并发 3 个请求，以及 Stripe 每秒 20 个请求、并发 5 个请求。这些是工程控制，摘录里没有吞吐量或任务完成率的基准。

#### Evidence
- [AI Can now control your desktop](../Inbox/2026-06-06--ai-can-now-control-your-desktop.md): Describes clawdcursor's MCP desktop-control design, compact tool groups, platform support, and safety gate.
- [Show HN: Aquifer – an MCP runtime for spiky agent tool traffic](../Inbox/2026-06-06--show-hn-aquifer-an-mcp-runtime-for-spiky-agent-tool-traffic.md): Describes Aquifer's durable queue, rate controls, SQLite persistence, webhooks, SSE status, and example rate limits.

### 编码代理成本治理
成本控制现在已经进入编码代理的产品设计。Cursor 将 Teams 年费座位价格下调 20%，降到每用户每月 32 美元，新增 120 美元的 Premium 档，把第一方 Composer 用量和第三方模型额度分开，还增加了支出提醒、仪表盘、预算、模型访问控制和代理权限设置。列出的模型价格说明了压力：Composer 2.5 的定价是每百万输入 token 0.50 美元、每百万输出 token 2.50 美元，而 Claude Opus 4.7 和 4.8 的标价大约是这个的 10 倍。

维护问题出现在 Code Is Cheap(er) 里。文章认为，生成代码出现的速度可能快过审阅者理解它的速度，所以团队应当把 LLM 改动控制得很小，并把简化当作工程职责。它没有给出测量数据，但和运行层面的主题一致：便宜的生成仍会带来审阅、归属和预算工作。

#### Evidence
- [Cursor cuts prices, adds enterprise spend controls amid "tokenomics" reckoning](../Inbox/2026-06-06--cursor-cuts-prices-adds-enterprise-spend-controls-amid-tokenomics-reckoning.md): Provides Cursor pricing changes, enterprise spend controls, and model cost comparisons.
- [Code Is Cheap(er)](../Inbox/2026-06-06--code-is-cheap-er.md): Summarizes the argument that AI lowers code creation cost while increasing the burden of reading, judging, and simplifying generated code.

### 高后果动作的封控
这条安全主题主张，对那些一旦出问题就来不及补救的动作，要设硬边界。Observational Governance Infrastructure（IGO）用了四层结构：前三层监测可恢复故障，第四层收纳必须保持不可达的动作。它的 Cognitive Performance Index（CPI）公式在时间置信度方差上升时降低分数，80 分以上标为稳定，50 分以下标为临界波动。

报告中的证据包括 4 家机构的测量，以及对 4 个全球 LLM 的审计。CPI 报告值大约在 22 到 55 之间，接近或低于临界阈值。论文还报告了一次对 Claude Opus 4.8 的压力测试，但最强的结论是架构层面的：可恢复错误交给检测，毁灭性风险动作交给封控。

#### Evidence
- [You can't detect your way out of catastrophic LLM failure](../Inbox/2026-06-06--you-can-t-detect-your-way-out-of-catastrophic-llm-failure.md): Summarizes IGO's four-layer safety design, CPI formula and bands, production measurements, and Claude Opus 4.8 stress-test claims.
