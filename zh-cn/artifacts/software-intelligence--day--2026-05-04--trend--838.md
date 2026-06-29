---
kind: trend
trend_doc_id: 838
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
topics:
- coding agents
- repository repair
- tool calling
- program generation
- software quality
run_id: materialize-outputs
aliases:
- recoleta-trend-838
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-repair
- topic/tool-calling
- topic/program-generation
- topic/software-quality
language_code: zh-CN
---

# 编码代理正在按接口、token 成本和仓库证据接受评判

## Overview
5 月 4 日最强的工作把大语言模型（LLM）编码代理当作工程系统来审视，关注受限工具、显式仓库状态和可测量成本。Terminus-4B、ARISE 和 TSCG 给出了最清楚的证据：当代理拿到合适的接口时，更小的专用组件可以节省 token，或者改善修复效果。

## Clusters

### Bounded execution and tool interfaces
Agent 执行正变成一个有成本的子系统。Terminus-4B 训练了一个 4B 模型，让它为编码代理运行终端命令，再把简短摘要返回给主代理。文中给出的 Serilog 示例把主代理 token 从 2.46M 降到 740k，同时子代理在内部处理 9 条命令，并用大约 200 个 token 报告构建、测试和失败细节。

TSCG 在工具目录层面处理同样的部署压力。它在模型看到之前，把 JSON 工具 schema 编译成结构化文本。论文报告了跨 12 个模型约 19,000 次基准调用，小模型在 20 到 50 个工具时提升很大，在生产风格 schema 上也节省了大量 token。这个实际主张很窄，也很有用：当代理的接口按模型消费方式来写时，它调用工具会更可靠。

#### Evidence
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): Terminus-4B summary gives the execution-subagent setup, token reductions, Serilog example, and training corpus details.
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): TSCG summary gives schema-compilation method, benchmark scale, token savings, and tool-use accuracy results.

### Repository repair needs structured code evidence
仓库级修复论文关注的是，代理在改代码前能检查到哪些证据。ARISE 给仓库图增加了语句级定义-使用边，再把切片和上下文工具暴露给 SWE-agent 设置。在 SWE-bench Lite 上，它报告 Function Recall@1 提高 17.0 个百分点，Line Recall@1 提高 15.0 个百分点，Pass@1 为 22.0%，修复了 300 个问题中的 66 个。

结构化规范驱动工程（SSDE）在生成任务上提出了类似观点。它在构建 Python MVC 后端时，给 LLM 提供 Gherkin 场景、领域模型、生成的 API 签名和模板。试点结果显示，生成的签名往往比原始领域模型更有帮助：在所有测试过的 LLM 中，签名把平均测试通过率提高了 7.82 个百分点，并降低了方差。失败分析也很有用，因为 49.0% 的错误是不存在的 API 调用，20.2% 是类型不匹配。

#### Evidence
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): ARISE summary gives repository graph design, SWE-bench Lite setup, localization gains, and Pass@1 results.
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE summary gives structured inputs, evaluation setup, test-pass changes, and failure categories.

### Program generation is using search and accumulated failure evidence
ARIADNE 把竞赛编程看成固定预算下的搜索问题。它使用 Monte Carlo Tree Search (MCTS) 和一个共享黑板，黑板里存放约束、候选策略、生成的测试、反例、诊断和修复笔记。使用 GPT-4o 时，它在 APPS 上的 Pass@1 为 41.30，在 CodeContests 上为 46.67，在 CodeContests+ 上为 27.27，在 LiveCodeBench 上为 20.91，并且都优于文中列出的 CodeSim 基线。

这条工作线把执行反馈当作可复用状态。关键细节是反馈的格式：ARIADNE 把标量奖励和结构化笔记结合起来，再把搜索预算导向测试和修复更好的分支。这样做让隐藏边界情况和失败尝试进入下一次编码决策。

#### Evidence
- [ARIADNE: Agentic Reward-Informed Adaptive Decision Exploration via Blackboard-Driven MCTS for Competitive Program Generation](../Inbox/2026-05-04--ariadne-agentic-reward-informed-adaptive-decision-exploration-via-blackboard-driven-mcts-for-competitive-program-generation.md): ARIADNE summary gives MCTS and blackboard design, reward structure, datasets, and Pass@1 results.

### Functional tests are not enough for generated software
一篇论文把评估目标扩展到了可维护性。AI-generated smells 研究把 LLM 在 90 个 CodeContest 问题上的输出与人工提交对比，然后又审查了 20 个 MetaGPT 项目在需求阶段递进时的表现。它报告了 Long Method、Too Many Branches、Potential Improper API Usage、Unstable Dependency 和 God Class 这类 smell 模式。

这些证据没有修复和工具调用论文那么数值化，但警告很具体。能通过测试的代码仍然会积累维护债务，更大的生成系统需要静态检查和测试通过率一起看。SSDE 的失败分析也支持同样的工程需求：很多仓库生成错误都是 API 和类型错误，运行测试之前就能被静态分析抓到。

#### Evidence
- [AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development](../Inbox/2026-05-04--ai-generated-smells-an-analysis-of-code-and-architecture-in-llm-and-agent-driven-development.md): AI-generated smells summary gives experiments, smell categories, and claims about maintainability debt in generated code.
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE summary reports static API and type error categories and notes that more than 70% of failures can be detected by static analysis.
