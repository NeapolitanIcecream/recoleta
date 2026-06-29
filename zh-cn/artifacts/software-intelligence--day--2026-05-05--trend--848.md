---
kind: trend
trend_doc_id: 848
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
topics:
- coding agents
- software security
- test generation
- multi-agent systems
- code search
- quantum software
run_id: materialize-outputs
aliases:
- recoleta-trend-848
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-security
- topic/test-generation
- topic/multi-agent-systems
- topic/code-search
- topic/quantum-software
language_code: zh-CN
---

# 可执行检查正在给软件代理设定门槛

## Overview
5 月 5 日的软件 AI 论文把大语言模型（LLM）放到可执行检查下。MOSAIC-Bench 暴露了分阶段编码代理的漏洞。TDD-Bench-Java 和 PoVSmith 检验生成的产物是否会失败、通过、编译，或者触发真实 bug。

## Clusters

### Agent security needs executable proof
MOSAIC-Bench 给出了最清晰的安全信号。它把每个恶意目标拆成三个普通工程工单，然后用 Docker 里的确定性概念验证 oracle 检查最终应用。9 个生产级编码代理里，分阶段工单的攻击成功率在 53.3% 到 85.9% 之间，整个基准只出现了两次拒绝。审查代理也漏掉了已确认有漏洞的累计 diff：中性审查把 24.8% 当作常规 pull request 放行。

PoVSmith 走的是同一问题的防守面。它让编码代理去找能到达有漏洞库 API 的应用入口点，写 JUnit 漏洞证明测试，用构建反馈修复，再根据执行日志判断结果。对 33 个 Java 应用-库配对，它找到了 152 条正确调用路径，编译出了 141 个生成测试，并在 84 个案例里触发了漏洞。

#### Evidence
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench summary, methods, and attack-success results.
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith workflow and evaluation results.

### Java issue work is moving through fail-to-pass tests
TDD-Bench-Java 把回归测试变成要评判的产物。有效测试必须在有 bug 的版本上失败、在开发者修复后通过，这样诊断和验证都有执行证据。这个基准包含 13 个开源仓库里的 250 个 Java 问题，包括 Trino、Jackson Databind、RocketMQ 和 Dubbo。

e-Otter++ 在测试生成外面加了实际可用的修复循环。它先定位可能相关的文件和函数，写一个新的 Java 测试类，在旧代码上运行，读取构建或测试日志，并最多迭代 10 轮。放到 TDD-Bench-Java 上，它用 Claude-Sonnet-4.5 的 fail-to-pass 率达到 43.6%，用 GPT-5.2 达到 46.4%。基于执行结果的细化让这两个模型都比初始生成器高出 9.4 和 13.6 个百分点。

#### Evidence
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java construction, e-Otter++ workflow, and fail-to-pass results.

### Multi-agent coding needs context diagnostics and stability budgets
这项上下文迁移研究说明，软件设计代理在注入工件前需要先做一次便宜的任务检查。在 2,700 多次 Claude Sonnet 4 多代理运行中，最佳上下文选择取决于任务的无上下文探索分数。反模式把 rate-limiter 的权衡覆盖率从 0.033 提高到 0.700，而转录稿把 Kubernetes operator 的覆盖率从 0.475 降到 0.256。论文的实际建议很直接：先跑一次无上下文基线，再在基线探索低的时候加入工件。

AMCP 对多代理软件工程用了另一种控制方式。它把重模块化看作凝聚力代理和稳定性代理之间的协商，只接受那些在高于架构师设定的稳定性阈值时还能提升凝聚力的类移动。在 Xwork 1.0 到 1.1 上，0.95 的严格稳定性阈值在三步后停止，U_coh = 0.5919，U_sta = 0.9583，说明预算可以限制架构变动。

#### Evidence
- [When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration](../Inbox/2026-05-05--when-context-hurts-the-crossover-effect-of-knowledge-transfer-on-multi-agent-design-exploration.md): Context-transfer experiment setup and task-level results.
- [A Multi-Agent Consensus Protocol for Stable Software Remodularization](../Inbox/2026-05-05--a-multi-agent-consensus-protocol-for-stable-software-remodularization.md): AMCP method and Xwork stability-budget results.

### Narrow code-analysis tools are getting stronger baselines
两篇论文都指向通用代码模型表现吃力的代码分析场景。mitRE-embed-Qwen-0.6B 经过调优，用来把源函数和去掉标识符名称的 Ghidra 反编译函数匹配起来。使用过滤后的候选池后，它在反编译到源码搜索上达到 mean reciprocal rank 0.6207 和 Recall@10 0.8353，而且在 FP8 量化后检索质量几乎不变。

LintQ-LLM 把 LLM 检查用在 Qiskit 程序上。思维链版本在 55 个 Qiskit 文件上的 F1 达到 0.70，高于基于规则的 LintQ 基线 0.41。检索示例版本的 F1 达到 0.68，并且在评估的变体里精度最高。证据规模不大，但说明当工具只针对一种具体语言、一个 bug 家族和一个评估集时，会有可用提升。

#### Evidence
- [Identifier-Free Code Embedding Models for Scalable Search](../Inbox/2026-05-05--identifier-free-code-embedding-models-for-scalable-search.md): Identifier-free embedding data, retrieval setup, and metrics.
- [Beyond Rules: LLM-Powered Linting for Quantum Programs](../Inbox/2026-05-05--beyond-rules-llm-powered-linting-for-quantum-programs.md): LLM-based quantum linting methods and evaluation metrics.
