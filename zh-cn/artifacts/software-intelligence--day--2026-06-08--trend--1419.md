---
kind: trend
trend_doc_id: 1419
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
topics:
- AI coding agents
- code uncertainty
- software testing
- agent runtime control
- MCP
- bug localization
- structured output
run_id: materialize-outputs
aliases:
- recoleta-trend-1419
tags:
- recoleta/trend
- topic/ai-coding-agents
- topic/code-uncertainty
- topic/software-testing
- topic/agent-runtime-control
- topic/mcp
- topic/bug-localization
- topic/structured-output
language_code: zh-CN
---

# AI 软件论文优先关注可测量的置信度和受控的 agent 运行时

## Overview
当天的研究把 AI 软件工作当作一个工程控制问题。最强的论文会在生成代码和 agent 行动周围加入可测量的置信度、上下文限制和可追踪验证。《Code Is More Than Text》、FASE 和 Less Context, Better Agents 给出了最清晰的量化信号。

## Clusters

### Code confidence signals
两篇论文给出在生成代码进入更大工作流前对其打分的具体方法。《Code Is More Than Text》把 token 熵峰值、采样得到的伪代码一致性和自生成测试结合起来。在五个代码大语言模型（LLMs）和四个基准上，它的集成方法把接收者操作特征曲线下面积（AUROC）平均提高到 0.776，比最强的自然语言衍生基线高 8.1 个百分点。

FASE，即 Fast Adaptive Semantic Entropy，走的是更便宜的路线。它为每个任务嵌入 10 个代码样本，用最小生成树规则聚类，并在这些簇上计算熵。在 HumanEval 和 BigCodeBench-hard 上，Qwen3-Embedding-8B 版本报告与 Pass@1 的 Spearman 相关系数平均提升 25%，运行成本约为基于 LLM 的语义熵的 0.3%。

结构化输出控制提供了一个边界案例。Template Token Match Generation 几乎消除了 JSON、SQL、代码和函数调用中的语法错误，但模式错误和值错误仍然存在。格式控制能帮助流水线解析输出；它不能证明生成的产物就是正确的那个。

#### Evidence
- [Code Is More Than Text: Uncertainty Estimation for Code Generation](../Inbox/2026-06-08--code-is-more-than-text-uncertainty-estimation-for-code-generation.md): Code-specific uncertainty ensemble, AUROC results, and cost comparisons.
- [FASE: Fast Adaptive Semantic Entropy for Code Quality](../Inbox/2026-06-08--fase-fast-adaptive-semantic-entropy-for-code-quality.md): FASE method, benchmark scope, correlation gains, and runtime-cost result.
- [Empirical Study for Structured Output Control in LLMs for Software Engineering](../Inbox/2026-06-08--empirical-study-for-structured-output-control-in-llms-for-software-engineering.md): Structured-output failure taxonomy and TTMG finding.

### Agent runtime control
Agent 论文关注模型周围的运行时层：保留哪些上下文、哪些工具可以改变状态，以及企业集成如何失败。Less Context, Better Agents 给出了最清楚的测量结果。在一个 50 任务的 Microsoft Dynamics 365 Finance and Operations 酒店费用基准上，只保留最近五次工具交互再加一段简短摘要，可以达到 91.6% 的完成率，同时使用 553,374 个 token。保留完整历史的完成率是 71.0%，使用 1,480,996 个 token。

这篇 harness 定义论文把一个含糊术语收紧为四项操作要求：一个 agent 循环、会改变环境的工具、任务感知的上下文管理，以及不依赖模型服从的控制。它把这个测试应用到 Claude Code、Codex CLI、Aider、Cline、OpenHands 和 SWE-agent。

企业 Model Context Protocol（MCP）的证据指向同一个控制面。对 20 位从业者的访谈发现，所有人都认为 MCP 重要，同时所有人也把快速故障定位列为主要排障障碍。Context rot 带来一条维护警告：在 356 个仓库中，23.0% 至少有一处过时的 AI 配置引用。

#### Evidence
- [Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents](../Inbox/2026-06-08--less-context-better-agents-efficient-context-engineering-for-long-horizon-tool-using-llm-agents.md): Context-pruning setup and measured completion, token, and time results.
- [What makes a harness a harness: necessary and sufficient conditions for an agent harness](../Inbox/2026-06-08--what-makes-a-harness-a-harness-necessary-and-sufficient-conditions-for-an-agent-harness.md): Agent harness definition and inclusion tests.
- [Understanding How Enterprises Adopt the Model Context Protocol for LLM-Driven Software Engineering](../Inbox/2026-06-08--understanding-how-enterprises-adopt-the-model-context-protocol-for-llm-driven-software-engineering.md): Enterprise MCP interview findings and adoption obstacles.
- [Context Rot in AI-Assisted Software Development: Repurposing Documentation Consistency for AI Configuration Artifacts](../Inbox/2026-06-08--context-rot-in-ai-assisted-software-development-repurposing-documentation-consistency-for-ai-configuration-artifacts.md): Context rot definition and repository-level stale-reference measurements.

### Validation artifacts and repair evidence
几篇论文为 AI 系统生成或检查的产物建立了证据链。TestMap 记录 foundation-model 生成的单元测试在 C#/.NET 仓库中的生命周期。它保存构建结果、执行结果、覆盖率、变异信号、测试异味、修复尝试、提示词和模型设置。这篇论文没有报告基准胜出，所以它的贡献是候选级别的可观测性。

MLC 试图降低 bug 定位成本。它在冻结的代码 LLM 上加了一个小型 bug/no-bug 输出头，并用每个文件一个生成 token 来预测所有有 bug 的行。在完整文件版 Defects4J 上，采用参数高效微调的 MLC Qwen1.7B 达到 39.5% 的 Top-5 准确率，领先于列出的 Ochiai 和 DeepFL Top-5 基线。

ATTAIN 把轨迹证据用于安全维护。它在历史 Java 库版本上运行公开漏洞利用，比较执行分歧，让一个 LLM 检查相关 diff，并标记受影响的版本。它的评估覆盖 224 个 CVE、25,943 个版本和 128 个库，报告的 F1 分数是 93.24%。

#### Evidence
- [TestMap: Evidence Infrastructure for Foundation-Model-Assisted Test Generation](../Inbox/2026-06-08--testmap-evidence-infrastructure-for-foundation-model-assisted-test-generation.md): TestMap evidence categories, tools, outcomes, and lack of quality benchmark results.
- [Multi-task LLMs for Bug Classification: Efficient Inference with Auxiliary Decoding Heads](../Inbox/2026-06-08--multi-task-llms-for-bug-classification-efficient-inference-with-auxiliary-decoding-heads.md): MLC method and Defects4J/PypiBugs line-level localization results.
- [ATTAIN: Automated Exploit Failure Analysis through Trace-Driven Diff Analysis](../Inbox/2026-06-08--attain-automated-exploit-failure-analysis-through-trace-driven-diff-analysis.md): ATTAIN trace-driven method, evaluation scale, and F1 result.

### Domain-specific agent grounding
SIGA 给出了特定科学软件的一种实用模式。它保持 coding-agent harness 不变，再加入模拟器特定检索、短程序记忆、XML 验证器和停止规则。在一个代表性的 GEOS 任务上，它大约五分钟就能生成完整输入 deck，TreeSim 高于 0.90，和花了大约三小时的人类专家一致。在更难的保留 GEOS 集上，加入 grounding 后，TreeSim 从 0.720 提升到 0.789。

这篇网络运维论文给出更大的生产环境结论：一个用于超大规模故障响应的多 agent 系统可以自主解决 90% 以上已经明确的故障类别，平均修复时间从小时降到分钟。摘录里没有原始故障数量和按类别的表格，所以这个结论更适合作为架构证据，作为可独立核查的基准则要弱一些。

#### Evidence
- [SIGA: Self-Evolving Coding-Agent Adapters for Scientific Simulation](../Inbox/2026-06-08--siga-self-evolving-coding-agent-adapters-for-scientific-simulation.md): SIGA grounding components and GEOS results.
- [Autonomous Incident Resolution at Hyperscale: An Agentic AI Architecture for Network Operations](../Inbox/2026-06-08--autonomous-incident-resolution-at-hyperscale-an-agentic-ai-architecture-for-network-operations.md): Autonomous network-incident architecture and reported production outcomes, with missing raw evaluation details.
