---
kind: trend
trend_doc_id: 838
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
topics:
- "\u7F16\u7801 agent"
- "\u4ED3\u5E93\u4FEE\u590D"
- "\u5DE5\u5177\u8C03\u7528"
- "\u7A0B\u5E8F\u751F\u6210"
- "\u8F6F\u4EF6\u8D28\u91CF"
run_id: materialize-outputs
aliases:
- recoleta-trend-838
tags:
- recoleta/trend
- "topic/\u7F16\u7801-agent"
- "topic/\u4ED3\u5E93\u4FEE\u590D"
- "topic/\u5DE5\u5177\u8C03\u7528"
- "topic/\u7A0B\u5E8F\u751F\u6210"
- "topic/\u8F6F\u4EF6\u8D28\u91CF"
language_code: zh-CN
---

# 编码 agent 正在按接口、token 成本和仓库证据接受评判

## Overview
5 月 4 日最有力的工作把大型语言模型（LLM）编码 agent 当作工程系统来评估，重点是有边界的工具、明确的仓库状态和可度量成本。Terminus-4B、ARISE 和 TSCG 给出了最清晰的证据：当 agent 获得合适接口时，更小的专用组件可以节省 token 或改进修复。

## Clusters

### 有边界的执行和工具接口
Agent 执行正在变成一个需要计量成本的子系统。Terminus-4B 训练了一个 4B 模型，让它为编码 agent 运行终端命令，再向主 agent 返回紧凑摘要。论文报告的 Serilog 示例把主 agent token 从 2.46M 降到 740k，同时子 agent 在内部处理 9 条命令，并用约 200 个 token 报告构建、测试和失败细节。

TSCG 在工具目录层面处理同一类部署压力。它在模型看到 JSON 工具 schema 之前，先把这些 schema 编译成结构化文本。论文报告了约 19,000 次基准调用，覆盖 12 个模型；在 20 到 50 个工具的设置下，小模型提升很大，并且在接近生产环境的 schema 上节省了大量 token。它的实用主张范围很窄，但有用：当接口按模型消费方式来编写时，agent 能更可靠地调用工具。

#### Evidence
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): Terminus-4B 摘要给出了执行子 agent 的设置、token 减少、Serilog 示例和训练语料细节。
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): TSCG 摘要给出了 schema 编译方法、基准规模、token 节省和工具使用准确率结果。

### 仓库修复需要结构化代码证据
仓库级修复论文关注 agent 在编辑代码前能检查哪些证据。ARISE 向仓库图加入语句级 definition-use 边，然后把切片和上下文工具提供给 SWE-agent 设置。在 SWE-bench Lite 上，它报告 Function Recall@1 提升 17.0 点，Line Recall@1 提升 15.0 点，Pass@1 达到 22.0%，修复了 300 个问题中的 66 个。

结构化规格驱动工程（SSDE）在生成任务上提出了相关观点。它在构建 Python MVC 后端时，向 LLM 提供 Gherkin 场景、领域模型、生成的 API 签名和模板。试点结果显示，生成的签名通常比原始领域模型更有帮助：在所有测试的 LLM 中，签名把平均测试通过率提高了 7.82 个百分点，并降低了方差。失败分析也有用，因为 49.0% 的错误是不存在的 API 调用，20.2% 是类型不匹配。

#### Evidence
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): ARISE 摘要给出了仓库图设计、SWE-bench Lite 设置、定位提升和 Pass@1 结果。
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE 摘要给出了结构化输入、评估设置、测试通过率变化和失败类别。

### 程序生成正在使用搜索和累积的失败证据
ARIADNE 把竞赛编程视为固定预算下的搜索问题。它使用 Monte Carlo Tree Search（MCTS）和一个共享黑板，黑板保存约束、候选策略、生成的测试、反例、诊断和修复记录。使用 GPT-4o 时，它报告 APPS 上 Pass@1 为 41.30，CodeContests 上为 46.67，CodeContests+ 上为 27.27，LiveCodeBench 上为 20.91，高于列出的 CodeSim 基线。

这类工作把执行反馈当作可复用状态。关键细节是反馈格式：ARIADNE 结合标量奖励和结构化记录，然后把搜索预算分配给测试和修复效果更好的分支。这种设计让隐藏边界情况和失败尝试进入下一次编码决策。

#### Evidence
- [ARIADNE: Agentic Reward-Informed Adaptive Decision Exploration via Blackboard-Driven MCTS for Competitive Program Generation](../Inbox/2026-05-04--ariadne-agentic-reward-informed-adaptive-decision-exploration-via-blackboard-driven-mcts-for-competitive-program-generation.md): ARIADNE 摘要给出了 MCTS 和黑板设计、奖励结构、数据集和 Pass@1 结果。

### 功能测试不足以评估生成软件
一篇论文把评估目标扩展到可维护性。AI-generated smells 研究把 90 个 CodeContest 问题上的 LLM 输出与人类提交进行比较，然后审计了 20 个 MetaGPT 项目在需求阶段逐步增加时的表现。它报告了 Long Method、Too Many Branches、Potential Improper API Usage、Unstable Dependency 和 God Class 结构等坏味道模式。

这些证据比修复和工具调用论文更少使用数字，但警告很具体。通过测试的代码仍然可能积累维护债务，更大的生成系统需要在测试通过率之外加入静态检查。SSDE 的失败分析支持同一项工程需求：许多仓库生成错误是 API 和类型错误，静态分析可以在运行时测试之前捕获这些错误。

#### Evidence
- [AI-Generated Smells: An Analysis of Code and Architecture in LLM and Agent-Driven Development](../Inbox/2026-05-04--ai-generated-smells-an-analysis-of-code-and-architecture-in-llm-and-agent-driven-development.md): AI-generated smells 摘要给出了实验、坏味道类别，以及关于生成代码中可维护性债务的主张。
- [LLM-Assisted Repository-Level Generation with Structured Spec-Driven Engineering](../Inbox/2026-05-04--llm-assisted-repository-level-generation-with-structured-spec-driven-engineering.md): SSDE 摘要报告了静态 API 和类型错误类别，并指出超过 70% 的失败可由静态分析检测到。
