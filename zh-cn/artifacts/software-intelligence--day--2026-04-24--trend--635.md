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

# 现实限制已成为 AI 编码研究的主线

## Overview
今天的编码研究，最有力的内容集中在现实限制上。RealBench 表明，仓库级生成在完整项目上仍然会失效；token 成本研究则显示，agentic coding 的成本可能远高于聊天式辅助。当前最可信的改进来自更严格的结构：验证器反馈、自适应检索，以及围绕数据库访问设置的明确防护。

## Clusters

### 成本控制已成为编码代理研究议程的一部分
Token 成本是这批研究里最明确的现实约束。最强的证据来自一项在 OpenHands 中用八个前沿模型评估 SWE-bench Verified 的轨迹研究。Agentic coding 的 token 用量大约是单轮代码推理的 3500×，也是多轮代码聊天的约 1200×。同一个任务上的成本波动也很大，不同运行之间最高可相差 30×。论文将高成本失败与反复查看和编辑文件联系起来，也显示模型在执行前很难准确预测自己的 token 开销。第二篇论文 R2Code 提出了一条具体应对路径：更严格的检索和更小的上下文。它报告称，在五个可追踪性数据集上，平均 F1 提升 7.4%，同时通过自适应上下文控制将 token 使用最多降低 41.7%。

#### Evidence
- [How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks](../Inbox/2026-04-24--how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic-coding-tasks.md): Agentic coding 中 token 成本规模、波动性和较弱自我预测能力的主要证据。
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): 说明自适应检索可以在改进维护任务表现的同时降低 token 使用的证据。

### 仓库规模基准正在暴露当前模型对端到端实现的自动化程度有多低
当任务更接近真实软件工作时，仓库级生成仍然偏弱。RealBench 构建了来自 20 个领域的 61 个 Python 仓库，每个仓库都包含自然语言需求、UML 包图和类图，以及经人工核验的测试。最佳平均 Pass@1 只有 19.39%。仓库规模影响很大：代码行数低于 500 时，得分高于 40%；超过 2000 行时，得分低于 15%。这个基准也说明了为什么小型基准上的胜利不能直接迁移过来。平均只有 44.73% 的方法是独立的，在最大规模分层中这一比例降到 26.23%，所以依赖处理是核心问题。论文还报告，较小项目更适合整仓库生成，而仓库变大后，增量生成效果更好。

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): 仓库级基准设计、较低通过率和规模效应的主要证据。

### 结构化证据和可执行检查正在承担更多工作
在验证和维护工作里，结构化辅助仍然很有效。一篇关于自然语言到 Dafny 生成的论文报告称，直接提示几乎普遍失败；当模型拿到方法签名和验证器反馈后，结果明显改善。在抽样任务上，Gemma 4-31B 的验证成功率达到 90.91%，GPT-OSS 120B 在签名引导反馈下从 0% 提升到 81.82%。另一篇论文 R2Code 将需求和代码拆成对齐的语义部分，加入一致性检查，并在五个数据集上报告了提升。这两篇论文都指向同一种模式：当模型依据显式结构、可执行检查和更窄的证据切片工作时，编码辅助效果会更好。

#### Evidence
- [From Natural Language to Verified Code: Toward AI Assisted Problem-to-Code Generation with Dafny-Based Formal Verification](../Inbox/2026-04-24--from-natural-language-to-verified-code-toward-ai-assisted-problem-to-code-generation-with-dafny-based-formal-verification.md): Dafny 代码生成中验证器引导带来提升的证据。
- [R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability](../Inbox/2026-04-24--r2code-a-self-reflective-llm-framework-for-requirements-to-code-traceability.md): 维护任务中结构化可追踪性和自适应检索的证据。

### 运行安全研究对代理权限的讨论正变得更具体
还有一条较小但很具体的线索，涉及代理访问真实系统时的运行防护。QueryBear 认为，数据库安全需要分层控制，而不是一条只读规则。它描述的控制栈包括 SQL 解析、表和列的允许列表、AST 级查询重写、执行前成本检查、语句超时和审计日志。例子都很实际：拦截藏在注释里的 DELETE 语句、`pg_sleep(3600)` 这类拒绝服务查询、过大的连接操作，以及会暴露 `oauth_tokens` 的连接查询。这不是一篇基准论文，但它符合当天的重点：让代理动作在接触生产资源之前可以被审查。

#### Evidence
- [Giving AI Agents Database Access Is Way Harder Than It Looks](../Inbox/2026-04-24--giving-ai-agents-database-access-is-way-harder-than-it-looks.md): 分层数据库防护和具体失效模式的主要证据。
