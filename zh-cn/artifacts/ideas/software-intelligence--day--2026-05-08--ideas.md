---
kind: ideas
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- formal verification
- agent governance
- repository automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/formal-verification
- topic/agent-governance
- topic/repository-automation
language_code: zh-CN
---

# 编码代理控制点

## Summary
采用编码代理的团队现在可以加入三项具体控制：针对陈旧问题的编辑前弃权检查，针对代理指令和权限的仓库配置审计，以及面向需要机器检查正确性的代码的证明专用通道。

## 针对陈旧和重复 bug 报告的编辑前弃权检查
由代理维护的问题工作流应加入一个必需的编辑前步骤：在代理修改可执行代码之前，证明报告中的 bug 仍然存在。一个低成本版本是小型测试框架，让代理复现失败，检查最近改动同一区域的提交，并在仓库已经满足该问题要求时返回带签名的“no code change”结果。

FixedBench 给出了测试这一点的具体理由。在已经修复的 SWE-bench Verified 任务中，代理仍在 35% 到 65% 的案例里做了不需要的可执行代码编辑。直接使用 “Abstain or Fix” 提示提高了部分模型的弃权率，但它也导致部分修复问题出现大量修复不足：在该设置下，GPT-5.4 mini 有 93.6% 的时间错误弃权。因此，这项检查应同时评分两类情况：正确结果是不提交补丁的陈旧报告，以及仍然需要补丁的部分修复。

首批用户是允许代理从问题队列打开或更新维护 PR 的团队。工作流改动很小：在代理推送代码 diff 之前，要求提供复现说明，以及一条说明“为什么不编辑是安全的”的路径。人工评审者仍保留合并权限，这与当前 GitHub 证据一致：在 29,585 个与 AI 代理相关的 PR 中，由代理批准的 PR 总数只有 14 个，并且每个工具都低于 0.1%。

### Evidence
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench 衡量了代理在已经修复的问题上进行不需要编辑的情况，并展示了提示在部分修复问题上的取舍。
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): 该论文把陈旧和重复的 bug 报告描述为常见的仓库情形，在这些情形下代理应该弃权。
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): 这项 PR 生命周期研究显示，在 AI 代理 PR 工作流中，人类几乎总是保留合并权限。

## 针对编码代理指令、钩子和权限的仓库配置审计
使用 Claude Code、GitHub Copilot、Cursor、Gemini、OpenAI Codex 或 AGENTS.md 的仓库应在 CI 中维护代理配置清单。清单应列出上下文文件、技能、子代理、命令、规则、设置、钩子和 MCP 连接；记录哪些文件会影响每次会话；并标记可在人工评审前运行的权限或钩子。

新的 GitHub 配置数据集显示，这已经是常见的仓库材料。该数据集在 4,738 个仓库中发现了 15,591 个配置工件，其中上下文文件出现在 4,463 个仓库中。这些文件已经不再是开发者设置中的旁注；它们是团队引导代理的方式之一。

安全研究指出了清单应优先运行的检查。子代理系统需要有边界的内存继承、按角色限定的资源访问、生命周期控制和安全的终止规则。运行时治理工作补充了一种实用的布置模型：针对被阻止操作的动作前门禁，针对高风险工具使用的动作中监控，针对轨迹审查的动作后审计，以及在策略无法自动判定时的升级路由。CI 审计可以从静态检测开始，并把高风险项目转入代理执行位置的运行时检查。

### Evidence
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): 该数据集量化了跨工具和配置机制的仓库级代理配置工件。
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): 该论文定义了上下文文件、技能、子代理、命令、规则、设置、钩子和 MCP 配置。
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): 这篇子代理安全论文识别了内存继承、资源访问、陈旧状态和终止控制漏洞。
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC 规定了代理执行中约束的运行时执行位置。

## 面向有正确性要求代码的证明专用编码通道
编写安全敏感库、解析器、支付逻辑或协议代码的团队，应把普通代码生成与证明工作分开。一个实用的起步方案是为一小组函数建立内部 Rust/Verus 通道：代理提出代码，开发者或验证人员审查规格，系统在合并前要求机器检查证明以及正向和负向测试。

VeriContest 说明了为什么范围应收窄。GPT-5.5 在自然语言到代码生成上达到 92.18% pass@1，随后在规格生成上降至 48.31%，在证明生成上降至 13.95%，在端到端验证生成上降至 5.29%。所有被评估模型的端到端结果都低于 6%。这个差距足够大，证明生成应作为单独的评审工作处理，并配有专门的失败报告，而不是藏在通过的测试套件后面作为附加项。

有用的采用测试很小：选择十个具有明确前置条件和后置条件的函数，要求 Verus 检查，并跟踪代理失败的位置：缺失规格、不完整后置条件、无效不变式或错误代码。VeriContest 使用 Post2Exe 和大型负向测试套件，也提供了一种具体模式，用于在信任薄弱规格之前发现它们。

### Evidence
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest 报告了基准组成，以及从普通代码生成到验证生成的大幅下降。
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): 该论文报告了代码、规格、证明和端到端验证生成之间的 pass@1 拆分。
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): 该内容描述了 Verus 规格、可执行 Rust 代码、循环不变式、断言和证明结构。
