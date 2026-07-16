---
kind: trend
trend_doc_id: 635
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
topics:
- coding-agents
- token-cost
- repo-level-generation
- verification
- traceability
- agent-safety
run_id: materialize-outputs
aliases:
- recoleta-trend-635
tags:
- recoleta/trend
- topic/coding-agents
- topic/token-cost
- topic/repo-level-generation
- topic/verification
- topic/traceability
- topic/agent-safety
language_code: zh-CN
---

# 实际限制现在是 AI 编码研究的主线

## 概览
今天的编码研究最强的部分是对实际限制的说明。RealBench 显示 repo 级生成在完整项目上仍然会失效，token 成本研究显示 agentic coding 可能比聊天式帮助贵得多。最可信的改进来自更紧的结构：验证器反馈、自适应检索，以及围绕数据库访问的明确防护。

## 研究发现

### Cost control is now part of the coding-agent research agenda
Token 成本是这一批研究里最清楚的实际约束。最强证据来自一项在 OpenHands 上、使用八个前沿模型对 SWE-bench Verified 的轨迹研究。Agentic coding 使用的 token 约比单轮代码推理多 3500 倍，约比多轮代码聊天多 1200 倍。同一任务的成本波动也很大，运行之间最高可差 30 倍。论文把高成本失败与反复查看和编辑文件联系起来，并显示模型在执行前很难预测自己的 token 账单。另一篇论文 R2Code 给出一个具体方向：更紧的检索和更小的上下文。它在五个可追踪性数据集上平均提升 7.4% 的 F1，同时通过自适应上下文控制将 token 使用最多减少 41.7%。

#### 资料来源
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Main evidence for token cost scale, variance, and weak self-prediction in agentic coding.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Evidence that adaptive retrieval can cut token use while improving a maintenance task.

### Repo-scale benchmarks are exposing how little current models automate end-to-end implementation
当任务看起来像真实软件工作时，repo 级生成仍然很弱。RealBench 构建了 61 个 Python 仓库，来自 20 个领域，每个仓库都有自然语言需求、UML 包图和类图，以及人工验证的测试。最佳平均 Pass@1 只有 19.39%。仓库规模影响很大：500 行代码以下的得分高于 40%，2000 行以上低于 15%。这个基准也说明了为什么小型基准上的进步很难直接迁移。平均只有 44.73% 的方法是独立的，在最大一档里这个比例降到 26.23%，所以处理依赖关系才是核心问题。论文还报告说，整个仓库生成在较小项目上更好，而增量生成在仓库变大后更好。

#### 资料来源
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Primary evidence for repo-level benchmark design, low pass rates, and size effects.

### Structured evidence and executable checks are carrying more of the load
验证和维护工作仍然适合结构化辅助。一篇关于自然语言到 Dafny 生成的论文报告说，直接提示几乎总是失败；当模型拿到方法签名和验证器反馈后，结果好得多。在抽样任务上，Gemma 4-31B 的验证成功率达到 90.91%，GPT-OSS 120B 在签名引导反馈下从 0% 提升到 81.82%。另一篇论文 R2Code 把需求和代码拆成对齐的语义部分，加上一致性检查，并在五个数据集上报告提升。合起来看，这些论文指向同一种模式：当模型依靠明确结构、可执行检查和更窄的证据片段工作时，编码辅助效果更好。

#### 资料来源
- [From Natural Language to Verified Code: Toward AI Assisted Problem-to-Code Generation with Dafny-Based Formal Verification](../Inbox/2026-04-24--from-natural-language-to-verified-code-toward-ai-assisted-problem-to-code-generation-with-dafny-based-formal-verification.md): Evidence for verifier-guided gains in Dafny code generation.
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): Evidence for structured traceability and adaptive retrieval in maintenance tasks.

### Operational safety work is getting more specific about agent permissions
另一个较小但具体的主题是围绕 agent 访问真实系统的运行防护。QueryBear 认为数据库安全需要分层控制，而不是单一的只读规则。它描述的技术栈包括 SQL 解析、表和列白名单、AST 级查询重写、执行前成本检查、语句超时和审计日志。例子很实际：阻止注释隐藏的 DELETE 语句、`pg_sleep(3600)` 拒绝服务查询、过大的 join，以及暴露 `oauth_tokens` 的 join。这不是一篇基准论文，但它符合当天的重点：在 agent 接触生产资源之前，先让它们的动作可审查。

#### 资料来源
- [Giving AI Agents Database Access Is Way Harder Than It Looks](../Inbox/2026-04-24--giving-ai-agents-database-access-is-way-harder-than-it-looks.md): Primary evidence for layered database guardrails and concrete failure modes.
