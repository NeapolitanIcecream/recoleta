---
kind: ideas
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent evaluation
- test generation
- trajectory training
- self-evolving agents
- pull requests
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/test-generation
- topic/trajectory-training
- topic/self-evolving-agents
- topic/pull-requests
language_code: zh-CN
---

# 编码代理验证轨迹

## 摘要
编码代理的采用现在需要保留结果背后证据的检查：生成测试要看突变体是否存活，拉取请求要看审查上下文和重构风险，已部署代理的源代码级更新要回放用户失败。

## 生成的问题测试的突变检查
使用编码代理写测试的团队，可以在这些测试影响补丁批准、基准分数或修复代理训练之前，加一道小型突变检查。生成的测试套件应该对原始 bug 失败，对修复通过，并能抓住由修复派生出的几个语义上合理的错误变体。

SWE-Mutation 说明了这道检查有用的原因。DeepSeek-V3.1 搭配 Mini-Swe-Agent 在 Python 测试生成上达到 88.20% 的 Pass@1，但验证率只有 10.20%，突变体检测率只有 36.15%。这些测试文件能运行，但很多并没有证明报告的问题，也没有抓住附近的错误修复。一个成本不高的试点做法，是选取最近修复过的问题，每个修复生成 3 到 5 个突变体，并在 CI 或评估运行里把 VRR 和 RDR 与 Pass@1 一起跟踪。

### 资料来源
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): SWE-Mutation defines the issue-test evaluation with Pass@1, VRR, and RDR, and reports the large gap between executable tests and useful tests.
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): The paper states the dataset size, DeepSeek-V3.1 verification and detection rates, and the drop in detection under agentic mutants.

## 带重构检查的代理拉取请求审查记录
接受代理生成拉取请求的仓库，应该把审查证据记录在和合并状态相同的位置。GitHub bot 可以附上 CI 结果、审查者评论、审查者应用的提交、关闭原因、重复或被替代的工作，以及明确的人类反馈字段。对于 Java 补丁，同样的检查还可以运行 RefactoringMiner，标记问题没有要求的纠缠式重构。

这项拉取请求研究发现，样本中的拒绝型 agentic PR 只有 35.7% 属于明确的代理失败，31.2% 来自流程约束，33.1% 没有可见理由。合并的 PR 也需要上下文：15.4% 涉及明确的审查反馈或审查者应用的提交。Refactoring Runaway 为保留这类记录补上一条补丁级理由：在有效的 Java 代理补丁中，21.43% 出现了纠缠式重构，并且与更低的可编译性相关。RefUntangle 将平均编译成功率从 19.34% 提高到 38.33%，说明对有风险的结构性修改，可以在审查前先做一次修复。

### 资料来源
- [Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study](../Inbox/2026-05-21--why-are-agentic-pull-requests-merged-or-rejected-an-empirical-study.md): The study quantifies rejected and merged agentic PRs and shows why merge status alone misreads agent performance.
- ["Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution](../Inbox/2026-05-21--refactoring-runaway-understanding-and-mitigating-tangled-refactorings-in-coding-agents-for-issue-resolution.md): The paper measures tangled refactorings in Java agent patches and reports RefUntangle’s compilation gains.

## 源代码级代理更新前的失败批次回放
运行已部署代理的团队，可以把反复出现的用户可见失败变成受控更新流程。系统记录弱对话片段或缺失对话片段，封存一个小批次，要求编码代理定位并修改源代码级故障，然后在隔离 worker 中先对候选镜像回放这批失败，再做任何生产变更。推进上线需要人工 apply 步骤、健康探针和回滚。

MOSS 给出了这个流程的具体模式。它针对路由、钩子顺序、会话状态、分发和并发中的失败，这些问题未必靠 prompt 或技能编辑就能修好。在 OpenClaw 上，一轮演化把四个任务的平均评分从 0.25 提高到 0.61，没有人工代码编辑。采用时，安全细节很关键：MOSS 在临时 trial-worker 容器中测试候选镜像，并且在推进前要求 `moss evo apply`、健康检查和回滚。

### 资料来源
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): MOSS describes failure batching, ordered repair stages, candidate-image replay, consent-gated promotion, and the OpenClaw score gain.
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): The paper states that code changes are delegated to external coding-agent CLIs and verified through replay in trial workers before promotion.
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): The paper lists harness-level failures such as routing, hooks, state management, dispatch, and session lifecycle as source-level repair targets.
