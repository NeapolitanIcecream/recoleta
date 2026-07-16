---
kind: trend
trend_doc_id: 898
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- formal verification
- agent governance
- repository automation
run_id: materialize-outputs
aliases:
- recoleta-trend-898
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/formal-verification
- topic/agent-governance
- topic/repository-automation
language_code: zh-CN
---

# 编码代理正在接受克制、证明和仓库纪律的评判

## 概览
编码代理研究正在用可执行检查来测试决策质量。FixedBench 测量代理什么时候应该保持代码不变。SWE Atlas 评测日常仓库工作。VeriContest 表明，普通代码生成离机器检查过的正确性还有差距。

## 研究发现

### Abstention and engineering-quality benchmarks
FixedBench 盯住了常规 issue-resolution 分数看不到的一种失败模式：代理在正确补丁已经应用后，仍然继续改代码。在主要的 resolved 设置里，代理仍然在 35% 到 65% 的案例中做出了不该有的可执行代码修改。直接使用 “Abstain or Fix” 提示词能让一些模型更愿意放弃操作，但也会让部分已修复问题上出现有害的不作为。

SWE Atlas 把评测范围扩展到代码库问答、编写测试和重构，覆盖 18 个活跃仓库。它的 rubric 检查会在功能测试通过后暴露质量缺口。最好的原生脚手架结果在 Pass@1 上仍停留在 40 多分，最佳 Pass³ 也只有 29.2，所以一致性仍然是明确瓶颈。

#### 资料来源
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench design, abstention rates, prompt effects, and partial-fix failure mode.
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas task categories, repository scope, Pass@1 and Pass³ results, and rubric-quality gaps.

### Formal verification exposes the proof bottleneck
VeriContest 给代码模型设了更严格的目标：为 946 个竞赛编程问题生成 Rust/Verus 代码、规格说明和可由机器检查的证明。这个基准包含专家验证的规格说明、评测器接受的 Rust 代码、已检查的证明，以及大规模正负样例测试集。

结果把代码流畅度和经过验证的正确性分开了。GPT-5.5 在自然语言到代码生成上达到 92.18% pass@1，随后在规格生成上降到 48.31%，在证明生成上降到 13.95%，在端到端验证生成上只有 5.29%。所有评测模型的端到端结果都低于 6%。

#### 资料来源
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest dataset construction, task counts, verification artifacts, and pass@1 results.

### Repository agents need better action credit and prepared context
CLI（command-line interface）代理论文把 shell 工作看成一串结构化动作。A3 会把 shell 命令解析成抽象语法树签名，在相似动作之间分配 credit，并与 σ-Reveal 结合，由后者在 token 预算内选出初始文件树视图。在 ShellOps 的精确匹配字符串任务上，A3 加 σ-Reveal 得到 48.5%，而表里最强的非 A3 基线是 27.5%。

另一份 GitHub 数据集展示了团队已经如何为代理准备仓库。它包含 4,738 个仓库中的 15,591 个配置工件，覆盖 context files、skills、subagents、commands、rules、settings、hooks 和 Model Context Protocol 配置。样本里 context files 最多，有 4,463 个仓库中的 9,470 个工件。

#### 资料来源
- [Learning CLI Agents with Structured Action Credit under Selective Observation](../Inbox/2026-05-08--learning-cli-agents-with-structured-action-credit-under-selective-observation.md): A3, σ-Reveal, ShellOps scope, and reported performance on multi-turn filesystem tasks.
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): Repository-level agent configuration dataset, tool coverage, artifact counts, and mechanism breakdown.

### Agent deployment research is pinning down control points
安全和治理论文关注约束在执行过程中应放在哪里。subagent-inheritance 研究报告了多代理系统中的四类漏洞：不受限制的内存继承、缺失的资源访问控制、异步内存分歧，以及未经授权的跨代理终止。作者描述了针对原版 OpenClaw 的可运行概念验证利用，以及在其他厂商系统上的检查结果。

SARC 把约束放进代理循环内部，通过行动前闸门、行动时监控、行动后审计和升级路由来控制。在一个 50 个随机种子的合成采购任务中，它在精确谓词下报告了零个硬约束违规，并且相对仅使用 policy-as-code 的基线，将软窗口超限减少了 89.5%。

拉取请求数据给出了一个操作边界。在 29,585 个与 AI 代理相关的 GitHub PR 中，代理对某些工具常常会先发起工作，但被代理批准的 PR 只有 14 个，每种工具都低于 0.1%。在人类合并权限仍然是这个数据集里的常态。

#### 资料来源
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): Subagent inheritance threat model, vulnerability classes, tested systems, and exploit claims.
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC runtime control sites and synthetic procurement results.
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): GitHub PR lifecycle study, agent initiation patterns, and human merge authority findings.
