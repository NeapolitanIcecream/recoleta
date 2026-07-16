---
kind: ideas
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- interactive benchmarks
- long-horizon coding
- LLM serving
- agent security
- MCP
- software engineering evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/interactive-benchmarks
- topic/long-horizon-coding
- topic/llm-serving
- topic/agent-security
- topic/mcp
- topic/software-engineering-evaluation
language_code: zh-CN
---

# 编码智能体运行控制

## 摘要
编码智能体团队现在可以把会话级检查加入发布和运维工作：统计用户纠正的多轮测试、显示重复前缀读取的服务看板，以及在执行前阻止不安全工具序列的 MCP 网关。

## 面向编码智能体用户负担的多轮发布测试
编码智能体评估应在模型或智能体策略发布前加入一次重放的开发者会话。测试应从一个不完整请求开始，让用户模拟器检查工作区，要求智能体修改计划，并记录最终验证器状态、用户纠正轮次和遗忘需求。

SWE-Together 给出了一种可用的测量方式：它在从真实会话重建的 109 个仓库任务上，评分最终仓库正确性和 User Correction。SWE-INTERACT 说明了为什么这类测试应进入发布检查。在相同底层任务上，Opus 4.8 的单轮解决率从 50.7% 降到交互设置下的 26.7%，GPT-5.5 从 48.0% 降到 24.7%，每次试验成本从 $2.78 升到 $9.84。

一个小规模采用测试可直接执行：取 20 个近期内部智能体会话，要求它们有足够的仓库状态可重放，把最终需求集隐藏在评审脚本或模拟器中，然后比较候选智能体的通过率、纠正轮次、用户消息数、成本和失败标签。这样可以发现那些能找出大多数目标、但仍会漏掉需求或提交实现缺陷的智能体。

### 资料来源
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): SWE-Together 定义了重放的多轮编码任务、最终正确性评分、User Correction 和已报告的模型结果。
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): SWE-INTERACT 报告了从单轮到交互设置的大幅解决率下降、更高的单次试验成本，以及遗忘需求和实现缺陷等失败标签。

## 面向编码智能体服务的前缀 token 成本看板
运行编码智能体的基础设施团队应在 LLM 步骤级跟踪成本，并拆分为前缀 token、追加 token 和输出 token。实用的看板应按会话组织：请求数、LLM 步骤、工具调用、前缀缓存命中和未命中、长时间工具调用，以及每个请求的成本。

TraceLab 给出了具体证据。它的轨迹覆盖 4,265 个 Claude Code 和 Codex 会话、357,161 个 LLM 步骤和 432,510 次工具调用。中位步骤读取约 119K 个前缀 token，并写出 214 个输出 token。前缀 token 占 54.90B 输入 token 中的 52.56B，占估算 API 成本的 59.5%。全局前缀缓存命中率高达 95.7%，但缓存未命中造成的预填充量仍是真正新增输入 token 的 3.8 倍。

一个低成本的第一版可以是面向本地和托管编码智能体会话的日志规范化器。它可以丢弃原始用户文本和工具 I/O，保留时间戳和 token 计数，并标记前缀缓存未命中或超过一分钟的工具调用主导成本的会话。这样，产品和基础设施团队在改变模型选择或上下文策略前，可以共同看到哪些智能体循环成本较高。

### 资料来源
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): TraceLab 提供了步骤级 schema、token 拆分、会话规模、缓存命中结果，以及前缀 token 的成本占比。

## 带作用域工具暴露的 MCP 工具流执行控制
把智能体连接到 MCP 工具的团队应把执行控制放在智能体外部，并根据已批准的工具路径和数据流规则检查每次调用。实际起点可以是一个网关：阻止没有已安装承诺的会话，记录原因代码，并防止敏感读取通过后续工具调用流向外部接收端。

trajeckt 展示了 MCP 智能体的具体机制：执行前用一个密封的承诺图声明允许的工具、顺序、数据接收端、作用域和预算。在它的冒烟测试中，`read_database` 和 `summarize` 被允许，随后当敏感数据会离开边界时，`send_email_external` 被 HTTP 403 阻止。评估范围仍然较窄，因此团队应先在少量高风险工作流上试点，例如数据库查询加工单更新、邮件或 shell 访问。

工具暴露也需要运行限制。MCP 模式研究报告称，Claude Haiku 4.5 的可见工具数在 10 到 15 个之间时，工具选择准确率降到 90% 以下；Claude Sonnet 4 的对应范围是 20 到 30 个。网关可以同时处理这两类控制：只暴露与当前会话作用域相关的工具，并在选择后执行已批准的调用路径。

### 资料来源
- [Show HN: A Firewall for AI agents with auditing](../Inbox/2026-06-29--show-hn-a-firewall-for-ai-agents-with-auditing.md): trajeckt 描述了密封的会话前承诺、失败关闭检查、污点跟踪、审计原因代码，以及读取、总结、发邮件被阻止的示例。
- [MCP Server Architecture Patterns for LLM-Integrated Applications](../Inbox/2026-06-29--mcp-server-architecture-patterns-for-llm-integrated-applications.md): MCP 服务器模式研究报告称，随着可见工具数量增加，工具选择质量会下降，并建议大型部署采用有作用域的聚合或工具检索。
