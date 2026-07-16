---
kind: trend
trend_doc_id: 1588
granularity: day
period_start: '2026-06-21T00:00:00'
period_end: '2026-06-22T00:00:00'
topics:
- agent evaluation
- coding agents
- open weights
- local observability
- cost governance
- architecture boundaries
run_id: materialize-outputs
aliases:
- recoleta-trend-1588
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/open-weights
- topic/local-observability
- topic/cost-governance
- topic/architecture-boundaries
language_code: zh-CN
---

# 智能体工作正通过学习测试、边界检查和本地收据接受评估

## 概览
当天最明确的信号是围绕智能体的问责。Machine Studying 询问智能体能否在考试前学会一个新语料。ANMA、PeekAI 和 Lupen 让开发者更容易在本地机器上阻断、追踪和审计编码智能体的行为。

## 研究发现

### 语料专业能力评估
Machine Studying 为评估智能体在下游任务公布前，能否基于未见过的文档语料做准备，提供了一个具体测试。论文提出的 StudyBench 覆盖 DSPy 代码、OpenClaw 代码和机器学习文献。它的指标奖励在较低推理 token 预算下取得更高准确率，因此需要多轮搜索循环的智能体得分较低。

早期结果偏谨慎。检索增强生成、长上下文和简单微调都不能稳定地产生可用的语料专业能力。一个例子显示，Qwen3.5-9B 在被强制使用 20 次搜索迭代时，在 DSPy 上有所提升；但更广泛的结论是，如果缺少更好的学习行为，可访问的证据仍可能没有被用上。

#### 资料来源
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Machine Studying、StudyBench 设计、专业能力指标和早期结果的摘要。

### 开放权重编码模型
Z.ai 发布 GLM-5.2，把开放权重描述为编码智能体团队的一项运维选择。模型卡声称该模型有 7530 亿参数、MIT 许可证、可下载权重和 100 万 token 上下文窗口。这些声明关系到需要让智能体处理大型代码库，同时控制数据处理和访问风险的团队。

基准数字很具体，但仍由厂商发布。Z.ai 报告称，在 Terminus-2 运行设置下，GLM-5.2 在 SWE-bench Pro 上得分 62.1，在 Terminal-Bench 2.1 上得分 81.0。更强的证据来自部署层面：已复制的权重比托管 API 访问更难撤回。

#### 资料来源
- [China's Z.ai open-sourced a frontier coding model as Washington bans it rival](../Inbox/2026-06-21--china-s-z-ai-open-sourced-a-frontier-coding-model-as-washington-bans-it-rival.md): GLM-5.2 发布、许可、上下文长度和基准声明的摘要。

### 面向较便宜编码智能体的架构边界
ANMA 针对一个窄范围失效模式：编码智能体跨越已声明的模块边界进行编辑。开发者为模块编写 YAML 契约，然后 `anma sync` 生成 Claude Code 指引、钩子、后端配置、持续集成检查，以及可选的所有权文件。

最有力的证据来自较便宜的模型。在 Python 基准中，Claude Haiku 4.5 在 19 次普通仓库运行中有 13 次违反边界，而使用 ANMA 的 20 次运行中有 0 次违反。TypeScript 后续测试报告称，对照组 20 次中有 18 次违反，使用 ANMA 时 20 次中有 0 次违反。作者还表示，Claude Opus 4.8 在没有 ANMA 的情况下也遵守了 Python 边界，这把结论限定在治理和较便宜智能体的使用场景。

#### 资料来源
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): ANMA 契约、生成产物、语言支持和基准结果的摘要。

### 本地 trace 和成本收据
PeekAI 和 Lupen 都把智能体操作视为本地记录，开发者应能在不上传敏感日志的情况下检查这些记录。PeekAI 通过 `peekai.init()` 为 Python 智能体调用加上检测，记录大语言模型调用、工具调用、token、成本、错误和重放运行，并存入本地 SQLite 数据库。它的演示展示了一条含三个 span 的 trace，包括运行时间、token 和成本拆分，但没有正式基准。

Lupen 关注 Claude Code 和 Codex 的支出。它读取本地 JSONL 日志，按会话、轮次、步骤、技能组和子智能体分组，然后根据 token 数量和公开价格表重新计算成本。它的 CLI 可以在预算或验证检查失败时以退出码 4 退出，这让脚本更容易捕捉成本漂移和失控会话。

#### 资料来源
- [Show HN: PeekAI – Local-first observability for Python AI agents](../Inbox/2026-06-21--show-hn-peekai-local-first-observability-for-python-ai-agents.md): PeekAI 本地追踪、存储、重放、演示指标，以及缺少正式基准的摘要。
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): Lupen 本地日志解析、成本重算、验证和预算门禁的摘要。
