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

# 编码代理正在接受项目规则、完整工作流和测量失败的检验

## Overview
当天最强的工作把代码代理当作必须遵守项目上下文、处理多文件工作流并接受可追踪证据检验的系统。Context-Augmented Code Generation 给出了最清晰的产品上下文结果。BenchGuard 和 TraceToChain 关注的是测试和可靠性声明是否可信。

## Clusters

### Project context and cross-file contracts
代码生成论文关注的是围绕代码的决策。Context-Augmented Code Generation 报告称，在 Claude Code 中加入 Brief 后，8 个 Next.js 任务、41 个决策点上的加权决策遵循率从 46% 提升到 95%。这个结果有用，但这种设置也会通过规格说明、验收标准和构建过程中的指导改变工作流。

工业 DSL 研究在仓库规模上得出了同样的结论。BMW 将一个 Xtext 领域特定语言项目编码为保留路径的 JSON，然后训练 7B 代码模型输出完整的多文件更新。QLoRA 微调在 105 个留出样本上达到了 1.00 的结构保真度，开发者审查和生成器执行被用作实际检查。

#### Evidence
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): Reports the 46% to 95% decision-compliance gain and the benchmark limits.
- [Leveraging LLMs for Multi-File DSL Code Generation: An Industrial Case Study](../Inbox/2026-04-27--leveraging-llms-for-multi-file-dsl-code-generation-an-industrial-case-study.md): Describes BMW's multi-file DSL setup, QLoRA fine-tuning, and structural fidelity result.

### Coordinated software migration and repair
当代理系统在阶段之间传递明确产物时，表现更好。Mono2Sls 先用静态分析提取端点、调用边、异步提示和模式候选项，再让四个代理生成架构、Lambda 代码、AWS SAM 模板和一致性修复。在 6 个 Flask 和 Express 应用上，它报告了 100% 的部署成功率，没有手工修复，端到端正确率为 66.1%。

FGDM 把类似的分阶段设计用于漏洞检测和修复。它将代码转成流图，定位有缺陷的节点，修复图区域，再重建源代码。论文报告了对 100 个 BugsInPy 程序的测试，这些程序被转换到 Python 和 C 中，Python 修复与参考表示的平均余弦相似度为 0.951，C 修复为 0.974。

#### Evidence
- [Mono2Sls: Automated Monolith-to-Serverless Migration via Multi-Stage Pipeline with Static Analysis](../Inbox/2026-04-27--mono2sls-automated-monolith-to-serverless-migration-via-multi-stage-pipeline-with-static-analysis.md): Gives the Mono2Sls stages, benchmark size, deployment success, and correctness figures.
- [FGDM: Reasoning Aware Multi-Agentic Framework for Software Bug Detection using Chain of Thought and Tree of Thought Prompting](../Inbox/2026-04-27--fgdm-reasoning-aware-multi-agentic-framework-for-software-bug-detection-using-chain-of-thought-and-tree-of-thought-prompting.md): Summarizes FGDM's graph-based repair pipeline and reported Python/C repair metrics.

### Benchmark quality and reliability modeling
评估工作正在检查测量工具本身。BenchGuard 通过检查任务说明、参考程序、评估器和环境之间是否冲突，来审计基于执行的代理基准。在 ScienceAgentBench 上，它发现了 102 个任务中的 12 个经作者确认的缺陷。在 BIXBench Verified-50 上，五模型审计与专家识别的 24 个原子问题中的 20 个完全一致。

TraceToChain 走的是另一条路。它把代理轨迹拟合为一个吸收马尔可夫链，让 pass@k、重复运行失败和可靠性衰减共享同一个成功时间分布。在 7 个受控设置上，留出集可靠性曲线与解析曲线的最大误差为 0.053，而且拟合后的链在 7 次试验中都通过了报告的 KS 检验。原始 SWE-bench 和 tau-bench 轨迹验证仍留待后续工作。

#### Evidence
- [BenchGuard: Who Guards the Benchmarks? Automated Auditing of LLM Agent Benchmarks](../Inbox/2026-04-27--benchguard-who-guards-the-benchmarks-automated-auditing-of-llm-agent-benchmarks.md): Provides BenchGuard's audit method and defect-recall results on ScienceAgentBench and BIXBench.
- [Measuring the Unmeasurable: Markov Chain Reliability for LLM Agents](../Inbox/2026-04-27--measuring-the-unmeasurable-markov-chain-reliability-for-llm-agents.md): Provides TraceToChain's Markov-chain reliability method and controlled validation results.

### Operational probes for autonomous research behavior
两个代理基准在测试模型能否在有限指令或部分发现后构建系统。在 AlphaZero 风格的 Connect Four 任务中，代理只拿到一个简短提示、3 小时和消费级硬件。Claude Opus 4.7 作为先手，在对 Pascal Pons 求解器的 8 次主要试验中赢了 7 次，而其他测试代理都没有超过 2 次胜利。

SciCrafter 在 Minecraft 红石中测试发现和应用能力。最好的基线在 25 个参数化电路任务上的成功率为 26.0%。Oracle 研究提示和一个 scientist 子代理把最高结果提高到 64.0%，但剩余差距仍然很大，说明在这个受控场景里，代理还是难以识别并应用缺失的因果规则。

#### Evidence
- [Frontier Coding Agents Can Now Implement an AlphaZero Self-Play Machine Learning Pipeline For Connect Four That Performs Comparably to an External Solver](../Inbox/2026-04-27--frontier-coding-agents-can-now-implement-an-alphazero-self-play-machine-learning-pipeline-for-connect-four-that-performs-comparably-to-an-external-solver.md): Describes the AlphaZero-style Connect Four benchmark, 3-hour setup, and solver comparison.
- [Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft](../Inbox/2026-04-27--can-current-agents-close-the-discovery-to-application-gap-a-case-study-in-minecraft.md): Describes SciCrafter's redstone tasks, baseline success rates, and intervention results.
