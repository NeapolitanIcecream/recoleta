---
kind: ideas
granularity: day
period_start: '2026-04-22T00:00:00'
period_end: '2026-04-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- real-world-evaluation
- agent-harness
- developer-docs
- execution-based-validation
- security-testing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/real-world-evaluation
- topic/agent-harness
- topic/developer-docs
- topic/execution-based-validation
- topic/security-testing
language_code: zh-CN
---

# Repository-Verified Agent Evaluation

## 摘要
编码代理评估正在更接近团队能在自己仓库和流水线里核实的东西。这里最可用的方向是：一份按提交关联的评分卡，用来衡量保留代码和审查阻力；一个窄范围的 `AGENTS.md` 生成流程，并和最近 PR 的回放评估绑定；以及 Node.js 安全分诊，只放行那些已经执行过概念验证利用的案例。

## Commit-linked coding-agent scorecards for kept code and review friction
使用编码代理的团队需要一份面向提交的评分卡，衡量开发者保留了什么、丢弃了什么，以及代理带来了多少审查阻力。SWE-chat 提供了最清楚的例子。大约 6,000 次真实会话里，代理写出的代码总体保留率是 50.3%，协作会话降到 44.1%。用户在 39% 的轮次里提出了反对，vibe coding 的 token 成本更高、每行提交代码耗时更长，引入的漏洞也更多。这些数字支持一个明确的产品改动：在代理日志里加入会话后的归因和提交关联，然后按代码保留率、审查返工、打断率和每行提交代码的安全发现，对提示、仓库和工作流排序。最先会用到这套东西的是那些已经为共享仓库里的编码代理付费、还在争论输出到底有没有帮助的团队。一个低成本试点是做一个 GitHub 应用或 CLI 包装器，把会话轨迹和合并后的 diff 关联起来，在正常使用一周后展示保留率和拒绝率。

### 资料来源
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): Provides real-world metrics on code survival, user pushback, cost, and vulnerability rates across coding-agent sessions.
- [SWE-chat: Coding Agent Interactions From Real Users in the Wild](../Inbox/2026-04-22--swe-chat-coding-agent-interactions-from-real-users-in-the-wild.md): Confirms the dataset scale and the focus on linking session traces to what developers actually committed.

## Task-specific AGENTS.md generation with before-and-after PR replay
一个简短、面向具体任务的 `AGENTS.md` 生成器，加上评估循环，现在对使用仓库代理的团队来说已经可做。证据足够具体，可以把文档当作性能输入来看待。在 Augment 的研究里，长度大约 100 到 150 行的优质文件带来了 10% 到 15% 的提升；一个用于新增集成的六步流程把缺失接线文件的比例从 40% 降到 10%，同时把正确性提高 25%，把完整性提高 20%。同一项研究也说明了事情有多容易做坏：偏架构的文件拉进了大约 80K 无关 token，只有警告的规则把 PR 时间拉长了一倍。这里有用的产品不是通用文档生成器，而是一个仓库扫描器，它围绕狭窄的任务类型起草 `AGENTS.md`，从本地代码库里插入决策表和小代码示例，并在最近的 PR 上运行前后任务回放。最先购买的是平台和开发效率团队，他们已经维护内部上手文档，但不知道哪些说明会被代理框架真正读到。

### 资料来源
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): Gives the main quantitative findings on helpful and harmful AGENTS.md patterns, including workflow and token-loading effects.
- [A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all](../Inbox/2026-04-22--a-good-agents-md-is-a-model-upgrade-a-bad-one-is-worse-than-no-docs-at-all.md): Details the six-step workflow result that reduced missing wiring files and improved correctness and completeness.

## Proof-of-concept exploit confirmation for Node.js dependency triage
Node.js 包安全扫描可以通过生成并执行概念验证利用，向可供分诊的输出再靠近一步。LLMVD.js 说明这件事现在已经能做。这个系统确认了 84% 的基准漏洞，明显高于摘录中的此前工具，并且在 260 个最近发布的包里为 36 个生成了经过验证的利用。它的流程和这个数字一样重要：它把候选发现、可利用性判断、约束推断和基于执行的确认分开处理，并针对路径遍历、代码注入、原型污染和命令注入使用不同的 oracle。这给注册表运营方、供应链安全厂商，以及依赖很多 npm 包的大型应用团队提供了一种可执行的工作方式改动。把利用确认放在静态怀疑之后、分析师审查之前，这样分诊一开始面对的就是已经有可复现产物的包。一个小的验证步骤，是把它跑在一套最近的内部依赖上，看看有多少扫描告警能被带运行证明的确认案例替代。

### 资料来源
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): Summarizes the execution-backed vulnerability confirmation pipeline and benchmark results.
- [Taint-Style Vulnerability Detection and Confirmation for Node.js Packages Using LLM Agent Reasoning](../Inbox/2026-04-22--taint-style-vulnerability-detection-and-confirmation-for-node-js-packages-using-llm-agent-reasoning.md): Confirms the reported 84% benchmark confirmation rate and 36 validated exploits on recent packages.
