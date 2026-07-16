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

# Coding Agent Control Points

## 摘要
采用 coding agent 的团队现在可以加上三个具体控制：针对过期问题的预编辑拒答检查、针对代理指令和权限的仓库配置审计，以及针对需要机器检查正确性的代码的证明导向通道。

## Pre-edit abstention checks for stale and duplicate bug reports
由代理维护的问题工单流程应加入一个必需的预编辑步骤，先证明所报 bug 仍然存在，再让代理改动可执行代码。一个低成本做法是用一个小型 harness，要求代理复现失败、检查同一区域的最近提交，并在仓库已经满足问题时返回一个签名的“无需改代码”结果。

FixedBench 给出了测试这一点的直接理由。在已经修复的 SWE-bench Verified 任务中，代理仍在 35% 到 65% 的案例里做出了不需要的可执行代码改动。直接使用 “Abstain or Fix” 提示词能提高部分模型的拒答率，但在部分修复问题上也会造成严重漏修，在该设置下 GPT-5.4 mini 误拒答的比例达到 93.6%。因此，这个检查应把两类情况一起计分：过期报告，正确结果是不打补丁；部分修复，仍然需要补丁。

最先会用到它的是那些让代理从问题队列里打开或更新维护类 PR 的团队。流程改动很小：在代理提交代码 diff 之前，要求一份复现说明和一条“为什么不改代码是安全的”路径。人类审阅者仍然保留合并权限，这也符合当前的 GitHub 证据：在 29,585 个与 AI 代理相关的 PR 中，代理批准的 PR 只有 14 个，并且每个工具都低于 0.1%。

### 资料来源
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench measures unwanted edits on already-fixed issues and shows the prompt tradeoff on partially fixed issues.
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): The paper frames stale and duplicate bug reports as a routine repository condition where agents should abstain.
- [Collaborator or Assistant? How AI Coding Agents Partition Work Across Pull Request Lifecycles](../Inbox/2026-05-08--collaborator-or-assistant-how-ai-coding-agents-partition-work-across-pull-request-lifecycles.md): The PR lifecycle study shows humans almost always retain merge authority in AI-agent PR workflows.

## Repository configuration audits for coding-agent instructions, hooks, and permissions
使用 Claude Code、GitHub Copilot、Cursor、Gemini、OpenAI Codex 或 AGENTS.md 的仓库，应在 CI 中维护一份代理配置清单。清单应列出上下文文件、skills、subagents、commands、rules、settings、hooks 和 MCP 连接；记录哪些文件会影响每次会话；并标出可以在人工审查前运行的权限或 hooks。

新的 GitHub 配置数据集表明，这已经是常见的仓库材料。它发现 4,738 个仓库里有 15,591 个配置工件，其中上下文文件出现在 4,463 个仓库中。这些文件不再只是开发者环境里的附注，而是团队控制代理的方式之一。

安全研究给出了清单应先运行的检查。subagent 系统需要有边界的记忆继承、按角色划分的资源访问、生命周期控制和安全终止规则。运行时治理研究补充了一种实用的放置方式：对受限操作设置 pre-action 门禁，对高风险工具使用设置 action-time 监视器，对轨迹审计设置 post-action 审核器，在策略无法自动决定时走升级路由。CI 审计可以先做静态检测，再把高风险项移到代理实际动作时的运行时检查中。

### 资料来源
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): The dataset quantifies repository-level agent configuration artifacts across tools and configuration mechanisms.
- [A Dataset of Agentic AI Coding Tool Configurations](../Inbox/2026-05-08--a-dataset-of-agentic-ai-coding-tool-configurations.md): The paper defines context files, skills, subagents, commands, rules, settings, hooks, and MCP configurations.
- [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](../Inbox/2026-05-08--when-child-inherits-modeling-and-exploiting-subagent-spawn-in-multi-agent-networks.md): The subagent security paper identifies memory inheritance, resource access, stale state, and termination-control vulnerabilities.
- [SARC: A Governance-by-Architecture Framework for Agentic AI Systems](../Inbox/2026-05-08--sarc-a-governance-by-architecture-framework-for-agentic-ai-systems.md): SARC specifies runtime enforcement sites for constraints inside agent execution.

## Proof-focused coding lanes for code with correctness obligations
编写安全敏感库、解析器、支付逻辑或协议代码的团队，应把普通代码生成和证明工作分开。一个可行的起步方案是内部 Rust/Verus 通道，只覆盖一小部分函数：代理提出代码，开发者或验证者审查规格说明，系统在合并前要求机器检查通过的证明，以及正向和反向测试。

VeriContest 说明了为什么应该把这个范围收窄。GPT-5.5 在自然语言到代码生成上的 pass@1 达到 92.18%，随后在规格生成上降到 48.31%，在证明生成上降到 13.95%，在端到端可验证生成上只有 5.29%。所有评估模型的端到端结果都低于 6%。这个差距足够大，证明生成应被当作独立的审查工作，配套单独的失败报告，而不是被藏进一个通过了测试的流程里。

一个有用的落地测试很小：选 10 个带清晰前置条件和后置条件的函数，要求 Verus 检查，并记录代理在哪一步失败：缺少规格、后置条件不完整、不变式无效，还是代码错误。VeriContest 使用的 Post2Exe 和大规模负测试集，也给出了一个具体模式，可以在弱规格被信任前把它们抓出来。

### 资料来源
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest reports the benchmark composition and the large drop from ordinary code generation to verified generation.
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): The paper reports the pass@1 split across code, specification, proof, and end-to-end verified generation.
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): The content describes Verus specifications, executable Rust code, loop invariants, assertions, and proof structure.
