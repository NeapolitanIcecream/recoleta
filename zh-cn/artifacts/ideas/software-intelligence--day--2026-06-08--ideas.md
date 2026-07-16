---
kind: ideas
granularity: day
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-09T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- code uncertainty
- software testing
- agent runtime control
- MCP
- bug localization
- structured output
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/code-uncertainty
- topic/software-testing
- topic/agent-runtime-control
- topic/mcp
- topic/bug-localization
- topic/structured-output
language_code: zh-CN
---

# 编码代理保障机制

## 摘要
代理式软件工作有三个可用的控制点：生成代码可以在进入评审或另一个代理前先打分，MCP 代理可以用截断的最近工具历史加简短摘要运行，AI 生成测试可以在构建、执行、覆盖率、突变和修复步骤中保留候选级证据。

## 在生成代码进入评审或另一个代理步骤前做置信度评分
使用编码代理的团队可以在每个生成的补丁或函数进入评审前加一个评分。Code Is More Than Text 给出了一套具体做法：把 Top-K token 熵、采样得到的伪代码计划之间的一致性，以及自生成测试的通过率结合起来。覆盖五个代码 LLM 和四个基准后，这个集成把预测隐藏测试通过情况的平均 AUROC 从 0.696 提高到 0.776。

FASE 在测试缺失或测试成本过高时提供了一个更便宜的配套检查。它采样 10 个代码解，把它们嵌入到 Qwen3-Embedding-8B 这类模型中，用最小生成树规则聚类，再对这些簇计算熵。在 HumanEval 和 BigCodeBench-hard 上，它报告的 Spearman 相关性与 Pass@1 的平均提升为 25%，成本约为基于 LLM 的语义熵的 0.3%。

实际落地时，可以在 CI 或代理路由步骤里记录这些分数，再把分数区间和真实的评审结果、单元测试失败以及回滚数据对照。低分输出可以先送去重试、补充测试，或人工评审，再让另一个代理继续处理。

### 资料来源
- [Code Is More Than Text: Uncertainty Estimation for Code Generation](../Inbox/2026-06-08--code-is-more-than-text-uncertainty-estimation-for-code-generation.md): Shows the three code-specific uncertainty signals and benchmark gains for predicting generated-code correctness.
- [FASE: Fast Adaptive Semantic Entropy for Code Quality](../Inbox/2026-06-08--fase-fast-adaptive-semantic-entropy-for-code-quality.md): Shows a lower-cost semantic entropy method based on sample embeddings and MST clustering.

## 为 MCP 代理截断最近工具历史，并加摘要以适应冗长的企业工作流
面向企业 MCP 的代理应该有明确的上下文策略，保留最近的工具状态，并把完整轨迹存到模型上下文之外。在 D365 Finance and Operations 酒店费用基准上，保留完整的历史对话完成了 71.0% 的任务，使用了 1,480,996 个 token。保留最近 5 组完整的工具调用和响应把完成率提高到 79.0%，token 降到 535,274。再加上对最近被移出的 3 次交互做一个简短摘要，完成率提高到 91.6%，token 为 553,374。

这个方案足够小，可以放进 MCP 客户端周围的一层中间件：保存每次调用，只把最近 5 次完整交互加上一个简短的滚动摘要传给模型，并给每个工具结果附上 trace ID。trace ID 很重要，因为 20 次访谈里的企业 MCP 从业者都把快速故障定位列为主要排障障碍。同一运行层还应该在模型服从之外强制控制，比如工具白名单、状态检查和停止条件，这与 agent-harness 对独立于模型服从的控制机制要求一致。

### 资料来源
- [Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents](../Inbox/2026-06-08--less-context-better-agents-efficient-context-engineering-for-long-horizon-tool-using-llm-agents.md): Reports the D365 F&O context-pruning experiment, completion rates, token counts, and the last-five-plus-summary policy.
- [Understanding How Enterprises Adopt the Model Context Protocol for LLM-Driven Software Engineering](../Inbox/2026-06-08--understanding-how-enterprises-adopt-the-model-context-protocol-for-llm-driven-software-engineering.md): Reports enterprise MCP adoption interviews and the universal complaint about fault localization.
- [What makes a harness a harness: necessary and sufficient conditions for an agent harness](../Inbox/2026-06-08--what-makes-a-harness-a-harness-necessary-and-sufficient-conditions-for-an-agent-harness.md): Defines agent-harness runtime requirements, including task-aware context management and controls independent of model obedience.

## AI 生成单元测试的候选级证据记录
接收 AI 生成测试的团队需要为每个候选测试保留记录，包括失败和修复过的候选项。TestMap 展示了这类记录在 C#/.NET 里的样子：仓库和提交元数据、Roslyn 项目信息、构建结果、TRX 执行结果、Cobertura 覆盖率、Stryker.NET 突变数据、xNose 测试异味检查、提示词、模型设置、修复尝试，以及最终结果标签。

这会给测试生成试点带来一个实际的流程变化。每个生成的测试进入评审时，都可以附上目标方法、基线覆盖率、覆盖变化、突变信号、构建和执行日志、修复次数，以及异味检查。评审者可以拒绝那些只是能编译的测试，优先看有覆盖率或突变证据的测试，并按模型、提示词、上下文模式或修复预算查看反复出现的失败模式。一个有用的第一步，是看这份记录能否减少评审时间，并在一个真实仓库里抓住低价值但通过了的测试。

### 资料来源
- [TestMap: Evidence Infrastructure for Foundation-Model-Assisted Test Generation](../Inbox/2026-06-08--testmap-evidence-infrastructure-for-foundation-model-assisted-test-generation.md): Describes TestMap’s evidence categories, .NET toolchain, outcome labels, and candidate-level traceability for generated tests.
