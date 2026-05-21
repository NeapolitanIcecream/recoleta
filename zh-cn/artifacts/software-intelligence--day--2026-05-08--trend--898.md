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

# 代码代理正按克制、证明和代码库纪律接受评判

## Overview
代码代理研究正在用可执行检查来测试决策质量。FixedBench 衡量代理何时应保持代码不变。SWE Atlas 评估日常代码库工作。VeriContest 显示，普通代码生成仍未达到机器检查正确性的要求。

## Clusters

### 不出手与工程质量基准
FixedBench 针对常规 issue 解决评分会漏掉的一种失败模式：正确补丁已经应用后，代理仍然编辑代码。在主要的已解决设置中，代理仍在 35% 到 65% 的案例中做了不需要的可执行代码编辑。直接使用“Abstain or Fix”提示提升了一些模型的不出手率，但也导致模型在部分修复的问题上有害地不采取行动。

SWE Atlas 把评估扩展到 18 个活跃代码库中的代码库问答、测试编写和重构。它的评分细则检查暴露了功能测试通过后的质量缺口。最高的原生 scaffold 结果在 Pass@1 上仍接近 40% 出头，最佳 Pass³ 也只有 29.2，因此一致性仍是明确瓶颈。

#### Evidence
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench 设计、不出手率、提示效果，以及部分修复失败模式。
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas 任务类别、代码库范围、Pass@1 和 Pass³ 结果，以及评分细则中的质量缺口。

### 形式化验证暴露证明瓶颈
VeriContest 给代码模型设定了更严格的目标：为 946 个竞赛编程问题生成 Rust/Verus 代码、规格说明和可由机器检查的证明。该基准包含经专家验证的规格说明、被评测系统接受的 Rust 代码、已检查证明，以及大规模正向和负向测试套件。

结果把代码熟练度和经验证的正确性区分开来。GPT-5.5 在自然语言到代码生成上的 pass@1 达到 92.18%，但在规格说明生成上降至 48.31%，在证明生成上降至 13.95%，在端到端验证生成上降至 5.29%。所有被评估模型的端到端成绩都低于 6%。

#### Evidence
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest 数据集构建、任务数量、验证产物和 pass@1 结果。

### 代码库代理需要更好的动作信用和预备上下文
CLI（命令行界面）代理论文把 shell 工作视为结构化动作序列。A3 将 shell 命令解析为抽象语法树签名，在相似动作之间共享信用，并结合 σ-Reveal；σ-Reveal 会在 token 预算内选择初始文件树视图。在 ShellOps 精确匹配字符串任务上，带 σ-Reveal 的 A3 得分为 48.5%，而表中最强的非 A3 基线得分为 27.5%。

另一个 GitHub 数据集显示，团队已经在为代理准备代码库。它包含 4,738 个代码库中的 15,591 个配置产物，覆盖上下文文件、skills、subagents、commands、rules、settings、hooks 和 Model Context Protocol 配置。上下文文件在样本中占主导，共有 4,463 个代码库中的 9,470 个产物。

#### Evidence
- [Learning CLI Agents with Structured Action Credit under Selective Observation](../Inbox/2026-05-08--learning-cli-agents-with-structured-action-credit-under-selective-observation.md): A3、σ-Reveal、ShellOps 范围，以及多轮文件系统任务上的报告性能。
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): 代码库级代理配置数据集、工具覆盖范围、产物数量和机制拆分。

### 代理部署研究正在确定控制点
安全和治理论文关注执行期间约束应放置在哪里。子代理继承研究报告了多代理系统中的四类漏洞：不受限制的记忆继承、缺失的资源访问控制、异步记忆分歧，以及未经授权的跨代理终止。作者描述了针对原版 OpenClaw 的可工作概念验证漏洞利用，并检查了其他供应商的系统。

SARC 通过动作前门控、动作时监控、动作后审计和升级路由，把约束放入代理循环。在一个跨 50 个种子的合成采购任务中，它报告在精确谓词下硬约束违规为零；相对于仅使用 policy-as-code 的基线，软窗口超额减少了 89.5%。

拉取请求证据补充了操作边界。在 29,585 个与 AI 代理相关的 GitHub PR 中，某些工具的代理经常发起工作，但由代理批准的 PR 总数只有 14 个，并且每个工具都低于 0.1%。在这个数据集中，人类合并权限仍是常态。

#### Evidence
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): 子代理继承威胁模型、漏洞类别、被测试系统和漏洞利用声明。
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC 运行时控制位置和合成采购结果。
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): GitHub PR 生命周期研究、代理发起模式和人类合并权限发现。
