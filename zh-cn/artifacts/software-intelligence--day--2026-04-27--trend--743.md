---
kind: trend
trend_doc_id: 743
granularity: day
period_start: '2026-04-27T00:00:00'
period_end: '2026-04-28T00:00:00'
topics:
- coding agents
- software engineering
- agent evaluation
- benchmark auditing
- repository-scale generation
- agent reliability
run_id: materialize-outputs
aliases:
- recoleta-trend-743
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/benchmark-auditing
- topic/repository-scale-generation
- topic/agent-reliability
language_code: zh-CN
---

# 编码智能体的测试开始覆盖项目规则、完整工作流和测量失效

## Overview
当天最有分量的工作把编码智能体视为必须遵守项目上下文、承受多文件工作流，并用可追踪证据测量的系统。Context-Augmented Code Generation 给出了最清晰的产品上下文结果。BenchGuard 和 TraceToChain 关注测试与可靠性声明是否可信。

## Clusters

### 项目上下文和跨文件契约
这些代码生成论文关注代码周边的决策。Context-Augmented Code Generation 报告称，在 8 个 Next.js 任务、41 个决策点上，把 Brief 加入 Claude Code 后，加权决策遵从率从 46% 提高到 95%。这个结果有用，但该设置也通过规格说明、验收标准和开发中指导改变了工作流。

这项工业 DSL 研究在代码库规模上说明了同一点。BMW 将一个 Xtext 领域特定语言项目编码为保留路径的 JSON，然后训练 7B 代码模型输出完整的多文件更新。QLoRA 微调在 105 个留出样例上达到 1.00 的结构保真度，并用开发者审查和生成器执行作为实际检查。

#### Evidence
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): 报告了决策遵从率从 46% 到 95% 的提升，以及该基准的限制。
- [Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study](../Inbox/2026-04-27--leveraging-llms-for-multi-file-dsl-code-generation-an-industrial-case-study.md): 描述了 BMW 的多文件 DSL 设置、QLoRA 微调和结构保真度结果。

### 协同的软件迁移和修复
当各阶段传递明确产物时，智能体系统表现更好。Mono2Sls 先用静态分析提取端点、调用边、异步提示和模式候选项，然后由四个智能体生成架构、Lambda 代码、AWS SAM 模板和一致性修复。在 6 个 Flask 和 Express 应用上，它报告了 100% 的部署成功率，且无需手动修复；端到端正确率为 66.1%。

FGDM 将类似的分阶段设计用于缺陷检测和修复。它把代码转换为流图，定位故障节点，修复图区域，并重建源代码。论文报告了在 100 个 BugsInPy 程序上的测试，这些程序在 Python 和 C 之间转换；相对于参考表示，Python 修复的平均余弦相似度为 0.951，C 修复为 0.974。

#### Evidence
- [Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis](../Inbox/2026-04-27--mono2sls-automated-monolith-to-serverless-migration-via-multi-stage-pipeline-with-static-analysis.md): 给出了 Mono2Sls 的阶段、基准规模、部署成功率和正确率数据。
- [FGDM: Reasoning Aware Multi-Agentic Framework for Software Bug Detection using Chain of Thought and Tree of Thought Prompting](../Inbox/2026-04-27--fgdm-reasoning-aware-multi-agentic-framework-for-software-bug-detection-using-chain-of-thought-and-tree-of-thought-prompting.md): 概述了 FGDM 的基于图的修复流程，以及报告的 Python/C 修复指标。

### 基准质量和可靠性建模
评测研究正在检查测量工具本身。BenchGuard 通过检查任务指令、参考程序、评估器和环境之间的冲突，审计基于执行的智能体基准。在 ScienceAgentBench 上，它在 102 个任务中发现 12 个经作者确认的缺陷。在 BIXBench Verified-50 上，五模型审计精确匹配了专家识别的 24 个原子问题中的 20 个。

TraceToChain 采用另一条路线。它把智能体轨迹拟合到吸收马尔可夫链，使 pass@k、重复运行失败和可靠性衰减共享同一个成功时间分布。在 7 个受控设置上，留出可靠性曲线与解析曲线匹配，最大误差为 0.053；拟合链在全部 7 个案例中都通过了报告的 KS 检验。原始 SWE-bench 和 tau-bench 轨迹验证仍留待未来工作。

#### Evidence
- [BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks](../Inbox/2026-04-27--benchguard-who-guards-the-benchmarks-automated-auditing-of-llm-agent-benchmarks.md): 提供了 BenchGuard 的审计方法，以及在 ScienceAgentBench 和 BIXBench 上的缺陷召回结果。
- [Measuring the Unmeasurable: Markov Chain Reliability for LLM Agents](../Inbox/2026-04-27--measuring-the-unmeasurable-markov-chain-reliability-for-llm-agents.md): 提供了 TraceToChain 的马尔可夫链可靠性方法和受控验证结果。

### 自主研究行为的操作性测试
两个智能体基准测试模型能否在有限指令或部分发现之后构建系统。在 AlphaZero 风格的四子棋任务中，智能体获得一个简短提示、3 小时和消费级硬件。Claude Opus 4.7 在 8 次主要试验中的 7 次里，作为先手战胜 Pascal Pons 求解器；其他受测智能体最多只赢 2 次。

SciCrafter 在 Minecraft 红石中测试发现和应用能力。最佳基线在 25 个参数化电路任务上的成功率为 26.0%。Oracle 调查提示和一个 scientist 子智能体把最高结果提高到 64.0%，但剩余差距仍然很大，说明在这个受控设置中，智能体仍难以识别并应用缺失的因果规则。

#### Evidence
- [Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline For Connect Four That Performs Comparably to an External Solver](../Inbox/2026-04-27--frontier-coding-agents-can-now-implement-an-alphazero-self-play-machine-learning-pipeline-for-connect-four-that-performs-comparably-to-an-external-solver.md): 描述了 AlphaZero 风格的四子棋基准、3 小时设置和求解器比较。
- [Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft](../Inbox/2026-04-27--can-current-agents-close-the-discovery-to-application-gap-a-case-study-in-minecraft.md): 描述了 SciCrafter 的红石任务、基线成功率和干预结果。
