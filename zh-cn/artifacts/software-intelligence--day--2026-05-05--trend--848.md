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

# 可执行检查正在为软件智能体设定标准

## Overview
5 月 5 日的软件 AI 论文把大语言模型（LLM）置于可执行检查之下。MOSAIC-Bench 暴露了分阶段编码智能体漏洞。TDD-Bench-Java 和 PoVSmith 测试生成工件是否会失败、通过、编译或触发真实缺陷。

## Clusters

### 智能体安全需要可执行证明
MOSAIC-Bench 给出了最清晰的安全信号。它把每个恶意目标拆分到三个普通工程工单中，然后在 Docker 中用确定性的概念验证 oracle 检查最终应用。在九个生产级编码智能体中，分阶段工单产生的攻击成功率为 53.3% 到 85.9%，整个基准中只有两次拒绝。审查智能体也漏掉了已确认存在漏洞的累积 diff：中性审查把 24.8% 批准为常规拉取请求。

PoVSmith 处理同一问题的防御侧。它要求编码智能体找到能到达易受攻击库 API 的应用入口点，编写 JUnit 漏洞证明测试，根据构建反馈修复测试，并判断执行日志。在 33 个 Java 应用-库配对上，它找到了 152 条正确调用路径，编译了 141 个生成测试，并在 84 个案例中触发了漏洞。

#### Evidence
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench 摘要、方法和攻击成功结果。
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith 工作流和评估结果。

### Java 问题处理正在转向 fail-to-pass 测试
TDD-Bench-Java 把复现测试作为判断对象。有效测试必须在有缺陷版本上失败，并在开发者修复后通过，这为诊断和验证提供执行证据。该基准包含来自 13 个开源仓库的 250 个 Java 问题，包括 Trino、Jackson Databind、RocketMQ 和 Dubbo。

e-Otter++ 在测试生成周围加入实用的修复循环。它定位可能相关的文件和函数，编写一个新的 Java 测试类，在旧代码上运行，读取构建或测试日志，并最多修订 10 轮。在 TDD-Bench-Java 上，它使用 Claude-Sonnet-4.5 达到 43.6% 的 fail-to-pass 率，使用 GPT-5.2 达到 46.4%。对这些模型而言，基于执行的细化比初始生成器分别提高了 9.4 和 13.6 个百分点。

#### Evidence
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java 构建、e-Otter++ 工作流和 fail-to-pass 结果。

### 多智能体编码需要上下文诊断和稳定性预算
上下文迁移研究表明，软件设计智能体在注入工件前需要一次低成本任务检查。在 2,700 多次 Claude Sonnet 4 多智能体运行中，最佳上下文选择取决于任务的无上下文探索分数。反模式把限流器权衡覆盖率从 0.033 提高到 0.700，而转录记录把 Kubernetes operator 覆盖率从 0.475 降到 0.256。论文给出的实用建议很简单：先运行无上下文基线，然后在基线探索较低时加入工件。

AMCP 对多智能体软件工程使用另一种控制方式。它把重新模块化视为内聚性智能体和稳定性智能体之间的协商，只接受能提高内聚性且保持在架构师设定稳定性阈值以上的类移动。在 Xwork 1.0 到 1.1 上，0.95 的严格稳定性阈值在三步后停止，U_coh = 0.5919，U_sta = 0.9583，说明该预算可以限制架构变动。

#### Evidence
- [When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration](../Inbox/2026-05-05--when-context-hurts-the-crossover-effect-of-knowledge-transfer-on-multi-agent-design-exploration.md): 上下文迁移实验设置和任务级结果。
- [A Multi-Agent Consensus Protocol for Stable Software Remodularization](../Inbox/2026-05-05--a-multi-agent-consensus-protocol-for-stable-software-remodularization.md): AMCP 方法和 Xwork 稳定性预算结果。

### 窄域代码分析工具正在形成更强的基线
两篇论文面向通用代码模型表现吃力的代码分析场景。mitRE-embed-Qwen-0.6B 被调优为匹配源函数和剥离标识符后的 Ghidra 反编译函数，此时有用的标识符名称缺失。在过滤后的候选池中，它在反编译到源码搜索上达到平均倒数排名 0.6207 和 Recall@10 0.8353，并在 FP8 量化后保持接近相同的检索质量。

LintQ-LLM 把 LLM 检查用于 Qiskit 程序。chain-of-thought 版本在 55 个 Qiskit 文件上达到 F1 = 0.70，高于基于规则的 LintQ 基线 0.41。检索示例版本达到 F1 = 0.68，并在已评估变体中取得最高精确率。证据规模较小，但它显示，当工具范围限定在具体语言、缺陷类别和评估集时，可以获得有用提升。

#### Evidence
- [Identifier-Free Code Embedding Models for Scalable Search](../Inbox/2026-05-05--identifier-free-code-embedding-models-for-scalable-search.md): 无标识符嵌入数据、检索设置和指标。
- [Beyond Rules: LLM-Powered Linting for Quantum Programs](../Inbox/2026-05-05--beyond-rules-llm-powered-linting-for-quantum-programs.md): 基于 LLM 的量子 linting 方法和评估指标。
